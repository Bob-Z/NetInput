import pygame
import json
import sys
import socket


def send_event(sock_index, key, data):
    sock_list[sock_index].sendall(key.encode('utf_8'))
    sock_list[sock_index].sendall("\n".encode('utf_8'))
    sock_list[sock_index].sendall(data.encode('utf_8'))
    sock_list[sock_index].sendall("\n".encode('utf_8'))


first = True
sock_list = []
index = 0
action_list = {}

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

        for i in input_json["key"]:
            print(i)
            action_list[pygame.key.key_code(i)] = [index, input_json["key"][i]["action"],
                                                   input_json["key"][i]["value"]]
        index = index + 1

pygame.display.init
main_window = pygame.display.set_mode((300, 0))
pygame.display.set_caption('NetInput')

while True:
    event = pygame.event.wait()

    if event.type == pygame.KEYDOWN:
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], action_list[event.key][2])

    if event.type == pygame.KEYUP:
        if event.key in action_list:
            send_event(action_list[event.key][0], action_list[event.key][1], "0")

    if event.type == pygame.QUIT:
        pygame.quit()
