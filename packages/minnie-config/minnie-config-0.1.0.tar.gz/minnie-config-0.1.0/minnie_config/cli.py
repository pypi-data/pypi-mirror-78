#!/usr/bin/env python

import argparse
import sys
import os
import subprocess
import traceback

def ismount_windows(path):
    subprocess # Sincerely need an accurate way of checking the mount correctly after mapped or unmapped drive is disconnected,
               # otherwise it just claims it's mounted requiring -r to succefully remount.

def mounter(): # using pathlib.Path here might enable me to skip the drive_letter check down below
    if os.name == 'nt':
        dir_name = r'\\at-storage.ad.bcm.edu\dj-stor01'
        mount_cmd = 'net use {drive} {dir} {password} /user:{username} /persistent:{persistence}'
        unmount_cmd = 'net use {switch} /delete'
    elif False and os.name == 'posix':
        # os.path.ismount(path) only works for Unix/Posix, same for pathlib.Pathlib().is_mount()
        dir_name = '/at-storage.ad.bcm.edu/dj-stor01' # Wrong?
        mount_cmd = ''
        unmount_cmd = ''
    else:
        print('Currently only works for Windows')
        return 1
    
    parser = argparse.ArgumentParser(description='Mounts {}'.format(dir_name), usage='%(prog)s [options]')

    parser.add_argument('-m', '--unmount', action='store_true',
                        help='unmounts {}'.format(dir_name))
    parser.add_argument('-s', '--save', action='store_true',
                        help='sets the mount as persistent')
    parser.add_argument('-d', '--drive', type=str, default='',
                        help='chooses which drive letter to assign to, if absent will mount without mapping, will fail if the drive letter is already mapped to')
    parser.add_argument('-u', '--user', type=str,
                        help='username credentials for mounting, if absent it will ask for input')
    parser.add_argument('-p', '--password', type=str,
                        help='password credentials for mounting, if absent will ask for input')
    parser.add_argument('-r', '--reset', action='store_true',
                        help='retries the mount command even if the drive is already mounted'
                        ', also useful if the program believes it is mounted even when it isn\'t')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='prints traceback on subprocess errors')

    args = parser.parse_args()

    drive_letter = args.drive
    if drive_letter:
        if not drive_letter.endswith(':'):
            drive_letter += ':'

    if args.unmount:
        if os.path.ismount(dir_name):
            switch = drive_letter if drive_letter else dir_name
            print('Unmounting {}'.format(switch))
            unmount_cmd = unmount_cmd.format(switch=switch)
            if args.verbose: print(unmount_cmd)
            try:
                subprocess.check_call(unmount_cmd.split())
            except subprocess.CalledProcessError:
                if args.verbose:
                    traceback.print_exc()
        else:
            print('{} was not found'.format(dir_name))
            
        return 0

    if os.path.ismount(dir_name): # This sometimes returns only true for Windows, even if the point is not mounted
        print('{} is already mounted'.format(dir_name))
        if args.reset:
            print('Retrying mount')
        else:
            return 1

    if os.path.isdir(drive_letter):
        print('Drive {} is already in use'.format(drive_letter))
        return 1
    
    username = args.user
    if username is None:
        username = input('Username: ')

    password = args.password
    if password is None:
        from getpass import getpass
        password = getpass('Password: ')

    if args.save:
        persistence = 'yes'
    else:
        persistence = 'no'

    mount_cmd = mount_cmd.format(
        drive=drive_letter,
        dir=dir_name,
        username=username,
        password=password,
        persistence=persistence
    )

    if args.verbose: print(mount_cmd)

    try:
        subprocess.check_call(mount_cmd.split())
    except subprocess.CalledProcessError:
        if args.verbose:
            traceback.print_exc()