import pygame
import requests
from io import BytesIO

pygame.init()
window = pygame.display.set_mode((800, 600))

CARD_WIDTH: int = 100
CARD_HEIGHT: int = 125
CARD_START_X: int = 20
PLAYER_START_Y: int = window.get_height() - CARD_HEIGHT - 10
DEALER_START_Y: int = 10

deck_id = requests.get(
    "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
).json()["deck_id"]

values: dict[str, int] = {
    "ACE": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "JACK": 10,
    "QUEEN": 10,
    "KING": 10,
}


class Card:
    def __init__(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        response: requests.Response,
    ) -> None:
        """Creates a Card object

        Args:
            x_position (int): The X position of the Card
            y_position (int): The Y position of the Card
            width (int): The width of the Card
            height (int): The height of the Card
            response (requests.Response): The Card object's response from the API
        """
        self.position = pygame.Vector2(x_position, y_position)

        self.card = response.json()["cards"][0]

        self.img = pygame.image.load(BytesIO(requests.get(self.card["image"]).content))
        self.img = pygame.transform.scale(self.img, (width, height))

        self.value = self.card["value"]
        self.suit = self.card["suit"]

    def __repr__(self) -> str:
        """The Representation of the Card

        Returns:
            str: VALUE of SUIT
        """
        return f"{self.value} of {self.suit}"

    def draw(self, window: pygame.Surface) -> None:
        """Sraws a card on the game window

        Args:
            window (pygame.Surface): The window to draw on
        """
        window.blit(self.img, self.position)


def draw_card(deck_id: str, player_turn: bool) -> None:
    """Draws a card and places it in either the player or the dealer's hand

    Args:
        deck_id (str): The Deck ID to draw from
        player_turn (bool): If it is the player's turn when called
    """
    if player_turn:
        player_cards.append(
            Card(
                CARD_START_X,
                PLAYER_START_Y,
                CARD_WIDTH,
                CARD_HEIGHT,
                requests.get(
                    f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
                ),
            )
        )
    else:
        dealer_cards.append(
            Card(
                CARD_START_X,
                DEALER_START_Y,
                CARD_WIDTH,
                CARD_HEIGHT,
                requests.get(
                    f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
                ),
            )
        )


def update_screen(window: pygame.Surface) -> None:
    """Draws all game objects on the screen

    Args:
        window (pygame.Surface): The window to draw on
    """
    global player_score, dealer_score

    player_score = 0
    dealer_score = 0

    window.fill((0, 0, 0))

    for index, player_card in enumerate(player_cards):
        player_score += values[player_card.value]
        player_card.position.x = index * CARD_WIDTH + CARD_START_X
        player_card.draw(window)

    for index, dealer_card in enumerate(dealer_cards):
        dealer_score += values[dealer_card.value]
        dealer_card.position.x = index * CARD_WIDTH + CARD_START_X
        dealer_card.draw(window)

    pygame.display.update()


player_score: int = 0
dealer_score: int = 0
player_cards: list[Card] = []
dealer_cards: list[Card] = []

run = True
while run:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        draw_card(deck_id, True)
        draw_card(deck_id, False)

    print(player_score, dealer_score)

    update_screen(window)

pygame.quit()
exit()
