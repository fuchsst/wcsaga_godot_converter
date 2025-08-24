#!/usr/bin/env python3

import re

# Test the sound entry pattern
sound_pattern = re.compile(r"^\$Name:\s*(\d+)\s+([^,]+),\s*(\d+),\s*([\d\.]+),\s*(\d+)(?:,\s*([\d\.]+),\s*([\d\.]+))?\s*;\s*(.*)", re.IGNORECASE)

# Test lines from sounds.tbl
test_lines = [
    "$Name:    0     snd_missile_tracking.wav,       0, 0.40, 0              ; Missle tracking to acquire a lock (looped)",
    "$Name:    1     snd_missile_lock.wav,           0, 0.40, 0              ; Missle lock (non-looping)",
    "$Name:    6     snd_death_roll.wav,             0, 1.00, 2,  100,  800  ; ship death roll (3d sound)",
    "$Name:    7     snd_ship_explode_1.wav,         0, 0.90, 2,  750, 1500  ; ship explosion 1 (3d sound)",
]

print("Testing sound entry pattern:")
print(f"Pattern: {sound_pattern.pattern}")
print()

for i, line in enumerate(test_lines):
    match = sound_pattern.match(line)
    if match:
        print(f"✓ Line {i}: MATCH - {len(match.groups())} groups")
        for j, group in enumerate(match.groups()):
            print(f"  Group {j}: '{group}'")
    else:
        print(f"✗ Line {i}: NO MATCH")
    print()