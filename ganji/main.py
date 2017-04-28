#! -*-encoding:utf-8-*-

from get_all_links import get_all_links
from get_all_infomation import get_all_commodity_info

def start():
    print('欢迎使用本程序')
    print('输入a或A:获取所有二手商品的url链接')
    print('输入b或B,获取商品的详细信息')
    print('输入q或Q,退出程序')
    selection = input('请输入你的选择：')
    while True:
        if selection.lower() == 'a':
            # 获取所有二手商品详细信息
            get_all_links()
            print('保存完毕,请查看')
            input('按任意键退出程序')
            return None
        if selection.lower() == 'b':
            # 获取商品详细信息
            get_all_commodity_info()
            print('保存完毕,请查看')
            input('按任意键退出程序')
            return None
        if selection.lower() == 'q':
            # 退出程序
            print('谢谢使用')
            return None
        else:
            selection = input('请输入你的选择：')


if __name__ == '__main__':
    start()