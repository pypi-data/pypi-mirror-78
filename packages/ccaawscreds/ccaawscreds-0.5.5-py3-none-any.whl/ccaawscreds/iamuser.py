"""IAM user module for the awscreds application."""

from datetime import datetime

import boto3
from botocore.exceptions import ProfileNotFound


class AccessKeyError(Exception):
    pass


class IAMUser:
    def __init__(self, username, profile):
        try:
            self.profileok = False
            if profile is None:
                self.client = boto3.client("iam")
                self.profileok = True
            else:
                sess = boto3.session.Session(profile_name=profile)
                self.client = sess.client("iam")
                self.profileok = True
            self.founduser = self.getUserInfo(username)
            self.newkey = None
        except ProfileNotFound as e:
            print(f"aws account profile: {profile} does not exist")
        except Exception as e:
            msg = f"Exception in IAMUser.__init__: {type(e).__name__}: {e}"
            print(msg)
            raise

    def getUserInfo(self, username):
        try:
            self.userinfo = self.client.get_user(UserName=username)["User"]
            self.userinfo["passwordage"] = self.getPasswordAge()
            return True
        except self.client.exceptions.NoSuchEntityException as e:
            print(f"user: {username} does not exist.")
            return False
        except Exception as e:
            msg = f"Exception in IAMUser.getUserInfo: {type(e).__name__}: {e}"
            print(msg)
            raise

    def getPasswordAge(self):
        try:
            passwordage = None
            lp = self.client.get_login_profile(UserName=self.userinfo["UserName"])
            if lp is not None:
                if "LoginProfile" in lp:
                    passwordage = lp["LoginProfile"]["CreateDate"]
            return passwordage
        except self.client.exceptions.NoSuchEntityException as e:
            return None
        except Exception as e:
            msg = f"Exception in IAMUser.getPasswordAge: {type(e).__name__}: {e}"
            print(msg)
            raise

    def changePassword(self, oldpw, newpw):
        """Changes the calling users password.

        Relies on boto3 raising an exception if it fails
        """
        try:
            if self.profileok and self.founduser:
                kwargs = {"OldPassword": oldpw, "NewPassword": newpw}
                pwchanged = self.client.change_password(**kwargs)
                return True
        except Exception as e:
            msg = f"Exception in IAMUser.changePassword: {type(e).__name__}: {e}"
            print(msg)
        return False

    def getKeys(self, username):
        """returns a user dict complete with registered access keys."""
        try:
            keys = self.client.list_access_keys(UserName=username)
            okeys = []
            for key in keys["AccessKeyMetadata"]:
                kid = key["AccessKeyId"]
                klu = self.client.get_access_key_last_used(AccessKeyId=kid)
                if "LastUsedDate" in klu["AccessKeyLastUsed"]:
                    key["LastUsedDate"] = klu["AccessKeyLastUsed"]["LastUsedDate"]
                    key["lastused"] = int(
                        datetime.timestamp(klu["AccessKeyLastUsed"]["LastUsedDate"])
                    )
                okeys.append(key)
            return okeys
        except Exception as e:
            msg = f"Exception in IAMUser.getKeys: {e}"
            msg += f"Failed to obtain access key information for user: {username}"
            raise Exception(msg)

    def __delete_inactive_keys(self, username):
        """If the user has an inactive key, this will delete it."""
        try:
            activekeys = 0
            keys = self.getKeys(username)
            for key in keys:
                if key["Status"] == "Inactive":
                    self.client.delete_access_key(
                        AccessKeyId=key["AccessKeyId"], UserName=username
                    )
                else:
                    activekeys += 1
            if activekeys > 1:
                raise AccessKeyError(
                    f"user {username} has more than one active access key, please delete one and try again"
                )
        except Exception as e:
            msg = f"Exception in IAMUser.__delete_inactive_keys: {e}"
            msg += f"""\nAn error occurred deleting the inactive access key: {key["AccessKeyId"]}"""
            msg += f"\nfor user {username}"
            print(msg)
            raise

    def __deactivate_key(self, username, keyid):
        """Deactivates the keyid key."""
        try:
            self.client.update_access_key(
                AccessKeyId=keyid, UserName=username, Status="Inactive"
            )
            return True
        except Exception as e:
            msg = f"Exception in IAMUser.__deactivate_key: {e}"
            msg += f"Failed to deactivate the key {keyid} for user {username}"
            print(msg)
        return False

    def __generate_new_key(self, username):
        key = False
        try:
            self.newkey = self.client.create_access_key(UserName=username)
            return True
        except Exception as e:
            msg = f"Exception in IAMUser.__generate_new_key: {e}"
            print(msg)
            raise
        return False

    def rotateKeys(self, username, ckeyid):
        """This will leave the user with a new, active key

        It first deletes any inactive key,
        then generates a new active key,
        the de-activates the original key.
        returns a dictionary of the new key:
        {'AccessKey':
            {'UserName': 'chris.allison',
            'AccessKeyId': 'AKIAXIPAILAXFADFIWPV',
            'Status': 'Active',
            'SecretAccessKey': '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',
            'CreateDate': datetime.datetime(2020, 9, 2, 16, 32, 4, tzinfo=tzutc())},
            'ResponseMetadata': {...}
        }
        """
        try:
            self.__delete_inactive_keys(username)
            # at this point we should only have one key, the current, active one
            # passed in as ckeyid param.
            self.__generate_new_key(username)
            keys = self.getKeys(username)
            if len(keys) > 0:
                for key in keys:
                    if key["AccessKeyId"] == ckeyid:
                        self.__deactivate_key(username, ckeyid)
            return self.newkey
        except Exception as e:
            msg = f"Exception in IAMUser.rotateKeys: {e}"
            print(msg)
            raise
