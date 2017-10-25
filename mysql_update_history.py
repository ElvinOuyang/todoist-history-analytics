import todoist_functions as todofun
import mysql_functions as sqlfun

if __name__ == '__main__':
    since_date = sqlfun.get_latest_eventdate()
    update_df = todofun.act_fetch_new(since=since_date)
    print('>>> update_df is created with shape {}'.format(update_df.shape))
    print('>>> the update history ranges from {} to {}'.format(
        update_df.event_date.min().strftime('%Y-%m-%d'),
        update_df.event_date.max().strftime('%Y-%m-%d')
    ))
    sqlfun.append_table_mysql(update_df, 'activity_history')
