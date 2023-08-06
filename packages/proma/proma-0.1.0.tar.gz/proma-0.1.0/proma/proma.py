from setuptools import _install_setup_requires
from distutils.dist import Distribution
from setuptools.config import read_configuration
import codecs
import os
import subprocess

from cookiecutter.main import cookiecutter


def load_project_param():
    """

    Examples:
      >>> p = load_project_param()
      >>> p['name']
      'proma'

    """
    conf_pth = "setup.cfg"
    conf_dict = read_configuration(conf_pth)

    opt = conf_dict["options"]
    if not "install_requires" in opt.keys():
        opt["install_requires"] = []

    with codecs.open(
        "requirements.txt",
        mode="r",
        encoding="utf-8",
    ) as f:
        req = f.read().strip().split("\n")
        conf_dict["options"]["install_requires"].extend(req)

    param = {}
    param.update(**conf_dict["option"])
    # param.update(**conf_dict["options"])
    param.update(**conf_dict["metadata"])

    if "script_name" not in param:
        param["script_name"] = "setup.py"

    return param


def create(name):
    print("Creating '%s'" % name)

    params = {
        "full_name": "Yann de The",
        "email": "ydethe@gmail.com",
        "github_username": "ydethe",
        "project_name": name,
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
        "version": "0.1.0",
        "add_pyup_badge": "y",
        "command_line_interface": "y",
    }

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter(
        "https://gitlab.com/ydethe/YannCookieCutter.git",
        checkout=None,  # The branch, tag or commit ID to checkout after clone.
        no_input=True,  # Prompt the user at command line for manual configuration?
        extra_context=params,  # A dictionary of context that overrides default and user configuration.
        replay=False,
        overwrite_if_exists=True,  # Overwrite the contents of output directory if it exists
        output_dir=".",  # Where to output the generated project dir into.
        config_file=None,  # User configuration file path
        default_config=False,  # Use default values rather than a config file
        password=None,  # The password to use when extracting the repository
        directory=None,  # Relative path to a cookiecutter template in a repository
        skip_if_file_exists=False,
    )


def test(args):
    param = load_project_param()

    name = param["name"]

    print("Testing '%s'" % name)

    cmd = ["tox", "-e", "py"]
    cmd.extend(args)

    process = subprocess.run(cmd, universal_newlines=True)


def build(args):
    param = load_project_param()

    param["script_args"] = ["sdist", "bdist_wheel"] + args

    name = param["name"]

    print("Building '%s' --> whl and tar.gz" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    # Find and parse the config file(s): they will override options from
    # the setup script, but be overridden by the command line.
    dist.parse_config_files()

    dist.run_command("bdist_wheel")
    dist.run_command("sdist")

def install(args):
    param = load_project_param()

    param["script_args"] = ["install"] + args

    name = param["name"]

    print("Installing '%s'" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    # Find and parse the config file(s): they will override options from
    # the setup script, but be overridden by the command line.
    dist.parse_config_files()

    dist.run_command("install")

def develop(args):
    param = load_project_param()

    param["script_args"] = ["develop"] + args

    name = param["name"]

    print("Develop '%s'" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    # Find and parse the config file(s): they will override options from
    # the setup script, but be overridden by the command line.
    dist.parse_config_files()

    dist.run_command("develop")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
