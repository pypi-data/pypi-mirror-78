import os

#后续将本地笔记中的os.py总结完成
#以及调整顺序，按照名称吧

def get_abs_path():
    #得到当前文件的绝对路径
    print(os.path.dirname(os.path.abspath(__file__)))

def get_all_files(dir_path):
    #得到指定文件夹下所有的文件和文件夹
    for one in os.listdir(dir_path):
        print(dir_path + one)

def judge_file_or_dir(file_or_dir_path):
    #判断路径是文件还是文件夹
    if os.path.isfile(file_or_dir_path):
        print(file_or_dir_path,"is a file:")
    if os.path.isdir(file_or_dir_path):
        print(file_or_dir_path,"is a dir")


