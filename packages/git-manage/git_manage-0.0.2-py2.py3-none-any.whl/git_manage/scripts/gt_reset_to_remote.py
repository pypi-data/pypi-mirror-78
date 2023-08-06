# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os

import os
from git import Repo
import git
import getpass

import requests

import git_manage.git_tools as git_tools
import argparse
import yaml

def reset_branches(git_list,verbose=True):    

    git_command_error = []
    no_path = []
    
    ll = len(git_list)
    for ii,repo_path in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),repo_path)
        try:
            r = Repo(repo_path)
            
            # remote_branches = []
            # for rr in r.remote().refs:
                # if not rr.name.lower().endswith('/head'):
                    # remote_branches.append(rr)
            # remote_branches_s = set(remote_branches)
            
            active_branch = r.active_branch
            
            try:
                
                if not r.is_dirty(untracked_files=True):
                    
                    for branch in r.branches:
                        if branch.tracking_branch() is not None:
    
                            tb = branch.tracking_branch()
                            if r.is_ancestor(branch.commit,tb.commit):
                                if branch.commit.hexsha != tb.commit.hexsha:
                                    branch.checkout()
                                    r.head.reset(tb.commit,index=True,working_tree=True)
                                    print('Yes')
            except Exception as e:
                print(e)
            finally:
                active_branch.checkout()
        except git.NoSuchPathError as e:        
         no_path.append((repo_path,e))
        except git.GitCommandError as e:        
            git_command_error.append((repo_path,e))   



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

    reset_branches(git_list)
