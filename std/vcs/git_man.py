import os

import git
import subprocess

from std.std import merge


def git_clone(url: str, dst: str, depth: int=1, branch: str = "master") -> None:
    print("clone_git_rep")
    git.Git().clone(url, dst, depth=depth, branch=branch)
    # git.Git().clone(url, dst, depth=depth, branch="fix-issues-2018-08")


def check_local_rep(src: str) -> bool:
    print("check_local_rep")
    if os.path.exists(src):
        return True
    return False


def git_pull(git_dir: str) -> None:
    print("update_local_rep")
    repo = git.Repo(git_dir)
    o = repo.remotes.origin
    o.pull()


def generate_pods(src: str, assets_path: str) -> None:
    path = "MASTER_PATH"

    script_path = merge(assets_path, '/cocoa_install.sh')
    params = os.environ

    params[path] = src  # Put path to final project in variables environment
    print(script_path)
    # TODO REPLACE ON os.chmode
    subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
    subprocess.call([script_path], shell=True, env=params)  # Run script
