# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:06:40 2019

@author: daukes
"""
import os
import yaml
import git_manage.git_tools as git_tools
import sys
import argparse


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude_local',dest='exclude_local_f',default = None)
    parser.add_argument('--exclude_remote',dest='exclude_remote_f',default = None)
    parser.add_argument('--user',dest='user',default = None)
    args = parser.parse_args()
    
    if args.exclude_local_f:
        with open(args.exclude_local_f) as f:
            exclude = yaml.load(f,Loader=yaml.FullLoader)
    else:
        exclude = None

    if args.exclude_remote_f:
        with open(args.exclude_remote_f) as f:
            exclude_remote = yaml.load(f,Loader=yaml.FullLoader)
    else:
        exclude_remote = None

    search_path = os.path.abspath(os.path.expanduser('~'))

    git_tools.retrieve_nonlocal_repos(search_path,exclude = exclude, exclude_remote=exclude_remote,user = args.user)    
