导入 math 称作 数学


打印('''
测试多行数据，
''这是一个测试''
"用来测试多行数据"
''', "成功!")


类 测试用类:
    定义 初始化(自己, 名字):
        自己的高度 = 0
        自己的名字 = 名字
    
    定义 打印名字(自己):
        打印(自己的名字)
    
    定义 自增高度(自己):
        自己的高度 += 1
        自己.检查()
    
    定义 检查(自己):
        如果 自己的高度 等于 3:
            打印("超高了!")


定义 自增(数字):
    返回 数字 + 1

定义 测试用函数(参数1, 参数2, 参数3):
    甲 = 0
    当甲 小于等于 3:
        参数1 = 自增(参数1)
        甲 = 甲 + 1
    返回 数学.sqrt(参数1) + 数学.sqrt(参数2) + \
        数学.sqrt(参数3)


定义 主函数():
    实例 = 测试用类("测试用名字")
    打印(实例的名字)
    对于 甲 属于 区间(0, 5):
        实例.自增高度()
    打印(测试用函数(1, 2, 3))


如果 __name__ 等于 "__main__":
    #这是一个测试用注释
    主函数()
    幸运数字 = [7, 6, 5, 4, 3, 2, 1]
    不幸数字 = [10, 20, 30]
    对于 甲 属于 区间(0, 5):
        输入数据 = 整数(输入("这是一个测试,请输入数字:\n"))
        如果 输入数据 属于 幸运数字:
            打印("你输入了幸运数字%s!" % 输入数据)
        又如果 输入数据 属于 不幸数字:
            打印("你输入了不幸数字%d!" % 输入数据)
        否则:
            打印("你好,\
                世界" + " " + 字符串(输入数据))
