pytoggl_get_timeentries
===================

A small python script to get your current work week Toggl time entries (or for a specific dates range)


How to use : 
===================
$ python main.py 'YOU_API_TOKEN'

(python main.py -h for more option : workhours, specific dates range, send_by_mail, etc.)

/!\ For a specific dates range the limit of the return is 1000. So only the first 1000 found time entries are returned /!\ (view Toggl API : https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md#get-time-entries-started-in-a-specific-time-range)


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
    
    
    # Date : 2014-12-31
        * Project : None
        |   Name : TIME ENTRY 1
        |         Duration (H:M:S) : 8:45:00
        |         Duration (Hours) : 8.75
        |         Duration (Days) : 1.09375
    # Date : 2014-12-30
        * Project : PROJECT1
        |   Name : TIME ENTRY 2
        |         Duration (H:M:S) : 8:35:07
        |         Duration (Hours) : 8.5853
        |         Duration (Days) : 1.0731625
    # Date : 2014-12-29
        * Project : PROJECT1
        |   Name : TIME ENTRY 3
        |         Duration (H:M:S) : 8:23:20
        |         Duration (Hours) : 8.3889
        |         Duration (Days) : 1.0486125
    # Date : 2015-01-02
        * Project : PROJECT4
        |   Name : TIME ENTRY 4
        |         Duration (H:M:S) : 7:50:44
        |         Duration (Hours) : 7.8456
        |         Duration (Days) : 0.9807
        |   Name : TIME ENTRY 5
        |         Duration (H:M:S) : 2:30:00
        |         Duration (Hours) : 2.5
        |         Duration (Days) : 0.3125
        * Project : PROJECT3
        |   Name : TIME ENTRY 6
        |         Duration (H:M:S) : 1:30:00
        |         Duration (Hours) : 1.5
        |         Duration (Days) : 0.1875


Todo :
===================
* add options for smtp configuration (server, user, password, etc)
* add total by project
* round duration (days) amounts
* order by dates
