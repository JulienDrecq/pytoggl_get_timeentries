pytoggl_week_timeentries
===================

A small python script to get your current work week Toggl time entries


How to use : 
===================
$ python main.py 'YOU_API_TOKEN'

(python main.py -h for more option : workhours, specific date range, etc.)


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
* send the time entries message by email (add options or a config file for smtp configuration)
* add total by project
* round duration (days) amounts
* order by dates
