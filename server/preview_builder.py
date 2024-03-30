

from typing import List

def build_preview(unpaired: List[str], pairings: List[tuple[str, str]], email_content: str) -> str:

    preview = "<h1>Preview</h1>"

    if len(pairings) > 0:
        preview += "<h2>Pairings</h2>"
        preview += "<ul>"
        for p1, p2 in pairings:
            preview += f"<li>{p1} - {p2}</li>"
        preview += "</ul>"

    if len(unpaired) > 0:
        preview += "<h2>Unpaired</h2>"
        preview += "<ul>"
        for u in unpaired:
            preview += f"<li>{u}</li>"
        preview += "</ul>"
        
    preview += f"<h2>Email Content</h2><p>{email_content}</p>"

    return preview
