# SuperCollider bridge module
# By Mathias Bredholt

import webbrowser
# from sclib import *
# from string import Template
import parser

pytab = "{}:"
sctab = "(),"

# lib = {
#     'lfo': {
#         'type': 'ugen',
#         'args_key': ('freq', 'from', 'to', 'phase'),
#         'args_val': (1, 0, 1, 0),
#         'scl_str': Template('SinOsc.kr($freq, $phase).range($from, $to)')
#     },
#     'aenv': {
#         'type': 'ugen',
#         'args_key': ('attack', 'decay', 'mul', 'add'),
#         'args_val': (0.05, 1, 1, 0),
#         'scl_str':
#         Template('EnvGen.kr(Env.perc($attack, $decay), 1, $mul, $add, 1, 2)')
#     },
#     'env': {
#         'type': 'ugen',
#         'args_key': ('attack', 'decay', 'mul', 'add'),
#         'args_val': (0.05, 1, 1, 0),
#         'scl_str':
#         Template('EnvGen.kr(Env.perc($attack, $decay), 1, $mul, $add, 1, 0)')
#     },
#     'lpf': {
#         'type': 'ugen',
#         'args_key': ('input', 'freq', 'q'),
#         'args_val': (0, 440, 1),
#         'scl_str': Template('RLPF.ar($input, $freq, $q)')
#     },
#     'del': 'CombC.ar({0}, {1}, {2}, {3}, {4}, {5})',
#     'sinosc': {
#         'type': 'ugen',
#         'args_key': ('freq', 'phase', 'mul', 'add'),
#         'args_val': (440, 0, 1, 0),
#         'scl_str': Template('SinOsc.ar($freq, $phase, $mul, $add)')
#     },
#     'saw': {
#         'type': 'ugen',
#         'args_key': ('freq', 'mul', 'add'),
#         'args_val': (440, 1, 0),
#         'scl_str': Template('Saw.ar($freq, $mul, $add)')
#     }
# }


def run():
    while True:
        prompt = input('PySc> ')
        if prompt == 'start':
            sclang()
        elif prompt == '.':
            stop()
        elif 'play' in prompt:
            prompt = prompt[5:]
            cmd('{' + parser.parse_ugen(prompt) + '.dup}.play')
        elif 'add' in prompt:
            prompt = prompt[5:]
            addInstr()
        elif prompt != '':
            print('I don\'t understand')
            # print(parse_cmd(prompt))

            # def parse_paren(string):
            #     stack = []
            #     for i, c in enumerate(string):
            #         if c == '(':
            #             stack.append(i)
            #         elif c == ')' and stack:
            #             start = stack.pop()
            #             # yield (len(stack), string[start + 1:i])
            #             yield [string[start + 1:i], start + 1, i]
            #
            #
            # def parse_nested(groups):
            #     if len(groups) > 1:
            #         from_i = groups[0][1] - groups[1][1]
            #         to_i = groups[0][2] - groups[1][2]
            #         sub_string = groups[0][0]
            #         parsed_string = parse_keyword(sub_string)
            #         groups[1][0] = groups[1][0][:from_i
            #                                     ] + parsed_string + groups[1][0][to_i:]
            #         groups.pop(0)
            #         parse_nested(groups)
            #     else:
            #         groups[0][0] = parse_keyword(groups[0][0])
            #
            #
            # def parse_keyword(string):
            #     values = re.findall(r'[0-9]*\.[0-9]+|\w+|\(.*\)', string)
            #     for val in values:
            #         if val in lib:
            #             keyword = val
            #             index = values.index(val)
            #     return format_scl_str(keyword, index, values)
            #
            #
            # def parse_cmd(string):
            #     groups = list(parse_paren(string))
            #     groups.append([string, 0, len(string)])
            #     parse_nested(groups)
            #     return groups[0][0]
            #
            #
            # def format_scl_str(keyword, index, values):
            #     args_key = list(lib[keyword]['args_key'])
            #     args_val = list(lib[keyword]['args_val'])
            #     for i in range(0, len(args_key)):
            #         if index + i + 1 < len(values):
            #             args_val[i] = values[index + i + 1]
            #     args = dict(zip(args_key, args_val))
            #     return lib[keyword]['scl_str'].substitute(args)


def cmd(str):
    proc.stdin.write(str + "\n")
    print(procio.process_input(proc, queue, thread, 0.5))

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
