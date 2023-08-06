import hashlib
import os
import random

# initialise the random number generator
random.seed()


def pwgen(length=15, nospaces=False):
    # acceptable list of chars that can be capitalised
    capl = "acdefghjkmnpqrstuvwxyz"
    # list of acceptable symbols
    symbols = "=-!$%^&*(){}[]"
    # find the current directory name
    wlfn = "/".join([os.path.dirname(__file__), "wordlist.txt"])
    # read the words into a list (note: each word will still have the
    # trailing newline)
    with open(wlfn, "r") as wl:
        wlist = wl.readlines()
    # pick 4 random words from the list
    words = [word.rstrip() for word in random.choices(wlist, k=4)]
    # join the words into a phrase
    phrase = " ".join(words)
    # convert to bytes and hash into 64 chars.
    hphrase = hashlib.sha256(phrase.encode()).hexdigest()
    # pick 15 random characters from the hashed phrase
    ch = "".join(random.choices(hphrase, k=length))
    # pick a letter in the string to capitalise
    # filter out letters that are not in our acceptable list
    pos = [ch.index(c) for c in ch if c in capl]
    pi = random.choice(pos)
    # split the string apart at our chosen letter
    # capitalise the letter and re-combine the string
    left = ch[: pi - 1] if pi > 0 else ""
    c = ch[pi].upper()
    right = ch[pi + 1 :] if pi < len(ch) - 1 else ""
    pw = f"{left}{c}{right}"
    # pick a random position within that password
    # where we can insert a symbol
    pi = random.randint(0, len(pw) - 1)
    # string slicing again
    left = pw[:pi] if pi > 0 else ""
    right = pw[pi:] if pi < len(pw) - 1 else ""
    # pick a random symbol
    symbol = random.choice(symbols)
    # create the final password
    pw = f"{left}{symbol}{right}"
    # split the password into blocks of 4 chars.
    xpw = [pw[i : i + 4] for i in range(0, len(pw), 4)]
    # join them together into one string seperated by a space
    if nospaces:
        op = "".join(xpw)
    else:
        op = " ".join(xpw)
    # display our work to the world
    return op


if __name__ == "__main__":
    pwgen()
