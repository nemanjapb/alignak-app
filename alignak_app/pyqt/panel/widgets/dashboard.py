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
    Dashboard manage the creation of Hosts and Services resume QWidgets
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, QLabel, Qt, QWidget, QTimer, QPushButton, QIcon

from alignak_app.core.utils.config import app_css, get_image, get_app_config
from alignak_app.core.utils.config import open_url, get_url_endpoint_from_icon_name
from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.host import Host
from alignak_app.core.models.service import Service

logger = getLogger(__name__)


class DashboardQWidget(QWidget):
    """
        Class who manage Host and Services resume QWidgets with number of:
        - hosts: UP, UNREACHABLE, DOWN, ACKNOWLEDGED, DOWNTIMED
        - services: OK, WARNING, CRITICAL, UNKNWON, UNREACHABLE, ACKNOWLEDGED, DOWNTIMED
    """

    def __init__(self, parent=None):
        super(DashboardQWidget, self).__init__(parent)
        self.setStyleSheet(app_css)
        # Fields
        self.layout = QGridLayout()
        self.items_nb = {
            'hosts_nb': QLabel(),
            'services_nb': QLabel()
        }
        self.hosts_labels = {
            'hosts_up': QLabel(),
            'hosts_unreachable': QLabel(),
            'hosts_down': QLabel(),
            'acknowledge': QLabel(),
            'downtime': QLabel()
        }
        self.services_labels = {
            'services_ok': QLabel(),
            'services_warning': QLabel(),
            'services_critical': QLabel(),
            'services_unknown': QLabel(),
            'services_unreachable': QLabel(),
            'acknowledge': QLabel(),
            'downtime': QLabel()
        }
        self.hosts_buttons = {
            'hosts_up': QPushButton(),
            'hosts_unreachable': QPushButton(),
            'hosts_down': QPushButton(),
            'acknowledge': QPushButton(),
            'downtime': QPushButton()
        }
        self.services_buttons = {
            'services_ok': QPushButton(),
            'services_warning': QPushButton(),
            'services_critical': QPushButton(),
            'services_unknown': QPushButton(),
            'services_unreachable': QPushButton(),
            'acknowledge': QPushButton(),
            'downtime': QPushButton()
        }
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.setLayout(self.layout)

        self.get_host_resume_widget()
        self.get_services_resume_widget()

        self.update_dashboard()

        update_dashboard = int(get_app_config('Alignak-app', 'update_dashboard')) * 1000
        self.refresh_timer.setInterval(update_dashboard)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_dashboard)

    def get_host_resume_widget(self):
        """
        Return Host resume QWidget

        """

        self.layout.addWidget(QLabel('<b>Hosts:</b>'), 0, 0, 1, 1)
        self.items_nb['hosts_nb'].setObjectName('dashboard')
        self.layout.addWidget(self.items_nb['hosts_nb'], 1, 0, 1, 1)
        row = 1
        for icon in Host.get_available_icons():
            self.hosts_buttons[icon].setIcon(QIcon(get_image(icon)))
            self.hosts_buttons[icon].setFixedSize(48, 24)
            self.hosts_buttons[icon].setObjectName(icon)
            self.hosts_buttons[icon].setToolTip(
                _('Hosts %s. See in WebUI ?') % icon.replace('hosts_', '').upper()
            )
            self.hosts_buttons[icon].clicked.connect(
                lambda: self.open_item_type_url('hosts')
            )
            self.layout.addWidget(self.hosts_buttons[icon], 0, row, 1, 1)
            self.layout.setAlignment(self.hosts_buttons[icon], Qt.AlignCenter)
            self.hosts_labels[icon].setObjectName(icon)
            self.layout.addWidget(self.hosts_labels[icon], 1, row, 1, 1)
            self.layout.setAlignment(self.hosts_labels[icon], Qt.AlignCenter)
            row += 1

    def get_services_resume_widget(self):
        """
        Return Services resume QWidget

        """

        self.layout.addWidget(QLabel('<b>Services:</b>'), 2, 0, 1, 1)
        self.items_nb['services_nb'].setObjectName('dashboard')
        self.layout.addWidget(self.items_nb['services_nb'], 3, 0, 1, 1)
        row = 1
        for icon in Service.get_available_icons():
            self.services_buttons[icon].setIcon(QIcon(get_image(icon)))
            self.services_buttons[icon].setFixedSize(48, 24)
            self.services_buttons[icon].setObjectName(icon)
            self.services_buttons[icon].setToolTip(
                _('Services %s. See in WebUI ?') % icon.replace('services_', '').upper()
            )
            self.services_buttons[icon].clicked.connect(
                lambda: self.open_item_type_url('services')
            )
            self.layout.addWidget(self.services_buttons[icon], 2, row, 1, 1)
            self.layout.setAlignment(self.services_buttons[icon], Qt.AlignCenter)
            self.services_labels[icon].setObjectName(icon)
            self.layout.addWidget(self.services_labels[icon], 3, row, 1, 1)
            self.layout.setAlignment(self.services_labels[icon], Qt.AlignCenter)
            row += 1

    def open_item_type_url(self, item_type):
        """
        Retrieve sender to send right endpoint to open_url() function for item type

        :param item_type: type of item: hosts | services
        :type item_type: str
        """

        endpoint = self.sender().objectName()

        open_url('%s%s' % (item_type, get_url_endpoint_from_icon_name(endpoint)))

    def update_dashboard(self):
        """
        Update number of items in dashboard

        """

        synthesis = data_manager.get_synthesis_count()

        logger.info('Update Dashboard QWidget...')

        hosts_sum = 0
        for item in synthesis['hosts']:
            hosts_sum += synthesis['hosts'][item]
        services_sum = 0
        for item in synthesis['services']:
            services_sum += synthesis['services'][item]

        self.items_nb['hosts_nb'].setText("%d hosts" % hosts_sum)
        for icon in Host.get_available_icons():
            host_nb = synthesis['hosts'][icon.replace('hosts_', '')]
            percent = 0.0
            try:
                percent = float(host_nb) * 100.0 / float(hosts_sum)
            except ZeroDivisionError as e:
                logger.error(e)
            item_text = '%d (%.02f%%)' % (host_nb, percent)
            self.hosts_labels[icon].setText(item_text)

        self.items_nb['services_nb'].setText("%d services" % services_sum)
        for icon in Service.get_available_icons():
            service_nb = synthesis['services'][icon.replace('services_', '')]
            percent = 0.0
            try:
                percent = float(service_nb) * 100.0 / float(services_sum)
            except ZeroDivisionError as e:
                logger.error(e)
            item_text = '%d (%.01f%%)' % (service_nb, percent)
            self.services_labels[icon].setText(item_text)

        for button in self.hosts_buttons:
            if get_app_config('Alignak', 'webui'):
                self.hosts_buttons[button].setEnabled(True)
                self.hosts_buttons[button].setToolTip(
                    _('Hosts %s. See in WebUI ?') % button.replace('hosts_', '').upper()
                )
            else:
                self.hosts_buttons[button].setToolTip(
                    _("Hosts %s. WebUI is not set in configuration file.") % button.replace(
                        'hosts_', '').upper()
                )

        for button in self.services_buttons:
            if get_app_config('Alignak', 'webui'):
                self.services_buttons[button].setEnabled(True)
                self.services_buttons[button].setToolTip(
                    _('Services %s. See in WebUI ?') % button.replace('services_', '').upper()
                )
            else:
                self.services_buttons[button].setToolTip(
                    _("Services %s. WebUI is not set in configuration file.") % button.replace(
                        'services_', '').upper()
                )
