import pygame
import requests
from io import BytesIO

pygame.init()
window = pygame.display.set_mode((800, 600))

CARD_WIDTH: int = 100
CARD_HEIGHT: int = 125
PLAYER_START_X: int = 20
PLAYER_START_Y: int = window.get_height() - CARD_HEIGHT - 10

deck_id = requests.get(
    "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
).json()["deck_id"]


class Card:
    def __init__(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        response: requests.Response,
    ) -> None:
        self.position = pygame.Vector2(x_position, y_position)

        self.card = response.json()["cards"][0]

        self.img = pygame.image.load(BytesIO(requests.get(self.card["image"]).content))
        self.img = pygame.transform.scale(self.img, (width, height))

        self.value = self.card["value"]

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.img, self.position)


def draw_card(deck_id: str) -> requests.Response:
    return requests.get(
        f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
    )


def update_screen(window: pygame.Surface) -> None:
    for index, player_card in enumerate(player_cards):
        player_card.position.x = index * CARD_WIDTH + PLAYER_START_X
        player_card.draw(window)
    pygame.display.update()


player_cards: list[Card] = []
player_cards.append(
    Card(PLAYER_START_X, PLAYER_START_Y, CARD_WIDTH, CARD_HEIGHT, draw_card(deck_id))
)
player_cards.append(
    Card(PLAYER_START_X, PLAYER_START_Y, CARD_WIDTH, CARD_HEIGHT, draw_card(deck_id))
)

run = True
while run:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    update_screen(window)

pygame.quit()
exit()
