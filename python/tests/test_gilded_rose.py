# -*- coding: utf-8 -*-

from typing import List, Tuple

import pytest
from gilded_rose.gilded_rose import GildedRose, Item

GENERIC_ITEM_NAME = "foo"
AGED_BRIE_ITEM_NAME = "Aged Brie"
SULFURAS_ITEM_NAME = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES_ITEM_NAME = "Backstage passes to a TAFKAL80ETC concert"


def test_item_fields():
    """
    GIVEN: A name, SellIn and Quality value.
    WHEN: An Item object is created with these values.
    THEN: These values should be avaiable as item properties.
    """
    item = Item(GENERIC_ITEM_NAME, 10, 20)
    assert GENERIC_ITEM_NAME == item.name
    assert 10 == item.sell_in
    assert 20 == item.quality


@pytest.mark.xfail(reason="Not implemented")
@pytest.mark.parametrize("illegal_quality", [-1, 51])
def test_cannot_create_generic_item_with_out_of_range_quality(illegal_quality):
    """
    GIVEN: A quality not in the range [0, 50].
    WHEN: An Item object is created with this value.
    THEN: An exception should be raised.
    """
    with pytest.raises(Exception):
        Item(
            GENERIC_ITEM_NAME,
            sell_in=10,
            quality=illegal_quality,
        )


def test_update_quantity_decrements_all_values():
    """
    GIVEN: A GildedRose object with multiple generic items.
    WHEN: update_quantity is called.
    THEN: The sell_in and quantity properties of all items should be decremented by 1.
    """
    gilded_rose = GildedRose(
        [
            Item("foo", 10, 20),
            Item("bar", 30, 40),
        ]
    )

    gilded_rose.update_quality()
    item1, item2 = gilded_rose.items
    assert "foo" == item1.name
    assert 9 == item1.sell_in
    assert 19 == item1.quality
    assert "bar" == item2.name
    assert 29 == item2.sell_in
    assert 39 == item2.quality

    gilded_rose.update_quality()
    item1, item2 = gilded_rose.items
    assert "foo" == item1.name
    assert 8 == item1.sell_in
    assert 18 == item1.quality
    assert "bar" == item2.name
    assert 28 == item2.sell_in
    assert 38 == item2.quality


@pytest.mark.parametrize(
    ("initial_sell_in", "initial_quality", "expected_progression"),
    [
        (4, 3, [(4, 3), (3, 2), (2, 1), (1, 0), (0, 0), (-1, 0)]),
        (3, 3, [(3, 3), (2, 2), (1, 1), (0, 0), (-1, 0)]),
        (3, 4, [(3, 4), (2, 3), (1, 2), (0, 1), (-1, 0), (-2, 0)]),
        (2, 4, [(2, 4), (1, 3), (0, 2), (-1, 0), (-2, 0)]),
        (1, 5, [(1, 5), (0, 4), (-1, 2), (-2, 0), (-3, 0)]),
    ],
)
def test_generic_item_quality_value_progression(
    initial_sell_in: int,
    initial_quality: int,
    expected_progression: List[Tuple[int, int]],
):
    """
    GIVEN: A generic item.
    WHEN: update_quantity is repeatedly called.
    THEN: The quality will reduce to zero, reduce twice as quickly when
          past the sell by date, and never go negative.
    """
    gilded_rose = GildedRose(
        [
            Item(
                name=GENERIC_ITEM_NAME, sell_in=initial_sell_in, quality=initial_quality
            ),
        ]
    )
    item = gilded_rose.items[0]

    for sell_in, quality in expected_progression:
        assert sell_in == item.sell_in
        assert quality == item.quality
        gilded_rose.update_quality()


@pytest.mark.parametrize(
    ("initial_sell_in", "initial_quality", "expected_progression"),
    [
        (3, 0, [(3, 0), (2, 1), (1, 2), (0, 3), (-1, 5), (-2, 7)]),
        (10, 48, [(10, 48), (9, 49), (8, 50), (7, 50)]),
        (3, 48, [(3, 48), (2, 49), (1, 50), (0, 50), (-1, 50)]),
        (2, 48, [(2, 48), (1, 49), (0, 50), (-1, 50)]),
        (1, 48, [(1, 48), (0, 49), (-1, 50), (-2, 50)]),
    ],
)
def test_aged_brie_quality_value_progression(
    initial_sell_in: int,
    initial_quality: int,
    expected_progression: List[Tuple[int, int]],
):
    """
    GIVEN: An "Aged Brie" item.
    WHEN: update_quantity is repeatedly called.
    THEN: The quality will increase, increase twice as quickly when
          past the sell by date, and never go above 50.
    """
    gilded_rose = GildedRose(
        [
            Item(
                name=AGED_BRIE_ITEM_NAME,
                sell_in=initial_sell_in,
                quality=initial_quality,
            ),
        ]
    )
    item = gilded_rose.items[0]

    for sell_in, quality in expected_progression:
        assert sell_in == item.sell_in
        assert quality == item.quality
        gilded_rose.update_quality()


@pytest.mark.xfail(reason="Not implemented")
@pytest.mark.parametrize(
    "illegal_quality",
    [-1, 0, 1, 79, 81],
)
def test_cannot_create_sulfuras_with_invalid_quality(illegal_quality: int):
    """
    GIVEN: A "Sulfuras, Hand of Ragnaros" item.
    WHEN: A Sulfaras item is created with an quality that is not excatly 80.
    THEN: An exception is raised.
    """
    with pytest.raises(Exception):
        Item(
            SULFURAS_ITEM_NAME,
            sell_in=10,
            quality=illegal_quality,
        )


@pytest.mark.parametrize(
    ("initial_sell_in", "initial_quality", "expected_progression"),
    [
        (1, 80, [(1, 80), (1, 80), (1, 80)]),
        (0, 80, [(0, 80), (0, 80), (0, 80)]),
        (-1, 80, [(-1, 80), (-1, 80), (-1, 80)]),
    ],
)
def test_sulfuras_quality_value_progression(
    initial_sell_in: int,
    initial_quality: int,
    expected_progression: List[Tuple[int, int]],
):
    """
    GIVEN: A "Sulfuras, Hand of Ragnaros" item.
    WHEN: update_quantity is repeatedly called.
    THEN: The quality is always 80.
    """
    gilded_rose = GildedRose(
        [
            Item(
                name=SULFURAS_ITEM_NAME,
                sell_in=initial_sell_in,
                quality=initial_quality,
            ),
        ]
    )
    item = gilded_rose.items[0]

    for sell_in, quality in expected_progression:
        assert sell_in == item.sell_in
        assert quality == item.quality
        gilded_rose.update_quality()


@pytest.mark.xfail(reason="Not implemented")
def test_cannot_create_backstage_passes_with_positive_quality_when_expired():
    """
    GIVEN:
    WHEN: A Backstage Passes item is created with negative sell_in value and
          positive quality.
    THEN: An exception is raised.
    """
    with pytest.raises(Exception):
        Item(
            BACKSTAGE_PASSES_ITEM_NAME,
            sell_in=-1,
            quality=1,
        )


@pytest.mark.parametrize(
    ("initial_sell_in", "initial_quality", "expected_progression"),
    [
        (12, 0, [(12, 0), (11, 1), (10, 2), (9, 4), (8, 6)]),
        (6, 0, [(6, 0), (5, 2), (4, 5), (3, 8)]),
        (2, 10, [(2, 10), (1, 13), (0, 16), (-1, 0), (-2, 0)]),
    ],
)
def test_backstage_passes_quality_value_progression(
    initial_sell_in: int,
    initial_quality: int,
    expected_progression: List[Tuple[int, int]],
):
    """
    GIVEN: A Backstage Passes item.
    WHEN: update_quantity is repeatedly called.
    THEN: - The quality will increase by 1 when there are > 10 days to go,
          - The quality will increase by 2 when 5 < sell_in <= 10.
          - The quality will increase by 3 when 0 < sell_in <= 5.
          - The quality will drop to zero when sell_in <= 0.
    """
    gilded_rose = GildedRose(
        [
            Item(
                name=BACKSTAGE_PASSES_ITEM_NAME,
                sell_in=initial_sell_in,
                quality=initial_quality,
            ),
        ]
    )
    item = gilded_rose.items[0]

    for sell_in, quality in expected_progression:
        assert sell_in == item.sell_in
        assert quality == item.quality
        gilded_rose.update_quality()
