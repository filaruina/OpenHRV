import redis
import numpy as np
from config import REDIS_HOST, REDIS_PORT
from PySide2.QtCore import QObject


class RedisLogger(QObject):

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.redis = redis.Redis(REDIS_HOST, REDIS_PORT)    # connection to server is not established at instantiation, but once first command to server is issued (i.e., first publish() call)

        self.model.ibis_buffer_update.connect(self.publish)
        self.model.mean_hrv_update.connect(self.publish)
        self.model.mac_addresses_update.connect(self.publish)
        self.model.pacer_rate_update.connect(self.publish)
        self.model.hrv_target_update.connect(self.publish)
        self.model.biofeedback_update.connect(self.publish)

    def publish(self, value):
        key, val = value
        if isinstance(val, (list, np.ndarray)):
            val = val[-1]
        if isinstance(val, np.int32):
            val = int(val)
        try:
            self.redis.publish(key, val)
        except redis.exceptions.ConnectionError as e:
            print(e)    # client (re)-connects automatically; as soon as server is back up (in case of previous outage) client-server communication resumes

    def record():
        pass


    def set_marker():
        pass
