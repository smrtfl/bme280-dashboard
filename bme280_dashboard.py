#!/usr/bin/env python3

import getopt
import curses
from BME280 import BME280
from Dashboard import Dashboard


if __name__ == "__main__":
    bme280 = BME280("")
    curses.wrapper(lambda stdscr: Dashboard(stdscr, bme280))
