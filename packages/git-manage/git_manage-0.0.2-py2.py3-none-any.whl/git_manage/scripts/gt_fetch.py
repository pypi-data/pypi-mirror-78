# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os
import git_manage.git_tools as git_tools
import argparse
import yaml

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude_local',dest='exclude_local_f',default = None)
    args=parser.parse_args()
    
    if args.exclude_local_f:
        with open(args.exclude_local_f) as f:
            exclude = yaml.load(f,Loader=yaml.FullLoader)
    else:
        exclude = None

    p1 = os.path.abspath(os.path.expanduser('~'))
    search_depth = 5

    git_list = git_tools.find_repos(p1,search_depth = 5,exclude=exclude)
    git_list = git_tools.fetch(git_list)
    git_tools.check_unmatched(git_list)

