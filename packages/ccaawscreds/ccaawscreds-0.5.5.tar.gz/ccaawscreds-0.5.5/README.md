# ccaawscreds
Command line commands, `awskey` and `awspw`, to change your AWS credentials.

Command `genpw` to generate arbitray passwords using the password generator.

These tools will only work with credentials stored in the ~/.aws/config file,
not in the ~/.aws/credentials file.

AWS Config format is:

```
[profile profile-name]
aws_access_key_id = AKIA....
aws_secret_access_key = ....
```

These tools use 2 extra keys for each section in the config file: `user` and
`password` i.e.

```
[profile profile-name]
aws_access_key_id = AKIA....
aws_secret_access_key = ....
user = chris.allison
password = anythIng you W@ant
```

Both of these commands rely on the entries in the config file, if one of the
items is missing they will fail.

Note: though the AWS Config file format requires that each profile section has
`profile ` prepended to the name, there is no need to type that when referencing
it, both these tools, boto3 and the AWS CLI look for just the bare profile name
without the word `profile` prepended (see the examples below).


## awspw
This command will change the users password in the named profile, storing the
new password back into the config file and also displaying it to the screen
along with the old password.  The password generator can be optionally
configured to return passwords of a certain length.  It also splits the
generated password into blocks of 4 characters seperated by spaces, as AWS
allows spaces in passwords.

### Example awspw
```
$ awspw -l 32 sadmin-static
awscreds 0.2.3
current: 98b8 8d89 7e82 9bec 2)05 1e14 a8Fb a0e9
new: d96d 21fd A816 2762 a[19 81e3 cc52 2af9
$
```

## awskey
This command rotates the users access key for the named profile.  It will first
delete any inactive keys, then generate a new one, storing it in the config
file. Lastly, it deactivates the old, active key.

If you have 2 active aws keys, this command will fail, delete or deactivate one
of them and try again.

### Example awskey
```
$ awskey sadmin-static
awscreds 0.2.3
New access key id AKIAXxxxxxxxxxxxxxxx created.
$
```

## genpw
This command will generate an arbitrary password and display it.  It uses the
password generator with the same limits as above (between 8 and 32 characters,
default being 16).  It can optionally remove all the spaces from the password.

The password generator works by selecting 4 random words from a list, hashing
them with the sha256 function, randomly selecting characters from the resulting
string up to the required length. It will then insert a random non-alphabetic
character into a random position in the string, and then switch one of the
alphabetic characters to upper-case.  This should be enough for most password
policies.

There is also a list of characters that will not appear in the password to avoid
misinterpretation, they are `bBiIlLoO` so a `0` in the output is definitely a
zero not a capital `o`, simarlarly, a '1' in the output is definitely a one not
a lower case L.

### Example genpw
```
$ genpw -l 32
ca4b 4dac 74bb d^1c 2b2F 0d2e 8b4d 264c

$ genpw -l 10 -n
149388^34A
```
