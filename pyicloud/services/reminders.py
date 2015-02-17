from __future__ import absolute_import
from datetime import datetime, timedelta
from calendar import monthrange
import time

import pytz

class RemindersService(object):
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._reminders_endpoint = '%s/rd' % self._service_root
        self._reminders_active_url = '%s/startup' % self._reminders_endpoint

    def get_all_possible_timezones_of_local_machine(self):
        """
        Return all possible timezones in Olson TZ notation
        This has been taken from
        http://stackoverflow.com/questions/7669938
        """
        local_names = []
        if time.daylight:
            local_offset = time.altzone
            localtz = time.tzname[1]
        else:
            local_offset = time.timezone
            localtz = time.tzname[0]

        local_offset = timedelta(seconds=-local_offset)

        for name in pytz.all_timezones:
            timezone = pytz.timezone(name)
            if not hasattr(timezone, '_tzinfos'):
                continue
            for (utcoffset, daylight, tzname), _ in timezone._tzinfos.items():
                if utcoffset == local_offset and tzname == localtz:
                    local_names.append(name)
        return local_names

    def get_system_tz(self):
        """
        Retrieves the system's timezone from a list of possible options.
        Just take the first one
        """
        return self.get_all_possible_timezones_of_local_machine()[0]


    def refresh_client(self, from_dt=None, to_dt=None):
        """
        Refreshes the RemindersService endpoint, ensuring that the
        reminder data is up-to-date. If no 'from_dt' or 'to_dt' datetimes
        have been given, the range becomes this month.
        """
        today = datetime.today()
        first_day, last_day = monthrange(today.year, today.month)
        if not from_dt:
            from_dt = datetime(today.year, today.month, first_day)
        if not to_dt:
            to_dt = datetime(today.year, today.month, last_day)
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        params = dict(self.params)
        params.update({
            'lang': 'en-us',
            'usertz': self.get_system_tz(),
            'startDate': from_dt.strftime('%Y-%m-%d'),
            'endDate': to_dt.strftime('%Y-%m-%d')
        })
        req = self.session.get(self._reminders_active_url, params=params)
        self.response = req.json()

    def active(self, from_dt=None, to_dt=None):
        """
        Retrieves reminders for a given date range, by default, this month.
        """
        self.refresh_client(from_dt, to_dt)
        return self.response['Reminders']
