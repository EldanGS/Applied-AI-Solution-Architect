from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("shop")
ORDERS = {"A-1001": {"status": "shipped", "eta": "Oct 12"},
          "A-1002": {"status": "packing", "eta": "Oct 15"}}

@mcp.tool()
def get_order(order_id: str) -> dict:
    """Look up ONE order by its ID, e.g. A-1001."""
    if order_id not in ORDERS:
        raise ToolError(f"No order {order_id}. Check the ID.")
    return ORDERS[order_id]

@mcp.tool()
def cancel_order(order_id: str) -> dict:
    """Cancel ONE order by its ID. Only when the customer asks."""
    if get_order(order_id)["status"] == "shipped":
        raise ToolError("Shipped. Offer a return.")
    ORDERS[order_id]["status"] = "cancelled"
    return {"cancelled": order_id}

@mcp.resource("shop://policy", mime_type="text/plain")
def policy() -> str:
    """Acme Shop's cancel and return policy."""
    return "Cancel before shipping. Return within 30 days."

if __name__ == "__main__":
    mcp.run()
