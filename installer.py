# Installer for run
# WARNING! UNTESTED!
print("this installer is untested! are you sure you want to continue?")
c=input()
if c!="y":
    print("""Manual installation instructions:
1. install MSVC C++ 2022 compiler tools
2. execute pip install setuptools g4f colorama shellingham pyinstaller
3. run pyinstaller main.py
4. copy all of dist's files to where you want to install
5. rename main.exe to run.exe
6. (optional but recommended) add folder to path""")
    sys.exit(1)
print("run installer")
import subprocess, sys, os
print("checking for MSVC C++ 2022 compiler tools")
# check if C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat exists
try:
    f=open("C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvars64.bat")
    exists=True
except:
    exists=False
if not exists:
    print("Please install it to install the required dependencies. Exiting.")
    sys.exit(1)
print("installing required dependencies")
subprocess.run("pip install setuptools", shell=True)
subprocess.run("pip install g4f", shell=True)
subprocess.run("pip install colorama", shell=True)
subprocess.run("pip install shellingham", shell=True)
subprocess.run("pip install pyinstaller", shell=True)
p=input("where to install? ")
p=os.path.abspath(p)
# make directory if not exists
if not os.path.exists(p):
    os.makedirs(p)
# use pyinstaller to build main.py
subprocess.run("pyinstaller main.py", shell=True)
# move all of dist's contents to p
import shutil
import os

# Move all of dist's contents to p
dist_path = os.path.join(os.getcwd(), "dist")
for item in os.listdir(dist_path):
    item_path = os.path.join(dist_path, item)
    destination_path = os.path.join(p, item)
    shutil.move(item_path, destination_path)