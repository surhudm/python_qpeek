#!/usr/bin/env python
import re
import argparse
from subprocess import Popen, PIPE
import shlex
import sys

class Result:
    pass

def exec_cmd(command):
    result = Result()
    p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    result.exit_code = p.returncode
    result.stdout = stdout
    result.stderr = stderr
    result.command = command
    if p.returncode != 0:
        print 'Error executing command [%s]' % command
        print 'stderr: [%s]' % stderr
        print 'stdout: [%s]' % stdout
    return result

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--cat", help="Show all of the output file", type=bool, default=True)
parser.add_argument("--head", help="Show the beginning of the output file", type=bool, default=False)
parser.add_argument("--tail", help="Show the end of the output file", type=bool, default=False)
parser.add_argument("--err", help="Show the stderr of the job", type=bool, default=False)
parser.add_argument("--out", help="Show the stdout of the job", type=bool, default=True)
parser.add_argument("--spool", help="Show the stdout of the job", default="/var/spool/torque/spool")
parser.add_argument("--ssh", help="Use SSH command", type=bool, default=True)
parser.add_argument("--rsh", help="Use RSH command", type=bool, default=False)
parser.add_argument('jobid', help="Jobid", type=int)

args = parser.parse_args()

def get_command(ssh, rsh, cat, head, tail, err, out, spool, host, jobid):
    if cat:
        cmd = "cat"
    elif head:
        cmd = "head"
    elif tail:
        cmd = "tail"
    else:
        sys.stderr.write("Performing default cat command\n")
        cmd = "cat"

    if out:
        cmd = "%s %s/%d.%s.OU" % (cmd, spool, jobid, host)
    elif err:
        cmd = "%s %s/%d.%s.ER" % (cmd, spool, jobid, host)

    if ssh:
        cmd = "ssh %s %s" % (host, cmd)
    elif rsh:
        cmd = "rsh %s %s" % (host, cmd)
    else:
        sys.stderr.write("Performing default ssh command\n")
        cmd = "ssh %s %s" % (host, cmd)

    return cmd

def get_host(jobid):
    # Get the host number using qstat
    cmd = "qstat %d" % (jobid)
    qstat_result = exec_cmd(cmd)

    success = False
    for line in result.stdout.split("\n"):
        compare_string = line.strip().split("=")
        exechost = compare_string[0].strip()
        if exechost == "exec_host":
            success = True
            host_string = compare_string[1].split("/")

    if not success:
        sys.stderr.write("The command %s did not result in host identification\n")
        return None

    return host_string

# Parse exec_host

host = get_host(jobid)
cmd = get_command(args.ssh, args.rsh, args.cat, args.head, args.tail, args.err, args.out, args.spool, host, args.jobid)

result = exec_cmd(cmd)
print result.stdout
