replace
=======
作用
==
和shell提供的 sed 一样,就是在文件中查找替换字符串的.

不过这个默认遍历当前目录的所有子目录的所有文件.

为什么要有这个
==
我喜欢用 vim,没有 IDE 替换一个项目的n多文件有些麻烦.(别让我用vim的替换!)

sed 有些反人类,看看这个

    sed -i "s/要查找的字符串/替换字符串/g" `grep "要查找的字符串" -rl 目录`

我还没提字符串里要是有要转义的字符的情况呢.

install
==

    chmod a+x replace.py
    sudo mv replace.py /usr/local/bin

使用
==

    replace.py 要替换的字符串 替换成什么


不支持正则,也就不需要有字符转义,就是替换.

小心使用,会替换所有子目录里的文件的
