import os
import argparse
import hashlib
import time

# 解析命令行参数
parser = argparse.ArgumentParser(description='Compare files in multiple folders.')
parser.add_argument('folders', metavar='FOLDER', type=str, nargs='+',
                    help='path to the folder')
args = parser.parse_args()  # print(args.folders) # 将参数输出为列表，类似后面的形式 ['D:\\1']

# 校验文件或文件夹是否存在
def check_file_or_folder(path):
    if os.path.exists(path):
        return True  # print(f"{path} 存在。")
    else:
        return False  # print(f"{path} 不存在。")

# 读取多层嵌套文件夹的文件
def read_files_in_directory(directory):
    file_lists = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_lists.append(file_path)  # print(f"读取文件: {file_path}")
    return file_lists

# 检查文件大小，输入一个文件列表，筛选出文件大小相同的文件
def check_folder_duplicate_size(files_path):
    file_size_dict = {}
    for file in files_path:
        file_size = os.path.getsize(file)
        file_size_dict.update({file: file_size})
    # print(file_size_dict)  # 输出文件名和文件大小的列表  {'d:\\1\\新建 M作表.xlsx': 6601, 'd:\\1\\新建 文本文档.txt': 0}
    result = [[k for k, v in file_size_dict.items() if v == value] for value in
              set(file_size_dict.values())]  # 将字典中值相同的 他们的键放到字典里面
    return result  # print(result)  # 将所有文件大小相同的列出来

# 检查文件hash，输入一个文件列表，筛选出文件大小相同的文件
def check_file_hash(file_path):
    hash_type = 'md5'  # 选择哈希算法
    hash_dict = {}
    for file in file_path:
        hash_func = getattr(hashlib, hash_type)()
        try:
            with open(file, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            hash_dict.update(
                {file: hash_func.hexdigest()})  # 将文件名和hash值放到字典里面 # print(hash_func.hexdigest()) # 当前文件的hash值
        except Exception as e:
            print(f"{file}计算hash报错: {e}")
    result = [[k for k, v in hash_dict.items() if v == value] for value in
              set(hash_dict.values())]  # 将字典中值相同的 他们的键放到字典里面
    aaa = []
    for result1 in result:
        if len(result1) > 1:
            aaa.append(result1)
    if len(aaa) == 0:
        print("[+] 当前批次文件大小重复的文件，hash不等，开始检测下一批文件大小的文件\n")
        return False
    else:
        return aaa

# 将文件名最短的从列表剔除
def check_file_name(file_path):
    # print("正在剔除文件名最短的文件...")
    file_tichu_list = []  # 剔除文件名最短的文件
    for a in file_path:
        filename = {}
        for file in a:
            file_name = os.path.basename(file)  # 去除路径获取文件名
            filename.update({file: file_name})
        min_key = min(filename, key=filename.get)  # 找到最小值的键
        data = {k: v for k, v in filename.items() if k != min_key}  # 剔除最小值的键值对
        keys = list(data.keys())  # 提取剩下的键值对的键 组成一个列表
        file_tichu_list.append(keys)  # 将剩下的键值对的键 组成一个列表
    return file_tichu_list

def main():
    timestart = time.time()
    print("[=] 开始检测重复文件，建议搭配everything试验后再使用\n[=] 数据无价，谨慎删除(默认不会删除文件，只会输出重复文件，需要把 # os.remove(j)  # 删除文件 这一行注释去掉才会删除文件)\n\n")
    folder_list = []
    for folder in args.folders:  # 遍历输入的参数也就是文件列表
        if check_file_or_folder(folder):
            folder_list.append(folder)
        else:
            continue
    if len(folder_list) == 0:
        print("[-] 请正确输入文件夹路径，例如：D:\\")
        return 0
    # print(folder_list)  # 输出当前文件夹列表
    file_list = []
    for folder in folder_list:  # 获取这些文件夹内的所有文件
        file_lists = read_files_in_directory(folder)
        for file in file_lists:
            file_list.append(file)
    # print(f"文件列表：{file_list}")  # 输出当前所有文件的列表
    num = 0
    print(f"[+] 开始对文件大小进行校验")
    for a in check_folder_duplicate_size(file_list):  # 遍历多层文件夹
        if len(a) > 1:
            print(f"[+] 文件大小相同的文件列表有：{a}\n[+] 开始进一步校验重复大小文件的hash")
            filequchong = check_file_hash(a)  # 输出hash相同的文件
            if not filequchong:
                continue
            print(f"[+] 检查完毕，hash相同的文件列表如下：{filequchong}")
            print(f"[+] 将保留文件名最短的文件，此文件列表其它重复项将开始删除")
            filezuizhong = check_file_name(filequchong)  # 剔除文件名最短的文件
            for i in filezuizhong:  # 遍历后删除里面的文件
                for j in i:
                    # os.remove(j)  # 删除文件
                    print(f"[+] 删除文件：{j}")
                    num += 1
            print("\n")
        else:
            continue
    timeend = time.time()
    timeh = timeend - timestart
    print(f"检查结束, 当前总计检测文件数：{len(file_list)}，共检测并删除重复文件{num}个，花费时间{timeh}秒")



main()
