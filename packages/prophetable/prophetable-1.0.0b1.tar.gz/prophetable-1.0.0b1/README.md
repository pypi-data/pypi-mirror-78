# Prophetable

![image](https://raw.githubusercontent.com/jucyai/prophetable/dev/prophetable.png)

Define and run Prophet forecasting models using just a configuration file.

`Prophet` is a python library from Facebook for forecasting time series data. Using `Prophetable`,
you can define a forecasting model by specifying parameters in a configurations file (`json`) or a
config object (`dict`).

## Configuring a model

Example data and configuration files are include in the `data` directory of this project. See
[configurations](https://github.com/jucyai/prophetable/blob/master/doc/configurations.md) for a full list of
configurations and their descriptions.

A minimal configuration looks like this:

In a `data/config.minimal.json` file:

```json
{
  "data_uri": "/data/example_wp_log_peyton_manning.csv"
}
```

or in your `Python` code:

```python
config = {
    'data_uri': '/data/example_wp_log_peyton_manning.csv'
}
```

Full list of configurations:

```json
{
  "data_uri": "/data/example_wp_log_peyton_manning.csv",
  "train_uri": "/data/models/full/train.csv",
  "output_uri": "/data/models/full/output.csv",
  "model_uri": "/data/models/full/model.pickle",
  "holidays_input_uri": null,
  "holidays_output_uri": null,
  "delimiter": ",",
  "ds": "ds",
  "y": "y",
  "ts_frequency": "D",
  "min_train_date": null,
  "max_train_date": null,
  "saturating_min": null,
  "saturating_max": null,
  "na_fill": null,
  "random_seed": 1234,
  "country_holidays": null,
  "custom_seasonalities": null,
  "outliers": null,
  "cv": null,
  "growth": "linear",
  "changepoints": null,
  "n_changepoints": 25,
  "changepoint_range": 0.8,
  "yearly_seasonality": "auto",
  "weekly_seasonality": "auto",
  "daily_seasonality": "auto",
  "holidays": null,
  "seasonality_mode": "additive",
  "seasonality_prior_scale": 10.0,
  "holidays_prior_scale": 10.0,
  "changepoint_prior_scale": 0.05,
  "mcmc_samples": 0,
  "interval_width": 0.8,
  "uncertainty_samples": 1000,
  "stan_backend": null
}
```

## Using the `Python` package

### Install the package

```sh
pip install prophetable
```

### Run a model with minimal configuration (defaults)

```python
from prophetable import Prophetable

# reading from a json file
p = Prophetable(config='/data/config.minimal.json')
# or a config dictionary
p = Prophetable(config={'data_uri': '/data/example_wp_log_peyton_manning.csv'})

p.run()
```

## Using Docker

Using the setup in this project, you can either use the released version on `pypi` (with
`docker/Dockerfile`) or use the development version by installing from `setup.py` (with
`Dockerfile.dev`).

Example usage `docker-run.sh`:

```sh
# git clone https://github.com/jucyai/prophetable.git
# cd prophetable

export $(egrep -v '^#' .env | xargs)

docker build --tag prophetable --file docker/Dockerfile.dev . && \
    docker run --rm \
    -v $VOLUME:/data \
    --env-file .env \
    --name=pm \
    prophetable
```

Here we used an `.env` file in the roor diretory for specifying credentials and local path variables

```sh
VOLUME='path/to/data/'
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
```

### Cleanup Docker

```sh
docker stop pm
docker rm pm
```

### Developing and Testing

See `DEVELOPMENT.md` for details.

## TODO

- Add advanced config for seasonalities that depend on other factors.
- Add advanced config for additional regressors.
