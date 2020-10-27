#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rebootpi.py
#
#  Copyright 2019  <martin@orchardrecovery.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Version: 0.3
#  Date:    2020-10-27
#
#  Revisions: 0.1 2019-01-09 Original Issue
#             0.2 2019-01-23 Added logging
#             0.3 2020-10-27 Use configuration file to determine if we want logging

#=======================================================================
# Required imports
#=======================================================================

import json                                     # JSON routines
import logging                                  # Logging routines
from gpiozero   import Button                   # GPIO Button handling
from signal     import pause                    # Pause program
from subprocess import call                     # Call script

#=======================================================================
# Function: reboot
#
# Reboot the pi using a custom script
#=======================================================================

def reboot():
    logging.info('System Rebooting')
    call([RESETFILE])

#=======================================================================
# Constants
#=======================================================================

LOGFILE   = '/home/pi/work/rebootpi/status.log'
RESETFILE = '/home/pi/scripts/rebootpi.sh'

#=======================================================================
# Read JSON configuration
#=======================================================================

with open('config.json', 'r') as f:
    config = json.load(f)

#=======================================================================
# Setup Logging since this is running in a daemon
#    - Output message
#         to filename LOGFILE
#         with date format in Y/M/D H:M:S
#         and allow logging of CRITICAL, ERROR, WARNING, INFO and DEBUG
#=======================================================================

if True == config['wantLogging']:
    logging.basicConfig(filename=LOGFILE, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.DEBUG)
    logging.info('System started');

#=======================================================================
# Main program
#=======================================================================

reset = Button(21, hold_time=2)                 # GPIO 21, held down for 2 sec

reset.when_held = reboot                        # When reset held, reboot

pause()                                         # Wait forever

