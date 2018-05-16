from __future__ import print_function

import gdb
import string
import subprocess
import sys


class ShellPipe (gdb.Command):
    "Command to pipe gdb internal command output to external commands."

    def __init__(self):
        super (ShellPipe, self).__init__("shell-pipe",
                gdb.COMMAND_DATA,
                gdb.COMPLETE_NONE, True)
        gdb.execute("alias -a sp = shell-pipe", True)

    def invoke(self, arg, from_tty):
        arg = arg.strip()
        if arg == "":
            print("Argument required (gdb_command_and_args | externalcommand..).")
            return

        gdb_command, shell_commands = None, None

        if '|' in arg:
            gdb_command, shell_commands = arg.split("|", maxsplit=1)
            gdb_command, shell_commands = gdb_command.strip(), shell_commands.strip()
        else:
            gdb_command = arg

        # If there is an error executing the first command as a gdb command,
        # assume that it is a shell command.
        try:
            # Collect the output and feed it through the pipe
            output = gdb.execute(gdb_command, True, True)
        except:
            output = None
            shell_commands = arg
            sys.stderr.write("Command '%s' is not a gdb command; treating it as a shell command.\n" % gdb_command)

        if shell_commands:
            shell_process = subprocess.Popen(shell_commands, stdin=subprocess.PIPE, shell=True)
            if output:
                shell_process.communicate(output.encode('utf-8'))
            shell_process.wait()
        else:
            sys.stdout.write(output)

ShellPipe()
