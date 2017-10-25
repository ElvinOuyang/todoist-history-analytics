# Todoist Activity History Analytics

## Introduction
As a brief introduction, [Todoist](https://en.todoist.com/guide/getting-started) is a modern personal productivity management app (or ["Getting Things Done"](https://en.wikipedia.org/wiki/Getting_Things_Done), GTD, app) that provides cloud syncing functionality across platforms on iOS, MacOS, Web App, Android, and Windows. More interestingly, the cloud-enabled service allows users to link other services such as [IFTTT](https://support.todoist.com/hc/en-us/articles/212102065-How-can-I-use-Todoist-with-IFTTT-), [Slack](https://support.todoist.com/hc/en-us/articles/207659179-How-can-I-use-Todoist-with-Slack-), [Dropbox](https://support.todoist.com/hc/en-us/articles/211497749-How-can-I-use-Todoist-with-Google-Drive-Dropbox-), to enable easy accessibility and automated scheduling. Even better, the cloud-based service grants developers almost [full API access](https://developer.todoist.com/sync/v7/) for app development or service integration.

As a professional in data science, I am a Todoist premium subscriber and use the tool to manage my taskflow every day. Since I rely heavily on Todoist to manage my work and study, I often feel the urge to review my productivity over time. However, the native Todoist app does not provide deep enough insight of my productivity: it only provides a "karma" system that calculates your productivity based on the numeric total of number of tasks you complete everyday. For an extensive period of time, I was frustrated with the lackluster analytics functionality of Todoist and other GTD services (such as OmniFocus, Toledo) in general.

My frustration comes to an end when I heard that Todoist service provides [a new "activity log" feature](https://www.engadget.com/2016/06/28/todoist-business-updates-activity-log-notifications/) for premium subscribers that unlocks the history of any kind of changes (add, update, delete, complete) to tasks and projects. With this data flow available from the official API, I can now build a personal analytics solution that gives me the insight of how am I doing in my daily work and study.

In this project, I plan to build an the analytics solution with a python portal that communicates with Todoist API, a live MySQL database maintained on Amazon Web Services (AWS), and a Bokeh dashboard with server hosted on AWS EC2. Since this is an ongoing project, I will keep updating my codes and my project description.

## Project Stages
### Stage One: Connect and Download Activity Logs from TodoistAPI (Completed)
At this stage, I created codes in Python that use Todoist's official API package [`todoist-python`](https://github.com/Doist/todoist-python) and standard data science packages to fetch activity records and transform them into `pandas.DataFrame`. The key features I created at this stage include:
1. Initiate API engine/connection with credentials saved as environment variables
2. Transform API-returned JSON-like dictionary records into structured `pandas.DataFrame`, which is typical for analytics in following stages
3. Create a looping mechanism that fetches records based on `event_date` ranges of downloaded records, since the API has a limit of 100 records per query

### Stage Two: Connect to AWS RDS MySQL Server and Save/Load Activity Records (Completed)
At this stage, I created codes in Python that use [`sqlalchemy`](https://www.sqlalchemy.org/) package and data science packages to connect, read, and write to a remote MySQL server hosted on [Amazon Web Service Relational Database Service](https://aws.amazon.com/rds/). The key features I created at this stage include:
1. Initiate SQLAlchemy connection engine to AWS MySQL database and autoload table structure for easy querying
2. Create quiries to automatically recognize the latest records saved in the database and upate the records using codes created in Stage One

### Stage Three: Data Cleaning and In-depth Analytics Dashboarding with Bokeh (Ongoing)
I will keep updating this post and provide more information as I continue to build out this project.
