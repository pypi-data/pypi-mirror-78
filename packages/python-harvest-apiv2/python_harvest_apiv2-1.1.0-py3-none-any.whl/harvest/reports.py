
# Copyright 2020 Bradbase
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools

from harvest import Harvest
from .harvestdataclasses import *

class Reports(Harvest):

    def __init__(self, *argsv, **kwargs):
        super(Reports, self).__init__(*argsv, **kwargs)
        self.client_cache = {}
        self.project_cache = {}
        self.task_cache = {}
        self.user_cache = {}

    def timeframe(self, timeframe, from_date = None, to_date = None):

        if timeframe == 'This Week':
            return {'from' : None, 'to' : None}

        elif timeframe == 'Last Week':
            pass

        elif timeframe == 'This Semimonth':
            pass

        elif timeframe == 'Last Semimonth':
            pass

        elif timeframe == 'This Month':
            pass

        elif timeframe == 'Last Month':
            pass

        elif timeframe == 'This Quarter':
            pass

        elif timeframe == 'Last Quarter':
            pass

        elif timeframe == 'This Year':
            pass

        elif timeframe == 'Last Year':
            pass

        elif timeframe == 'All Time':
            return {}

        elif timeframe == 'Custom':
            pass

    def show(self, hours):

        if hours == 'All Hours':
            pass

        elif hours == 'Billable Hours':
            pass

        elif hours == 'Non-Billable Hours':
            pass

        elif hours == 'Uninvoiced Billable Hours':
            pass

        elif hours == 'Uninvoiced Hours':
            pass

        elif hours == 'Invoiced Hours':
            pass


    # team is user
    def detailed_time(self, time_frame='All Time', clients=[None], projects=[None], tasks=[None], team=[None], include_archived_items=False, show='All Hours', group_by='Date', activeProject_only=False):
        arg_configs = []
        time_entry_results = DetailedTimeReport([])

        for element in itertools.product(clients, projects, team):
            kwargs = {}

            if element[0] !=None:
                kwargs['client_id'] = element[0]

            if element[1] !=None:
                kwargs['project_id'] = element[1]

            if element[2] !=None:
                kwargs['user_id'] = element[2]

            kwargs = dict(self.timeframe(time_frame), **kwargs)

            arg_configs.append(kwargs)

        tmp_time_entry_results = []
        if arg_configs == []:
            time_entries = self.time_entries()
            tmp_time_entry_results.extend(time_entries.time_entries)
            if time_entries.total_pages > 1:
                for page in range(2, time_entries.total_pages + 1):
                    time_entries = self.time_entries(page=page)
                    tmp_time_entry_results.extend(time_entries.time_entries)
        else:
            for config in arg_configs:
                time_entries = self.time_entries(**kwargs)
                tmp_time_entry_results.extend(time_entries.time_entries)
                if time_entries.total_pages > 1:
                    for page in range(2, time_entries.total_pages + 1):
                        time_entries = self.time_entries(page=page, **kwargs)
                        tmp_time_entry_results.extend(time_entries.time_entries)

        for time_entry in tmp_time_entry_results:
            user = None
            if time_entry.user.id not in self.user_cache.keys():
                user = self.get_user(time_entry.user.id)
                self.user_cache[time_entry.user.id] = user
            else:
                user = self.user_cache[time_entry.user.id]

            hours = time_entry.hours
            billable_amount = 0.0
            cost_amount = 0.0
            billable_rate = time_entry.billable_rate
            cost_rate = time_entry.cost_rate

            if hours is not None:
                if billable_rate is not None:
                    billable_amount = billable_rate * hours
                if cost_rate is not None:
                    cost_amount = cost_rate * hours

            time_entry_results.detailed_time_entries.append( DetailedTimeEntry(date=time_entry.spent_date, client=time_entry.client.name, project=time_entry.project.name, project_code=time_entry.project.code, task=time_entry.task.name, notes=time_entry.notes, hours=hours, billable=str(time_entry.billable), invoiced='', approved='', first_name=user.first_name, last_name=user.last_name, roles=user.roles, employee='Yes', billable_rate=billable_rate, billable_amount=billable_amount, cost_rate=cost_rate, cost_amount=cost_amount, currency=time_entry.client.currency, external_reference_url=time_entry.external_reference) )

        return time_entry_results
