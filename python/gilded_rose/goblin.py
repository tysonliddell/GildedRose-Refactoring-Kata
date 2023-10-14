"""
WARNING: Do not alter the Item class as this belongs to the goblin in the corner
who will insta-rage and one-shot you as he doesn't believe in shared code
ownership!
"""


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
