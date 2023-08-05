from datetime import datetime
from os import listdir
from os.path import isfile, join
import jsonpickle
from cvjd_common.models.cv_match import CvMatch
from cvjd_common.persistent.persistent_base import PersistentBase


result_file_name_prefix = "bestjd_"

RESULT_SPLITTER = "================i am splitter==============="


class FileBackend(PersistentBase):

    def __init__(self, job_dir):
        self.job_dir = job_dir

    def writeJobStatus(self, status: str, cvMatch: CvMatch):
        """
        write job status to text file if job is finished
        :param cvMatch:
        :param status: str, doing or finished
        :param result: [(job id, job type, job description, skill list, gap list), (job id, job type, job description, skill list, gap list)]
        :return:
        """
        if "finished" != status:
            return

        nowStr = datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = '%s%s_%s' % (result_file_name_prefix, cvMatch.cv.cv_id, nowStr)
        filePath = '%s/%s' % (self.job_dir, fileName)
        f = open(filePath, "w+", encoding='utf-8')
        # write cv content
        json_dict = {"cvMatch": cvMatch, "status": status}
        j = jsonpickle.encode(json_dict)
        f.write(j)
        f.flush()
        f.close()

    def readJobStatus(self, cvId: str):
        """
        read job status from text file
        :param cvId: str, cv id
        :return: (status, CvMatch)
        """
        fileName = '%s%s' % (result_file_name_prefix, cvId)
        only_files = [f for f in listdir(self.job_dir) if
                      isfile(join(self.job_dir, f)) and f.startswith(fileName)]
        if len(only_files) == 0:
            return None, None
        only_files.sort()
        targetFile = only_files[-1]
        f = open("%s/%s" % (self.job_dir, targetFile), "r", encoding='utf-8')
        job = jsonpickle.decode(f.read())
        return job['status'], job['cvMatch']
