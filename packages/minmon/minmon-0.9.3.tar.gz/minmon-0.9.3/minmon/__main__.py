#!/usr/bin/python3
# -*- coding: utf-8 -*-

# imports

from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from math import log
from os import makedirs
from os.path import expanduser, join as joinpath
from psutil import virtual_memory as mem, swap_memory as swap
from psutil import cpu_percent as cpu, sensors_temperatures as temp
from psutil import disk_io_counters as disk, net_io_counters as net
from sys import argv, exit
from time import localtime, sleep, time
from warnings import simplefilter

# constants

log1024 = log(1024)

# classes

class args: pass # container for arguments

# specific functions

def now(date_too=True):
    'return current time (format = "YYYY-mm-dd HH:MM:SS" if date else "HH:MM:SS"'
    return "%04d-%02d-%02d %02d:%02d:%02d" % localtime()[:6] if date_too else "%02d:%02d:%02d" % localtime()[3:6]

def strlin(x):
    '2-digits display (linear data)'
    x = round(x)
    return ' 0' if x <= 0 else '**' if x >= 100 else '%2d' % x

def hislin(xx, cc, i):
    'histogram display (linear data)'
    hh = list('├─────────┼─────────┤' if i % 5 == 2 else '│ . . . . │ . . . . │')
    for x, c in zip(xx, cc):
        j = max(0, min(20, round(0.2 * x)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)
            
def strlog(x):
    '5-chars display (logarithmic data)'
    x = max(0, round(x))
    if x < 1024:
        return '%5d' % x
    for e, c in enumerate('KMGTPEZY'):
        if x < 1024 ** (e + 2):
            return (str(x / 1024 ** (e + 1)).replace('.', c) + '00000')[:5]
    return '*****'
    
def hislog(xx, cc, i):
    'histogram display (logarithmic data)'
    hh = list('├─────┼─────┼─────┼─────┤' if i % 5 == 2 else '│ . . │ . . │ . . │ . . │')
    for x, c in zip(xx, cc):
        j = max(0, min(24, round(6.0 * log(max(1.0, x)) / log1024)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)

# main functions

def minmon(argv):

    # get arguments
    from .__init__ import __doc__ as description, __version__ as version
    parser = Parser(prog="minmon", formatter_class=Formatter, description=description)
    parser.add_argument("-V", "--version", action="version", version="minmon " + version)
    parser.add_argument("-s","--sec", type=int, default=1, help="seconds between lines (integer >= 1, default: 1)")
    parser.add_argument("-t","--time-only", action='store_true',
                        help="display time only (default: date and time, no effect on CSV format)")
    parser.add_argument("-n","--numbers-only", action='store_true',
                        help="display numbers only (default: numbers and graphics, no effect on CSV format)")
    parser.add_argument("-g","--graphics-only", action='store_true',
                        help="display graphics only (default: numbers and graphics, no effect on CSV format)")
    parser.add_argument("-c","--csv", action='store_true', help="output in CSV format")
    parser.add_argument("-l","--log", type=str, help=f"write lines into LOG logfile (default path: '~/.minmon')")
    parser.parse_args(argv[1:], args)
    
    # check arguments 
    if args.sec < 1:
        exit(f"minmon: error: --sec is {args.sec} but can't be less than 1")
    date = not args.time_only
    numb, grap = ((True, True) if args.numbers_only and args.graphics_only else
                  (not args.graphics_only, not args.numbers_only))
    
    # perform
    head = (date * "DATE TIME MEM SWAP CPU TEMP READ WRITE DOWNLOAD UPLOAD" if args.csv else
        (date * "YYYY-mm-dd " + "HH:MM:SS " +
        numb * "M% S% " + grap * "0 . . . .50 . . . 100 " +
        numb * "C% T° " + grap * "0 . . . .50 . . . 100 " +
        numb * "R-B/s W-B/s " + grap * "1 . . K . . M . . G . . T " +
        numb * "D-B/s U-B/s " + grap * "1 . . K . . M . . G . . T "))
    if args.log:
        if "/" not in args.log:
            path = expanduser("~/.minmon")
            makedirs(path, exist_ok=True)
        args.log = joinpath(path, args.log)
        log_file = open(args.log, "a")
        print(head, file=log_file, flush=True)
    i, r0, w0, d0, u0, k0, k2 = 0, 0, 0, 0, 0, 0.0, args.sec
    while True:
        dk = k2 - k0
        k0 = time()
        i += 1
        s = swap().percent
        m = mem().percent
        c = cpu()
        t = max(x.current for xx in temp().values() for x in xx)
        r1 = disk().read_bytes;  r = max(0, r1 - r0) / dk; r0 = r1
        w1 = disk().write_bytes; w = max(0, w1 - w0) / dk; w0 = w1
        d1 = net().bytes_recv;   d = max(0, d1 - d0) / dk; d0 = d1
        u1 = net().bytes_sent;   u = max(0, u1 - u0) / dk; u0 = u1
        if i > 1:
            if args.csv:
                line = f"{now()} {m} {s} {c} {t} {r} {w} {d} {u}"
            else:
                items = [now(date)]
                if numb: items.extend([strlin(m), strlin(s)])
                if grap: items.append(hislin([m, s], 'MS', i))
                if numb: items.extend([strlin(c), strlin(t)])
                if grap: items.append(hislin([c, t], 'CT', i))
                if numb: items.extend([strlog(r), strlog(w)])
                if grap: items.append(hislog([r, w], 'RW', i))
                if numb: items.extend([strlog(d), strlog(u)])
                if grap: items.append(hislog([d, u], 'DU', i))
                line = " ".join(items)
            print(line)
            if args.log:
                print(line, file=log_file, flush=True)
        k1 = time()
        sleep(args.sec - (k1 - k0))
        k2 = time()
            
def main():
    simplefilter('ignore') # avoid unuseful warnings
    try:
        minmon(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()

