#!/bin/sh
sudo iwlist wlan0 scan | egrep "Cell|ESSID|Signal|Rates"
