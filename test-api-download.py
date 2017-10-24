from todoist.api import TodoistAPI
from sys import argv
import todoist_functions as todofun
import pandas as pd

script, token = argv
print('argv is {}'.format(token))

# set up api engine to my developer app
api = TodoistAPI(token)

# get activity log from api
act = api.activity.get(limit=100)
act_df = todofun.transform_act(act)
act_df = todofun.df_standardization(act_df)
print('>>> act_df is created with shape {}'.format(act_df.shape))
print('>>> below is a brief view of the data:')
print(act_df.head())

full_fetch_until = datetime.datetime.now() - datetime.timedelta(weeks=15)
full_df = todofun.act_fetch_all(api, until=full_fetch_until)
print('>>> full_df is created with shape {}'.format(full_df.shape))
print('>>> the history ranges from {} to {}'.format(
    full_df.event_date.min().strftime('%Y-%m-%d'),
    full_df.event_date.max().strftime('%Y-%m-%d')
))

full_df = todofun.df_standardization(pd.read_csv('all_history.csv'))
update_df = todofun.act_fetch_new(api, full_df)
print('>>> update_df is created with shape {}'.format(update_df.shape))
print('>>> the history ranges from {} to {}'.format(
    update_df.event_date.min().strftime('%Y-%m-%d'),
    update_df.event_date.max().strftime('%Y-%m-%d')
))
