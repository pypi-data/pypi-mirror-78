"""MINimum MONitor - display on stdout: timestamp, RAM and CPU usage, temperature, disk i/o and net i/o

minmon displays at fixed time intervals a line in stdout containing:

    1. date 'YYYY-mm-dd' (only if -d/--date argument is set)
    2. time 'HH:MM:SS'
    3. physical Memory % usage and Swap memory % usage
    4. CPU % usage and CPU Temperature in °C
    5. file system Read and Write rate in bytes/second
    6. network Download and Upload rate in bytes/second

Formats for 3. and 4. are:

    - two 2-digit decimal numbers ('**' = 100)
    - and a linear 0-100 graphic

Formats for 5. an 6. are:

    - two 5-chars human-readable numbers
    - and a logarithmic 1-K-M-G-T graphic

On overlap in graphics an 'X' is displayed.

As examples of 5-chars human-readable format:

    - '10K50' means 10.50 * 1024 = 10752 (about)
    - '287K6' means 287.6 * 1024 = 294502 (about)

Letters have the usual meaning:

    - 'K' = 2 ** 10 = 1024 ** 1 =          1024
    - 'M' = 2 ** 20 = 1024 ** 2 =       1048576
    - 'G' = 2 ** 30 = 1024 ** 3 =    1073741824
    - 'T' = 2 ** 40 = 1024 ** 4 = 1099511627776

The program is minimalistic as it has a minimal RAM (6 MB) and CPU footprint.

To stop the program press Ctrl-C.

Example:

    $ minmon -d -l log3.log # write on stdout and on ~/.minmon/log3.log
    YYYY-mm-dd HH:MM:SS M% S% 0 . . . .50 . . . 100 C% T° 0 . . . .50 . . . 100 R-B/s W-B/s 1 . . K . . M . . G . . T D-B/s U-B/s 1 . . K . . M . . G . . T
    2020-05-17 18:38:38 24  0 S────M────┼─────────┤  1 60 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:39 24  0 S . .M. . │ . . . . │  3 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:40 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:41 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:42 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:43 24  0 S────M────┼─────────┤  4 58 ├C────────┼─T───────┤     0 10K50 R─────┼─W───┼─────┼─────┤     0     0 X─────┼─────┼─────┼─────┤
    2020-05-17 18:38:44 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:45 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:46 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-05-17 18:38:47 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0 287K6 R . . │ . .W│ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:48 24  0 S────M────┼─────────┤  2 58 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-05-17 18:38:49 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-05-17 18:38:50 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    ^C
"""

__version__ = "0.9.3"

