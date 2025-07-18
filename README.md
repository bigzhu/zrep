# zrep

[![CI](https://github.com/bigzhu/zrep/workflows/CI/badge.svg)](https://github.com/bigzhu/zrep/actions/workflows/ci.yml)
[![CodeQL](https://github.com/bigzhu/zrep/workflows/CodeQL/badge.svg)](https://github.com/bigzhu/zrep/actions/workflows/codeql.yml)
[![Release](https://github.com/bigzhu/zrep/workflows/Release/badge.svg)](https://github.com/bigzhu/zrep/actions/workflows/release.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

z replace, 用于替换文件中的字符串

## 作用

和 shell 提供的 `sed` 一样,就是在文件中查找替换字符串的.

不过这个默认遍历当前目录的所有子目录的所有文件.

## 为什么要有这个

我喜欢用 vim, 没有 IDE 替换一个项目的 n 多文件有些麻烦.(别让我用 vim 的替换!)

`sed` 有些反人类, 看看这个

    sed -i "s/要查找的字符串/替换字符串/g" `grep "要查找的字符串" -rl 目录`

我还没提字符串里要是有要转义的字符的情况呢.

加上一段引用自 [yinwang](http://www.yinwang.org/) 的说明吧:

     在我所在的软件行业里, 就有很多这样的设计错误。在我看来, 整个软件行业基本就是建立在一堆堆的设计失误之上。做程序员如此困难和辛苦, 大部分原因就是因为软件系统里面积累了大量前人的设计失误, 所以我们需要做大量的工作来弥补或者绕过。举个例子, Unix/Linux 操作系统就是一个重大的设计失误。Unix 系统的命令行, 系统 API，各种工具程序, 编辑器, 程序语言(C，C++等)，设计其实都很糟糕。很多工具程序似乎故意设计得晦涩难用, 让人摸不着头脑, 需要大量时间学习, 而且容易出错。出错之后难以发现, 难以弥补.

    然而一般程序员都没有意识到这里面的设计错误, 知道了也不敢指出来, 他们反而喜欢显示自己死记硬背得住这些稀奇古怪的规则。这就导致了软件行业的“皇帝的新装现象”——没有人敢说工具的设计有毛病, 因为如果你说出来, 别人就会认为你在抱怨, 那你不是经验不足, 就是能力不行。这就像你不敢说皇帝没穿衣服, 否则别人就会认为你就是白痴或者不称职的人! Unix 系统的同盟者和后裔们(Linux，C 语言, Go 语言)，俨然形成了这样一种霸权, 他们鄙视觉得它们难用, 质疑它们的设计的人。他们嘲笑这些用户为失败者, 即使其实有些“用户”水平比 Unix 的设计者还要高。久而久之, 他们封住了人们的嘴, 让人误以为难用的东西就是好的.

## install

```bash
pip install zrep
```

## 使用

尽量还是加上"",这样你就完全不用去管转义和特殊字符的问题了

    replace.py "要替换的字符串" "替换成什么"

- 不支持正则
- 小心使用, 会替换所有子目录里的文件的
- 已经做了限制, 不会去影响到 .git node_modules 里面的内容,也不会破坏 git node_modules
- 跳过了二进制文件
