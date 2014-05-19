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
import time
import unittest

PROJECT_NAME_PREFIX = 'libretro-'

class LibretroProject:
    @staticmethod
    def GetProjectNamePrefix():
        """
        Libretro projects start with 'libretro-', e.g. libretro-bnes.        
        """
        return PROJECT_NAME_PREFIX
    
    def __init__(self, projectDir):
        self._projectDir = projectDir
        
        # Project name is directory name minus PROJECT_NAME_PREFIX
        self._name = ''
        filename = os.path.split(self._projectDir)[1]
        if filename.startswith(PROJECT_NAME_PREFIX):
            self._name = filename[len(PROJECT_NAME_PREFIX) : ]
        
        self._versionHash = self._ComputeVersionHash()
        self._date = self._ComputeDate()
    
    def _ComputeVersionHash(self):
        """
        Get the SHA-1 hash of the HEAD commit.
        """
        gitHash = None
        if os.path.exists(self._projectDir):
            gitHash = Environment.CheckOutput(self._projectDir, ['git', 'rev-parse', 'HEAD'])
            
            # If git rev-parse returned an error message, expect it to contain spaces
            if ' ' in gitHash:
                gitHash = None
        return gitHash
    
    def _ComputeDate(self):
        """
        Get the date of the HEAD commit. YYYY-M-D
        """
        gitDate = None
        
        if os.path.exists(self._projectDir):
            commitTime = Environment.CheckOutput(self._projectDir,
                                                 ['git', 'log', '-1', '--format=%ct'])
            if ' ' not in commitTime:
                date = time.gmtime(int(commitTime))
                gitDate = '%s-%s-%s' % (date.tm_year, date.tm_mon, date.tm_mday)
        
        return gitDate
    
    def IsValid(self):
        if not self._name:
            return False # Project directory didn't start with PROJECT_NAME_PREFIX
        if not self._versionHash:
            return False
        return True
    
    def GetName(self):
        return self._name
    
    def GetVersionHash(self):
        return self._versionHash
    
    def GetDate(self):
        return self._date

class TestLibretroProject(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_libretro_project(self):
        from libretro_super import LibretroSuper
        libretroSuper = LibretroSuper()
        
        projects = libretroSuper.GetProjects()
        self.assertNotEqual(len(projects), 0)
        
        for project in projects:
            # GetProjects() only returns valid projects, but we can check anyway
            self.assertTrue(project.IsValid())

if __name__ == '__main__':
    unittest.main()
