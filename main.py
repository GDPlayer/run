# run - natural language to command line

# USAGE:
# run <command>

# example:
# $ run directory listing
# running "ls"
# ENTER - run/confirm
# BKSP - cancel
# E - explain
import g4f # for generating the command
g4f.debug.check_version=False
import sys # for grabbing command
import shellingham # for detecting shell
import platform # for detecting platform
import os # for creating config file
import configparser # for parsing config file
config=configparser.ConfigParser()
# check if platform is linux
if platform.system()=="Linux":
    if not os.path.exists('~/.config/run.config'):
        config['run']={'alwaysAccept': False}
        f=open('~/.config/run.config', 'x')
        f.close()
        with open('~/.config/run.config', 'w') as configfile:
            config.write(configfile)
    config.read('~/.config/run.config')
elif platform.system()=="Windows":
    appdata=os.getenv('APPDATA')
    if not os.path.exists(appdata+'\\run.config'):
        config['run']={'alwaysAccept': False}
        with open(appdata+'\\run.config', 'w') as configfile:
            config.write(configfile)
    config.read(appdata+'\\run.config')
# config['run']['alwaysAccept'] - whether to automatically run the command
if platform.system() == "Windows":
    import msvcrt as getch
else:
    import getch 
from colorama import Fore, Back, Style # for coloring output
import subprocess # for running command
if len(sys.argv) > 1:
    command = sys.argv[1:]
else:
    print("Usage: run <command>")
    sys.exit(1)
try:
    sh = shellingham.detect_shell()[0]
except:
    if platform.system() == "Windows":
        sh = "cmd"
    else:
        sh = "bash"
print("generating command...")
def ask(question):
    return g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role":"user","content":question}],
        provider=g4f.Provider.Bing,
    )
generatedCommand=ask("[[convert this string to command line for shell "+sh+", for platform "+platform.system()+", [[no extra text, no codeblock, no explanation, no markdown, no introduction]], this will be automatically run, so there should be no extra text or explanation]]: "+" ".join(command))
running=True
def run(*command):
    subprocess.run("".join(command), shell=True)
    running=False
def explain(*command):
    print("generating explanation...")
    print(ask("explain the command, for shell "+sh+", for platform "+platform.system()+",[[[[no introduction of self, just explain the command]]]], also no markdown since this is in a console, make your response short :) and space it out using newlines: "+generatedCommand)+"\n")
while running:
    print(Style.BRIGHT+"running \""+generatedCommand+"\""+Style.RESET_ALL)
    if config["run"]["alwaysAccept"]=="False":
        print(Style.BRIGHT+Fore.GREEN+"enter"+Style.RESET_ALL+" - run/confirm")
        print(Style.BRIGHT+Fore.RED+"backspace"+Style.RESET_ALL+" - cancel")
        print(Style.BRIGHT+Fore.YELLOW+"e"+Style.RESET_ALL+" - explain")
        char=ord(getch.getch())
        if char==13:
            run(generatedCommand)
            running=False
        elif char==101:
            explain(generatedCommand)
        else:
           running=False
    else:
        run(generatedCommand)
        running=False