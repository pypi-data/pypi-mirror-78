import subprocess

__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> str:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    pyvenv_bin = subprocess.check_output(["which", "pyvenv"]).decode().rstrip()
    subprocess.check_call([pyvenv_bin, "--help"])
    return pyvenv_bin


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    env_bin = hub.tiamat.virtualenv.pyvenv.bin(bname)
    cmd = [env_bin, opts.venv_dir, "--clear"]
    if opts.sys_site:
        cmd.append("--system-site-packages")

    subprocess.check_call(cmd)
