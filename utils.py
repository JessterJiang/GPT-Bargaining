import sys
import time


#utils类：工具类，用于存放常用的工具函数
def wprint(s, fd=None, verbose=True):
    if(fd is not None): fd.write(s + '\n')
    if(verbose): print(s)
    return 

class Logger(object):
    def __init__(self, log_file, verbose=True):
        #设置为控制台输出
        self.terminal = sys.stdout
        #打开日志文件，设置状态为写入
        self.log = open(log_file, "w")
        #verbose是一种模式，代表详细输出
        self.verbose = verbose

        self.write("All outputs written to %s" % log_file)
        return 


    def write(self, message):
        self.log.write(message + '\n') # 里面的write与外面的write不同，恰好同名
        if(self.verbose): self.terminal.write(message + '\n')# 外面的write是对对象进行操作，里面的对属性进行操作

    def flush(self):
        pass #不执行任何操作，当作占位符，为了部分代码还没准备好但整体要正常运行的情况。

# def reverse_identity(agent_type):
#     assert agent_type in ["buyer", "seller", "moderator", "critic"]
#     if(agent_type == "buyer"): return "seller"
#     elif(agent_type == "seller"): return "buyer"
#     else: return agent_type


def check_price_range(price, p_min=8, p_max=20):
    """check if one price is in legal range
        检查给定的价格在合法范围中
    """
    if(price > p_min and price < p_max): return True
    else: return False

def check_k_price_range(prices, p_min=8, p_max=20):
    """check if all prices are in legal range
        检查所有人给出的价格都在合法范围中
    """
    all_in_range = True
    for p in prices:
        if(not check_price_range(p, p_min, p_max)): 
            all_in_range = False
            break
    return all_in_range


# parse：指的是对文本或数据进行解析
def parse_outputs(filepath, price_per_case=4):
    # 每个案列的价格数量为4
    prices = []
    lines = open(filepath).readlines()
    case_price = []
    for l in lines:
        if(l.startswith("==== CASE")):
            if(len(case_price) > 0): 
                assert(len(case_price) == price_per_case) #检测是不是四个一组
                prices.append(case_price)
            case_price = []
        elif(l.startswith("PRICE: ")):
            price = float(l.split('PRICE: ')[1].strip())
            case_price.append(price)
# PRICE后面没有CASE时，后面的自成一组
    if(len(case_price) > 0): 
        assert(len(case_price) == price_per_case)
        prices.append(case_price)
    return prices

# 与上面的代码功能基本相同，去掉了四个一组的限制，不太清楚price是怎么分析的
def parse_outputs_v2(filepath):
    prices = []
    lines = open(filepath).readlines()
    case_price = []
    for l in lines:
        if(l.startswith("==== ver")):
            if(len(case_price) > 0):
                prices.append(case_price)
            case_price = []
        elif(l.startswith("PRICE: ")):
            price = float(l.split('PRICE: ')[1].strip())
            case_price.append(price)

    if(len(case_price) > 0):
        prices.append(case_price)
    return prices


# 计算运行时间，得到分钟数
def compute_time(start_time):
    return (time.time() - start_time) / 60.0