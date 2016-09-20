#!/usr/bin/env python

import os
import sys
import subprocess

def query(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    try:
        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
    except KeyboardInterrupt:
        sys.exit()

def main():
    flags = []
    files = []

    recursive = False
    force = False

    for arg in sys.argv:
        if arg == sys.argv[0]:
            continue
        elif arg.startswith("--"):
            flags.append(arg)
            if arg == "--recursive":
                recursive = True
            elif arg == "--force":
                force = True
        elif arg.startswith("-"):
            flags.append(arg)
            for c in arg[1:]:
                if c is "r" or c is "R":
                    recursive = True
                elif c is "f":
                    force = True
        else:
            files.append(os.path.expanduser(arg))

    print("Flags: " + ", ".join(flags))
    print("Files: " + ", ".join(files))

    for cfile in files:
        cfile_recursive = recursive

        if not cfile_recursive and os.path.isdir(cfile) and os.listdir(cfile):
            print("%s is a directory but the recursive flag was not set" % cfile)
            if query("Would you like to recursively remove it?"):
                cfile_recursive = True
                files.remove(cfile)

        if cfile_recursive and not force:
            if (os.path.isdir(cfile + "/.git")):
                print("Detected git repository in " + cfile)
                if query("Would you like to force remove the .git directory?", default="yes"):
                    subprocess.call(["rm"] + flags + ["--recursive", "--force", cfile + "/.git"])
                    print("Force removed %s" % cfile + "/.git")

        if cfile_recursive:
            subprocess.call(["rm"] + flags + ["--recursive", cfile])

    subprocess.call(["rm"] + flags + files)

if __name__ == '__main__':
    main()
