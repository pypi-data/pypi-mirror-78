import paramiko


def command_remote(server, username, password, cmd_to_execute):
    """
    Executes a command over ssh

    Implementation relies on paramiko
    """
    print(cmd_to_execute)
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    return "".join(ssh_stdout.readlines()), "".join(ssh_stderr.readlines())
