# -*- coding: utf-8 -*-
from typing import List

MIN_QUALITY = 0
MAX_QUALITY = 50
SULFURAS_QUALITY = 80

AGED_BRIE_ITEM_NAME = "Aged Brie"
SULFURAS_ITEM_NAME = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES_ITEM_NAME = "Backstage passes to a TAFKAL80ETC concert"


def advance_day_generic_item(item: "Item"):
    new_quality = item.quality - 1 if item.sell_in > 0 else item.quality - 2
    item.quality = max(new_quality, MIN_QUALITY)
    item.sell_in -= 1


def advance_day_aged_brie(item: "Item"):
    new_quality = item.quality + 1 if item.sell_in > 0 else item.quality + 2
    item.quality = min(new_quality, MAX_QUALITY)
    item.sell_in -= 1


def advance_day_sulfarus(item: "Item"):
    # This item should have its fields unchanged between days
    return


def advance_day_backstage_passes(item: "Item"):
    if item.sell_in <= 0:
        # concert is over, backstage passes are worthless
        item.quality = MIN_QUALITY
    else:
        new_quality = item.quality + 1
        if item.sell_in <= 10:
            new_quality += 1
        if item.sell_in <= 5:
            new_quality += 1
        item.quality = min(new_quality, MAX_QUALITY)
    item.sell_in -= 1


class GildedRose:
    def __init__(self, items: List["Item"]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item_name = item.name
            if item_name == AGED_BRIE_ITEM_NAME:
                advance_day_aged_brie(item)
            elif item_name == SULFURAS_ITEM_NAME:
                advance_day_sulfarus(item)
            elif item_name == BACKSTAGE_PASSES_ITEM_NAME:
                advance_day_backstage_passes(item)
            else:
                advance_day_generic_item(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
