# Written by Michael Rice
# Github: https://github.com/michaelrice
# Website: https://michaelrice.github.io/
# Blog: http://www.errr-online.com/
# This code has been released under the terms of the Apache 2 licenses
# http://www.apache.org/licenses/LICENSE-2.0.html
# modifications by jessebot: changed uuid finding to dns
# added info gathered from vm, from another of errr's vminfo_quick.py

__author__ = 'errr'

import atexit

from pyVim import connect
from tools import cli


def setup_args():
    """
    Adds additional args to allow the vm uuid to
    be set.
    """
    parser = cli.build_arg_parser()
    parser.add_argument('-n', '--name',
                        required=True,
                        help='DNS name of the VirtualMachine you want info on.')
    my_args = parser.parse_args()
    return cli.prompt_for_password(my_args)

args = setup_args()
si = None
try:
    si = connect.SmartConnect(host=args.host,
                              user=args.user,
                              pwd=args.password,
                              port=int(args.port))
    atexit.register(connect.Disconnect, si)
except IOError, e:
    pass

if not si:
    raise SystemExit("Unable to connect to host with supplied info.")
vm = si.content.searchIndex.FindByDnsName(None, args.name, True)
if not vm:
    raise SystemExit("Unable to locate VirtualMachine.")

summary = vm.summary
print("Name       : ", summary.config.name)
print("Path       : ", summary.config.vmPathName)
print("Os      : ", summary.config.guestFullName)
annotation = summary.config.annotation
if annotation != None and annotation != "":
    print("Annotation : ", annotation)
    print("State      : ", summary.runtime.powerState)
if summary.guest != None:
    ip = summary.guest.ipAddress
    if ip != None and ip != "":
        print("IP         : ", ip)
    if summary.runtime.question != None:
        print("Question  : ", summary.runtime.question.text)
    print("")
