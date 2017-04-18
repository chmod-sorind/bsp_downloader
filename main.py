#!C:\Python35\python.exe

import argparse
import os
import re
import subprocess
import urllib.request
import sys
import time


# Arguments
parser = argparse.ArgumentParser(description='Download specified package from link/URL and installs it.')
parser.add_argument('url', metavar='URL', type=str, help='The Link/URL to target package.')
parser.add_argument('process', metavar='URL', type=str, help='Target Package is BSP.')
parser.add_argument('-l', action='store_true', help='Create Install Log.')
parser.add_argument('-r', action='store_true', help='Reboot after install.')
args = parser.parse_args()


# Get the name of the package.
def getPackageName(link):
    regex = re.compile(r'\w{9}\%\d{2}\w{6}-\d{2}_\d{1,2}_\d{1,2}-\d{1,5}.\w{3}')
    matches = re.findall(regex, link)
    return matches[0].replace("%20", "_")


getPackageName(args.url)
packageName = getPackageName(args.url)


def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r" + packageName + " > %d%%" % percent)
    sys.stdout.flush()


urllib.request.urlretrieve(args.url, packageName, reporthook=dlProgress)
print(" \n")


# Kill bsp process if open.
# ToDo: Call this function somewhere. Currently not called so the script wont work.
def kill_process():
    process = args.process
    if process == 'bsp':
        if b'bsp.exe' in subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0]:
            os.system("taskkill /F /im bspsh.exe")
            os.system("taskkill /F /im bsp.exe")
            print('"SUCCESS: The process "bsp.exe" with has been terminated."')
        else:
            print('\nSKIP: The process "bsp.exe" not found.\n')


# Install Log.
# ToDo: Call this function. Currently not working.
def log():
    logName = packageName.replace(".msi", "_Install.log")
    return logName


# Install package
# askForLog = input('Generate a install log? (Yes/No) \n')
# ToDo: Replace asking for logs function with optional parameter -l
askForLog = "yes"
if askForLog.lower() in ('y', 'yes'):
    try:
        os.system("msiexec /i {} /qn /l*v {}".format(packageName, log()))
    except WindowsError as e:
        print(e)
elif askForLog.lower() in ('n', 'no'):
    print('Cool, No logs then..')
    try:
        os.system("msiexec /i %s /qn" % packageName)
    except WindowsError as e:
        print(e)
print("Installation Done!\n")
print("Start cleaning...")
os.system("del /F *.msi")
print("Done!\n")
print("Dedicate the player...\n")
cmdline = r'"C:\Program Files (x86)\BroadSign\bsp\bin\bsp_dedicate.exe"'
os.system(cmdline + " --dedicate")
print("\nSuccessfully setup dedicatet player.")

askRestart = input("Reboot the System? (Yes/No) \n")
if askRestart.lower() in ('y', 'yes'):
    try:
        print("System is now restarting.\n")
        time.sleep(1)
        os.system("shutdown.exe /f /r /t 0")
    except WindowsError as e:
        print(e)
elif askRestart.lower() in ('n', 'no'):
    print("Lame..")

print("Script done... ")
