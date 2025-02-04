import pygame
import requests
from io import BytesIO
 
pygame.init()
screen = pygame.display.set_mode((800, 600))

deck_id = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()["deck_id"]

class Card:
    def __init__(self, response: requests.Response):
        self.position = pygame.Vector2(0, 0)
        self.img = pygame.image.load(BytesIO(requests.get(response.json()["cards"][0]["image"]).content))
        self.img = pygame.transform.scale(self.img, (100, 155))
        self.rect = self.img.get_rect()
    
    def draw(self, window: pygame.Surface):
        window.blit(self.img, self.position)

response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")

card = Card(response)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    card.draw(screen)
    pygame.display.update()