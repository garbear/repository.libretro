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

#include "LibretroDLL.h"
#include "xbmc_game_types.h"

#ifdef _WIN32
  #include "dlfcn-win32.h"
#else
  #include <dlfcn.h>
#endif

#include <assert.h>
#include <stdio.h>

using namespace LIBRETRO;
using namespace std;

#define ADDON_ID_TYPE    "gameclient."
#define LIBRETRO_SUFFIX  "_libretro"

CLibretroDLL::CLibretroDLL()
 : m_libretroClient(NULL)
{
}

void CLibretroDLL::Unload(void)
{
  if (m_libretroClient)
  {
    dlclose(m_libretroClient);
    m_libretroClient = NULL;
  }

  m_strId.clear();
  m_strLibraryDirectory.clear();
  m_strSystemDirectory.clear();
  m_strContentDirectory.clear();
  m_strSaveDirectory.clear();
}

// Get directory part of path, or empty if path doesn't contain any directory separators
string GetDirectory(const string& path)
{
  size_t pos = path.find_last_of("/\\");
  if (pos != 0 && pos != string::npos)
  {
    // Don't include trailing slash, it causes some libretro clients to fail
    return path.substr(0, pos);
  }
  return "";
}

// Get filename part of path, or entire path if path doesn't contain any directory separators
string GetFilename(const string& path)
{
  size_t pos = path.find_last_of("/\\");
  if (pos == string::npos)
    return path;
  else
    return path.substr(pos + 1);
}

// If filename contains ".", the "." and trailing extension will be removed
string RemoveExtension(const string& filename)
{
  size_t pos = filename.find_last_of(".");
  if (pos == string::npos)
    return filename;
  else
    return filename.substr(0, pos);
}

// If libraryName ends in "_libretro", the "_libretro" part will be stripped
string RemoveLibretroSuffix(const string& libraryName)
{
  // TODO: Also check if string ends in "_libretro"
  if (libraryName.length() < strlen(LIBRETRO_SUFFIX))
    return libraryName;
  else
    return libraryName.substr(0, libraryName.length() - strlen(LIBRETRO_SUFFIX));
}

// Replace "_" with "."
string ReplaceUnderscoreWithPeriod(const string& str)
{
  string strCopy(str);
  for (string::iterator it = strCopy.begin(); it != strCopy.end(); ++it)
  {
    if (*it == '_')
      *it = '.';
  }
  return strCopy;
}

string PrependAddonType(const string& baseId)
{
  return ADDON_ID_TYPE + baseId;
}

// Convert functionPtr to a string literal
#define LIBRETRO_REGISTER_SYMBOL(dll, functionPtr)  RegisterSymbol(dll, functionPtr, #functionPtr)

// Register symbols from DLL, cast to type T and store in member variable
template <typename T>
bool RegisterSymbol(void* dll, T& functionPtr, const char* strFunctionPtr)
{
  return (functionPtr = (T)dlsym(dll, strFunctionPtr)) != NULL;
}

// Trailing slash causes some libretro cores to fail
void RemoveSlashAtEnd(std::string& path)
{
  if (!path.empty())
  {
    char last = path[path.size() - 1];
    if (last == '/' || last == '\\')
      path.erase(path.size() - 1);
  }
}

bool CLibretroDLL::Load(const game_client_properties& gameClientProps)
{
  Unload();

  m_libretroClient = dlopen(gameClientProps.library_path, RTLD_LAZY);
  if (m_libretroClient == NULL)
  {
    printf("Unable to load %s", dlerror());
    return false;
  }

  try
  {
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_environment)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_video_refresh)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_audio_sample)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_audio_sample_batch)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_input_poll)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_input_state)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_init)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_deinit)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_api_version)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_get_system_info)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_get_system_av_info)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_set_controller_port_device)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_reset)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_run)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_serialize_size)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_serialize)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_unserialize)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_cheat_reset)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_cheat_set)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_load_game)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_load_game_special)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_unload_game)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_get_region)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_get_memory_data)) throw false;
    if (!LIBRETRO_REGISTER_SYMBOL(m_libretroClient, retro_get_memory_size)) throw false;
  }
  catch (const bool& bSuccess)
  {
    printf("Unable to assign function %s", dlerror());
    return bSuccess;
  }

  /*
   * ID is determined from dll name. Remove the trailing "_libretro" and
   * extension, convert "_" to "." and prefix with "gameclient.", e.g:
   * bsnes_accuracy_libretro.dylib -> gameclient.bsnes.accuracy
   */
  m_strId = PrependAddonType(
            ReplaceUnderscoreWithPeriod(
            RemoveLibretroSuffix(
            RemoveExtension(
            GetFilename(gameClientProps.library_path)))));

  m_strLibraryDirectory = GetDirectory(gameClientProps.library_path);
  m_strSystemDirectory  = gameClientProps.system_directory;
  m_strContentDirectory = gameClientProps.content_directory;
  m_strSaveDirectory    = gameClientProps.save_directory;

  // Trailing slash causes some libretro cores to fail
  RemoveSlashAtEnd(m_strLibraryDirectory);
  RemoveSlashAtEnd(m_strSystemDirectory);
  RemoveSlashAtEnd(m_strContentDirectory);
  RemoveSlashAtEnd(m_strSaveDirectory);

  return true;
}
