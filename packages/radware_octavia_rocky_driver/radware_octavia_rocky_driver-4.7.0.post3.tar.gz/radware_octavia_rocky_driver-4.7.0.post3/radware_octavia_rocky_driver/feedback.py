# Copyright 2018, Radware LTD. All rights reserved
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

from octavia.api.drivers import driver_lib
from octavia.common import constants

LOG = logging.getLogger(__name__)


def _report_status(status):
    LOG.debug("Updating statuses:" + repr(status))
    driver_lib.DriverLibrary().update_loadbalancer_status(status)


def _report_stats(stats):
    LOG.debug("Updating statistics:" + repr(stats))
    driver_lib.DriverLibrary().update_listener_statistics(stats)


def post_lb_create(**kwargs):
    result = kwargs.get('result')
    lb_id = kwargs.get('lb_id')
    status_dict = {constants.LOADBALANCERS: [{'id': lb_id}]}

    if result[3]['success']:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ACTIVE
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ONLINE
    else:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ERROR
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def post_lb_configure(**kwargs):
    deleted_id = kwargs.get('deleted_id')
    status_dict = kwargs.get('statuses')
    result = kwargs.get('result')
    success = result[3]['success']

    for type, objects in status_dict.items():
        for object in objects:
            if success:
                if deleted_id and object['id'] == deleted_id:
                    object[constants.PROVISIONING_STATUS] = constants.DELETED
                else:
                    object[constants.PROVISIONING_STATUS] = constants.ACTIVE
                    object[constants.OPERATING_STATUS] = constants.ONLINE
            else:
                object[constants.PROVISIONING_STATUS] = constants.ERROR
                object[constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def post_lb_delete(**kwargs):
    result = kwargs.get('result')
    lb_id = kwargs.get('lb_id')

    status_dict = {constants.LOADBALANCERS: [{'id': lb_id}]}

    if result[3]['success']:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.DELETED
    else:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ERROR
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def update_operating_status(**kwargs):
    result = kwargs.get('result')
    if not result[3]['success']:
        LOG.error('Failed to get loadbalancer status')
        return

    statuses = result[3]['parameters']['status']
    LOG.info('Status received:' + repr(statuses))

    statuses_dict = {constants.LOADBALANCERS: [
        {'id': _dash_uuid(statuses['id']), constants.OPERATING_STATUS: statuses['status']}]}

    listeners_list = []
    pools_list = []
    members_list = []

    for l in statuses['listeners']:
        listeners_list.append({'id': _dash_uuid(l['id']), constants.OPERATING_STATUS: _convert_status(l['status'])})
    for p in statuses['pools']:
        pools_list.append({'id': _dash_uuid(p['id']), constants.OPERATING_STATUS: _convert_status(p['status'])})
        for m in p['members']:
            members_list.append({'id': _dash_uuid(m['id']), constants.OPERATING_STATUS: _convert_status(m['status'])})
    statuses_dict['listeners'] = listeners_list
    statuses_dict['pools'] = pools_list
    statuses_dict['members'] = members_list
    _report_status(statuses_dict)


def update_statistics(**kwargs):
    result = kwargs.get('result')
    if not result[3]['success']:
        LOG.error('Failed to get loadbalancer statistics')
        return

    stats = result[3]['parameters']['stats']
    LOG.info('Stats received:' + repr(stats))

    listeners_list = []
    for l in stats['virts']:
        l['id'] = _dash_uuid(l['id'])
        l['request_errors'] = 0
        listeners_list.append(l)
    stats_dict = {constants.LISTENERS: listeners_list}
    _report_stats(stats_dict)


def _dash_uuid(uuid):
    return uuid[:8] + "-" + uuid[8:12] + "-" + uuid[12:16] + "-" + uuid[16:20]+ "-" + uuid[20:32]


def _convert_status(status):
    return constants.OFFLINE if status == 'DISABLED' else status

