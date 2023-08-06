import errno
import json
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
import zmq
from framework.log_handler import DefaultLogHandler
from framework.utils_requests import get_page_json


class ActionFun:
    """
    用户自定义函数封装
    """
    typeName = ''  # 函数名
    fun = None  # 执行的函数
    threadId = None  # 执行线程

    def __init__(self):
        self.typeName = ''
        self.fun = None  # 执行的函数
        self.threadId = None  # 执行线程


class StrategiesManager:
    remote_history_url = 'http://{}/gethistory?code={}&startTime={}&endTime={}&ktype={}'
    threads = {}
    finished = False
    action = []
    tempDir = './temp'
    prepareActionQueue = Queue()
    getAllQuote = False

    def __init__(self, configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=True):
        """
        初始化

        配置文件格式：
        {
            "remote_history_url": "127.0.0.1:10039",
            "kl_real_time_addr_in": "tcp://127.0.0.1:10019",
            "kl_real_time_addr_out": "tcp://127.0.0.1:10020"
        }
        :param configPath: 配置文件路径，默认./sconfig.conf
        :param tempPath: 数据缓存文件夹路径，默认./temp
        :param isShowQuoteMsg: 是否输出行情数据，默认True
        """
        self.logHandler = DefaultLogHandler(filename='strategies.log')
        self.logHandler.info('************** 策略管理器初始化 ***************')
        self.config = self.file2dict(configPath)
        self.url_ip = self.config['remote_history_url']
        self.kl_real_time_addr_in = self.config['kl_real_time_addr_in']
        self.kl_real_time_addr_out = self.config['kl_real_time_addr_out']
        self.tempDir = tempPath
        self.isShowQuoteMsg = isShowQuoteMsg

    def __del__(self):
        self.finished = True
        for k in self.threads.keys():
            self.threads[k].join()
        self.threads.clear()

    def file2dict(self, path):
        """
        从文件读取配置信息转字典
        :param path: 配置文件路径
        :return:
        """
        # 读取配置文件
        with open(path) as f:
            return json.load(f)

    def registAction(self, fun):
        """
        注册回调方法
        :param fun:
        :return:
        """
        af = ActionFun()
        af.typeName = fun.__name__
        af.fun = fun
        self.action.append(af)

    def getHistory(self, stock_code, startTime='', endTime='', ktype='') -> dict:
        """
        获取合约历史数据
        :param stock_code:
        :param startTime:
        :param endTime:
        :param ktype:
        :return:
        """
        url = self.remote_history_url.format(self.url_ip, stock_code, startTime, endTime, ktype)
        rsp = get_page_json(url)
        return rsp

    def _doAction(self, stock_code, startTime='', endTime='', ktype=''):
        self.logHandler.info(f'开启任务 ---> \n历史回测 {stock_code}合约 从{startTime}到{endTime} {ktype} 数据')
        start = startTime.replace('-', '')
        end = endTime.replace('-', '')
        #
        import os
        if not os.path.exists(self.tempDir):
            os.makedirs(self.tempDir)
        #
        filePath = f'{self.tempDir}/{stock_code}-{start}-{end}-{ktype}.dat'
        data_list = None
        if os.path.exists(filePath):
            data_list = self.file2dict(filePath)
        #
        if data_list is None:
            url = self.remote_history_url.format(self.url_ip, stock_code, startTime, endTime, ktype)
            rsp = get_page_json(url)
            data_list = rsp['data']
            if len(data_list) == 0:
                self.logHandler.error(f'从网络获取历史数据返回为空,历史回测 {stock_code}合约 从{startTime}到{endTime} {ktype} 数据')
                return
            # 缓存到本地
            with open(filePath, 'w') as file:
                bJson = json.dumps(data_list, ensure_ascii=False)  # dict转json
                file.writelines(bJson)

        for item in data_list:
            for act in self.action:
                act(item)
        self.logHandler.info('完成任务 --->')
        key = stock_code + startTime + endTime + ktype
        self.threads.pop(key)

    def select_pan_type(self, code: str) -> str:
        """
        判断内外盘
        :param code:NYMEX_F_CL_2007
        :return:
        """
        contratelist = str(code).split('_')
        if contratelist[0].upper() in ['SHFE', 'CFFEX', 'DCE', 'CZCE']:
            return 'in'  # 内盘
        else:
            return 'out'  # 外盘

    def _connect_zmq(self, stock_code, ktype):
        try:
            quote_ctx = zmq.Context()
            client = quote_ctx.socket(zmq.SUB)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL, 500)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL_MAX, 5000)

            pan_type = self.select_pan_type(stock_code)
            # 请求历史数据
            if pan_type == 'in':
                client.connect(self.kl_real_time_addr_in)
            elif pan_type == 'out':
                client.connect(self.kl_real_time_addr_out)
            else:
                self.logHandler.info("无法判断内外盘")
                return None

            client.setsockopt_string(zmq.SUBSCRIBE, ktype)
            client.setsockopt(zmq.RCVTIMEO, 10000)
            # client.setsockopt_string(zmq.SUBSCRIBE, '3Min')
            # client.setsockopt_string(zmq.SUBSCRIBE, '5Min')
            # client.setsockopt_string(zmq.SUBSCRIBE, '15Min')
            # client.setsockopt_string(zmq.SUBSCRIBE, '30Min')
            # client.setsockopt_string(zmq.SUBSCRIBE, '60Min')
            # client.setsockopt_string(zmq.SUBSCRIBE, 'klDay')
            # client.setsockopt_string(zmq.SUBSCRIBE, 'qt')
            # client.setsockopt_string(zmq.SUBSCRIBE, 'ba')
            # client.setsockopt_string(zmq.SUBSCRIBE, 'ticket')

            return client
        except zmq.error.ZMQError as e:
            self.logHandler.error("zmq 连接出错:%s" % e)
            return None

    def _doRealTimeAction(self, stock_code, ktype):
        self.logHandler.info(f'开启任务 ---> \n实时模拟 {stock_code}合约 {ktype} 数据')
        client = self._connect_zmq(stock_code, ktype)

        for action in self.action:
            self.prepareActionQueue.put(action)

        while not self.finished:
            try:
                if client is not None:
                    response = client.recv()
                else:
                    self.logHandler.error(f'zmq尝试重连......')
                    client = self._connect_zmq(stock_code, ktype)
                    continue
            except zmq.ZMQError as e:
                self.logHandler.error(f'zmq {e.args}')

                client.close()
                self.logHandler.error(f'zmq尝试重连......')
                client = self._connect_zmq(stock_code, ktype)
                continue

            response = str(response, encoding='GB2312')
            if response != ktype:
                if self.isShowQuoteMsg:
                    self.logHandler.info("response:     {}".format(response))
                code = str(stock_code).split('_')
                temp = response[:20].split(',')
                if self.getAllQuote \
                        or (code[0] == temp[0] and code[1] == temp[1] and code[2] == temp[2] and code[3] == temp[3]):
                    size = self.prepareActionQueue.qsize()
                    while size != 0:
                        size -= 1
                        if not self.prepareActionQueue.empty():
                            try:
                                doact = self.prepareActionQueue.get(block=False)
                                if doact is not None:
                                    handle_thread = Thread(target=self._wraperFun, name=doact.typeName,
                                                           args=(doact, response))
                                    doact.threadId = handle_thread
                                    handle_thread.start()
                            except Empty as e:
                                self.logHandler.error(f'队列为空:{e.args}')
                                # act(response)
        client.close()
        self.logHandler.info('完成任务 --->')
        key = stock_code + ktype
        self.threads.pop(key)

    def _wraperFun(self, doactfun, data):
        if isinstance(doactfun, ActionFun):
            try:
                doactfun.fun(data)
            except Exception as e:
                self.logHandler.error(f'执行任务<{doactfun.typeName}>发生异常：{e.args}')
            doactfun.threadId = None
            self.prepareActionQueue.put(doactfun)

    def runRealTime(self, stock_code, ktype='1Min', getAllQuote=False):
        """
        运行实时数据模拟
        :param stock_code:例如：COMEX_F_GC_2012
        :param ktype: k线类型，默认1Min，例如：1Min
        :param getAllQuote:是否获取所有合约行情
        :return:
        """
        if stock_code == "":
            self.logHandler.error('合约信息为空，请输入合约代码')
            return
        self.getAllQuote = getAllQuote
        _watch_thread = Thread(target=self._doRealTimeAction, args=[stock_code, ktype], name="runRealTime")
        key = stock_code + ktype
        if self.threads.get(key) is None:
            self.threads[key] = _watch_thread
            _watch_thread.start()
        else:
            self.logHandler.info('任务已存在 --->')

    def runHistory(self, stock_code, startTime='', endTime='', ktype='1Min'):
        """
        运行历史回测
        :param stock_code:
        :param startTime:
        :param endTime:
        :param ktype:
        :return:
        """
        _watch_thread = Thread(target=self._doAction, args=[stock_code, startTime, endTime, ktype], name="runHistory")
        key = stock_code + startTime + endTime + ktype
        if self.threads.get(key) is None:
            self.threads[key] = _watch_thread
            _watch_thread.start()
        else:
            self.logHandler.info('任务已存在 --->')
