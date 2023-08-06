// STL headers
#if __has_include("cstdlib")
#include <cstdlib>
#endif
#if __has_include("csignal")
#include <csignal>
#endif
#if __has_include("csetjmp")
#include <csetjmp>
#endif
#if __has_include("cstdarg")
#include <cstdarg>
#endif
#if __has_include("typeinfo")
#include <typeinfo>
#endif
#if __has_include("typeindex")
#include <typeindex>
#endif
#if __has_include("type_traits")
#include <type_traits>
#endif
#if __has_include("bitset")
#include <bitset>
#endif
#if __has_include("functional")
#include <functional>
#endif
#if __has_include("utility")
#include <utility>
#endif
#if __has_include("ctime")
#include <ctime>
#endif
#if __has_include("chrono")
#include <chrono>
#endif
#if __has_include("cstddef")
#include <cstddef>
#endif
#if __has_include("initializer_list")
#include <initializer_list>
#endif
#if __has_include("tuple")
#include <tuple>
#endif
#if __has_include("new")
#include <new>
#endif
#if __has_include("memory")
#include <memory>
#endif
#if __has_include("scoped_allocator")
#include <scoped_allocator>
#endif
#if __has_include("climits")
#include <climits>
#endif
#if __has_include("cfloat")
#include <cfloat>
#endif
#if __has_include("cstdint")
#include <cstdint>
#endif
#if __has_include("cinttypes")
#include <cinttypes>
#endif
#if __has_include("limits")
#include <limits>
#endif
#if __has_include("exception")
#include <exception>
#endif
#if __has_include("stdexcept")
#include <stdexcept>
#endif
#if __has_include("cassert")
#include <cassert>
#endif
#if __has_include("system_error")
#include <system_error>
#endif
#if __has_include("cerrno")
#include <cerrno>
#endif
#if __has_include("cctype")
#include <cctype>
#endif
#if __has_include("cwctype")
#include <cwctype>
#endif
#if __has_include("cstring")
#include <cstring>
#endif
#if __has_include("cwchar")
#include <cwchar>
#endif
#if __has_include("cuchar")
#include <cuchar>
#endif
#if __has_include("string")
#include <string>
#endif
#if __has_include("array")
#include <array>
#endif
#if __has_include("vector")
#include <vector>
#endif
#if __has_include("deque")
#include <deque>
#endif
#if __has_include("list")
#include <list>
#endif
#if __has_include("forward_list")
#include <forward_list>
#endif
#if __has_include("set")
#include <set>
#endif
#if __has_include("map")
#include <map>
#endif
#if __has_include("unordered_set")
#include <unordered_set>
#endif
#if __has_include("unordered_map")
#include <unordered_map>
#endif
#if __has_include("stack")
#include <stack>
#endif
#if __has_include("queue")
#include <queue>
#endif
#if __has_include("algorithm")
#include <algorithm>
#endif
#if __has_include("iterator")
#include <iterator>
#endif
#if __has_include("cmath")
#include <cmath>
#endif
#if __has_include("complex")
#include <complex>
#endif
#if __has_include("random")
#include <random>
#endif
#if __has_include("numeric")
#include <numeric>
#endif
#if __has_include("ratio")
#include <ratio>
#endif
#if __has_include("cfenv")
#include <cfenv>
#endif
#if __has_include("iosfwd")
#include <iosfwd>
#endif
#if __has_include("ios")
#include <ios>
#endif
#if __has_include("istream")
#include <istream>
#endif
#if __has_include("ostream")
#include <ostream>
#endif
#if __has_include("iostream")
#include <iostream>
#endif
#if __has_include("fstream")
#include <fstream>
#endif
#if __has_include("sstream")
#include <sstream>
#endif
#if __has_include("iomanip")
#include <iomanip>
#endif
#if __has_include("streambuf")
#include <streambuf>
#endif
#if __has_include("cstdio")
#include <cstdio>
#endif
#if __has_include("locale")
#include <locale>
#endif
#if __has_include("clocale")
#include <clocale>
#endif
#if __has_include("atomic")
#include <atomic>
#endif
#if __has_include("thread")
#include <thread>
#endif
#if __has_include("mutex")
#include <mutex>
#endif
#if __has_include("future")
#include <future>
#endif
#if __has_include("condition_variable")
#include <condition_variable>
#endif
#if __has_include("ciso646")
#include <ciso646>
#endif
#if __has_include("ccomplex")
#include <ccomplex>
#endif
#if __has_include("regex")
#include <regex>
#endif
#if __has_include("shared_mutex")
#include <shared_mutex>
#endif
#if __has_include("any")
#include <any>
#endif
#if __has_include("optional")
#include <optional>
#endif
#if __has_include("variant")
#include <variant>
#endif
#if __has_include("memory_resource")
#include <memory_resource>
#endif
#if __has_include("string_view")
#include <string_view>
#endif
#if __has_include("charconv")
#include <charconv>
#endif
#if __has_include("filesystem")
#include <filesystem>
#endif
// treat regex separately
#if __has_include("regex") && !defined __APPLE__
#include <regex>
#endif
// STL Deprecated headers
#define _BACKWARD_BACKWARD_WARNING_H
#pragma clang diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated"
#if __has_include("strstream")
#include <strstream>
#endif
#pragma clang diagnostic pop
#undef _BACKWARD_BACKWARD_WARNING_H
#include "etc/cling/Interpreter/DynamicLookupRuntimeUniverse.h"
#include "etc/cling/Interpreter/DynamicLookupLifetimeHandler.h"
#include "etc/cling/Interpreter/Exception.h"
#include "etc/cling/Interpreter/RuntimePrintValue.h"
#include "etc/cling/Interpreter/RuntimeUniverse.h"
#include "etc/cling/Interpreter/Value.h"
// ./core/thread/G__ThreadLegacy.cxx
#include "TPosixCondition.h"
#include "TPosixMutex.h"
#include "TPosixThread.h"
#include "TPosixThreadFactory.h"
#include "PosixThreadInc.h"
#include "TCondition.h"
#include "TConditionImp.h"
#include "ThreadLocalStorage.h"
#include "TMutex.h"
#include "TMutexImp.h"
#include "TThreadFactory.h"
#include "TThread.h"
#include "TThreadImp.h"
#include "ROOT/TReentrantRWLock.hxx"
#include "ROOT/TSpinMutex.hxx"
// ./io/io/G__RIOLegacy.cxx
#include "TBufferFile.h"
#include "TBufferIO.h"
#include "TCollectionProxyFactory.h"
#include "TContainerConverters.h"
#include "TEmulatedMapProxy.h"
#include "TEmulatedCollectionProxy.h"
#include "TDirectoryFile.h"
#include "TFree.h"
#include "TFile.h"
#include "TGenCollectionStreamer.h"
#include "TGenCollectionProxy.h"
#include "TKey.h"
#include "TMemFile.h"
#include "TStreamerInfoActions.h"
#include "TVirtualCollectionIterators.h"
#include "TStreamerInfo.h"
#include "TVirtualArray.h"
// ./core/G__CoreLegacy.cxx
#include "Bytes.h"
#include "Byteswap.h"
#include "Riostream.h"
#include "Rtypes.h"
#include "TApplication.h"
#include "TBuffer.h"
#include "TDatime.h"
#include "TDirectory.h"
#include "TEnv.h"
#include "TError.h"
#include "TException.h"
#include "TInetAddress.h"
#include "TMathBase.h"
#include "TMD5.h"
#include "TMemberInspector.h"
#include "TNamed.h"
#include "TObject.h"
#include "TObjString.h"
#include "TProcessID.h"
#include "TProcessUUID.h"
#include "TRegexp.h"
#include "TROOT.h"
#include "TStorage.h"
#include "TString.h"
#include "TSysEvtHandler.h"
#include "TSystem.h"
#include "TThreadSlots.h"
#include "TTime.h"
#include "TTimeStamp.h"
#include "TUrl.h"
#include "TUUID.h"
#include "TVersionCheck.h"
#include "TVirtualMutex.h"
#include "TVirtualRWMutex.h"
#include "strlcpy.h"
#include "snprintf.h"
#include "TArrayC.h"
#include "TArray.h"
#include "TBits.h"
#include "TClassTable.h"
#include "TCollection.h"
#include "TCollectionProxyInfo.h"
#include "TExMap.h"
#include "THashList.h"
#include "THashTable.h"
#include "TIterator.h"
#include "TList.h"
#include "TMap.h"
#include "TObjArray.h"
#include "TObjectTable.h"
#include "TOrdCollection.h"
#include "TSeqCollection.h"
#include "TVirtualCollectionProxy.h"
#include "ESTLType.h"
#include "RStringView.h"
#include "TClassEdit.h"
#include "ROOT/RMakeUnique.hxx"
#include "ROOT/RSpan.hxx"
#include "ROOT/RStringView.hxx"
#include "ROOT/TypeTraits.hxx"
#include "TUnixSystem.h"
#include "root_std_complex.h"
#include "TClingRuntime.h"
#include "TBaseClass.h"
#include "TClassGenerator.h"
#include "TClass.h"
#include "TClassRef.h"
#include "TClassStreamer.h"
#include "TDataMember.h"
#include "TDataType.h"
#include "TDictAttributeMap.h"
#include "TDictionary.h"
#include "TEnumConstant.h"
#include "TEnum.h"
#include "TFunction.h"
#include "TFunctionTemplate.h"
#include "TGenericClassInfo.h"
#include "TGlobal.h"
#include "TInterpreter.h"
#include "TInterpreterValue.h"
#include "TIsAProxy.h"
#include "TListOfDataMembers.h"
#include "TListOfEnums.h"
#include "TListOfEnumsWithLock.h"
#include "TListOfFunctions.h"
#include "TListOfFunctionTemplates.h"
#include "TMemberStreamer.h"
#include "TMethodArg.h"
#include "TMethod.h"
#include "TProtoClass.h"
#include "TRealData.h"
#include "TStreamerElement.h"
#include "TStreamer.h"
#include "TVirtualIsAProxy.h"
#include "TVirtualStreamerInfo.h"
#include "Getline.h"
