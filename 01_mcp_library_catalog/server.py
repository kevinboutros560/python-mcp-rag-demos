from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Campus Library Catalog")

BOOKS = [
    {
        "id": "B101",
        "title": "Python for Beginners",
        "topic": "Programming",
        "status": "Available",
        "shelf": "A2",
    },
    {
        "id": "B102",
        "title": "Statistics Made Simple",
        "topic": "Mathematics",
        "status": "On loan",
        "shelf": "B1",
    },
    {
        "id": "B103",
        "title": "Introduction to Web Development",
        "topic": "Programming",
        "status": "Available",
        "shelf": "A3",
    },
]


@mcp.tool()
def search_books(query: str) -> dict[str, list[dict[str, str]]]:
    """Search the library catalog by title or topic."""
    term = query.strip().casefold()
    if not term:
        return {"books": []}

    matches = [
        book
        for book in BOOKS
        if term in book["title"].casefold() or term in book["topic"].casefold()
    ]
    return {"books": matches}


@mcp.tool()
def get_book_status(book_id: str) -> dict[str, str]:
    """Look up a book's availability and shelf using its catalog ID."""
    requested_id = book_id.strip().upper()
    for book in BOOKS:
        if book["id"] == requested_id:
            return book
    return {"error": f"No book found with ID {requested_id!r}."}


if __name__ == "__main__":
    mcp.run(transport="stdio")
