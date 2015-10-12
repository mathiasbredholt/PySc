instr = '\instrument'
midi = '\midinote'
inf = 'inf'

LFOsin = 0


def seq(li, rep):
    return 'Pseq({},{})'.format(li, rep)


def out(bus, ugen):
    return 'Out.ar({}, {})'.format(bus, ugen)


class Number():
    """docstring for Number"""

    def __init__(self, value):
        super(Number, self).__init__()
        self.value = value

    def to_sclang(self):
        return self.value


# Ugens
class UGen():
    """docstring for UGen"""

    def __init__(self):
        super(UGen, self).__init__()

    def play(self, name):
        return '~{} = {{ {}.dup }}.play'.format(name, self.to_sclang())


# Generators
class SinOsc(UGen):
    """docstring for SinOsc"""

    def __init__(self,
                 freq=Number(440),
                 phase=Number(0),
                 mul=Number(1),
                 add=Number(0)):
        super(SinOsc, self).__init__()
        self.freq = freq
        self.phase = phase
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'SinOsc.ar({}, {}, {}, {})'.format(
            self.freq.to_sclang(), self.phase.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang(), )


class Saw(UGen):
    """docstring for Saw"""

    def __init__(self, freq=Number(440), mul=Number(1), add=Number(0)):
        super(Saw, self).__init__()
        self.freq = freq
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'Saw.ar({}, {}, {})'.format(
            self.freq.to_sclang(), self.mul.to_sclang(), self.add.to_sclang())


class LFSaw(UGen):
    """docstring for LFSaw"""

    def __init__(self,
                 freq=Number(440),
                 phase=Number(0),
                 mul=Number(1),
                 add=Number(0)):
        super(LFSaw, self).__init__()
        self.freq = freq
        self.phase = phase
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'LFSaw.ar({}, {}, {}, {})'.format(
            self.freq.to_sclang(), self.phase.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang())


class PWM(UGen):
    """docstring for PWM"""

    def __init__(self,
                 freq=Number(440),
                 pulsewidth=Number(0.5),
                 mul=Number(1),
                 add=Number(0)):
        super(PWM, self).__init__()
        self.freq = freq
        self.pulsewidth = pulsewidth
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'Pulse.ar({}, {}, {}, {})'.format(
            self.freq.to_sclang(), self.pulsewidth.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang())


class Noise(UGen):
    """docstring for Noise"""

    def __init__(self, mul=Number(1), add=Number(0)):
        super(Noise, self).__init__()
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'WhiteNoise.ar({}, {})'.format(
            self.mul.to_sclang(), self.add.to_sclang())


# Filters
class LPF(UGen):
    """docstring for LPF"""

    def __init__(self, input, freq=Number(1000), rq=Number(1)):
        super(LPF, self).__init__()
        self.input = input
        self.freq = freq
        self.rq = rq

    def to_sclang(self):
        return 'BLowPass4.ar({}, {}, {})'.format(
            self.input.to_sclang(), self.freq.to_sclang(), self.rq.to_sclang())


# Delay and reverb
class Delay1(UGen):
    """docstring for Delay1"""

    def __init__(self,
                 input,
                 max=Number(0.2),
                 time=Number(0.2),
                 decay=Number(1),
                 mul=Number(1),
                 add=Number(0)):
        super(Delay1, self).__init__()
        self.input = input
        self.max = max
        self.time = time
        self.decay = decay
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'CombC.ar({}, {}, {}, {}, {}, {})'.format(
            self.input.to_sclang(), self.max.to_sclang(),
            self.time.to_sclang(), self.decay.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang())


# Envelopes
class AEnv(UGen):
    """docstring for AmpEnv"""

    def __init__(self,
                 attack=Number(0.05),
                 decay=Number(1),
                 mul=Number(1),
                 add=Number(0)):
        super(AEnv, self).__init__()
        self.attack = attack
        self.decay = decay
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'EnvGen.ar(Env.perc({}, {}), 1, {}, {}, 1, 2)'.format(
            self.attack.to_sclang(), self.decay.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang())


class Env(UGen):
    """docstring for Env"""

    def __init__(self,
                 attack=Number(0.05),
                 decay=Number(1),
                 mul=Number(1),
                 add=Number(0)):
        super(Env, self).__init__()
        self.attack = attack
        self.decay = decay
        self.mul = mul
        self.add = add

    def to_sclang(self):
        return 'EnvGen.kr(Env.perc({}, {}), 1, {}, {}, 1, 0)'.format(
            self.attack.to_sclang(), self.decay.to_sclang(),
            self.mul.to_sclang(), self.add.to_sclang())

# class Mix(UGen):
#     """docstring for Mix"""
#
#     def __init__(self, *args, amp=1):
#         super(Mix, self).__init__()
#         self.args = Number(args)
#         self.amp = Number(amp)
#
#     def to_sclang(self):
#         return 'MulAdd.new(Mix.new([{}]), {})'.format(", ".join(self.args),
#                                                       self.amp)


class LFO(UGen):
    """docstring for LFO"""

    def __init__(self,
                 wave=Number(0),
                 freq=Number(1),
                 from_val=Number(0),
                 to_val=Number(1),
                 phase=Number(0)):
        super(LFO, self).__init__()
        self.wave = wave
        self.freq = freq
        self.from_val = from_val
        self.to_val = to_val
        self.phase = phase

    def to_sclang(self):
        if self.wave.value == 0:
            return 'SinOsc.kr({}, {}).range({}, {})'.format(
                self.freq.to_sclang(), self.phase.to_sclang(),
                self.from_val.to_sclang(), self.to_val.to_sclang())


def lpf(input, freq=1000, rq=0.82):
    return 'BLowPass4.ar({}, {}, {})'.format(input, freq, rq)


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


def sinosc(freq=440, phase=0, mul=0.5, add=0):
    return 'SinOsc.ar({}, {}, {}, {})'.format(freq, phase, mul, add)


def saw(freq=440, mul=0.5, add=0):
    return 'Saw.ar({}, {}, {})'.format(freq, mul, add)


def pwm(freq=440, pulsewidth=0.5, mul=0.5, add=0):
    return 'Pulse.ar({}, {}, {}, {})'.format(freq, pulsewidth, mul, add)


def noise(mul=1, add=0):
    return 'WhiteNoise.ar({}, {})'.format(mul, add)


# Patterns
def pbind(name, args):
    result = ""
    for key, value in args.items():
        result += "{}, {},".format(key, value)
    return 'Pdef(\\{},Pbind({})).play(quant:-1)'.format(name, result[:-1])


def pseq(input, repetitions):
    return 'Pseq({}, {})'.format(input, repetitions)


# Control
def play(name='test', playable=SinOsc()):
    return playable.play(name)


def add_instr(name, ugen, *args):
    argument_list = 'arg out=0,'
    for item in args:
        argument_list += "{}={},".format(item[0], item[1])
    argument_list = argument_list[:-1] + ";"
    return r'SynthDef({},{{{} Out.ar(out,{}.dup)}}).add'.format(
        name, argument_list, ugen.to_sclang())


lib = {
    'sinosc': SinOsc,
    'saw': Saw,
    'lfsaw': LFSaw,
    'pwm': PWM,
    'noise': Noise,
    'lfo': LFO,
    'delay1': Delay1,
    'lpf': LPF,
    # 'mix': Mix,
    'aenv': AEnv,
    'env': env,
    'play': play,
    'add': add_instr
}
