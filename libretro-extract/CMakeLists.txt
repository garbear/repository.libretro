cmake_minimum_required(VERSION 2.6)
project(libretro-extract)

set(SRCS
	ClientBridge.cpp
	LibretroDLL.cpp
	LibretroEnvironment.cpp
	main.cpp
)

set(LIBRETRO_EXTRACT_EXECUTABLE libretro-extract)
add_executable(${LIBRETRO_EXTRACT_EXECUTABLE} ${SRCS})
target_link_libraries(${LIBRETRO_EXTRACT_EXECUTABLE} ${CMAKE_DL_LIBS})

