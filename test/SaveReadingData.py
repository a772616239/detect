import shelve
import dbm.dumb
import os

def save_data(data, filename):
    """将数据保存到指定文件，使用dbm.dumb模块确保兼容性"""
    if not filename:
        raise ValueError("保存文件名不能为空！")
    
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    print(f"save_data {data}")
    # 显式使用dbm.dumb模块创建数据库
    with shelve.Shelf(dbm.dumb.open(filename, 'c')) as db:
        db['data'] = data

def load_data(filename):
    """从指定文件加载数据，检查dbm.dumb生成的文件是否存在"""
    # 检查dbm.dumb生成的标志文件之一是否存在
    if not os.path.exists(filename + '.dat') and not (os.path.exists(filename + '.dir')):
        print(f"文件 {filename} 不存在!")
        return 0
    
    try:
        with shelve.Shelf(dbm.dumb.open(filename, 'r')) as db:
            return db.get('data', 0)
    except dbm.error:
        return 0

# 示例使用
number = 1
filename = 'data/number_shelve'  # 注意不要添加文件扩展名

# 保存数据
# save_data(number, filename)

# 加载数据
loaded_number = load_data(filename)
print(loaded_number)  # 输出: 42