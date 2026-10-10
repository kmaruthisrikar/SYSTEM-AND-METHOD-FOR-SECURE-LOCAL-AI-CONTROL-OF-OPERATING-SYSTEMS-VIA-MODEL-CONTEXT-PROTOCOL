import subprocess
import os
import glob
from pathlib import Path
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
    global pyautogui, gw, pyperclip, webbrowser, time, psutil, Image, pytesseract
    import pyautogui
    import pygetwindow as gw
    import pyperclip
    import webbrowser
    import time
    import psutil
    from PIL import Image
    import pytesseract

def lazy_selenium():
    global webdriver, By, Keys, Select, ChromeDriverManager, EdgeChromiumDriverManager
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

# -------------------------------
# GUI & Input Tools
# -------------------------------
@mcp.tool()
def move_mouse(x: int, y: int, duration: float = 0.3):
    """Move the mouse cursor to specific screen coordinates (x, y)."""
    lazy_imports()
    pyautogui.moveTo(x, y, duration=duration)
    return f"Mouse moved to ({x},{y})"

@mcp.tool()
def click(x: int = None, y: int = None, button: str = "left"):
    """Click at coordinates (x, y) or at current cursor position if omitted."""
    lazy_imports()
    if x is not None and y is not None:
        pyautogui.click(x, y, button=button)
    else:
        pyautogui.click(button=button)
    return f"{button.capitalize()} click at ({x or 'current'}, {y or 'current'})"

@mcp.tool()
def double_click(x: int = None, y: int = None):
    """Double-click at coordinates (x, y) or at current mouse position."""
    lazy_imports()
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()
    return f"Double click performed at ({x or 'current'}, {y or 'current'})"

@mcp.tool()
def right_click(x: int = None, y: int = None):
    """Right-click at coordinates (x, y) or at current mouse position."""
    lazy_imports()
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()
    return f"Right click performed at ({x or 'current'}, {y or 'current'})"

@mcp.tool()
def drag_mouse(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
    """Drag the mouse from (start_x, start_y) to (end_x, end_y)."""
    lazy_imports()
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(end_x, end_y, duration=duration)
    return f"Mouse dragged from ({start_x},{start_y}) to ({end_x},{end_y})"

@mcp.tool()
def type_text(text: str, interval: float = 0.05):
    """Type out the specified string with typing interval delay."""
    lazy_imports()
    pyautogui.write(text, interval=interval)
    return f"Typed: {text}"

@mcp.tool()
def press_key(key: str):
    """Press a single key (e.g., 'enter', 'esc', 'tab', 'backspace')."""
    lazy_imports()
    pyautogui.press(key)
    return f"Pressed key: {key}"

@mcp.tool()
def press_hotkey(keys: list[str]):
    """Press a sequence of keys simultaneously (e.g., ['ctrl', 'c'] or ['win', 'r'])."""
    lazy_imports()
    pyautogui.hotkey(*keys)
    return f"Pressed hotkey: {' + '.join(keys)}"

@mcp.tool()
def scroll(amount: int):
    """Scroll mouse wheel (positive for up, negative for down)."""
    lazy_imports()
    pyautogui.scroll(amount)
    return f"Scrolled by {amount} units"

@mcp.tool()
def take_screenshot(path: str = "screenshot.png"):
    """Capture full desktop screenshot and save to path."""
    lazy_imports()
    pyautogui.screenshot(path)
    return f"Screenshot saved to {os.path.abspath(path)}"

@mcp.tool()
def get_screen_size():
    """Get width and height of primary monitor."""
    lazy_imports()
    w, h = pyautogui.size()
    return {"width": w, "height": h}

# -------------------------------
# Clipboard Tools
# -------------------------------
@mcp.tool()
def get_clipboard():
    """Get current clipboard text content."""
    lazy_imports()
    return pyperclip.paste()

@mcp.tool()
def set_clipboard(text: str):
    """Set system clipboard text content."""
    lazy_imports()
    pyperclip.copy(text)
    return "Clipboard updated."

# -------------------------------
# Window Management
# -------------------------------
@mcp.tool()
def list_windows():
    """List titles of all currently open windows."""
    lazy_imports()
    return [w.title for w in gw.getAllWindows() if w.title]

@mcp.tool()
def get_active_window_info():
    """Get details (title, position, dimensions) of the active window."""
    lazy_imports()
    try:
        win = gw.getActiveWindow()
        if win:
            return {
                "title": win.title,
                "left": win.left,
                "top": win.top,
                "width": win.width,
                "height": win.height,
                "isActive": win.isActive
            }
        return "No active window detected."
    except Exception as e:
        return f"Error getting active window: {e}"

@mcp.tool()
def focus_window(title: str):
    """Bring window matching title to focus/foreground."""
    lazy_imports()
    try:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].activate()
            return f"Focused window: {wins[0].title}"
        return f"Window '{title}' not found."
    except Exception as e:
        return f"Error focusing window '{title}': {e}"

@mcp.tool()
def move_window(title: str, x: int, y: int):
    """Move window matching title to screen coordinates (x, y)."""
    lazy_imports()
    try:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].moveTo(x, y)
            return f"Moved '{wins[0].title}' to ({x},{y})"
        return f"Window '{title}' not found."
    except Exception as e:
        return f"Error moving window '{title}': {e}"

@mcp.tool()
def resize_window(title: str, width: int, height: int):
    """Resize window matching title to specified width and height."""
    lazy_imports()
    try:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].resizeTo(width, height)
            return f"Resized '{wins[0].title}' to {width}x{height}"
        return f"Window '{title}' not found."
    except Exception as e:
        return f"Error resizing window '{title}': {e}"

@mcp.tool()
def close_window(title: str):
    """Close window matching title."""
    lazy_imports()
    try:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].close()
            return f"Closed window: {wins[0].title}"
        return f"Window '{title}' not found."
    except Exception as e:
        return f"Error closing window '{title}': {e}"

# -------------------------------
# Process & System Monitoring
# -------------------------------
@mcp.tool()
def list_processes(top_n: int = 20, sort_by: str = "memory"):
    """List running system processes sorted by cpu or memory."""
    lazy_imports()
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = p.info
                procs.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "cpu_percent": round(info['cpu_percent'] or 0.0, 2),
                    "memory_percent": round(info['memory_percent'] or 0.0, 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        key = 'memory_percent' if sort_by.lower() == 'memory' else 'cpu_percent'
        sorted_procs = sorted(procs, key=lambda x: x[key], reverse=True)[:top_n]
        return sorted_procs
    except Exception as e:
        return f"Error listing processes: {e}"

@mcp.tool()
def kill_process(name_or_pid: str):
    """Terminate a process by PID or name."""
    lazy_imports()
    try:
        killed = []
        if name_or_pid.isdigit():
            pid = int(name_or_pid)
            p = psutil.Process(pid)
            p.terminate()
            killed.append(f"PID {pid} ({p.name()})")
        else:
            for p in psutil.process_iter(['pid', 'name']):
                if p.info['name'].lower() == name_or_pid.lower():
                    p.terminate()
                    killed.append(f"PID {p.info['pid']} ({p.info['name']})")
        if killed:
            return f"Successfully terminated: {', '.join(killed)}"
        return f"No matching process found for: {name_or_pid}"
    except Exception as e:
        return f"Error terminating process: {e}"

@mcp.tool()
def get_system_stats():
    """Get real-time CPU, Memory, Disk, and System uptime overview."""
    lazy_imports()
    try:
        cpu_usage = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = psutil.boot_time()
        import time as t
        uptime_hours = round((t.time() - boot_time) / 3600, 2)
        
        return {
            "cpu_usage_percent": cpu_usage,
            "memory_total_gb": round(mem.total / (1024**3), 2),
            "memory_used_gb": round(mem.used / (1024**3), 2),
            "memory_percent": mem.percent,
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "disk_percent": disk.percent,
            "uptime_hours": uptime_hours
        }
    except Exception as e:
        return f"Error getting system stats: {e}"

# -------------------------------
# OCR & Vision Tools
# -------------------------------
@mcp.tool()
def ocr_screen(region: list[int] = None):
    """Perform OCR on screen or bounding region [left, top, width, height]."""
    lazy_imports()
    try:
        if region:
            shot = pyautogui.screenshot(region=tuple(region))
            offset_x, offset_y = region[0], region[1]
        else:
            shot = pyautogui.screenshot()
            offset_x, offset_y = 0, 0

        data = pytesseract.image_to_data(shot, output_type=pytesseract.Output.DICT)
        results = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if text:
                x = data['left'][i] + offset_x
                y = data['top'][i] + offset_y
                w = data['width'][i]
                h = data['height'][i]
                conf = data['conf'][i]
                results.append({
                    "text": text,
                    "confidence": conf,
                    "bbox": [x, y, w, h],
                    "center": [x + w // 2, y + h // 2]
                })
        return results if results else "No text recognized."
    except pytesseract.TesseractNotFoundError:
        return "Error: Tesseract OCR binary not found on Windows PATH. Install Tesseract OCR to use screen OCR."
    except Exception as e:
        return f"Error performing OCR: {e}"

@mcp.tool()
def click_text(text: str, region: list[int] = None):
    """Search screen for matching text using OCR and click on its center."""
    lazy_imports()
    ocr_results = ocr_screen(region)
    if isinstance(ocr_results, str):
        return ocr_results
    
    target_lower = text.lower()
    for item in ocr_results:
        if target_lower in item['text'].lower():
            cx, cy = item['center']
            pyautogui.click(cx, cy)
            return f"Clicked on text '{item['text']}' at screen coordinates ({cx}, {cy})"
    return f"Text '{text}' not found on screen."

@mcp.tool()
def take_window_screenshot(title: str, path: str = "window_screenshot.png"):
    """Capture screenshot of a specific open window by title."""
    lazy_imports()
    try:
        wins = gw.getWindowsWithTitle(title)
        if not wins:
            return f"Window '{title}' not found."
        win = wins[0]
        region = (win.left, win.top, win.width, win.height)
        pyautogui.screenshot(path, region=region)
        return f"Screenshot of window '{win.title}' saved to {os.path.abspath(path)}"
    except Exception as e:
        return f"Error capturing window screenshot: {e}"

# -------------------------------
# File System Tools
# -------------------------------
@mcp.tool()
def read_file(path: str):
    """Reads content of a file at specified path."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Content of {path}:\n\n{content}"
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error reading file: {e}"

@mcp.tool()
def write_file(path: str, content: str, append: bool = False):
    """Write text content to a file."""
    try:
        mode = 'a' if append else 'w'
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        action = "Appended to" if append else "Written to"
        return f"Successfully {action} {path}"
    except Exception as e:
        return f"Error writing to file: {e}"

@mcp.tool()
def edit_file(path: str, old_text: str, new_text: str, replace_all: bool = False):
    """Replace text in an existing file. Set replace_all=True to update every occurrence."""
    try:
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File not found at {path}"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_text not in content:
            return f"Error: The provided old_text was not found in {path}"

        updated_content = content.replace(old_text, new_text) if replace_all else content.replace(old_text, new_text, 1)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return f"Successfully updated {path}"
    except Exception as e:
        return f"Error editing file: {e}"

@mcp.tool()
def list_directory(path: str = "."):
    """List directory contents with file size and modification info."""
    try:
        import time as t
        p = Path(path)
        if not p.exists():
            return f"Error: Path '{path}' does not exist."
        items = []
        for child in p.iterdir():
            stat = child.stat()
            items.append({
                "name": child.name,
                "is_dir": child.is_dir(),
                "size_bytes": stat.st_size if child.is_file() else None,
                "modified": t.ctime(stat.st_mtime)
            })
        return items
    except Exception as e:
        return f"Error listing directory '{path}': {e}"

@mcp.tool()
def search_files(directory: str = ".", pattern: str = "*"):
    """Search for files matching glob pattern within directory."""
    try:
        search_path = os.path.join(directory, pattern)
        matches = glob.glob(search_path, recursive=True)
        return matches[:100]
    except Exception as e:
        return f"Error searching files: {e}"

# -------------------------------
# Application & Automation Tools
# -------------------------------
@mcp.tool()
def open_application(app_name: str):
    """Open specified application by name or path."""
    lazy_imports()
    known_apps = {
        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "notepad": "notepad.exe",
        "explorer": "explorer.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe"
    }
    app = known_apps.get(app_name.lower(), app_name)
    try:
        subprocess.Popen(app)
        return f"Opened application: {app_name}"
    except Exception as e:
        return f"Error opening {app_name}: {e}"

@mcp.tool()
def perform_action(task_description: str):
    """High-level automation helper to open browser, navigate, or search."""
    lazy_imports()
    try:
        desc = task_description.lower()

        if "brave" in desc:
            open_application("brave")
        elif "chrome" in desc:
            open_application("chrome")
        elif "edge" in desc:
            open_application("edge")

        for word in desc.split():
            if any(x in word for x in [".com", ".to", ".net", ".org", ".io"]):
                webbrowser.open(word)

        if "search" in desc:
            query = desc.split("search")[-1].strip()
            pyautogui.hotkey("ctrl", "l")
            pyautogui.typewrite(query)
            pyautogui.press("enter")

        return f"Performed action: {task_description}"
    except Exception as e:
        return f"Error performing action: {e}"

@mcp.tool()
def lock_workstation():
    """Lock the Windows workstation session immediately."""
    try:
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        return "Workstation locked."
    except Exception as e:
        return f"Error locking workstation: {e}"

# -------------------------------
# DIRECT WEB BROWSER AUTOMATION (Hermes-Style Agent Control)
# -------------------------------
_browser_driver = None

def get_browser_by_type(by_str: str):
    lazy_selenium()
    by_map = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT
    }
    return by_map.get(by_str.lower(), By.CSS_SELECTOR)

@mcp.tool()
def start_browser(url: str = None, browser_name: str = "chrome", headless: bool = False):
    """
    Launch direct automated browser instance (Hermes-style WebDriver control).
    Args:
        url: Optional initial URL to navigate to
        browser_name: 'chrome' or 'edge'
        headless: If True, runs browser in background without showing window
    """
    global _browser_driver
    lazy_selenium()
    try:
        if _browser_driver is not None:
            try:
                _browser_driver.quit()
            except Exception:
                pass

        if browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--start-maximized")
            service = webdriver.edge.service.Service(EdgeChromiumDriverManager().install())
            _browser_driver = webdriver.Edge(service=service, options=options)
        else:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            service = webdriver.chrome.service.Service(ChromeDriverManager().install())
            _browser_driver = webdriver.Chrome(service=service, options=options)

        status_msg = f"Browser ({browser_name}, headless={headless}) started successfully."
        if url:
            _browser_driver.get(url)
            status_msg += f" Navigated to {url}."
        return status_msg
    except Exception as e:
        return f"Error starting browser: {e}"

@mcp.tool()
def close_browser():
    """Safely close active automated browser session."""
    global _browser_driver
    if _browser_driver is not None:
        try:
            _browser_driver.quit()
            _browser_driver = None
            return "Browser session closed."
        except Exception as e:
            _browser_driver = None
            return f"Error closing browser: {e}"
    return "No active browser session found."

@mcp.tool()
def navigate_to(url: str):
    """Navigate active browser to specified URL."""
    global _browser_driver
    if _browser_driver is None:
        start_result = start_browser(url=url)
        return start_result
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        _browser_driver.get(url)
        return f"Navigated to {url}. Title: {_browser_driver.title}"
    except Exception as e:
        return f"Error navigating to {url}: {e}"

@mcp.tool()
def get_page_info():
    """Get title, current URL, and tab handles of the active browser."""
    global _browser_driver
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        return {
            "title": _browser_driver.title,
            "url": _browser_driver.current_url,
            "tab_count": len(_browser_driver.window_handles),
            "current_tab_index": _browser_driver.window_handles.index(_browser_driver.current_window_handle)
        }
    except Exception as e:
        return f"Error getting page info: {e}"

@mcp.tool()
def get_page_text():
    """Extract visible text content directly from page DOM (token-efficient reading)."""
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        body = _browser_driver.find_element(By.TAG_NAME, "body")
        text = body.text
        return f"Page URL: {_browser_driver.current_url}\nPage Title: {_browser_driver.title}\n\nVisible Content:\n{text[:5000]}"
    except Exception as e:
        return f"Error reading page text: {e}"

@mcp.tool()
def get_page_html(selector: str = None):
    """Get raw HTML of page or element matching CSS selector."""
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        if selector:
            by_type = get_browser_by_type("css")
            elem = _browser_driver.find_element(by_type, selector)
            return elem.get_attribute("outerHTML")
        return _browser_driver.page_source[:5000]
    except Exception as e:
        return f"Error getting HTML: {e}"

@mcp.tool()
def click_element(by: str = "css", selector: str = ""):
    """
    Click DOM element matching selector directly.
    by: 'css', 'xpath', 'id', 'name', 'class', 'tag', 'link_text'
    """
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        by_type = get_browser_by_type(by)
        elem = _browser_driver.find_element(by_type, selector)
        _browser_driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        elem.click()
        return f"Successfully clicked element [{by}='{selector}']."
    except Exception as e:
        return f"Error clicking element [{by}='{selector}']: {e}"

@mcp.tool()
def type_into_element(by: str = "css", selector: str = "", text: str = "", clear_first: bool = True):
    """
    Type text into DOM element (input, textarea).
    by: 'css', 'xpath', 'id', 'name'
    """
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        by_type = get_browser_by_type(by)
        elem = _browser_driver.find_element(by_type, selector)
        _browser_driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        if clear_first:
            elem.clear()
        elem.send_keys(text)
        return f"Typed '{text}' into element [{by}='{selector}']."
    except Exception as e:
        return f"Error typing into element [{by}='{selector}']: {e}"

@mcp.tool()
def press_browser_key(key: str = "enter"):
    """Send key (e.g. 'enter', 'tab', 'escape', 'backspace') to active browser element."""
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        key_map = {
            "enter": Keys.RETURN,
            "return": Keys.RETURN,
            "tab": Keys.TAB,
            "escape": Keys.ESCAPE,
            "backspace": Keys.BACKSPACE,
            "space": Keys.SPACE,
            "down": Keys.DOWN,
            "up": Keys.UP
        }
        target_key = key_map.get(key.lower(), Keys.RETURN)
        active_elem = _browser_driver.switch_to.active_element
        active_elem.send_keys(target_key)
        return f"Sent key '{key}' to active element."
    except Exception as e:
        return f"Error pressing browser key '{key}': {e}"

@mcp.tool()
def select_dropdown_option(by: str = "css", selector: str = "", value_or_text: str = ""):
    """Select option in HTML <select> element by visible text or value attribute."""
    global _browser_driver
    lazy_selenium()
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        by_type = get_browser_by_type(by)
        elem = _browser_driver.find_element(by_type, selector)
        sel = Select(elem)
        try:
            sel.select_by_visible_text(value_or_text)
        except Exception:
            sel.select_by_value(value_or_text)
        return f"Selected option '{value_or_text}' in dropdown [{by}='{selector}']."
    except Exception as e:
        return f"Error selecting option in [{by}='{selector}']: {e}"

@mcp.tool()
def open_new_tab(url: str = None):
    """Open new browser tab and optionally navigate to URL."""
    global _browser_driver
    if _browser_driver is None:
        return start_browser(url=url)
    try:
        _browser_driver.execute_script("window.open();")
        _browser_driver.switch_to.window(_browser_driver.window_handles[-1])
        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            _browser_driver.get(url)
            return f"Opened new tab and navigated to {url}."
        return "Opened new blank tab."
    except Exception as e:
        return f"Error opening new tab: {e}"

@mcp.tool()
def switch_to_tab(index: int = 0):
    """Switch active browser control to tab at specific 0-based index."""
    global _browser_driver
    if _browser_driver is None:
        return "Error: No active browser session. Call start_browser first."
    try:
        handles = _browser_driver.window_handles
        if 0 <= index < len(handles):
            _browser_driver.switch_to.window(handles[index])
            return f"Switched to tab index {index}. Title: {_browser_driver.title}"
        return f"Invalid tab index {index}. Total tabs: {len(handles)}"
    except Exception as e:
        return f"Error switching to tab {index}: {e}"

@mcp.tool()
def close_tab():
    """Close currently active tab."""
    global _browser_driver
    if _browser_driver is None:
        return "Error: No active browser session."
    try:
        _browser_driver.close()
        handles = _browser_driver.window_handles
        if handles:
            _browser_driver.switch_to.window(handles[-1])
            return f"Closed tab. Switched to tab '{_browser_driver.title}'."
        _browser_driver = None
        return "Closed last tab and exited browser."
    except Exception as e:
        return f"Error closing tab: {e}"

@mcp.tool()
def execute_javascript(script: str):
    """Execute custom JavaScript in active web page context."""
    global _browser_driver
    if _browser_driver is None:
        return "Error: No active browser session."
    try:
        res = _browser_driver.execute_script(script)
        return {"result": res}
    except Exception as e:
        return f"Error executing JavaScript: {e}"

@mcp.tool()
def take_browser_screenshot(path: str = "browser_screenshot.png"):
    """Capture precise full web page render screenshot."""
    global _browser_driver
    if _browser_driver is None:
        return "Error: No active browser session."
    try:
        _browser_driver.save_screenshot(path)
        return f"Browser screenshot saved to {os.path.abspath(path)}"
    except Exception as e:
        return f"Error taking browser screenshot: {e}"

# -------------------------------
# Tool Summary List
# -------------------------------
@mcp.tool()
def list_tools():
    """List all available Windows Universal MCP tools."""
    return """
Available Tool Categories:

1️⃣ CLI COMMANDS:
   - run_command(command)
   - run_cmd(command)

2️⃣ DIRECT BROWSER AUTOMATION (Hermes Agent Style):
   - start_browser(url, browser_name, headless)
   - close_browser()
   - navigate_to(url)
   - get_page_info()
   - get_page_text()
   - get_page_html(selector)
   - click_element(by, selector)
   - type_into_element(by, selector, text, clear_first)
   - press_browser_key(key)
   - select_dropdown_option(by, selector, value_or_text)
   - open_new_tab(url)
   - switch_to_tab(index)
   - close_tab()
   - execute_javascript(script)
   - take_browser_screenshot(path)

3️⃣ GUI & INPUT CONTROL:
   - move_mouse(x, y, duration)
   - click(x, y, button)
   - double_click(x, y)
   - right_click(x, y)
   - drag_mouse(start_x, start_y, end_x, end_y, duration)
   - type_text(text, interval)
   - press_key(key)
   - press_hotkey(keys)
   - scroll(amount)
   - take_screenshot(path)
   - get_screen_size()

4️⃣ CLIPBOARD:
   - get_clipboard()
   - set_clipboard(text)

5️⃣ WINDOW MANAGEMENT:
   - list_windows()
   - get_active_window_info()
   - focus_window(title)
   - move_window(title, x, y)
   - resize_window(title, width, height)
   - close_window(title)

6️⃣ PROCESS & SYSTEM MONITORING:
   - list_processes(top_n, sort_by)
   - kill_process(name_or_pid)
   - get_system_stats()

7️⃣ OCR & VISION:
   - ocr_screen(region)
   - click_text(text, region)
   - take_window_screenshot(title, path)

8️⃣ FILE SYSTEM MANAGEMENT:
   - read_file(path)
   - write_file(path, content, append)
   - edit_file(path, old_text, new_text, replace_all)
   - list_directory(path)
   - search_files(directory, pattern)

9️⃣ APPLICATION & SYSTEM:
   - open_application(app_name)
   - perform_action(task_description)
   - lock_workstation()
"""

# -------------------------------
# Main Entry Point
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
    logger.info("Starting Advanced Windows Universal MCP with Direct Web Automation (stdio mode)")
    mcp.run(transport="stdio")
