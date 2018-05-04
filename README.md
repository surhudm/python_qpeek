# python_qpeek
qpeek in python

```
usage: python_qpeek.py [-h] [--cat] [--head] [--tail] [--err] [--out]
                       [--spool SPOOL] [--ssh] [--rsh]
                       jobid

positional arguments:
  jobid          Jobid

optional arguments:
  -h, --help     show this help message and exit
  --cat          Show all of the output file (default: True)
  --head         Show the beginning of the output file (default: False)
  --tail         Show the end of the output file (default: False)
  --err          Show the stderr of the job (default: False)
  --out          Show the stdout of the job (default: True)
  --spool SPOOL  Show the stdout of the job (default: /var/spool/torque/spool)
  --ssh          Use SSH command (default: True)
  --rsh          Use RSH command (default: False)
```
