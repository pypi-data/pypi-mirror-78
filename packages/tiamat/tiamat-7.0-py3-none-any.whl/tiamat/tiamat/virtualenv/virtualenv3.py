import subprocess
from typing import List

__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> List[str]:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    ret = subprocess.check_output(["which", "virtualenv3"]).decode().rstrip()
    if ret:
        virtualenv_bin = [ret]
    else:
        virtualenv_bin = [opts.pybin, "-m", "virtualenv", "--verbose"]

    subprocess.check_call(virtualenv_bin + ["--help"])
    return virtualenv_bin


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    env_bin = hub.tiamat.virtualenv.virtualenv.bin(bname)
    cmd = env_bin + [opts.venv_dir, "--clear"]
    pyenv = opts.get("pyenv")
    if pyenv and pyenv != "system":
        cmd.extend(["--python", opts.pyenv])
    if opts.sys_site:
        cmd.append("--system-site-packages")

    subprocess.check_call(cmd)
