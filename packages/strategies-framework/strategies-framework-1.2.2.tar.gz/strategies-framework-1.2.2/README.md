**StrategiesManager**

# 这是一个策略回测库，支持内外盘期货历史回测跟实时回测两种模式

# 例子：
```python
import time
from framework.strategies_manager import StrategiesManager

# 自定义操作函数
from utils_redis import RedisUtils

ri = RedisUtils('./redis.conf')
ri.lookup_redist_info()


def myAction2(data):
    print(f'_______> {data}')
    # time.sleep(2)


def myAction(data):
    """
    自定义操作
    :param data: 行情数据，字典类型
    {'time_key': '2020-07-21 14:53:00', 'open': 4659.2, 'high': 4659.8, 'low': 4657.4, 'close': 4658.8, 'volume': 326.0, 'code': 'CFFEX.IF2008', 'pe_ratio': 0, 'turnover_rate': 0, 'turnover': 0, 'last_close': 4659.2, 'change_rate': -0.0085851648}
    :return:
    """
    print(f'&&&&&&> {data}')
    # rsp = manager.getHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-08-17', endTime='2020-08-17', ktype='1Min')
    # print(rsp)
    time.sleep(5)


def myAction3(data):
    print(f'*********> {data}')
    global ri
    ri.set_key_value('test1', 1)
    ri.push_list_value('test2', data)


# 创建实例，参数可以不传
manager = StrategiesManager(configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=True)

# 注册自定义函数
manager.registAction(myAction)
manager.registAction(myAction2)
manager.registAction(myAction3)

# 实时数据使用，支持内外盘合约
manager.runRealTime(stock_code='COMEX_F_GC_2012', ktype='1Min', getAllQuote=True)
# 历史数据回测使用，支持内外盘合约
# manager.runHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')

# manager.runRealTime(stock_code='CFFEX_F_IF_2008', ktype='1Min')
# manager.runHistory(stock_code='CFFEX_F_IF_2008', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')

```

# 注意：实时模拟跟历史回测返回的数据格式不一样

# 更新日志
- 2020.08.26
    1) 支持zmq断线重连
    2) 添加自定义函数异常捕捉
    
- 2020.08.21
    1) 修改执行自定义方法为异步
    2) 修改实时数据订阅合约过滤

- 2020.08.20
    1) 历史回测数据缓存本地

- 2020.08.17
    1) 策略框架构建
    2) 添加获取历史记录接口