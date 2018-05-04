# python_qpeek
qpeek in python

```
usage: python_qpeek.py [-h] [--cat CAT] [--head HEAD] [--tail TAIL]                                                         
                       [--err ERR] [--out OUT] [--spool SPOOL] [--ssh SSH]                                                  
                       [--rsh RSH]                                                                                          
                       jobid

positional arguments:
  jobid          Jobid

optional arguments:
  -h, --help     show this help message and exit
  --cat CAT      Show all of the output file (default: True)
  --head HEAD    Show the beginning of the output file (default: False)
  --tail TAIL    Show the end of the output file (default: False)
  --err ERR      Show the stderr of the job (default: False)
  --out OUT      Show the stdout of the job (default: True)
  --spool SPOOL  Show the stdout of the job (default: /var/spool/torque/spool)
  --ssh SSH      Use SSH command (default: True)
  --rsh RSH      Use RSH command (default: False)
```
