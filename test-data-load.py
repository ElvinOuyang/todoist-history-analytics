import todoist_functions as todofun
import mysql_functions as sqlfun
import datetime

if __name__ == '__main__':
    api = todofun.create_api()
    act = api.activity.get(limit=100)
    act_df = todofun.transform_act(act)
    act_df = todofun.df_standardization(act_df)
    sqlfun.overwrite_table_mysql(act_df, 'activity_test')

    # get a full activity log fetch from api
    full_fetch_until = datetime.datetime.now() - datetime.timedelta(weeks=15)
    full_df = todofun.act_fetch_all(until=full_fetch_until)
    print('>>> full_df is created with shape {}'.format(full_df.shape))
    print('>>> the history ranges from {} to {}'.format(
        full_df.event_date.min().strftime('%Y-%m-%d'),
        full_df.event_date.max().strftime('%Y-%m-%d')
        ))
    sqlfun.overwrite_table_mysql(full_df, 'activity_history')

# TODO: change the update since date method by using SQL query and get the
# latest event date from the MySQL table
    full_df = sqlfun.create_full_activity()
    update_df = todofun.act_fetch_new(full_df)
    print('>>> update_df is created with shape {}'.format(update_df.shape))
    print('>>> the update history ranges from {} to {}'.format(
        update_df.event_date.min().strftime('%Y-%m-%d'),
        update_df.event_date.max().strftime('%Y-%m-%d')
    ))
    sqlfun.append_table_mysql(update_df, 'activity_history')
