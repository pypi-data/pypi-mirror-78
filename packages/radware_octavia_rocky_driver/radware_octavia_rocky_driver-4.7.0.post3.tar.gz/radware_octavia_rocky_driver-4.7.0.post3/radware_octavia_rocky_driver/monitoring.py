# Copyright 2018 Radware LTD. All rights reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging
import threading
#import multiprocessing
import time

LOG = logging.getLogger(__name__)


class Monitor(threading.Thread):
    def __init__(self, driver,
                 status_feedback=None,
                 stats_feedback=None):
        #multiprocessing.Process.__init__(self)
        threading.Thread.__init__(self)

        self.driver = driver
        self.monitoring_pace = driver.config.monitoring_pace
        self.status_action_name = driver.config.status_action_name
        self.stats_action_name = driver.config.stats_action_name
        self.status_feedback = status_feedback
        self.stats_feedback = stats_feedback

        #self.stoprequest = multiprocessing.Event()
        self.stoprequest = threading.Event()
        self.name = 'STATUS_MONITOR'

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Monitor, self).join(timeout)

    def run(self):
        #while not self.stoprequest.is_set():
        while not self.stoprequest.isSet():
            time.sleep(self.monitoring_pace)
            lb_wf_names = self.driver.wf_driver.get_existing_lb_workflows()
            if not lb_wf_names or len(lb_wf_names) == 0:
                continue

            for wf_name in lb_wf_names:
                if self.status_feedback:
                    LOG.debug('STATUS: Running status action on:' + repr(wf_name))
                    result = self.driver.wf_driver.run_workflow_action(
                        self.driver.wf_driver._wf_lb_id(wf_name), self.status_action_name, {})
                    t = threading.Thread(
                        target=self.status_feedback,
                        kwargs=dict(result=result))
                    t.start()

                if self.stats_feedback:
                    LOG.debug('STATUS: Running stats action on:' + repr(wf_name))
                    result = self.driver.wf_driver.run_workflow_action(
                        self.driver.wf_driver._wf_lb_id(wf_name), self.stats_action_name, {})
                    t = threading.Thread(
                        target=self.stats_feedback,
                        kwargs=dict(result=result))
                    t.start()
