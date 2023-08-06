usage: minmon [-h] [-V] [-s SEC] [-l LOG]

    minmon 0.9.1

MINimum MONitor - display on stdout: mem, swap, cpu, temp, disk i/o and net i/o

    1. date and time
    2. physical Memory % usage and Swap memory % usage
    3. Cpu % usage and cpu Temperature in °C 
    4. file system Read and Write rate in bytes/second
    5. network Download and Upload rate in bytes/second

Formats are:

    - 1: 'YYYY-mm-dd HH:MM:SS'
    - 2, 3: two 2-digit decimal numbers ('**' = 100) and a linear 0-100 graphic
    - 4, 5: two 5-digit human-readable numbers and a logarithmic 1-K-M-G-T graphic

As an example of 5-digit human-readable format, '11K50' means 11.50 * 1024 = 11776.

    - 'K' = 2 ** 10 = 1024 ** 1 =             1,024
    - 'M' = 2 ** 20 = 1024 ** 2 =         1,048,576
    - 'G' = 2 ** 30 = 1024 ** 3 =     1,073,741,824
    - 'T' = 2 ** 40 = 1024 ** 4 = 1,099,511,627,776

The program is minimalistic as it has a minimal memory (6 MB) and cpu footprint.

To stop the program press Ctrl-C.

Example:

    $ minmon -l log3.log # write on stdout and on ~/.minmon/log3.log
    YYYY-mm-dd HH:MM:SS M% S% 0 . . . .50 . . . 100 C% T° 0 . . . .50 . . . 100 R-B/s W-B/s 1 . . K . . M . . G . . T D-B/s U-B/s 1 . . K . . M . . G . . T
    2020-05-17 18:38:38 24  0 S────M────┼─────────┤  1 60 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:39 24  0 S . .M. . │ . . . . │  3 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:40 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:41 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:42 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:43 24  0 S────M────┼─────────┤  4 58 ├C────────┼─T───────┤     0 11K50 R─────┼─W───┼─────┼─────┤     0     0 X─────┼─────┼─────┼─────┤
    2020-05-17 18:38:44 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:45 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:46 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:47 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0 287K6 R . . │ . .W│ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:48 24  0 S────M────┼─────────┤  2 58 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:49 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:50 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    ^C

optional arguments:
    
    -h, --help         show this help message and exit
    -V, --version      show program's version number and exit
    -s SEC, --sec SEC  seconds between lines (integer >= 1, default: 1)
    -l LOG, --log LOG  append lines into LOG logfile (default path: '~/.minmon')
