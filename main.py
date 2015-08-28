#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Maxime JACQUET <m.jacquet@outlook.fr> & Julien DRECQ <drecq.julien@outlook.com>'
__version__ = 0.2
import argparse
import datetime
import smtplib
import requests
import collections
from socket import error as socket_error
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
            return start, end, []
        time_entries = self.get_time_entries(start, end)
        return start, end, self.get_time_entries_datas(time_entries)
    
    def get_range_time_entries(self, start, end):
        start = start.strftime('%Y-%m-%dT00:00:00+02:00') or None
        end = end.strftime('%Y-%m-%dT23:59:59+02:00') or None
        if not start or not end:
            return start, end, []
        time_entries = self.get_time_entries(start, end)
        return start, end, self.get_time_entries_datas(time_entries)
 
    def get_time_entries_datas(self, time_entries):
        entries = []
        projects = {}
        for te in time_entries:
            if 'description' not in te:
                te['description'] = 'None'
            project_name = None
            if te.get('pid', False):
                if te['pid'] not in projects:
                    p = self.get_projects(te['pid'])
                    if p and p['data']:
                        projects[p['data']['id']] = p['data']['name']
                project_name = projects[te['pid']]
            start = te['start'].split('T')
            start = start and start[0]
            entries.append({
                'date': start,
                'name': te['description'],
                'duration': te['duration'],
                'project_name': project_name,
            })
        return entries


def mkdate(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d')


def check_dates(dstart, dend):
    if not dstart or not dend:
        return False
    assert dend >= dstart, 'End date must be greater than Start date'
    return True


def add_options(parser):
    parser.add_argument('api_token', type=str, help='Toggl API token')
    # TOGGL OPTIONS
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
    # HOURS AND DATES OPTIONS
    parser.add_argument('--hours',
                        type=int,
                        help='Number of hours in a workday (default : 8)',
                        dest='workhours',
                        default='8')
    parser.add_argument('--start',
                        type=mkdate,
                        help='Start date for time entries',
                        dest='dstart')
    parser.add_argument('--end',
                        type=mkdate,
                        help='End date for time entries',
                        dest='dend')
    # EMAIL OPTIONS
    parser.add_argument('--send_by_mail',
                        action='store_true',
                        help='Enable email sending for times entries',
                        dest='send_by_mail')
    parser.add_argument('-t', '--to',
                        type=str,
                        help='Specify a receiver for email sending',
                        dest='email_to')
    parser.add_argument('-f', '--from',
                        type=str,
                        help='Specify a sender for email sending',
                        dest='email_from')
    parser.add_argument('-s', '--subject',
                        type=str,
                        help='Specify a subject for email sending',
                        dest='subject',
                        default='PyToggl time entries')
    parser.add_argument('--smtp',
                        type=str,
                        dest="smtp",
                        help="SMTP serveur")
    parser.add_argument('--smtp-port',
                        type=int,
                        dest="smtp_port",
                        help="SMTP port")
    parser.add_argument('--starttls',
                        action='store_true',
                        help='Start TLS mode',
                        dest='starttls')
    parser.add_argument('--login',
                        type=str,
                        dest='login',
                        help="SMTP login")
    parser.add_argument('--password',
                        type=str,
                        dest='password',
                        help="SMTP password")



def get_ordered_dict(datas):
    return collections.OrderedDict(sorted(datas.items()))


def group_by_date_and_project(time_entries):
    grouped_entries = {}
    for entries in time_entries:
        if entries['date'] in grouped_entries:
            grouped_entries[entries['date']].append({
                'project_name': entries['project_name'],
                'name': entries['name'],
                'duration': entries['duration'],
            })
        else:
            grouped_entries[entries['date']] = [{
                'project_name': entries['project_name'],
                'name': entries['name'],
                'duration': entries['duration'],
            }]
    for date in grouped_entries:
        grouped_entries[date] = group_by_project(grouped_entries[date])
    return get_ordered_dict(grouped_entries)


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
    start = start.split('T')
    start = start and start[0]
    message += "From : %s\n" % start
    end = end.split('T')
    end = end and end[0]
    message += "To : %s\n" % end
    message += "\n"
    message += "\n"
    for date in grouped_entries:
        message += '# Date : %s\n' % date or 'None'
        total_hours_day = 0.0
        for project in grouped_entries[date]:
            total_hours = 0.0
            message += '    * Project : %s\n' % project or 'None'
            for entries in grouped_entries[date][project]:
                message += '    |   Name : %s\n' % entries['name']
                message += '    |         Duration (H:M:S) : %s\n' % get_hms_duration(entries['duration'])
                hours = get_float_hours_duration(entries['duration'])
                total_hours += hours
                message += '    |         Duration (Hours) : %s\n' % round(hours, 3)
                message += '    |         Duration (Days) : %s\n' % round(get_float_days_duration(hours, workhours), 3)
            total_hours_day += total_hours
            message += '    > Duration total (Hours) : %s\n' % round(total_hours, 3)
            message += '    > Duration total (Days) : %s\n' % round(get_float_days_duration(total_hours, workhours), 3)
        message += '> Total (Hours) : %s\n' % round(total_hours_day, 3)
        message += '> Total (Days) : %s\n' % round(get_float_days_duration(total_hours_day, workhours), 3)
    return message


def send_by_email(message, smtp, smtp_port, starttls, login, password, email_to, email_from, subject):
    server = None
    try:
        if smtp and smtp_port:
            server = smtplib.SMTP(smtp, smtp_port)
        else:
            server = smtplib.SMTP()
            server.connect()
        if starttls:
            server.ehlo()
            server.starttls()
            server.ehlo()
        if login and password:
            server.login(login, password)
        header = 'To:' + email_to + '\n' + 'From: ' + email_from + '\n' + 'Subject:' + subject + '\n'
        msg = header + '\n%s \n\n' % message
        server.sendmail(email_from, email_to, msg.encode('utf-8'))
    except socket_error, e:
        print 'An error has occured during SMTP connection : %s' % e
    except Exception, e:
        print 'An error has occured during email creation : %s' % e
    finally:
        if server:
            server.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List Toggl time entries for invoicing report')
    add_options(parser)
    args = parser.parse_args()
    toggl = TogglObject(args.api_token,
                        args.api_version,
                        args.api_url)
    if check_dates(args.dstart, args.dend):
        start, end, entries = toggl.get_range_time_entries(args.dstart, args.dend)
    else:
        start, end, entries = toggl.get_week_time_entries()

    grouped_entries = group_by_date_and_project(entries)
    message = build_message(start,
                            end,
                            args.workhours,
                            grouped_entries)
    if args.send_by_mail and args.email_to and args.email_from:
        send_by_email(message,
                      args.smtp,
                      args.smtp_port,
                      args.starttls,
                      args.login,
                      args.password,
                      args.email_to,
                      args.email_from,
                      args.subject)
    else:
        print message
