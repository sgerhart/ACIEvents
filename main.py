from __future__ import absolute_import, division, print_function
from builtins import *


import argparse
from apic.auth import apic_auth
from listener import start


def main(inargs):

    auth_token = apic_auth(inargs)
    apic_ip = inargs.aip

    apic_url = 'https://' + apic_ip + '/api/'

    # This Starts the Threads
    start(apic_ip, auth_token, apic_url)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ACICSP')

    parser.add_argument('-i', dest='aip', type=str, default='172.16.1.1',
                        help='APIC IP: x.x.x.x')

    parser.add_argument('-p', dest='apwd', type=str, default='password',
                        help='APIC Password')

    parser.add_argument('-u', dest='auser', type=str, default='admin',
                        help='APIC Username. "admin" defaulted')



    inargs = parser.parse_args()

    main(inargs)