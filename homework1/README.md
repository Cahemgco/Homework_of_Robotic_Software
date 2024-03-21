# Homework 1 介绍
## 作业内容
利用OpenCV库展示图片，并利用CMakeLists.txt进行编译。

## 文件架构
本文件夹包括以下三个文件：

1. **CMakeLists.txt**: 这是一个CMake构建系统所需的配置文件。它指导CMake如何编译项目。通常包括编译选项、链接库等信息。下面是一个简单的示例：

    ```cmake
    cmake_minimum_required(VERSION 3.1)
    project(show_pic)

    find_package(OpenCV REQUIRED)
    include_directories(${OpenCV_INCLUDE_DIRS})
    add_executable(show_pic show_pic.cpp)
    TARGET_LINK_LIBRARIES(show_pic ${OpenCV_LIBS})
    ```

2. **show_pic.cpp**: 这是一个C++源代码文件，使用了OpenCV库来展示名为pic.jpeg的图像。代码如下：

    ```cpp
    #include<iostream>
    #include<opencv2/opencv.hpp>

    using namespace std;
    using namespace cv;

    int main(void)
    {

        Mat image=imread("pic.jpeg");
        namedWindow("demo", 0);
        resizeWindow("demo", 500, 500);
        imshow("demo", image);
        waitKey(1000);
        destroyAllWindows();
        return 0;

    }
    ```

3. **pic.jpeg**: 这是一个JPEG格式的图像文件，用于展示。

这些文件组成了一个简单的项目，通过CMakeLists.txt配置文件可以使用CMake编译并链接show_pic.cpp文件，从而生成一个可以展示pic.jpeg图像的可执行文件。

## 运行方法

1. **安装 OpenCV**: 确保在您的系统中安装了 OpenCV 库。

2. **创建文件夹**: 在项目文件夹中创建一个新的的文件夹，并将上述三个文件放入其中。

3. **编译代码**: 在终端中进入该 文件夹，并执行以下命令编译代码：

   ```bash
   mkdir build
   cd build
   cmake ..
   make
4. **运行可执行文件**：编译后将得到可执行文件show_pic，运行该文件即可展示图片。
   ```bash
   ./show_pic