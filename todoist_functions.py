import pandas as pd
from todoist.api import TodoistAPI
import os
import sys
import numpy as np
import datetime


def create_api():
    try:
        token = os.environ['TODOIST_TOKEN']
    except KeyError:
        sys.stderr.write("TODOIST_* environment variable not set\n")
        sys.exit(1)
    api = TodoistAPI(token)
    return api


def transform_act(act_dict):
    """
    Function to Transform TodoistAPI Returned Activity Dictionary
    -----INPUT-----
    act_dict: the activity dictionary returned by TodoistAPI.activity.get()
    -----OUTPUT-----
    act_df: the standardized Pandas Dataframe for activity history, with all
    possible variables included
    """
    for i in range(len(act_dict)):
        for key, item in act_dict[i]['extra_data'].items():
            act_dict[i][key] = item
        del(act_dict[i]['extra_data'])
    act_df = pd.DataFrame(act_dict)
    vnames = ['client', 'content', 'due_date', 'event_date', 'event_type',
              'id', 'initiator_id', 'last_content', 'last_due_date',
              'name', 'object_id', 'object_type', 'parent_item_id',
              'parent_project_id']
    for vname in vnames:
        if vname not in act_df.columns:
            act_df[vname] = np.nan
    return act_df


def df_standardization(df):
    """
    Function to Standardize the Downloaded or Loaded Todoist Activity DataFrame
    -----INPUT-----
    df: activity dataframe that has been created with transform_act()
    -----OUTPUT-----
    df: activity Pandas Dataframe with needed dtypes for further analysis
    """
    df.client = df.client.astype('category')
    df.content = df.content.astype(str)
    df.due_date = pd.to_datetime(df.due_date)
    df.event_date = pd.to_datetime(df.event_date)
    df.event_type = df.event_type.astype('category')
    df.id = df.id.astype(str)
    df.initiator_id = df.initiator_id.astype(str)
    df.last_content = df.last_content.astype(str)
    df.last_due_date = pd.to_datetime(df.last_due_date)
    df.name = df.name.astype(str)
    df.object_id = df.object_id.astype(str)
    df.object_type = df.object_type.astype('category')
    df.parent_item_id = df.parent_item_id.astype(float)
    df.parent_project_id = df.parent_project_id.astype(float)
    return df


def act_fetch_all(until=datetime.datetime.now()):
    """
    Function to Download All Activity History as Todoist Activity
    -----INPUT-----
    api_engine: a TodoistAPI(token) object that connects to Todoist API
    until: a datetime.datetime object that signifies the latest time the
    user wants to fetch the history. Defaults to the time of the excution.
    -----OUTPUT-----
    act_df: a standardized Activity DataFrame with all activity history
    -----DEPENDENCY-----
    transform_act(): transforms dictionary to Pandas DataFrame
    df_standardization(): standardizes Pandas DataFrame
    """
    api_engine = create_api()
    until_param = until.strftime('%Y-%m-%dT%H:%M:%S')
    act_df = df_standardization(transform_act(
        api_engine.activity.get(limit=100, until=until_param)))
    # print('act_df is downloaded until {}'.format(until_param))
    new_len = len(act_df)
    # print('new_len is {}'.format(new_len))
    while new_len == 100:
        until = act_df.event_date.min() - datetime.timedelta(seconds=1)
        until_param = until.strftime('%Y-%m-%dT%H:%M:%S')
        new_df = df_standardization(transform_act(
            api_engine.activity.get(limit=100, until=until_param)))
        # print('act_df is downloaded until {}'.format(until_param))
        new_len = len(new_df)
        # print('new_len is updated to {}'.format(new_len))
        act_df = act_df.append(new_df)
    return act_df


def act_fetch_new(since, until=datetime.datetime.now()):
    """
    Function to Update Activity History as Todoist Activity
    -----INPUT-----
    since: datetime object of the latest event_date from loaded records
    until: a datetime.datetime object that signifies the latest time the
    user wants to fetch the history. Defaults to the time of the excution.
    -----OUTPUT-----
    act_df: an updated standardized full Activity DataFrame
    df: the new activity history since last fetch
    -----DEPENDENCY-----
    transform_act(): transforms dictionary to Pandas DataFrame
    df_standardization(): standardizes Pandas DataFrame
    """
    api_engine = create_api()
    since_param = since.strftime('%Y-%m-%dT%H:%M:%S')
    until_param = until.strftime('%Y-%m-%dT%H:%M:%S')
    df = df_standardization(transform_act(
        api_engine.activity.get(limit=100, since=since_param,
                                until=until_param)))
    new_len = len(df)
    while new_len == 100:
        since = df.event_date.max() + datetime.timedelta(seconds=1)
        since_param = since.strftime('%Y-%m-%dT%H:%M:%S')
        new_df = df_standardization(transform_act(
            api_engine.activity.get(limit=100, since=since_param,
                                    until=until_param)))
        new_len = len(new_df)
        df = df.append(new_df)
    return df
