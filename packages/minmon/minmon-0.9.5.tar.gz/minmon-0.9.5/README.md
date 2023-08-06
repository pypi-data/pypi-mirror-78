usage: minmon [-h] [-V] [-s SECONDS] [-t] [-n] [-g] [-c] [-l LOG_FILE]

MINimum MONitor - write on stdout (and maybe on log file): timestamp, RAM and CPU usage, temperature, disk i/o and net i/o

minmon writes at fixed time intervals a line in stdout containing:
```
    1. date 'YYYY-mm-dd' (unless -t/--time is set)
    2. time 'HH:MM:SS'
    3. physical Memory % usage and Swap memory % usage
    4. CPU % usage and CPU Temperature in °C
    5. file system Read and Write rate in bytes/second
    6. network Download and Upload rate in bytes/second
```
Formats for 3. and 4. are:
```
    - numeric: two 2-digit decimal numbers, '**' = 100 (unless -g/--graphic is set)
    - graphic: a linear 0-100 graphic (unless -n/--numeric is set)
```
Formats for 5. an 6. are:
```
    - numeric: two 5-chars human-readable numbers (unless -g/--graphic is set)
    - graphic: a logarithmic 1-K-M-G-T graphic (unless -n/--numeric is set)
```
On overlap in graphics an 'X' is displayed.

As examples of 5-chars human-readable format:
```
    - '10K50' means 10.50 * 1024 = 10752 (about)
    - '287K6' means 287.6 * 1024 = 294502 (about)
```
Letters have the usual meaning:
```
    - 'K' = 2 ** 10 = 1024 ** 1 =          1024
    - 'M' = 2 ** 20 = 1024 ** 2 =       1048576
    - 'G' = 2 ** 30 = 1024 ** 3 =    1073741824
    - 'T' = 2 ** 40 = 1024 ** 4 = 1099511627776
```
The program is minimalistic as it has a minimal RAM (6 MB) and CPU footprint.

To stop the program press Ctrl-C.

Examples:
```
    $ minmon -l log3.log # write on stdout and on ~/.minmon/log3.log
    YYYY-mm-dd HH:MM:SS M% S% 0 . . . .50 . . . 100 C% T° 0 . . . .50 . . . 100 R-B/s W-B/s 1 . . K . . M . . G . . T D-B/s U-B/s 1 . . K . . M . . G . . T
    2020-09-03 16:09:38 24  0 S────M────┼─────────┤  1 60 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-09-03 16:09:39 24  0 S . .M. . │ . . . . │  3 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:40 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-09-03 16:09:41 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:42 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:43 24  0 S────M────┼─────────┤  4 58 ├C────────┼─T───────┤     0 10K50 R─────┼─W───┼─────┼─────┤     0     0 X─────┼─────┼─────┼─────┤
    2020-09-03 16:09:44 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:45 24  0 S . .M. . │ . . . . │  4 58 │C. . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:46 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │    52     0 U .D. │ . . │ . . │ . . │
    2020-09-03 16:09:47 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0 287K6 R . . │ . .W│ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:48 24  0 S────M────┼─────────┤  2 58 C─────────┼─T───────┤     0     0 X─────┼─────┼─────┼─────┤    52     0 U──D──┼─────┼─────┼─────┤
    2020-09-03 16:09:49 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    2020-09-03 16:09:50 24  0 S . .M. . │ . . . . │  2 58 C . . . . │ T . . . │     0     0 X . . │ . . │ . . │ . . │     0     0 X . . │ . . │ . . │ . . │
    ^C
    $ minmon -tg # time only, no date, graphic only, no numeric, narrower output
    HH:MM:SS 0 . . . .50 . . . 100 0 . . . .50 . . . 100 1 . . K . . M . . G . . T 1 . . K . . M . . G . . T
    16:12:22 S──────M──┼─────────┤ C─────────┼─T───────┤ X─────┼─────┼─────┼─────┤ X─────┼─────┼─────┼─────┤
    16:12:23 S . . .M. │ . . . . │ │C. . . . │ T . . . │ X . . │ . . │ . . │ . . │ U .D. │ . . │ . . │ . . │
    16:12:24 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:25 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:26 S . . .M. │ . . . . │ │C. . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:27 S──────M──┼─────────┤ C─────────┼─T───────┤ X─────┼─────┼─────┼─────┤ U──D──┼─────┼─────┼─────┤
    16:12:28 S . . .M. │ . . . . │ │C. . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:29 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ U .D. │ . . │ . . │ . . │
    16:12:30 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:31 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ U .D. │ . . │ . . │ . . │
    16:12:32 S──────M──┼─────────┤ C─────────┼─T───────┤ X─────┼─────┼─────┼─────┤ X─────┼─────┼─────┼─────┤
    16:12:33 S . . .M. │ . . . . │ C . . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    16:12:34 S . . .M. │ . . . . │ │C. . . . │ T . . . │ X . . │ . . │ . . │ . . │ X . . │ . . │ . . │ . . │
    ^C
```
optional arguments:
```
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -s SECONDS, --seconds SECONDS
                        seconds between lines (integer >= 1, default: 1)
  -t, --time-only       display time only, no date (default: date and time, no effect on CSV format)
  -n, --numeric-only    display numeric only, no graphic (default: numeric and graphic, no effect on CSV format)
  -g, --graphic-only    display graphic only, no numeric (default: numeric and graphic, no effect on CSV format)
  -c, --csv-format      write lines in CSV format
  -l LOG_FILE, --log-file LOG_FILE
                        append lines into log file too (default path: '~/.minmon')

```
