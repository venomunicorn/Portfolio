"""
Safe Minecraft /fill automation
- Guarantees each /fill clears <= FILL_LIMIT blocks
- Copies the command, pastes (Ctrl+V), presses Enter, then presses 't' to reopen chat
- Requires: pyautogui, pyperclip
- Usage: run this script, switch to Minecraft (in-game), keep the game window focused.
"""

import pyautogui
import pyperclip
import time
import math
import sys

# -------- USER INPUT: cuboid corners (inclusive) --------
# Given in the prompt:
x1, y1, z1 = -944, 63, -432
x2, y2, z2 = -608, 100, 0

# maximum blocks per single /fill (user-specified)
FILL_LIMIT = 30000

# delay settings (adjust if needed)
INITIAL_DELAY = 6.0     # seconds to switch to Minecraft after starting script
BETWEEN_COMMAND_DELAY = 0.18  # delay after Enter before pressing 't' and next operation
PAUSE_AFTER_T = 0.12    # small pause after pressing 't' to let chat open

# safety settings for pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# normalize coords (ensure min <= max)
xmin, xmax = min(x1, x2), max(x1, x2)
ymin, ymax = min(y1, y2), max(y1, y2)
zmin, zmax = min(z1, z2), max(z1, z2)

# inclusive lengths
dx = xmax - xmin + 1
dy = ymax - ymin + 1
dz = zmax - zmin + 1
total_blocks = dx * dy * dz

def compute_step(limit, len_a, len_b):
    # returns the largest integer step >=1 such that step * len_a * len_b <= limit
    if len_a * len_b == 0:
        return 1
    step = limit // (len_a * len_b)
    return max(1, step)

# compute candidate steps if we slice along each axis
step_if_slicing_x = compute_step(FILL_LIMIT, dy, dz)  # thickness along X
step_if_slicing_y = compute_step(FILL_LIMIT, dx, dz)  # thickness along Y
step_if_slicing_z = compute_step(FILL_LIMIT, dx, dy)  # thickness along Z

# choose axis that gives largest step (minimizes number of commands)
axis, step = max(
    (('x', step_if_slicing_x), ('y', step_if_slicing_y), ('z', step_if_slicing_z)),
    key=lambda pair: pair[1]
)

# calculate number of commands expected
if axis == 'x':
    commands = math.ceil(dx / step)
elif axis == 'y':
    commands = math.ceil(dy / step)
else:
    commands = math.ceil(dz / step)

print(f"Cuboid size: dx={dx}, dy={dy}, dz={dz}  -> total blocks = {total_blocks:,}")
print(f"Slicing axis chosen: {axis.upper()} with step = {step} -> approx {commands} commands")
print("Each command will clear at most", FILL_LIMIT, "blocks.")
print("Script will start in", INITIAL_DELAY, "seconds. Switch to Minecraft and open chat (or let script open it).")
time.sleep(INITIAL_DELAY)

# open chat to start (press 't')
pyautogui.press('t')
time.sleep(PAUSE_AFTER_T)

def send_command(cmd):
    pyperclip.copy(cmd)
    # On macOS the paste hotkey uses 'command' instead of 'ctrl'
    if sys.platform == 'darwin':
        pyautogui.hotkey('command', 'v')
    else:
        pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.06)
    pyautogui.press('enter')
    time.sleep(BETWEEN_COMMAND_DELAY)
    pyautogui.press('t')  # reopen chat for next command
    time.sleep(PAUSE_AFTER_T)

# iterate slices
if axis == 'x':
    start = xmin
    end = xmax
    for xs in range(start, end + 1, step):
        xe = min(xs + step - 1, end)
        blocks_here = (xe - xs + 1) * dy * dz
        # safety: if it accidentally exceeds limit, shrink xe
        while blocks_here > FILL_LIMIT:
            xe -= 1
            blocks_here = (xe - xs + 1) * dy * dz
        cmd = f"/fill {xs} {ymin} {zmin} {xe} {ymax} {zmax} minecraft:air"
        print("Sending:", cmd, f"({blocks_here} blocks)")
        send_command(cmd)

elif axis == 'y':
    start = ymin
    end = ymax
    for ys in range(start, end + 1, step):
        ye = min(ys + step - 1, end)
        blocks_here = dx * (ye - ys + 1) * dz
        while blocks_here > FILL_LIMIT:
            ye -= 1
            blocks_here = dx * (ye - ys + 1) * dz
        cmd = f"/fill {xmin} {ys} {zmin} {xmax} {ye} {zmax} minecraft:air"
        print("Sending:", cmd, f"({blocks_here} blocks)")
        send_command(cmd)

else:  # axis == 'z'
    start = zmin
    end = zmax
    for zs in range(start, end + 1, step):
        ze = min(zs + step - 1, end)
        blocks_here = dx * dy * (ze - zs + 1)
        while blocks_here > FILL_LIMIT:
            ze -= 1
            blocks_here = dx * dy * (ze - zs + 1)
        cmd = f"/fill {xmin} {ymin} {zs} {xmax} {ymax} {ze} minecraft:air"
        print("Sending:", cmd, f"({blocks_here} blocks)")
        send_command(cmd)

print("Done. Cleared cuboid area safely.")
