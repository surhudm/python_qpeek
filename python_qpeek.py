#!/usr/bin/env python
import re
import argparse
from subprocess import Popen, PIPE
import shlex
import sys
import os

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
parser.add_argument("--cat", help="Show all of the output file", dest="cat", default=True, action='store_true')
parser.add_argument("--head", help="Show the beginning of the output file", dest="head", default=False, action='store_true')
parser.add_argument("--tail", help="Show the end of the output file", dest="tail", default=False, action='store_true')
parser.add_argument("--err", help="Show the stderr of the job", dest="err", default=False, action='store_true')
parser.add_argument("--out", help="Show the stdout of the job", dest="out", default=True, action='store_true')
parser.add_argument("--spool", help="Show the stdout of the job", default="/var/spool/torque/spool")
parser.add_argument("--ssh", help="Use SSH command", default=True, dest="ssh", action='store_true')
parser.add_argument("--rsh", help="Use RSH command", default=False, dest="rsh", action='store_true')
parser.add_argument('jobid', help="Jobid", type=int)

args = parser.parse_args()

def get_command(ssh, rsh, cat, head, tail, err, out, spool, host, jobid, truehost):
    if head:
        cmd = "head"
    elif tail:
        cmd = "tail"
    else:
        sys.stderr.write("Defaulting to cat \n")
        cmd = "cat"

    if err:
        cmd = "%s %s/%d.%s.ER" % (cmd, spool, jobid, truehost)
    else:
        sys.stderr.write("Showing default stdout \n")
        cmd = "%s %s/%d.%s.OU" % (cmd, spool, jobid, truehost)

    if rsh:
        cmd = "rsh %s %s" % (host, cmd)
    else:
        sys.stderr.write("Defaulting to ssh\n")
        cmd = "ssh %s %s" % (host, cmd)

    return cmd

def get_host(jobid):
    # Get the host number using qstat
    cmd = "qstat -f %d" % (jobid)
    qstat_result = exec_cmd(cmd)

    success = False
    for line in qstat_result.stdout.split("\n"):
        compare_string = line.strip().split("=")
        exechost = compare_string[0].strip()
        if exechost == "exec_host":
            success = True
            host_string = compare_string[1].strip().split("/")[0]

    if not success:
        sys.stderr.write("The command %s did not result in host identification\n" % cmd)
        return None

    return host_string

# Parse exec_host
truehost = os.environ.get("HOSTNAME")
host = get_host(args.jobid)
cmd = get_command(args.ssh, args.rsh, args.cat, args.head, args.tail, args.err, args.out, args.spool, host, args.jobid, truehost)

result = exec_cmd(cmd)
print result.stdout
