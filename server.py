import subprocess
from fastmcp import FastMCP

mcp = FastMCP("Windows Universal MCP")

# -------------------------------
# CLI Tools
# -------------------------------
@mcp.tool()
def run_command(command: str):
    """Execute PowerShell command."""
    if not command:
        return "Error: No command provided"
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True, text=True, timeout=600
        )
        return result.stdout or result.stderr or f"Command completed with code {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error executing PowerShell: {e}"

@mcp.tool()
def run_cmd(command: str):
    """Execute CMD command."""
    if not command:
        return "Error: No command provided"
    try:
        result = subprocess.run(
            ["cmd", "/c", command],
            capture_output=True, text=True, timeout=600
        )
        return result.stdout or result.stderr or f"Command completed with code {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error executing CMD: {e}"

# -------------------------------
# Lazy import function for heavy libraries
# -------------------------------
def lazy_imports():
    global pyautogui, pygetwindow, pyperclip, webbrowser, time
    import pyautogui
    import pygetwindow as gw
    import pyperclip
    import webbrowser
    import time

# -------------------------------
# GUI Tools
# -------------------------------
@mcp.tool()
def move_mouse(x: int, y: int, duration: float = 0.3):
    lazy_imports()
    pyautogui.moveTo(x, y, duration=duration)
    return f"Mouse moved to ({x},{y})"

@mcp.tool()
def click(x: int = None, y: int = None, button: str = "left"):
    lazy_imports()
    if x is not None and y is not None:
        pyautogui.click(x, y, button=button)
    else:
        pyautogui.click(button=button)
    return f"{button.capitalize()} click at ({x or 'current'}, {y or 'current'})"

@mcp.tool()
def type_text(text: str, interval: float = 0.05):
    lazy_imports()
    pyautogui.write(text, interval=interval)
    return f"Typed: {text}"

@mcp.tool()
def press_key(key: str):
    lazy_imports()
    pyautogui.press(key)
    return f"Pressed key: {key}"

@mcp.tool()
def scroll(amount: int):
    lazy_imports()
    pyautogui.scroll(amount)
    return f"Scrolled by {amount} units"

@mcp.tool()
def take_screenshot(path: str = "screenshot.png"):
    lazy_imports()
    pyautogui.screenshot(path)
    return f"Screenshot saved to {path}"

@mcp.tool()
def get_screen_size():
    lazy_imports()
    w, h = pyautogui.size()
    return {"width": w, "height": h}

# -------------------------------
# Clipboard Tools
# -------------------------------
@mcp.tool()
def get_clipboard():
    lazy_imports()
    return pyperclip.paste()

@mcp.tool()
def set_clipboard(text: str):
    lazy_imports()
    pyperclip.copy(text)
    return "Clipboard updated."

# -------------------------------
# Window Management
# -------------------------------
@mcp.tool()
def list_windows():
    lazy_imports()
    return [w.title for w in gw.getAllWindows() if w.title]

@mcp.tool()
def focus_window(title: str):
    lazy_imports()
    try:
        gw.getWindowsWithTitle(title)[0].activate()
        return f"Focused window: {title}"
    except IndexError:
        return f"Window '{title}' not found."

@mcp.tool()
def move_window(title: str, x: int, y: int):
    lazy_imports()
    try:
        win = gw.getWindowsWithTitle(title)[0]
        win.moveTo(x, y)
        return f"Moved '{title}' to ({x},{y})"
    except IndexError:
        return f"Window '{title}' not found."

@mcp.tool()
def resize_window(title: str, width: int, height: int):
    lazy_imports()
    try:
        win = gw.getWindowsWithTitle(title)[0]
        win.resizeTo(width, height)
        return f"Resized '{title}' to {width}x{height}"
    except IndexError:
        return f"Window '{title}' not found."

@mcp.tool()
def close_window(title: str):
    lazy_imports()
    try:
        gw.getWindowsWithTitle(title)[0].close()
        return f"Closed window: {title}"
    except IndexError:
        return f"Window '{title}' not found."

# -------------------------------
# Application & High-Level Automation
# -------------------------------
@mcp.tool()
def open_application(app_name: str):
    lazy_imports()
    known_apps = {
        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "notepad": "notepad.exe",
        "explorer": "explorer.exe"
    }
    app = known_apps.get(app_name.lower(), app_name)
    try:
        subprocess.Popen(app)
        return f"Opened application: {app_name}"
    except Exception as e:
        return f"Error opening {app_name}: {e}"

@mcp.tool()
def perform_action(task_description: str):
    """
    High-level AI automation tool.
    AI can use CLI + GUI to perform tasks like:
    'Open Brave, go to hianime.to, search One Piece, play episode 43'
    """
    lazy_imports()
    try:
        desc = task_description.lower()

        # Step 1: Open browser
        if "brave" in desc:
            open_application("brave")
            time.sleep(0.5)
        elif "chrome" in desc:
            open_application("chrome")
            time.sleep(0.5)
        elif "edge" in desc:
            open_application("edge")
            time.sleep(0.5)

        # Step 2: Navigate to website
        for word in desc.split():
            if any(x in word for x in [".com", ".to", ".net", ".org"]):
                webbrowser.open(word)
                time.sleep(0.5)

        # Step 3: Perform search if mentioned
        if "search" in desc:
            query = desc.split("search")[-1].strip()
            pyautogui.hotkey("ctrl", "l")
            time.sleep(0.1)
            pyautogui.typewrite(query)
            pyautogui.press("enter")

        return f"Performed action: {task_description}"
    except Exception as e:
        return f"Error performing action: {e}"

@mcp.tool()
def read_file(path: str):
    """Reads the content of a file at the given path."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Content of {path}:\n\n{content}"
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error reading file: {e}"

# -------------------------------
# Tool List
# -------------------------------
@mcp.tool()
def list_tools():
    return """
Available Tool Categories:

1️⃣ CLI COMMANDS:
   - run_command(command)
   - run_cmd(command)

2️⃣ GUI CONTROL:
   - move_mouse(x, y)
   - click(x, y, button)
   - type_text(text)
   - press_key(key)
   - scroll(amount)
   - take_screenshot(path)
   - get_screen_size()

3️⃣ CLIPBOARD:
   - get_clipboard()
   - set_clipboard(text)

4️⃣ WINDOW MANAGEMENT:
   - list_windows()
   - focus_window(title)
   - move_window(title, x, y)
   - resize_window(title, width, height)
   - close_window(title)

5️⃣ APPLICATION & AUTOMATION:
   - open_application(app_name)
   - perform_action(task_description)
   - read_file(path)
"""

# -------------------------------
# Main entry point — auto-start
# -------------------------------
if __name__ == "__main__":
    import logging
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Windows Universal MCP (stdio mode)")
    # ✅ DO NOT RUN MANUALLY — AI will spawn and control it
    mcp.run(transport="stdio")
