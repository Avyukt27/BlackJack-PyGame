import pygame
import requests
import sys
from io import BytesIO
 
pygame.init()
screen = pygame.display.set_mode((800, 600))

deck_id = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()["deck_id"]

response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
response = requests.get(response.json()["cards"][0]["image"])
img = pygame.image.load(BytesIO(response.content))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(img, (0, 0))
    pygame.display.update()