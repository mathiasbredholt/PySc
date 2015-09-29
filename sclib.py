instr = '\instrument'
midi = '\midinote'
inf = 'inf'

LFOsin = 0


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


# Filters
def lpf(input, freq=1000, rq=0.82):
    return 'BLowPass4.ar({}, {}, {})'.format(input, freq, rq)


# Envelopes
def ampEnv(attack=0.05, decay=1, mul=1, add=0):
    return 'EnvGen.kr(Env.perc({}, {}), levelScale: {}, levelBias: {}, doneAction:2)'.format(
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


def lfo(wave, freq, from_val, to_val, phase=0):
    if wave == LFOsin:
        return 'SinOsc.kr({}, {}).range({}, {})'.format(freq, phase, from_val,
                                                        to_val)


def noise(mul=1, add=1):
    return 'WhiteNoise.ar({}, {})'.format(mul, add)


def random(from_val, to_val):
    return 'Rand({}, {})'.format(from_val, to_val)
