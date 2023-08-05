import hashlib
import logging

from solitude import TOOL_NAME
from solitude.slurmjob import SlurmJob


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


class CommandBase(object):
    def __init__(self, cmd, plugin, cache=None):
        self.logger = logging.getLogger(type(self).__name__)
        self._plugin = plugin
        self.cmd = cmd.strip()
        self.cache = cache
        self.hash = md5(
            self.get_plugin_short_name()
            + self._plugin.get_command_hash(self.cmd)
        )
        self.job_info = None
        self._set_basic_job_info_from_cache()
        self._state = {}
        self.errors = []

    def get_plugin_short_name(self):
        return self._plugin.__name__.rsplit(".", 2)[-1].replace(
            f"{TOOL_NAME}_", ""
        )

    def update(self):
        self.update_job_info()
        self.update_state()
        self.update_errors()

    def update_state(self):
        self._state = self._plugin.retrieve_state(self.cmd)

    def update_errors(self):
        self.errors = self._update_errors()

    def _set_basic_job_info_from_cache(self):
        self.job_info = None
        if self.cache is not None and self.hash in self.cache:
            entry = self.cache[self.hash]
            self.job_info = SlurmJob.from_dict(dic=entry)

    def update_job_info(self):
        if self.cache is not None and self.hash in self.cache:
            try:
                job_info = SlurmJob(jobid=self.cache[self.hash]["id"])
                job_info.update()
                self.job_info = job_info
            except ValueError:
                self.job_info = None
            except Exception as e:
                self.logger.warning(
                    "Job with id: {} has no job_info: {}".format(self.hash, e)
                )
                raise e

    def _update_errors(self):
        if (
            self.has_job_link()
            and not self.job_info.is_running()
            and not self.is_finished()
        ):
            try:
                joblog = self.job_info.get_log_text()
                errors = self._plugin.get_errors_from_log(log=joblog)
                return errors
            except Exception as e:
                self.logger.error(
                    f"Exception while fetching errors from log: {e}"
                )
        return []

    def has_job_link(self):
        return self.job_info is not None

    def get_job_status_str(self):
        status = "IDLE"
        if self.has_job_link() and self.job_info.is_pending():
            status = "PEND"
        elif self.has_job_link() and self.job_info.is_timeout():
            status = "TIME"
        elif self.is_running():
            status = "RUN"
        elif self.is_erroneous():
            status = "ERR!"
        elif self.is_finished():
            status = "."
        return status

    def __str__(self):
        self._errors = []
        url = self.job_info.get_log_url() if self.has_job_link() else "-"
        return "{status:4}{priority:2} {url:28} {plugin:10} {tag} {errors}".format(
            plugin=self.get_plugin_short_name(),
            tag=self.get_job_info_str(),
            status=self.get_job_status_str(),
            url=url,
            priority="H*"
            if self.is_running() and self.job_info.priority == "high"
            else "",
            errors=f'!!ERRORS: {" ".join(self.errors)}!!'
            if self.is_erroneous()
            else "",
        )

    @staticmethod
    def header_str():
        return (
            "id  {status:6} {url:28} {plugin:10} {info}".format(
                plugin="plugin",
                info="job_info",
                status="status",
                url="log_url",
            )
            + "\n"
            + "--  {status:6} {url:28} {plugin:10} {info}".format(
                plugin="------",
                info="--------",
                status="------",
                url="-------",
            )
        )

    def is_running(self):
        return self.has_job_link() and self.job_info.is_running()

    def is_finished(self):
        return self._plugin.is_command_job_done(
            cmd=self.cmd, state=self._state
        )

    def is_erroneous(self):
        return len(self.errors) > 0

    def get_job_info_str(self):
        return self._plugin.get_command_status_str(
            cmd=self.cmd, state=self._state
        )
