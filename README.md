# kodi-buffalo-remote

Control kodi with Buffalo gamepad, via JSON-RPC API

## Prerequisites

You need to already have pygame, or at least the prerequisites for building pygame.

 What you see below might be the minimal requirements for raspbian-jessie:

 `apt-get install python-dev libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev`

 See also [this forum post](https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=33157&p=332140&hilit=croston%2bpygame#p284266).

## Install

Install directly from github: `pip install -e git+git://github.com/mattvonrocketstein/kodi-buffalo-remote.git@master#egg=buffalo`

## Usage

Run the joystick listener process in the foreground, with the default keybindings, pointed at the kodi instance described by environment variables:

```
export KODI_HOST=localhost
export KODI_PORT=8080
export KODI_USER=guest
export KODI_PASSWORD=guest
sudo buffalo
```

Run the tests with 'python setup.py test'

## Known Issues 

<!-- **Platform is Linux only?**  Yes, this uses `evdev` which  -->
**Why Sudo?**

Sometimes pygame / sdl seem to require root even when `SDL_VIDEODRIVER`is set to `dummy` (as is our default).  You might never be affected by this if you're actually running from xwindows, but

Errors like what you see below are most likely caused by not using sudo, which

```
Traceback (most recent call last):
  File "/home/pi/tmp/bin/buffalo", line 10, in <module>
    sys.exit(main())
  File "/home/pi/tmp/src/buffalo/buffalo/cli/entry.py", line 13, in main
    pygame.display.init()
pygame.error: Unable to open a console terminal
```
