from enum import Enum

from gilded_rose.goblin import Item

MIN_QUALITY = 0
MAX_QUALITY = 50


class ItemType(Enum):
    GENERIC_ITEM = 0
    AGED_BRIE = 1
    SULFURAS = 2
    BACKSTAGE_PASSES = 3
    CONJURED = 4

    @classmethod
    def from_item(cls, item: Item) -> "ItemType":
        if "aged brie" in item.name.lower():
            return cls.AGED_BRIE
        if "sulfuras" in item.name.lower():
            return cls.SULFURAS
        if "backstage passes" in item.name.lower():
            return cls.BACKSTAGE_PASSES
        if "conjured" in item.name.lower():
            return cls.CONJURED
        return cls.GENERIC_ITEM


def advance_item_day(item: Item):
    item_type = ItemType.from_item(item)
    if item_type == ItemType.AGED_BRIE:
        advance_day_aged_brie(item)
    elif item_type == ItemType.SULFURAS:
        advance_day_sulfarus(item)
    elif item_type == ItemType.BACKSTAGE_PASSES:
        advance_day_backstage_passes(item)
    elif item_type == ItemType.CONJURED:
        advance_day_conjured_item(item)
    else:
        advance_day_generic_item(item)


def advance_day_generic_item(item: Item):
    new_quality = item.quality - 1 if item.sell_in > 0 else item.quality - 2
    item.quality = max(new_quality, MIN_QUALITY)
    item.sell_in -= 1


def advance_day_conjured_item(item: Item):
    # Conjured items degrade in quality twice as fast as generic items.
    new_quality = item.quality - 2 if item.sell_in > 0 else item.quality - 4
    item.quality = max(new_quality, MIN_QUALITY)
    item.sell_in -= 1


def advance_day_aged_brie(item: Item):
    new_quality = item.quality + 1 if item.sell_in > 0 else item.quality + 2
    item.quality = min(new_quality, MAX_QUALITY)
    item.sell_in -= 1


def advance_day_sulfarus(item: Item):
    # This item should have its fields unchanged between days
    return


def advance_day_backstage_passes(item: Item):
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
