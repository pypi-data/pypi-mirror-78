# -*- coding: utf-8 -*-
# Import python libs
import os
import shutil


def report(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    art = os.path.abspath(os.path.join("dist", opts.name))
    print(f"Executable created in {art}")


def clean(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    shutil.rmtree(opts.venv_dir)
    os.remove(opts.spec)
    os.remove(opts.req)
    try:
        # try to remove pyinstaller warn-*** file
        os.remove(os.path.join(opts.dir, "build", opts.name, f"warn-{opts.name}.txt"))
    except FileNotFoundError:
        pass
