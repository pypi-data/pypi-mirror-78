import collections

import os
import copy
import re
import json
import pprint
from typing import Dict, List

import click

import solitude.core
from solitude.core import log_setup
from solitude.config import Config
from solitude import TOOL_NAME, __version__
from solitude.slurmjob import SlurmJob


def resolve_jobids(ctx, param, value) -> List[int]:
    # split values out on " " and ","
    substrs = [
        v3
        for v in value
        for v2 in v.strip().split(" ")
        for v3 in v2.strip().split(",")
    ]
    indices = []
    for entry in substrs:
        res = re.match(r"(\d+)(?=-(\d+))?", entry)
        if not res:
            click.echo(
                "Indices should be specified using numbers, "
                "ranges (a-b) or as a list of comma separated indices"
            )
            ctx.exit()
        grps = res.groups()
        if grps[1] is None:
            # parse number
            indices.append(int(grps[0]))
        else:
            # parse range
            a, b = int(grps[0]), int(grps[1])
            if a > b:
                click.echo(
                    "The second value (b) in a range should "
                    "be greater or equal to the first value (a) (b >= a)"
                )
                ctx.exit()
            indices = indices + [e for e in range(a, b + 1)]
    indices = [e for e in sorted(set(indices))]
    if not all(map(lambda x: x > 0, indices)):
        click.echo("Jobids should be greater than 0")
        ctx.exit()
    return indices


def is_config_valid() -> bool:
    cfg = Config()
    if not cfg.is_config_present():
        click.echo(
            "Configuration file could not be found. "
            "Generate one using `solitude config create`"
        )
        return False
    if not cfg.is_ssh_configured():
        click.echo(
            f"Configuration file was found at {cfg.config_path}. "
            f"However ssh was not properly configured. "
            "Generate new settings using `solitude config create`"
        )
        return False
    return True


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"{TOOL_NAME} {__version__}")
    ctx.exit()


class BaseGroup(click.core.Group):
    def __init__(self, name=None, commands=None, **kwargs):
        commands = commands or collections.OrderedDict()
        super().__init__(name, commands, **kwargs)
        self.params.insert(
            200,
            click.core.Option(
                param_decls=("-v", "--version"),
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=print_version,
                help="Show the version and exit.",
            ),
        )

    def list_commands(self, ctx):
        return self.commands


class BaseCommand(click.core.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            200,
            click.core.Option(
                param_decls=("-v", "--version"),
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=print_version,
                help="Show the version and exit.",
            ),
        )


class SharedCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            0,
            click.core.Option(
                param_decls=("-f", "--cmd-files"),
                multiple=True,
                required=True,
                type=str,
                default=Config().defaults.cmdfiles,
                help=f"File(s) containing a list of commands. Default: {Config().defaults.cmdfiles}",
            ),
        )
        self.params.insert(
            1,
            click.core.Option(
                param_decls=("-i", "--jobids"),
                multiple=True,
                type=str,
                callback=resolve_jobids,
                help="Select specific jobids. E.g.: 1-5,7,9",
            ),
        )
        self.params.insert(
            2,
            click.core.Option(
                param_decls=("-w", "--workers"),
                default=Config().defaults.workers,
                help=f"Workers to use for scheduling. Default: {Config().defaults.workers}",
            ),
        )


@click.group(
    cls=BaseGroup,
    help="A tool for running and managing commands on the DIAG SOL cluster",
)
def cli():
    pass


def are_jobids_specified(jobids: List):
    are_specified = len(jobids) > 0
    if not are_specified:
        click.echo(
            "This operation requires specification of jobids with -i or --jobids"
        )
    return are_specified


@click.command(cls=SharedCommand, help="Run jobs")
@click.option(
    "-u",
    "--user",
    default=Config().defaults.username,
    help="Run command job(s) for the given user.",
)
@click.option(
    "-p",
    "--priority",
    default=Config().defaults.priority,
    type=click.Choice(["idle", "low", "high"], case_sensitive=False),
    help="Run command job(s) with priority level (idle|low|high)",
)
@click.option(
    "-r",
    "--reservation",
    default=None,
    help="Run command job(s) for the given reservation.",
)
@click.option(
    "-d",
    "--duration",
    default=None,
    type=int,
    help="Run command job(s) for the given duration.",
)
@click.option(
    "-x",
    "--ignore-errors",
    default=False,
    flag_value=True,
    help="Run command job(s) despite reported errors.",
)
def run(
    cmd_files,
    jobids,
    workers,
    user,
    priority,
    reservation,
    duration,
    ignore_errors,
):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.run(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            user=user,
            priority=priority,
            reservation=reservation,
            duration=duration,
            ignore_errors=ignore_errors,
            cfg=Config(),
            cache_file=Config().cache_path,
        )


@click.command(cls=SharedCommand, help="Extend running jobs")
def extend(cmd_files, jobids, workers):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.extend(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            cfg=Config(),
            cache_file=Config().cache_path,
        )


@click.command(cls=SharedCommand, help="Stop running jobs")
def stop(cmd_files, jobids, workers):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.stop(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            cfg=Config(),
            cache_file=Config().cache_path,
        )


@click.command(cls=SharedCommand, help="Link jobs to existing slurm job")
@click.option(
    "-s",
    "--slurm-jobid",
    "slurm_jobid",
    required=True,
    type=int,
    help="Slurm job id to link the jobs to.",
)
def link(cmd_files, jobids, workers, slurm_jobid):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        if SlurmJob.check_if_job_exists(jobid=slurm_jobid):
            for jobid in jobids:
                success = solitude.core.link(
                    cmd_files=cmd_files,
                    jobid=jobid,
                    slurm_jobid=slurm_jobid,
                    cfg=Config(),
                    cache_file=Config().cache_path,
                )
                click.echo(
                    f"Linked job id {jobid} to slurm job: {slurm_jobid} {'succeeded' if success else 'failed'}"
                )
        else:
            click.echo(f"Slurm job id: {slurm_jobid} does not exists...")


@click.command(cls=SharedCommand, help="Unlink jobs from slurm job")
def unlink(cmd_files, jobids, workers):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        for jobid in jobids:
            success = solitude.core.unlink(
                cmd_files=cmd_files,
                jobid=jobid,
                cfg=Config(),
                cache_file=Config().cache_path,
            )
            if success:
                click.echo(f"Unlinked job id {jobid} from slurm jobs.")
            else:
                click.echo(
                    f"Job id {jobid} has no slurm job associated with it."
                )


@click.command(name="list", cls=SharedCommand, help="List jobs")
@click.option(
    "-s",
    "--selected-only",
    "selected_only",
    flag_value=True,
    default=False,
    help="Only display the jobs indicated by jobids. Default=No",
)
def list_jobs(cmd_files, jobids, workers, selected_only):
    if is_config_valid():
        solitude.core.list_jobs(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            selected_only=selected_only,
            cfg=Config(),
            cache_file=Config().cache_path,
        )


@click.group(cls=BaseGroup, help="Job operations")
def job():
    pass


@click.group(cls=BaseGroup, help="Configuration operations")
def config():
    pass


@click.command(cls=BaseCommand, help="Show status of the configuration")
def status():
    cfg = Config()
    is_config_valid()
    if cfg.is_config_present():
        click.echo(f"Configuration file found at: {cfg.config_path}")
        with open(cfg.config_path, "r") as f:
            cfg = json.load(f)
        display_configuration(cfg=cfg)


@click.command(cls=BaseCommand, help="Create or refresh the configuration")
@click.option(
    "--user",
    prompt="Default username for running jobs using SOL",
    type=str,
    required=True,
    help="Set default user to run jobs on SOL.",
)
@click.option(
    "--workers",
    type=int,
    default=8,
    help="Set default number of workers for issuing jobs on the server.",
)
@click.option(
    "--priority",
    type=click.Choice(["idle", "low", "high"]),
    default="low",
    help="Set default priority to run jobs with.",
)
@click.option(
    "--cmd-files",
    type=str,
    multiple=True,
    default=(),
    help="Set default command file(s) to use.",
)
@click.option(
    "--ssh-server",
    prompt="Default ssh DIAG deep learning server to use",
    type=str,
    required=True,
    help="Set default ssh DIAG deep learning server (dlc-machine.umcn.nl).",
)
@click.option(
    "--ssh-user",
    prompt="Default ssh username to use",
    type=str,
    required=True,
    help="Set default ssh username.",
)
@click.option(
    "--ssh-pass",
    prompt="Default ssh password to use",
    type=str,
    required=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Set default ssh password.",
)
@click.option(
    "-f",
    "--force",
    default=False,
    flag_value=True,
    help="Overwrite previous configuration file if it exists.",
)
def create(
    user, workers, priority, cmd_files, ssh_server, ssh_user, ssh_pass, force
):
    cfg = Config()
    if (
        not cfg.is_config_present()
        or force
        or click.confirm(
            f"There already is a configuration file at: {cfg.config_path}"
            f", Do you want to overwrite this file?",
            default=False,
        )
    ):
        cfgnew = {
            "defaults": {
                "username": user,
                "workers": workers,
                "priority": priority,
                "cmdfiles": list(cmd_files),
            },
            "ssh": {
                "server": ssh_server,
                "username": ssh_user,
                "password": ssh_pass,
            },
            "plugins": [],
        }
        click.echo(f"Writing configuration to: {cfg.config_path}")
        os.makedirs(os.path.dirname(cfg.config_path), exist_ok=True)
        with open(cfg.config_path, "w") as f:
            json.dump(cfgnew, f)
        display_configuration(cfg=cfgnew)


def display_configuration(cfg: Dict):
    """Display configuration, but obscure the ssh password"""
    cfgcopy = copy.deepcopy(cfg)
    if "ssh" in cfgcopy and "password" in cfgcopy["ssh"]:
        cfgcopy["ssh"]["password"] = "********"
    click.echo("Configuration dump:")
    pprint.pprint(cfgcopy)


job.add_command(list_jobs)
job.add_command(run)
job.add_command(extend)
job.add_command(stop)
job.add_command(link)
job.add_command(unlink)
cli.add_command(job)

config.add_command(status)
config.add_command(create)
cli.add_command(config)


def main():
    log_setup()
    cli()


if __name__ == "__main__":
    main()
