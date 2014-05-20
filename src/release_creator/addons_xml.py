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
from md5_file import MD5File

import os
import unittest

ADDONS_XML       = 'addons.xml'
XML_DECLARATION  = '<?xml version="1.0" encoding="UTF-8"?>'
ADDONS_TAG_OPEN  = '<addons>'
ADDONS_TAG_CLOSE = '</addons>'

class AddonsXml:
    @staticmethod
    def GetFileName():
        return os.path.join(Environment.GetReleaseDir(), ADDONS_XML)
    
    def __init__(self, addons):
        self._addons = addons
    
    def Save(self):
        addonsXml = [XML_DECLARATION, ADDONS_TAG_OPEN]
        for addon in self._addons:
            addonXmlText = addon.GetAddonXmlText()
            
            # Remove leading <?xml> tag
            if addonXmlText.startswith(XML_DECLARATION[ : 5]):
                addonXmlText = addonXmlText.split('\n', 1)[1]
            
            addonsXml.append(addonXmlText)
        addonsXml.append(ADDONS_TAG_CLOSE)
        
        with open(AddonsXml.GetFileName(), 'w') as f:
            f.write('\n\n'.join(addonsXml))
        
        md5File = MD5File(AddonsXml.GetFileName())
        if md5File.Save():
            return True
        
        return False

class TestAddonsXml(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_addons_xml(self):
        from addon import Addon
        from libretro_super import LibretroSuper
        libretroSuper = LibretroSuper()
        
        dlls = libretroSuper.GetDlls()
        self.assertNotEqual(len(dlls), 0)
        
        addons = []
        for dll in dlls:
            addon = Addon(dll)
            self.assertTrue(addon.Save())
            self.assertTrue(addon.CreateRelease())
            addons.append(addon)
        
        addonsXml = AddonsXml(addons)
        self.assertTrue(addonsXml.Save())

if __name__ == '__main__':
    unittest.main()
