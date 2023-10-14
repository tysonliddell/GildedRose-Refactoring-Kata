# -*- coding: utf-8 -*-
from typing import List

from gilded_rose.item import Item, advance_item_day


class GildedRose:
    def __init__(self, items: List[Item]):
        # The GildenRose.items property is owned by the Goblin. Do not modify
        # this!
        self.items = items

    def update_quality(self):
        for item in self.items:
            advance_item_day(item)
