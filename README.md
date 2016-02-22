pytoggl_get_timeentries
===================

A small python script to get your current work week Toggl time entries (or for a specific dates range)


How to use : 
===================
$ python main.py 'YOU_API_TOKEN'

(python main.py -h for more option : workhours, specific dates range, send_by_mail, etc.)

/!\ For a specific dates range the limit of the return is 1000. So only the first 1000 found time entries are returned /!\ (view Toggl API : https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md#get-time-entries-started-in-a-specific-time-range)


Redmine time entries :
===================
You can auto create time entries if the "Redmine" option is set (--redmine option)
You have to set the "Redmine URL" and the "Redmine API key" options (--rurl and --rkey options)

You need to specify the ticket number in the TOGGL time entrie's description (ie : #12345 - TEST TOGGL TO REDMINE)
If many ticket number found in the description, a time entry will be created by ticket. The duration will be divided by the number of ticket


Exemple : 
===================
The script is started the 2014-01-04, the current work week will be 2014-12-29 - 2015-01-04

Output : 
    
    ------------------------------------------------
    |              TOGGL TIME ENTRIES              |
    ------------------------------------------------
    Here are your Toggl's time entries.
    From : 2014-12-29
    To : 2015-01-04
    
    
    # Date : 2014-12-29
        * Project : None
        |   Name : TIME ENTRY 1
        |         Duration (H:M:S) : 8:45:00
        |         Duration (Hours) : 8.75
        |         Duration (Days) : 1.094
        > Duration total (Hours) : 8.75
        > Duration total (Days) : 1.094
    # Date : 2014-12-30
        * Project : PROJECT1
        |   Name : TIME ENTRY 2
        |         Duration (H:M:S) : 8:35:07
        |         Duration (Hours) : 8.585
        |         Duration (Days) : 1.073
        > Duration total (Hours) : 8.585
        > Duration total (Days) : 1.073
    # Date : 2014-12-31
        * Project : PROJECT1
        |   Name : TIME ENTRY 3
        |         Duration (H:M:S) : 8:23:20
        |         Duration (Hours) : 8.389
        |         Duration (Days) : 1.049
        > Duration total (Hours) : 8.389
        > Duration total (Days) : 1.049
    # Date : 2015-01-02
        * Project : PROJECT4
        |   Name : TIME ENTRY 4
        |         Duration (H:M:S) : 7:50:44
        |         Duration (Hours) : 7.846
        |         Duration (Days) : 0.980
        |   Name : TIME ENTRY 5
        |         Duration (H:M:S) : 2:30:00
        |         Duration (Hours) : 2.5
        |         Duration (Days) : 0.313
        > Duration total (Hours) : 10.346
        > Duration total (Days) : 1,293
        * Project : PROJECT3
        |   Name : TIME ENTRY 6
        |         Duration (H:M:S) : 1:30:00
        |         Duration (Hours) : 1.5
        |         Duration (Days) : 0.188
        > Duration total (Hours) : 1.5
        > Duration total (Days) : 0.188

Todo :
===================
* test new smtplib auth (not fully tested) and maybe an email smtplib improvements
* better options management (maybe cfg file instead ?)
* general improvement
