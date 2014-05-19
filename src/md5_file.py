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
import unittest

try:
    import md5
except ImportError:
    import hashlib

MD5_EXTENSION = '.md5'

class MD5File:
    @staticmethod
    def GetExtension():
        return MD5_EXTENSION
    
    def __init__(self, path):
        """
        Creates an MD5 object for the specified path of a file. The filename
        for the generated MD5 stamp is the filename + '.md5'
        """
        self._filename = path + MD5_EXTENSION
        self._LoadMD5(path)
    
    def _LoadMD5(self, path):
        self._md5 = None
        
        data = None
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = f.read()
        
        if data is not None:
            try:
                self._md5 = hashlib.md5(data).hexdigest()
            except NameError:
                self._md5 = md5.new(data).hexdigest()
    
    def IsValid(self):
        return self._md5 is not None
    
    def GetPath(self):
        """
        Get the path of the .md5 file, including the .md5 extension.
        """
        return self._filename
    
    def Save(self):
        if not self.IsValid():
            return False
        
        with open(self._filename, 'w') as f:
            f.write(self._md5)
        
        return True

class TestMD5File(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        try:
            os.remove(self._md5Path)
        except:
            pass
    
    def test_md5_file(self):
        from addon_xml import AddonXml
        testfile = os.path.join(Environment.GetSrcDir(), AddonXml.GetTemplateFileName())
        self.assertTrue(os.path.exists(testfile))
        
        md5File = MD5File(testfile)
        self.assertTrue(md5File.IsValid())
        self.assertTrue(md5File.Save())
        
        # Save md5 path so we can remove it in tearDown()
        self._md5Path = md5File.GetPath()
        
        md5_1 = None
        with open(testfile + MD5_EXTENSION, 'r') as f:
            md5_1 = f.read()
        self.assertNotEqual(md5_1, None)
        
        # Compare against output of md5sum
        md5_2 = Environment.CheckOutput('.', ['md5sum', testfile])
        self.assertTrue(' ' in md5_2) # md5sum output includes filename
        md5_2 = md5_2.split(' ')[0] # Extract first word
        self.assertEqual(md5_1, md5_2)

if __name__ == '__main__':
    unittest.main()
