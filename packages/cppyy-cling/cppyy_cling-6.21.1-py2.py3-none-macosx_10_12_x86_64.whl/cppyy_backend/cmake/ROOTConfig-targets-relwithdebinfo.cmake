#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ROOT::Cling" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::Cling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::Cling PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libCling.so"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libCling.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::Cling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::Cling "${_IMPORT_PREFIX}/lib/libCling.so" )

# Import target "ROOT::ThreadLegacy" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::ThreadLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::ThreadLegacy PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libThreadLegacy.so"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libThreadLegacy.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::ThreadLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::ThreadLegacy "${_IMPORT_PREFIX}/lib/libThreadLegacy.so" )

# Import target "ROOT::CoreLegacy" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::CoreLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::CoreLegacy PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libCoreLegacy.so"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libCoreLegacy.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::CoreLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::CoreLegacy "${_IMPORT_PREFIX}/lib/libCoreLegacy.so" )

# Import target "ROOT::rmkdepend" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::rmkdepend APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::rmkdepend PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/rmkdepend"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rmkdepend )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rmkdepend "${_IMPORT_PREFIX}/bin/rmkdepend" )

# Import target "ROOT::RIOLegacy" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::RIOLegacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::RIOLegacy PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libRIOLegacy.so"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libRIOLegacy.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::RIOLegacy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::RIOLegacy "${_IMPORT_PREFIX}/lib/libRIOLegacy.so" )

# Import target "ROOT::rootcling" for configuration "RelWithDebInfo"
set_property(TARGET ROOT::rootcling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ROOT::rootcling PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/rootcling"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rootcling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rootcling "${_IMPORT_PREFIX}/bin/rootcling" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
