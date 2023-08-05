import numpy as np
import pandas as pd
from fbprophet import Prophet

# set standard events
ny = pd.DataFrame({'holiday': "New Year's Day",
                   'ds': pd.to_datetime(['2020-01-01', '2021-01-01', '2022-01-01',
                                         '2023-01-01', '2024-01-01', '2025-01-01']),
                   'factor': 0.7
                   })

mem = pd.DataFrame({'holiday': "Memorial Day",
                    'ds': pd.to_datetime(['2020-05-25', '2021-05-31', '2022-05-30',
                                          '2023-05-29', '2024-05-27', '2025-05-26']),
                    'factor': 0.9
                    })

ind = pd.DataFrame({'holiday': "Independence Day",
                    'ds': pd.to_datetime(['2020-07-04', '2021-07-04', '2022-07-04',
                                          '2023-07-04', '2024-07-04', '2025-07-04']),
                    'factor': 0.7
                    })

lab = pd.DataFrame({'holiday': "Labor Day",
                    'ds': pd.to_datetime(['2020-09-07', '2021-09-06', '2022-09-05',
                                          '2023-09-04', '2024-09-02', '2025-09-01']),
                    'factor': 0.9
                    })

thanks = pd.DataFrame({'holiday': "Thanksgiving",
                       'ds': pd.to_datetime(['2020-11-26', '2021-11-25', '2022-11-24',
                                             '2023-11-23', '2024-11-28', '2025-11-27']),
                       'factor': 0.9
                       })

xmas = pd.DataFrame({'holiday': "Christmas",
                     'ds': pd.to_datetime(['2020-12-25', '2021-12-25', '2022-12-25',
                                           '2023-12-25', '2024-12-25', '2025-12-25']),
                     'factor': 0.9
                     })

standard_events = pd.concat([ny, mem, ind, lab, thanks, xmas]).reset_index(drop=True)


def add_events(events, names, dates, factors):
    new_events = pd.DataFrame({'holiday': [*names],
                               'ds': pd.to_datetime([*dates]),
                               'factor': [*factors]})
    events = pd.concat([events, new_events], axis=0, ignore_index=True)
    return events


# def drop_events(events, names, dates, factors):
#     drop_events = pd.DataFrame({'holiday': [*names],
#                                 'ds': pd.to_datetime(*dates),
#                                 'factor': [*factors]})
#     events = events.loc[not drop_events]
#     return events


def apply_event_factor(forecast, events, output='dict'):

    if type(forecast) != pd.core.frame.DataFrame:  # no historical sales data
        return 'Error - not enough data to provide forecast'

    if len(forecast.ds) == len(forecast.ds.dt.date.unique()):  # long term forecast
        events = events[['ds', 'factor']]
        events_dict = events.set_index('ds').to_dict(orient='index')

        for row in range(len(forecast)):
            if events_dict.get(forecast.ds[row]):
                forecast.loc[row, 'yhat'] *= events_dict.get(forecast.ds[row]).get('factor')

    else:  # short term forecast
        expanded_ds = pd.Series(name='ds', dtype='datetime64[ns]')
        expanded_factors = pd.Series(name='factors', dtype='float')

        for row in range(len(events)):
            expanded_ds = pd.concat([expanded_ds,
                                     pd.Series(pd.date_range(start=events.ds[row], freq='30min', periods=48))],
                                    ignore_index=True)
            expanded_factors = pd.concat([expanded_factors,
                                          pd.Series(np.repeat(events.factor[row], 48))], ignore_index=True)

        events_hh = pd.DataFrame(columns=['ds', 'factor'])
        events_hh['ds'] = expanded_ds
        events_hh['factor'] = expanded_factors

        events_hh_dict = events_hh.set_index('ds').to_dict(orient='index')

        for row in range(len(forecast)):
            if events_hh_dict.get(forecast.ds[row]):
                forecast.loc[row, 'yhat'] *= events_hh_dict.get(forecast.ds[row]).get('factor')

    if output == 'df':
        return forecast
    else:
        return forecast.to_dict(orient='records')


def remove_event_factor(historical, events):
    if len(historical.ds) == len(historical.ds.dt.date.unique()):  # sales histories
        events = events[['ds', 'factor']]
        events_dict = events.set_index('ds').to_dict(orient='index')

        for row in range(len(historical)):
            if events_dict.get(historical.ds[row]):
                historical.loc[row, 'y'] *= 2 - events_dict.get(historical.ds[row]).get('factor')

    else:  # tank histories
        expanded_ds = pd.Series(name='ds', dtype='datetime64[ns]')
        expanded_factors = pd.Series(name='factors', dtype='float')

        for row in range(len(events)):
            expanded_ds = pd.concat([expanded_ds,
                                     pd.Series(pd.date_range(start=events.ds[row], freq='30min', periods=48))],
                                    ignore_index=True)
            expanded_factors = pd.concat([expanded_factors,
                                          pd.Series(np.repeat(events.factor[row], 48))], ignore_index=True)

        events_hh = pd.DataFrame(columns=['ds', 'factor'])
        events_hh['ds'] = expanded_ds
        events_hh['factor'] = expanded_factors

        events_hh_dict = events_hh.set_index('ds').to_dict(orient='index')

        for row in range(len(historical)):
            if events_hh_dict.get(historical.ds[row]):
                historical.loc[row, 'y'] *= 2 - events_hh_dict.get(historical.ds[row]).get('factor')

    return historical

