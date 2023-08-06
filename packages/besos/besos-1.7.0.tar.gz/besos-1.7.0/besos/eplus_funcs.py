"""
Functions related to under-the-hood interactions with energyplus.
"""
import json
import os
import platform
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path

from deprecated.sphinx import deprecated

import besos.eppy_funcs as ef
import config
from besos import objectives
from besos.errors import ModeError
from besos.types import PathLike


# TODO: Make this a method of the building class when we add it
def get_idf_version(building):
    """ get energyplus version from idf or json file """
    mode = ef.get_mode(building)
    if mode == "idf":
        return building.idfobjects["VERSION"][0].Version_Identifier
    elif mode == "json":
        try:
            return building["Version"]["Version 1"]["version_identifier"]
        except KeyError:
            warnings.warn(f"Cannot find IDF version, substituting default.")
            return config.energy_plus_version
    else:
        raise ModeError(mode)


@deprecated(
    version="1.6.0",
    reason=("Version is derived automatically, this check is redundant."),
)
def check_idf_version(building, version):
    """ check if the version of energyplus matches the version in idf/json. """
    idf_version = get_idf_version(building).replace("-", ".")
    version = version.replace("-", ".")
    if idf_version != version[:3]:
        msg = f"IDF v{idf_version} does not match energyplus v{version[:3]}."
        warnings.warn(msg)


def has_hvac_templates(building) -> bool:
    """Returns whether or not the building contains HVACTemplate objects
    https://bigladdersoftware.com/epx/docs/8-0/input-output-reference/page-061.html

    :param building:
    :return: True if at leas one HVACTemplate object is present in the building.
    """
    mode = ef.get_mode(building)
    prefix = ef.convert_format("HVACTemplate", "class", mode)
    if mode == "idf":
        return any(
            k for k, v in building.idfobjects.items() if k.startswith(prefix) and v
        )
    else:
        return any(k for k in building if k.startswith(prefix))


def run_building(building, out_dir=config.out_dir, version=None, **eplus_args):
    """Run energy plus on a building object and return results

    If out_dir is not defined, the results will not be saved
    in the file system"""
    # backwards compatibility
    if version:
        warnings.warn(
            "the version argument is deprecated for run_building,"
            " and will be removed in the future",
            FutureWarning,
        )
        assert version == get_idf_version(building), "Incorrect version"

    with tempfile.TemporaryDirectory(dir=Path.home(), prefix=".besos_") as temp_dir:
        if out_dir is None:
            out_dir = temp_dir
        try:
            building_path = Path(temp_dir, "in.idf").resolve()
            building.saveas(str(building_path))
        except AttributeError:
            building_path = Path(temp_dir, "in.epJSON").resolve()
            with open(str(building_path), "w") as f:
                json.dump(building, f)
        expand_objects = has_hvac_templates(building)
        run_energyplus(
            building_path,
            out_dir=out_dir,
            version=get_idf_version(building),
            expand_objects=expand_objects,
            **eplus_args,
        )
        return objectives.read_eso(out_dir)


def run_energyplus(
    building_path: PathLike,
    out_dir: PathLike = config.out_dir,
    epw: PathLike = config.files["epw"],
    err_dir: PathLike = config.err_dir,
    schema_file=None,
    error_mode="Silent",
    version=config.energy_plus_version,
    ep_path=None,
    expand_objects: bool = False,
):
    """Run energy plus.
    This method is intended to work as similar to the cli tool as possible"""

    ep_exe_path, ep_directory = get_ep_path(version, ep_path)
    schema_file = schema_file or Path(ep_directory, "Energy+.idd")

    cmd = [
        ep_exe_path,
        "--idd",
        schema_file,
        "--weather",
        epw,
    ]
    if out_dir:
        cmd += ["--output-directory", out_dir]
    if expand_objects:
        cmd.append("--expandobjects")
    cmd.append(building_path)
    needs_shell = platform.system() == "Windows"
    try:
        subprocess.run(cmd, check=True, shell=needs_shell)
    except subprocess.CalledProcessError as e:
        # TODO: This log is excessively noisy. Can we cut it down to just the command's stderr?
        if error_mode != "Silent":
            # print eplus error
            filename = Path(out_dir, "eplusout.err")
            if os.path.exists(filename):
                err_file = open(filename, "r")
                for line in err_file:
                    print(line)
                print()
                err_file.close()
        if err_dir is not None and out_dir != err_dir:
            # copy eplus error files to err_dir
            if os.path.exists(err_dir):
                shutil.rmtree(err_dir)
            shutil.copytree(out_dir, err_dir)
        raise e


def get_ep_path(version, ep_path=None):
    """ get energyplus installation path by version"""
    if ep_path is not None:
        ep_directory = ep_path
        if platform.system() == "Windows":
            ep_exe = os.path.join(ep_directory, "energyplus.exe")
        elif platform.system() == "Linux":
            ep_exe = os.path.join(ep_directory, "energyplus")
        else:
            ep_exe = os.path.join(ep_directory, "energyplus")
    else:
        if len(version) == 3:
            if version == "9.0":
                version = "9-0-1"
            else:
                version = version.replace(".", "-") + "-0"
        else:
            version = version.replace(".", "-")
        # this is duplicated from eppy.runner.run_functions.paths_from_version
        if platform.system() == "Windows":
            ep_directory = "C:/EnergyPlusV{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus.exe")
        elif platform.system() == "Linux":
            ep_directory = "/usr/local/EnergyPlus-{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus")
        else:
            ep_directory = "/Applications/EnergyPlus-{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus")
    return ep_exe, ep_directory


def print_available_outputs(
    building,
    version=None,
    name=None,
    frequency=None,
):
    # backwards compatibility
    if version:
        warnings.warn(
            "the version argument is deprecated for print_available_outputs,"
            " and will be removed in the future",
            FutureWarning,
        )
        assert version == get_idf_version(building), "Incorrect version"

    if name is not None:
        name = name.lower()
    if frequency is not None:
        frequency = frequency.lower()
    results = run_building(building)
    for key in results.keys():
        if name is not None:
            if name not in key[0].lower():
                continue
            if frequency is not None:
                if key[1].lower() != frequency:
                    continue
        elif frequency is not None:
            if key[1].lower() != frequency:
                continue
        print(list(key))
