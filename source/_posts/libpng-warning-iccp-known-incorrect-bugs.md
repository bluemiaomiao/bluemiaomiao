---
title: 解决libpng warning iccp known incorrect
tags: ['libpng', 'iccp', '错误集锦']
date: 2021-01-28 19:38:33
category: 运维错误集锦
description: '本文摘要: 解决libpng库产生的warning警告信息'
top: false
filename: libpng-warning-iccp-known-incorrect-bugs.md
---

> 本文章迁移自[https://blog.51cto.com/xvjunjie/2348645](https://blog.51cto.com/xvjunjie/2348645), 原站点不再更新。[感谢有你, 一路相伴。](https://blog.51cto.com/xvjunjie/2563261)

# 一、下载libpng源代码

```bash
wget https://sourceforge.net/projects/libpng/files/libpng16/1.6.36/libpng-1.6.36.tar.xz
```

# 二、修改`png.c`文件

```c
if (png_sRGB_checks[i].is_broken != 0)
{
     /* These profiles are known to have bad data that may cause
        * problems if they are used, therefore attempt to
        * discourage their use, skip the 'have_md5' warning below,
        * which is made irrelevant by this error.
        */
     // 注释掉下边这两行代码
     // png_chunk_report(png_ptr, "known incorrect sRGB profile",
     //     PNG_CHUNK_ERROR);
}
```

# 三、编译安装覆盖原来的可执行文件

> 以Ubuntu发行版为例, 其他发行版类似

```bash
sudo apt install zlib* -y
sudo apt install gcc make cmake -y
./configure && make -j && sudo make install
```
