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
    Dock manage creation of Alignak-app Dock
"""

import sys

from PyQt5.Qt import QApplication, QWidget, QGridLayout, QIcon, QListWidget, QLabel, Qt

from alignak_app.core.config import app_css, get_image
from alignak_app.widgets.dock.buttons import ButtonsQWidget
from alignak_app.widgets.dock.events import events_widget
from alignak_app.widgets.dock.livestate import LivestateQWidget
from alignak_app.widgets.dock.spy import SpyQWidget
from alignak_app.widgets.dock.status import StatusQWidget
from alignak_app.widgets.common.frames import AppQFrame, get_frame_separator


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        # Fields
        self.app_widget = AppQFrame()
        self.status_widget = StatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.livestate_widget = LivestateQWidget()
        self.spy_widgetlist = QListWidget()
        self.spy_widget = SpyQWidget()

    def initialize(self):
        """
        Initialize dock QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        # Add Alignak status
        status = QLabel(_('Alignak'))
        status.setObjectName('title')
        layout.addWidget(status)
        layout.setAlignment(status, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.status_widget.initialize()
        layout.addWidget(self.status_widget)

        layout.addWidget(self.buttons_widget)

        # Livestate
        livestate = QLabel(_('Livestate'))
        livestate.setObjectName('title')
        layout.addWidget(livestate)
        layout.setAlignment(livestate, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.livestate_widget.initialize()
        layout.addWidget(self.livestate_widget)

        # Last Events
        last_event_label = QLabel(_('Last Events'))
        last_event_label.setObjectName('title')
        layout.addWidget(last_event_label)
        layout.setAlignment(last_event_label, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        layout.addWidget(events_widget)

        # Spieds hosts
        spy_title = QLabel(_('Spied Hosts'))
        spy_title.setObjectName('title')
        layout.addWidget(spy_title)
        layout.setAlignment(spy_title, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.spy_widget.initialize()
        layout.addWidget(self.spy_widget)

        self.spy_widget.spied_list_widget.item_dropped.connect(events_widget.remove_event)

        self.set_size_and_position()

    def set_size_and_position(self):
        """
        Set the size and postion of DockQWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        x_size = desktop.width() * 0.2
        y_size = desktop.height()

        self.app_widget.initialize('', logo=True)
        self.app_widget.add_widget(self)
        self.app_widget.resize(x_size, y_size)

        if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
            pos_x = desktop.width() - (x_size * 0.5)
        else:
            pos_x = desktop.width() - x_size

        self.app_widget.move(pos_x, 0)

        # Give width for PanelQWidget
        self.buttons_widget.initialize(self.app_widget.width(), self.spy_widget)

    def show_dock(self):
        """
        Show the dock by making AppQWidget window active

        """

        self.app_widget.show()

        self.buttons_widget.panel_widget.dock_width = self.app_widget.width()
        QWidget.activateWindow(self.app_widget)