# NetInput

Netinput acts as a workaround for current MAME limitation with user inputs.
- It allows to use multiple mice with one MAME instance (using other computers mice) in Linux.
- It allows to use the same keyboard on several instances of MAME in Linux.
- It allows to use several joysticks/wheels with multiple MAME instance.

Netinput consists of 2 scripts, a server script and a client script.

- Server

It's called `netinput.lua`. It's configured through the NETINPUT_ADDR environnement variable. It's loaded in MAME through the `-autoboot_script` command line.

- Client

It's called `netinput_client.py`. It uses Python and the PyGame library:

Install PyGame: pip3 install pygame

PyGame version must be greater than 2.0.0

It's configured with JSON file. Some samples configuration files are provided in this repository.

With some configuration, NetInput client grabs inputs. To release this grab, push ESC key.


## Virtua Formula: Using the same keyboard for multiple MAME instances

Running 2 linked MAME instances:

`NETINPUT_ADDR=0.0.0.0:54321 mame vformula -window -nomaximize -nohttp -nomouse -cfg_directory cfg1 -nvram_directory nvram1 -comm_remotehost 127.0.0.1 -comm_remoteport 15122 -comm_localhost 0.0.0.0 -comm_localport 15121 -comm_framesync -autoboot_script netinput.lua -autoboot_delay 0`

`NETINPUT_ADDR=0.0.0.0:54322 mame vformula -window -nomaximize -nohttp -nomouse -cfg_directory cfg2 -nvram_directory nvram2 -comm_remotehost 127.0.0.1 -comm_remoteport 15121 -comm_localhost 0.0.0.0 -comm_localport 15122 -comm_framesync -autoboot_script netinput.lua -autoboot_delay 0`

(One of those instance muste be configured as "Master" in F2 menu inside MAME. The other must be "Slave")

Running NetInput client:

`./netinput_client.py vr_A_key.json vr_B_key.json`

From now, when the NetInput has the focus, you could use keys described in JSON files (arrow keys and keypad arrows) to control both MAME instances.

Click for video
[![VF demo video](https://img.youtube.com/vi/AYk97BY5BzU/0.jpg)](https://www.youtube.com/watch?v=AYk97BY5BzU)

## Wing War: Using multiple joysticks/wheels for multiple MAME instances

This is the same setup than for keyboard. The only difference is the JSON configuration files:

`./netinput_client.py wingwar_A_joy.json wingwar_B_joy.json`

Click for video
[![WingWar demo video](https://img.youtube.com/vi/1W3-yOFDW6Y/0.jpg)](https://www.youtube.com/watch?v=1W3-yOFDW6Y)

## Point Blank: Using multiple mice with one MAME instance.

Running Point Blank on computer 1 (with IP = 192.168.0.1, see JSON file to change this)

`NETINPUT_ADDR=0.0.0.0:54321 mame ptblank -autoboot_script netinput.lua -autoboot_delay 0`

Running NetInput client on computer 2:

Note that the provided JSON files uses 192.168.0.1 as server address. You may have to change this on your personnal network.

`./netinput_client.py ptblank.json`

You can now control the first cursor with computer 1's mouse, and the second cursor with computer 2's mouse.

Click for video
[![Point Blank demo video](https://img.youtube.com/vi/X3eC7ARrHzU/0.jpg)](https://www.youtube.com/watch?v=X3eC7ARrHzU)

