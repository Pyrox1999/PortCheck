import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import socket

random.seed()

pygame.mixer.music.load("song.mp3") #G_P
pygame.mixer.music.play(-1)

level = -2
target = "127.0.0.1"
start_port = 1
end_port = 10
scan_results = []  

def run_scan():
    global scan_results,port
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        result = sock.connect_ex((target, port))
        if result == 0:
            scan_results.append(port)
        sock.close()
        print(port)

def draw():
    global level, target, scan_results,port,start_port,end_port,y
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to scan:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.draw.text(f"Scanning {target} from port {start_port} to {end_port}", center=(400, 130), fontsize=24, color=(25, 200, 255))
        y = 180
        #screen.draw.text("Port: "+str(port), center=(400, 230), fontsize=24, color=(25, 200, 255))
        for port in scan_results:
            screen.draw.text(f"Port {port} is open", center=(400, y), fontsize=24, color=(25, 200, 255))
            y += 25
        #screen.draw.text("Scan complete!", center=(400, y + 30), fontsize=24, color=(25, 200, 255))
        if end_port<1024:
            start_port+=10
            end_port+=10

def on_key_down(key, unicode=None):
    global level, target
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "127.0.0.1"
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        target += unicode

def update():
    global level
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==2:
        run_scan()

pgzrun.go()
