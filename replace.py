#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tempfile import mkstemp
from shutil import move
import os
import sys


def check(open_file, pattern):
    '''检查是否有需要替换的内容'''
    if pattern in open_file.read():
        return True


def replace(file_path, pattern, subst):
    '''进行替换'''
    #Create temp file
    old_file = open(file_path)
    if check(old_file, pattern):
        print '替换: ' + file_path
        old_file.seek(0)
        old_file = open(file_path)
        fh, abs_path = mkstemp()
        new_file = open(abs_path, 'w')
        for line in old_file:
            new_file.write(line.replace(pattern, subst))
        #close temp file
        new_file.close()
        os.close(fh)
        old_file.close()
        #Remove original file
        os.remove(file_path)
        #Move new file
        move(abs_path, file_path)


file_paths = []


def getFilePath(root_path):
    for lists in os.listdir(root_path):
        the_path = os.path.join(root_path, lists)
        if os.path.isdir(the_path):
            getFilePath(the_path)
        else:
            file_paths.append(the_path)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        pattern = sys.argv[1]
        subst = sys.argv[2]
        print '%s 将被替换为 %s' % (pattern, subst)
        path = os.getcwd()
        getFilePath(path)
        for file_path in file_paths:
            replace(file_path, pattern, subst)
    else:
        print '需要输入参数:'
        print 'python %s 待替换字符 替换成这个' % sys.argv[0]
