from pyparsing import Literal, Keyword, Optional, Word, Combine, ZeroOrMore, OneOrMore, Forward, Group, Regex, alphas, nums, alphanums, oneOf, ParseException
import sclib


def run_single_cmd(t):
    try:
        sclib.lib[t[0]]()
    except KeyError as err:
        print('Command not recognized.')


def run_group_cmd(t):
    print(t)
    key = t[0][0]
    args = t[0][:]
    args.pop(0)
    try:
        sclib.lib[key](*args)
    except KeyError as err:
        print('Command not recognized.')


def cmd_syntax():
    single_cmd = Word(alphas).setParseAction(run_single_cmd)
    cmd = Word(alphas)
    arg = Word(alphanums)
    arg_func = (Word(alphas) + Word('=') + Word(nums)).setParseAction(
        lambda t: (t[0], t[2]))
    ugen = Regex(r'\[.*\]').setParseAction(lambda t: parse_ugen(t[0]))
    group_cmd = Group(cmd + OneOrMore(arg_func | arg | ugen)).setParseAction(
        run_group_cmd)
    expr = group_cmd | single_cmd
    return expr


def format_ugen(t):
    # print(t)
    key = t[0][0]
    args = t[0][:]
    args.pop(0)
    if sclib.lib[key]:
        return sclib.lib[key](*args)


def ugen_syntax():
    lpar = Literal('[').suppress()
    rpar = Literal(']').suppress()
    cmd = Word(alphas)
    point = Literal('.')
    sign = Literal('-')
    number = Word(nums)
    integer = Combine(Optional(sign) + number).setParseAction(
        lambda t: int(t[0]))
    floatnumber = Combine(integer + point + number).setParseAction(
        lambda t: float(t[0]))
    expr = Forward()
    cmd_gp = Group(lpar + expr + rpar).setParseAction(format_ugen)
    atom = cmd_gp | floatnumber | integer | cmd
    expr << atom + ZeroOrMore(expr)
    return expr


cmd_parser = cmd_syntax()
ugen_parser = ugen_syntax()


def parse_cmd(string):
    try:
        cmd_parser.parseString(string).asList()[0]
    except ParseException as err:
        print(err)


def parse_ugen(string):
    return ugen_parser.parseString(string).asList()[0]

    parse_cmd('add asdf [sinosc] freq=440 phase=4')
# word_func = pp.Word(pp.alphas)
# word_int = pp.Word(pp.nums)
# word_float = pp.
# word_list = pp.ZeroOrMore(word_func) + pp.Or([pp.ZeroOrMore(
#     word_integer), pp.ZeroOrMore(word_float), pp.ZeroOrMore(word_func)])
# parser_scl = pp.Group(word_list).setParseAction(format_ugen)
# nested = pp.nestedExpr(content=parser_scl)
# # nested.parseString('(saw 4 (saw))').asList()
# parser_scl.parseString('saw 4 (saw)').asList()
