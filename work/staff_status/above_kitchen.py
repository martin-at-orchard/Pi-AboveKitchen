#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  above_kitchen.py
#
#  Copyright 2019-2020  <martin@orchardrecovery.com>
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
#  Version:   0.6
#  Date:      2020-10-27
#
#  Revisions: 0.1 2019-01-09 Original Issue
#             0.2 2019-01-14 Use global to store the status of the switch
#             0.3 2019-01-16 Use GPIO instead of gpiozero
#             0.4 2019-01-16 Use pigpio instead of GPIO
#             0.5 2019-01-23 Added logging
#             0.6 2020-10-27 Use configuration file to determine if we want logging
#
#=======================================================================
# Required imports
#=======================================================================

import json                                 # JSON    Routines
import logging                              # Logging Routines
import requests                             # HTML    Routines
from signal     import pause                # Wait    Routines
from time       import sleep                # Sleep   Routines
import pigpio                               # GPIO    Routines

#=======================================================================
# Constants
#=======================================================================

martin_gpio    = 4                        # Broadcom GPIO04
martin_id      = 1                        # ID in OX

cassandra_gpio = 17                       # Broadcom GPIO17
cassandra_id   = 115                      # ID in OX

URL            = 'http://ox.orchardrecoveryonline.com/admin/setabovekitchen.php'
LOGFILE        = '/home/pi/work/staff_status/status.log'

#=======================================================================
# Globals
#=======================================================================

martin_status    = -1
cassandra_status = -1
pi               = -1

#=======================================================================
# Read JSON configuration
#=======================================================================

with open('config.json', 'r') as f:
    config = json.load(f)

#=======================================================================
# Called when the GPIO detects a change from out to in
# Ignore if already in
#=======================================================================
def process_switch(gpio, status, tick):
    global martin_status
    global cassandra_status
    global config

    if martin_gpio == gpio:
        if martin_status != status:
            martin_status = status
            PARAMS = {'id':martin_id, 'status':status}
            r = requests.get(url = URL, params = PARAMS)
            if True == config['wantLogging']:
                s = '{name} {status} - {result}'.format(name='Martin', status=status, result=r.text)
                logging.info(s);
    else:
        if cassandra_status != status:
            cassandra_status = status
            PARAMS = {'id':cassandra_id, 'status':status}
            r = requests.get(url = URL, params = PARAMS)
            if True == config['wantLogging']:
                s = '{name} {status} - {result}'.format(name='Cassandra', status=status, result=r.text)
                logging.info(s);

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
# Configure GPIO
#    - Set to input, with internal pull up resistor, with glitch filter
#      set to 300,000 uSecs
#=======================================================================

pi = pigpio.pi()                              # Get access to GPIO

pi.set_mode(martin_gpio, pigpio.INPUT)
pi.set_pull_up_down(martin_gpio, pigpio.PUD_UP)
pi.set_glitch_filter(martin_gpio, 300000)

pi.set_pull_up_down(cassandra_gpio, pigpio.PUD_UP)
pi.set_mode(cassandra_gpio, pigpio.INPUT)
pi.set_glitch_filter(cassandra_gpio, 300000)

pi.callback(martin_gpio, pigpio.EITHER_EDGE, process_switch)
pi.callback(cassandra_gpio, pigpio.EITHER_EDGE, process_switch)

#=======================================================================
# Startup check, read the state of the switchs
#=======================================================================

process_switch(martin_gpio, pi.read(martin_gpio), 1)
sleep(0.1)
process_switch(cassandra_gpio, pi.read(cassandra_gpio), 1)
sleep(0.1)

pause()                                         # Wait forever

pi.stop()                                       # Release GPIO Resources
