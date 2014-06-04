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
from environment import Environment

import os
import re
import unittest

ADDON_XML          = 'addon.xml'
ADDON_TEMPLATE_XML = 'addon.template.xml'
ICON_PNG           = 'icon.png'
FANART_JPG         = 'fanart.jpg'
LIBRETRO_PROVIDER  = 'Libretro Team'

class AddonXml:
    @staticmethod
    def GetFileName():
        return ADDON_XML
    
    @staticmethod
    def GetTemplateFileName():
        return ADDON_TEMPLATE_XML
    
    @staticmethod
    def GetIconFileName():
        return ICON_PNG
    
    @staticmethod
    def GetFanartFileName():
        return FANART_JPG
    
    @staticmethod
    def _LoadTemplate(path):
        with open(path) as f:
            return f.read().splitlines(False) # Don't keep line endings
        return None
    
    def __init__(self, dll):
        self._id           = dll.GetID()
        self._info         = dll.GetInfo()
        self._libraryPath  = dll.GetPath()
        self._project      = dll.GetProject()
        
        addonDir = Environment.GetAddonDir(self._id)
        
        self._addonVersion = None
        self._path         = os.path.join(addonDir, ADDON_XML)
        self._template     = AddonXml._LoadTemplate(os.path.join(Environment.GetSrcDir(), ADDON_TEMPLATE_XML))
        self._iconPath     = None
        self._fanartPath   = None
        self._properties   = { } # Cache for resolved properties
        
        if self.IsValid() and os.path.exists(addonDir):
            files = os.listdir(addonDir)
            if ICON_PNG in files:
                self._iconPath = os.path.join(addonDir, ICON_PNG)
            if FANART_JPG in files:
                self._fanartPath = os.path.join(addonDir, FANART_JPG)
    
    def IsValid(self):
        if not self._template:
            return False
        if not self._info.IsValid():
            return False
        return True
    
    def GetIconPath(self):
        return self._iconPath
    
    def GetFanartPath(self):
        return self._fanartPath
    
    def GetAddonXml(self):
        if self.IsValid():
            return '\n'.join([self.ReplaceTokens(line) for line in self._template])
        return ''
    
    def GetVersion(self):
        """
        Get the version set by SetVersion(). Falls back to parsing the display
        version if SetVersion() hasn't been called.
        """
        if self._addonVersion:
            return self._addonVersion
        elif self.IsValid():
            return AddonVersion(self._info.GetDisplayVersion())
        else:
            return AddonVersion()
    
    def SetVersion(self, addonVersion):
        """
        Set the version of the add-on as seen by XBMC (may be different than
        display version). addonVersion is an object of type AddonVersion.
        """
        self._addonVersion = addonVersion
    
    def Save(self):
        if not os.path.exists(Environment.GetAddonDir(self._id)):
            os.makedirs(Environment.GetAddonDir(self._id))
        
        if self.IsValid():
            with open(self._path, 'w') as f:
                f.write(self.GetAddonXml())
            return True
        
        return False
    
    def ReplaceTokens(self, line):
        """
        Replace tokens (like @tokenname@) with the corresponding property.
        """
        # Skip characters at the beginning of line (increases for every processed token)
        skip = 0
        
        # Validate on XML identifiers (assuming ASCII characters)
        validToken = re.compile('^[A-Za-z:_][A-Za-z0-9:_.-]*$')
        
        while line.count('@', skip) >= 2:
            index1 = line.find('@') + 1
            index2 = line.find('@', index1)
            token = line[index1 : index2]
            
            # Make sure that discovered token is a valid XML identifier (no spaces, etc)
            if validToken.match(token):
                line = line[ : index1 - 1] + self.GetProperty(token) + line[index2 + 1 : ]
                skip = index1 - 1 # Rewind 1 character so that tokens can be recursive
            else:
                skip = index1
        
        return line
    
    def GetProperty(self, prop):
        if   prop == 'id':               value = self._id
        elif prop == 'name':             value = self._info.GetDisplayName()
        elif prop == 'version':          value = self.GetVersion().ToString()
        elif prop == 'display_version':  value = self._info.GetDisplayVersion()
        elif prop == 'core_name':        value = self._info.GetCoreName()
        elif prop == 'authors':          value = self._info.GetAuthors() if self._info.GetAuthors() else LIBRETRO_PROVIDER
        elif prop == 'description':      value = self._GetDescription()
        elif prop == 'library_android':  value = self._GetLibraryPath(Environment.ANDROID)
        elif prop == 'library_linux':    value = self._GetLibraryPath(Environment.LINUX64, Environment.LINUX32)
        elif prop == 'library_osx':      value = self._GetLibraryPath(Environment.OSX64)
        elif prop == 'library_win':      value = self._GetLibraryPath(Environment.WIN)
        elif prop == 'platforms':        value = self._info.GetSystemName()
        elif prop == 'extensions':       value = self._info.GetExtensions()
        elif prop == 'supports_vfs':     value = self._info.SupportsVfs()
        elif prop == 'supports_no_game': value = self._info.SupportsNoGame()
        elif prop == 'platform':         value = '' # TODO
        elif prop == 'nofanart':         value = 'true' if not self._fanartPath else 'false'
        elif prop == 'noicon':           value = 'true' if not self._iconPath else 'false'
        elif prop == 'broken':           value = '' # TODO
        else:                            value = ''
        return value
    
    def _GetDescription(self):
        description = self._info.GetDescription()
        
        # If the core specified extensions, include these in the description
        if self._info.GetExtensions():
            if description:
                description += '\n\n'
            
            description += 'Supported files: @extensions@'
        
        if description:
            description += '\n\n'
        
        # Including the git hash will cause the release archive to be updated if a new version is compiled
        description += 'Last updated %s (%s)' % (self._project.GetDate(), self._project.GetVersionHash())
        
        return description
    
    def _GetLibraryPath(self, platform, backupPlatform=''):
        """
        Returns the library path if platform or backupPlatform matches the
        current library, or an empty string otherwise.
        """
        if platform == Environment.GetPlatform() or \
          (backupPlatform and backupPlatform == Environment.GetPlatform()):
            return os.path.split(self._libraryPath)[1]
        return ''

class TestAddonXml(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_addon_xml(self):
        from libretro_super import LibretroSuper
        libretroSuper = LibretroSuper()
        
        dlls = libretroSuper.GetDlls()
        self.assertNotEqual(len(dlls), 0)
        
        for dll in dlls:
            # GetDlls() only returns valid DLLs, but we can check anyway
            self.assertTrue(dll.IsValid())
            
            addonXml = AddonXml(dll)
            self.assertTrue(addonXml.Save())

if __name__ == '__main__':
    unittest.main()
