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
    History display the history of a host
"""


from logging import getLogger

from PyQt5.Qt import QPixmap, QIcon, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel  # pylint: disable=no-name-in-module

from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_css, get_image_path
from alignak_app.core.items.item_history import History
from alignak_app.frames.app_frame import AppQFrame, get_frame_separator

logger = getLogger(__name__)


class HistoryQWidget(QWidget):
    """
        Class who create the History QWidget for host
    """

    def __init__(self, parent=None):
        super(HistoryQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        self.setObjectName("history")
        # Fields
        self.app_widget = AppQFrame()
        self.refresh_btn = None

    def initialize(self, hostname, host_id):
        """
        Initialize History QWidget

        :param hostname: name of the host
        :type hostname: str
        :param host_id: Id of Host
        :type host_id: str
        """

        # Create ScrollArea
        scroll = QScrollArea()
        scroll.setWidget(self)
        scroll.setWidgetResizable(True)
        scroll.setMinimumSize(1000, 800)

        self.app_widget.initialize(_('History of %s') % hostname.capitalize())
        self.app_widget.layout().setSpacing(0)
        self.app_widget.add_widget(scroll)

        layout = QGridLayout()
        self.setLayout(layout)

        # History Description
        event_desc = QLabel(_("The last 25 events for %s") % hostname.capitalize())
        event_desc.setObjectName("title")
        layout.addWidget(event_desc, 0, 0, 1, 1)
        layout.setAlignment(event_desc, Qt.AlignCenter)

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon(get_image_path('refresh')))
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setObjectName(host_id)
        self.refresh_btn.setToolTip(_("Refresh history"))
        layout.addWidget(self.refresh_btn, 0, 1, 1, 1)
        layout.setAlignment(self.refresh_btn, Qt.AlignRight)

        # History QWidgets
        host_history_events = data_manager.get_item('history', host_id)
        line = 1

        for history_event in host_history_events.data:
            history_widget = self.get_hostory_widget_model(history_event, hostname)

            layout.addWidget(history_widget, line, 0, 2, 2)
            layout.addWidget(get_frame_separator(), line + 1, 0, 1, 2)

            line += 3

    @staticmethod
    def get_hostory_widget_model(event, hostname):
        """
        Create and return event QWidgets

        :param event: event of history given by backend
        :type event: dict
        :param hostname: name of host
        :type hostname: str
        :return: history Qwidget model with data
        :rtype: QWidget
        """

        history_widget_model = QWidget()
        history_widget_model.setToolTip(event['type'])
        history_widget_model.setObjectName("event")

        event_layout = QGridLayout()
        history_widget_model.setLayout(event_layout)

        if event['service_name']:
            event_name = event['service_name'].capitalize()
        else:
            event_name = hostname.capitalize()

        icon_name = History.get_history_icon_name_from_message(event['message'], event['type'])
        event_label = QLabel(event_name)
        event_label.setObjectName(icon_name)
        event_layout.addWidget(event_label, 0, 0, 1, 1)

        message_label = QLabel('%s' % event['message'])
        message_label.setWordWrap(True)
        event_layout.addWidget(message_label, 1, 0, 1, 1)

        icon = QPixmap(get_image_path(icon_name))
        icon_label = QLabel()
        icon_label.setToolTip(event['type'])
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(icon)
        icon_label.setScaledContents(True)

        event_layout.addWidget(icon_label, 0, 1, 2, 1)
        event_layout.setAlignment(icon_label, Qt.AlignVCenter)

        return history_widget_model
