from todoist.api import TodoistAPI
import todoist_functions as todofun
import pandas as pd
import datetime

if __name__ == '__main__':
    # set up api engine to my developer app
    api = todofun.create_api()

    # get one-time activity log from api
    act = api.activity.get(limit=100)
    act_df = todofun.transform_act(act)
    act_df = todofun.df_standardization(act_df)
    print('>>> act_df is created with shape {}'.format(act_df.shape))
    print('>>> below is a brief view of the data:')
    print(act_df.head())

    # get a full activity log fetch from api
    full_fetch_until = datetime.datetime.now() - datetime.timedelta(weeks=15)
    full_df = todofun.act_fetch_all(until=full_fetch_until)
    print('>>> full_df is created with shape {}'.format(full_df.shape))
    print('>>> the history ranges from {} to {}'.format(
        full_df.event_date.min().strftime('%Y-%m-%d'),
        full_df.event_date.max().strftime('%Y-%m-%d')
        ))

    # get a activity update fetch from api
    full_df = todofun.df_standardization(pd.read_csv('all_history.csv'))
    update_df = todofun.act_fetch_new(full_df)
    print('>>> update_df is created with shape {}'.format(update_df.shape))
    print('>>> the update history ranges from {} to {}'.format(
        update_df.event_date.min().strftime('%Y-%m-%d'),
        update_df.event_date.max().strftime('%Y-%m-%d')
    ))
