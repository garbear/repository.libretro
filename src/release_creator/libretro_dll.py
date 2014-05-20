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

from addon_xml import AddonXml
from libretro_info import LibretroInfo

import os
import unittest

LIBRETRO_SUFFIX = '_libretro'
INFO_SUFFIX     = LIBRETRO_SUFFIX + LibretroInfo.GetInfoExtension()
GAMECLIENT_ID   = 'gameclient.%s'

class LibretroDll:
    """
    Class representing a libretro DLL.
    """
    def __init__(self, path, libretroSuper):
        self._path = path
        
        # Name is the filename before LIBRETRO_SUFFIX 
        filename = os.path.split(path)[1]
        self._name = filename.split(LIBRETRO_SUFFIX)[0]
        
        self._info = LibretroInfo(os.path.join(libretroSuper.GetInfoDir(), self._name + INFO_SUFFIX))
        
        self._project = libretroSuper.GetProject(self._name)
    
    def IsValid(self):
        if not self._name:
            return False
        if not self._info or not self._info.IsValid():
            return False
        if not self._project or not self._project.IsValid():
            return False
        return True
    
    def GetAddonXml(self):
        return AddonXml(self.GetID(), self.GetInfo())
    
    def GetPath(self):
        return self._path
    
    def GetID(self):
        return GAMECLIENT_ID % self._name.replace('_', '.')
    
    def GetInfo(self):
        return self._info
    
    def GetProject(self):
        return self._project

class TestLibretroDll(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_libretro_dll(self):
        from libretro_super import LibretroSuper
        libretroSuper = LibretroSuper()
        
        dlls = libretroSuper.GetDlls()
        self.assertNotEqual(len(dlls), 0)
        
        for dll in dlls:
            # GetDlls() only returns valid DLLs, but we can check anyway
            self.assertTrue(dll.IsValid())

if __name__ == '__main__':
    unittest.main()
