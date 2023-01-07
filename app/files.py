from os import remove, path as ospath, makedirs
import shutil


def delete_path(path):
    if ospath.exists(path):
        if ospath.isdir(path):
            shutil.rmtree(path)
        else:
            remove(path)


def create_dir(path: str):
    if not ospath.exists(f'{path}'):
        makedirs(f'{path}')
