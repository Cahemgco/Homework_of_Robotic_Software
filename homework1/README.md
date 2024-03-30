# Homework 1 介绍
## 作业内容
利用OpenCV库展示图片，并利用CMakeLists.txt进行编译。

## 文件架构
```
- Homework1/
    - CMakeLists.txt：用于编译C++代码
    - show_pic.cpp：利用OpenCV库显示图像
    - pic.jpeg：显示的图像
```
## 运行方法

1. **安装 OpenCV**: 确保在系统中安装了 OpenCV 库。

2. **创建文件夹**: 在项目文件夹中创建一个新的的文件夹，并将上述三个文件放入其中。

3. **编译代码**: 在终端中进入该文件夹，并执行以下命令编译代码：

   ```bash
   mkdir build
   cd build
   cmake ..
   make
4. **运行可执行文件**：编译后将得到可执行文件show_pic，运行该文件即可展示图片。
   ```bash
   ./show_pic