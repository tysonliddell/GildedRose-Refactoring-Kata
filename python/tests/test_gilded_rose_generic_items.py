# -*- coding: utf-8 -*-

import pytest
from gilded_rose.gilded_rose import GildedRose, Item


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


def test_quality_value_is_never_negative():
    """
    GIVEN: An item with non-negative quality.
    WHEN: update_quantity is repeatedly called.
    THEN: The quality will reduce to zero, and never go negative.
    """
    gilded_rose = GildedRose(
        [
            Item(name="foo", sell_in=10, quality=3),
        ]
    )
    item = gilded_rose.items[0]

    gilded_rose.update_quality()
    assert 2 == item.quality
    gilded_rose.update_quality()
    assert 1 == item.quality
    gilded_rose.update_quality()
    assert 0 == item.quality

    # the quality reach 0 in the previous call, it should remain zero with this
    # call
    gilded_rose.update_quality()
    assert 0 == item.quality


def test_quality_decreases_twice_as_fast_after_sell_by_date():
    """
    GIVEN: An item's sell_in value is <= 0.
    WHEN: update_quantity is called.
    THEN: The quality will reduce twice as fast (-2 instead of -1).
    """
    gilded_rose = GildedRose(
        [
            Item(name="foo", sell_in=2, quality=20),
        ]
    )
    item = gilded_rose.items[0]
    assert 2 == item.sell_in
    assert 20 == item.quality

    gilded_rose.update_quality()
    assert 1 == item.sell_in
    assert 19 == item.quality

    gilded_rose.update_quality()
    assert 0 == item.sell_in
    assert 18 == item.quality

    gilded_rose.update_quality()
    assert -1 == item.sell_in
    assert 16 == item.quality

    gilded_rose.update_quality()
    assert -2 == item.sell_in
    assert 14 == item.quality
