"""awscreds Credentials module."""

import os

import boto3
import click

from ccaawscreds import __version__
from ccaawscreds.iamuser import IAMUser
from ccaawscreds.inifile import IniFile
from ccaawscreds.pwgen import pwgen


@click.group()
def awsk():
    pass


@click.group()
def awspw():
    pass


@click.group()
def genpw():
    pass


def findConfigFile():
    try:
        ini = None
        fn = os.path.expanduser("~/.aws/config")
        if os.path.exists(fn):
            ini = IniFile(fn)
        return ini
    except Exception as e:
        msg = f"Exception in findConfigFile: {type(e).__name__}: {e}"
        print(msg)
        raise


def setup(profile):
    """Returns the iam and ini objects, finds the named profile and user.

    will raise exceptions if any of that fails
    """
    try:
        ini = user = iam = xprofile = None
        print(f"awscreds {__version__}")
        ini = findConfigFile()
        if ini is not None:
            xprofile = f"profile {profile}"
            if ini.sectionExists(xprofile):
                items = ini.getSectionItems(xprofile)
                user = items["user"]
                iam = IAMUser(user, profile)
                if not iam.profileok:
                    msg = f"Failed to locate profile: {profile} in config file"
                    raise Exception(msg)
                if not iam.founduser:
                    msg = f"cannot find the 'user' key in profile {profile}"
                    raise Exception(msg)
            else:
                msg = f"profile {profile} not found in config file ~/.aws/config"
                raise Exception(msg)
        else:
            msg = "Config file not found: ~/.aws/config"
            raise Exception(msg)
        return (ini, iam, user, xprofile)
    except Exception as e:
        msg = f"Exception in setup: {type(e).__name__}: {e}"
        print(msg)
        raise


@awsk.command()
@click.argument("profile")
def awsK(profile):
    """Rotate the users access key for the named profile in the ~/.aws/config file."""
    try:
        ini, iam, user, xprofile = setup(profile)
        if (
            ini is not None
            and iam is not None
            and user is not None
            and xprofile is not None
        ):
            items = ini.getSectionItems(xprofile)
            akid = items["aws_access_key_id"]
            newkey = iam.rotateKeys(user, akid)
            # print(newkey)
            ak = newkey["AccessKey"]
            items["aws_access_key_id"] = ak["AccessKeyId"]
            items["aws_secret_access_key"] = ak["SecretAccessKey"]
            ini.updateSection(xprofile, items, True)
            print(f"""New access key id {items["aws_access_key_id"]} created.""")
    except Exception as e:
        msg = f"Exception in awsK: {type(e).__name__}: {e}"
        print(msg)


@awspw.command()
@click.option(
    "--length",
    "-l",
    default="16",
    help="overall length of the new password (default: 16)",
)
@click.argument("profile")
def awsPW(profile, length):
    """Change the users AWS Console Password for the named profile in the ~/.aws/config file."""
    try:
        ilength = int(length)
        if ilength > 32:
            ilength = 32
        if ilength < 8:
            ilength = 8
        ini, iam, user, xprofile = setup(profile)
        if (
            ini is not None
            and iam is not None
            and user is not None
            and xprofile is not None
        ):
            items = ini.getSectionItems(xprofile)
            newpw = pwgen(ilength)
            iam.changePassword(items["password"], newpw)
            print(f"""current: {items["password"]}""")
            items["password"] = newpw
            ini.updateSection(xprofile, items, True)
            print(f"new: {newpw}")
    except Exception as e:
        msg = f"Exception in awsPW: {type(e).__name__}: {e}"
        print(msg)


@genpw.command()
@click.option(
    "--length",
    "-l",
    default="16",
    help="overall length of the new password (default: 16)",
)
@click.option(
    "--nospaces",
    "-n",
    default=False,
    is_flag=True,
    help="do not put spaces in the generated password. Default is to chunk the new password into blocks of 4 characters, seperated by spaces.",
)
def genPW(length, nospaces):
    """Generate a new password of `length` characters. (limited to between 8 and 32 - default is 16)."""
    try:
        ilength = int(length)
        if ilength > 32:
            ilength = 32
        if ilength < 8:
            ilength = 8
        newpw = pwgen(ilength)
        if nospaces:
            print(newpw.replace(" ", ""))
        else:
            print(newpw)
    except Exception as e:
        msg = f"Exception in genPW: {type(e).__name__}: {e}"
        print(msg)
