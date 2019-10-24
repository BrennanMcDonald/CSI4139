from pathlib import Path
from os import listdir
from os.path import isfile, join
import sys
import os
import hashlib
import itertools


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
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

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def recursiveDir(dir, files):
    p = Path(dir)
    files.update(buildFiles(dir))
    dirs = [x.name for x in p.iterdir() if x.is_dir()]
    for iter_dir in dirs:
        files.update(recursiveDir(dir + "/" + iter_dir, files))
    return files


def printInCurrentDir(dirs):
    for dir in dirs:
        print(dirs)

def buildFiles(dir):
    files = []
    for file in [os.getcwd() + "/" + dir + "/" + f for f in listdir(dir) if isfile(join(dir, f))]:
        files.append(file)
    return files

def compareAgainstVirus(fname, byteList):
    with open(fname, "rb") as f:
      b = f.read()
      for byteset in byteList:
        if (bytes(byteset, 'UTF-8') in b):
              return True,fname
      return False,""

def cypherBump(input, i):
    return "".join(list(map(lambda x: chr((ord(x)+i) % 122), input)))

def encrypt(text, s):
    result = ""
    for char in text:
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


if __name__ == "__main__":
    virusDict = set([])
    if (sys.argv[1] == "" or sys.argv[1] == None):
        print("Please enter a path to scan.")
        print("antivirus.py [path] [virus_list]")
        exit()
    if (sys.argv[2] == "" or sys.argv[2] == None):
        print("Please enter a virus list to scan against.")
        print("antivirus.py [path] [virus_list]")
        exit()
    virus_file = open(sys.argv[2])
    virus_list = list(map(lambda x: x.replace(
        "\n", ""), virus_file.readlines()))
    for virus in virus_list:
        virusDict.add(virus)
        virusDict.update([encrypt(virus,i) for i in range(26)] + [virus])
    file_list = recursiveDir(sys.argv[1],set([]))
    print("Scanning " + str(len(file_list)) + " files")
    suspicious = []
    for file in file_list:
          b,file = compareAgainstVirus(file,virusDict)
          if (b):
            suspicious.append(file)
    print("The following files are suspicious:")
    for file in suspicious:
          print(file)
    quarentine = query_yes_no("Would you like to quarentine?", "yes")
    if(quarentine):
      os.mkdir(os.getcwd() + "/quar/")
      for file in suspicious:
        os.rename(file, os.getcwd() + "/quar/" + file.split("/")[-1])
