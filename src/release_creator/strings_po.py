# *
# *  Copyright (C) 2012-2014 Garrett Brown
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *

from environment import Environment

import os
import unittest

STRINGS_PO  = 'strings.po'

class StringsPo:
    @staticmethod
    def GetFileName():
        return STRINGS_PO
    
    def __init__(self, addonXml):
        self._id = addonXml.GetProperty('id')
        self._path = os.path.join(Environment.GetStringsDir(self._id), STRINGS_PO)
        self._addonXml = addonXml
    
    def IsValid(self):
        return os.path.exists(self._path)
    
    def ReadPo(self):
        """
        Read strings.po file
        """
        if self.IsValid():
            with open(self._path) as f:
                return '\n'.join([self._addonXml.ReplaceTokens(line.strip()) for line in f.read().splitlines()])
        return ''

class TestSettingsXml(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_file_name(self):
        self.assertTrue(StringsPo.GetFileName(), STRINGS_PO)

if __name__ == '__main__':
    unittest.main()
