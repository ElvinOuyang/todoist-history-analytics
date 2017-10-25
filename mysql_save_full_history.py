import todoist_functions as todofun
import mysql_functions as sqlfun
import datetime


if __name__ == '__main__':
    full_fetch_until = datetime.datetime.now()
    full_df = todofun.act_fetch_all(until=full_fetch_until)
    print('>>> full_df is created with shape {}'.format(full_df.shape))
    print('>>> the history ranges from {} to {}'.format(
        full_df.event_date.min().strftime('%Y-%m-%d'),
        full_df.event_date.max().strftime('%Y-%m-%d')
        ))
    sqlfun.overwrite_table_mysql(full_df, 'activity_history')
