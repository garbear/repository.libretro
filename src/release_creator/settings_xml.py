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

SETTINGS_XML  = 'settings.xml'

class SettingsXml:
    @staticmethod
    def GetFileName():
        return SETTINGS_XML
    
    def __init__(self, addonId):
        self._id = addonId
        self._path = os.path.join(Environment.GetResourceDir(addonId), SETTINGS_XML)
    
    def IsValid(self):
        return os.path.exists(self._path)
    
    def ReadXml(self):
        if self.IsValid():
            with open(self._path) as f:
                return f.read()
        return ''

class TestSettingsXml(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_file_name(self):
        self.assertTrue(SettingsXml.GetFileName(), SETTINGS_XML)
    
    def test_read_xml(self):
        settingsXml = SettingsXml('gameclient.desmume')
        self.assertTrue(settingsXml.IsValid())
        self.assertNotEqual(settingsXml.ReadXml(), '')

if __name__ == '__main__':
    unittest.main()
