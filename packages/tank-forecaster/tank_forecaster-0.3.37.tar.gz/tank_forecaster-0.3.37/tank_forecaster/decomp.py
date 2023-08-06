import numpy as np
import pandas as pd
import requests
from fbprophet import Prophet
from sparkles.fbprophet_hacks import suppress_stdout_stderr

# declare variables for testing
store = "KT220"
tank = "7"
fc_url = "https://fc.bbdev.host3.capspire.com"


def decompose_sales(sales_data):

    # not enough data
    if sales_data is None or len(sales_data) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    # fit model for weekly seasonality
    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        seasonality_mode="multiplicative",
    )
    with suppress_stdout_stderr():
        m.fit(sales_data)

    # calculate weekly seasonality
    future = m.make_future_dataframe(periods=1, freq="1D")
    forecast = m.predict(future)
    forecast_reduced = forecast.loc[:, ["ds", "yearly", "weekly"]]
    forecast_reduced["dow"] = forecast_reduced.ds.dt.weekday
    forecast_reduced["doy"] = forecast_reduced.ds.dt.dayofyear
    forecast_reduced["woy"] = forecast_reduced.ds.dt.week

    weekly_seasonality = forecast_reduced.groupby("dow")["weekly"].mean() + 1

    if len(weekly_seasonality) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    if len(sales_data) < 350:
        return pd.Series([1] * 53), weekly_seasonality

    # if nearly a full year, or more of data exists, calculate yearly seasonality
    forecast_reduced = forecast_reduced.iloc[-366:]
    forecast_reduced.sort_values(by=["woy", "dow"], inplace=True)
    year_trend = forecast_reduced.groupby("woy").mean()
    year_trend = year_trend["yearly"] + 1

    # ensure 53 weeks are calculated by wrapping week values to end of the year
    if len(year_trend) < 53:
        delta = 53 - len(year_trend)
        yearly_seasonality = pd.concat(
            [year_trend, year_trend[:delta]], ignore_index=True
        )

    if len(weekly_seasonality) == 7 and len(yearly_seasonality) == 53:
        return yearly_seasonality, weekly_seasonality

    return pd.Series([1] * 53), pd.Series([1] * 7)


def decompose_tank(tank_history):

    if tank_history is None or len(tank_history) < 48:
        return generic_hh_seasonality

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode="multiplicative",
    )
    with suppress_stdout_stderr():
        m.fit(tank_history)

    future = m.make_future_dataframe(periods=1, freq="30min")
    forecast = m.predict(future)

    forecast_reduced = forecast.loc[:, ["ds", "daily"]]
    forecast_reduced["time"] = forecast_reduced["ds"].dt.time
    forecast_reduced.drop(columns="ds", inplace=True)
    day_trend = forecast_reduced.groupby("time").mean()
    day_trend.sort_values(by=["time"], inplace=True)

    if len(day_trend) != 48:
        return generic_hh_seasonality

    hh_seasonality = day_trend["daily"] + 1

    return hh_seasonality


def decompose_holiday(input):
    if type(input) != pd.core.frame.DataFrame:
        return print("error - input is not a DataFrame")
    else:
        event_1 = pd.DataFrame(
            {
                "holiday": "event_1_name",
                "ds": pd.to_datetime(["2020-03-01"]),
                "lower_window": 0,
                "upper_window": 0,
            }
        )
        event_2 = pd.DataFrame(
            {
                "holiday": "event_2_name",
                "ds": pd.to_datetime(["2020-03-02"]),
                "lower_window": 0,
                "upper_window": 0,
            }
        )
        holidays = pd.concat([event_1, event_2])
        m = Prophet(
            holidays=holidays,
            changepoint_prior_scale=0.05,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            seasonality_mode="multiplicative",
        )
        m.add_country_holidays(country_name="US")
        with suppress_stdout_stderr():
            m.fit(input)
        future = m.make_future_dataframe(periods=1, freq="1D")
        forecast = m.predict(future)
        forecast_reduced = forecast.loc[:, ["ds", "holidays"]]

    return forecast_reduced


generic_weekly_seasonality = [0.95, 1.0, 1.05, 1.05, 1.2, 0.95, 0.8]
generic_yearly_seasonality = [
    0.95,
    0.95,
    *np.repeat(0.9, 10),
    0.925,
    0.95,
    0.975,
    *np.repeat(1, 7),
    1.025,
    1.05,
    *np.repeat(1.075, 11),
    1.05,
    1.025,
    *np.repeat(1, 7),
    *np.repeat(0.95, 9),
]
generic_hh_seasonality = [
    1.0,
    0.85,
    0.7,
    0.55,
    0.4,
    0.25,
    0.1,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
    2.0,
    2.0,
    2.0,
    1.9,
    1.8,
    1.7,
    1.6,
    1.5,
    1.4,
    1.3,
    1.2,
    1.1,
]


# request sales data
# def get_sales_history(
#     store_number: str, tank_id: str,
# ):
#     parameters = {
#         "store_number": store_number,
#         "tank_id": tank_id,
#         "limit": 365,
#         "system_psk": "lol",
#     }
#
#     r = requests.post(url=f"{fc_url}/sales_data/list", params=parameters)
#
#     return r.json()


from tank_forecaster import validation

#
# def main():
#     x = get_sales_history(store_number=store, tank_id=tank)
#     y = validation.format_sales(x)
#     z = decompose_sales(y)
#     print(z[0], z[1])
#     print(len(z[0]), len(z[1]))


if __name__ == "__main__":
    pass
