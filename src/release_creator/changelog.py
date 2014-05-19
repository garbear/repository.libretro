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

import unittest

FILENAME           = 'changelog.txt'
VERSIONED_FILENAME = 'changelog-%s.txt' # %s is version, e.g. 1.0.0

class ChangeLog:
    @staticmethod
    def GetFileName():
        return FILENAME
    
    @staticmethod
    def GetVersionedFileName(version):
        """
        In the release dir changelog is appended with version, e.g.
        changelog-1.0.0.txt
        """
        return VERSIONED_FILENAME % version
    
    def __init__(self):
        pass
    
    def IsValid(self):
        return True # Nothing to be invalid yet
    
    def GetText(self):
        return '' # TODO
    
    def Save(self):
        return True # TODO
    
    def CreateRelease(self):
        #with open(os.path.join(Environment.GetReleaseDir(addon.GetID()), VERSIONED_FILENAME % version), 'w') as f:
        return True # TODO

class TestChangelog(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_change_log(self):
        from libretro_super import LibretroSuper
        from addon import Addon
        
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
