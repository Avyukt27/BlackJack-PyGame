import pygame
import requests
from io import BytesIO
 
pygame.init()
window = pygame.display.set_mode((800, 600))

deck_id = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()["deck_id"]

class Card:
    def __init__(self, response: requests.Response) -> None:
        self.position = pygame.Vector2(0, 0)
        self.img = pygame.image.load(BytesIO(requests.get(response.json()["cards"][0]["image"]).content))
        self.img = pygame.transform.scale(self.img, (100, 155))
        self.rect = self.img.get_rect()
    
    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.img, self.position)

def draw_card(deck_id: str) -> requests.Response:
    return requests.get(f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")

def update_screen(window: pygame.Surface) -> None:
    card.draw(window)
    pygame.display.update()

card = Card(draw_card(deck_id))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    update_screen(window)

pygame.quit()
exit()