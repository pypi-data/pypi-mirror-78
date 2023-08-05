# Solitude

[![PyPI version](https://badge.fury.io/py/solitude.svg)](https://badge.fury.io/py/solitude) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple light-weight command line tool for managing jobs on the SOL cluster

### Features

* Querying status of a specified list of slurm jobs and presenting them in a nice list overview
* Tools to manage the specified jobs (starting/stopping/extending)
* Cross platform due to using ssh (paramiko) for querying and issuing commands
* Extendable and customizable through pluggy plugins

### Setup and configuration

1) Install trough pip using: `$ pip install solitude`
2) Configure the tool through: `$ solitude config create` and fill out the prompts.
3) Previous step should have generated a configuration file at the proper location (installation directory or the user's home directory). It should contain a target cluster machine and the login credentials, which will be used to query and issue commands. It's contents and whereabouts can be queried using `solitude config status` and should contain something like:
```json
{
    "defaults": {
        "user": "username",
        "workers": 8
    }, 
    "ssh":{
        "server" : "dlc-machine.umcn.nl",
        "username" : "user",
        "password" : "*******"
    },
    "plugins":[    
    ]
}
```
Now the tool is ready for usage. See below for examples...

### Example usage

Create a file for your deep learning project with a list of jobs (here we call this `commands.sol`) using the following format:
```text
# Test jobs 
# (commented lines and empty lines will be ignored)

./c-submit --require-mem=1g --require-cpus=1 --gpu-count=0 {user} test 1 hello-world
./c-submit --require-mem=1g --require-cpus=1 --gpu-count=0 {user} test 1 ubuntu /usr/bin/sleep 500
./c-submit --require-mem=1g --require-cpus=1 --gpu-count=0 {user} test 1 ubuntu /usr/bin/echo "CUDA_ERROR"

```

This format supports the special tag `{user}` which will be substituted with the default user name.

After creating this use the following command to list the commands:

`$ solitude job list -f /path/to/commands.sol`

Running specific jobs can be achieved with:

`$ solitude job run -f /path/to/commands.sol -i 1-3 --priority=high`

For stopping and extending running jobs you can use `solitude job stop` and `solitude job extend` commands respectively.

### Plugins

The supported commands can be tweaked and extended by writing custom `pluggy` plugins. 
This can change the way commands are being treated, which information is retrieved etc. 
The pluggy documentation has some excellent detailed documentation on how to create and package your own plugins: https://pluggy.readthedocs.io/en/latest/

Here is a brief extract on how to do this for solitude. 

First make a separate project folder and create the following files:  

`solitude-exampleplugin/solitude_exampleplugin.py`

```python
import solitude
from typing import Dict, List


@solitude.hookimpl
def matches_command(cmd: str) -> bool:
    """Should this command be processed by this plugin?

    :param cmd: the command to test
    :return: True if command matches False otherwise
    """    
    return "custom_command" in cmd


@solitude.hookimpl
def get_command_hash(cmd: str) -> str:
    """Computes the hash for the command
    This is used to uniquely link job status to commands.
    So if the exact same command is found they both link to the same job.
    Therefore it is recommended to remove parts from cmd that do not change
    the final results for the job.
    If you are uncertain what to do just return `cmd` as hash

    :param cmd: the command to compute the hash for
    :return: the command hash
    """
    return cmd


@solitude.hookimpl
def retrieve_state(cmd: str) -> Dict:
    """Retrieve state for the job which can be set in a dictionary

    :param cmd: the command to test
    :return: a dictionary with the retrieved state (used in other calls)
    """
    return {}


@solitude.hookimpl
def is_command_job_done(cmd: str, state: Dict) -> bool:
    """Checks if the command has finished

    :param cmd: the command to test
    :param state: the retrieved state dictionary for this job
    :return: True if job is done False otherwise
    """
    return False


@solitude.hookimpl
def get_command_status_str(cmd: str, state: Dict) -> str:
    """Retrieve state for the job which can be set in a dictionary

    :param cmd: the command to test
    :param state: the retrieved state dictionary for this job
    :return: a string containing job information and progress status
    """
    return cmd


@solitude.hookimpl
def get_errors_from_log(log: str) -> List[str]:
    """Checks the log for errors

    :param log: the log string to parse
    :return: A list of error messages, empty list if no errors were found
    """
    errors = []
    return errors

```

`solitude-exampleplugin/setup.py`

```python
from setuptools import setup

setup(
    name="solitude-exampleplugin",
    install_requires="solitude",
    entry_points={"solitude": ["exampleplugin = solitude_exampleplugin"]},
    py_modules=["solitude_exampleplugin"],
)
```

Now let's install the plugin and test it:

```
$ pip install --editable solitude-exampleplugin
$ solitude job list -f your_test_commands.sol 
```

### Contributing

Fork the solitude repository

Setup your forked repository locally as an editable installation:

```
$ cd ~
$ git clone https://github.com/yourproject/solitude
$ pip install --editable solitude
```

Now you can work locally and create your own pull requests.

#### Maintainer

Sil van de Leemput

#### History

##### 0.1.5 (2020-07-15)

* Changed to using the *.sol extension for the command lists in the README 
* CLI fixed --ignore-errors typo on solitude job run
* Added black code style and pre-commit hooks

##### 0.1.4 (2020-07-10)

* HOTFIX cache wasn't properly created from scratch if folder didn't exist
* CLI Warnings have been added if run/extend/stop commands are issued without jobids 

##### 0.1.3 (2020-07-09)

* Added support for default command files option
* Renamed plugin interface get_command_hash
* Added job group to CLI interface
* Added support for defaults in config create
* Improved docs and added history section
