import pygame
import json
import sys
import socket


def send_event(key, data):
    sock.sendall(key.encode('utf_8'))
    sock.sendall("\n".encode('utf_8'))
    sock.sendall(data.encode('utf_8'))
    sock.sendall("\n".encode('utf_8'))


print(sys.argv[1])

input_data = None
with open(sys.argv[1]) as json_file:
    input_data = json.load(json_file)

pygame.display.init
pygame.font.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connect to", input_data["server"]["ip"], input_data["server"]["port"])
sock.connect((input_data["server"]["ip"], int(input_data["server"]["port"])))

main_window = pygame.display.set_mode((300, 0))
pygame.display.set_caption('NetInput')

action_list = {}
value_list = {}
for i in input_data["key"]:
    action_list[pygame.key.key_code(i)] = input_data["key"][i]["action"]
    value_list[pygame.key.key_code(i)] = input_data["key"][i]["value"]

while True:
    event = pygame.event.wait()

    if event.type == pygame.KEYDOWN:
        if event.key in action_list:
            send_event(action_list[event.key], value_list[event.key])

    if event.type == pygame.KEYUP:
        if event.key in action_list:
            send_event(action_list[event.key], "0")

    if event.type == pygame.QUIT:
        pygame.quit()
