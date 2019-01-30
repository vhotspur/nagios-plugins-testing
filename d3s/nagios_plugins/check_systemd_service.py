#!/usr/bin/env python3

import re
import argparse
from d3s.nagios import NagiosPluginBase


class CheckSystemdService(NagiosPluginBase):
    """
    Checks that given service is running and enabled.
    """

    DETAILS_BASE_RE = re.compile('''
        ^\\s+(Tasks|Memory):
        \\s+
        ([^ \t]+)
        .*$
        ''', re.VERBOSE)

    def __init__(self):
        NagiosPluginBase.__init__(self, 'SRV')
        parser = argparse.ArgumentParser()
        parser.add_argument('--service', dest='service', metavar='UNIT', required=True)
        args = parser.parse_args()
        self.service = args.service

    def collect(self):
        self.add_perf_data('service_name', self.service)

        is_enabled_output = self.read_command_output(['systemctl', 'is-enabled', self.service])
        is_enabled = self.contains_line(re.compile('^enabled$'), is_enabled_output)
        if not is_enabled:
            self.worsen_to_warning()

        is_active_output = self.read_command_output(['systemctl', 'is-active', self.service])
        is_active = self.contains_line(re.compile('^active$'), is_active_output)
        if not is_active:
            self.worsen_to_critical()

        for line in self.grep_lines(CheckSystemdService.DETAILS_BASE_RE, self.read_command_output(['systemctl', 'status', self.service])):
            key = line.group(1)
            if key == 'Tasks':
                self.add_perf_data('service_tasks', line.group(2))
            elif key == 'Memory':
                self.add_perf_data('service_memory', line.group(2))

        details = ', {service_memory}, {service_tasks} tasks'
        if not is_active:
            self.set_message_from_perf('{service_name} not running')
        elif not is_enabled:
            self.set_message_from_perf('{service_name} running but not enabled' + details)
        else:
            self.set_message_from_perf('{service_name} running' + details)


if __name__ == '__main__':
    import sys
    CheckSystemdService().run()
