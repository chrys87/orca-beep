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

"""Speaks information about the current object of interest."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi
import debug
import speech

# [[[TODO: WDW - need to handle the old _speakText functionality that changes
# settings.verbalizePunctuationStyle = settings.PUNCTUATION_STYLE_SOME
# if we're doing an extended where am I.]]]

class WhereAmI:

    def __init__(self, script):
        """Create a new WhereAmI that will be used to speak information
        about the current object of interest.
        """

        self._script = script
        self._debugLevel = debug.LEVEL_FINEST
        self._lastAttributeString = ""

    def whereAmI(self, obj, basicOnly):
        """Speaks information about the current object of interest, including
        the object itself, which window it is in, which application, which
        workspace, etc.

        The object of interest can vary depending upon the mode the user
        is using at the time. For example, in focus tracking mode, the
        object of interest is the object with keyboard focus. In review
        mode, the object of interest is the object currently being visited,
        whether it has keyboard focus or not.
        """

        if (not obj):
            return False

        role = obj.getRole()
        if role in [pyatspi.ROLE_ENTRY,
                    pyatspi.ROLE_TEXT,
                    pyatspi.ROLE_PASSWORD_TEXT,
                    pyatspi.ROLE_TERMINAL,
                    pyatspi.ROLE_PARAGRAPH,
                    pyatspi.ROLE_SECTION,
                    pyatspi.ROLE_HEADING,
                    pyatspi.ROLE_DOCUMENT_FRAME]:
            self._speakText(obj, basicOnly)
        else:
            speech.speak(self.getWhereAmI(obj, basicOnly))

        return True

    def _speakText(self, obj, basicOnly):
        # [[[TODO: WDW - we handle ROLE_ENTRY specially here because
        # there is a bug in getRealActiveDescendant: it doesn't dive
        # deep enough into the hierarchy (see comment #12 of bug
        # #542714).  So, we'll do this nasty hack until we can feel
        # more comfortable with mucking around with
        # getRealActiveDescendant.]]]
        #
        ancestor = self._script.getAncestor(obj,
                                            [pyatspi.ROLE_TABLE_CELL,
                                             pyatspi.ROLE_LIST_ITEM],
                                            [pyatspi.ROLE_FRAME])
        if ancestor and not self._script.isLayoutOnly(ancestor.parent):
            if ancestor.getRole() == pyatspi.ROLE_TABLE_CELL:
                if obj.getRole() != pyatspi.ROLE_ENTRY:
                    speech.speak(self.getWhereAmI(ancestor, basicOnly))
                    return
            else:
                speech.speak(self.getWhereAmI(ancestor, basicOnly))
                return
        speech.speak(self.getWhereAmI(obj, basicOnly))

    def getWhereAmI(self, obj, basicOnly):
        """Returns an array of strings (and possibly voice and audio
        specifications) that represent the complete speech for the
        object.  The speech to be generated depends highly upon the
        speech formatting strings in formatting.py.
        """
        if basicOnly:
            formatType = 'basicWhereAmI'
        else:
            formatType = 'detailedWhereAmI'
        return self._script.speechGenerator.generateSpeech(
                   obj,
                   alreadyFocused=True,
                   formatType=formatType,
                   forceMnemonic=True,
                   forceTutorial=True)
