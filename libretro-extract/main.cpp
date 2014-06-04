
#include "ClientBridge.h"
#include "LibretroDLL.h"
#include "LibretroEnvironment.h"
#include "xbmc_game_types.h"

#include <dirent.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

using namespace LIBRETRO;
using namespace std;

// Get directory part of path, or empty if path doesn't contain any directory separators
string GetDirectory2(const string& path)
{
  size_t pos = path.find_last_of("/\\");
  if (pos != 0 && pos != string::npos)
  {
    // Don't include trailing slash, it causes some libretro clients to fail
    return path.substr(0, pos);
  }
  return "";
}

// Trailing slash causes some libretro cores to fail
void RemoveSlashAtEnd2(string& path)
{
  if (!path.empty())
  {
    char last = path[path.size() - 1];
    if (last == '/' || last == '\\')
      path.erase(path.size() - 1);
  }
}

int main(int argc, const char* argv[])
{
  if (argc == 1)
  {
    cout << "Must call with libretro core as first argument" << endl;
    return 0;
  }

  string libraryDir = GetDirectory2(argv[1]);

  DIR* dp;
  struct dirent* ep;
  dp = opendir(libraryDir.c_str());

  if (dp == NULL)
  {
    printf("Could not open directory %s", libraryDir.c_str());
    return 1;
  }

  while ((ep = readdir(dp)) != NULL)
  {
    string name = ep->d_name;
    if (name == "." || name == "..")
      continue;

    if (name == "genesis_plus_gx_libretro.dylib" || name == "genesis_plus_gx_libretro.so")
      continue; // Thread 1: EXC_BAD_ACCESS (code=2, address=0x100207240)

    if (name == "mame078_libretro.dylib" || name == "mame078_libretro.so")
      continue; // Thread 1: EXC_BAD_ACCESS (code=1, address=0x0)

    if (name == "nxengine_libretro.dylib" || name == "nxengine_libretro.so")
      continue; // code=2

    if (name == "pcsx_rearmed_libretro.dylib" || name == "pcsx_rearmed_libretro.so")
      continue; // "Error allocating memory!"

    if (name == "prboom_libretro.dylib" || name == "prboom_libretro.so")
      continue; // code=2

    if (name == "snes9x_next_libretro.dylib" || name == "snes9x_next_libretro.so")
      continue; // code=2

    if (name == "vba_next_libretro.dylib" || name == "vba_next_libretro.so")
      continue; // error: memory read failed for 0x0

    if (name == "vbam_libretro.dylib" || name == "vbam_libretro.so")
      continue; // error: memory read failed for 0x0

    if (name == "mame_libretro.so" || name == "mame_libretro.dylib")
      continue; // Segmentation fault on linux, Bus Error 10 on OSX

    string libretroCore = libraryDir + "/" + name;

    cout << "libretroCore: " << name << endl;

    game_client_properties gameClientProps = { };
    gameClientProps.library_path      = libretroCore.c_str();
    gameClientProps.system_directory  = libraryDir.c_str();
    gameClientProps.content_directory = libraryDir.c_str();
    gameClientProps.save_directory    = libraryDir.c_str();

    CLibretroDLL* CLIENT = new CLibretroDLL();
    if (!CLIENT || !CLIENT->Load(gameClientProps))
    {
      cout << "Failed to load " << gameClientProps.library_path << endl;
      return 1;
    }

    const unsigned int version = CLIENT->retro_api_version();
    if (version != 1)
    {
      cout << "Expected libretro api v1, found version " << version << endl;
      return 1;
    }


    // Environment must be initialized before calling retro_init()
    CClientBridge* CLIENT_BRIDGE = new CClientBridge;
    CLibretroEnvironment::Initialize(CLIENT, CLIENT_BRIDGE);

    CLIENT->retro_init();

    retro_system_info info = { };
    CLIENT->retro_get_system_info(&info);
    cout << "Library name:    " << info.library_name << endl;
    cout << "supported_extensions = \"" << info.valid_extensions << "\"" << endl;
    cout << "version = \"" << info.library_version << "\"" << endl;
    cout << "need_fullpath = \"" << (info.need_fullpath ? "true" : "false") << "\"" << endl;
    cout << "block_extract = \"" << (info.block_extract ? "true" : "false") << "\"" << endl;
    cout << endl;

    // Skip deinit if name contains "mednafen_" and ".dylib"
    // Thread 1: EXC_BAD_ACCESS (code=2, address=0x7fff5bfef0)
    if (!(name.find("mednafen_") != string::npos && (name.find(".dylib") != string::npos || name.find(".so") != string::npos)))
      CLIENT->retro_deinit();

    delete CLIENT;
    delete CLIENT_BRIDGE;
  }

  closedir(dp);


  return 0;
}

