import gnote
from pathlib import Path
from typing import List, Dict
import subprocess

from rich.markdown import Markdown
from rich.console import Console
from gnote import repo_dir
import platform

console = Console()
root = Path(repo_dir)
cmd = ['powershell'] if 'windows' == platform.system().lower() else []


def list_note() -> Dict[str, Path]:
    paths: List[Path] = []

    def recursion_file(p: Path):
        for sub in p.iterdir():
            if sub.name.startswith('.'):
                continue
            if sub.is_dir():
                recursion_file(sub)
            else:
                paths.append(sub)

    recursion_file(gnote.repo_dir)
    return {p.name.rsplit('.md')[0]: p for p in paths}


def code(name):
    if name == '.':
        subprocess.call(cmd + (['code', '-w', root]))
    else:
        dct = list_note()
        new_p = root / name
        new_p = new_p.with_suffix('.md')
        p = dct.get(name, new_p)
        subprocess.call(cmd + (['code', '-w', p]))


def push():
    # 自动提交到远程
    g = gnote.git_repo.git
    g.add('.')
    g.commit(m='update')
    g = gnote.git_repo.git
    g.push()


def cat(name):
    name_path = list_note()
    path = name_path.get(name, None)
    return Markdown(path.read_text()) if path else ''


def search(name) -> List[str]:
    dct = list_note()
    return [i for i in dct.keys() if name in i]


def pyvim(name):
    dct = list_note()
    new_p = root / name
    new_p = new_p.with_suffix('.md')
    p = dct.get(name, new_p)
    subprocess.call(cmd + ['pyvim', p])


def open_root_path():
    return root


def auto_complete(ctx, args, incomplete):
    notes = list_note()
    return [n for n in notes if incomplete in n]
