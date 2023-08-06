import argparse
import importlib.util
import os
import platform
import shutil
import stat
import subprocess
import tarfile
import urllib.request
import warnings
from collections import namedtuple
from dataclasses import dataclass, field
from inspect import isfunction, getmembers
from os import path
from typing import List, Callable
from urllib.parse import urlparse
from zipfile import ZipFile, ZipInfo

# Getting Platform Information


def guess_platforms():
    system = platform.system().lower()
    arch = platform.architecture()[0]

    if system == 'darwin':
        return ['macOS']

    if arch == '64bit':
        return [f'{system}-32bit', f'{system}-64bit']

    return [f'{system}-{arch}']


# Data Structures


@dataclass
class BuildSettings:
    platforms: List[str] = field(default_factory=guess_platforms)
    libs: List[str] = field(default_factory=list)
    do_clean: bool = False


Actions = namedtuple("Actions", [
    "download",
    "run",
    "copy_headers",
    "copy_binaries"
])


# Parsing CLI Arguments


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Builds dependecies from dependencies.py'
    )

    parser.add_argument('libraries',
                        type=str,
                        nargs='*',
                        help='List of libraries to build. If none is provided, every library will be buit.',
                        default=None)
    parser.add_argument('--platforms',
                        type=str,
                        nargs='+',
                        default=None,
                        help='List of platofrms to build for. If none is provided, it will be guessed based on the current machine.')
    parser.add_argument('--clean',
                        dest='clean',
                        default=False,
                        action='store_true',
                        help='Clean third-party folder before build')

    args = parser.parse_args()

    return BuildSettings(libs=args.libraries,
                         platforms=args.platforms or guess_platforms(),
                         do_clean=args.clean)


# File System Operations


def make_exec(file):
    """ Adds executable rights to a file. """

    st = os.stat(file)
    os.chmod(file, st.st_mode | stat.S_IEXEC)


def copy_everything_from(source: str,
                         dest: str,
                         overwrite=False,
                         exclude_dirs=[],
                         extensions=[]) -> int:
    """ Copies all files and directories from `from_dir` to `to_dir`,
        overwriting existing files if `overwrite` is `True`"""

    num_copied = 0

    for root, _, files in os.walk(source):
        for name in files:
            stem, ext = path.splitext(name)
            file_path = path.join(root, name)
            source_dir = path.dirname(file_path)
            folder_name = path.basename(source_dir)
            relative_dir = path.relpath(source_dir, source)
            dest_dir = path.join(dest, relative_dir)
            dest_file_path = path.join(dest_dir, name)

            if folder_name in exclude_dirs:
                continue

            if extensions and ext not in extensions:
                continue

            if not path.isdir(dest_dir):
                os.makedirs(dest_dir)

            if not overwrite:
                copy_i = 1
                while path.exists(dest_file_path):
                    dest_file_path = path.join(dest_dir,
                                               f'{stem}-{copy_i}{ext}')
                    copy_i += 1
            elif path.exists(dest_file_path):
                os.remove(dest_file_path)

            shutil.copy(file_path, dest_file_path)
            num_copied += 1

    return num_copied


def create_third_party_dir_if_needed():
    if not path.isdir(THIRD_PARTY_DIR):
        os.makedirs(THIRD_PARTY_DIR)


def remove_third_party_dir():
    if path.isdir(THIRD_PARTY_DIR):
        shutil.rmtree(THIRD_PARTY_DIR)


def create_third_party_include_dir_if_needed():
    if not path.isdir(THIRD_PARTY_INCLUDE_DIR):
        os.makedirs(THIRD_PARTY_INCLUDE_DIR)


def create_third_party_libs_dir_if_needed(platform: str):
    lib_dir = path.join(THIRD_PARTY_DIR, 'lib', platform)
    if not path.isdir(lib_dir):
        os.makedirs(lib_dir)


def remove_tmp_dir():
    if path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR, ignore_errors=True)


def reset_tmp_dir():
    remove_tmp_dir()
    os.mkdir(TMP_DIR)


def make_build_dir_if_needed(platform: str):
    build_dir = path.join(TMP_DIR, 'build', platform)
    if not path.isdir(build_dir):
        os.makedirs(build_dir)


# Actions Factories


def download_lib(url: str) -> str:
    """ Downloads a file from `url` to the current temporary location
        and unpacks it if it's an archive. """

    print(f'\tDownloading "{url}" ...')

    file_name = path.basename(urlparse(url).path)
    _, ext = path.splitext(file_name)

    if ext == '.zip':
        download_zip(url)
    elif ext == '.bz2' or ext == '.gz':
        download_tar(url)
    else:
        download_file(url)


def download_file(url: str) -> str:
    file_name = path.basename(urlparse(url).path)
    file_path = path.join(TMP_DIR, file_name)

    urllib.request.urlretrieve(url, file_path)

    return file_path


def download_tar(url: str):
    tar_filename = download_file(url)
    _, ext = path.splitext(tar_filename)
    ext = ext[1:]

    tar = tarfile.open(tar_filename, f"r:{ext}")
    tar.extractall(TMP_DIR)
    tar.close()

    os.remove(tar_filename)

    handle_extracted_archive()


class ZipFileWithPermissions(ZipFile):
    """ Custom ZipFile class handling file permissions. """

    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)
        return targetpath


def download_zip(url: str):
    """ Downloads an archive from `url` and unpacks it to the current temporary location. """

    zip_filename = download_file(url)

    with ZipFileWithPermissions(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(TMP_DIR)
        os.remove(zip_filename)

        handle_extracted_archive()


def handle_extracted_archive():
    try:
        subdirs = list(filter(lambda f: path.isdir(path.join(TMP_DIR, f)),
                              os.listdir(TMP_DIR)))
        first_subdir = path.join(TMP_DIR, subdirs[0])

        if len(subdirs) == 1:
            try:
                os.mkdir(TMP_COPY_DIR)
                copy_everything_from(first_subdir, TMP_COPY_DIR)
            except Exception as e:
                shutil.rmtree(TMP_COPY_DIR)
                raise e

            remove_tmp_dir()
            os.rename(TMP_COPY_DIR, TMP_DIR)

    except Exception as e:
        remove_tmp_dir()
        raise e


def copy_lib_headers(source_dir="source_dir",
                     target_dir="target_dir",
                     with_enclosing_dir=False,
                     exclude_dirs=[]):
    """ Copies all headers from `include` subdirectory found in `source_dir`,
        or, if none such found, from `source_dir` iself. """

    enclosing_folder_name = path.basename(source_dir)
    target_dir = path.join(THIRD_PARTY_INCLUDE_DIR, enclosing_folder_name) \
        if with_enclosing_dir \
        else THIRD_PARTY_INCLUDE_DIR

    def log_copying_from(source_dir: str):
        print(f'\tCopying headers from "{source_dir}" '
              f'to "{target_dir}"...')

    include_dir = path.join(source_dir, 'include')
    create_third_party_include_dir_if_needed()

    if path.isdir(include_dir):
        source_dir = include_dir

    log_copying_from(source_dir)

    num_copied = copy_everything_from(source_dir,
                                      target_dir,
                                      exclude_dirs=exclude_dirs,
                                      extensions=['.h', '.hpp', '.ipp'])

    if not num_copied:
        warnings.warn("Asked to copy headers, but nothing was copied.")


def copy_lib_binaries(source_dir="source_dir", target_dir="target_dir"):
    ''' Copies all binaries from `source_dir` to `target_dir`. '''

    print(f'\tCopying binaries from "{source_dir}" to "{target_dir}"...')

    for file in os.listdir(source_dir):
        _, ext = path.splitext(file)

        if ext not in ['.a', '.so', '.dylib', '.lib', '.dll']:
            continue

        file_path = path.join(source_dir, file)
        dest_file_path = path.join(target_dir, file)

        shutil.copyfile(file_path, dest_file_path, follow_symlinks=False)


def run(command: str, args: list = [], cwd="."):
    ''' Runs system `command` with arguments `args` in working directory `cwd`.
        Raises an exception if system command ends with an error. '''

    print(f'\tFrom working directory "{cwd}":')
    print(f'\t  Running command: "{command} {" ".join(args)}"')

    subprocess.run([command] + args, cwd=cwd, check=True)


# Building

def load_depsfile():
    if not path.exists("dependencies.py"):
        raise Exception("No dependencies.py in the current working directory.")

    spec = importlib.util.spec_from_file_location("dependencies",
                                                  "dependencies.py")

    global dependencies
    dependencies = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(dependencies)

    global THIRD_PARTY_DIR
    THIRD_PARTY_DIR = dependencies.THIRD_PARTY_DIR \
        if 'THIRD_PARTY_DIR' in dir(dependencies) \
        else 'third-party'

    global THIRD_PARTY_INCLUDE_DIR
    THIRD_PARTY_INCLUDE_DIR = path.join(THIRD_PARTY_DIR, 'include')

    global TMP_DIR
    TMP_DIR = path.join(THIRD_PARTY_DIR, 'tmp')

    global TMP_COPY_DIR
    TMP_COPY_DIR = path.join(THIRD_PARTY_DIR, 'tmp_copy')


def build(settings: BuildSettings):
    load_depsfile()

    print(f'-- Building dependencies to "{THIRD_PARTY_DIR}"... -- ')

    if settings.do_clean:
        remove_third_party_dir()

    if settings.libs:
        for name in settings.libs:
            not_found_exept = Exception(
                f'Build function for "{name}" not found in dependencies.py')

            try:
                fn = getattr(dependencies, name)
                if not isfunction(fn):
                    raise not_found_exept

                build_lib(name, fn, settings.platforms)

            except AttributeError:
                raise not_found_exept

    else:
        for name, fn in reversed(getmembers(dependencies)):
            if isfunction(fn) and name[0] != '_':
                build_lib(name, fn, settings.platforms)

    print(f'\n\nDependecies are built to "{THIRD_PARTY_DIR}".\n\n')


def build_lib(libname: str, build_fn: Callable, platforms: List[str]):
    print(f'\n-- Setting up dependency: {libname} --\n')

    create_third_party_dir_if_needed()
    reset_tmp_dir()

    already_downloaded = False

    def _download(url: str, only_once=True):
        if not only_once:
            download_lib(url)
            return

        nonlocal already_downloaded
        if not already_downloaded:
            download_lib(url)
            already_downloaded = True

    headers_already_copied = False
    for platform in platforms:
        src_dir = TMP_DIR
        build_dir = path.join(src_dir, 'build', platform)
        include_dir = path.join(THIRD_PARTY_DIR, 'include')
        libs_dir = path.join(THIRD_PARTY_DIR, 'lib', platform)

        def _copy_headers(source_dir=src_dir,
                          target_dir=include_dir,
                          only_once=True,
                          with_enclosing_dir=False,
                          exclude_dirs=[]):
            def configured_copy_fn():
                copy_lib_headers(source_dir,
                                 target_dir,
                                 with_enclosing_dir=with_enclosing_dir,
                                 exclude_dirs=exclude_dirs)

            if not only_once:
                configured_copy_fn()
                return

            nonlocal headers_already_copied
            if source_dir != src_dir or target_dir != include_dir:
                headers_already_copied = False

            if not headers_already_copied:
                configured_copy_fn()
                headers_already_copied = True

        def _copy_binaries(source_dir=build_dir, target_dir=libs_dir):
            create_third_party_libs_dir_if_needed(platform)
            copy_lib_binaries(source_dir, target_dir)

        def _run(command: str, args: list = [], cwd=path.realpath(build_dir)):
            make_build_dir_if_needed(platform)
            run(command, args, cwd)

        actions = Actions(download=_download,
                          run=_run,
                          copy_headers=_copy_headers,
                          copy_binaries=_copy_binaries)

        print(f'\n\tPlatform: {platform}:\n')

        build_fn(path.realpath(src_dir),
                 path.realpath(build_dir),
                 platform,
                 actions)

    remove_tmp_dir()


def main():
    build(parse_cli_args())


if __name__ == "__main__":
    main()
