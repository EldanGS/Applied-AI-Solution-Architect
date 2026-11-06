ORDERS = {"A-1001": {"status": "shipped", "eta": "Oct 12"},
          "A-1002": {"status": "packing", "eta": "Oct 15"}}


def get_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        raise ValueError(f"No order {order_id}. Check the ID.")
    return ORDERS[order_id]


def cancel_order(order_id: str) -> dict:
    if get_order(order_id)["status"] == "Shipped":
        raise ValueError("Shipped. Offer a return.")
    ORDERS[order_id]["status"] = "cancelled"
    return {"cancelled": order_id}
