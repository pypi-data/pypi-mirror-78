# coding:utf-8
import gevent
import threading
import sys
if sys.version_info.major < 3:
    import Queue
    reload(sys)
    sys.setdefaultencoding("utf-8")
else:
    import queue as Queue
import time
from kombu import Connection
# from gevent.monkey import patch_all
from gevent.lock import BoundedSemaphore

# patch_all()


class InsertQueue(object):
    def __init__(self, host=None, port=None, virtual_host=None, heartbeat_interval=3, name=None, password=None,
                 logger=None, db_mincached=None, db_maxcached=None,
                 db_pool_maxconnections=None, db_info=None, maxIdle=20, maxActive=50, timeout=1,
                 disable_time=20, confirm=True, is_gevet=False):
        """
        :param db_mincached:
        :param db_maxcached:
        :param db_pool_maxconnections:db pool maxconnections
        :param db_info:eg:dict(
                    host='10.128.2.211',
                    port=8066,
                    user='root',
                    password='123',
                    database='dzqd',
                    buffered=True,
                    get_warnings=True,
                    raise_on_warnings=True
            )
        :param str host: Hostname or IP Address to connect to
        :param int port: TCP port to connect to
        :param str virtual_host: RabbitMQ virtual host to use
        :param int heartbeat_interval:  How often to send heartbeats
        :param str name: auth credentials name
        :param str password: auth credentials password
        """
        self.logger = logger
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.heartbeat_interval = heartbeat_interval
        self.name = name
        self.password = password
        self.mutex = threading.RLock()
        self.maxIdle = maxIdle
        self.maxActive = maxActive
        self.available = self.maxActive
        self.timeout = timeout
        self._queue = Queue.Queue(maxsize=self.maxIdle)
        self.disable_time = disable_time
        self.db_mincached = db_mincached
        self.db_maxcached = db_maxcached
        self.db_pool_maxconnections = db_pool_maxconnections
        self.db_info = db_info
        self.confirm = confirm
        self.is_gevet = is_gevet
        self.sem_lock = BoundedSemaphore(self.maxIdle)

    def get_new_connection_pipe(self):
        """
        产生新的队列连接
        :return:
        """

        with self.mutex:
            if self.available <= 0:
                raise GetConnectionException
            self.available -= 1
        try:

            conn = Connection(hostname=self.host,
                              port=self.port,
                              virtual_host=self.virtual_host,
                              heartbeat=self.heartbeat_interval,
                              userid=self.name,
                              password=self.password)
            producer = conn.Producer()

            return ConnectionPipe(conn, producer, self.logger)
        except:
            with self.mutex:
                self.available += 1
            raise GetConnectionException

    def get_connection_pipe(self):
        """
        获取连接
        :return:
        """
        try:
            connection_pipe = self._queue.get(False)
        except Queue.Empty:
            try:
                connection_pipe = self.get_new_connection_pipe()
            except GetConnectionException as ex:
                self.logger.exception(str(ex))
                timeout = self.timeout
                try:
                    connection_pipe = self._queue.get(timeout=timeout)
                except Queue.Empty as ex:
                    self.logger.exception(str(ex))
                    try:
                        connection_pipe = self.get_new_connection_pipe()
                    except GetConnectionException as ex:
                        self.logger.exception(str(ex))
        if (time.time() - connection_pipe.use_time) > self.disable_time:
            self.close(connection_pipe)
            return self.get_connection_pipe()
        return connection_pipe

    def close(self, connection_pipe):
        """
        close the connection and the correlative channel
        :param connection_pipe:
        :return:
        """
        with self.mutex:
            self.available += 1
            connection_pipe.close()
        return

    def insert_message(self, exchange=None, body=None, routing_key='', mandatory=True):
        """
        insert message to queue
        :param str exchange: exchange name
        :param str body: message
        :param str routing_key: routing key
        :param bool mandatory: is confirm: True means confirm, False means not confirm
        :return:
        """
        insert_result = True
        try:
            if not exchange:
                self.logger.warn('err exchange is None, body=%s', body)
                return False
            if self.is_gevet:
                gevent.spawn(self.sync_insert_message, exchange, body, routing_key, mandatory)
            else:
                insert_result = self.sync_insert_message(exchange, body, routing_key, mandatory)
        except Exception as ex:
            insert_result = False
            self.logger.exception(str(ex))
        return insert_result

    def sync_insert_message(self, exchange=None, body=None, routing_key='', mandatory=True):
        """
        insert message to queue
        :param str exchange: exchange name
        :param str body: message
        :param str routing_key: routing key
        :param bool mandatory: is confirm: True means confirm, False means not confirm
        :return:
        """
        put_into_queue_flag = True
        insert_result = False
        connection_pipe = None
        use_time = time.time()
        try:
            if self.is_gevet:
                with self.sem_lock:
                    connection_pipe = self.get_connection_pipe()
                    producer = connection_pipe.channel
                    producer.publish(exchange=exchange,
                                     body=body,
                                     delivery_mode=2,
                                     routing_key=routing_key,
                                     mandatory=mandatory
                                     )
            else:
                connection_pipe = self.get_connection_pipe()
                producer = connection_pipe.channel
                producer.publish(exchange=exchange,
                                 body=body,
                                 delivery_mode=2,
                                 routing_key=routing_key,
                                 mandatory=mandatory
                                 )
            insert_result = True
        except Exception as ex:
            insert_result = False
            put_into_queue_flag = False
            self.logger.exception(str(ex))
        finally:
            if put_into_queue_flag is True:
                try:
                    connection_pipe.use_time = use_time
                    self._queue.put_nowait(connection_pipe)
                except Queue.Full:
                    self.close(connection_pipe)
            else:
                if connection_pipe is not None:
                    self.close(connection_pipe)
        return insert_result


class ConnectionPipe(object):
    """
    connection和channel对象的封装
    """

    def __init__(self, connection, channel, logger):
        self.connection = connection
        self.channel = channel
        self.use_time = time.time()
        self.logger = logger

    def close(self):
        try:
            self.connection.close()
        except Exception as ex:
            self.logger.exception(str(ex))



class GetConnectionException():
    """
    获取连接异常
    """
    pass
