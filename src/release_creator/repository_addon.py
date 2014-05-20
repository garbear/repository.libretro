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
from environment import Environment
from md5_file import MD5File
from release_archive import ReleaseArchive

import os
import shutil
import unittest
import zipfile

REPO_ADDON_ID               = 'repository.libretro-%s'

class RepositoryAddon:
    def __init__(self):
        self._id = REPO_ADDON_ID % Environment.GetPlatform()
    
    def GetID(self):
        return self._id
    
    def GetAddonXmlText(self):
        addonXmlText = ''
        
        addonXmlPath = os.path.join(Environment.GetAddonDir(self._id), AddonXml.GetFileName())
        with open(addonXmlPath, 'r') as f:
            addonXmlText = f.read().strip()
        
        return addonXmlText
    
    def CreateRelease(self):
        """
        Create a release archive (and associated files like md5 and changelog)
        in the /release folder.
        """
        print('Creating release archive for %s' % self._id)
        
        version = AddonVersion('1.0.0') # TODO: Read from addon.xml
        
        addonXmlPath = os.path.join(Environment.GetAddonDir(self._id), AddonXml.GetFileName())
        iconPngPath  = os.path.join(Environment.GetAddonDir(self._id), AddonXml.GetIconFileName())
        
        if not os.path.exists(Environment.GetReleaseDir(self._id)):
            os.makedirs(Environment.GetReleaseDir(self._id))
        
        # Shove everything into the zip file
        zipPath = ReleaseArchive.GetArchivePath(self._id, version)
        if not os.path.exists(zipPath):
            myzip = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
            myzip.write(addonXmlPath, os.path.join(self._id, AddonXml.GetFileName()))
            myzip.write(iconPngPath, os.path.join(self._id, AddonXml.GetIconFileName()))
            
            md5File = MD5File(zipPath)
            if not md5File.Save():
                print('Failed to create release archive for %s' % self._id)
                try:
                    os.remove(zipPath)
                except:
                    pass
                return False
        else:
            print('Archive %s is up to date' % os.path.split(zipPath)[1])
        
        if os.path.exists(iconPngPath):
            shutil.copy2(iconPngPath, os.path.join(Environment.GetReleaseDir(self._id), AddonXml.GetIconFileName()))
        
        return True

class TestRepositoryAddon(unittest.TestCase):
    def setUp(self):
        repositoryAddon = RepositoryAddon()
        archiveDir = Environment.GetReleaseDir(repositoryAddon.GetID())
        if os.path.exists(archiveDir):
            shutil.rmtree(archiveDir)
        
        self.assertTrue(not os.path.exists(archiveDir))
    
    def test_repository_addon(self):
        repositoryAddon = RepositoryAddon()
        self.assertNotEqual(repositoryAddon.GetAddonXmlText(), '')
        self.assertTrue(repositoryAddon.CreateRelease())
        self.assertTrue(repositoryAddon.CreateRelease())

if __name__ == '__main__':
    unittest.main()
