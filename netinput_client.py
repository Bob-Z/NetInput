#!/usr/bin/python3

# Key names are at https://github.com/pygame/pygame/blob/main/src_c/key.c , in SDL1_scancode_names

import time

import pygame
import json
import sys
import socket
import datetime

joystick_list = []
joystick_count = 0


def init_joystick():
    global joystick_count
    global joystick_list

    pygame.joystick.init()

    joystick_count = pygame.joystick.get_count()

    print("Number of joysticks: ", joystick_count)

    for j in range(joystick_count):
        joystick_list.append(pygame.joystick.Joystick(j))
        joystick_list[j].init()

        jid = joystick_list[j].get_instance_id()
        print("JID", jid)

        name = joystick_list[j].get_name()
        print("name", name)

        guid = joystick_list[j].get_guid()
        print("guid", guid)

        axes = joystick_list[j].get_numaxes()
        print("axes", axes)

        for a in range(axes):
            axis = joystick_list[j].get_axis(a)
            print("axis", a, "value", axis)

        buttons = joystick_list[j].get_numbuttons()
        print("buttons", buttons)

        for b in range(buttons):
            button = joystick_list[j].get_button(b)
            print("button", b, "value", button)

        hats = joystick_list[j].get_numhats()
        print("hats", hats)

        for h in range(hats):
            hat = joystick_list[j].get_hat(h)
            print("hat", h, "value", hat)

        balls = joystick_list[j].get_numballs()
        print("balls (not supported yet)", balls)

        for b in range(balls):
            ball = joystick_list[j].get_ball(b)
            print("ball", b, "value", ball)


def get_joy_entry(input_entry):
    global joystick_count
    global joystick_list

    if "joy" not in input_entry:
        if "joy_name" in input_entry:
            for c in range(joystick_count):
                if input_entry["joy_name"] == joystick_list[c].get_name():
                    input_entry["joy"] = c
                    print(input_entry["joy_name"], "is joystick", input_entry["joy"])
                    break
        elif "joy_guid" in input_entry:
            for c in range(joystick_count):
                if input_entry["joy_guid"] == joystick_list[c].get_guid():
                    input_entry["joy"] = c
                    print(input_entry["joy_guid"], "is joystick", input_entry["joy"])
                    break
        else:
            print("You must provide a valid \"joy\", \"joy_name\" or \"joy_guid\" for joystick entries")
            sys.exit(-1)

    return input_entry


def send_event(sock_index, key, data):
    sock_list[sock_index].sendall(key.encode('utf_8'))
    sock_list[sock_index].sendall("\n".encode('utf_8'))
    sock_list[sock_index].sendall(data.encode('utf_8'))
    sock_list[sock_index].sendall("\n".encode('utf_8'))


first = True
sock_list = []
index = 0
action_list = {}
mouse_X = None
mouse_Y = None
mouse = {}
joy_axis = []
# joy_ball = []
joy_hat = []
joy_button = []

init_joystick()

for a in sys.argv:
    if first is True:
        first = False  # skip first arg (executable file name)
    else:
        input_json = None
        with open(a) as json_file:
            input_json = json.load(json_file)

        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        print("Connect to", input_json["server"]["ip"], input_json["server"]["port"])
        retry = True
        while retry is True:
            retry = False
            try:
                sock_list[index].connect((input_json["server"]["ip"], int(input_json["server"]["port"])))
            except ConnectionRefusedError:
                print("Connect failed, retry...")
                time.sleep(1)
                retry = True
        print("Connected to", input_json["server"]["ip"], input_json["server"]["port"])

        if "key" in input_json:
            for key_name in input_json["key"]:
                print(key_name)
                action_list[pygame.key.key_code(key_name)] = [index, input_json["key"][key_name]["action"],
                                                              input_json["key"][key_name]["value"]]

        if "mouse" in input_json:
            if "X" in input_json["mouse"]:
                mouse_X = {"index": index, "action": input_json["mouse"]["X"]["action"],
                           "max": input_json["mouse"]["X"]["max"],
                           "min": input_json["mouse"]["X"]["min"],
                           "factor": input_json["mouse"]["X"]["factor"]}

            if "Y" in input_json["mouse"]:
                mouse_Y = {"index": index, "action": input_json["mouse"]["Y"]["action"],
                           "max": input_json["mouse"]["Y"]["max"],
                           "min": input_json["mouse"]["Y"]["min"],
                           "factor": input_json["mouse"]["X"]["factor"]}

            if "left" in input_json["mouse"]:
                mouse["left"] = {"index": index, "action": input_json["mouse"]["left"]["action"],
                                 "value": input_json["mouse"]["left"]["value"]}

            if "right" in input_json["mouse"]:
                mouse["right"] = {"index": index, "action": input_json["mouse"]["right"]["action"],
                                  "value": input_json["mouse"]["right"]["value"]}

            if "middle" in input_json["mouse"]:
                mouse["middle"] = {"index": index, "action": input_json["mouse"]["middle"]["action"],
                                   "value": input_json["mouse"]["middle"]["value"]}

            if "up" in input_json["mouse"]:
                mouse["up"] = {"index": index, "action": input_json["mouse"]["up"]["action"],
                               "value": input_json["mouse"]["up"]["value"]}

            if "down" in input_json["mouse"]:
                mouse["down"] = {"index": index, "action": input_json["mouse"]["down"]["action"],
                                 "value": input_json["mouse"]["down"]["value"]}

        if "joy" in input_json:
            for key_name in input_json["joy"]:
                if key_name == "axis":
                    for entry in input_json["joy"]["axis"]:
                        complete_entry = get_joy_entry(entry)
                        joy_axis.append({"index": index, "entry": complete_entry, "value": 0.0, "ready_to_send": False})
                # if key_name == "ball":
                #    for entry in input_json["joy"]["ball"]:
                #        complete_entry = get_joy_entry(entry)
                #        joy_ball.append({"index": index, "entry": complete_entry})
                if key_name == "hat":
                    for entry in input_json["joy"]["hat"]:
                        complete_entry = get_joy_entry(entry)
                        joy_hat.append({"index": index, "entry": complete_entry, "action": None})
                if key_name == "button":
                    for entry in input_json["joy"]["button"]:
                        complete_entry = get_joy_entry(entry)
                        joy_button.append({"index": index, "entry": complete_entry})

        index = index + 1

pygame.display.init
pygame.display.set_caption('NetInput')

# PyGame virtual mouse
if len(mouse) > 0:
    main_window = pygame.display.set_mode((400, 400))
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
else:
    main_window = pygame.display.set_mode((300, 10))

current_mouse_x = 0
current_mouse_y = 0

send_mouse_x = False
send_mouse_y = False

send_date = datetime.datetime.now()

while True:
    event = pygame.event.wait()

    # Focus
    if event.type == pygame.WINDOWFOCUSGAINED:
        if len(mouse) > 0:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

    # Keyboard
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if pygame.event.get_grab() is True:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            else:
                pygame.quit()
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], action_list[event.key][2])

    elif event.type == pygame.KEYUP:
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], "0")

    # Mouse buttons
    elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:

        if event.button == 1:
            mouse_button_name = "left"
        if event.button == 2:
            mouse_button_name = "middle"
        if event.button == 3:
            mouse_button_name = "right"
        if event.button == 4:
            mouse_button_name = "up"
        if event.button == 5:
            mouse_button_name = "down"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_button_name in mouse:
                if pygame.event.get_grab() is False:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

                send_event(mouse[mouse_button_name]["index"], mouse[mouse_button_name]["action"],
                           mouse[mouse_button_name]["value"])

        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_button_name in mouse:
                send_event(mouse[mouse_button_name]["index"], mouse[mouse_button_name]["action"], "0")

    # Mouse motion
    elif event.type == pygame.MOUSEMOTION:
        rel = pygame.mouse.get_rel()

        if mouse_X is not None:
            current_mouse_x = max(min(current_mouse_x + (rel[0] * int(mouse_X["factor"])), int(mouse_X["max"])),
                                  int(mouse_X["min"]))
            send_mouse_x = True

        if mouse_Y is not None:
            current_mouse_y = max(min(current_mouse_y + (rel[1] * int(mouse_Y["factor"])), int(mouse_Y["max"])),
                                  int(mouse_Y["min"]))
            send_mouse_y = True

    elif event.type == pygame.JOYAXISMOTION:
        for a in joy_axis:
            if a["entry"]["joy"] == event.joy and a["entry"]["id"] == event.axis and a["value"] != event.value:
                a["value"] = event.value
                a["ready_to_send"] = True
                break
    # elif event.type == pygame.JOYBALLMOTION:
    #    for a in joy_ball:
    #        if a["entry"]["joy"] == event.joy and a["entry"]["id"] == event.ball:
    #            print("ball", event.joy, event.ball, event.value)
    #            break
    elif event.type == pygame.JOYBUTTONDOWN:
        print("JOY",event.joy,"button",event.button)
        for a in joy_button:
            if a["entry"]["joy"] == event.joy and a["entry"]["id"] == event.button:
                send_event(a["index"], a["entry"]["action"], a["entry"]["value"])
                break
    elif event.type == pygame.JOYBUTTONUP:
        for a in joy_button:
            if a["entry"]["joy"] == event.joy and a["entry"]["id"] == event.button:
                send_event(a["index"], a["entry"]["action"], "0")
                break
    elif event.type == pygame.JOYHATMOTION:
        for a in joy_hat:
            if a["entry"]["joy"] == event.joy and a["entry"]["id"] == event.hat:
                if event.value[0] == 1:
                    if a["entry"]["direction"] == "-X":
                        send_event(a["index"], a["entry"]["action"], "0")
                    elif a["entry"]["direction"] == "X":
                        send_event(a["index"], a["entry"]["action"], a["entry"]["value"])

                elif event.value[0] == -1:
                    if a["entry"]["direction"] == "X":
                        send_event(a["index"], a["entry"]["action"], "0")
                    if a["entry"]["direction"] == "-X":
                        send_event(a["index"], a["entry"]["action"], a["entry"]["value"])

                elif event.value[0] == 0:
                    if a["entry"]["direction"] == "-X" or a["entry"]["direction"] == "X":
                        send_event(a["index"], a["entry"]["action"], "0")

                if event.value[1] == 1:
                    if a["entry"]["direction"] == "-Y":
                        send_event(a["index"], a["entry"]["action"], "0")
                    elif a["entry"]["direction"] == "Y":
                        send_event(a["index"], a["entry"]["action"], a["entry"]["value"])

                elif event.value[1] == -1:
                    if a["entry"]["direction"] == "Y":
                        send_event(a["index"], a["entry"]["action"], "0")
                    if a["entry"]["direction"] == "-Y":
                        send_event(a["index"], a["entry"]["action"], a["entry"]["value"])

                elif event.value[1] == 0:
                    if a["entry"]["direction"] == "-Y" or a["entry"]["direction"] == "Y":
                        send_event(a["index"], a["entry"]["action"], "0")

    elif event.type == pygame.QUIT:
        pygame.quit()

    # Avoid spamming network
    if send_date < datetime.datetime.now():
        if send_mouse_x is True:
            send_event(mouse_X["index"], mouse_X["action"], str(current_mouse_x))
            send_mouse_x = False
        if send_mouse_y is True:
            send_event(mouse_Y["index"], mouse_Y["action"], str(current_mouse_y))
            send_mouse_y = False

        for a in joy_axis:
            if a["ready_to_send"] is True:
                send_event(a["index"], a["entry"]["action"], str(a["value"] * float(a["entry"]["factor"])))
                a["ready_to_send"] = False

        send_date = datetime.datetime.now() + datetime.timedelta(milliseconds=10)
