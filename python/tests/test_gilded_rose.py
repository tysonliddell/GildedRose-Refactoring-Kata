# -*- coding: utf-8 -*-

from typing import List, Tuple

import pytest
from gilded_rose.gilded_rose import GildedRose, Item

AGED_BRIE_ITEM_NAME = "Aged Brie"


def test_item_fields():
    """
    GIVEN: A name, SellIn and Quality value.
    WHEN: An Item object is created with these values.
    THEN: These values should be avaiable as item properties.
    """
    item = Item("foo", 10, 20)
    assert "foo" == item.name
    assert 10 == item.sell_in
    assert 20 == item.quality


@pytest.mark.xfail(reason="Not implemented")
@pytest.mark.parametrize("illegal_quality", [-1, 51])
def test_cannot_create_item_with_out_of_range_quality(illegal_quality):
    """
    GIVEN: A quality not in the range [0, 50].
    WHEN: An Item object is created with this value.
    THEN: An exception should be raised.
    """
    with pytest.raises(Exception):
        Item(
            "foo",
            sell_in=10,
            quality=illegal_quality,
        )


def test_update_quantity_decrements_all_values():
    """
    GIVEN: A generic GildedRose object with multiple items.
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
            Item(name="foo", sell_in=initial_sell_in, quality=initial_quality),
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
