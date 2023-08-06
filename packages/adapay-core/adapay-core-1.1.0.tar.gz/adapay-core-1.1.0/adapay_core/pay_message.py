import json
import threading
import uuid

from paho.mqtt import client as mqtt

from adapay_core.log_util import log_info, log_error


class AdapayMessage:

    def __init__(self, api_key, token):
        self.api_key = api_key
        # 建立连接请求标识
        self.token = token

        # MQTT GroupID,创建实例后从 MQTT 控制台创建
        self.group_id = 'GID_CRHS_ASYN'
        # MQTT ClientID，由 GroupID 和后缀组成，需要保证全局唯一
        self.client_id = self.group_id + '@@@' + str(hash(api_key + (str(uuid.uuid1()))))
        # Topic， 其中第一级父级 Topic 需要从控制台创建
        self.topic = 'topic_crhs_sender/' + api_key

        # 实例 ID，购买后从产品控制台获取
        self.instance_id = 'post-cn-0pp18zowf0m'
        # 账号AccessKey 从阿里云账号控制台获取
        self.access_key = 'LTAIOP5RkeiuXieW'
        # MQTT 接入点域名，实例初始化之后从控制台获取
        self.broker_url = 'post-cn-0pp18zowf0m.mqtt.aliyuncs.com'

        # self.instance_id = 'post-cn-459180sgc02'
        # self.access_key = 'LTAILQZEm73RcxhY'
        # self.broker_url = 'post-cn-459180sgc02.mqtt.aliyuncs.com'

        # 长连接建立结果回调方法
        self.connect_callback = None
        # 建立监听成功回调
        self.subscribe_callback = None
        # 收到消息回调方法
        self.received_callback = None

    def set_connect_callback(self, connect_callback):
        self.connect_callback = connect_callback

    def set_subscribe_callback(self, subscribe_callback):
        self.subscribe_callback = subscribe_callback

    def set_received_callback(self, received_callback):
        self.received_callback = received_callback

    def subscribe(self):
        pay_msg_thread = threading.Thread(target=self._execute)
        pay_msg_thread.start()

    def _on_connect(self, client, userdata, flags, resp_code):
        """
        建立长连接成功回调
        """
        log_info('connected with result code ' + str(resp_code))

        # 如果这里返回非0，表示长连接成功但是代码有异常
        if self.connect_callback is not None:
            self.connect_callback(resp_code)

        if resp_code == 0:
            client.subscribe(self.topic, 0)

    def _on_disconnect(self, client, userdata, resp_code):
        """
        :param resp_code:
         长连接链接失败回调
        1	伪造 Token，不可解析
        2	Token 已经过期
        3	Token 已经被吊销
        4	资源和 Token 不匹配
        5	权限类型和 Token 不匹配
        8	签名不合法
        -1	帐号权限不合法

        :return:
        """
        log_info('unexpected disconnection %s' % resp_code)

        if self.connect_callback is not None:
            self.connect_callback(resp_code)

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """
        订阅成功回调
        """
        log_info('on_subscribe')
        if self.subscribe_callback is not None:
            self.subscribe_callback(0)

    def _on_unsubscribe(self, client, userdata, mid):
        """
        订阅成功回调
        """
        log_info('on_unsubscribe')
        if self.subscribe_callback is not None:
            self.subscribe_callback(-1)

    def _on_message(self, client, userdata, messages):
        """
        接收到交易结果回调
        """
        message_str = messages.payload.decode('utf-8')
        log_info('on_msg_receive:' + message_str)

        if self.received_callback is not None:
            try:
                msg_dict = json.loads(message_str)
                self.received_callback(msg_dict, self.topic)
            except Exception as e:
                log_error(str(e))
                log_error('pay message loads error:' + message_str)

    def _execute(self):
        # 初始化的时候获取 client
        client = mqtt.Client(self.client_id, protocol=mqtt.MQTTv311, clean_session=True)

        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_subscribe = self._on_subscribe
        client.on_unsubscribe = self._on_unsubscribe
        client.on_message = self._on_message

        # 签名模式下的设置方法，参考文档
        # https://help.aliyun.com/document_detail/48271.html?spm=a2c4g.11186623.6.553.217831c3BSFry7
        user_name = 'Token|' + self.access_key + '|' + self.instance_id
        password = 'R|' + self.token
        client.username_pw_set(user_name, password)
        client.connect(self.broker_url, 1883, 60)
        client.loop_forever()
