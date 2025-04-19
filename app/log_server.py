import os
from fastmcp import FastMCP

mcp = FastMCP("troubleshoot", host="0.0.0.0", port=4000)

@mcp.resource("log://{path}")
def fetch(path: str) -> str:
    """
    • If *path* points to a file ⇒ return its last 400 lines.
    • If *path* points to a directory or is empty ⇒ return a directory listing.
    """
    base = "/var/log"
    target = os.path.join(base, path)

    # when client calls log://  (empty path) we list /var/log
    if path == "" or os.path.isdir(target):
        entries = os.listdir(target if path else base)
        return "\n".join(sorted(entries))

    try:
        with open(target, "r", encoding="utf‑8", errors="ignore") as f:
            return "".join(f.readlines()[-400:])
    except FileNotFoundError:
        return f"[error] {target} not found"

if __name__ == "__main__":
    mcp.run(transport="sse")
