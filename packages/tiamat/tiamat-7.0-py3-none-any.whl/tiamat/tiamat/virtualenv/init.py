# Import python libs
import ast
import os
import subprocess
import shutil
import sys
import tarfile
from typing import Dict, List

# "venv" is a keyword for bash, call the directory "virtualenv" but allow it to be accessed with the alias
__sub_alias__ = ["venv"]
__func_alias__ = {"bin_": "bin"}

OMIT = (
    "__pycache__",
    "PyInstaller",
)


def bin_(hub, bname: str) -> List[str]:
    func = getattr(hub.tiamat.virtualenv, hub.OPT.tiamat.venv_plugin).bin
    return func(bname)


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    func = getattr(hub.tiamat.virtualenv, hub.OPT.tiamat.venv_plugin).create
    func(bname)

    return hub.tiamat.virtualenv.init.setup_pip(bname)


def env(hub, bname) -> List[str]:
    opts = hub.tiamat.BUILDS[bname]
    ret = []
    if opts.locale_utf8:
        ret.extend(["env", "PYTHONUTF8=1", "LANG=POSIX"])
    return ret


def scan(hub, bname: str):
    """
    Scan the new venv for files and imports.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    for root, dirs, files in os.walk(opts.vroot):
        if _omit(root):
            hub.log.debug(f"Ignoring root in {root}")
            continue
        for d in dirs:
            full = os.path.join(root, d)
            if _omit(full):
                hub.log.debug(f"Ignoring dirs in {full}")
                continue
            opts.all_paths.add(full)
        for f in files:
            full = os.path.join(root, f)
            if _omit(full):
                hub.log.debug(f"Ignoring full in {full}")
                continue
            opts.all_paths.add(full)


def mk_adds(hub, bname: str):
    """
    Make the imports and datas for pyinstaller.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    for path in opts.all_paths:
        if "site-packages" not in path:
            continue
        if os.path.isfile(path):
            if not path.endswith(".py"):
                continue
            if path.endswith("__init__.py"):
                # Skip it, we will get the dir
                continue
            imp = _to_import(path)
            if imp:
                opts.imports.add(imp)
        if os.path.isdir(path):
            data = _to_data(path)
            imp = _to_import(path)
            if imp:
                opts.imports.add(imp)
            if data:
                opts.datas.add(data)


def setup_pip(hub, bname: str):
    """
    Initialize pip in the new virtual environment

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    pip_cmd = [opts.pybin, "-m", "pip"]

    # Verify that the pip executable exists
    subprocess.check_call(pip_cmd + ["--version"])

    # Upgrade pip, setuptools, and wheel
    pre_reqs = ["pip", "setuptools<45.0.0>=49.1.1", "wheel"]
    # Distro is included in python3.8 and later, explicitly install it otherwise
    if sys.version_info < (3, 8):
        pre_reqs.append("distro")

    # Install pre-requirements
    subprocess.check_call(pip_cmd + ["install", "--upgrade"] + pre_reqs)

    # Install old pycparser to fix: https://github.com/eliben/pycparser/issues/291
    requirements = ["pycparser==2.14"]
    if opts.get("req"):
        requirements.extend(["-r", opts.req])
    if opts.srcdir:
        files = _get_srcdir_files(opts.srcdir)
        requirements.extend(files)
    if os.path.isfile(os.path.join(opts.dir, "setup.py")):
        requirements.append(opts.dir)
    if opts.dev_pyinst:
        # Install development version of pyinstaller to run on python 3.8
        requirements.append(
            "https://github.com/pyinstaller/pyinstaller/tarball/develop"
        )
    else:
        requirements.append("PyInstaller==3.6")

    subprocess.check_call(pip_cmd + ["install"] + requirements, cwd=opts.srcdir)

    if opts.system_copy_in:
        _copy_in(opts)
    if os.path.isfile(opts.exclude):
        subprocess.check_call(pip_cmd + ["uninstall", "-y", "-r"] + opts.exclude)

    os.environ[
        "LD_LIBRARY_PATH"
    ] = f'{os.environ.get("LD_LIBRARY_PATH")}:{os.path.join(opts.venv_dir, "lib")}'.strip(
        ":"
    )
    # Add libpath to the environment for AIX
    os.environ[
        "LIBPATH"
    ] = f"{os.environ.get('LIBPATH')}:{os.path.join(opts.venv_dir, 'lib')}".strip(":")


def _omit(test: str) -> bool:
    """
    :param test:
    :return:
    """
    for bad in OMIT:
        if bad in test:
            return True
    return False


def _to_import(path: str) -> str:
    """
    :param path:
    :return:
    """
    ret = path[path.index("site-packages") + 14 :].replace(os.sep, ".")
    if ret.endswith(".py"):
        ret = ret[:-3]
    return ret


def _to_data(path: str) -> str:
    """
    :param path:
    :return:
    """
    dest = path[path.index("site-packages") + 14 :]
    src = path
    if not dest.strip():
        return ""
    ret = f"{src}{os.pathsep}{dest}"
    return ret


def _copy_in(opts: Dict[str, str]):
    """
    Copy in any extra directories from the python install.

    :param opts:
    """
    cmd = [opts["pybin"], "-c", "'import sys;print(sys.path)'"]
    tgt = ""
    dtgt = os.path.join(os.path.join(opts["venv_dir"], "lib"))
    for fn in os.listdir(dtgt):
        tmptgt = os.path.join(dtgt, fn)
        if os.path.isdir(tmptgt):
            tgt = os.path.join(tmptgt, "site-packages")
    data = subprocess.check_output(cmd).decode()
    done = set()
    for path in ast.literal_eval(data):
        if not path:
            continue
        if not os.path.isdir(path):
            continue
        for fn in os.listdir(path):
            if fn in done:
                continue
            if fn in opts["system_copy_in"]:
                full = os.path.join(path, fn)
                if os.path.isdir(full):
                    shutil.copytree(full, os.path.join(tgt, fn))
                    done.add(fn)


def _get_srcdir_files(srcdir: str) -> List[str]:
    """
    Return the files that are python archives.

    :param srcdir:
    """
    files = []
    for fn in os.listdir(srcdir):
        if fn.endswith(".whl"):
            files.append(fn)
        if fn.endswith(".tar.gz"):
            # Might be a source archive
            with tarfile.open(fn) as tfp:
                for name in tfp.getnames():
                    if name.count(os.sep) > 1:
                        continue
                    if os.path.basename(name) == "PKG-INFO":
                        files.append(fn)
                        break
    return files
