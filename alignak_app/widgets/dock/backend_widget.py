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
    Livestate QWidget manage resume of hosts, services and problems
"""

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.data_manager import data_manager

from PyQt5.Qt import QWidget, QVBoxLayout, QHBoxLayout, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QPixmap, QTimer  # pylint: disable=no-name-in-module


class LivestateQWidget(QWidget):
    """
        Class who display hosts, services and problems number
    """

    def __init__(self):
        super(LivestateQWidget, self).__init__()
        self.setStyleSheet(get_css())
        # Fields
        self.labels = {
            'host': None,
            'service': None,
            'problem': None
        }
        self.timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        item_types = ['host', 'service', 'problem']

        for item_type in item_types:
            item_widget = self.get_item_type_widget(item_type, 0, 0)
            layout.addWidget(item_widget)

        self.update_labels()

        self.timer.setInterval(15000)
        self.timer.start()
        self.timer.timeout.connect(self.update_labels)

    def get_item_type_widget(self, item_type, problem_nb, total_nb):
        """
        Create and return QWidget with backend data

        :param item_type: type of item: host, service, problem
        :type item_type: str
        :param problem_nb: number of problems for item type
        :type problem_nb: int
        :param total_nb: total number of item type
        :type total_nb: int
        :return: widget with its data
        :rtype: QWidget
        """

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        problem_label = QLabel('%d' % problem_nb)
        problem_label.setObjectName('ko')
        problem_label.setToolTip(
            _('Number of unhandled %s problems') % (
                item_type if 'problem' not in item_type else ''
            )
        )
        layout.addWidget(problem_label)
        layout.setAlignment(problem_label, Qt.AlignCenter)

        icon_label = QLabel()
        layout.addWidget(icon_label)
        layout.setAlignment(icon_label, Qt.AlignCenter)

        total_label = QLabel('%d' % total_nb)
        total_label.setObjectName('total')
        total_label.setToolTip(
            _('Number of monitored %s') % (
                item_type if 'problem' not in item_type else 'items'
            )
        )
        layout.addWidget(total_label)
        layout.setAlignment(total_label, Qt.AlignCenter)

        self.labels[item_type] = {
            'problem': problem_label,
            'icon': icon_label,
            'total': total_label
        }

        return widget

    def update_labels(self):
        """
        Update Qlabels of widget

        """

        items_and_problems = self.get_items_and_problems()

        for item_type in self.labels:
            self.labels[item_type]['problem'].setText(
                '%s' % str(items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['icon'].setPixmap(
                self.get_icon_item(item_type, items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['total'].setText(
                '%s' % str(items_and_problems[item_type]['total'])
            )

    @staticmethod
    def get_icon_item(item_type, problem_nb):
        """
        Return QPixmap with the corresponding image

        :param item_type: type of item: host, service or problem
        :type item_type: str
        :param problem_nb: problem number
        :type problem_nb: int
        :return: QPixmap with corresponding image
        :rtype: QPixmap
        """

        if problem_nb > 0:
            if item_type == 'host':
                icon_type = 'hosts_down'
            elif item_type == 'service':
                icon_type = 'services_critical'
            else:
                icon_type = 'problem'
        else:
            if item_type == 'host':
                icon_type = 'hosts_up'
            elif item_type == 'service':
                icon_type = 'services_ok'
            else:
                icon_type = 'problem_ok'
        icon = QPixmap(get_image_path(icon_type))

        return icon

    @staticmethod
    def get_items_and_problems():
        """
        Return total of items and problems

        :return: dict of problem and total number for each item
        :rtype: dict
        """

        livesynthesis = data_manager.database['livesynthesis']

        hosts_total = 0
        hosts_problems = 0
        services_total = 0
        services_problems = 0
        for synth in livesynthesis:
            hosts_total += synth.data['hosts_total']
            hosts_problems += synth.data['hosts_down_soft']
            hosts_problems += synth.data['hosts_down_hard']

            services_total += synth.data['services_total']
            services_problems += synth.data['services_critical_soft']
            services_problems += synth.data['services_critical_hard']

        items_and_problems = {
            'host': {
                'problem': hosts_problems,
                'total': hosts_total
            },
            'service': {
                'problem': services_problems,
                'total': services_total
            },
            'problem': {
                'problem': hosts_problems + services_problems,
                'total': hosts_total + services_total
            }
        }

        return items_and_problems