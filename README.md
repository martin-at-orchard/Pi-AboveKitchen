# Pi-AboveKitchen

The Raspberry Pi Above Kitchen is used to monitor 2 switches in the office above the kitchen and update the status when the state of the switch changes.

The following is needed:
* Raspberry Pi 3 or higher
* 8 GByte or larger micro SSD

## Pi Setup

These setup instructions allow you to take a brand new Raspbery Pi and get the application working.

Additional wiring will be required to connect the switches to the GPIO pins.
The appliction uses internal pull-up resistors to pull the GPIO pins high
which is connected to one side of the switch. The other side of the switch is connected to ground.

### Install the operating system

* Download Rapsberry Pi OS (32-bit) Lite from [the Raspberry Pi Website](https://www.raspberrypi.org/downloads/raspberry-pi-os/)
* Install it on the micro SD using [belenaEtcher](https://www.balena.io/etcher/) or some other software
* Add an empty text file called SSH in the boot partition
* Connect the Raspberry Pi to:
  * Ethernet connection
  * Micro USB Power Supply (minimum 2.5A)
* Boot the Raspberry Pi
  
### Configure the Operating System

* Login to the Raspberry Pi once it has finished booting using SSH (puTTY on Windows, terminal on Mac OS/X or Linux)
  * User: pi
  * Password: raspberry

* Mount the /tmp, /var/tmp, /var/log directories into RAM (optional, but will reduce the ware on the micro SD card, but the log files will be lost on reboot and the available RAM will be reduced by 230 MB).
  ```shell
  sudo nano /etc/fstab
  ```
  * Once editing the file enter the following at the bottom of the file.
    ```shell
    /tmpfs /tmp     tmpfs defaults,noatime,nosuid,size=100m           0 0
    /tmpfs /var/tmp tmpfs defaults,noatime,nosuid,size=30m            0 0
    /tmpfs /var/log tmpfs defaults,noatime,nosuid,size=100m,mode=0755 0 0
   ```
  * Press **^o** then **Enter** then **^x** to save and exit.

* Start up the Raspberry Pi configuration program
  ```script
  sudo raspi-config
  ```
  * Cursor down to `1 Change User Password`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** At the `You will now be asked to enter a new password for the pi user` press `Enter`
    ** Enter the new password and confirmation of the password
    ** At the `Password changed successfully` press `Enter`
    
  * Cursor down to `2 Network Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `N1 Hostname`, press `Tab` to highlight `<Select>` then press `Enter`
    ** At the hostname instructions, press `Enter`
    ** At the `Please enter a hostname` enter an appropriate hostname `doorsensorpi` for example, press `Tab` to highlight `<Ok>` then press `Enter`
  
  * **Note:** Optionally set up the Wireless LAN. Cursor down to `2 Network Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `N2 Wireless LAN`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor down to select the country in which the Pi is to be used (`CA Canada`), press `Tab` to highlight `<Ok>` then press `Enter`
    ** At the WiLAN country confirmation press `Enter`
    ** Enter the SSID, press `Tab` to highlight `<Ok>` then press `Enter`
    ** Enter the passphrase, press `Tab` to highlight `<Ok>` then press `Enter`  
   
  * **Note** Optionally change the locale from British English. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I1 Change Locale`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor or page down to find `en_CA.UTF-8 UTF-8` (or other locale), then press the `space bar` to enable
    ** Cursor down to find `en_GB.UTF-8 UTF-8`, then press the `space bar` to disable
    ** Press `Tab` to highlight `<Ok>` then press `Enter`
    ** Cursor down to `en_CA.UTF-8`, press `Tab` to highlight `<Ok>` then press `Enter`
    ** **NOTE:** The border of the configuration program might look odd, ignore it
    
  * **Note** Optionally change the timezone from GMT. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I2 Change Time Zone`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor down to `America` (or other location), press `Tab` to highlight `<Ok>` then press `Enter`
    ** Cursor or page down to `Vancouver` (or other timezone), press `Tab` to highlight `<Ok>` then press `Enter`
 
  * **Note** Optionally change the keyboard from English. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I3 Change Keyboard Layout`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Pick an appropirate keyboard.
    
  * Press `Tab` twice to highlight `<Finish>` then press Enter
  * If the system prompts you to reboot **DON'T** reboot at this time

* Edit the pi user .bashrc file.
  ```shell
  nano ~/.bashrc
  ```
  * Enter the above aliases to avoid making mistakes.
    ```shell
    alias rm='rm -i'
    alias cp='cp -i'
    alias mv='mv -i'
    ```

* **Note** Optionally set a Static IP address
  ```script
  sudo nano /etc/dhcpcd.conf
  ```
  * Scroll down to the commented out section Example static IP configuration and modify it accordingly
    
* Reboot the Raspberry Pi
  ```script
  sudo reboot
  ```
    
### Update and install all required software

* Update and Upgrade the Rasperry Pi
  ```script
  sudo apt update && sudo apt upgrade -y
  ```
  
* Install the GPIO python scripts (this installs the Python 3 GPIO, but the Python 2 GPIO could be used as instead)
  ```script
  sudo apt install python3-gpiozero python3-pigpio -y
  ```
  
* FTP the scripts directory and work directory to the /home/pi directory

* Make the scripts executable
  ```script
  chmod +x /home/pi/scripts/*.py
  chmod +x /home/pi/work/*/*.py
  ```

* Enable the reboot/halt service.
  ```shell
  cd /etc/systemd/system
  sudo systemctl enable /home/pi/work/rebootpi/rebootpi.service
  ```
* Start the reboot/halt service.
  ```shell
  sudo systemctl start rebootpi.service
  ```

* Enable the above kitchen monitoring service.
  ```shell
  cd /etc/systemd/system
  sudo systemctl enable /home/pi/work/staff_status/above_kitchen.service
  ```
* Start the above kitchen monitoring service.
  ```shell
  sudo systemctl start above_kitchen.service
  ```

### Hardware Setup

The following connections are required for the correct operation of the scripts

* Momentory pushbutton switch between GPIO21 (pin 40) and Ground (pin 39) for rebooting the Pi
* SPST switch between GPIO4 (pin 7) and Ground (pin 9) for monitioring Martin
* SPST switch between GPIO17 (pin 11) and Ground (pin 14) for monitoring Cassandra

* Reboot the pi
  ```shell
  cd ~/scripts
  ./rebootpi.sh
  ```
