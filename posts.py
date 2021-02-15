#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import prettytable as pt


def get_all_markdown_files():
    items = os.listdir('source/_posts')
    files = []
    for item in items:
        item_path = os.path.join(os.getcwd(), 'source/_posts/' + item)
        if os.path.isfile(item_path):
            files.append(item_path)
    return files

def get_markdown_front_matter(path):
    fms = {}
    with open(path, 'r', encoding='utf-8-sig') as md:

        # 将文件指针移动到第一个FrontMatter
        start_line = md.readline().replace('\n', '').replace('\r', '').replace('\r\n', '')
        while start_line != '---':
            start_line = md.readline().replace('\n', '').replace('\r', '').replace('\r\n', '')
        
        lines = []

        # 读取FrontMatter数据
        end_line = md.readline().replace('\n', '').replace('\r', '').replace('\r\n', '')
        while end_line != '---':
            lines.append(end_line)
            end_line = md.readline().replace('\n', '').replace('\r', '').replace('\r\n', '').replace("'", '')

        # 解析数据
        for line in lines:
            arr = line.split(': ')
            fms[arr[0].lstrip().rstrip()] = arr[1].lstrip().rstrip()

    return fms



if __name__ == '__main__':
    files = get_all_markdown_files()

    tb = pt.PrettyTable()
    tb.field_names = ['标题', '文件位置', '分类', '置顶', '创建日期']
    
    for file in files:
        fms = get_markdown_front_matter(file)
        title = '《' + fms['title'] + '》' if 'title' in fms.keys() else ''
        filename = '@Hexo/source/_posts/' + fms['filename'] if 'filename' in fms.keys() else ''
        category = fms['category'] if 'category' in fms.keys() else ''
        top = ('是' if fms['top'].lower() == 'true' else '') if 'top' in fms.keys() else ''
        date = fms['date'] if 'date' in fms.keys() else ''
        tb.add_row([title, filename, category, top, date])
    
    print(tb)
