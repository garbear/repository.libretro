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

#include "LibretroEnvironment.h"
#include "ClientBridge.h"
#include "libretro.h"
#include "LibretroDLL.h"
#include "LibretroSettings.h"

#include <iostream>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

using namespace LIBRETRO;
using namespace std;

#define DEFAULT_NOTIFICATION_TIME_MS  3000 // Time to display toast dialogs, from AddonCallbacksAddon.cpp

CLibretroDLL*          CLibretroEnvironment::m_client = NULL;
CClientBridge*         CLibretroEnvironment::m_clientBridge = NULL;

bool   CLibretroEnvironment::m_bSupportsNoGame = false;
double CLibretroEnvironment::m_fps = 0.0;
bool   CLibretroEnvironment::m_bFramerateKnown = false;

map<string, set<string> > CLibretroEnvironment::m_variables;
map<string, string> CLibretroEnvironment::m_settings;

void CLibretroEnvironment::Initialize(CLibretroDLL* client, CClientBridge* clientBridge)
{
  m_client = client;
  m_clientBridge = clientBridge;

  // Install environment callback
  m_client->retro_set_environment(EnvironmentCallback);
}

void CLibretroEnvironment::Deinitialize()
{
}

void CLibretroEnvironment::UpdateFramerate(double fps)
{
  m_fps = fps;
  m_bFramerateKnown = true;
}

bool CLibretroEnvironment::EnvironmentCallback(unsigned int cmd, void* data)
{
  if (!m_client || !m_clientBridge)
    return false;

  switch (cmd)
  {
  case RETRO_ENVIRONMENT_SET_ROTATION:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_OVERSCAN:
    {
      bool* typedData = reinterpret_cast<bool*>(data);
      if (typedData)
        *typedData = false;
      break;
    }
  case RETRO_ENVIRONMENT_GET_CAN_DUPE:
    {
      bool* typedData = reinterpret_cast<bool*>(data);
      if (typedData)
        *typedData = true;
      break;
    }
  case RETRO_ENVIRONMENT_SET_MESSAGE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_SHUTDOWN:
    {
      break;
    }
  case RETRO_ENVIRONMENT_SET_PERFORMANCE_LEVEL:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_SYSTEM_DIRECTORY:
    {
      const char** typedData = reinterpret_cast<const char**>(data);
      if (typedData)
      {
        if (!m_client->GetSystemDirectory().empty())
          *typedData = m_client->GetSystemDirectory().c_str();
        else
          *typedData = NULL;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_PIXEL_FORMAT:
    {
      const retro_pixel_format* typedData = reinterpret_cast<const retro_pixel_format*>(data);
      if (!typedData)
        return false;
      break;
    }
  case RETRO_ENVIRONMENT_SET_INPUT_DESCRIPTORS:
    {
      break;
    }
  case RETRO_ENVIRONMENT_SET_KEYBOARD_CALLBACK:
    {
      const retro_keyboard_callback* typedData = reinterpret_cast<const retro_keyboard_callback*>(data);
      if (typedData)
      {
        // Store callback from libretro client
        m_clientBridge->m_retro_keyboard_event = typedData->callback;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_DISK_CONTROL_INTERFACE:
    {
      const retro_disk_control_callback* typedData = reinterpret_cast<const retro_disk_control_callback*>(data);
      if (typedData)
      {
        // Store callbacks from libretro client
        m_clientBridge->m_retro_disk_set_eject_state     = typedData->set_eject_state;
        m_clientBridge->m_retro_disk_get_eject_state     = typedData->get_eject_state;
        m_clientBridge->m_retro_disk_get_image_index     = typedData->get_image_index;
        m_clientBridge->m_retro_disk_set_image_index     = typedData->set_image_index;
        m_clientBridge->m_retro_disk_get_num_images      = typedData->get_num_images;
        m_clientBridge->m_retro_disk_replace_image_index = typedData->replace_image_index;
        m_clientBridge->m_retro_disk_add_image_index     = typedData->add_image_index;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_HW_RENDER:
    {
      retro_hw_render_callback* typedData = reinterpret_cast<retro_hw_render_callback*>(data);
      if (typedData)
      {
        // Store callbacks from libretro client
        m_clientBridge->m_retro_hw_context_reset   = typedData->context_reset;
        m_clientBridge->m_retro_hw_context_destroy = typedData->context_destroy;
      }
      break;
    }
  case RETRO_ENVIRONMENT_GET_VARIABLE:
    {
      retro_variable* typedData = reinterpret_cast<retro_variable*>(data);
      if (typedData)
      {
        typedData->value = NULL;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_VARIABLES:
    {
      const retro_variable* typedData = reinterpret_cast<const retro_variable*>(data);
      if (typedData)
      {
        //cout << "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>" << endl;
        //cout << "<settings>" << endl;
        //cout << "\t<category label=\"32001\">" << endl;

        vector<retro_variable> variables;
        for (const retro_variable* variable = typedData; variable->key && variable->value; variable++)
          variables.push_back(*variable);

        const string addonDir = m_client->GetLibraryDirectory()      +
                                "/../../../libretro-extract/addons/" +
                                m_client->GetID();
        CLibretroSettings settings(addonDir, variables);
        settings.PrintSettings();
        settings.PrintLanguage();
      }
      break;
    }
  case RETRO_ENVIRONMENT_GET_VARIABLE_UPDATE:
    {
      bool* typedData = reinterpret_cast<bool*>(data);
      if (typedData)
      {
        // TODO: Need to return true if the setting's value has changed
        *typedData = false;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_SUPPORT_NO_GAME:
    {
      const bool* typedData = reinterpret_cast<const bool*>(data);
      if (typedData)
      {
        // Store this value so that it can be queried directly via the Game API
        m_bSupportsNoGame = *typedData;
        cout << "supports_no_game = \"" << (m_bSupportsNoGame ? "true" : "false") << "\"" << endl;
      }
      break;
    }
  case RETRO_ENVIRONMENT_GET_LIBRETRO_PATH:
    {
      const char** typedData = reinterpret_cast<const char**>(data);
      if (typedData)
      {
        if (!m_client->GetLibraryDirectory().empty())
          *typedData = m_client->GetLibraryDirectory().c_str();
        else
          *typedData = NULL;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_AUDIO_CALLBACK:
    {
      const retro_audio_callback* typedData = reinterpret_cast<const retro_audio_callback*>(data);
      if (typedData)
      {
        // Store callbacks from libretro client
        m_clientBridge->m_retro_audio_callback           = typedData->callback;
        m_clientBridge->m_retro_audio_set_state_callback = typedData->set_state;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_FRAME_TIME_CALLBACK:
    {
      const retro_frame_time_callback* typedData = reinterpret_cast<const retro_frame_time_callback*>(data);
      if (typedData)
      {
        // Store callback from libretro client
        m_clientBridge->m_retro_frame_time_callback = typedData->callback;
      }
      break;
    }
  case RETRO_ENVIRONMENT_GET_RUMBLE_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_INPUT_DEVICE_CAPABILITIES:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_SENSOR_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_CAMERA_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_LOG_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_PERF_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_LOCATION_INTERFACE:
    {
      break;
    }
  case RETRO_ENVIRONMENT_GET_CONTENT_DIRECTORY:
    {
      const char** typedData = reinterpret_cast<const char**>(data);
      if (typedData)
      {
        if (!m_client->GetContentDirectory().empty())
          *typedData = m_client->GetContentDirectory().c_str();
        else
          *typedData = NULL;
      }
      break;
    }
  case RETRO_ENVIRONMENT_GET_SAVE_DIRECTORY:
    {
      const char** typedData = reinterpret_cast<const char**>(data);
      if (typedData)
      {
        if (!m_client->GetSaveDirectory().empty())
          *typedData = m_client->GetSaveDirectory().c_str();
        else
          *typedData = NULL;
      }
      break;
    }
  case RETRO_ENVIRONMENT_SET_SYSTEM_AV_INFO:
    {
      break;
    }
  }

  return true;
}
