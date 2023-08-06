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

import logging

from storops.unity.resource import UnityResource, UnityResourceList

__author__ = 'Ryan Liang'

log = logging.getLogger(__name__)


class UnityPotentialHost(UnityResource):
    pass


class UnityPotentialHostList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityPotentialHost


class UnityHostContainer(UnityResource):
    @classmethod
    def create(cls, cli, service_type, target_name, target_address, username,
               password, description=None, local_username=None,
               local_password=None, potential_hosts=None):
        vasa_provider_parameters = None
        if local_username and local_password:
            vasa_provider_parameters = {'localUsername': local_username,
                                        'localPassword': local_password}
        resp = cli.post(cls().resource_class,
                        serviceType=service_type,
                        targetName=target_name,
                        targetAddress=target_address,
                        username=username,
                        password=password,
                        description=description,
                        vasaProviderParameters=vasa_provider_parameters,
                        potentialHosts=potential_hosts)
        resp.raise_if_err()
        return cls(_id=resp.resource_id, cli=cli)

    @classmethod
    def recommend(cls, cli, address, username, password):
        """ Get a list of candidate hosts that can be imported for a VC or an
        ESXi server.

        :return: a tuple of (type, container_name, container_version,
            vasa_provider_state, potential_hosts), while type is of type
            `HostContainerTypeEnum` which is the type of the VC/ESXi server,
            container_name is the name of VC or ESXi server, container_version
            is the software version of VC or ESXi server,
            vasa_provider_state is of type `VasaProviderStateEnum` which
            indicates storage system’s VASA vendor provider state on the
            vCenter, potential_hosts is a list of `UnityPotentialHost` which is
            the list of candidate hosts that can be imported.
        """
        resp = cli.type_action(cls().resource_class,
                               'recommend',
                               address=address, username=username,
                               password=password)
        resp.raise_if_err()
        content = resp.first_content
        return (content.get('type'),
                content.get('containerName'),
                content.get('containerVersion'),
                content.get('vasaProviderState'),
                content.get('potentialHosts'))


class UnityHostContainerList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityHostContainer
