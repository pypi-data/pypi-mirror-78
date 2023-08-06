# -*- coding: utf-8 -*-
# Import python libs
import os
import pprint
import tempfile
import uuid
from dict_tools import data
from typing import List


def __init__(hub):
    """
    :param hub: The redistributed pop central hub.
    """
    hub.pop.sub.load_subdirs(hub.tiamat)
    os.environ["POP_BUILD"] = "1"
    os.environ["TIAMAT_BUILD"] = "1"
    hub.tiamat.BUILDS = {}
    hub.tiamat.SYSTEMD = ("rhel7", "rhel8", "arch", "debian10")
    hub.tiamat.SYSTEMD_DIR = "usr/lib/systemd/system/"
    hub.tiamat.SYSV = ("rhel5", "rhel6")
    hub.tiamat.SYSV_DIR = "etc/init.d"


def cli(hub):
    """
    Execute the routine from the CLI.

    :param hub: The redistributed pop central hub.
    """
    hub.pop.config.load(["tiamat"], cli="tiamat")
    hub.tiamat.init.builder(
        hub.OPT.tiamat.name,
        hub.OPT.tiamat.requirements,
        hub.OPT.tiamat.system_site,
        hub.OPT.tiamat.exclude,
        os.path.abspath(hub.OPT.tiamat.directory),
        hub.OPT.tiamat.dev_pyinstaller,
        hub.OPT.tiamat.pyinstaller_runtime_tmpdir,
        hub.OPT.tiamat.build,
        hub.OPT.tiamat.pkg,
        hub.OPT.tiamat.onedir,
        hub.OPT.tiamat.pyenv,
        hub.OPT.tiamat.run,
        hub.OPT.tiamat.no_clean,
        hub.OPT.tiamat.locale_utf8,
        hub.OPT.tiamat.dependencies,
        hub.OPT.tiamat.release,
        hub.OPT.tiamat.pkg_tgt,
        hub.OPT.tiamat.pkg_builder,
        hub.OPT.tiamat.srcdir,
        hub.OPT.tiamat.system_copy_in,
        hub.OPT.tiamat.tgt_version,
        python_bin=hub.OPT.tiamat.python_bin,
    )


def new(
    hub,
    name: str,
    requirements: str,
    sys_site: bool,
    exclude: str,
    directory: str,
    dev_pyinst: bool = False,
    pyinstaller_runtime_tmpdir: str = None,
    build: str = None,
    pkg: str = None,
    onedir: bool = False,
    pyenv: str = "system",
    run: str = "run.py",
    locale_utf8: bool = False,
    dependencies: str = None,
    release: str = None,
    pkg_tgt: str = None,
    pkg_builder: str = None,
    srcdir: str = None,
    system_copy_in: List[str] = None,
    tgt_version: str = None,
    python_bin: str = None,
) -> str:
    """
    :param hub: The redistributed pop central hub.
    :param name: The name of the project to build.
    :param requirements: The name of the requirements.txt file to use.
    :param sys_site: Include the system site-packages when building.
    :param exclude: The path to the exclude file, these python packages will be uninstalled.
    :param directory: The path to the directory to build from.
        This denotes the root of the python project source tree to work from.
        This directory should have the setup.py and the paths referenced in configurations will assume that this is the root path they are working from.
    :param dev_pyinst: Use the latest development build of PyInstaller.
    :param pyinstaller_runtime_tmpdir: Pyinstaller runtime tmpdir.
    :param build: Enter in commands to build a non-python binary into the deployed binary.
        The build options are set on a named project basis. This allows for multiple shared
        binaries to be embedded into the final build:

        build:
          libsodium:
            make:
              - wget libsodium
              - tar xvf libsodium*
              - cd libsodium
              - ./configure
              - make
            src: libsodium/libsodium.so
            dest: lib64/
    :param pkg: Options for building packages.
    :param onedir: Instead of producing a single binary produce a directory with all components.
    :param pyenv: The python version to build with.
    :param run: The location of the project run.py file.
    :param locale_utf8: Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540.
    :param dependencies: Comma separated list of dependencies needed for the build.
    :param release: Release string i.e. '1.el7'.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param pkg_builder: The package builder plugin to use.
    :param srcdir: Install all of the python package sources and/or wheels found in this directory.
    :param system_copy_in: A list of directories to copy into the build venv that are not otherwise detected.
    :param tgt_version: Target package version.
    :param python_bin: The python binary to use for system calls
    :return: The build name.
    """
    if name == ".":
        name = os.path.basename(os.path.abspath("."))
    venv_dir = tempfile.mkdtemp()
    is_win = os.name == "nt"
    if python_bin is None:
        if is_win:
            python_bin = os.path.join(venv_dir, "Scripts", "python")
        else:
            python_bin = os.path.join(venv_dir, "bin", "python3")
    if is_win:
        s_path = os.path.join(venv_dir, "Scripts", name)
    elif locale_utf8:
        s_path = "env PYTHONUTF8=1 LANG=POSIX " + os.path.join(venv_dir, "bin", name)
    else:
        s_path = os.path.join(venv_dir, "bin", name)

    bname = str(uuid.uuid1())
    requirements = os.path.join(directory, requirements)
    hub.tiamat.BUILDS[bname] = data.NamespaceDict(
        name=name,
        build=build,
        pkg=pkg,
        pkg_tgt=pkg_tgt,
        pkg_builder=pkg_builder,
        dependencies=dependencies,
        release=release,
        binaries=[],
        is_win=is_win,
        exclude=exclude,
        requirements=requirements,
        sys_site=sys_site,
        dir=os.path.abspath(directory),
        srcdir=srcdir,
        dev_pyinst=dev_pyinst,
        pyinstaller_runtime_tmpdir=pyinstaller_runtime_tmpdir,
        system_copy_in=system_copy_in,
        run=os.path.join(directory, run),
        spec=os.path.join(directory, f"{name}.spec"),
        pybin=python_bin,
        s_path=s_path,
        venv_dir=venv_dir,
        vroot=os.path.join(venv_dir, "lib"),
        onedir=onedir,
        all_paths=set(),
        imports=set(),
        datas=set(),
        cmd=[python_bin, "-B", "-OO", "-m", "PyInstaller"],
        pyenv=pyenv,
        pypi_args=[
            s_path,
            "--log-level=INFO",
            "--noconfirm",
            "--onedir" if onedir else "--onefile",
            "--clean",
        ],
        locale_utf8=locale_utf8,
        tgt_version=tgt_version,
    )
    req = hub.tiamat.init.mk_requirements(bname)
    hub.tiamat.BUILDS[bname].req = req
    return bname


def mk_requirements(hub, bname: str) -> str:
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    :return:
    """
    opts = hub.tiamat.BUILDS[bname]
    req = os.path.join(opts.dir, "__build_requirements.txt")
    with open(opts.requirements, "r") as rfh:
        data_ = rfh.read()
    with open(req, "w+") as wfh:
        wfh.write(data_)
    return req


def builder(
    hub,
    name,
    requirements: str,
    sys_site: str,
    exclude: str,
    directory: str,
    dev_pyinst: bool = False,
    pyinstaller_runtime_tmpdir: str = None,
    build: str = None,
    pkg: str = None,
    onedir: bool = False,
    pyenv: str = "system",
    run: str = "run.py",
    no_clean: bool = False,
    locale_utf8: bool = False,
    dependencies: str = None,
    release: str = None,
    pkg_tgt: str = None,
    pkg_builder: str = None,
    srcdir: str = None,
    system_copy_in: List[str] = None,
    tgt_version: str = None,
    python_bin: str = None,
):
    """
    :param hub: The redistributed pop central hub.
    :param name: The name of the project to build.
    :param requirements: The name of the requirements.txt file to use.
    :param sys_site: Include the system site-packages when building.
    :param exclude: The path to the exclude file, these python packages will be uninstalled.
    :param directory: The path to the directory to build from.
        This denotes the root of the python project source tree to work from.
        This directory should have the setup.py and the paths referenced in configurations will assume that this is the root path they are working from.
    :param dev_pyinst: Use the latest development build of PyInstaller.
    :param pyinstaller_runtime_tmpdir: Pyinstaller runtime tmpdir.
    :param build: Enter in commands to build a non-python binary into the deployed binary.
        The build options are set on a named project basis. This allows for multiple shared
        binaries to be embedded into the final build:

        build:
          libsodium:
            make:
              - wget libsodium
              - tar xvf libsodium*
              - cd libsodium
              - ./configure
              - make
            src: libsodium/libsodium.so
            dest: lib64/
    :param pkg: Options for building packages.
    :param onedir: Instead of producing a single binary produce a directory with all components.
    :param pyenv: The python version to build with.
    :param run: The location of the project run.py file.
    :param no_clean: Don't run the clean up sequence, this will leave the venv, spec file and other artifacts.
    :param locale_utf8: Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540.
    :param dependencies: Comma separated list of dependencies needed for the build.
    :param release: Release string i.e. '1.el7'.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param pkg_builder: The package builder plugin to use.
    :param srcdir: Install all of the python package sources and/or wheels found in this directory.
    :param system_copy_in: A list of directories to copy into the build venv that are not otherwise detected.
    :param tgt_version: Target package version.
    :param python_bin: The python binary to use for system calls
    """
    bname = hub.tiamat.init.new(
        name,
        requirements,
        sys_site,
        exclude,
        directory,
        dev_pyinst,
        pyinstaller_runtime_tmpdir,
        build,
        pkg,
        onedir,
        pyenv,
        run,
        locale_utf8,
        dependencies,
        release,
        pkg_tgt,
        pkg_builder,
        srcdir,
        system_copy_in,
        python_bin=python_bin,
    )
    hub.log.debug(
        f"Build config '{bname}':\n{pprint.pformat(hub.tiamat.BUILDS[bname])}"
    )
    hub.tiamat.virtualenv.init.create(bname)
    if tgt_version:
        hub.tiamat.BUILDS[bname].version = tgt_version
    else:
        hub.tiamat.data.version(bname)
    hub.tiamat.build.make(bname)
    hub.tiamat.virtualenv.init.scan(bname)
    hub.tiamat.virtualenv.init.mk_adds(bname)
    hub.tiamat.inst.mk_spec(bname)
    hub.tiamat.inst.call(bname)
    if pkg_tgt:
        hub.tiamat.pkg.init.build(bname)
    hub.tiamat.post.report(bname)
    if not no_clean:
        hub.tiamat.post.clean(bname)
