# This file is part of rainbow
#
# rainbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# Copyright 2019 Victor Servant, Ledger SAS

from typing import List
from PyQt5 import QtWidgets as qt
from visplot import plot


class Interface(qt.QMainWindow):
    def __init__(self, instructions: List[str], *args, **kwargs):
        super().__init__()

        # Visplot widget
        self.plot_ = plot(*args, **kwargs, parent=self)
        self.plot_.canvas.connect(self.on_mouse_double_click)
        self.instr_ruler = None  # vertical ruler on selected instruction

        # Instructions list widget
        self.instr_list = qt.QListWidget(self)
        self.instr_list.currentRowChanged.connect(self.on_instr_list_row_change)
        self.instr_list.addItems(instructions)

        self.place_widgets()
        self.showMaximized()

    def on_instr_list_row_change(self, _event):
        """Event called when instructions list selection changes"""
        item = self.instr_list.currentItem()
        index = self.instr_list.row(item)
        self.focus_change(index)

    def focus_change(self, x: int):
        """Place vertical ruler on focused instruction"""
        # Delete previous ruler if exists
        if self.instr_ruler is not None:
            self.instr_ruler.parent = None

        self.instr_ruler = self.plot_.add_vertical_ruler(x)

    def place_widgets(self):
        """Build window structure

        QMainWindow > QFrame > QHBoxLayout > {self.instr_list, self.plot_}
        """
        self.frame = qt.QFrame(self)
        self.setCentralWidget(self.frame)

        self.frame_layout = qt.QHBoxLayout(self.frame)
        self.frame_layout.addWidget(self.instr_list)
        self.frame_layout.addWidget(self.plot_.canvas.native)

    def on_mouse_double_click(self, event):
        """Event called on double click in plot"""
        tr = self.plot_.canvas.scene.node_transform(self.plot_.view.scene)
        x, *_ = tr.map(event.pos)
        self.instr_list.setCurrentRow(int(x))
