# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Treble.ai
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Helper script to package wheels and relocate binaries."""

# Standard library imports
import os
import io
import sys
import glob
import shutil
import zipfile
import hashlib
import platform
import subprocess
import os.path as osp
from base64 import urlsafe_b64encode

# Third party imports
import toml
from auditwheel.lddtree import lddtree
from wheel.bdist_wheel import get_abi_tag


HERE = osp.dirname(osp.abspath(__file__))
PACKAGE_ROOT = osp.dirname(HERE)
PLATFORM_ARCH = platform.machine()
PYTHON_VERSION = sys.version_info


def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
    """Yield pieces of data from a file-like object until EOF."""
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk


def rehash(path, blocksize=1 << 20):
    """Return (hash, length) for path using hashlib.sha256()"""
    h = hashlib.sha256()
    length = 0
    with open(path, 'rb') as f:
        for block in read_chunks(f, size=blocksize):
            length += len(block)
            h.update(block)
    digest = 'sha256=' + urlsafe_b64encode(
        h.digest()
    ).decode('latin1').rstrip('=')
    # unicode/str python2 issues
    return (digest, str(length))  # type: ignore


def unzip_file(file, dest):
    """Decompress zip `file` into directory `dest`."""
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest)


def get_metadata():
    """Get version from text file and avoids importing the module."""
    with open(os.path.join(PACKAGE_ROOT, 'Cargo.toml'), 'r') as f:
        data = toml.load(f)
    # version = data['package']['version']
    return data['package']


def is_program_installed(basename):
    """
    Return program absolute path if installed in PATH.
    Otherwise, return None
    On macOS systems, a .app is considered installed if
    it exists.
    """
    if (sys.platform == 'darwin' and basename.endswith('.app') and
            osp.exists(basename)):
        return basename

    for path in os.environ["PATH"].split(os.pathsep):
        abspath = osp.join(path, basename)
        if osp.isfile(abspath):
            return abspath


def find_program(basename):
    """
    Find program in PATH and return absolute path
    Try adding .exe or .bat to basename on Windows platforms
    (return None if not found)
    """
    names = [basename]
    if os.name == 'nt':
        # Windows platforms
        extensions = ('.exe', '.bat', '.cmd')
        if not basename.endswith(extensions):
            names = [basename+ext for ext in extensions]+[basename]
    for name in names:
        path = is_program_installed(name)
        if path:
            return path


def patch_new_path(library_path, new_dir):
    library = osp.basename(library_path)
    name, *rest = library.split('.')
    rest = '.'.join(rest)
    hash_id = hashlib.sha256(library_path.encode('utf-8')).hexdigest()[:8]
    new_name = '.'.join([name, hash_id, rest])
    return osp.join(new_dir, new_name)


def patch_mac():
    # Find delocate location
    delocate_wheel = find_program('delocate-wheel')
    delocate_list = find_program('delocate-listdeps')
    if delocate_wheel is None:
        raise FileNotFoundError('Delocate was not found in the system, '
                                'please install it via pip')
    # Produce wheel
    print('Producing wheel...')
    subprocess.check_output(
        [
            sys.executable,
            'setup.py',
            'bdist_wheel'
        ],
        cwd=PACKAGE_ROOT
    )

    package_info = get_metadata()
    version = package_info['version'].replace('-', '.')
    wheel_name = 'pyduckling_native-{0}-cp{1}{2}-{3}-macosx_10_15_{4}.whl'.format(
        version, PYTHON_VERSION.major, PYTHON_VERSION.minor,
        get_abi_tag(), PLATFORM_ARCH)
    dist = osp.join(PACKAGE_ROOT, 'dist', wheel_name)

    print('Calling delocate...')
    subprocess.check_output(
        [
            delocate_wheel,
            '-v',
            dist
        ],
        cwd=PACKAGE_ROOT
    )

    print('Resulting libraries')
    subprocess.check_output(
        [
            delocate_list,
            '--all',
            dist
        ],
        cwd=PACKAGE_ROOT
    )


def patch_linux():
    # Get patchelf location
    patchelf = find_program('patchelf')
    if patchelf is None:
        raise FileNotFoundError('Patchelf was not found in the system, please'
                                ' make sure that is available on the PATH.')

    # Produce wheel
    print('Producing wheel...')
    subprocess.check_output(
        [
            sys.executable,
            'setup.py',
            'bdist_wheel'
        ],
        cwd=PACKAGE_ROOT
    )

    package_info = get_metadata()
    version = package_info['version'].replace('-', '.')
    wheel_name = 'pyduckling_native-{0}-cp{1}{2}-{3}-linux_{4}.whl'.format(
        version, PYTHON_VERSION.major, PYTHON_VERSION.minor,
        get_abi_tag(), PLATFORM_ARCH)
    dist = osp.join(PACKAGE_ROOT, 'dist', wheel_name)
    output_dir = osp.join(PACKAGE_ROOT, '.wheel-process')

    print(glob.glob(osp.join(PACKAGE_ROOT, 'dist', '*.whl')))

    if osp.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    print('Unzipping wheel...')
    unzip_file(dist, output_dir)

    print('Finding ELF dependencies...')
    main_binary = 'duckling.cpython-{0}-{1}-linux-gnu.so'.format(
        get_abi_tag().replace('cp', ''), PLATFORM_ARCH)
    output_library = osp.join(output_dir, 'duckling')
    binary_path = osp.join(output_library, main_binary)

    ld_tree = lddtree(binary_path)
    tree_libs = ld_tree['libs']

    binary_queue = [(n, main_binary) for n in ld_tree['needed']]
    binary_paths = {main_binary: binary_path}
    binary_dependencies = {}

    while binary_queue != []:
        library, parent = binary_queue.pop(0)
        library_info = tree_libs[library]
        print(library)
        print(library_info)
        if (library_info['path'].startswith('/lib') and
                not library.startswith('libpcre')):
            # Omit glibc/gcc/system libraries
            continue

        parent_dependencies = binary_dependencies.get(parent, [])
        parent_dependencies.append(library)
        binary_dependencies[parent] = parent_dependencies

        if library in binary_paths:
            continue

        binary_paths[library] = library_info['path']
        binary_queue += [(n, library) for n in library_info['needed']]

    print('Copying dependencies to wheel directory')
    new_libraries_path = osp.join(output_dir, 'duckling.libs')
    os.makedirs(new_libraries_path)
    new_names = {main_binary: binary_path}

    for library in binary_paths:
        if library != main_binary:
            library_path = binary_paths[library]
            new_library_path = patch_new_path(library_path, new_libraries_path)
            print('{0} -> {1}'.format(library, new_library_path))
            shutil.copyfile(library_path, new_library_path)
            new_names[library] = new_library_path

    print('Updating dependency names by new files')
    for library in binary_paths:
        if library != main_binary:
            if library not in binary_dependencies:
                continue
            library_dependencies = binary_dependencies[library]
            new_library_name = new_names[library]
            for dep in library_dependencies:
                new_dep = osp.basename(new_names[dep])
                print('{0}: {1} -> {2}'.format(library, dep, new_dep))
                subprocess.check_output(
                    [
                        patchelf,
                        '--replace-needed',
                        dep,
                        new_dep,
                        new_library_name
                    ],
                    cwd=new_libraries_path)

            print('Updating library rpath')
            subprocess.check_output(
                [
                    patchelf,
                    '--set-rpath',
                    "$ORIGIN",
                    new_library_name
                ],
                cwd=new_libraries_path)

            subprocess.check_output(
                [
                    patchelf,
                    '--print-rpath',
                    new_library_name
                ],
                cwd=new_libraries_path)

    print("Update main library dependencies")
    library_dependencies = binary_dependencies[main_binary]
    for dep in library_dependencies:
        new_dep = osp.basename(new_names[dep])
        print('{0}: {1} -> {2}'.format(main_binary, dep, new_dep))
        subprocess.check_output(
            [
                patchelf,
                '--replace-needed',
                dep,
                new_dep,
                main_binary
            ],
            cwd=output_library)

    print('Update main library rpath')
    subprocess.check_output(
        [
            patchelf,
            '--set-rpath',
            "$ORIGIN:$ORIGIN/../duckling.libs",
            binary_path
        ],
        cwd=output_library
    )

    print('Update RECORD file in wheel')
    dist_info = osp.join(
        output_dir, 'pyduckling_native-{0}.dist-info'.format(version))
    record_file = osp.join(dist_info, 'RECORD')

    with open(record_file, 'w') as f:
        for root, _, files in os.walk(output_dir):
            for this_file in files:
                full_file = osp.join(root, this_file)
                rel_file = osp.relpath(full_file, output_dir)
                if full_file == record_file:
                    f.write('{0},,\n'.format(rel_file))
                else:
                    digest, size = rehash(full_file)
                    f.write('{0},{1},{2}\n'.format(rel_file, digest, size))

    print('Compressing wheel')
    shutil.make_archive(dist, 'zip', output_dir)
    os.remove(dist)
    shutil.move('{0}.zip'.format(dist), dist)
    shutil.rmtree(output_dir)


if __name__ == '__main__':
    if sys.platform == 'linux':
        patch_linux()
    elif sys.platform == 'darwin':
        patch_mac()
