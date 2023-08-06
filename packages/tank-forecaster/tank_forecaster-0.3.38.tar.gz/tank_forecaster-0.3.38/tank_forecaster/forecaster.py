from datetime import datetime, timedelta
from sparkles.fbprophet_hacks import suppress_stdout_stderr

import numpy as np
import pandas as pd
from fbprophet import Prophet

from tank_forecaster.decomp import (
    generic_hh_seasonality,
    generic_weekly_seasonality,
    generic_yearly_seasonality,
)


def gen_future(df, periods=30, freq="1D"):
    start_0 = df.iloc[-1, 0]
    future = pd.date_range(start=start_0, freq=freq, periods=periods) + pd.Timedelta(
        freq
    )
    future = pd.DataFrame(future)
    future.rename(columns={0: "ds"}, inplace=True)

    return future


def forecast_far(
    sales_history,
    yearly_decomp=None,
    weekly_decomp=None,
    forecast_length=90,
    daily_lift_est=0,
):
    # if no decompositions are created, or not a full year of sales data, use generic
    if yearly_decomp is None or len(yearly_decomp) <= 52:
        yearly_decomp = generic_yearly_decomp

    if weekly_decomp is None or len(weekly_decomp) <= 6:
        weekly_decomp = generic_weekly_decomp

    # generate predictions DataFrame
    predictions = pd.DataFrame(columns=["woy", "dow", "base", "weekly", "daily"])
    predictions["woy"] = np.repeat(range(1, 54), 7)  # 52.14 'week of year' -> 53
    predictions["dow"] = [0, 1, 2, 3, 4, 5, 6] * 53  # 7 'day of week' each week of year

    # if no sales data is given, use daily_lift_estimate input w/ generic seasonality
    if sales_history is None or len(sales_history) == 0:
        predictions["base"] = daily_lift_est
        weekly = np.repeat(predictions.base.iloc[1] * 7 * generic_yearly_decomp, 7)
        weekly.index = range(0, 371)
        predictions["weekly"] = weekly
        weekly_decomp_rep = pd.concat([generic_weekly_decomp] * 53, ignore_index=True)
        predictions["daily"] = predictions.weekly * (1 / 7) * weekly_decomp_rep
        data = {
            "ds": [pd.to_datetime(datetime.now()), pd.to_datetime(datetime.now())],
            "sales": [0, 0],
        }
        sales_history = pd.DataFrame(data=data)
        sales_history["date"] = sales_history["ds"].dt.date

    else:  # if full year or more of sales data, use last year's average
        predictions["base"] = sales_history.y[-365:].mean()

    weekly = np.repeat(predictions.base[1] * 7 * yearly_decomp, 7)
    weekly.index = range(0, 371)
    predictions["weekly"] = weekly
    weekly_decomp_rep = pd.concat([weekly_decomp] * 53, ignore_index=True)

    predictions["daily"] = predictions.weekly * (1 / 7) * weekly_decomp_rep

    # match predictions DataFrame to gen future DataFrame
    future = gen_future(sales_history, periods=forecast_length, freq="1D")
    future["dow"] = future.ds.dt.weekday
    future["woy"] = future.ds.dt.week  # deprecated?
    output = pd.merge(
        future, predictions, left_on=["woy", "dow"], right_on=["woy", "dow"]
    )
    output = output[["ds", "daily"]]
    output.rename(columns={"daily": "yhat"}, inplace=True)

    # confidence interval
    output["lower"] = output["yhat"] - 2 * output["yhat"].std()
    output["upper"] = output["yhat"] + 2 * output["yhat"].std()

    # non-negative predictions
    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    return output


def forecast_near(
    validated_tank_history,
    forecast_freq="30min",
    forecast_length=144,
    daily_lift_est=0,
):

    # less than 9 days of historical data
    if validated_tank_history is None:
        validated_tank_history = pd.DataFrame(columns=["ds", "y"])

    if len(validated_tank_history) < 432:

        if validated_tank_history.empty:
            now = datetime.now()
            now_hh = now - (now - datetime.min) % timedelta(minutes=30)

        else:
            now_hh = validated_tank_history["ds"].iloc[-1]

        forecast = forecast_far(
            sales_history=[],
            yearly_decomp=generic_yearly_decomp,
            weekly_decomp=generic_weekly_decomp,
            daily_lift_est=daily_lift_est,
            forecast_length=3,
        )
        fake_data = {"ds": [now_hh], "sales": [0]}
        validated_tank_history = pd.DataFrame(data=fake_data)

        future = gen_future(
            validated_tank_history, periods=forecast_length, freq=forecast_freq
        )

        predictions = pd.DataFrame(columns=["ds", "daily"])
        predictions["ds"] = future.ds
        predictions["daily"] = np.repeat(forecast.yhat[0], len(predictions))
        predictions["ts"] = predictions["ds"].dt.time

        predictions = pd.merge(
            left=predictions,
            right=generic_daily_decomp,
            how="left",
            left_on="ts",
            right_on="ts",
        )

        predictions["hh"] = predictions.daily * (predictions.daily_multi * 1 / 48)
        output = predictions[["ds", "hh"]].copy()
        output.rename(columns={"hh": "yhat"}, inplace=True)

        output["lower"] = output["yhat"] - 2 * output["yhat"].std()
        output["upper"] = output["yhat"] + 2 * output["yhat"].std()

        # non-negative predictions
        for field in ["yhat", "lower", "upper"]:
            output.loc[output[field] < 0, field] = 0

        return output

    future = gen_future(
        validated_tank_history, periods=forecast_length, freq=forecast_freq
    )

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
    )

    with suppress_stdout_stderr():
        m.fit(validated_tank_history)

    forecast = m.predict(future)

    # format output
    output = forecast.loc[:, ["ds", "yhat_lower", "yhat_upper", "yhat"]]
    output.rename(columns={"yhat_lower": "lower", "yhat_upper": "upper"}, inplace=True)

    # non-negative predictions
    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    return output
