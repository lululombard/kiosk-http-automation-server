# kiosk-http-automation-server
Small Python app to start/stop services that I use with Home Assistant to start/stop kiosk/camera services and display.

It was written in ~30 minutes so it's far from perfect but it works.

:warning: There is no authentication at all, so don't run this on a public network!

## Example

### Service

`curl http://localhost:5000/services/vlc.service/status` -> `{"running":false,"success":true}`

`curl -X POST http://localhost:5000/services/vlc.service/start` -> `{"success":true}`

`curl http://localhost:5000/services/vlc.service/status` -> `{"running":true,"success":true}`

`curl -X POST http://localhost:5000/services/vlc.service/stop` -> `{"success":true}`

### Display

`curl http://10.1.0.39:5000/display/status` -> `{"on":true,"success":true}`

`curl -X POST http://10.1.0.39:5000/display/off` -> `{"success":true}`

`curl http://10.1.0.39:5000/display/status` -> `{"on":false,"success":true}`

`curl -X POST http://10.1.0.39:5000/display/on` -> `{"success":true}`

## Setup

You'll need Python 3.8 (or later) for this.
Tested on Ubuntu 20.04 LTS.

```bash
sudo apt install build-essential libpython3-dev libdbus-1-dev libdbus-glib-1-dev
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## How to run

You can just run server.py as root, like `sudo env/bin/python server.py`.

The way I host it on my Kiosk computer is with the systemd file provided, and I use it to start a custom VLC service to display my CCTV camera when a motion is detected via Home Assistant using a command line switch and curl.
