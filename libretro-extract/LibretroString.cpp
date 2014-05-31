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
#include <dirent.h>
#include <fstream>
#include <sys/stat.h>

using namespace LIBRETRO;
using namespace std;

#define XBMC_STRING_START  30000

#define RESOURCES_DIR  "resources"
#define LANGUAGES_DIR  "languages"
#define ENGLISH_DIR    "english"
#define STRINGS_FILE   "strings.po"

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

void CLibretroString::PrintLanguage(const string& strAddonDir)
{
  const mode_t mode = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH;
  mkdir(strAddonDir.c_str(), mode);
  mkdir((strAddonDir + "/" RESOURCES_DIR).c_str(), mode);
  mkdir((strAddonDir + "/" RESOURCES_DIR "/" LANGUAGES_DIR).c_str(), mode);
  mkdir((strAddonDir + "/" RESOURCES_DIR "/" LANGUAGES_DIR "/" ENGLISH_DIR).c_str(), mode);
  string strFilePath = strAddonDir + "/" RESOURCES_DIR "/" LANGUAGES_DIR "/" ENGLISH_DIR "/" STRINGS_FILE;

  fstream file;
  file.open(strFilePath.c_str(), ios::out);

  if (!file.is_open())
    return;

  file << "# XBMC Media Center language file" << endl;
  file << "# Addon Name: @name@" << endl;
  file << "# Addon id: @id@" << endl;
  file << "# Addon Provider: @authors@" << endl;
  file << "msgid \"\"" << endl;
  file << "msgstr \"\"" << endl;
  file << "\"Project-Id-Version: Libretro Clients\\n\"" << endl;
  file << "\"Report-Msgid-Bugs-To: alanwww1@xbmc.org\\n\"" << endl;
  file << "\"POT-Creation-Date: 2014-05-30 17:00+8\\n\"" << endl;
  file << "\"PO-Revision-Date: 2014-05-30 17:00+8\\n\"" << endl;
  file << "\"Last-Translator: XBMC Translation Team\\n\"" << endl;
  file << "\"Language-Team: English (http://www.transifex.com/projects/p/xbmc-addons/language/en/)\\n\"" << endl;
  file << "\"MIME-Version: 1.0\\n\"" << endl;
  file << "\"Content-Type: text/plain; charset=UTF-8\\n\"" << endl;
  file << "\"Content-Transfer-Encoding: 8bit\\n\"" << endl;
  file << "\"Language: en\\n\"" << endl;
  file << "\"Plural-Forms: nplurals=2; plural=(n != 1);\\n\"" << endl;

  for (vector<string>::const_iterator it = m_strings.begin(); it != m_strings.end(); ++it)
  {
    const unsigned int id = XBMC_STRING_START + (it - m_strings.begin());
    file << endl;
    file << "msgctxt \"#" << id << "\"" << endl;
    file << "msgid \"" << *it << "\"" << endl;
    file << "msgstr \"\"" << endl;
  }
}
