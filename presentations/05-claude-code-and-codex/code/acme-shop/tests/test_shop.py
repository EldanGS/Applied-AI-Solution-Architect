import pytest

from shop import cancel_order, get_order


def test_get_order():
    assert get_order("A-1001")["eta"] == "Oct 12"


def test_cancel_packing_order():
    assert cancel_order("A-1002") == {"cancelled": "A-1002"}


def test_cancel_refuses_shipped_order():
    with pytest.raises(ValueError, match="Offer a return"):
        cancel_order("A-1001")
