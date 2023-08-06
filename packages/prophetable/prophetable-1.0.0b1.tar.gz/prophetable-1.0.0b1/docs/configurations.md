# Prophetable configurations

## File related

- data_uri: URI for input data, required.
- train_uri: URI for training data, if saving is needed.
- output_uri: URI for forecast output, if saving is needed.
- model_uri: URI for model object, if saving is needed.
- holiday_input_uri: URI for holidays input data in csv, if provided, as opposed to
`holidays` config in Prophet parameters. THis takes priority over `holidays`
config.
- holiday_output_uri: URI for holidays output data in csv, if saving is needed.
- delimiter: The delimiler for input data.

## Model related

- min_train_date: Start date for training data.
- max_train_date: End date for training data.
- saturating_min: Maps to `floor` column in Prophet training data.
- saturating_max: Maps to `cap` column in Prophet training data.
- random_seed: Random seed for reproducibility.
- country_holidays: Name of the country, like 'UnitedStates' or 'US'. Built-in country
- holidays can only be set for a single country.
- custom_seasonalities: A list of dictionary including:
- name: string name of the seasonality component.
- period: float number of days in one period.
- fourier_order: int number of Fourier components to use.
- prior_scale: optional float prior scale for this component.
- mode: optional 'additive' or 'multiplicative'
- condition_name: string name of the seasonality condition.
- outliers: list of dates or date ranges (outliers) to remove from training.
- cv:  A dictionary of cross validation configurations, will force `ts_frequency` if
unit is not included in the string.
    - horizon: string with pd.Timedelta compatible style, e.g., '5 days', '3 hours',
    '10 seconds'.
    - period: Not required, string with pd.Timedelta compatible style. Simulated
    forecast will be  done at every this period. If not provided, 0.5 * horizon
    is used.
    - initial: Not required, string with pd.Timedelta compatible style. The first
    training period will begin here. If not provided, 3 * horizon is used.
    - rolling_window: Proportion of data to use in each rolling window for computing
    the metrics. Should be in [0, 1] to average. If rolling_window < 0, then
    metrics are computed at each datapoint with no averaging (i.e., 'mse' will
    actually be squared error with no mean).
    - metrics: one or more of ['mse', 'rmse', 'mae', 'mape', 'mdape', 'coverage'].
    Default None and use all.
- cv_output_uri: save the cv forecast (csv), if provided.
- cv_metrics_uri: save the performance metrics (csv), if provided.

## Mapped directly from Prophet forecaster

- growth: String 'linear' or 'logistic' to specify a linear or logistic trend.
changepoints: List of dates at which to include potential changepoints. If not
specified, potential changepoints are selected automatically.
- n_changepoints: Number of potential changepoints to include. Not used if input
`changepoints` is supplied. If `changepoints` is not supplied, then
n_changepoints potential changepoints are selected uniformly from the first
`changepoint_range` proportion of the history.
Example: ['2014-01-01', '2014-01-03']
- changepoint_range: Proportion of history in which trend changepoints will be
estimated. Defaults to 0.8 for the first 80%. Not used if `changepoints` is
specified.
- yearly_seasonality: Fit yearly seasonality. Can be 'auto', True, False, or a number
of Fourier terms to generate.
- weekly_seasonality: Fit weekly seasonality. Can be 'auto', True, False, or a number
of Fourier terms to generate.
- daily_seasonality: Fit daily seasonality. Can be 'auto', True, False, or a number of
Fourier terms to generate.
- holidays: pd.DataFrame with columns holiday (string) and ds (date type) and
optionally columns lower_window and upper_window which specify a range of days
around the date to be included as holidays. lower_window=-2 will include 2 days
prior to the date as holidays. Also optionally can have a column prior_scale
specifying the prior scale for that holiday.
- seasonality_mode: 'additive' (default) or 'multiplicative'.
- seasonality_prior_scale: Parameter modulating the strength of the seasonality model.
Larger values allow the model to fit larger seasonal fluctuations, smaller
values dampen the seasonality. Can be specified for individual seasonalities
using add_seasonality.
- holidays_prior_scale: Parameter modulating the strength of the holiday components
model, unless overridden in the holidays input.
- changepoint_prior_scale: Parameter modulating the flexibility of the automatic
changepoint selection. Large values will allow many changepoints, small values
will allow few changepoints.
- mcmc_samples: Integer, if greater than 0, will do full Bayesian inference with the
specified number of MCMC samples. If 0, will do MAP estimation.
- interval_width: Float, width of the uncertainty intervals provided for the forecast.
If mcmc_samples=0, this will be only the uncertainty in the trend using the MAP
estimate of the extrapolated generative model. If mcmc.samples>0, this will be
integrated over all model parameters, which will include uncertainty in
seasonality.
- uncertainty_samples: Number of simulated draws used to estimate uncertainty
intervals. Settings this value to 0 or False will disable uncertainty estimation
and speed up the calculation. uncertainty intervals.
- stan_backend: str as defined in StanBackendEnum default: None - will try to iterate
over all available backends and find the working one

## Prediction related

- future_periods: number of future periods to predict
