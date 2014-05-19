#/usr/bin/env python
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

from release_creator.addon import Addon
from release_creator.addons_xml import AddonsXml
from release_creator.libretro_super import LibretroSuper
from release_creator.repository_addon import RepositoryAddon

import unittest

def CreateRelease():
    print('This can take a while. Grab a drink!')
    
    libretroSuper = LibretroSuper()
    
    print('Creating repository libretro-super')
    libretroSuper.CloneIfNotValid()
    if not libretroSuper.IsValid():
        print('Repository libretro-super is not in a usable state')
        return
    
    print('Using branch %s of libretro-super' % libretroSuper.GetBranch())
    
    print('Updating libretro-super projects')
    libretroSuper.Fetch()
    
    print('Building libretro-super projects')
    libretroSuper.Build()
    
    print('Analyzing build results for generated binaries')
    dlls = libretroSuper.GetDlls()
    
    print('Found %d libretro binaries' % len(dlls))
    
    addons = []
    for dll in dlls:
        addon = Addon(dll)
        if not addon.CreateRelease():
            print('Failed to create release archive for %s', addon.GetID())
            continue
        addons.append(addon)
    
    # Don't forget about the repository add-on!
    repositoryAddon = RepositoryAddon()
    repositoryAddon.CreateRelease()
    addons.append(repositoryAddon)
    
    print('Creating add-on index addons.xml')
    addonsXml = AddonsXml(addons)
    addonsXml.Save()
    
    print('Finished!')

class TestCreateRelease(unittest.TestCase):
    def test_create_release(self):
        CreateRelease()

if __name__ == '__main__':
    unittest.main()
