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
    Service QTreeWidgetItem subclass to store Service item data
"""

from logging import getLogger

from PyQt5.Qt import QIcon, QTreeWidgetItem

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.item import get_icon_name
from alignak_app.core.utils.config import get_image

logger = getLogger(__name__)


class ServicesTreeItem(QTreeWidgetItem):  # pylint: disable=too-few-public-methods
    """
        Class who create QTreeWidgetItem with service data
    """

    def __init__(self, parent=None):
        super(ServicesTreeItem, self).__init__(parent)
        self.service_item = None
        self.service_id = None

    def initialize(self, service_item):
        """
        Initialize the QTreeWidgetItem

        :param service_item: service item with its data
        :type service_item: alignak_app.core.models.service.Service
        """

        self.service_item = service_item
        self.service_id = service_item.item_id
        self.setText(0, self.service_item.get_display_name())

        icon_name = get_icon_name(
            'service',
            service_item.data['ls_state'],
            service_item.data['ls_acknowledged'],
            service_item.data['ls_downtimed']
        )

        self.setIcon(0, QIcon(get_image(icon_name)))

    def update_item(self):
        """
        Update QIcon of service

        """

        service = data_manager.get_item('service', '_id', self.service_id)
        logger.debug('Update current Service QTreeWidgetItem...')
        logger.debug('... for service: %s', service.name)

        icon_name = get_icon_name(
            'service',
            self.service_item.data['ls_state'],
            self.service_item.data['ls_acknowledged'],
            self.service_item.data['ls_downtimed']
        )

        self.setData(0, 0, service.get_display_name())
        self.setData(0, 1, QIcon(get_image(icon_name)))

        self.service_item = service

        assert service.item_id == self.service_id
