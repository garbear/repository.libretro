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

from addon_version import AddonVersion
from addon_xml import AddonXml
from changelog import ChangeLog
from environment import Environment
from release_archive import ReleaseArchive
from settings_xml import SettingsXml
from strings_po import StringsPo

import os
import unittest

class Addon:
    def __init__(self, dll):
        self._id             = dll.GetID()
        self._dll            = dll
        self._addonXml       = AddonXml(dll)
        self._changeLog      = ChangeLog() # TODO
        self._settingsXml    = SettingsXml(self._id)
        self._stringsPo      = StringsPo(self._addonXml)
        self._releaseArchive = ReleaseArchive(self._id)
        """
        # Get the most recent release
        maxVersion = Addon._GetMaxVersion(self.addonXml.)
        
        if releaseArchive.IsValid():
            self._addonVersion = maxVersion
            self._releaseArchive = releaseArchive
        else:
            self._addonVersion = AddonVersion(dll.GetInfo().GetDisplayVersion())
            self._releaseArchive = ReleaseArchive(self._id, self._addonVersion)
        """
    
    def IsValid(self):
        return self._dll.IsValid()       and \
               self._changeLog.IsValid() and \
               self._addonXml.IsValid()
    
    def GetID(self):
        return self._id
    
    def GetDll(self):
        return self._dll
    
    def GetAddonXml(self):
        return self._addonXml
    
    def GetAddonXmlText(self):
        return self._addonXml.GetAddonXml()
    
    def GetChangeLog(self):
        return self._changeLog
    
    def Save(self):
        """
        Save the addon components (addon.xml, changelog.txt and libretro
        library) to /addons folder.
        """
        return self._addonXml.Save() and self._changeLog.Save() and self._settingsXml.Save()
    
    def CreateRelease(self):
        """
        Create a release archive (and associated files like md5 and changelog)
        in the /release folder.
        """
        if not os.path.exists(Environment.GetReleaseDir(self._id)):
            os.makedirs(Environment.GetReleaseDir(self._id))
        
        return self._releaseArchive.Update(self._addonXml, self._changeLog, self._dll, self._settingsXml, self._stringsPo)

class TestAddonXml(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_addon(self):
        from libretro_super import LibretroSuper
        libretroSuper = LibretroSuper()
        
        dlls = libretroSuper.GetDlls()
        self.assertNotEqual(len(dlls), 0)
        
        for dll in dlls:
            # GetDlls() only returns valid DLLs, but we can check anyway
            self.assertTrue(dll.IsValid())
            
            addon = Addon(dll)
            self.assertTrue(addon.IsValid())
            self.assertTrue(addon.Save())
            self.assertTrue(addon.CreateRelease())

if __name__ == '__main__':
    unittest.main()
