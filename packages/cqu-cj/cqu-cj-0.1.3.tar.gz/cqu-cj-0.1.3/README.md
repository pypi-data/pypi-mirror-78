# CQU-CJ
[![cqu-tool-bucket](https://img.shields.io/badge/CQU-%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A6%E5%85%A8%E5%AE%B6%E6%A1%B6%E8%AE%A1%E5%88%92-blue)](https://github.com/topics/cqu-tool-bucket)
![Liscence](https://img.shields.io/github/license/CQU-AI/cqu-cj)
[![pypi](https://img.shields.io/pypi/v/cqu-cj)](https://pypi.org/project/cqu-cj/)
![download](https://pepy.tech/badge/cqu-cj)
![Upload Python Package](https://github.com/CQU-AI/cqu-cj/workflows/Upload%20Python%20Package/badge.svg)

CQU-cj 是一个基于 Python3 的第三方重庆大学成绩查询工具。

## 特性

使用本查询工具，你可以
 - 直接生成csv格式的成绩表（可以用excel打开）
 - 无论评教与否都能查询入学以来的所有成绩
 - 查询到的数据段包括`课程编码`，`课程名称`，`成绩`，`学分`，`选修`，`课程类别`（专选，必修等），`教师`，`考试类别`，`备注`，`考试时间`
 - 开包即用，直接输入用户和密码，无需配置
 - 完美支持Mac和Linux,在Windows上也能稳定运行

## 安装和使用

1. 安装Python
2. 安装cqu-cj：`pip install cqu-cj`
3. 连接到重庆大学内网（可以不用登录上网帐号，但需要连接到CQU-WIFI或插上网线）
4. 在命令行中输入`cqu-cj`即可开始运行
5. 首次运行，需要输入学号和密码（身份证后六位）
6. 运行成功后，成绩将被保存到桌面的`成绩.csv`文件中。

帐号和密码会存储在你的电脑上，如需清除记录，可使用`cqu-cj -r`


## 声明

1. 本程序开放源代码，可自行检查是否窃取你的信息。
2. 本程序不存储用户的帐号，密码。
3. 本程序不存储任何人的成绩，所有的数据来自于重庆大学老教务网。