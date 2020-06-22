#!/bin/sh

DEV=/dev/ttyUSB0

stty -F $DEV 57600
rz > $DEV < $DEV

