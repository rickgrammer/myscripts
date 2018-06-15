#! /usr/local/bin/python3.6
import os

try:
    os.chdir(os.sys.argv[1])
except IndexError:
    print('enter a path to look for an activate file')
    exit()

def get_files(list_of_dirs, prev=False):
    if prev:
        current_dir=os.getcwd()
        os.chdir('../')
    l=[]
    for each_dir in list_of_dirs:
        if os.path.isdir(each_dir):
            os.chdir(each_dir)
            for i in os.listdir():
                l.append(os.path.abspath(i))
            os.chdir('../')
    if prev:
        os.chdir(current_dir)
    return l

search_lists = [os.listdir(), os.listdir('../'), get_files(os.listdir()), get_files(os.listdir('../'), True)]

target=None
break_again=False
for index,each_search_list in enumerate(search_lists):
    for index2,path in enumerate(each_search_list):
        if path.split('/')[-1] == 'activate':
            target=index,index2
            break_again=True
            break;
    if break_again: break

try:
    activate_path=search_lists[target[0]][target[1]]
    print(activate_path)
    os.system('/bin/bash --rcfile '+activate_path)
except:
    print('no activate file found')

