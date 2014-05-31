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
#pragma once

#include "LibretroString.h"

#include <vector>

struct retro_variable;

namespace LIBRETRO
{
  class CLibretroSettings
  {
  public:
    CLibretroSettings(const std::vector<retro_variable>& variables);
    ~CLibretroSettings();
    
    void PrintSettings();
    void PrintLanguage();
    
  private:
    static std::string Trim(const std::string& str);

    struct LibretroSetting
    {
      std::string              strId;
      std::string              strName;
      std::vector<std::string> vecValues;
    };

    std::string                  m_strCategoryTitle;
    std::vector<LibretroSetting> m_settings;
  };
} // namespace LIBRETRO
