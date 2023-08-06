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
    'return current time (format = "YYYY-mm-dd HH:MM:SS" if dat else "HH:MM:SS"'
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
    parser.add_argument("-s","--seconds", type=int, default=1, help="seconds between lines (integer >= 1, default: 1)")
    parser.add_argument("-t","--time-only", action='store_true',
                        help="write time only, no date (default: date and time, no effect on CSV format)")
    parser.add_argument("-n","--numeric-only", action='store_true',
                        help="write numeric only, no graphic (default: numeric and graphic, no effect on CSV format)")
    parser.add_argument("-g","--graphic-only", action='store_true',
                        help="write graphic only, no numeric (default: numeric and graphic, no effect on CSV format)")
    parser.add_argument("-c","--csv-format", action='store_true', help="write lines in CSV format")
    parser.add_argument("-l","--log-file", type=str, help=f"append lines into log file too (default path: '~/.minmon')")
    parser.parse_args(argv[1:], args)
    
    # check arguments 
    if args.seconds < 1:
        exit(f"minmon: error: --seconds is {args.seconds} but can't be less than 1")
    dat = not args.time_only
    num, gra = ((True, True) if args.numeric_only and args.graphic_only else
                  (not args.graphic_only, not args.numeric_only))
    
    # perform
    head = (dat * "DATE TIME MEM SWAP CPU TEMP READ WRITE DOWNLOAD UPLOAD" if args.csv_format else
        (dat * "YYYY-mm-dd " + "HH:MM:SS " +
        num * "M% S% " + gra * "0 . . . .50 . . . 100 " +
        num * "C% T° " + gra * "0 . . . .50 . . . 100 " +
        num * "R-B/s W-B/s " + gra * "1 . . K . . M . . G . . T " +
        num * "D-B/s U-B/s " + gra * "1 . . K . . M . . G . . T "))
    print(head)
    if args.log_file:
        if "/" not in args.log_file:
            path = expanduser("~/.minmon")
            makedirs(path, exist_ok=True)
        args.log_file = joinpath(path, args.log_file)
        log_file = open(args.log_file, "a")
        print(head, file=log_file, flush=True)
    i, r0, w0, d0, u0, k0, k2 = 0, 0, 0, 0, 0, 0.0, args.seconds
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
            if args.csv_format:
                line = f"{now()} {m} {s} {c} {t} {r} {w} {d} {u}"
            else:
                items = [now(dat)]
                if num: items.extend([strlin(m), strlin(s)])
                if gra: items.append(hislin([m, s], 'MS', i))
                if num: items.extend([strlin(c), strlin(t)])
                if gra: items.append(hislin([c, t], 'CT', i))
                if num: items.extend([strlog(r), strlog(w)])
                if gra: items.append(hislog([r, w], 'RW', i))
                if num: items.extend([strlog(d), strlog(u)])
                if gra: items.append(hislog([d, u], 'DU', i))
                line = " ".join(items)
            print(line)
            if args.log_file:
                print(line, file=log_file, flush=True)
        k1 = time()
        sleep(args.seconds - (k1 - k0))
        k2 = time()
            
def main():
    simplefilter('ignore') # avoid unuseful warnings
    try:
        minmon(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()

