# Conda's cmake does not support https so the regular
# file DOWNLOAD may fail. This adds a fallback path.
function(download URL DESTINATION)
    file(DOWNLOAD ${URL} ${DESTINATION} STATUS status)
    list(GET status 0 error)
    if(error)
        execute_process(COMMAND wget -q -O ${DESTINATION} ${URL}
                        RESULT_VARIABLE error)
    endif()
    if(error)
        execute_process(COMMAND curl --create-dirs -fsSL -o ${DESTINATION} ${URL}
                        RESULT_VARIABLE error)
    endif()
    if(error)
        message(FATAL_ERROR "Could not download ${URL}")
    endif()
endfunction()

# Download tar.gz file from URL, extract it and copy
# files given by ARGN glob expressions to DIR.
function(download_tar_gz URL DIR)
    set(tmp_dir "${CMAKE_CURRENT_SOURCE_DIR}/deps/tmp")
    set(tar_file "${tmp_dir}/tmp.tar.gz")
    download("${url}/${first_file}" ${tar_file})
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar xzf ${tar_file} WORKING_DIRECTORY ${tmp_dir}
                    RESULT_VARIABLE error)
    if(error)
        message(FATAL_ERROR "Could not extract ${URL}")
    endif()
    file(REMOVE ${tar_file})

    file(MAKE_DIRECTORY ${DIR})
    foreach(file_expr ${ARGN})
        file(GLOB path "${tmp_dir}/${file_expr}")
        get_filename_component(filename ${path} NAME)
        file(RENAME ${path} "${DIR}/${filename}")
    endforeach()
    file(REMOVE_RECURSE ${tmp_dir})
endfunction()

# Download a dependency from the given URL. The files to download
# are given by ARGN. If the first file is *.tar.gz, the following
# argument must be a glob pattern specifying the files to extract.
# The version number is saved in a file along with the dependency.
# If a matching version already exists, the download is skipped.
function(download_dependency NAME VERSION URL_FMT FIRST_FILE_FMT)
    set(dir "${CMAKE_CURRENT_SOURCE_DIR}/deps/${NAME}")

    set(version_file "${dir}/_pybinding_dependency_version")
    if(EXISTS ${version_file})
        file(READ ${version_file} cached_version)
    endif()

    if(NOT "${cached_version}" STREQUAL "${VERSION}")
        if(EXISTS ${dir})
            file(REMOVE_RECURSE ${dir})
            message(STATUS "Removed cached ${NAME} ${cached_version}")
        endif()

        message(STATUS "Downloading ${NAME} v${VERSION}...")
        string(CONFIGURE ${URL_FMT} url)
        string(CONFIGURE ${FIRST_FILE_FMT} first_file)

        if(${first_file} MATCHES ".*\\.tar\\.gz")
            download_tar_gz(${url} ${dir} ${ARGN})
        else()
            foreach(file_fmt ${first_file} ${ARGN})
                string(CONFIGURE ${file_fmt} file)
                download("${url}/${file}" "${dir}/${file}")
            endforeach()
        endif()

        file(WRITE ${version_file} ${VERSION})
    endif()

    string(TOUPPER ${NAME} upper_name)
    set(${upper_name}_VERSION ${VERSION} PARENT_SCOPE)
    set(${upper_name}_INCLUDE_DIR ${dir} PARENT_SCOPE)
endfunction()
