INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ANALYZER analyzer)

FIND_PATH(
    ANALYZER_INCLUDE_DIRS
    NAMES analyzer/api.h
    HINTS $ENV{ANALYZER_DIR}/include
        ${PC_ANALYZER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ANALYZER_LIBRARIES
    NAMES gnuradio-analyzer
    HINTS $ENV{ANALYZER_DIR}/lib
        ${PC_ANALYZER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ANALYZER DEFAULT_MSG ANALYZER_LIBRARIES ANALYZER_INCLUDE_DIRS)
MARK_AS_ADVANCED(ANALYZER_LIBRARIES ANALYZER_INCLUDE_DIRS)
