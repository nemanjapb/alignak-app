#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

"""
    ItemService manage creation of service item
"""

import json
from logging import getLogger

from alignak_app.core.models.item import ItemModel

logger = getLogger(__name__)


class Service(ItemModel):
    """
        Class who create a service item
    """

    def __init__(self):
        super(Service, self).__init__()
        self.item_type = 'service'

    @staticmethod
    def get_request_model():
        """
        Return the request model for service requests

        :return: request model for service endpoint
        :rtype: dict
        """

        services_projection = [
            'name', 'alias', 'display_name', 'ls_state', 'ls_acknowledged', 'ls_downtimed',
            'ls_last_check', 'ls_output', 'business_impact', 'customs', '_overall_state_id',
            'aggregation', 'host'
        ]

        request = {
            'endpoint': 'service',
            'params': {'where': json.dumps({'_is_template': False})},
            'projection': services_projection
        }

        return request

    @staticmethod
    def get_service_states_nb():
        """
        Return all service state in a dict with int() as zero

        :return: all service state with int() as zero
        :rtype: dict
        """

        return {
            'OK': 0,
            'UNKNOWN': 0,
            'WARNING': 0,
            'UNREACHABLE': 0,
            'CRITICAL': 0,
            'ACKNOWLEDGE': 0,
            'DOWNTIME': 0
        }

    @staticmethod
    def get_available_icons():
        """
        Return list of available icons for a Service item

        :return: list of available icons for Service
        :rtype: list
        """

        return [
            'services_ok', 'services_warning', 'services_critical', 'services_unknown',
            'services_unreachable', 'acknowledge', 'downtime'
        ]

    def get_display_name(self):
        """
        Return alias or name if available

        :return: name or alias
        :rtype: str
        """

        if self.data['alias']:
            return self.data['alias'].capitalize()

        return self.data['name'].capitalize()
