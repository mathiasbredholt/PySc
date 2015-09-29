# SuperCollider bridge module
# By Mathias Bredholt

import procio
import webbrowser
from sclib import *

pytab = "{}:"
sctab = "(),"

SYNTH_INDEX = 0


def sclang():
    sclangPath = "/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/sclang"
    print("Starting sclang...")
    global proc
    global queue
    global thread
    proc, queue, thread = procio.run(sclangPath)
    print(procio.process_input(proc, queue, thread, 10))
    cmd("s.makeGui")


def cmd(str):
    proc.stdin.write(str + "\n")
    # procio.process_input(proc, queue, thread, 0.1, True)
    print(procio.process_input(proc, queue, thread, 1))

# def kill():
#     proc.kill()


def demo():
    cmd("Pbind(\instrument,\default,\
    \midinote,Pseq([60, 64, 67, 71], inf)).play")


def stop():
    cmd("CmdPeriod.run")


def pysc(code):
    code = code.translate(str.maketrans(pytab, sctab)).replace(
        "'<", "").replace(">'", "").replace("<", "").replace(">", "")
    print(code)
    cmd(code)


def output():
    print(proc.stdout.readline())


def help(which):
    webbrowser.open("http://doc.sccode.org/Classes/{}.html".format(which))


# Synths and nodes
def play(name, **kwargs):
    cmd("~{} = Synth({})".format(name.strip("\\"), name))


def stopNode(name):
    cmd("~{}.free".format(name.strip("\\")))


def addInstr(ugen, out=0, **kwargs):
    global SYNTH_INDEX
    name = '\\pysc' + str(SYNTH_INDEX)
    SYNTH_INDEX += 1
    argument_list = ""
    if kwargs:
        argument_list += "arg "
        for key, value in kwargs.items():
            argument_list += "{}={},".format(key, value)
        argument_list = argument_list[:-1] + ";"
    cmd(r"SynthDef({},{{{} Out.ar({},{}.dup)}}).add;".format(
        name, argument_list, out, ugen))
    return name


def pattern(name, params):
    result = ""
    for key, value in params.items():
        result += "{}, {},".format(key, value)
    cmd("Pdef(\\{},Pbind({})).play(quant:-1)".format(name, result[:-1]))


def setTempo(tempo):
    cmd("TempoClock.default.tempo = {}".format(tempo / 60))
