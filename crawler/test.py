import os


def get_name(filepath):
    file_name = list()
    for t in os.listdir(filepath):
        data_collect = ''.join(t)
        file_name.append(data_collect)
    return file_name


if __name__ == '__main__':
    excel_path = r"G:\\Dataset\\fnbak\\利好\\"  # 路径，把excel放进文件夹下
    f_name = get_name(excel_path)
    for name in f_name:  # 循环
        path = excel_path + name  # name就是文件的文件名，path是拼好的绝对路径
        print(path)  # 然后在这写需要怎么操作
