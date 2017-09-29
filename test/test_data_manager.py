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

import json

import unittest2

from alignak_app.core.backend import AppBackend
from alignak_app.core.data_manager import DataManager
from alignak_app.core.utils import init_config


class TestDataManager(unittest2.TestCase):
    """
        This file test the DataManager class.
    """

    init_config()
    params = {'where': json.dumps({'_is_template': False})}
    host_projection = ['name', 'alias', 'ls_state', '_id', 'ls_acknowledged', 'ls_downtimed',
                       'ls_last_check', 'ls_output', 'address', 'business_impact', 'parents',
                       'ls_last_state_changed']

    def test_initialize(self):
        """Initialize DataManager"""

        under_test = DataManager()

        self.assertTrue('host' in under_test.database)
        self.assertTrue('service' in under_test.database)
