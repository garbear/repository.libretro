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

#include "LibretroSettings.h"
#include "libretro.h"

#include <dirent.h>
#include <fstream>
#include <string>
#include <sys/stat.h>

using namespace LIBRETRO;
using namespace std;

#define CATEGORY_TITLE  "Settings"

#define RESOURCES_DIR  "resources"
#define SETTINGS_FILE  "settings.xml"

CLibretroSettings::CLibretroSettings(const string& strAddonDir, const vector<retro_variable>& variables)
 : m_strAddonDir(strAddonDir),
   m_strCategoryTitle(CATEGORY_TITLE)
{
  for (vector<retro_variable>::const_iterator it = variables.begin(); it != variables.end(); ++it)
  {
    string strId(it->key);
    string strName;
    vector<string> vecValues;

    LibretroSetting setting;
    setting.strId = it->key;

    const string strNameAndValues = it->value;

    size_t pos = strNameAndValues.find(';');
    if (pos != string::npos)
    {
      setting.strName = Trim(strNameAndValues.substr(0, pos));
      string values = strNameAndValues.substr(pos + 1);

      while (!values.empty())
      {
        size_t pos2 = values.find('|');
        if (pos2 == string::npos)
        {
          setting.vecValues.push_back(Trim(values));
          values.clear();
        }
        else
        {
          setting.vecValues.push_back(Trim(values.substr(0, pos2)));
          values.erase(values.begin(), values.begin() + pos2 + 1);
        }
      }

      if (!setting.vecValues.empty())
        m_settings.push_back(setting);
    }
  }
}

CLibretroSettings::~CLibretroSettings()
{
  CLibretroString::Reset();
}

void CLibretroSettings::PrintSettings()
{
  const mode_t mode = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH;
  mkdir(m_strAddonDir.c_str(), mode);
  mkdir((m_strAddonDir + "/" RESOURCES_DIR).c_str(), mode);
  string strFilePath = m_strAddonDir + "/" RESOURCES_DIR "/" SETTINGS_FILE;

  fstream file;
  file.open(strFilePath.c_str(), ios::out);

  if (!file.is_open())
    return;

  file << "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>" << endl;
  file << "<settings>" << endl;
  file << "\t<category label=\"" << CLibretroString(m_strCategoryTitle).GetID() << "\">" << endl;

  for (vector<LibretroSetting>::iterator it = m_settings.begin(); it != m_settings.end(); ++it)
  {
    file << "\t\t<setting label=\"" << CLibretroString(it->strName).GetID() << "\" type=\"labelenum\" id=\"" << it->strId << "\" values=\"";
    for (vector<string>::const_iterator it2 = it->vecValues.begin(); it2 != it->vecValues.end(); ++it2)
    {
      if (it2 != it->vecValues.begin())
        file << "|";
      file << *it2;
    }
    file << "\"/>" << endl;
  }

  file << "\t</category>" << endl;
  file << "</settings>" << endl;
  file << endl;
}

void CLibretroSettings::PrintLanguage()
{
  CLibretroString::PrintLanguage(m_strAddonDir);
}

string CLibretroSettings::Trim(const string& str)
{
  string strCopy(str);
  while (!strCopy.empty() && strCopy[0] == ' ')
    strCopy.erase(strCopy.begin());
  while (!strCopy.empty() && strCopy[strCopy.length() - 1] == ' ')
    strCopy.erase(strCopy.end() - 1);
  return strCopy;
}
