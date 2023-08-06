# -*- coding: utf-8 -*-
"""
The build plugin is used to execute the build routines for non-python components.
"""
# Import python libs
import os
import glob
import shutil
import subprocess
import tempfile
import sys
import requests


def make(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    build = opts.build
    if not build:
        return
    bdir = tempfile.mkdtemp()
    cur_dir = os.getcwd()
    os.chdir(bdir)
    if opts.srcdir:
        for fn in os.listdir(opts.srcdir):
            shutil.copy(os.path.join(opts.srcdir, fn), bdir)
    for proj, conf in build.items():
        if not opts.srcdir:
            if "sources" in conf:
                sources = conf["sources"]
                if isinstance(sources, str):
                    sources = [sources]
                for source in sources:
                    response = requests.get(source)
                    with open(
                        os.path.join(bdir, os.path.split(source)[1]), "wb"
                    ) as file:
                        file.write(response.content)
        if "make" in conf:
            for cmd in conf["make"]:
                retcode = subprocess.call(cmd, shell=True, cwd=bdir)
                if retcode != 0:
                    hub.log.error("make failed.")
                    sys.exit(retcode)
        if "src" in conf and "dest" in conf:
            srcs = conf["src"]
            dest = os.path.join(opts.venv_dir, conf["dest"])
            hub.log.info(f"Copying: {srcs}->{dest}")
            if not isinstance(srcs, (list, tuple)):
                srcs = [srcs]
            final_srcs = set()
            for src in srcs:
                globed = glob.glob(src)
                if not globed:
                    hub.log.warning(f"Expression f{src} does not match any file paths")
                    continue
                final_srcs.update(globed)
            for src in final_srcs:
                fsrc = os.path.join(bdir, src)
                if os.path.isfile(fsrc):
                    try:
                        shutil.copy(fsrc, dest, follow_symlinks=True)
                    except IOError as e:
                        hub.log.warning(f"Unable to copy file {fsrc} to {dest}: {e}")
                    hub.tiamat.BUILDS[bname].binaries.append(
                        (os.path.join(dest, os.path.basename(fsrc)), ".")
                    )
                elif os.path.isdir(fsrc):
                    shutil.copytree(fsrc, dest)
                else:
                    hub.log.warning(f"FAILED TO FIND FILE {fsrc}")
    os.chdir(cur_dir)
