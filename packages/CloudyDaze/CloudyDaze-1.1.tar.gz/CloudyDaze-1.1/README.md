# CloudyDaze

bunch of usefull scripts for managing your cloud

please note that these use the most excellent credstash library for python,
you will need to setup your boto configuration for AWS for this to work.

[credstash setup](https://github.com/fugue/credstash)

---
## mySG.py

Tool to add your current IP address to the security group permissions.

Please add the following patameter to your ~/.aws/config file
```
mysg=sg_...
```

### help
```
$ ./mySG.py --help
usage: mySG.py [-h] [-p PROFILE] [-u URL] [-v] {enable,granted,myip,replace,revoke,args} ...

positional arguments:
  {enable,granted,myip,replace,revoke,args}
                        operations
    enable
    granted
    myip
    replace
    revoke
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        default=default
  -u URL, --url URL     default=https://api.ipify.org?format=json
  -v, --verbose         verbose logging
```

---
## myEC2.py

simple tool to start or stop ec2 instances

### help
```
$ ./myEC2.py --help
usage: myEC2.py [-h] [-p PROFILE] [-v] {list,start,stop,args} ...

positional arguments:
  {list,start,stop,args}
                        operations
    list
    start
    stop
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        default=default
  -v, --verbose         verbose logging
```

---
## mySSH.py

MySSH class for executing commands using SSH in Python

### help
```
$ ./mySSH.py -h
usage: mySSH.py [-h] [-H HOSTNAME] [-k KEY] [-p PASSWORD] [-P PORT] [-t TIMEOUT]
                [-u USERNAME] [-v]
                {execute,args} ...

positional arguments:
  {execute,args}        operations
    execute
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
  -k KEY, --key KEY     ssh key path
  -p PASSWORD, --password PASSWORD
  -P PORT, --port PORT  default=22, type=int
  -t TIMEOUT, --timeout TIMEOUT
                        connect timeout seconds, default=5, type=int
  -u USERNAME, --username USERNAME
  -v, --verbose         verbose logging

```
  
---
## mySCP.py

MySCP class for moving files using SSH in Python

### help
```
$ ./mySCP.py -h
usage: mySCP.py [-h] [-H HOSTNAME] [-k KEY] [-p PASSWORD] [-P PORT] [-t TIMEOUT]
                [-u USERNAME] [-v]
                {get,put,args} ...

positional arguments:
  {get,put,args}        operations
    get
    put
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
  -k KEY, --key KEY     ssh key path
  -p PASSWORD, --password PASSWORD
  -P PORT, --port PORT  default=22, type=int
  -t TIMEOUT, --timeout TIMEOUT
                        connect timeout seconds, default=5, type=int
  -u USERNAME, --username USERNAME
  -v, --verbose         verbose logging
```

---
## acknowledgements

code graciously borrowed from [StaSh for Pythonista](https://github.com/ywangd/stash)
