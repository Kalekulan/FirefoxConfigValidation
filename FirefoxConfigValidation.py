#!/usr/bin/env python3

from subprocess import Popen, PIPE
from time import sleep
from os import getenv
from collections import namedtuple

import sys
import traceback
import configparser


ConfigTuple = namedtuple('ConfigTuple', 'name value')
conf_tup = [ ConfigTuple('privacy.donottrackheader.enabled', 'true'),
             ConfigTuple('media.peerconnection.enabled', 'false'),
             ConfigTuple('media.navigator.enabled', 'false'),
             ConfigTuple('privacy.donottrackheader.enabled', 'true'),
             #ConfigTuple('privacy.trackingprotection.enabled', 'true'),
           ]

def check_vars(profile, var_tuple):
    ""
    read = open(profile).read()
    num_variables = len(var_tuple)
    num = 0
    for var in var_tuple:
        if var.name in read:
            num += 1
            print(str(num) + '/' + str(num_variables) + ' variables:', end = ' ')
            #print(str(num += 1) + '/' + str(num_variables), end = ' ')
            #print("'" + var + "' was found in file '" + file + "'")
            if var.value in read:
                print("OK")
            else:
                #print("'" + var + "' was NOT found in file '" + file + "'")
                print("NOK")
                raise Exception("'" + var + "' has incorrect value set to true in file '" + file + "'")
        else:
            print("NOK")


def get_profile(profile_name):
    ""
    ff_path = getenv('APPDATA') + '\\Mozilla\Firefox\\'
    config = configparser.ConfigParser()
    config.read(ff_path + 'profiles.ini')

    return (ff_path + config.get(profile_name, 'Path')).replace('/', '\\')

def main():
    try:
        profile_path = get_profile('Profile0')
    except Exception as e:
        print("Failed get_profile()")
        raise e
        sys.exit(1)

    try:
        check_vars(profile_path + '\\prefs.js', conf_tup)
    except Exception as e:
        print("Failed script with exception: " + str(e))
        raise e
        sys.exit(2)
    else:
        Popen("C:/Program Files/Mozilla Firefox/firefox.exe")
        print("Script done.")
        sys.exit(0)

if __name__ == '__main__': main()
