# Key names are at https://github.com/pygame/pygame/blob/main/src_c/key.c , in SDL1_scancode_names
import time

import pygame
import json
import sys
import socket
import datetime


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

for a in sys.argv:
    if first is True:
        first = False  # skip first arg (executable file name)
    else:
        input_json = None
        with open(a) as json_file:
            input_json = json.load(json_file)

        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        print("Connect to", input_json["server"]["ip"], input_json["server"]["port"])
        sock_list[index].connect((input_json["server"]["ip"], int(input_json["server"]["port"])))
        print("Connected to", input_json["server"]["ip"], input_json["server"]["port"])

        if "key" in input_json:
            for i in input_json["key"]:
                print(i)
                action_list[pygame.key.key_code(i)] = [index, input_json["key"][i]["action"],
                                                       input_json["key"][i]["value"]]

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

        index = index + 1

pygame.display.init
main_window = pygame.display.set_mode((400, 400))
pygame.display.set_caption('NetInput')

# PyGame virtual mouse
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

current_mouse_x = 0
current_mouse_y = 0

send_date = datetime.datetime.now()

while True:
    event = pygame.event.wait()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], action_list[event.key][2])

    if event.type == pygame.KEYUP:
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], "0")

    if event.type == pygame.MOUSEMOTION:
        rel = pygame.mouse.get_rel()
        print(rel)

        if mouse_X is not None:
            current_mouse_x = max(min(current_mouse_x + (rel[0] * int(mouse_X["factor"])), int(mouse_X["max"])),
                                  int(mouse_X["min"]))
            print(current_mouse_x)

        if mouse_Y is not None:
            current_mouse_y = max(min(current_mouse_y + (rel[1] * int(mouse_Y["factor"])), int(mouse_Y["max"])),
                                  int(mouse_Y["min"]))
            print(current_mouse_y)

    if event.type == pygame.QUIT:
        pygame.quit()

    # Avoid spamming network
    if send_date < datetime.datetime.now():
        send_event(mouse_X["index"], mouse_X["action"], str(current_mouse_x))
        send_event(mouse_Y["index"], mouse_Y["action"], str(current_mouse_y))
        send_date = datetime.datetime.now() + datetime.timedelta(milliseconds=50)
