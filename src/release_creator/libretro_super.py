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
from libretro_dll import LibretroDll
from libretro_project import LibretroProject
from utils import getClosestMatch

import os
import subprocess
import unittest

LIBRETRO_SUPER_GIT     = 'git://github.com/libretro/libretro-super.git'
LIBRETRO_SUPER_DIRNAME = 'libretro-super'
PLATFORM_WIN           = 'win'
PLATFORM_UNIX          = 'unix'
PLATFORM_OSX           = 'osx'
INFO_EXTENSION         = '.info'
FETCH_CMD              = 'libretro-fetch.sh'
BUILD_UNIX_CMD         = 'libretro-build.sh'
BUILD_OSX_CMD          = 'libretro-build.sh'
BUILD_WIN_CMD          = 'libretro-build-win.sh' 

class LibretroSuper:
    """
    libretro-super is a buildsystem for generating RetroArch and its libretro cores.
    The buildsystem is cloned from LIBRETRO_SUPER_GIT. This class contains
    operations performed on or by libretro-super.
    
    libretro-super fetch libretro projects from all corners of the earth (but mainly
    https://github.com/libretro). These projects are cloned to subfolders in the
    libretro-super directory, and can be analyzed using GetProjects().
    """
    
    @staticmethod
    def GetPlatform():
        """
        Libretro's build system has three platforms that we're currently concerned
        about: 'win', 'osx' and 'unix'.
        """
        if   Environment.GetPlatform() == Environment.WIN:         return 'win'
        elif Environment.GetPlatform() == Environment.OSX32   or \
             Environment.GetPlatform() == Environment.OSX32:       return 'osx'
        elif Environment.GetPlatform() == Environment.LINUX32 or \
             Environment.GetPlatform() == Environment.LINUX64:     return 'unix' # Used for all linux platforms. Note: not 'linux'!
        raise Exception('Libretro-super doesn\'t support platform %s yet' % Environment.GetPlatform())
    
    @staticmethod
    def GetRepoDir():
        """
        Get the directory that libretro-super will be cloned into (/libretro-super).
        """
        return os.path.join(Environment.GetRootDir(), LIBRETRO_SUPER_DIRNAME)
    
    @staticmethod
    def GetDllDir():
        """
        Compiled libretro binaries are placed in in a folder named after the
        platform at /libretro-super/dist.
        """
        return os.path.join(LibretroSuper.GetRepoDir(), 'dist', LibretroSuper.GetPlatform())
    
    @staticmethod
    def GetInfoDir():
        """
        Info files describing 
        """
        return os.path.join(LibretroSuper.GetRepoDir(), 'dist', 'info')
    
    @staticmethod
    def RunScript(scriptName):
        """
        Run the specified script in the repo directory.
        """
        Environment.RunScript(os.path.join(LibretroSuper.GetRepoDir(), scriptName))
    
    def __init__(self):
        self._InitalizeVariables()
    
    def _InitalizeVariables(self):
        self._branch = self._ComputeBranch()
    
    def _ComputeBranch(self):
        branch = None
        
        if os.path.exists(LibretroSuper.GetRepoDir()):
            branch = Environment.CheckOutput(LibretroSuper.GetRepoDir(),
                                             ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
            
            # If git rev-parse returned an error message, expect it to contain spaces
            if ' ' in branch:
                branch = None
        
        return branch
    
    def IsValid(self):
        """
        Repo is valid if constructor was able to initialize everything.
        """
        if not self._branch:
            return False
        return True
    
    def GetBranch(self):
        return self._branch
    
    def CloneIfNotValid(self):
        if not self.IsValid():
            if os.path.exists(LibretroSuper.GetRepoDir()):
                return False # TODO: Path exists but isn't a git repository?
            subprocess.call(['git', 'clone', LIBRETRO_SUPER_GIT, LibretroSuper.GetRepoDir()])
            self._InitalizeVariables()
        return self.IsValid()
    
    def GetProjects(self):
        """
        A project is a subfolder of /libretro-super. Projects are cloned from
        their respective repos using libretro-fetch.sh. Projects have several
        properties, including commit hash and date
        """
        if not self.IsValid():
            return []
        
        # Cache projects
        try:
            return self._projects
        except:
            pass
        
        self._projects = []
        
        for dirname in os.listdir(LibretroSuper.GetRepoDir()):
            # Must be a directory
            if not os.path.isdir(os.path.join(LibretroSuper.GetRepoDir(), dirname)):
                continue
            
            # Must start with 'libretro-'
            if not dirname.startswith(LibretroProject.GetProjectNamePrefix()):
                continue
            
            project = LibretroProject(os.path.join(LibretroSuper.GetRepoDir(), dirname))
            
            if project.IsValid():
                self._projects.append(project)
                print('Found project %s at %s (%s)' % (project.GetName(), project.GetVersionHash()[ : 7], project.GetDate()))
        
        print('Found %d projects' % len(self._projects))
        
        return self._projects
    
    def GetProject(self, name):
        """
        Use fuzzy string matching to resolve the filename of a compiled libretro
        core to the project that generated it.
        """
        projects = self.GetProjects()
        
        # Find the closest match
        projectName = getClosestMatch(name, [project.GetName() for project in projects])
        
        # In case of an extra suffix (like bsnes_performance), split on '_' and remove last token
        if not projectName:
            name2 = name.rpartition('_')[0]
            if name2:
                projectName = getClosestMatch(name2, [project.GetName() for project in projects])
        
        if not projectName:
            return None
        
        # Recover the project whose name matched
        for project in projects:
            if project.GetName() == projectName:
                return project
        
        return None
    
    def GetDlls(self):
        """
        Get a list of all the binaries that successfully compiled.
        """
        dlls = []
        
        if not self.IsValid():
            return dlls
        
        for dllName in os.listdir(LibretroSuper.GetDllDir()):
            dllPath = os.path.join(LibretroSuper.GetDllDir(), dllName)
            dll = LibretroDll(dllPath, self)
            if dll.IsValid():
                dlls.append(dll)
                print('Loaded dll %s (%s) from project %s' % (dll.GetID(), dll.GetInfo().GetDisplayVersion(), dll.GetProject().GetName()))
            else:
                print('Failed to loaded dll %s (%s): can\'t find libretro-super project!' % (dll.GetID(), dll.GetInfo().GetDisplayVersion()))
        
        return dlls
    
    def Fetch(self):
        """
        Fetch all libretro cores using FETCH_CMD
        """
        if self.IsValid():
            LibretroSuper.RunScript(FETCH_CMD)
            return True
        return False
    
    def Build(self):
        """
        Build all libretro cores for the current platform
        """
        if not self.IsValid():
            return False
        
        if   LibretroSuper.GetPlatform() == 'win':  LibretroSuper.RunScript(BUILD_WIN_CMD)
        elif LibretroSuper.GetPlatform() == 'unix': LibretroSuper.RunScript(BUILD_UNIX_CMD)
        elif LibretroSuper.GetPlatform() == 'osx':  LibretroSuper.RunScript(BUILD_OSX_CMD)
        
        return True

class TestLibretroSuper(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_libretro_super(self):
        libretro = LibretroSuper()
        self.assertTrue(libretro.CloneIfNotValid())
        self.assertTrue(libretro.IsValid())
        self.assertEqual(libretro.GetBranch(), 'master')
        self.assertTrue(libretro.Fetch())
        self.assertTrue(libretro.Build())

if __name__ == '__main__':
    unittest.main()
