#!C:\Python3\python.exe

import BSParser
import os
import re
import subprocess
import urllib.request
import sys


# Get the name of the package.
def getPackageName(link):
    regex = re.compile(r'\w{9}%\d{2}\w{6}-\d{2}_\d{1,2}_\d{1,2}-\d{1,5}.\w{3}')
    matches = re.findall(regex, link)
    return matches[0].replace("%20", "_")


# Progress Bar WannaBe for downloading the package.
def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r" + packageName + " > %d%%" % percent)
    sys.stdout.flush()


# Kill bsp process if open.
def kill_bspProcess():
    if b'bsp.exe' in subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0]:
        os.system("taskkill /F /im bspsh.exe")
        os.system("taskkill /F /im bsp.exe")
    else:
        print('\nSKIP: The process "bsp.exe" not found.\n')


# Install Log.
def log():
    logName = packageName.replace(".msi", "_Install.log")
    return logName


# Call System REBOOT
def reboot():
    try:
        os.system("shutdown.exe /f /r /t 0")
    except WindowsError as rebootError:
        print(rebootError)


# Install package
def install(package):
    if BSParser.args.log is True:
        try:
            os.system("msiexec /i {} /qn /l*v {}".format(package, log()))
        except WindowsError as installError:
            print(installError)
    elif BSParser.args.log is False:
        try:
            os.system("msiexec /i %s /qn" % package)
        except WindowsError as installError:
            print(installError)


# Clean leftovers.
def clean():
    print("Start cleaning...")
    try:
        os.system("del /F *.msi")
    except Exception as cleanError:
        print(cleanError)


# Run BSP dedication script.
def dedicate():
    try:
        cmdline = r'"C:\Program Files (x86)\BroadSign\bsp\bin\bsp_dedicate.exe"'
        os.system(cmdline + " --dedicate")
    except Exception as dedicationError:
        print(dedicationError)


def run_script():
    kill_bspProcess()
    install(packageName)
    if BSParser.args.dedicate is True:
        dedicate()

    if BSParser.args.clean is True:
        clean()

    if BSParser.args.reboot is True:
        reboot()

packageName = getPackageName(BSParser.args.url)
urllib.request.urlretrieve(BSParser.args.url, packageName, reporthook=dlProgress)
run_script()
