"""Generate the competition track floor texture (worlds/textures/yeyebei.png)."""

import math
from pathlib import Path
import struct
import zlib

FLOOR_MIN = -0.20
FLOOR_MAX = 4.20
# 360 mm white lane bounded on both sides by 50 mm continuous black bands.
WIDTH = 0.360
BOUNDARY_WIDTH = 0.050
START_X = 3.120
DASH_HALF_WIDTH = 0.005
OUTLINE = ((0.0, 0.0), (4.0, 0.0), (4.0, 1.520), (2.0, 4.0), (0.0, 1.520))
# Real-venue thin 10 mm dashes: two 45 mm stubs attached to both borders + two 60 mm floating dashes (50 mm gaps).
_DASH_SPANS = ((0.000, 0.045), (0.095, 0.155), (0.205, 0.265), (0.315, 0.360))


def edges(vertices):
    return zip(vertices, (*vertices[1:], vertices[0]))


def unit_normal(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    return -dy / length, dx / length


def inset(vertices, normals, distance):
    result = []
    for index, (x, y) in enumerate(vertices):
        ax, ay = normals[index - 1]
        bx, by = normals[index]
        scale = distance / (1 + ax * bx + ay * by)
        result.append((x + scale * (ax + bx), y + scale * (ay + by)))
    return tuple(result)


def chunk(name, data):
    return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data))


def main():
    normals = tuple(unit_normal(a, b) for a, b in edges(OUTLINE))
    outer = inset(OUTLINE, normals, BOUNDARY_WIDTH)
    inner = inset(OUTLINE, normals, BOUNDARY_WIDTH + WIDTH)
    inner_border = inset(OUTLINE, normals, 2 * BOUNDARY_WIDTH + WIDTH)
    lane_contours = (OUTLINE, outer, inner, inner_border)
    dashes = tuple(
        (START_X - DASH_HALF_WIDTH, outer[0][1] + lo, START_X + DASH_HALF_WIDTH, outer[0][1] + hi)
        for lo, hi in _DASH_SPANS
    )

    size = 2048
    scale = size / (FLOOR_MAX - FLOOR_MIN)
    floor = bytearray([237]) * (size * size)

    def paint(row, first, last, color):
        start = row * size + first
        length = last - first + 1
        floor[start:start + length] = color * length

    white, black = bytes([237]), bytes([16])
    # Paint nested contours from the outside in so the black bands meet at each corner.
    for contour, color in zip(lane_contours, (black, white, black, white)):
        sides = tuple(edges(contour))
        for row in range(size):
            y = FLOOR_MAX - (row + .5) / scale
            crossings = [x0 + (x1 - x0) * (y - y0) / (y1 - y0)
                         for (x0, y0), (x1, y1) in sides
                         if min(y0, y1) <= y < max(y0, y1)]
            if crossings:
                first = math.ceil((min(crossings) - FLOOR_MIN) * scale - .5)
                last = math.floor((max(crossings) - FLOOR_MIN) * scale - .5)
                if first <= last:
                    paint(row, first, last, color)
    for x0, y0, x1, y1 in dashes:
        for row in range(round((FLOOR_MAX - y1) * scale), round((FLOOR_MAX - y0) * scale)):
            paint(row, round((x0 - FLOOR_MIN) * scale), round((x1 - FLOOR_MIN) * scale), black)

    project_root = Path(__file__).resolve().parents[1]
    texture = project_root / "worlds" / "textures" / "yeyebei.png"
    texture.parent.mkdir(parents=True, exist_ok=True)
    rows = b"".join(b"\0" + floor[index:index + size] for index in range(0, len(floor), size))
    header = struct.pack(">IIBBBBB", size, size, 8, 0, 0, 0, 0)
    texture.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                        + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))
    print(f"Generated {texture} ({texture.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
