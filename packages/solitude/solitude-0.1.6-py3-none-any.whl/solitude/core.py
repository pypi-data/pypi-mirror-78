from typing import Callable, Dict, List, Tuple
from types import ModuleType

import os
import json
import sys
import tqdm
import re
import logging
import datetime

from solitude import TOOL_NAME, hookspecs
from solitude.commands import CommandBase
import solitude.utils.ssh as ssh
import solitude.plugins.default
import solitude.plugins.csubmit
import solitude.plugins.interactive

from multiprocessing.pool import ThreadPool

import pluggy

from solitude.config import Config
from solitude.slurmjob import SlurmJob

logger = logging.getLogger(f"{TOOL_NAME}")


def resolve_cmd_files(cmd_files: List[str]) -> List[str]:
    commands = []
    for cmd_file in cmd_files:
        commands = commands + resolve_cmd_file(cmd_file=cmd_file)
    return commands


def resolve_cmd_file(cmd_file: str) -> List[str]:
    try:
        with open(cmd_file, "r") as f:
            data = f.readlines()
        return [
            d.strip()
            for d in data
            if len(d.strip()) > 0 and d.strip()[0] != "#"
        ]
    except FileNotFoundError:
        logger.error(
            f"ERROR: Could not find command file: {cmd_file}, skipping..."
        )
        return []


def shared_section(
    cmd_files: List[str], cache_file: str, cfg: Config
) -> Tuple[List[CommandBase], Dict, Tuple[str, str, str]]:
    logger.info(f"Starting at: {datetime.datetime.now()}")
    # load plugins
    plugin_manager = setup_plugins(plugins=cfg.plugins)
    logger.info(
        "Read {} command plugins".format(len(plugin_manager.get_plugins()))
    )
    # load cache file
    cache = read_cache(cache_file)
    logger.info(
        "Read {} cached links (command_hash -> (job_id, user, priority))".format(
            len(cache)
        )
    )
    # load command files
    cmds = resolve_cmd_files(cmd_files=cmd_files)
    cmds = read_commands(
        commands=cmds, cache=cache, plugin_manager=plugin_manager
    )
    # retrieve ssh credentials
    return cmds, cache, cfg.ssh


class SpecialFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(SpecialFormatter, self).__init__(*args, **kwargs)
        self._main_formatter = logging.Formatter(fmt="%(message)s")
        self._special_formatter = logging.Formatter(
            fmt="%(asctime)s [%(name)-10s] %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
        )

    def format(self, record):
        if record.name == TOOL_NAME:
            return self._main_formatter.format(record=record)
        else:
            return self._special_formatter.format(record=record)


def log_setup(log_level=logging.DEBUG):
    """setup some basic logging"""
    log = logging.getLogger("")
    log.setLevel(log_level)
    fmt = SpecialFormatter()
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(fmt)
    log.addHandler(ch)
    logging.getLogger("paramiko.transport").setLevel(logging.ERROR)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
    return logging.getLogger(TOOL_NAME)


def get_attr_from_module(pclass):
    pclass = pclass.rsplit(".", 1)
    mod = __import__(pclass[0], fromlist=[str(pclass[1])])
    return getattr(mod, pclass[1])


def parse_plugins(plugins: List[str]):
    results = []
    for plugin_name in plugins:
        if len(plugin_name.strip()) > 0:
            try:
                results.append(get_attr_from_module(plugin_name.strip()))
            except ModuleNotFoundError:
                logger.error(
                    f"!WARNING! Could not find plugin listed in config: {plugin_name}"
                )
    return results


def match_plugin(pm: pluggy.PluginManager, cmd: str) -> ModuleType:
    try:
        idx = pm.hook.matches_command(cmd=cmd).index(True)
    except ValueError:
        raise ValueError(
            "No plugin found for handling this type of command: {}".format(cmd)
        )
    return pm.hook.matches_command.get_hookimpls()[::-1][idx].plugin


def read_commands(
    commands: List[str], cache: Dict, plugin_manager: pluggy.PluginManager
) -> List[CommandBase]:
    return [
        CommandBase(
            cmd=x, plugin=match_plugin(pm=plugin_manager, cmd=x), cache=cache
        )
        for x in commands
    ]


def execute_commands(
    commands: List[CommandBase], map_fn: Callable, workers: int
):
    if workers > 0:
        tpex = ThreadPool(processes=workers)
        list(
            tqdm.tqdm(
                tpex.imap(map_fn, commands),
                total=len(commands),
                desc="Processing cmds ({} threads)".format(workers),
            )
        )
    else:
        for cmd in tqdm.tqdm(commands, desc="Processing cmds (no threads)"):
            map_fn(cmd)


def read_cache(file_name: str) -> Dict:
    if not os.path.exists(file_name):
        return {}
    with open(file_name, "r") as f:
        data = json.load(f)
    return data


def write_cache(file_name: str, data: Dict):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w") as f:
        json.dump(data, f)


def extend(cmd_files, jobids, workers, cfg, cache_file):
    _run_command_on_running_job(
        cmd_files,
        jobids,
        workers,
        cfg,
        cache_file,
        command="c-extend",
        action_str="EXTENDING",
    )


def stop(cmd_files, jobids, workers, cfg, cache_file):
    _run_command_on_running_job(
        cmd_files,
        jobids,
        workers,
        cfg,
        cache_file,
        command="c-stop",
        action_str="STOPPING",
    )


def link(cmd_files, jobid: int, slurm_jobid: int, cfg, cache_file) -> bool:
    commands, cache, _ = shared_section(
        cmd_files=cmd_files, cache_file=cache_file, cfg=cfg
    )
    cmd = commands[jobid - 1]
    # link jobid to slurm_jobid
    if SlurmJob.check_if_job_exists(jobid=slurm_jobid):
        job = SlurmJob(jobid=slurm_jobid)
        job.update()
        cache[cmd.hash] = job.to_dict()
        write_cache(file_name=cache_file, data=cache)
        return True
    return False


def unlink(cmd_files, jobid: int, cfg, cache_file) -> bool:
    commands, cache, _ = shared_section(
        cmd_files=cmd_files, cache_file=cache_file, cfg=cfg
    )
    cmd = commands[jobid - 1]
    if cmd.hash in cache:
        del cache[cmd.hash]
        write_cache(file_name=cache_file, data=cache)
        return True
    return False


def _run_command_on_running_job(
    cmd_files, jobids, workers, cfg, cache_file, command, action_str
):
    commands, _, credentials = shared_section(
        cmd_files=cmd_files, cache_file=cache_file, cfg=cfg
    )

    # update selected commands only (use workers)
    subcmds = [cmd for idx, cmd in enumerate(commands) if idx + 1 in jobids]

    def _update_cmd(cmd):
        cmd.update_job_info()

    execute_commands(subcmds, map_fn=_update_cmd, workers=workers)

    for idx, cmd in zip(jobids, subcmds):
        if cmd.is_running():
            logger.info(f"ATTEMPT {action_str} Job: {idx}")
            try:
                result = ssh.command_remote(
                    *credentials, f"./{command} {cmd.job_info.id}"
                )[0]
                logger.info("SSH RESULT: {}".format(result))
            except Exception as e:
                logger.warning("Failed with: {}".format(e))
        else:
            logger.info(f"Job {idx} is no longer running. Skipping...")
    logger.info(f"Finished at: {datetime.datetime.now()}")


def list_jobs(
    cmd_files, jobids, workers, cfg, cache_file, selected_only: bool = False
):
    commands, _, _ = shared_section(
        cmd_files=cmd_files, cache_file=cache_file, cfg=cfg
    )

    # update selected commands only (use workers)
    selected_ids = jobids
    if not selected_only:
        jobids = range(1, len(commands) + 1)
    subcmds = [
        cmd
        for idx, cmd in enumerate(commands)
        if (idx + 1 in jobids) or not selected_only
    ]

    def _update_cmd(cmd):
        cmd.update()

    execute_commands(subcmds, map_fn=_update_cmd, workers=workers)

    logger.info("======Commands======")
    logger.info(CommandBase.header_str())
    for idx, cmd in zip(jobids, subcmds):
        logger.info(f'{idx:2d}{"*" if idx in selected_ids else " "} {cmd}')
    logger.info(f"Finished at: {datetime.datetime.now()}")


def run(
    cmd_files,
    jobids,
    workers,
    user,
    priority,
    reservation,
    duration,
    ignore_errors,
    cfg,
    cache_file,
):
    commands, cache, credentials = shared_section(
        cmd_files=cmd_files, cache_file=cache_file, cfg=cfg
    )

    def _update_cmd(cmd):
        cmd.update_job_info()

    execute_commands(commands, map_fn=_update_cmd, workers=workers)

    high_priority_job_available = not any(
        [
            c.is_running() and c.job_info.priority == "high"
            for c in commands
            if c.has_job_link() and c.job_info.user == user
        ]
    )
    if high_priority_job_available:
        logger.info(f"No high priority job running for user {user}!")
    elif priority == "high":
        logger.info(
            f"No high priority job available for user {user}! Switching to low priority..."
        )
        priority = "low"

    # update selected commands only (use workers)
    subcmds = [cmd for idx, cmd in enumerate(commands) if idx + 1 in jobids]

    def _update_cmd(cmd):
        cmd.update_state()
        cmd.update_errors()

    execute_commands(subcmds, map_fn=_update_cmd, workers=workers)

    for idx, cmd in zip(jobids, subcmds):
        logger.info(f"ATTEMPT EXECUTE Job {idx}")
        if cmd.is_running():
            logger.info("Job is already running. skipping...")
            logger.info(str(cmd))
        elif cmd.is_finished():
            logger.info("Job has already finished. skipping...")
            logger.info(str(cmd))
        elif cmd.is_erroneous() and not ignore_errors:
            logger.info(
                "Job has halted with errors. Use --ignore-errors to run anyway. skipping..."
            )
            logger.info(str(cmd))
        else:
            try:
                # set correct priority level in command
                cmdstr = cmd.cmd
                if "c-submit " in cmdstr:
                    # remove any priority optional flags
                    cmdstr = re.sub(r"--priority=[a-zA-Z0-9]*\s", "", cmdstr)
                    # add desired priority flag after c-submit command
                    cmdstr = re.sub(
                        r"c-submit",
                        "c-submit --priority={}".format(priority),
                        cmdstr,
                    )
                    if duration is not None:
                        cmdstr = re.sub(
                            r"\s(\d+)\soni:11500",
                            " {} oni:11500".format(str(duration)),
                            cmdstr,
                        )
                    if reservation is not None:
                        cmdstr = re.sub(
                            r"c-submit",
                            "c-submit --reservation={}".format(reservation),
                            cmdstr,
                        )
                cmdstr = cmdstr.replace("{user}", user)

                # attempt schedule command
                result = ssh.command_remote(*credentials, cmdstr)[0]
                logger.info("SSH RESULT: {}".format(result))
                if "c-submit " in cmdstr:
                    link_id = int(result.strip().split(" ")[-1])
                    # can have only one high priority job so switch to low priority afterwards
                    cache[cmd.hash] = dict(
                        id=link_id, user=user, priority=priority
                    )
                    if priority == "high":
                        logger.info(
                            "Assigned a high priority job switching to low priority now"
                        )
                        priority = "low"
                    logger.info("http://oni:11080/show/{}".format(link_id))
                    logger.info("Writing job_link to cache...")
                    write_cache(cache_file, cache)
            except Exception as e:
                logger.warning("Failed with: {}".format(e))
    logger.info(f"Finished at: {datetime.datetime.now()}")


def setup_plugins(
    plugins: List[str], debug: bool = False
) -> pluggy.PluginManager:
    plugin_manager = pluggy.PluginManager(TOOL_NAME)
    plugin_manager.add_hookspecs(hookspecs)
    # Add default fallback plugins
    plugin_manager.register(solitude.plugins.default)
    plugin_manager.register(solitude.plugins.csubmit)
    plugin_manager.register(solitude.plugins.interactive)
    # Load externally packaged plugins
    plugin_manager.load_setuptools_entrypoints(group=TOOL_NAME)
    # Add additional plugins from cfg
    plugins = parse_plugins(plugins=plugins)
    for plugin in reversed(plugins):
        plugin_manager.register(plugin)
    # validate plugins (must strictly implement all plugin methods)
    plugin_manager.check_pending()
    for plugin in plugin_manager.get_plugins():
        validate_plugin(plugin)
    if debug:
        plugin_manager.trace.root.setwriter(print)
        plugin_manager.enable_tracing()
    return plugin_manager


def validate_plugin(plugin):
    required_fns = [
        e for e in dir(solitude.plugins.default) if "__" not in e and "_" in e
    ]
    for fn in required_fns:
        if not hasattr(plugin, fn):
            raise NotImplementedError(
                f"Plugin {plugin} has no hook_implementation for {fn}"
            )
