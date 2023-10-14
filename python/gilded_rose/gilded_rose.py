# -*- coding: utf-8 -*-
from typing import List

MIN_QUALITY = 0
MAX_QUALITY = 50
SULFURAS_QUALITY = 80

AGED_BRIE_ITEM_NAME = "Aged Brie"
SULFURAS_ITEM_NAME = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES_ITEM_NAME = "Backstage passes to a TAFKAL80ETC concert"


def get_next_day_quality_generic_item(item: "Item") -> int:
    new_quality = item.quality - 1 if item.sell_in > 0 else item.quality - 2
    return max(new_quality, MIN_QUALITY)


def get_next_day_quality_aged_brie(item: "Item") -> int:
    new_quality = item.quality + 1 if item.sell_in > 0 else item.quality + 2
    return min(new_quality, MAX_QUALITY)


def get_next_day_quality_backstage_passes(item: "Item") -> int:
    if item.sell_in <= 0:
        # concert is over, backstage passes are worthless
        return MIN_QUALITY

    new_quality = item.quality + 1
    if item.sell_in <= 10:
        new_quality += 1
    if item.sell_in <= 5:
        new_quality += 1

    return min(new_quality, MAX_QUALITY)


class GildedRose:
    def __init__(self, items: List["Item"]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item_name = item.name
            if item_name == AGED_BRIE_ITEM_NAME:
                item.quality = get_next_day_quality_aged_brie(item)
                item.sell_in -= 1
            elif item_name == SULFURAS_ITEM_NAME:
                item.quality = SULFURAS_QUALITY
            elif item_name == BACKSTAGE_PASSES_ITEM_NAME:
                item.quality = get_next_day_quality_backstage_passes(item)
                item.sell_in -= 1
            else:
                item.quality = get_next_day_quality_generic_item(item)
                item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
