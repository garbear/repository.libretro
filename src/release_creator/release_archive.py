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
from md5_file import MD5File

import os
import shutil
import unittest
import zipfile

ARCHIVE_EXTENSION      = '.zip'
VERSIONED_ARCHIVE_NAME = '%s-%s' + ARCHIVE_EXTENSION # e.g. gameclient.bnes-1.0.0.zip

class ReleaseArchive:
    @staticmethod
    def GetExtension():
        """
        Release archives are .zip files.
        """
        return ARCHIVE_EXTENSION
    
    @staticmethod
    def GetArchivePath(id, addonVersion):
        """
        In the release dir archive is appended with version, e.g.
        gameclient.bnes-1.0.0.zip.
        """
        archiveName = VERSIONED_ARCHIVE_NAME % (id, addonVersion.ToString())
        return os.path.join(Environment.GetReleaseDir(id), archiveName)
    
    @staticmethod
    def GetIdAndVersion(path):
        """
        Given the path to the archive, return the ID and version.
        """
        filename = os.path.split(path)[1]
        id       = filename.split('-')[0]
        version  = filename.split('-')[1][ : -len(ARCHIVE_EXTENSION)]
        
        return id, AddonVersion(version)
    
    def __init__(self, id):
        self._id = id
    
    def _GetMaxVersion(self, fallback):
        """
        Get the highest version from the release archives in the release
        directory. Versions less than fallback are ignored. If the directory
        contains no release archives > fallback, fallback is returned.
        """
        maxVersion = fallback
        
        if os.path.exists(Environment.GetReleaseDir(self._id)):
            for filename in os.listdir(Environment.GetReleaseDir(self._id)):
                if not filename.endswith(ReleaseArchive.GetExtension()):
                    continue
                
                id, addonVersion = ReleaseArchive.GetIdAndVersion(filename)
                if maxVersion.Compare(addonVersion) < 0:
                    maxVersion = addonVersion
        
        return maxVersion
    
    def Update(self, addonXml, changeLog, dll):
        print('Creating release archive for %s' % self._id)
        
        # First check for existing archives
        maxAddonVersion = self._GetMaxVersion(addonXml.GetVersion())
        
        zipPath = ReleaseArchive.GetArchivePath(self._id, maxAddonVersion)
        if zipfile.is_zipfile(zipPath):
            addonXml.SetVersion(maxAddonVersion)
            
            addonXmlText  = addonXml.GetAddonXml()
            changeLogText = changeLog.GetText()
            
            # Release archive for this version already exists
            # Check if existing archive differs from updated archive
            different = False
            
            zipAddonXmlText, zipChangeLogText, zipHasIcon, zipHasFanart, zipHasLibrary = self._GetZipInfo(zipPath)
            
            if addonXmlText != zipAddonXmlText:
                different = True
            
            if changeLogText != zipChangeLogText:
                different = True
            
            if (addonXml.GetIconPath() != None) != zipHasIcon:
                different = True
            
            if (addonXml.GetFanartPath() != None) != zipHasFanart:
                different = True
            
            if not different:
                print('Archive %s is up to date' % os.path.split(zipPath)[1])
                return True # All done here
            
            # Archive differs, so bump the version and call Update() again
            addonXml.SetVersion(maxAddonVersion.Bump())
            if not self.Update(addonXml, changeLog, dll):
                return False
            
            # Archive has been updated to new version. Remove the old archive.
            os.remove(zipPath)
            os.remove(zipPath + MD5File.GetExtension())
        else:
            # Archive doesn't already exist. Create now
            assert(addonXml.GetVersion().ToString() == maxAddonVersion.ToString())
            
            addonXmlText  = addonXml.GetAddonXml()
            changeLogText = changeLog.GetText()
            
            if self._WriteZipFile(zipPath, addonXmlText, changeLogText, addonXml.GetIconPath(), addonXml.GetFanartPath(), dll.GetPath()):
                md5File = MD5File(zipPath)
                if not md5File.Save():
                    # MD5 file failed, remove archive
                    try:
                        os.remove(self._path)
                        os.remove(self._path + MD5File.GetExtension())
                    except:
                        pass
                    return False
                
                # Create changelog-version.txt
                #if changeLog.CreateRelease():
        
        # Copy icon.png and fanart.jpg if they exist
        if addonXml.GetIconPath() and os.path.exists(addonXml.GetIconPath()):
            shutil.copy2(addonXml.GetIconPath(), os.path.join(Environment.GetReleaseDir(self._id), AddonXml.GetIconFileName()))
        if addonXml.GetFanartPath() and os.path.exists(addonXml.GetFanartPath()):
            shutil.copy2(addonXml.GetFanartPath(), os.path.join(Environment.GetReleaseDir(self._id), AddonXml.GetFanartFileName()))
        
        return True
    
    def _GetZipInfo(self, path):
        addonXmlText  = ''
        changeLogText = ''
        hasIcon       = False
        hasFanart     = False
        hasLibrary    = False
        
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path, 'r') as myzip:
                for filepath in myzip.namelist():
                    # Strip leading folder (assuming it is named addonId)
                    filename = filepath[len(self._id) + 1 : ]
                    
                    if filename == AddonXml.GetFileName():
                        addonXmlText  = myzip.read(filepath).strip()
                    elif filename == ChangeLog.GetFileName():
                        changeLogText = myzip.read(filepath).strip()
                    elif filename == AddonXml.GetIconFileName():
                        hasIcon = True
                    elif filename == AddonXml.GetFanartFileName():
                        hasFanart = True
                    elif filename.endswith(Environment.GetDllExtension()):
                        hasLibrary = True
        
        return addonXmlText, changeLogText, hasIcon, hasFanart, hasLibrary
    
    def _WriteZipFile(self, zipPath, addonXmlText, changeLogText, iconPath, fanartPath, dllPath):
        # Shove everything into the zip file
        with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as myzip:
            myzip.writestr(os.path.join(self._id, AddonXml.GetFileName()), addonXmlText)
            #myzip.writestr(os.path.join(self._id, ChangeLog.GetFileName()), changeLogText) # TODO: Uncomment once changelogs are implemented
            myzip.write(dllPath, os.path.join(self._id, os.path.split(dllPath)[1]))
            if iconPath:
                myzip.write(iconPath, os.path.join(self._id, AddonXml.GetIconFileName()))
            if fanartPath:
                myzip.write(iconPath, os.path.join(self._id, AddonXml.GetFanartFileName()))
            return True
        
        return False

class TestReleaseArchive(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_addon(self):
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
            self.assertTrue(addon.CreateRelease())

if __name__ == '__main__':
    unittest.main()