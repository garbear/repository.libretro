/*
 *      Copyright (C) 2014 Team XBMC
 *      http://xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

#include "LibretroString.h"

#include <algorithm>
#include <assert.h>
#include <iostream>

using namespace LIBRETRO;
using namespace std;

#define XBMC_STRING_START  30000

vector<string> CLibretroString::m_strings;

CLibretroString::CLibretroString(const string &text)
 : m_string(text)
{
  m_id = XBMC_STRING_START + m_strings.size();
  m_strings.push_back(m_string);
}

CLibretroString::~CLibretroString()
{
  //vector<CLibretroString*>::iterator it = std::find(m_strings.begin(), m_strings.end(), this);
  //assert(it != m_strings.end());
  //m_strings.erase(it);
}

void CLibretroString::Reset()
{
  m_strings.clear();
}

void CLibretroString::PrintLanguage()
{
  cout << "# XBMC Media Center language file" << endl;
  cout << "# Addon Name: @name@" << endl;
  cout << "# Addon id: @id@" << endl;
  cout << "# Addon Provider: @authors@" << endl;
  cout << "msgid \"\"" << endl;
  cout << "msgstr \"\"" << endl;
  cout << "\"Project-Id-Version: Libretro Clients\\n\"" << endl;
  cout << "\"Report-Msgid-Bugs-To: alanwww1@xbmc.org\\n\"" << endl;
  cout << "\"POT-Creation-Date: 2014-05-30 17:00+8\\n\"" << endl;
  cout << "\"PO-Revision-Date: 2014-05-30 17:00+8\\n\"" << endl;
  cout << "\"Last-Translator: XBMC Translation Team\\n\"" << endl;
  cout << "\"Language-Team: English (http://www.transifex.com/projects/p/xbmc-addons/language/en/)\\n\"" << endl;
  cout << "\"MIME-Version: 1.0\\n\"" << endl;
  cout << "\"Content-Type: text/plain; charset=UTF-8\\n\"" << endl;
  cout << "\"Content-Transfer-Encoding: 8bit\\n\"" << endl;
  cout << "\"Language: en\\n\"" << endl;
  cout << "\"Plural-Forms: nplurals=2; plural=(n != 1);\\n\"" << endl;
  cout << endl;

  for (vector<string>::const_iterator it = m_strings.begin(); it != m_strings.end(); ++it)
  {
    const unsigned int id = XBMC_STRING_START + (it - m_strings.begin());
    cout << "msgctxt \"#" << id << "\"" << endl;
    cout << "msgid \"" << *it << "\"" << endl;
    cout << "msgstr \"\"" << endl;
    cout << endl;
  }
}
