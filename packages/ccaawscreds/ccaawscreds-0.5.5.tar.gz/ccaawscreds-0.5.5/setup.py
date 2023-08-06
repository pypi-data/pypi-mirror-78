# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccaawscreds']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.48,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['awskey = ccaawscreds.credentials:awsK',
                     'awspw = ccaawscreds.credentials:awsPW',
                     'genpw = ccaawscreds.credentials:genPW']}

setup_kwargs = {
    'name': 'ccaawscreds',
    'version': '0.5.5',
    'description': 'update AWS console PW, rotate Access Keys, generate random passwords.',
    'long_description': "# ccaawscreds\nCommand line commands, `awskey` and `awspw`, to change your AWS credentials.\n\nCommand `genpw` to generate arbitray passwords using the password generator.\n\nThese tools will only work with credentials stored in the ~/.aws/config file,\nnot in the ~/.aws/credentials file.\n\nAWS Config format is:\n\n```\n[profile profile-name]\naws_access_key_id = AKIA....\naws_secret_access_key = ....\n```\n\nThese tools use 2 extra keys for each section in the config file: `user` and\n`password` i.e.\n\n```\n[profile profile-name]\naws_access_key_id = AKIA....\naws_secret_access_key = ....\nuser = chris.allison\npassword = anythIng you W@ant\n```\n\nBoth of these commands rely on the entries in the config file, if one of the\nitems is missing they will fail.\n\nNote: though the AWS Config file format requires that each profile section has\n`profile ` prepended to the name, there is no need to type that when referencing\nit, both these tools, boto3 and the AWS CLI look for just the bare profile name\nwithout the word `profile` prepended (see the examples below).\n\n\n## awspw\nThis command will change the users password in the named profile, storing the\nnew password back into the config file and also displaying it to the screen\nalong with the old password.  The password generator can be optionally\nconfigured to return passwords of a certain length.  It also splits the\ngenerated password into blocks of 4 characters seperated by spaces, as AWS\nallows spaces in passwords.\n\n### Example awspw\n```\n$ awspw -l 32 sadmin-static\nawscreds 0.2.3\ncurrent: 98b8 8d89 7e82 9bec 2)05 1e14 a8Fb a0e9\nnew: d96d 21fd A816 2762 a[19 81e3 cc52 2af9\n$\n```\n\n## awskey\nThis command rotates the users access key for the named profile.  It will first\ndelete any inactive keys, then generate a new one, storing it in the config\nfile. Lastly, it deactivates the old, active key.\n\nIf you have 2 active aws keys, this command will fail, delete or deactivate one\nof them and try again.\n\n### Example awskey\n```\n$ awskey sadmin-static\nawscreds 0.2.3\nNew access key id AKIAXxxxxxxxxxxxxxxx created.\n$\n```\n\n## genpw\nThis command will generate an arbitrary password and display it.  It uses the\npassword generator with the same limits as above (between 8 and 32 characters,\ndefault being 16).  It can optionally remove all the spaces from the password.\n\nThe password generator works by selecting 4 random words from a list, hashing\nthem with the sha256 function, randomly selecting characters from the resulting\nstring up to the required length. It will then insert a random non-alphabetic\ncharacter into a random position in the string, and then switch one of the\nalphabetic characters to upper-case.  This should be enough for most password\npolicies.\n\nThere is also a list of characters that will not appear in the password to avoid\nmisinterpretation, they are `bBiIlLoO` so a `0` in the output is definitely a\nzero not a capital `o`, simarlarly, a '1' in the output is definitely a one not\na lower case L.\n\n### Example genpw\n```\n$ genpw -l 32\nca4b 4dac 74bb d^1c 2b2F 0d2e 8b4d 264c\n\n$ genpw -l 10 -n\n149388^34A\n```\n",
    'author': 'ccdale',
    'author_email': 'chris.charles.allison@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/ccaawscreds',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
