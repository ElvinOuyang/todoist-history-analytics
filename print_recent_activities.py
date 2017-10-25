import todoist_functions as todofun
import sys

if __name__ == '__main__':
    try:
        script, activity_count = sys.argv
    except ValueError:
        sys.stderr.write(
            "Please input desired rows of records after the script...\n")
        sys.exit(1)
    if int(activity_count) > 100:
        print(">>> This program prints up to 100 records. Printing:")
        activity_count = 100
    else:
        print(">>> Printing:")
        activity_count = int(activity_count)
    # set up api engine to my developer app
    api = todofun.create_api()
    # get one-time activity log from api
    act = api.activity.get(limit=activity_count)
    act_df = todofun.transform_act(act)
    act_df = todofun.df_standardization(act_df)
    print(act_df)
