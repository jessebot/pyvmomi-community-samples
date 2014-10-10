# Written by Michael Rice and Jesse Hunt                                                              
# Github: https://github.com/michaelrice                                                              
# Website: https://michaelrice.github.io/                                                             
# Blog: http://www.errr-online.com/                                                                   
# This code has been released under the terms of the Apache 2 licenses                                
# http://www.apache.org/licenses/LICENSE-2.0.html                                                     
# major modifications by jessebot                                                                     
                                                                                                      
__author__ = 'errr, also jessebot'                                                                    
                                                                                                      
import atexit                                                                                         
                                                                                                      
from pyVim import connect                                                                             
from tools import cli                                                                                 
                                                                                                      
                                                                                                      
def setup_args():                                                                                     
    """                                                                                               
    Adds additional args to allow the vm fqdn to                                                      
    be set.                                                                                           
    """                                                                                               
    parser = cli.build_arg_parser()                                                                   
    parser.add_argument('-n', '--name',                                                               
                        required=True,                                                                
                        help='FQDN of VirtualMachine you want to vanquish from this realm.')          
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
    raise SystemExit("I can't find the virtual machine. :<")                                          
                                                                                                      
print "Gonna try murdering this machine, {0}".format(vm.name)                                         
                                                                                                      
# Can't delete a machine with it on.                                                                  
vm.PowerOff()                                                                                         
                                                                                                      
# Deletes virtual machine from datastore                                                              
vm.Destroy_Task()                                                                                     
                                                                                                      
print "This probably worked."                                                                         
