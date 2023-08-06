# coding=utf-8
# Copyright (c) 2020 Dell Inc. or its subsidiaries.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import unicode_literals

from unittest import TestCase

import ddt
from hamcrest import assert_that, equal_to

from storops.unity.enums import FilesystemSnapAccessTypeEnum, \
    ScheduleTypeEnum, ScheduleVersionEnum, HostContainerTypeEnum, \
    VasaProviderStateEnum
from storops.unity.resource.host_container import UnityHostContainer, \
    UnityHostContainerList
from storops_test.unity.rest_mock import t_rest, patch_rest

__author__ = 'Ryan Liang'


@ddt.ddt
class UnityHostContainerTest(TestCase):
    @patch_rest
    def test_properties(self):
        container = UnityHostContainer(_id='mss_3', cli=t_rest())
        assert_that(container.existed, equal_to(True))
        # TODO(ryan)
        # assert_that(container.version, equal_to(ScheduleVersionEnum.LEGACY))
        # assert_that(container.name, equal_to('Snapshot Schedule 1'))
        # assert_that(container.is_default, equal_to(False))
        # assert_that(container.is_modified, equal_to(False))
        # assert_that(str(container.modification_time),
        #             equal_to('2020-03-17 07:37:56.695000+00:00'))
        # assert_that(len(container.rules), equal_to(1))
        # assert_that(container.rules[0].type,
        #             equal_to(ScheduleTypeEnum.DAY_AT_HHMM))
        # assert_that(len(container.rules[0].days_of_week), equal_to(0))
        # assert_that(container.rules[0].access_type,
        #             equal_to(FilesystemSnapAccessTypeEnum.CHECKPOINT))
        # assert_that(container.rules[0].minute, equal_to(0))
        # assert_that(container.rules[0].hours, equal_to([4]))
        # assert_that(container.rules[0].interval, equal_to(1))
        # assert_that(container.rules[0].is_auto_delete, equal_to(True))
        # assert_that(container.rules[0].retention_time, equal_to(0))
        # assert_that(container.is_sync_replicated, equal_to(False))
        # assert_that(len(container.luns), equal_to(1))
        # assert_that(container.luns[0].get_id(), equal_to('sv_2'))

    @patch_rest
    def test_get_all(self):
        containers = UnityHostContainerList(cli=t_rest())
        assert_that(containers[0].existed, equal_to(True))
        assert_that(len(containers), equal_to(1))

    @patch_rest
    def test_create(self):
        _type, name, _, _, hosts = UnityHostContainer.recommend(
            t_rest(), address='172.18.15.201',
            username='administrator@vsphere.local', password='Test123!'
        )
        container = UnityHostContainer.create(
            t_rest(), _type,
            name, name, 'administrator@vsphere.local',
            'Test123!', local_username='admin', local_password='Test123!',
            potential_hosts=hosts
        )
        assert_that(container.get_id(), equal_to('mss_3'))

    @patch_rest
    def test_recommend(self):
        _type, name, version, state, hosts = UnityHostContainer.recommend(
            t_rest(),
            address='172.18.15.201',
            username='administrator@vsphere.local',
            password='Test123!')
        assert_that(_type, equal_to(2))
        assert_that(name, equal_to('172.18.15.201'))
        assert_that(version, equal_to('7.0.0'))
        assert_that(state, equal_to(0))
        assert_that(len(hosts), equal_to(3))

    # TODO(ryan)
    # @patch_rest
    # def test_delete(self):
    #     container = UnityHostContainer(_id='mss_3', cli=t_rest())
    #     resp = container.delete()
    #     assert_that(resp.is_ok(), equal_to(True))
