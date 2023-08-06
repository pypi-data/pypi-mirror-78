#!/usr/bin/env python3
import os
import re
import sys
import argparse
from pprint import pprint

__version__ = '0.1.0'


class NotImplementedAction(argparse.Action):
    """ This class allows to work on getting your Argparse object
    ready even if nothing useful happens when used.

    Usage:
    Just set action=NotImplementedAction when calling add_argument, like this:

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--missing",
                        help="This will do something in the future",
                        action=NotImplementedAction)

    GIST URL: https://gist.github.com/buanzo/2a004348340ef79b0139ab38f719cf1e
    """
    def __call__(self, parser, namespace, values, option_string=None):
        msg = 'Argument "{}" still not implemented.'.format(option_string)
        sys.exit(msg)


def printerr(msg):
    print("{}".format(msg), file=sys.stderr)


def pprinterr(o):
    pprint(o, stream=sys.stderr)


def valueOrDefault(o, k, d):
    # This function tries to find a key
    # or an attribute named k.
    # If it finds either, it returns d.
    if isinstance(o, dict):
        if k in o.keys():
            return(o[k])
    try:
        r = getattr(o, k)
    except AttributeError:
        return(d)
    return(r)


def envOrDefault(v, d):
    # return the contents of an env var 'v'
    # or default d.
    ov = os.environ.get(v)
    if ov is None:
        return(d)
    else:
        return(str(ov).strip())


def is_valid_hostname(hostname):
    # https://stackoverflow.com/a/33214423
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False
    labels = hostname.split(".")
    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False
    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


if __name__ == '__main__':
    printerr('You are not supposed to call this script directly.')
    printerr('Use:\n\tfrom buanzobasics import printerr,pprinterr\n')
