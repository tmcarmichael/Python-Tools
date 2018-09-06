#Linux as root

#!usr/bin/env python3
import subprocess as sp
import optparse as op
#alt#import argparse as ap
import re

def get_args():
    cliparse = op.OptionParser()
    #alt#cliparse = ap.ArgumentParser()
    cliparse.add_option("-i", "--interface", dest="interface", help="Network interface to switch MAC address")
    #alt#cliparse.add_argument("-i", "--interface", dest="interface", help="Network interface to switch MAC address")
    cliparse.add_option("-m", "--MAC", dest="new_MAC", help="New MAC address")
    #alt#cliparse.add_argument("-m", "--MAC", dest="new_MAC", help="New MAC address")
    (opts, args) = cliparse.parse_args()
    #alt#opts = cliparse.parse_args()
    if not opts.interface:
        cliparse.error("Specify an interface, use --help for more information.")
    elif not opts.new_MAC:
        cliparse.error("Specify a new MAC address, use --help for more information.")
    return opts
    
def get_MAC(interface):
    ifconfig_search = sp.getoutput(["ifconfig", interface])
    mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_search)
    if mac_addr:
        return mac_addr.group(0)
    else:
        print('Could not find MAC address.')

def rename_MAC(interface, new_MAC):
    print('Changing MAC Address for network interface: ' + interface + ' to ' + new_MAC)
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_MAC])
    sp.call(["ifconfig", interface, "up"])

def main():
    opts = get_args()
    MACaddr_current = get_MAC(opts.interface)
    print('Current MAC: ' + str(MACaddr_current))
    rename_MAC(opts.interface, opts.new_MAC)
    MACaddr_current = get_MAC(opts.interface)
    if MACaddr_current == opts.new_MAC:
        print('MAC was successfully changed to: ' + MACaddr_current)
    else:
        print('MAC address was not changed, use \'MAC_addr_changer.py --help\' for more information.')

main()
