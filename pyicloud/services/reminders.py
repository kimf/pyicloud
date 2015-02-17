from __future__ import absolute_import
import os

class RemindersService(object):
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._calendar_endpoint = '%s/ca' % self._service_root
        self._calendar_refresh_url = '%s/events' % self._calendar_endpoint
        self._calendar_event_detail_url = '%s/eventdetail' % self._calendar_endpoint
        self._reminders_endpoint = '%s/rd' % self._service_root
        self._reminders_active_url = '%s/startup' % self._reminders_endpoint
        self._reminders_completed_url = '%s/completed' % self._reminders_endpoint

    def get_system_tz(self):
        """
        Retrieves the system's timezone.
        From: http://stackoverflow.com/a/7841417
        """
        return '/'.join(os.readlink('/etc/localtime').split('/')[-2:])

    def refresh_completed_client(self):
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        params = dict(self.params)

        params.update({
            'lang': 'en-us',
            # 'usertz': self.get_system_tz(),
            'usertz':'America/Indianapolis',
        })
        req = self.session.get(self._reminders_completed_url, params=params)

        self.response = req.json()

        # print self.response.Collections
        for key, value in self.response.iteritems():
            print key


    def completed(self):
        self.refresh_completed_client()

    def refresh_active_client(self):
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        params = dict(self.params)

        params.update({
            'lang': 'en-us',
            'usertz':'America/Indianapolis',
        })

        req = self.session.get(self._reminders_active_url, params=params)

        self.response = req.json()

    def active(self):
        self.refresh_active_client()
