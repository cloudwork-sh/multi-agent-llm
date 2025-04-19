import asyncio, requests
from fastmcp import Client
from fastmcp.client.transports import SSETransport

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL       = "mistral"

agents = {                    # unchanged …
    "project_manager": "You are a senior project manager. …",
    "solutions_architect": "You are a senior solutions architect. …",
    "developer": "You are a senior backend developer. …",
    "devops": "You are a DevOps engineer. …",
}

# ------------------------------------------------------------------
# read‑only log snippet from the other container
# ------------------------------------------------------------------
async def fetch_logs() -> str:
    url = "http://logserver:4000/sse"
    async with Client(SSETransport(url)) as c:
        # 1) list what exists
        listing = await c.read_resource("log://.")
        print("🗂  /var/log contains:\n", listing[0].text)

        # 2) choose a default file that *does* exist on macOS
        logfile = "system.log" if "system.log" in listing[0].text else "install.log"
        res = await c.read_resource(f"log://{logfile}")
        return res[0].text

def run_agent(role, system_prompt, text):
    print(f"\n🧠 {role.upper()} responding…\n")
    prompt = f"{system_prompt}\n\nHere is your input:\n{text}"
    r = requests.post(OLLAMA_URL, json={"model": MODEL,
                                        "prompt": prompt,
                                        "stream": False},
                      timeout=120)
    r.raise_for_status()
    out = r.json()["response"]
    print(out)
    return out
    

def main():
    log_tail  = asyncio.run(fetch_logs())
    user_goal = input("🎯 Enter your idea or request: ")

    prompt = f"----- syslog tail -----\n{log_tail}\n----- end -----\n\n{user_goal}"
    pm   = run_agent("project_manager",    agents["project_manager"],    prompt)
    sa   = run_agent("solutions_architect", agents["solutions_architect"], pm)
    dev  = run_agent("developer",          agents["developer"],          sa)
    run_agent("devops",                    agents["devops"],             dev)

    print("\n✅ All agents completed!\n")

if __name__ == "__main__":
    main()
