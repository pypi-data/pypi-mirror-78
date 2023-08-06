#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "ZLIB_INCLUDE_DIR=/root/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/root/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> ZLIB_VERSION=1.2.8 ZLIB_VERSION_STRING=1.2.8 "
#define R__CONFIGUREFEATURES  "cxx11  builtin_clang builtin_llvm builtin_zlib shared"

#endif
