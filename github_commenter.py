#!/usr/bin/env python3

from __future__ import with_statement

import sys
import os
import logging
import json



_moduleLogger = logging.getLogger(__name__)


def _parse_options(args):
    import optparse
    parser = optparse.OptionParser("usage: %prog [options] TOKEN FILE REPO UPLOAD PULL_REQUEST")

    # Setup parser
    parser.add_option(
        "-t", "--token",
        dest="token",
        metavar="TOKEN",
        help="Github Access token needed to perform write operations"
    )
    parser.add_option(
        "-f", "--file-path",
        dest="filePath",
        metavar="FILE",
        help="Path to the local file you want to upload"
    )
    parser.add_option(
        "-r", "--repo",
        dest="repo",
        metavar="REPO",
        help="Github Repository where file should be uploaded to"
    )
    parser.add_option(
        "-u", "--upload-path",
        dest="upload",
        metavar="UPLOAD",
        help="Path to file location relative to the repo rootwhen it is uploaded onto the repo."
    )
    parser.add_option(
        "-p", "--pull-request",
        dest="pullRequest",
        metavar="PULL_REQUEST",
        help="Github link to pull request."
    )

    debugGroup = optparse.OptionGroup(parser, "Debug")
    debugGroup.add_option(
        "-v", "--verbose",
        action="count", dest="verbosity", default=0,
        help="Turn on verbose output. (Useful if you really care to see what the tool is doing at all times.)"
    )
    debugGroup.add_option(
        "-q", "--quiet",
        action="count", dest="quietness", default=0,
        help="Don't print anything to the module logger."
    )
    debugGroup.add_option(
        "--test",
        action="store_true", dest="test", default=False,
        help="Run doctests then quit."
    )
    parser.add_option_group(debugGroup)

    (options, args) = parser.parse_args(args)

    # We want to default to WARNING
    # Quiet should make us only show CRITICAL
    # Verbosity gives us granularity to control past that
    verbosity = 2 + (2 * options.quietness) - options.verbosity
    loggingLevel = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL,
    }.get(verbosity, None)
    if loggingLevel is None:
        parser.error("Unsupported verbosity: %r" % verbosity)

    # Perform validation on results
    if options.test:
        return options, loggingLevel

    if args:
        parser.error("Positional arguments are not supported: %r" % (args, ))

    if options.inputPath is None or not os.path.exists(options.inputPath):
        parser.error("Input file does not exist: %r" % options.inputPath)

    return options, loggingLevel


def main(args):
    options, loggingLevel = _parse_options(args)

    logFormat = '(%(asctime)s) %(levelname)-5s %(name)s.%(funcName)s: %(message)s'
    logging.basicConfig(level=loggingLevel, format=logFormat)

    if options.test:
        import doctest
        print(doctest.testmod())
        return


    return 0


if __name__ == "__main__":
    retCode = main(sys.argv[1:])
    sys.exit(retCode)
