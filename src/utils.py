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

import difflib
import unittest

def getClosestMatch(needle, haystack):
    matches = difflib.get_close_matches(needle, haystack)
    if not matches:
        return None
    
    # Find match with highest ratio
    bestMatch = None
    maximum = -1
    for match in matches:
        ratio = difflib.SequenceMatcher(None, needle, match).ratio()
        if ratio > maximum:
            bestMatch = match
            maximum = ratio
    return bestMatch

class TestLibretroUtils(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_closest_match(self):
        needle = 'snes9x'
        haystack = ['bsnes', 'snes9x', 'snes9x-next']
        self.assertEqual(getClosestMatch(needle, haystack), haystack[1])
        needle = 'snes9x_next'
        haystack = ['bsnes', 'snes9x', 'snes9x-next']
        self.assertEqual(getClosestMatch(needle, haystack), haystack[2])

if __name__ == '__main__':
    unittest.main()
