import os
import json
import pickle
import pathlib
from urllib.parse import urlparse
from typing import Tuple, Dict, Union

import numpy as np
import pandas as pd
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from red_panda.red_panda import S3Utils

import logging

LOGGER = logging.getLogger(__name__)


def _create_parent_dir(full: str):
    """Creates parent path given a full uri."""
    dir_parts = pathlib.PurePath(full).parts[:-1]
    if len(dir_parts) > 0:
        path = pathlib.Path(*dir_parts)
        path.mkdir(parents=True, exist_ok=True)
        LOGGER.info(f"Created path: {path}")


def _split_s3_uri(uri: str) -> Tuple[str, str, str]:
    """Get S3, bucket, key from uri."""
    parsed = urlparse(uri, allow_fragments=False)
    return (parsed.scheme, parsed.netloc, parsed.path.lstrip("/"))


class Prophetable:
    """Wrapping `fbprophet.Prophet`.

    Args:
        config: Config file or `dict`.
            # Prophetable config:
                # File related
                data_uri: URI for input data, required.
                train_uri: URI for training data, if saving is needed.
                output_uri: URI for forecast output, if saving is needed.
                model_uri: URI for model object, if saving is needed.
                holiday_input_uri: URI for holidays input data in csv, if provided, as opposed to 
                    `holidays` config in Prophet parameters. THis takes priority over `holidays` 
                    config.
                holiday_output_uri: URI for holidays output data in csv, if saving is needed.
                delimiter: The delimiler for input data.

                # Model related
                min_train_date: Start date for training data.
                max_train_date: End date for training data.
                saturating_min: Maps to `floor` column in Prophet training data.
                saturating_max: Maps to `cap` column in Prophet training data.
                random_seed: Random seed for reproducibility.
                country_holidays: Name of the country, like 'UnitedStates' or 'US'. Built-in country
                    holidays can only be set for a single country.
                custom_seasonalities: A list of dictionary including:
                    name: string name of the seasonality component.
                    period: float number of days in one period.
                    fourier_order: int number of Fourier components to use.
                    prior_scale: optional float prior scale for this component.
                    mode: optional 'additive' or 'multiplicative'
                    condition_name: string name of the seasonality condition.
                outliers: list of dates or date ranges (outliers) to remove from training.
                cv:  A dictionary of cross validation configurations, will force `ts_frequency` if
                    unit is not included in the string.
                    horizon: string with pd.Timedelta compatible style, e.g., '5 days', '3 hours', 
                        '10 seconds'.
                    period: Not required, string with pd.Timedelta compatible style. Simulated 
                        forecast will be  done at every this period. If not provided, 0.5 * horizon 
                        is used.
                    initial: Not required, string with pd.Timedelta compatible style. The first 
                        training period will begin here. If not provided, 3 * horizon is used.
                    rolling_window: Proportion of data to use in each rolling window for computing 
                        the metrics. Should be in [0, 1] to average. If rolling_window < 0, then 
                        metrics are computed at each datapoint with no averaging (i.e., 'mse' will 
                        actually be squared error with no mean).
                    metrics: one or more of ['mse', 'rmse', 'mae', 'mape', 'mdape', 'coverage'].
                        Default None and use all.
                cv_output_uri: save the cv forecast (csv), if provided.
                cv_metrics_uri: save the performance metrics (csv), if provided.

            # Mapped directly from Prophet forecaster
                growth: String 'linear' or 'logistic' to specify a linear or logistic trend.
                changepoints: List of dates at which to include potential changepoints. If not 
                    specified, potential changepoints are selected automatically.
                n_changepoints: Number of potential changepoints to include. Not used if input 
                    `changepoints` is supplied. If `changepoints` is not supplied, then 
                    n_changepoints potential changepoints are selected uniformly from the first 
                    `changepoint_range` proportion of the history. 
                    Example: ['2014-01-01', '2014-01-03']
                changepoint_range: Proportion of history in which trend changepoints will be 
                    estimated. Defaults to 0.8 for the first 80%. Not used if `changepoints` is 
                    specified.
                yearly_seasonality: Fit yearly seasonality. Can be 'auto', True, False, or a number
                    of Fourier terms to generate.
                weekly_seasonality: Fit weekly seasonality. Can be 'auto', True, False, or a number 
                    of Fourier terms to generate.
                daily_seasonality: Fit daily seasonality. Can be 'auto', True, False, or a number of
                    Fourier terms to generate.
                holidays: pd.DataFrame with columns holiday (string) and ds (date type) and 
                    optionally columns lower_window and upper_window which specify a range of days 
                    around the date to be included as holidays. lower_window=-2 will include 2 days 
                    prior to the date as holidays. Also optionally can have a column prior_scale 
                    specifying the prior scale for that holiday.
                seasonality_mode: 'additive' (default) or 'multiplicative'.
                seasonality_prior_scale: Parameter modulating the strength of the seasonality model.
                    Larger values allow the model to fit larger seasonal fluctuations, smaller
                    values dampen the seasonality. Can be specified for individual seasonalities 
                    using add_seasonality.
                holidays_prior_scale: Parameter modulating the strength of the holiday components 
                    model, unless overridden in the holidays input.
                changepoint_prior_scale: Parameter modulating the flexibility of the automatic 
                    changepoint selection. Large values will allow many changepoints, small values 
                    will allow few changepoints.
                mcmc_samples: Integer, if greater than 0, will do full Bayesian inference with the 
                    specified number of MCMC samples. If 0, will do MAP estimation.
                interval_width: Float, width of the uncertainty intervals provided for the forecast.
                    If mcmc_samples=0, this will be only the uncertainty in the trend using the MAP 
                    estimate of the extrapolated generative model. If mcmc.samples>0, this will be 
                    integrated over all model parameters, which will include uncertainty in 
                    seasonality.
                uncertainty_samples: Number of simulated draws used to estimate uncertainty 
                    intervals. Settings this value to 0 or False will disable uncertainty estimation
                    and speed up the calculation. uncertainty intervals.
                stan_backend: str as defined in StanBackendEnum default: None - will try to iterate 
                    over all available backends and find the working one
                
            # Prediction related
                future_periods: number of future periods to predict
    """

    def __init__(self, config: Union[str, dict]):

        self._storages: Dict[str, Dict[str, Union[bool, str]]] = {
            "data_uri": {"required": True},
            "train_uri": {"required": False},
            "output_uri": {"required": False},
            "model_uri": {"required": False},
            "holidays_input_uri": {"required": False},
            "holidays_output_uri": {"required": False},
            "cv_output_uri": {"required": False},
            "cv_metrics_uri": {"required": False},
        }

        if isinstance(config, dict):
            self._config = config
        else:
            with open(config, "r") as f:
                self._config = json.load(f)

        ## File uri
        for attr, setting in self._storages.items():
            # Set class property
            self._get_config(attr, required=setting["required"])
            # Identify storage scheme
            uri = getattr(self, attr)
            if uri is not None:
                scheme, _, _ = _split_s3_uri(uri)
                self._storages[attr]["scheme"] = scheme if scheme != "" else "local"

        self._aws = {
            "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        }

        ## Other file related config
        self._get_config("delimiter", default=",", required=False)

        ## Model related config
        self._get_config("ds", default="ds", required=False)
        self._get_config("y", default="y", required=False)
        self._get_config("ts_frequency", default="D", required=False)
        # Modified in make_data()
        self._get_config("min_train_date", default=None, required=False)
        # Modified in make_data()
        self._get_config("max_train_date", default=None, required=False)
        self._get_config(
            "saturating_min", default=None, required=False, type_check=[int, float]
        )
        self._get_config(
            "saturating_max", default=None, required=False, type_check=[int, float]
        )
        # Set the default na_fill to None
        # https://facebook.github.io/prophet/docs/outliers.html
        # Prophet has no problem with missing data. If you set their values to NA in the history but
        # leave the dates in future, then Prophet will give you a prediction for their values.
        self._get_config(
            "na_fill", default=None, required=False, type_check=[int, float]
        )
        self._get_config("random_seed", default=None, required=False, type_check=[int])
        self._get_config(
            "country_holidays", default=None, required=False, type_check=[str]
        )
        self._get_config(
            "custom_seasonalities", default=None, required=False, type_check=[list]
        )
        self._get_config("outliers", default=None, required=False, type_check=[list])
        self._get_config("cv", default=None, required=False, type_check=[dict])

        ## Mapped directly for Prophet
        self._get_config("growth", default="linear", required=False, type_check=[str])
        self._get_config(
            "changepoints", default=None, required=False, type_check=[list]
        )
        self._get_config("n_changepoints", default=25, required=False, type_check=[int])
        self._get_config(
            "changepoint_range", default=0.8, required=False, type_check=[float, int]
        )
        self._get_config("yearly_seasonality", default="auto", required=False)
        self._get_config("weekly_seasonality", default="auto", required=False)
        self._get_config("daily_seasonality", default="auto", required=False)
        self._get_config("holidays", default=None, required=False, type_check=[list])
        self._get_config(
            "seasonality_mode", default="additive", required=False, type_check=[str]
        )
        self._get_config(
            "seasonality_prior_scale",
            default=10.0,
            required=False,
            type_check=[float, int],
        )
        self._get_config(
            "holidays_prior_scale",
            default=10.0,
            required=False,
            type_check=[float, int],
        )
        self._get_config(
            "changepoint_prior_scale",
            default=0.05,
            required=False,
            type_check=[float, int],
        )
        self._get_config("mcmc_samples", default=0, required=False, type_check=[int])
        self._get_config(
            "interval_width", default=0.8, required=False, type_check=[float]
        )
        self._get_config(
            "uncertainty_samples", default=1000, required=False, type_check=[int]
        )
        self._get_config("stan_backend", default=None, required=False, type_check=[str])

        ## Prediction
        self._get_config(
            "future_periods", default=365, required=False, type_check=[int]
        )

        ## Placeholder for other attributes set later
        self.data = None
        self.holidays_data = None
        self.model = None
        self.forecast = None
        self.cv_data = None
        self.cv_metrics = None

        ## Seed
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

    def __getattr__(self, attr):
        return None

    def _get_config(self, attr, required=True, default=None, type_check=None):
        try:
            set_attr = self._config[attr]
            if type_check is not None and set_attr is not None:
                if not isinstance(set_attr, tuple(type_check)):
                    raise TypeError(f"{attr} provided is not {type_check}")
        except KeyError:
            if required:
                raise ValueError(f"{attr} must be provided in config")
            else:
                set_attr = default
        setattr(self, attr, set_attr)
        LOGGER.info(f"{attr} set to {set_attr}")

    def _get_timedelta(self, time_str):
        if isinstance(time_str, (float, int)):
            return pd.to_timedelta(time_str, unit=self.ts_frequency or "ns")
        else:
            return time_str

    def save(self, obj, name, ftype="csv"):
        if self._storages[name]["scheme"] == "local":
            _create_parent_dir(getattr(self, name))
            if ftype == "pickle":
                with open(getattr(self, name), "wb") as f:
                    pickle.dump(obj, f)
            elif ftype == "csv":
                obj.to_csv(getattr(self, name), index=False)
        elif self._storages[name]["scheme"] == "s3":
            _, bucket, key = _split_s3_uri(getattr(self, name))
            if ftype == "pickle":
                S3Utils(aws_config=self._aws).get_s3_client().put_object(
                    Bucket=bucket, Key=key, Body=pickle.dumps(obj)
                )
            elif ftype == "csv":
                S3Utils(aws_config=self._aws).df_to_s3(obj, bucket, key, index=False)

    def load(self, name, ftype="csv"):
        if self._storages[name]["scheme"] == "local":
            if ftype == "pickle":
                with open(getattr(self, name), "rb") as f:
                    return pickle.load(f)
            elif ftype == "csv":
                return pd.read_csv(getattr(self, name), sep=self.delimiter or ",")
        elif self._storages[name]["scheme"] == "s3":
            _, bucket, key = _split_s3_uri(getattr(self, name))
            if ftype == "pickle":
                return pickle.loads(
                    S3Utils(aws_config=self._aws)
                    .get_s3_client()
                    .get_object(bucket, key)["Body"]
                    .read()
                )
            elif ftype == "csv":
                return S3Utils(aws_config=self._aws).s3_to_df(bucket, key, index=False)

    def make_holidays_data(self):
        if self.holidays_input_uri is not None:
            self.holidays_data = self.load("holidays_input_uri")
            LOGGER.info(f"Add custom holidays from {self.holidays_input_uri}")
        else:
            if self.holidays is not None:
                holidays = self.holidays
                for i, h in enumerate(holidays):
                    holidays[i]["ds"] = pd.to_datetime(h["ds"])
                    holidays[i] = pd.DataFrame(holidays[i])
                self.holidays_data = pd.concat(holidays)
                LOGGER.info(f"Add custom holidays {self.holidays}")
        if self.holidays_output_uri is not None:
            if self.holidays_data is not None:
                self.save(self.holidays_data, "holidays_output_uri")
                LOGGER.info(f"Holidays data saved to {self.holidays_output_uri}")
            else:
                LOGGER.warning(f"No holidays data to save")

    def make_data(self):
        self.data = self.load("data_uri")
        self.data[self.ds] = pd.to_datetime(
            self.data[self.ds], infer_datetime_format=True
        )
        if self.min_train_date is None:
            self.min_train_date = self.data[self.ds].min()
        if self.max_train_date is None:
            self.max_train_date = self.data[self.ds].max()
        model_data = pd.DataFrame(
            {
                "ds": pd.date_range(
                    self.min_train_date, self.max_train_date, freq=self.ts_frequency
                )
            }
        )
        model_data = model_data.merge(
            self.data[[self.ds, self.y]], left_on="ds", right_on=self.ds, how="left"
        )
        if self.ds != "ds":
            model_data = model_data.drop(columns=[self.ds])
        model_data = model_data.rename(columns={self.y: "y"})

        # TODO: More ways to handle missing data
        if self.na_fill is not None:
            model_data = model_data.fillna(self.na_fill)

        # Additional data processing instructed in config
        if self.saturating_min is not None:
            model_data["floor"] = self.saturating_min
        if self.saturating_max is not None:
            model_data["cap"] = self.saturating_max
        if self.outliers is not None:
            for o in self.outliers:
                if isinstance(o, list):
                    if len(o) != 2:
                        raise ValueError(
                            f"Length of data range config in outliers should be 2"
                        )
                    start, end = o
                    model_data.loc[
                        (
                            model_data["ds"]
                            >= pd.to_datetime(start, infer_datetime_format=True)
                        )
                        & (
                            model_data["ds"]
                            <= pd.to_datetime(end, infer_datetime_format=True)
                        ),
                        "y",
                    ] = None
                else:
                    model_data.loc[
                        model_data["ds"]
                        == pd.to_datetime(o, infer_datetime_format=True),
                        "y",
                    ] = None

        if self.train_uri is not None:
            self.save(model_data, "train_uri")
            LOGGER.info(f"Training data saved to {self.train_uri}")
        self.data = model_data

    def cross_validation(self):
        if self.cv is None:
            LOGGER.info("Cross validation not configured, skipping")
            return None
        try:
            horizon = self._get_timedelta(self.cv["horizon"])
            period = self._get_timedelta(self.cv.get("period"))
            initial = self._get_timedelta(self.cv.get("initial"))
        except KeyError:
            raise ValueError("Horizon is the required config for cross validation")
        self.cv_data = cross_validation(
            self.model, horizon=horizon, period=period, initial=initial
        )
        if self.cv_output_uri is not None:
            self.save(self.cv_data, "cv_output_uri")
            LOGGER.info(f"Cross validation data saved to {self.cv_output_uri}")
        rolling_window = self.cv.get("rolling_window") or 0.1
        metrics = self.cv.get("metrics")
        self.cv_metrics = performance_metrics(
            self.cv_data, rolling_window=rolling_window, metrics=metrics
        )
        if self.cv_metrics_uri is not None:
            self.save(self.cv_metrics, "cv_metrics_uri")
            LOGGER.info(f"Cross validation metrics saved to {self.cv_metrics_uri}")

    def train(self):
        """Method to train Prophet forecaster
        """
        model = Prophet(
            growth=self.growth,
            changepoints=self.changepoints,
            n_changepoints=self.n_changepoints,
            changepoint_range=self.changepoint_range,
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
            # holidays is not used directly from config, it's processed in make_holidays_data
            holidays=self.holidays_data,
            seasonality_mode=self.seasonality_mode,
            seasonality_prior_scale=self.seasonality_prior_scale,
            holidays_prior_scale=self.holidays_prior_scale,
            changepoint_prior_scale=self.changepoint_prior_scale,
            mcmc_samples=self.mcmc_samples,
            interval_width=self.interval_width,
            uncertainty_samples=self.uncertainty_samples,
            stan_backend=self.stan_backend,
        )

        if self.country_holidays is not None:
            model.add_country_holidays(country_name=self.country_holidays)
            LOGGER.info(f"Add built-in country holidays {self.country_holidays}")

        if self.custom_seasonalities is not None:
            kwargs = [
                "name",
                "period",
                "fourier_order",
                "prior_scale",
                "mode",
                "condition_name",
            ]
            for s in self.custom_seasonalities:
                model.add_seasonality(**{k: v for k, v in s.items() if k in kwargs})
            LOGGER.info(f"Add custom seasonalities {self.custom_seasonalities}")

        model.fit(self.data)

        if self.model_uri is not None:
            self.save(model, "model_uri", ftype="pickle")
            LOGGER.info(f"Model object saved to {self.model_uri}")

        self.model = model

    def predict(self):
        future = self.model.make_future_dataframe(
            periods=self.future_periods, freq=self.ts_frequency
        )
        forecast = self.model.predict(future)
        if self.output_uri is not None:
            self.save(forecast, "output_uri")
            LOGGER.info(f"Forecast output saved to {self.output_uri}")
        self.forecast = forecast

    def run(self):
        self.make_holidays_data()
        self.make_data()
        self.train()
        self.cross_validation()
        self.predict()
