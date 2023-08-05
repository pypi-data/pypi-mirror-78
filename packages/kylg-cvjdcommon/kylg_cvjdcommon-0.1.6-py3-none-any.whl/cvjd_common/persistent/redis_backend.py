import redis
from cvjd_common.models.cv_match import CvMatch
import jsonpickle
import logging
from cvjd_common.models.job import Job
from cvjd_common.persistent.persistent_base import PersistentBase


cv_predict_status_key = "cv_predict_status"


class RedisBackend(PersistentBase):

    def __init__(self, addr, port, user, passwd):
        logging.info("redis server %s:%s" % (addr, port))
        self.redis_server = redis.Redis(host=addr, port=port,
                                        password=user, username=passwd)

    def writeJobStatus(self, status: str, cvMatch: CvMatch):
        """
        :param status: doing or finished
        :param cvMatch: predict result
        :return:
        """
        job = Job(status, cvMatch)
        jsonDict = {cvMatch.cv.cv_id: jsonpickle.dumps(job)}
        self.redis_server.hmset(cv_predict_status_key, jsonDict)

    def readJobStatus(self, cvId: str):
        """
        :param cvId: cv id
        :return:  (status, CvMatch)
        """
        logging.info("get status for cv id: " + cvId)
        byteList = self.redis_server.hmget(cv_predict_status_key, cvId)
        if byteList is not None and len(byteList) > 0 and byteList[0] is not None:
            logging.info(str(byteList[0]))
            job = jsonpickle.decode(byteList[0])
            return job
        else:
            return None
