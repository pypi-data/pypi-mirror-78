# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:52:22 2018

@author: daukes
"""

import os
from git import Repo
import git
import getpass

from github import Github

def retrieve_nonlocal_repos(search_path=None,search_depth = 5,exclude = None,repo_path = None,exclude_remote = None,user = None):
    repo_path = repo_path or os.path.join(os.path.abspath(os.path.expanduser('~')),'repositories')
    if not (os.path.exists(repo_path) and os.path.isdir(repo_path)):
        os.mkdir(repo_path)
    exclude_remote = exclude_remote or []
    
    gits_local = find_repos(search_path,search_depth,exclude)
    print('local gits: ', gits_local)

    user = user or input('username: ')
    password = getpass.getpass('Password: ')

    gits_remote,owners = scan_github(user,password)
    print('remote gits: ', gits_remote)
    gits_remote_formatted = [reform_repo_name(item, user) for item in gits_remote]
    nonlocal_github_urls=diff(gits_local,gits_remote_formatted)
    remaining = list(set(nonlocal_github_urls).difference(set(exclude_remote)))
    print('diff: ', remaining)
    clone_list(remaining,repo_path,owners,user,password)    
#
    
#
def get_all_repos(user,password):


    g = Github(user, password)

    all_repos =  list(g.get_user().get_repos())
    return all_repos 
    
def scan_github(user,password):
    all_gits = []
    owners = {}
    for repo in get_all_repos(user,password):
        all_gits.append(repo.clone_url)
        owners[repo.clone_url]=repo.owner.login
    return all_gits,owners

def diff(local,github):    
    local_dict = {}
    local_urls = []
    for ii,item in enumerate(local):
    
        try:
            urls = []
            
            repo = Repo(item)
            for r in repo.remotes:
                urls.extend(r.urls)
            local_dict[item] = urls
            local_urls.extend(urls)
        except:
            pass        
    
    local_urls = set(local_urls)
    github_urls = set(github)
    
    nonlocal_github_urls =  list(github_urls-local_urls)
    return nonlocal_github_urls

def find_repos(search_path=None,search_depth=5,exclude=None):
    search_path = search_path or os.path.abspath(os.path.expanduser('~'))

    fp0 = os.path.normpath(os.path.abspath(search_path))
    base_depth = len(fp0.split(os.path.sep))
    
    exclude = exclude or [] 
    
    path_list = [search_path]
    git_list = []
    
    
    while len(path_list)>0:
        current_path = path_list.pop(0)
        fp = os.path.normpath(os.path.abspath(current_path))
        depth = len(fp.split(os.path.sep))
        
#        print(current_path)
        subpath = os.path.join(current_path,'.git')
        if os.path.isdir(subpath):
            git_list.append(current_path)
        else:
            if depth-base_depth<=search_depth:
                try:
                    subdirs = os.listdir(current_path)
                    subdirs = [os.path.join(current_path,item) for item in subdirs]
                    subdirs = [item for item in subdirs if os.path.isdir(item)]
                    subdirs = [item for item in subdirs if not item in exclude]
                    
                    path_list.extend(subdirs)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
    return git_list

def reform_repo_name(url,user):
        reponame = (url.split('/')[-1])
        repoowner = (url.split('/')[-2])
        newurl = 'git@'+user+'.github.com:'+repoowner+'/'+reponame
        return newurl
    

def clone_list(repo_addresses,full_path,owners,user,password):
    owners2 = dict([(reform_repo_name(url, user),owners[url]) for url in owners.keys()])
    for url in repo_addresses:
        reponame = (url.split('/')[-1])
        name=reponame.split('.')[0]
        owner = owners2[url]
        local_dest = os.path.normpath(os.path.join(full_path,owner,name))
        if not (os.path.exists(local_dest) and os.path.isdir(local_dest)):
            os.makedirs(local_dest)
        
        # newurl = reform_repo_name(url, user)
        print('cloning url:',url,'to: ',local_dest)

        repo = Repo.clone_from(url,local_dest)

def check_dirty(git_list):    
    dirty = []
    no_path = []
    git_list2 = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
            repo = Repo(item)
            if repo.is_dirty(untracked_files=True):
                dirty.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))

    return git_list2,dirty,no_path

def fetch(git_list,verbose = True):    

    unmatched = []
    git_command_error = []
    git_list2 = []
    no_path = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
            repo = Repo(item)
            
            fetches = repo.remotes[0].fetch()
            # if repo.commit().hexsha != fetches[0].commit.hexsha:
                # unmatched.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))
        except git.GitCommandError as e:        
            git_command_error.append((item,e))
            
    if verbose:
    
        print('---------')
        print('No Path:')
        for item,e in no_path:
            print(item,e)
        print('---------')
        print('Git Command:')
        for item,e in git_command_error:
            print(item,e)
        print('---------')
    
    return git_list2
    
def check_unmatched(git_list,verbose=True):    

    git_command_error = []
    no_path = []
    missing_local_branches = []
    missing_remote_branches = []
    unsynced_branches = []
    
    ll = len(git_list)
    for ii,repo_path in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),repo_path)
        try:
            r = Repo(repo_path)
            
            remote_branches = []
            for rr in r.remote().refs:
                if not rr.name.lower().endswith('/head'):
                    remote_branches.append(rr)
            remote_branches_s = set(remote_branches)
            
            
            for branch in r.branches:
                if branch.tracking_branch() is not None:
                    if branch.commit.hexsha != branch.tracking_branch().commit.hexsha:
                        unsynced_branches.append((repo_path,branch.name))
                else:
                    missing_remote_branches.append((repo_path,branch.name))
                
            b_s = [branch.tracking_branch() for branch in r.branches]
            b_s = [branch for branch in b_s if branch is not None]
            b_s = set(b_s)
            not_local = list(remote_branches_s.difference(b_s))
            for ref in not_local:
                missing_local_branches.append((repo_path,ref.name))
            
        except git.NoSuchPathError as e:        
            no_path.append((repo_path,e))
        except git.GitCommandError as e:        
            git_command_error.append((repo_path,e))
    
    if verbose:
    
        print('---------')
        print('Missing Local Branches:')
        for item in missing_local_branches:
            print(item)
        print('---------')
        print('Missing Remote Branches:')
        for item in missing_remote_branches:
            print(item)
        print('---------')
        print('Branches Unsynced:')
        for item in unsynced_branches:
            print(item)
        print('---------')
        print('No Path:')
        for item,e in no_path:
            print(item,e)
        print('---------')
        print('Git Command:')
        for item,e in git_command_error:
            print(item,e)
        print('---------')
    
    # return git_list2,unmatched,no_path,git_command_error   

if __name__=='__main__':
    r = get_all_repos()
    
