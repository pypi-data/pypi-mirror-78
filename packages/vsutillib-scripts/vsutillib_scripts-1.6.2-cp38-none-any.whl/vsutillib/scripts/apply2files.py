#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply a CLI command to all files in a directory
and subdirectory

User has control to select what wiles with
wildcards also to run on subdirectories or not

ie.
python -m apply2files -c wavpack -a '-y --import-id3 --allow-huge-tags' -w '*.dsf' .

Raises:
    ValueError: [description]

Returns:
    [type] -- [description]
"""
import argparse
import sys
import shlex
from pathlib import Path

from vsutillib import config
from vsutillib.process import RunCommand
from vsutillib.files import getFileList, getDirectoryList

VERSION = config.SCRIPTS_VERSION

__version__ = VERSION

def parserArguments():
    """construct parser"""

    parser = argparse.ArgumentParser(
        description=(
            "apply commnad 'COMMAND' to all files "
            "found in directory is recursive by default"
        )
    )

    parser.add_argument("directory", nargs="+", help="enter directory to process")
    parser.add_argument(
        "-a",
        "--arguments",
        action="store",
        default="",
        help="optional arguments pass to command before file",
    )
    parser.add_argument(
        "-p",
        "--append",
        action="store",
        default="",
        help="optional arguments pass to command after file",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="just print commands"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="increase verbosity"
    )
    parser.add_argument(
        "-c", "--command", action="store", default="", help="command to apply"
    )
    parser.add_argument(
        "-l",
        "--logfile",
        action="store",
        default="",
        help="file to log output",
    )
    parser.add_argument(
        "-w",
        "--wildcard",
        action="store",
        default="*",
        help="wildcard to select files to process",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-o",
        "--onlycurrentdir",
        action="store_true",
        default=False,
        help="don't proccess subdirectories",
    )
    group.add_argument(
        "-s",
        "--onlysubdir",
        action="store_true",
        default=False,
        help="don't proccess current working directory",
    )

    return parser


def printToConsoleAndFile(oFile, msg):
    """print to console and write to logfile"""
    if oFile is not None:
        oFile.write(msg.encode())
    print(msg)


def setLogFile(logFileName):
    """
    Setup logging file

    Arguments:
        logFileName {str} -- name of log file

    Returns:
        Pathlib.Path -- Pathlib object logfile
    """

    if not logFileName:
        return None

    lFile = Path(logFileName)

    if Path(lFile.parent).is_dir():
        lFile.touch(exist_ok=True)
    else:
        # cannot create log file
        # on command line
        lFile = Path("commandLog.txt")
        lFile.touch(exist_ok=True)

    return lFile


def verifyDirectories(args, logFile):
    """
    Verify that the directories in the argument are valid
    """

    fCheckOk = True
    goodDirectory = []

    for d in args.directory:

        p = Path(d)

        try:
            if not p.is_dir():
                msg = "Invalid directory {}\n".format(str(p))
                printToConsoleAndFile(logFile, msg)
                fCheckOk = False
        except OSError as error:
            if wildcardDirs := getDirectoryList(d):
                for g in wildcardDirs:
                    goodDirectory.append(str(g))
                continue

            msg = error.strerror
            fCheckOk = False

        if not fCheckOk:
            msg = "\n\nInput: {}"
            msg = msg.format(d)
            printToConsoleAndFile(logFile, msg)
            raise ValueError(msg)

        goodDirectory.append(d)

    args.directory = goodDirectory

    return fCheckOk


def apply2files():
    """
    script to apply supplied command to file in directory
    and subdirectories if needed

    ::

        usage: apply2files.py [-h] [-a ARGUMENTS] [-d] [-o] [-v] [-c COMMAND]
                            [-l LOGFILE] [-w WILDCARD] [--version]
                            directory [directory ...]

        positional arguments:
        directory             enter directory to process

        optional arguments:
        -h, --help            show this help message and exit
        -a ARGUMENTS, --arguments ARGUMENTS
                                optional arguments pass to command before file
        -p ARGUMENTS, --append ARGUMENTS
                                optional arguments pass to command after file
        -d, --debug           just print commands
        -o, --onlycurrentdir  don't proccess subdirectories
        -v, --verbose         increase verbosity
        -c COMMAND, --command COMMAND
                                command to apply
        -l LOGFILE, --logfile LOGFILE
                                file to log output
        -w WILDCARD, --wildcard WILDCARD
                                wildcard to select files to process
        --version             show program's version number and exit

    """

    args = parserArguments().parse_args()

    logFile = None
    if args.logfile:
        logFile = setLogFile(args.logfile).open(mode="wb")

    if not args.command:
        print("Nothing to do.")
        return None

    recursive = (not args.onlycurrentdir) and (not args.onlysubdir)

    print("Recursive {} subdironly {}".format(recursive, args.onlysubdir))

    msg = "Current directory {}\n".format(str(Path.cwd()))
    printToConsoleAndFile(logFile, msg)

    if not verifyDirectories(args, logFile):
        return

    processLine = None
    if args.verbose:
        processLine = sys.stdout.write

    cli = RunCommand(processLine=processLine)

    for d in args.directory:

        msg = "Working\n\nDirectory: [{}]\nWildcard:  {}\n\n".format(
            str(Path(d).resolve()), args.wildcard
        )
        printToConsoleAndFile(logFile, msg)

        filesList = getFileList(
            d, wildcard=args.wildcard, fullpath=True, recursive=recursive
        )

        for of in filesList:

            if args.onlysubdir:
                if of.resolve().parent == Path.cwd():
                    print("By pass.")
                    continue

            f = str(of)

            qf = shlex.quote(f)

            cliCommand = (
                args.command + " " + args.arguments + " " + qf + " " + args.append
            )
            cli.command = cliCommand

            msg = "Processing file [{}]\n".format(f)
            printToConsoleAndFile(logFile, msg)

            if args.debug:

                msg = "Debug Command: {}\n\n".format(cliCommand)
                printToConsoleAndFile(logFile, msg)

            else:

                cli.run()

                if cli.output:
                    for line in cli.output:
                        logFile.write(line.encode())
                    logFile.write("\n\n".encode())

    return None


if __name__ == "__main__":
    apply2files()
