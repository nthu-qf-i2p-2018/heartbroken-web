
class NotHaveCardException(Exception):
    def __init__(self, agent, cards_not_in):
        card_str = ', '.join(map(str, cards_not_in))
        self.message = "{} is not in {}!".format(card_str, agent.id)

    def __str__(self):
        return self.message


class PassCardIllegalException(Exception):
    def __init__(self, agent, cards):
        self.message = "{} does not pass card correctly: ".format(agent.id)
        self.message += "3 needed, found {}.".format(len(cards))

    def __str__(self):
        return self.message


class IllegalMoveException(Exception):
    def __init__(self, agent, card):
        self.message = "{} cannot play {}!".format(agent.id, card)

    def __str__(self):
        return self.message
