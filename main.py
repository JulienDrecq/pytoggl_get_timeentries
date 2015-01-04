#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Maxime JACQUET <m.jacquet@outlook.fr>'
__version__ = 0.1
import argparse
import datetime
import requests
from datetime import date, timedelta


def get_week_days_range(year, week):
    d = date(year, 1, 1)
    # Gestion du Vendredi, Samedi, Dimanche tombant un 1er Janvier
    # http://en.wikipedia.org/wiki/Week
    if d.weekday() > 3:
        d = d + timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt,  d + dlt + timedelta(days=6)


class TogglObject(object):

    def __init__(self, api_token=None, api_version=None, url_toggl=None):
        self.api_token = api_token
        self.api_version = api_version if api_version.endswith('/') else api_version + '/'
        self.url_toggl = url_toggl if url_toggl.endswith('/') else url_toggl + '/'

    def _get_requests(self, api_get=None, params={}):
        assert api_get is not None, "Must specify the toggl api to call"
        get_url = self.url_toggl + self.api_version + api_get
        get_headers = {'content-type': 'application/json'}
        get_auth = (self.api_token, 'api_token')
        return requests.get(get_url,
                            headers=get_headers,
                            auth=get_auth,
                            params=params)
    
    def get_time_entries(self, start, end):
        result = self._get_requests('time_entries', {'start_date': start, 'end_date': end})
        if result and result.status_code == 200:
            json_result = result.json()
            return json_result
        return []

    def get_projects(self, project_id):
        result = self._get_requests('projects/%s' % project_id)
        if result and result.status_code == 200:
            json_result = result.json()
            return json_result
        return []
    
    def get_week_time_entries(self):
        current_calandar = datetime.datetime.now().isocalendar()
        current_week_range = get_week_days_range(current_calandar[0], current_calandar[1])

        start = current_week_range and current_week_range[0].strftime('%Y-%m-%dT00:00:00+02:00') or None
        end = current_week_range and current_week_range[1].strftime('%Y-%m-%dT23:59:59+02:00') or None
        if not start or not end:
            return []
        time_entries = self.get_time_entries(start, end)
        entries = []
        projects = {}
        for te in time_entries:
            project_name = None
            if te.get('pid', False):
                if te['pid'] not in projects:
                    p = self.get_projects(te['pid'])
                    if p and p['data']:
                        projects[p['data']['id']] = p['data']['name']
                project_name = projects[te['pid']]
            entries.append({
                'name': te['description'],
                'duration': te['duration'],
                'project_name': project_name
            })
        return start, end, entries
    

def add_options(parser):
    parser.add_argument('api_token', type=str, help='Toggl API token')
    parser.add_argument('-v',
                        type=str,
                        help='Toggl API version (default : v8)',
                        dest='api_version',
                        default='v8')
    parser.add_argument('-u',
                        type=str,
                        help='Toggl API URL (default : https://www.toggl.com/api/)',
                        dest='api_url',
                        default='https://www.toggl.com/api/')
    parser.add_argument('--hours',
                        type=int,
                        help='Number of hours in a workday (default : 8)',
                        dest='workhours',
                        default='8')
    

def group_by_project(time_entries):
    grouped_entries = {}
    for entries in time_entries:
        if entries['project_name'] in grouped_entries:
            grouped_entries[entries['project_name']].append({
                'name': entries['name'],
                'duration': entries['duration'],
            })
        else:
            grouped_entries[entries['project_name']] = [{
                'name': entries['name'],
                'duration': entries['duration'],
            }]
    return grouped_entries

def get_hms_duration(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def get_float_hours_duration(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return round(h + m / 60.0 + s / (60.0 ** 2), 4)

def get_float_days_duration(hours, workhours):
    return hours / workhours

def build_message(start, end, workhours, grouped_entries):
    message = "------------------------------------------------\n"
    message += "|              TOGGL TIME ENTRIES              |\n"
    message += "------------------------------------------------\n"
    message += "Here are your Toggl's time entries.\n"
    message += "From : %s\n" % start
    message += "To : %s\n" % end
    message += "\n"
    message += "\n"
    for project in grouped_entries:
        message += '# Project : %s\n' % project or 'None'
        for entries in grouped_entries[project]:
            message += '|   Name : %s\n' % entries['name']
            message += '|       Duration (H:M:S) : %s\n' % get_hms_duration(entries['duration'])
            hours = get_float_hours_duration(entries['duration'])
            message += '|       Duration (Hours) : %s\n' % hours
            message += '|       Duration (Days) : %s\n' % get_float_days_duration(hours, workhours)
    return message

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List Toggl time entries for invoicing report')
    add_options(parser)
    args = parser.parse_args()

    toggl = TogglObject(args.api_token,
                        args.api_version,
                        args.api_url)
    start, end, entries = toggl.get_week_time_entries()
    print build_message(start, end, args.workhours, group_by_project(entries))
