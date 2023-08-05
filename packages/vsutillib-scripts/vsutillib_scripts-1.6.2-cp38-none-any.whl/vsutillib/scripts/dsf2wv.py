#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compress DSF files into WavPack

DSD format is preserved
"""

import argparse
import sys
import shlex

from pathlib import Path

from vsutillib import config
from vsutillib.process import RunCommand
from vsutillib.files import getFileList, getDirectoryList, getExecutable

VERSION = config.SCRIPTS_VERSION

__version__ = VERSION


class Files:  # pylint: disable=too-few-public-methods
    """
    utility class
    """

    total = 0
    count = 0
    noMatch = []


def parserArguments():
    """construct parser"""

    parser = argparse.ArgumentParser(
        description="compress dsf audio file to WavPack container"
    )

    parser.add_argument("directory", nargs="+", help="enter directory to process")
    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="just print commands"
    )
    parser.add_argument(
        "-o",
        "--onlycurrentdir",
        action="store_true",
        default=False,
        help="don't proccess subdirectories",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="increase verbosity"
    )
    parser.add_argument("-c", "--command", help="command to apply")
    parser.add_argument(
        "-l",
        "--logfile",
        action="store",
        default="dsf2wv.txt",
        help="file to log output",
    )
    parser.add_argument(
        "-w",
        "--wildcard",
        action="store",
        default="*.dsf",
        help="wildcard to select files to process",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)

    return parser


def printToConsoleAndFile(oFile, msg):
    """print to console and write to logfile"""
    if oFile:
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

    lFile = Path(logFileName)

    if Path(lFile.parent).is_dir():
        lFile.touch(exist_ok=True)
    else:
        # cannot create log file
        # on command line
        lFile = Path("dsf2wv.txt")
        lFile.touch(exist_ok=True)

    return lFile


def verifyDirectories(args, logFile):
    """
    Verify that the directories in the argument are valid
    and expand wildcards on directory specified
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


def dsf2wv():
    """Main"""

    executable = getExecutable("wavpack")

    if not executable:
        print("The wavpack program not found in path.")
        return (-1)

    command = "wavpack -y --import-id3 --allow-huge-tags"

    args = parserArguments().parse_args()

    logFile = setLogFile(args.logfile).open(mode="wb")

    msg = "Current directory {}\n".format(str(Path.cwd()))
    printToConsoleAndFile(logFile, msg)

    if not verifyDirectories(args, logFile):
        return

    processLine = None
    if args.verbose:
        processLine = sys.stdout.write

    cli = RunCommand(
        regexsearch=[
            r"created (.*?) in.* (.*?)%",
            r"sor.\W(.*?) Version (.*)\r",
            r"temp file (.*?) to (.*)!",
        ],
        processLine=processLine,
    )

    workFiles = Files()

    for d in args.directory:

        msg = "Working in \n\nDirectory: [{}]\nWildcard:  {}\n\n".format(
            str(Path(d).resolve()), args.wildcard
        )
        printToConsoleAndFile(logFile, msg)

        filesList = getFileList(
            d, wildcard=args.wildcard, fullpath=True, recursive=not args.onlycurrentdir
        )

        workFiles.total = len(filesList)
        workFiles.count = 0
        workFiles.noMatch = []

        for of in filesList:

            f = str(of)

            cliCommand = command + " " + shlex.quote(f)
            cli.command = cliCommand

            msg = "Processing file [{}]\n".format(f)
            printToConsoleAndFile(logFile, msg)

            if args.debug:

                msg = "Command: {}\n\n".format(cliCommand)
                printToConsoleAndFile(logFile, msg)

            else:

                cli.run()

                version = ""
                if fc := cli.regexmatch[1]:
                    version = "WavPack {} Version {} ".format(fc[0], fc[1])

                if fc := cli.regexmatch[0]:
                    if len(fc) == 2:
                        msg = "{}created file [{}] at {}% compression\n\n".format(
                            version, fc[0], fc[1]
                        )
                        printToConsoleAndFile(logFile, msg)
                        workFiles.count += 1
                    else:
                        workFiles.noMatch.append(f)

                if cli.output:
                    for line in cli.output:
                        logFile.write(line.encode())
                    logFile.write("\n\n".encode())

        if workFiles.count != workFiles.total:
            msg = "Bummer.."
            for f in workFiles.noMatch:
                msg = "Check file '{}'\n".format(f)
                logFile.write(msg.encode())


if __name__ == "__main__":
    dsf2wv()
