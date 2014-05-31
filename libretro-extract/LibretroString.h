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

#include <string>
#include <vector>

namespace LIBRETRO
{
  class CLibretroString
  {
  public:
    CLibretroString(const std::string& text);
    ~CLibretroString();

    unsigned int GetID() const { return m_id; }
    const std::string& GetString() const { return m_string; }

    static void Reset();

    static void PrintLanguage(const std::string& strAddonDir);

  private:
    unsigned int m_id;
    std::string  m_string;

    static std::vector<std::string> m_strings;
  };
} // namespace LIBRETRO
