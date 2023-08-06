cmake_minimum_required(VERSION 3.13)

project(${service_name} VERSION ${version} LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# Find sila_cpp library
find_package(sila_cpp CONFIG REQUIRED)
set(LIBS_SILA_CPP sila2::sila_cpp)

set(PROTOS
${indent(4):cmake_protos_declaration}
)

protoc_generate_cpp(PROTO_SRCS IMPL_SRCS $${PROTOS})

add_library($${PROJECT_NAME}Features
    $${PROTO_SRCS}
    $${IMPL_SRCS}
)
target_link_libraries($${PROJECT_NAME}Features
    $${LIBS_SILA_CPP}
)

foreach(_target
    $${PROJECT_NAME}Client $${PROJECT_NAME}Server)
    add_executable($${_target} "$${_target}.cpp")
    target_link_libraries($${_target}
        $${PROJECT_NAME}Features
    )
endforeach()

# The server need the FDL files which are compiled into the binary using the resource file
target_sources($${PROJECT_NAME}Server PRIVATE $${PROJECT_NAME}.qrc)
