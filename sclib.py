import procio

instr = '\instrument'
midi = '\midinote'
inf = 'inf'

LFOsin = 0

__sclang_running__ = False


def seq(li, rep):
    return 'Pseq({},{})'.format(li, rep)


def out(bus, ugen):
    return 'Out.ar({}, {})'.format(bus, ugen)

# Ugens


# Generators
def sinosc(freq=440, phase=0, mul=0.5, add=0):
    return 'SinOsc.ar({}, {}, {}, {})'.format(freq, phase, mul, add)


def saw(freq=440, mul=0.5, add=0):
    return 'Saw.ar({}, {}, {})'.format(freq, mul, add)


def pwm(freq=440, pulsewidth=0.5, mul=0.5, add=0):
    return 'Pulse.ar({}, {}, {}, {})'.format(freq, pulsewidth, mul, add)


def noise(mul=1, add=0):
    return 'WhiteNoise.ar({}, {})'.format(mul, add)


# Filters
def lpf(input, freq=1000, rq=0.82):
    return 'BLowPass4.ar({}, {}, {})'.format(input, freq, rq)


# Envelopes
def aenv(attack=0.05, decay=1, mul=1, add=0):
    return 'MulAdd.new(EnvGen.ar(Env.perc({}, {}), doneAction:2), {}, {})'.format(
        attack, decay, mul, add)


def env(attack=0.05, decay=1, mul=1, add=0):
    return 'EnvGen.kr(Env.perc({}, {}), levelScale: {}, levelBias: {}, doneAction:0)'.format(
        attack, decay, mul, add)


def mix(*args, amp=1):
    return 'MulAdd.new(Mix.new([{}]), {})'.format(", ".join(args), amp)


def inbus(bus, channels, mul=1, add=0):
    return 'MulAdd.new(In.ar({}, {}), {}, {})'.format(bus, channels, mul, add)


def delay1(input=0, max=0.2, time=0.2, decay=1, mul=1, add=0):
    return 'CombC.ar({}, {}, {}, {}, {}, {})'.format(input, max, time, decay,
                                                     mul, add)


def lfo(wave=0, freq=1, from_val=0, to_val=1, phase=0):
    if wave == LFOsin:
        return 'SinOsc.kr({}, {}).range({}, {})'.format(freq, phase, from_val,
                                                        to_val)


def random(from_val, to_val):
    return 'Rand({}, {})'.format(from_val, to_val)


# Control
def sclang():
    global __sclang_running__
    if not __sclang_running__:
        sclangPath = "/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/sclang"
        print("Starting sclang...")
        global proc
        global queue
        global thread
        proc, queue, thread = procio.run(sclangPath)
        __sclang_running__ = True
        print(procio.process_input(proc, queue, thread, 10))
        cmd("s.makeGui")
    else:
        proc.kill()
        __sclang_running__ = False
        sclang()


def play(ugen):
    print('{{ {} }}.play'.format(ugen))


def addInstr(name, ugen, *args):
    argument_list = 'arg out=0,'
    for item in args:
        argument_list += "{}={},".format(item[0], item[1])
    argument_list = argument_list[:-1] + ";"
    print(r'SynthDef({},{{{} Out.ar(out,{}.dup)}}).add'.format(
        name, argument_list, ugen))


lib = {
    'sinosc': sinosc,
    'saw': saw,
    'pwm': pwm,
    'noise': noise,
    'lfo': lfo,
    'aenv': aenv,
    'env': env,
    'lpf': lpf,
    'sclang': sclang,
    'play': play,
    'add': addInstr
}
