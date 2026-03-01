import asyncio
from mcp.server.fastmcp import FastMCP
from transactional_db import CUSTOMERS_TABLE, ORDERS_TABLE, PRODUCTS_TABLE

mcp = FastMCP("ecommerce_tools")

@mcp.tool()
async def get_customer_info(customer_id: str) -> str:
    """Search for a cutomer using theri unique identifier"""

    customer_info = CUSTOMERS_TABLE.get(customer_id)
    if not customer_id:
        return "Customer not found"

    return str(customer_info)

@mcp.tool()
async def get_order_details(order_id:str) -> str:
    """Get details about a specific order."""
    await asyncio.sleep(1)
    order =  ORDERS_TABLE.get(order_id)
    if not order:
        return f"No order found with ID {order_id}"

    items = [
        PRODUCTS_TABLE[SKU]["name"] for sku in order["items"] if sku in PRODUCTS_TABLE
    ]

    return (
        f"Order ID: {order_id}\n"
        f"Customer ID: {order['customer_id']}\n"
        f"Date: {order['date']}\n"
        f"Status: {order['status']}\n"
        f"Total: ${order['total']:.2f}\n"
        f"Items: {', '.join(items)}"
    )

if __name__ == "__main__":
    mcp.run(transport="stdio")
