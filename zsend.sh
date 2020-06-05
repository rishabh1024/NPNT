#!/bin/sh

DEV=/dev/ttyUSB0

stty -F $DEV 57600
sz $1 > $DEV < $DEV
