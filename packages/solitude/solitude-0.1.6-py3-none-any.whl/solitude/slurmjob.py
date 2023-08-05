import requests
import logging

DEFAULT_HOST = "http://oni:11080/"
logger = logging.getLogger("SlurmJob")


class SlurmJob(object):
    def __init__(self, jobid: int, user: str = None, priority: str = None):
        self.id = jobid
        self.user = user
        self.priority = priority
        self._status = None

    def update(self):
        info = requests.get(
            "{}json/jobinfo/{}".format(DEFAULT_HOST, self.id)
        ).json()
        self.id = info["jobid"]
        self.user = info["user"]
        self.priority = info["priority"]
        self._status = info["status"]

    def is_running(self):
        return self._status in ("RUNNING", "PENDING")

    def is_pending(self):
        return self._status == "PENDING"

    def is_timeout(self):
        return self._status == "TIMEOUT"

    def get_log_text(self):
        return requests.get(
            "{}text/log/{}".format(DEFAULT_HOST, self.id),
            allow_redirects=True,
        ).text

    def get_log_url(self):
        return "{}show/{}".format(DEFAULT_HOST, self.id)

    def to_dict(self):
        return dict(id=self.id, user=self.user, priority=self.priority)

    @staticmethod
    def check_if_job_exists(jobid):
        txt = requests.get(
            "{}json/jobinfo/{}".format(DEFAULT_HOST, jobid)
        ).text
        return "does not exist" not in txt

    @staticmethod
    def from_dict(dic):
        return SlurmJob(
            jobid=dic["id"], user=dic["user"], priority=dic["priority"]
        )
