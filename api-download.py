from todoist.api import TodoistAPI
import pandas as pd
# import numpy as np
from sys import argv

token = argv

# set up api engine to my developer app
api = TodoistAPI(token)

# get activity log from api

act = api.activity.get(limit=100)


def transform_act(act_dict):
    for i in range(len(act_dict)):
        for key, item in act_dict[i]['extra_data'].items():
            act_dict[i][key] = item
        del(act_dict[i]['extra_data'])
    return act_dict

act_clean = transform_act(act)
act_df = pd.DataFrame(act_clean)

print(act_df.head())

# TODO: Standardize the data type for each column from the activity log
# using the documentation listed at
# https://developer.todoist.com/sync/v7/?python#get-activity-logs

# TODO: Device a function that runs a first time request to get all
# activities. Something called act_fetch_all

# TODO: Device a function that runs an incremental request to get new
# activities since last sync. Something called act_fetch_new

# TODO: Device a function/pipeline that stores and load pandas dataframe
# of the activities in a csv (with standarized formats)
