#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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

import unittest2
import configparser as cfg

from alignak_app.application import AlignakApp
from alignak_app.alignak_data import AlignakData

class TestApplication(unittest2.TestCase):
    """
        This file test methods of AlignakApp class.
    """

    def test_initialization(self):
        under_test = AlignakApp()

        # Test initialization of Class and assert items are created.
        self.assertIsNone(under_test.Config)
        self.assertIsNone(under_test.backend_data)
        self.assertIsNotNone(under_test.up_item)
        self.assertIsNotNone(under_test.down_item)
        self.assertIsNotNone(under_test.quit_item)

    def test_alignak_config(self):
        # Assert Config is None before read
        under_test = AlignakApp()
        self.assertIsNone(under_test.Config)

        # Assert Config is NOT None after read
        under_test.read_configuration()
        self.assertIsNotNone(under_test.Config)

    def test_get_state(self):
        under_test = AlignakApp()

        Config = cfg.ConfigParser()
        Config.read('./etc/settings.cfg')
        under_test.Config = Config

        under_test.backend_data = AlignakData()
        under_test.backend_data.log_to_backend(under_test.Config)

        # UP and DOWN must be Integer and positive
        UP, DOWN = under_test.get_state()

        self.assertIsInstance(UP, int)
        self.assertIsInstance(DOWN, int)
        self.assertGreater(UP, -1)
        self.assertGreater(DOWN, -1)



