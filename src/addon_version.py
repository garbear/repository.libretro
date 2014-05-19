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

import unittest

class AddonVersion:
    @staticmethod
    def GetNumber(s, default=0):
        """
        Convert the string s to an int, stripping non-numeric characters from
        the biginning and ignoring any after the number. Assumes s is unsigned
        ("-" is ignored). If s doesn't contain a number, then default is
        returned.
        """
        if not s:
            return default
        
        # Strip leading non-numerics
        while len(s) > 0 and (s[0] < '0' or s[0] > '9'):
            s = s[1 : ]
        
        #Strip traling non-numerics
        i = 0
        while i < len(s) and ('0' <= s[i] and s[i] <= '9'):
            i += 1
        s = s[ : i]
        
        try:
            return int(s)
        except:
            pass
        
        return default
    
    def __init__(self, versionString=''):
        # Default to 1.0.0
        self._major = 1
        self._minor = 0
        self._build = 0
        
        parts = versionString.split('.')
        
        # Look through each part for a valid number
        if len(parts) >= 1:
            self._major = AddonVersion.GetNumber(parts[0], 1)
        if len(parts) >= 2:
            self._minor = AddonVersion.GetNumber(parts[1], 0)
        if len(parts) >= 3:
            self._build = AddonVersion.GetNumber(parts[2], 0)
    
    def Compare(self, addonVersion):
        """
        Similar to strcmp(), a 1 means this > addonVersion, -1 means
        this < addonVersion, and 0 means this == addonVersion.
        """
        if self._major > addonVersion._major:
            return 1
        if self._major < addonVersion._major:
            return -1
        
        if self._minor > addonVersion._minor:
            return 1
        if self._minor < addonVersion._minor:
            return -1
        
        if self._build > addonVersion._build:
            return 1
        if self._build < addonVersion._build:
            return -1
        
        return 0
    
    def ToString(self):
        return '%d.%d.%d' % (self._major, self._minor, self._build)
    
    def Bump(self):
        return AddonVersion('%d.%d.%d' % (self._major, self._minor, self._build + 1))
    
    def ToParts(self):
        return self._major, self._minor, self._build

class TestAddonVersion(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_addon_version(self):
        v1 = AddonVersion('1.0.0')
        v2 = AddonVersion('v1.0.0')
        self.assertEqual(v1.Compare(v2), 0)
        
        v1 = AddonVersion('')
        v2 = AddonVersion('1.0.0')
        self.assertEqual(v1.Compare(v2), 0)
        
        v1 = AddonVersion('1.0.0')
        v2 = AddonVersion('1.0.1')
        self.assertEqual(v1.Compare(v2), -1)
        
        v1 = AddonVersion('1.0.1')
        v2 = AddonVersion('1.0.0')
        self.assertEqual(v1.Compare(v2), 1)
        
        self.assertEqual(AddonVersion('git').ToString(),                '1.0.0')
        self.assertEqual(AddonVersion('0.78').ToString(),               '0.78.0')
        self.assertEqual(AddonVersion('v0.9.33.3').ToString(),          '0.9.33')
        self.assertEqual(AddonVersion('v1.0.2').ToString(),             '1.0.2')
        self.assertEqual(AddonVersion('v1').ToString(),                 '1.0.0')
        self.assertEqual(AddonVersion('r19').ToString(),                '19.0.0')
        self.assertEqual(AddonVersion('v0.2.97.30').ToString(),         '0.2.97')
        self.assertEqual(AddonVersion('v085 (Performance)').ToString(), '85.0.0')
        self.assertEqual(AddonVersion('(SVN)').ToString(),              '1.0.0')
        self.assertEqual(AddonVersion('2.0-rc2').ToString(),            '2.0.0')
        self.assertEqual(AddonVersion('v1.46-WIP').ToString(),          '1.46.0')
        self.assertEqual(AddonVersion('v1.46-WIP').Bump().ToString(),   '1.46.1')

if __name__ == '__main__':
    unittest.main()
