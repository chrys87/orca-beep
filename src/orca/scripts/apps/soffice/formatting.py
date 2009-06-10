# Orca
#
# Copyright 2005-2009 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Custom formatting for OpenOffice and StarOffice."""

__id__ = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc."
__license__   = "LGPL"

# pylint: disable-msg=C0301

import copy

import pyatspi

import orca.formatting

formatting = {
    'speech': {
        # Get rid of unselectedCell because we don't run into that in OOo
        # and we'd end up always speaking "not selected" for all table cells.
        #
        'suffix': {
            'focused': '[]',
            'unfocused': 'newNodeLevel + tutorial',
            'basicWhereAmI': 'tutorial + description',
            'detailedWhereAmI' : '[]'
            },
        pyatspi.ROLE_COMBO_BOX: {
            'focused': 'name + availability',
            'unfocused': 'labelAndName + roleName + availability'
            },
        pyatspi.ROLE_PUSH_BUTTON: {
            'unfocused': 'labelAndName + roleName + toggleState + availability',
            'focused': 'labelAndName + toggleState'
            },
        pyatspi.ROLE_TOGGLE_BUTTON: {
            'focused': 'labelAndName + toggleState'
            },
        'ROLE_SPREADSHEET_CELL': {
            # We treat spreadsheet cells differently from other table cells in
            # whereAmI.
            #
            'basicWhereAmI': 'roleName + column + columnHeader + row + rowHeader + (textContent or spreadSheetCell) + anyTextSelection'
            },
    }
}

class Formatting(orca.formatting.Formatting):
    def __init__(self, script):
        orca.formatting.Formatting.__init__(self, script)
        self.update(copy.deepcopy(formatting))
