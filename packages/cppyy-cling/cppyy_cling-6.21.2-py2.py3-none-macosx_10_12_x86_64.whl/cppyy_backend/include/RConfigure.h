#ifndef ROOT_RConfigure
#define ROOT_RConfigure

/* Configurations file for macosx64 */

/* #undef R__HAVE_CONFIG */

#ifdef R__HAVE_CONFIG
#define ROOTPREFIX    "$(ROOTSYS)"
#define ROOTBINDIR    "$(ROOTSYS)/bin"
#define ROOTLIBDIR    "$(ROOTSYS)/lib"
#define ROOTINCDIR    "$(ROOTSYS)/include"
#define ROOTETCDIR    "$(ROOTSYS)/etc"
#define ROOTDATADIR   ""
#define ROOTDOCDIR    ""
#define ROOTMACRODIR  ""
#define ROOTTUTDIR    ""
#define ROOTSRCDIR    "$(ROOTSYS)/src"
#define ROOTICONPATH  ""
#define TTFFONTDIR    ""
#endif

#define EXTRAICONPATH ""

#undef R__HAS_SETRESUID   /**/
#define R__HAS_PTHREAD    /**/
#undef R__USE_CXXMODULES   /**/
#define R__USE_LIBCXX    /**/
#define R__HAS_STD_STRING_VIEW   /**/
#undef R__HAS_STD_EXPERIMENTAL_STRING_VIEW   /**/
#undef R__HAS_STOD_STRING_VIEW /**/
#define R__HAS_OP_EQUAL_PLUS_STRING_VIEW /**/
#define R__HAS_STD_APPLY /**/
#define R__HAS_STD_INVOKE /**/
#define R__HAS_STD_INDEX_SEQUENCE /**/
#define R__HAS_ATTRIBUTE_ALWAYS_INLINE /**/
#define R__HAS_ATTRIBUTE_NOINLINE /**/

#if defined(R__HAS_VECCORE) && defined(R__HAS_VC)
#ifndef VECCORE_ENABLE_VC
#define VECCORE_ENABLE_VC
#endif
#endif

#define R__HAS_DEFAULT_ZLIB  /**/

#if __cplusplus > 201402L
#ifndef R__USE_CXX17
#define R__USE_CXX17
#endif
#ifdef R__USE_CXX14
#undef R__USE_CXX14
#endif
#ifdef R__USE_CXX11
#undef R__USE_CXX11
#endif

#ifndef R__HAS_STD_STRING_VIEW
#define R__HAS_STD_STRING_VIEW
#endif
#ifdef R__HAS_STD_EXPERIMENTAL_STRING_VIEW
#undef R__HAS_STD_EXPERIMENTAL_STRING_VIEW
#endif
#ifdef R__HAS_STOD_STRING_VIEW
#undef R__HAS_STOD_STRING_VIEW
#endif

#ifndef R__HAS_STD_INVOKE
#define R__HAS_STD_INVOKE
#endif
#ifndef R__HAS_STD_APPLY
#define R__HAS_STD_APPLY
#endif

#ifndef R__HAS_STD_INDEX_SEQUENCE
#define R__HAS_STD_INDEX_SEQUENCE
#endif

#elif __cplusplus > 201103L
#ifdef R__USE_CXX17
#undef R__USE_CXX17
#endif
#ifndef R__USE_CXX14
#define R__USE_CXX14
#endif
#ifdef R__USE_CXX11
#undef R__USE_CXX11
#endif

#ifndef R__HAS_STD_INDEX_SEQUENCE
#define R__HAS_STD_INDEX_SEQUENCE
#endif

#else
#ifdef R__USE_CXX17
#undef R__USE_CXX17
#endif
#ifdef R__USE_CXX14
#undef R__USE_CXX14
#endif
#ifndef R__USE_CXX11
#define R__USE_CXX11
#endif

#endif

#endif
