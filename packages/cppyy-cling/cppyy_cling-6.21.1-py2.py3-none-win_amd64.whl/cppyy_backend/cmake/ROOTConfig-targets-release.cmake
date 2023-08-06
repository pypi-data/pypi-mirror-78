#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ROOT::Cling" for configuration "Release"
set_property(TARGET ROOT::Cling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::Cling PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libCling.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libCling.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::Cling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::Cling "${_IMPORT_PREFIX}/lib/libCling.lib" "${_IMPORT_PREFIX}/bin/libCling.dll" )

# Import target "ROOT::ThreadLegacy" for configuration "Release"
set_property(TARGET ROOT::ThreadLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::ThreadLegacy PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libThreadLegacy.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libThreadLegacy.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::ThreadLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::ThreadLegacy "${_IMPORT_PREFIX}/lib/libThreadLegacy.lib" "${_IMPORT_PREFIX}/bin/libThreadLegacy.dll" )

# Import target "ROOT::CoreLegacy" for configuration "Release"
set_property(TARGET ROOT::CoreLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::CoreLegacy PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libCoreLegacy.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libCoreLegacy.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::CoreLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::CoreLegacy "${_IMPORT_PREFIX}/lib/libCoreLegacy.lib" "${_IMPORT_PREFIX}/bin/libCoreLegacy.dll" )

# Import target "ROOT::bindexplib" for configuration "Release"
set_property(TARGET ROOT::bindexplib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::bindexplib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/bindexplib.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::bindexplib )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::bindexplib "${_IMPORT_PREFIX}/bin/bindexplib.exe" )

# Import target "ROOT::rmkdepend" for configuration "Release"
set_property(TARGET ROOT::rmkdepend APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::rmkdepend PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/rmkdepend.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rmkdepend )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rmkdepend "${_IMPORT_PREFIX}/bin/rmkdepend.exe" )

# Import target "ROOT::RIOLegacy" for configuration "Release"
set_property(TARGET ROOT::RIOLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::RIOLegacy PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libRIOLegacy.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libRIOLegacy.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::RIOLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::RIOLegacy "${_IMPORT_PREFIX}/lib/libRIOLegacy.lib" "${_IMPORT_PREFIX}/bin/libRIOLegacy.dll" )

# Import target "ROOT::rootcling" for configuration "Release"
set_property(TARGET ROOT::rootcling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::rootcling PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/rootcling.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rootcling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rootcling "${_IMPORT_PREFIX}/bin/rootcling.exe" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
