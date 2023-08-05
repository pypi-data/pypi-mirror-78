import numpy as np
import pandas as pd
import requests
from fbprophet import Prophet

# declare variables
store = "KT220"
tank = "7"
fc_url = "https://fc.bbdev.host3.capspire.com"


def decompose_sales(df):

    if df is None:
        return None

    if len(df) == 0:
        return None

    else:
        m = Prophet(
            changepoint_prior_scale=0.05,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            seasonality_mode="multiplicative",
        )

        m.fit(df)
        future = m.make_future_dataframe(periods=1, freq="1D")
        forecast = m.predict(future)
        forecast_reduced = forecast.loc[:, ["ds", "yearly", "weekly"]]
        forecast_reduced["dow"] = forecast_reduced.ds.dt.weekday
        forecast_reduced["doy"] = forecast_reduced.ds.dt.dayofyear
        forecast_reduced["woy"] = forecast_reduced.ds.dt.week
        week_trend = forecast_reduced.groupby("dow")["weekly"].mean() + 1
        forecast_reduced = forecast_reduced.iloc[-366:]
        forecast_reduced.sort_values(by=["woy", "dow"], inplace=True)
        year_trend = forecast_reduced.groupby("woy").mean()
        year_trend = year_trend["yearly"] + 1
        if len(year_trend) < 53:
            delta = 53 - len(year_trend)
            yearly_seasonality = pd.concat([year_trend, year_trend[:delta]])
    return yearly_seasonality, week_trend


# tank history decomposition for daily trends
def decompose_tank(tank_history):

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode="multiplicative",
    )

    m.fit(tank_history)
    future = m.make_future_dataframe(periods=1, freq="30min")
    forecast = m.predict(future)
    forecast_reduced = forecast.loc[:, ["ds", "daily", "daily_lower", "daily_upper"]]
    forecast_reduced["time"] = forecast_reduced["ds"].dt.time
    forecast_reduced.drop(columns="ds", inplace=True)
    day_trend = forecast_reduced.groupby("time").mean()
    day_trend.sort_values(by=["time"], inplace=True)

    for field in ["daily", "daily_lower", "daily_upper"]:
        day_trend.loc[:, field] = day_trend.loc[:, field] + 1

    return day_trend


# holiday decomposition - needs improvement for consistent date mapping
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


# # request sales data
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


# from tank_forecaster import validation
#
#
# def main():
#     x = get_sales_history(store_number=store, tank_id=tank)
#     y = validation.format_sales(x)
#     z = decompose_sales(y)
#     print(z[0], z[1])
#     print(len(z[0]))
#
#
# print(generic_yearly_seasonality)
# print(len(generic_yearly_seasonality))

if __name__ == "__main__":
    main()
