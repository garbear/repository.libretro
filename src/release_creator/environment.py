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

import os
import platform
import subprocess
import unittest

ADDONS_DIR          = 'addons'
SRC_DIR             = 'src'
RELEASE_CREATOR_DIR = 'release_creator'
RELEASE_DIR         = 'release'

class Environment:
    WIN     = 'win32'
    LINUX32 = 'linux32'
    LINUX64 = 'linux64'
    OSX32   = 'osx32'
    OSX64   = 'osx64'
    ANDROID = 'android'
    
    @staticmethod
    def GetPlatform():
        if platform.system() == 'Windows':
            return Environment.WIN
        elif platform.system() == 'Darwin':
            return Environment.OSX64 # TODO: 32-bit vs 64-bit
        elif platform.system() == 'Linux':
            if platform.architecture()[0] == '64bit':
                return Environment.LINUX64
            else:
                return Environment.LINUX32
        raise Exception('System not supported: %s' % platform.system())
    
    @staticmethod
    def GetRootDir():
        myDir = os.path.abspath(os.path.dirname(__file__))
        
        # Verify that we're running from the /src directory
        myDirName = os.path.split(myDir)[1]
        if myDirName !=  RELEASE_CREATOR_DIR:
            raise Exception('File is not in /' + SRC_DIR + '/' + RELEASE_CREATOR_DIR)
        
        return os.path.abspath(os.path.join(myDir, '..', '..'))
    
    @staticmethod
    def GetAddonsDir():
        """
        Auxiliary data for add-ons is stored in /addons.
        """
        return os.path.join(Environment.GetRootDir(), ADDONS_DIR)
    
    @staticmethod
    def GetAddonDir(addonId):
        """
        Add-on dir is its ID in /addons.
        """
        return os.path.join(Environment.GetAddonsDir(), addonId)
    
    @staticmethod
    def GetSrcDir():
        """
        Python scripts are stored in /src.
        """
        return os.path.join(Environment.GetRootDir(), SRC_DIR)
    
    @staticmethod
    def GetReleaseDir(addonId=None):
        """
        Release archives are stored in /release/platform. If addonId is
        specified, the addon's individual release folder is returned.
        """
        if addonId:
            return os.path.join(Environment.GetRootDir(), RELEASE_DIR, Environment.GetPlatform(), addonId)
        else:
            return os.path.join(Environment.GetRootDir(), RELEASE_DIR, Environment.GetPlatform())
    
    @staticmethod
    def GetDllExtension():
        if Environment.GetPlatform() == Environment.WIN:
            return '.dll'
        if Environment.GetPlatform() == Environment.OSX32 or\
           Environment.GetPlatform() == Environment.OSX64:
            return '.dylib'
        if Environment.GetPlatform() == Environment.LINUX32 or \
           Environment.GetPlatform() == Environment.LINUX64:
            return '.so'
        raise Exception('Platform not supported: %s' % Environment.GetPlatform())
    
    @staticmethod
    def GetFilesBySuffix(directory, fileSuffix):
        """
        Return a list of files in directory having the specified suffix. Suffix
        is stripped from files before returning list.
        """
        files = [f for f in os.listdir(directory) if f.endswith(fileSuffix)]
        # Strip suffix from filenames
        names = [f[ : -len(fileSuffix)] for f in files]
        return names
    
    @staticmethod
    def CheckOutput(path, args):
        """
        Call an external process and return the output. path is the directory
        the process should be run from, and args are the command-line args
        appropriate for subprocess.Popen().
        """
        if not os.path.exists(path):
            return ''
        
        os.chdir(path)
        
        if Environment.GetPlatform() == Environment.WIN:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        output, err = proc.communicate()
        return output.strip()
    
    @staticmethod
    def RunScript(script):
        dir = os.path.dirname(script)
        if os.path.exists(dir):
            os.chdir(dir)
            
            if Environment.GetPlatform() == Environment.WIN:
                scriptName = os.path.split(script)[1]
                subprocess.call(['C:\\Program Files (x86)\\Git\\bin\\sh.exe', '--login', scriptName]) # TODO
            else:
                subprocess.call(os.path.abspath(script))

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_platform(self):
        self.assertTrue(Environment.GetPlatform() in [Environment.WIN,
                                                      Environment.LINUX32,
                                                      Environment.LINUX64,
                                                      Environment.OSX32,
                                                      Environment.OSX64,
                                                      Environment.ANDROID])
    
    def test_get_root_dir(self):
        self.assertNotEqual(Environment.GetRootDir(), '')
        self.assertTrue(os.path.exists(Environment.GetRootDir()))
    
    def test_addons_dir(self):
        self.assertNotEqual(Environment.GetAddonsDir(), '')
        self.assertTrue(os.path.exists(Environment.GetAddonsDir()))
    
    def test_addon_dir(self):
        ADDON_ID = 'repository.libretro-linux64'
        self.assertNotEqual(Environment.GetAddonDir(ADDON_ID), '')
        self.assertTrue(os.path.exists(Environment.GetAddonDir(ADDON_ID)))
    
    def test_src_dir(self):
        self.assertNotEqual(Environment.GetSrcDir(), '')
        self.assertTrue(os.path.exists(Environment.GetSrcDir()))
    
    def test_release_dir(self):
        self.assertNotEqual(Environment.GetReleaseDir(), '')
        self.assertTrue(os.path.exists(Environment.GetReleaseDir()))
    
    def test_get_dll_extension(self):
        self.assertTrue(Environment.GetDllExtension() in ['.dll', '.dylib', '.so'])
    
    def test_get_files_by_suffix(self):
        from libretro_super import LibretroSuper
        prefixes = Environment.GetFilesBySuffix(LibretroSuper.GetRepoDir(), '-build.sh')
        self.assertEqual(len(prefixes), 2)
        self.assertTrue('retroarch' in prefixes)
        self.assertTrue('libretro' in prefixes)
    
    def test_check_output(self):
        REF = 'Hello_world'
        args = ['echo', REF]
        output = Environment.CheckOutput(os.path.abspath('.'), args)
        self.assertEqual(output, REF)
    
    def test_run_script(self):
        from libretro_super import LibretroSuper
        Environment.RunScript(os.path.join(LibretroSuper.GetRepoDir(), 'libretro-config.sh'))

if __name__ == '__main__':
    unittest.main()
