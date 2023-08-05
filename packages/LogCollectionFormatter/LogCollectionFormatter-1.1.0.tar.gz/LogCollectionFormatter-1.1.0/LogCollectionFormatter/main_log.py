# coding:utf-8
import json
import threading
import time
import types
import uuid
import datetime
from flask import request
from functools import wraps
from LogCollectionFormatter.base_log import BaseLog
from LogCollectionFormatter.insert_mq_tools import InsertQueue


def ret_to_str(ret):
    if isinstance(ret, types.StringType):
        ret = ret
    else:
        ret = ret.data
    return ret


def is_json(data_string):
    try:
        data = json.loads(data_string)
    except ValueError:
        return dict()
    return data


def get_headers_data(header_item):
    raw_data = dict()
    for key, value in header_item.items():
        raw_data[key] = value
    data = json.dumps(raw_data)
    return data


class MainLog(BaseLog):

    def __init__(self, app_name, prefix_path, t_code, f_code="", when="D", backup_count=3,
                 journal_log_enable=True, journal_mq_enable=True, host="", port=5673, virtual_host="",
                 heartbeat_interval=30, name="", password="", confirm=False, is_gevet=True,
                 mq_exchange_name='x.journal'):
        BaseLog.__init__(self, app_name, prefix_path, t_code, f_code, when=when, backup_count=backup_count,
                         journal_log_enable=journal_log_enable)
        self.journal_mq_enable = journal_mq_enable
        if self.journal_mq_enable:
            self.insert_log_queue = InsertQueue(host=host,
                                                port=port,
                                                virtual_host=virtual_host,
                                                heartbeat_interval=heartbeat_interval,
                                                name=name,
                                                password=password,
                                                confirm=confirm,
                                                is_gevet=is_gevet,
                                                logger=self)
            self.mq_exchange_name = mq_exchange_name
        else:
            self.insert_log_queue = None

    def with_internal_journallog(self, method_code=""):
        def log_decorated(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                """
                对参数数量不确定的函数进行装饰
                :param args:
                :param kwargs:
                :return:
                """
                if not self.journal_log_enable:
                    self.debug('write_Internal_journallog  is Closed.Below is Abort.')
                    return f(*args, **kwargs)
                channel, ret, str_ret = None, None, None
                begin_time = time.time()
                try:
                    request_time = datetime.datetime.now()
                    ret = f(*args, **kwargs)
                    end_time = time.time()
                    try:
                        total_time = str(int((end_time - begin_time) * 1000))
                        f_code = request.headers.get('User-Agent')
                        self.debug('with_internal_journallog() connection  after:%s', str(total_time))
                        # 接口前置流水日志处理
                        self.debug('%s Interface start,with param: %s', f.__name__, str(request.args))
                        action_code = f.__name__  # 接口操作码
                        request_url = request.url.encode('utf-8')
                        request_content = request.data
                        request_length = len(request_content)  # request正文长度
                        order_id, phone_num = getattr(request, 'order_id', None), getattr(request, 'phone_num',
                                                                                          None)
                        if request.method == "GET":
                            transaction_id = request.args.get("id", "") or request.args.get("htId", "")
                        elif request.method == "POST":
                            transaction_id = json.loads(request_content).get('id')
                        else:
                            transaction_id = str(uuid.uuid1()).replace("-", "")
                        # 接口后置流水日志处理
                        str_ret = ret_to_str(ret)
                        self.debug('The Interface %s return: %s' % (f.__name__, str_ret))
                        if str_ret:
                            if len(str_ret) > 3000:
                                if not isinstance(str_ret, unicode):
                                    str_ret = unicode(str_ret, 'utf-8')
                                str_ret = str_ret[:3000]
                        if request_length > 3000:
                            if not isinstance(request_content, unicode):
                                request_content = unicode(request_content, 'utf-8')
                            request_content = request_content[:3000]
                        response_content = str_ret
                        response_length = len(response_content)  # response正文长度
                        log_head_length = 80
                        flow = log_head_length + request_length + response_length
                        req_agent = request.headers.environ['HTTP_USER_AGENT']
                        response_time = datetime.datetime.now()
                        com_name = request.headers.environ['HTTP_HOST']  # + ":" + request.environ['']#主机名
                        message = {u'actionCode': action_code,
                                   u'requestTime': request_time.strftime("%Y-%m-%d %H:%M:%S"),
                                   u'responseTime': response_time.strftime("%Y-%m-%d %H:%M:%S"),
                                   u'requestContent': request_content,
                                   u'responseContent': response_content,
                                   u'requesturl': request_url,
                                   u'reqagent': req_agent,
                                   u'comName': com_name,
                                   u'flow': str(flow),
                                   u'order_id': order_id,
                                   u'phone_num': phone_num}
                        message_body = json.dumps(message, ensure_ascii=False)
                        self.debug('messagebody is %s' % message_body)
                        if self.insert_log_queue:
                            self.insert_log_queue.insert_message(exchange=self.mq_exchange_name,
                                                                 body=message_body,
                                                                 routing_key='internal',
                                                                 mandatory=False
                                                                 )
                        """加入日志平台对内流水日志"""
                        response_data = is_json(str_ret)
                        if response_data:
                            if str(response_data.get('code', "")) or str(response_data.get(u'code', "")):
                                response_code = str(response_data.get('code', "")) or str(response_data.get(u'code', ""))
                            elif response_data.get('head'):
                                response_code = str(response_data.get('head').get('code'))
                            elif response_data.get(u'head'):
                                response_code = str(response_data.get(u'head').get(u'code'))
                            else:
                                response_code = ""
                        else:
                            response_code = ""
                        self.external_log(dialog_type='in',
                                          transaction_id=transaction_id,
                                          request_url=request_url,
                                          http_method=request.method,
                                          request_time=request_time,
                                          request_headers=get_headers_data(request.headers),
                                          request_content=request_content,
                                          response_headers=get_headers_data(ret.headers),
                                          response_content=str_ret,
                                          response_time=response_time,
                                          response_code=response_code,
                                          http_status_code=ret.status_code,
                                          total_time=total_time,
                                          order_id=order_id,
                                          phone_num=phone_num,
                                          method_code=method_code if method_code else action_code,
                                          f_code=f_code
                                          )
                    except Exception as ex:
                        self.exception('Internal Journallog write log error, %s', str(ex))
                except Exception as ex:
                    self.exception(str(ex))
                    end_time = time.time()
                    self.exception('Internal Journallog write Exception! after:%s', str(end_time - begin_time))
                finally:
                    pass
                return ret
            return decorated_function
        return log_decorated




