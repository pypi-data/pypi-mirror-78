from pathlib import Path
import git

config_dir = Path.home() / '.gnote'
config_dir.mkdir(parents=True, exist_ok=True)

repo_dir = config_dir / 'repo'
repo_url = 'git@gitee.com:gitgj/code_notes.git'


def __init_repo():
    if (repo_dir / '.git').exists():
        git_local = git.Repo(repo_dir)
        git_remote = git_local.remote()
        git_remote.pull()
    else:
        git_local = git.Repo.clone_from(url=repo_url, to_path=repo_dir, multi_options=['--depth 1'])
        git_local.config_writer().set_value('user', 'name', 'guojian').release()
        git_local.config_writer().set_value('user', 'email', 'guojian_k@qq.com').release()
    return git_local


git_repo = __init_repo()
