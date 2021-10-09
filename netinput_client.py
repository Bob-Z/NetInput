import pygame
import json
import sys
import socket


def send_event(key, data):
    sock.send(key.encode('utf_8'))
    sock.send("\n".encode('utf_8'))
    sock.send(data.encode('utf_8'))
    sock.send("\n".encode('utf_8'))


print(sys.argv[1])

input_data = None
with open(sys.argv[1]) as json_file:
    input_data = json.load(json_file)

pygame.display.init
pygame.font.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((input_data["server"]["ip"], int(input_data["server"]["port"])))

main_window = pygame.display.set_mode((300, 0))
pygame.display.set_caption('NetInput')

input_list = {}
for i in input_data["key"]:
    input_list[pygame.key.key_code(i)] = input_data["key"][i]

while True:
    event = pygame.event.wait()

    if event.type == pygame.KEYDOWN:
        if event.key in input_list:
            send_event(input_list[event.key], "1")

    if event.type == pygame.KEYUP:
        if event.key in input_list:
            send_event(input_list[event.key], "0")

    if event.type == pygame.QUIT:
        pygame.quit()
