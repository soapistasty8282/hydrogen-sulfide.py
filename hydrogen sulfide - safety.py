import ctypes
import random
import time
from ctypes import wintypes

# --- HIDE TERMINAL SAFELY ---
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
console = kernel32.GetConsoleWindow()
user32.ShowWindow(console, 0)  # SW_HIDE

gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)

# WinAPI signatures
user32.GetDesktopWindow.restype = wintypes.HWND
user32.GetDC.argtypes = [wintypes.HWND]
user32.GetDC.restype = wintypes.HDC
user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.GetSystemMetrics.restype = ctypes.c_int
user32.SetCursorPos.argtypes = [wintypes.INT, wintypes.INT]
user32.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
user32.GetAsyncKeyState.argtypes = [wintypes.INT]

gdi32.BitBlt.argtypes = [
    wintypes.HDC, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT,
    wintypes.HDC, wintypes.INT, wintypes.INT, wintypes.DWORD
]

# Get screen DC
hwnd = user32.GetDesktopWindow()
hdc = user32.GetDC(hwnd)

sw = user32.GetSystemMetrics(0)
sh = user32.GetSystemMetrics(1)

pt = wintypes.POINT()

# -------------------------
# CURSOR SHAKE FUNCTION
# -------------------------
def shake_cursor(strength=15):
    user32.GetCursorPos(ctypes.byref(pt))
    cx = random.randint(-strength, strength)
    cy = random.randint(-strength, strength)
    user32.SetCursorPos(pt.x + cx, pt.y + cy)
    return cx, cy

# -------------------------
# PHASE 1 — tunnel (NO MELT)
# -------------------------
def phase1(duration):
    start = time.time()
    t = 0
    while time.time() - start < duration:
        cx, cy = shake_cursor(20)
        zoom = (t % 40) + 20

        gdi32.BitBlt(
            hdc,
            zoom + cx,
            zoom + cy,
            sw - zoom * 2,
            sh - zoom * 2,
            hdc,
            0,
            0,
            0x00CC0020
        )

        time.sleep(0.01)
        t += 1

# -------------------------
# PHASE 2 — train + bounce (NO MELT)
# -------------------------
def phase2(duration):
    start = time.time()
    bx = sw//4
    by = sh//4
    vx = 15
    vy = 12

    while time.time() - start < duration:
        cx, cy = shake_cursor(30)

        gdi32.BitBlt(
            hdc,
            50 + cx,
            0 + cy,
            sw - 50,
            sh,
            hdc,
            0,
            0,
            0x00CC0020
        )

        sub_w = sw//3
        sub_h = sh//3

        gdi32.BitBlt(
            hdc,
            bx + cx,
            by + cy,
            sub_w,
            sub_h,
            hdc,
            0,
            0,
            0x00CC0020
        )

        bx += vx
        by += vy

        if bx <= 0 or bx + sub_w >= sw:
            vx = -vx
        if by <= 0 or by + sub_h >= sh:
            vy = -vy

        time.sleep(0.01)

# -------------------------
# PHASE 3 — chaos + 3 boxes (NO MELT)
# -------------------------
def phase3(duration):
    start = time.time()
    boxes = 0

    while time.time() - start < duration:
        cx, cy = shake_cursor(40)
        rx = random.randint(-100, 100)
        ry = random.randint(-100, 100)

        gdi32.BitBlt(
            hdc,
            rx + cx,
            ry + cy,
            sw,
            sh,
            hdc,
            0,
            0,
            0x00CC0020
        )

        if boxes < 3:
            user32.MessageBoxA(None, b"chaos.exe", b"chaos.exe", 0)
            boxes += 1

        time.sleep(0.01)

# -------------------------
# PHASE 4 — UNSTOPPABLE ULTRA FAST MELT
# -------------------------
def phase4(duration):
    start = time.time()

    while time.time() - start < duration:
        cx, cy = shake_cursor(80)

        # Ultra melt
        for _ in range(300):
            y = random.randint(0, sh - 4)
            gdi32.BitBlt(hdc, 0, y + 4, sw, 4, hdc, 0, y, 0x00CC0020)

        for _ in range(300):
            x = random.randint(0, sw - 4)
            gdi32.BitBlt(hdc, x + 4, 0, 4, sh, hdc, x, 0, 0x00CC0020)

        # Deep fry
        if random.random() < 0.6:
            gdi32.BitBlt(hdc, 0, 0, sw, sh, hdc, 0, 0, 0x005A0049)

        # Clicking does nothing visually (extra melt)
        if user32.GetAsyncKeyState(0x01):
            for _ in range(500):
                y = random.randint(0, sh - 4)
                gdi32.BitBlt(hdc, 0, y + 5, sw, 5, hdc, 0, y, 0x00CC0020)

        time.sleep(0.003)

# -------------------------
# RUN PHASES
# -------------------------
phase1(60)
phase2(60)
phase3(60)
phase4(30)

print("Effect finished.")
