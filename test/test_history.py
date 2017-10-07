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

import sys

import unittest2
from PyQt5.QtWidgets import QApplication, QWidget

from alignak_app.core.utils import init_config
from alignak_app.panel.history_widget import HistoryQWidget, AppQWidget


class TestHistory(unittest2.TestCase):
    """
        This file test the History class.
    """

    history_test = [
        {
            '_updated': 'Tue, 19 Sep 2017 13:07:16 GMT',
            'service_name': 'Load',
            'type': 'ack.processed',
            'message': 'Service Load acknowledged by admin, from Alignak-app',
        },
        {
            '_updated': 'Tue, 19 Sep 2017 13:07:01 GMT',
            'service_name': 'Load',
            'type': 'downtime.add',
            'message': 'Service Load acknowledged by admin, from Alignak-app',
         },
        {
            '_updated': 'Tue, 19 Sep 2017 13:05:26 GMT',
            'service_name': 'Memory',
            'type': 'check.result',
            'message': 'UNREACHABLE[HARD] (False/False): ERROR: netsnmp : No response from ...',
        },
        {
            '_updated': 'Tue, 19 Sep 2017 13:05:26 GMT',
            'service_name': 'NetworkUsage',
            'type': 'check.result',
            'message': 'UNREACHABLE[HARD] (False/False): ERROR: Description table : ...',
        }
    ]

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize History"""

        init_config()
        under_test = HistoryQWidget(self.history_test)

        self.assertTrue(under_test.history)
        self.assertIsNone(under_test.layout())
        self.assertIsInstance(under_test.app_widget, AppQWidget)
        self.assertIsNone(under_test.refresh_btn)

        under_test.initialize('charnay', 'id')

        self.assertIsNotNone(under_test.layout())
        self.assertIsNotNone(under_test.refresh_btn)
        self.assertEqual(under_test.refresh_btn.objectName(), 'id')
        self.assertEqual(under_test.app_widget.windowTitle(), "History of Charnay")

    def test_get_event_widget(self):
        """Get Event QWidget"""

        init_config()

        hist_widget_test = HistoryQWidget(self.history_test)

        under_test = hist_widget_test.get_event_widget(self.history_test[0])

        self.assertTrue("ack.processed" in under_test.toolTip())
        self.assertIsNotNone(under_test.layout())
        self.assertIsInstance(under_test, QWidget)
