"""Generates the pixel-art SVGs used by the profile README.

Everything is drawn from one fixed palette ("film stock") and a 5x7 bitmap
font, so the whole page stays cohesive. Edit the constants below and run:

    python3 tools/build_assets.py
"""

import math
from pathlib import Path

PALETTE = {
    "sky": "#2e3b3a",
    "glow": "#c98b5e",
    "ground": "#3d3a32",
    "hill": "#56614f",
    "sun": "#f2c48d",
    "cream": "#f4e7d0",
    "rust": "#a2543a",
    "sand": "#e8d8bf",
    "gold": "#e8c07d",
    "teal": "#6f9a95",
    "orange": "#d9734e",
    "ink": "#1e1f1c",
}
C = PALETTE

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "#..#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
    ".": ["..", "..", "..", "..", "..", "##", "##"],
    ":": ["..", "##", "##", "..", "##", "##", ".."],
    "·": ["..", "..", "..", "##", "##", "..", ".."],
    "!": ["##", "##", "##", "##", "##", "..", "##"],
    "-": ["....", "....", "....", "####", "....", "....", "...."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".####"],
    "▶": ["#...", "##..", "###.", "####", "###.", "##..", "#..."],
}

# Each sprite is rows of single-letter keys plus the palette color per key.
SPRITES = {
    "car": (
        [
            "......cccccccc......",
            ".....cwwwwcwwwwc....",
            "....cwwwwwcwwwwwc...",
            ".cccccccccccccccccc.",
            "tccccccccccccccccccl",
            "cccckkkkcccckkkkcccc",
            "...kkhhkk..kkhhkk...",
            "....kkkk....kkkk....",
        ],
        {"c": "body", "w": "glow", "t": "rust", "l": "sun", "k": "ink", "h": "sand"},
    ),
    "lock": (
        [
            "..sss..",
            ".s...s.",
            ".s...s.",
            "bbbbbbb",
            "bbbkbbb",
            "bbbkbbb",
            "bbbbbbb",
        ],
        {"s": "cream", "b": "sun", "k": "ink"},
    ),
    "runner_a": (
        [
            "....hh...",
            "....hh...",
            "...ss....",
            "..ssss.h.",
            ".h.ss.h..",
            "h..ss....",
            "...hh....",
            "..h..h...",
            ".h....h..",
            "h......h.",
        ],
        {"h": "cream", "s": "orange"},
    ),
    "runner_b": (
        [
            "....hh...",
            "....hh...",
            "...ss....",
            "...sss...",
            "...ssh...",
            "...ssh...",
            "...hh....",
            "...h.h...",
            "...h..h..",
            "..hh.....",
        ],
        {"h": "cream", "s": "orange"},
    ),
}

TITLE = "PEDRO TRICOSSI"
SUBTITLE = "LVL MSC CRYPTOGRAPHY · WORLD UFPR / FAU"
PRESS = "▶ PRESS START"
FOOTER = "THANKS FOR STOPPING BY!"

HEADINGS = {
    "h-about": ("ABOUT ME", "PLAYER 1", "About me"),
    "h-research": ("RESEARCH", "STAGE 1", "Research"),
    "h-papers": ("PAPERS", "STAGE 2", "Papers"),
    "h-projects": ("PROJECTS", "STAGE 3", "Projects"),
    "h-contact": ("CONTACT", "CONTINUE?", "Contact"),
}

BADGES = {
    "badge-bsc": ("BSC CS", "UFPR", "teal", "BSc Computer Science, UFPR"),
    "badge-msc": ("MSC CRYPTOGRAPHY", "UFPR", "orange", "MSc Cryptography, UFPR"),
    "badge-exchange": ("EXCHANGE YEAR", "FAU ERLANGEN", "glow",
                       "Exchange year, FAU Erlangen-Nürnberg"),
    "badge-email": ("EMAIL", "PEDRODTRICOSSI@GMAIL.COM", "orange",
                    "Email: pedrodtricossi@gmail.com"),
    "badge-linkedin": ("LINKEDIN", "PEDRO TRICOSSI", "teal", "LinkedIn: Pedro Tricossi"),
    "badge-orcid": ("ORCID", "0009-0002-4751-5805", "glow", "ORCID: 0009-0002-4751-5805"),
}

ALL_TEXT = [TITLE, SUBTITLE, PRESS, FOOTER]
ALL_TEXT += [t for left, right, _ in HEADINGS.values() for t in (left, right)]
ALL_TEXT += [t for label, value, _, _ in BADGES.values() for t in (label, value)]

REDUCED_MOTION = ("@media (prefers-reduced-motion: reduce)"
                  " { * { animation: none !important; } }")


# ---------------------------------------------------------------- drawing ---

def rect(x, y, w, h, fill, cls=None):
    attr = f' class="{cls}"' if cls else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{attr}/>'


def pixels(rows, colors, x, y, scale, flip=False):
    """Draws pixel rows, merging horizontal runs of one color into one rect."""
    out = []
    for r, row in enumerate(rows):
        if flip:
            row = row[::-1]
        c = 0
        while c < len(row):
            key = row[c]
            run = 1
            while c + run < len(row) and row[c + run] == key:
                run += 1
            if key != ".":
                out.append(rect(x + c * scale, y + r * scale, run * scale, scale, colors[key]))
            c += run
    return out


def text_width(text, scale):
    widths = [len(FONT[ch][0]) for ch in text]
    return (sum(widths) + len(widths) - 1) * scale


def text(s, x, y, scale, fill):
    out = []
    for ch in s:
        rows = FONT[ch]
        out += pixels(rows, {"#": fill}, x, y, scale)
        x += (len(rows[0]) + 1) * scale
    return out


def shadowed(s, x, y, scale, fill, shadow):
    return text(s, x + scale, y + scale, scale, shadow) + text(s, x, y, scale, fill)


def sprite(name, x, y, scale, body=None, flip=False):
    rows, keys = SPRITES[name]
    colors = {k: C[body if v == "body" else v] for k, v in keys.items() if v != "body" or body}
    return pixels(rows, colors, x, y, scale, flip)


def svg(w, h, title, body, style=""):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-labelledby="title" '
            f'shape-rendering="crispEdges">')
    parts = [head, f"<title id=\"title\">{title}</title>"]
    if style:
        parts.append(f"<style>\n{style}\n{REDUCED_MOTION}\n</style>")
    parts += body
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def notched_bg(w, h, fill, notch):
    """A background rectangle with pixel-cut corners."""
    return [rect(notch, 0, w - 2 * notch, h, fill), rect(0, notch, w, h - 2 * notch, fill)]


def runner(x, y, scale):
    return ([f'<g class="frame-a">'] + sprite("runner_a", x, y, scale) + ["</g>"]
            + [f'<g class="frame-b">'] + sprite("runner_b", x, y, scale) + ["</g>"])


RUNNER_STYLE = """\
.runner { animation: run 10s steps(230) infinite; }
.frame-b { opacity: 0; }
.frame-a { animation: frame-a .36s step-end infinite; }
.frame-b { animation: frame-b .36s step-end infinite; }
@keyframes run { from { transform: translateX(-40px); } to { transform: translateX(880px); } }
@keyframes frame-a { 0% { opacity: 1; } 50% { opacity: 0; } }
@keyframes frame-b { 0% { opacity: 0; } 50% { opacity: 1; } }"""

ROAD_STYLE = """\
.road { animation: road .6s steps(6) infinite; }
@keyframes road { to { transform: translateX(-48px); } }"""


def road(y):
    return (['<g class="road">'] + [rect(x, y, 24, 4, C["gold"]) for x in range(0, 888, 48)]
            + ["</g>"])


# ----------------------------------------------------------------- assets ---

def header():
    w, h, horizon = 840, 296, 184
    body = [
        "<defs>",
        '<pattern id="d25" width="8" height="8" patternUnits="userSpaceOnUse">',
        rect(0, 0, 8, 8, C["sky"]), rect(0, 0, 4, 4, C["glow"]), "</pattern>",
        '<pattern id="d50" width="8" height="8" patternUnits="userSpaceOnUse">',
        rect(0, 0, 8, 8, C["glow"]), rect(0, 0, 4, 4, C["sky"]), rect(4, 4, 4, 4, C["sky"]),
        "</pattern>",
        '<pattern id="d75" width="8" height="8" patternUnits="userSpaceOnUse">',
        rect(0, 0, 8, 8, C["glow"]), rect(4, 0, 4, 4, C["sky"]), "</pattern>",
        "</defs>",
        rect(0, 0, w, 96, C["sky"]),
        rect(0, 96, w, 16, "url(#d25)"),
        rect(0, 112, w, 16, "url(#d50)"),
        rect(0, 128, w, 16, "url(#d75)"),
        rect(0, 144, w, horizon - 144, C["glow"]),
    ]

    stars = [(40, 20, 1), (120, 60, 2), (196, 12, 3), (612, 12, 2), (692, 32, 1),
             (764, 68, 3), (300, 100, 1), (544, 104, 3), (808, 16, 2), (16, 88, 3)]
    body += [rect(x, y, 4, 4, C["cream"], f"star t{n}") for x, y, n in stars]

    # Sun sitting on the horizon, with retro stripes cut into its lower half.
    radius, cx, gaps = 60, 420, {2, 3, 6, 9}
    for k in range(1, radius // 4 + 1):
        if k in gaps:
            continue
        dy = k * 4 - 2
        half = int(math.sqrt(radius ** 2 - dy ** 2) / 4) * 4
        body.append(rect(cx - half, horizon - k * 4, 2 * half, 4, C["sun"]))

    # Hills: low in the middle so the sun shows, higher toward the edges.
    cols = []
    for c in range(w // 4):
        edge = abs(c - 105) / 105
        units = 2 + 8 * edge ** 1.4 + 1.6 * math.sin(c / 5) + 1.2 * math.sin(c / 2.3 + 1)
        cols.append(max(1, round(units)))
    c = 0
    while c < len(cols):
        run = 1
        while c + run < len(cols) and cols[c + run] == cols[c]:
            run += 1
        body.append(rect(c * 4, horizon - cols[c] * 4, run * 4, cols[c] * 4, C["hill"]))
        c += run

    body += [rect(0, horizon, w, h - horizon, C["ground"]), rect(0, horizon, w, 4, C["rust"])]

    tw = text_width(TITLE, 5)
    body += shadowed(TITLE, (w - tw) // 2, 20, 5, C["cream"], C["rust"])
    sw = text_width(SUBTITLE, 2)
    body += text(SUBTITLE, (w - sw) // 2, 72, 2, C["sand"])
    pw = text_width(PRESS, 2)
    body += ['<g class="blink">'] + text(PRESS, (w - pw) // 2, 198, 2, C["cream"]) + ["</g>"]

    body += road(250)
    body += ['<g class="car bob-a">'] + sprite("car", 200, 212, 4, "teal") + ["</g>"]
    body += ['<g class="car bob-b">'] + sprite("car", 560, 212, 4, "orange", flip=True) + ["</g>"]
    body += ['<g class="packet">'] + sprite("lock", 230, 186, 3) + ["</g>"]
    body += ['<g class="runner">'] + runner(0, 262, 3) + ["</g>"]

    style = "\n".join([
        ".blink { animation: blink 1.2s step-end infinite; }",
        "@keyframes blink { 50% { opacity: 0; } }",
        ".star { animation: twinkle 2.4s steps(2) infinite; }",
        ".t2 { animation-delay: -.8s; } .t3 { animation-delay: -1.6s; }",
        "@keyframes twinkle { 50% { opacity: .25; } }",
        ".bob-a { animation: bob .5s steps(1) infinite alternate; }",
        ".bob-b { animation: bob .5s steps(1) -.25s infinite alternate; }",
        "@keyframes bob { to { transform: translateY(-4px); } }",
        ".packet { animation: packet 6s infinite; animation-timing-function: steps(5); }",
        "@keyframes packet {",
        "  0%, 8% { transform: translate(0, 0); }",
        "  20% { transform: translate(85px, -24px); }",
        "  32% { transform: translate(170px, -32px); }",
        "  44% { transform: translate(255px, -24px); }",
        "  56%, 64% { transform: translate(340px, 0); }",
        "  72% { transform: translate(255px, -24px); }",
        "  80% { transform: translate(170px, -32px); }",
        "  88% { transform: translate(85px, -24px); }",
        "  100% { transform: translate(0, 0); }",
        "}",
        ROAD_STYLE,
        RUNNER_STYLE,
    ])
    title = ("Pedro Tricossi, MSc cryptography at UFPR and FAU: an 8-bit dusk scene where "
             "two pixel cars pass a locked message while a runner goes by")
    return svg(w, h, title, body, style)


def heading(left, right, title):
    w, h = 840, 48
    body = notched_bg(w, h, C["sky"], 4) + [rect(4, h - 4, w - 8, 4, C["rust"])]
    body += ['<g class="blink">'] + text("▶", 16, 13, 3, C["gold"]) + ["</g>"]
    body += shadowed(left, 40, 13, 3, C["cream"], C["rust"])
    rw = text_width(right, 2)
    body += text(right, w - 20 - rw, 17, 2, C["sand"])
    style = (".blink { animation: blink 1.2s step-end infinite; }\n"
             "@keyframes blink { 50% { opacity: 0; } }")
    return svg(w, h, title, body, style)


def badge(label, value, color, title):
    pad, scale, h = 10, 2, 28
    lw = text_width(label, scale) + 2 * pad
    vw = text_width(value, scale) + 2 * pad
    w = lw + vw
    body = notched_bg(w, h, C[color], 2) + [rect(0, 2, 2, h - 4, C["hill"]),
                                            rect(2, 0, lw - 2, h, C["hill"])]
    body += text(label, pad, 7, scale, C["cream"])
    body += text(value, lw + pad, 7, scale, C["ink"])
    return svg(w, h, title, body)


def footer():
    w, h = 840, 80
    body = notched_bg(w, h, C["ground"], 4)
    fw = text_width(FOOTER, 2)
    body += text(FOOTER, (w - fw) // 2, 10, 2, C["cream"])
    body += ['<g class="runner">'] + runner(0, 38, 3) + ["</g>"]
    body += road(70)
    return svg(w, h, "Thanks for stopping by!", body, ROAD_STYLE + "\n" + RUNNER_STYLE)


def build(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {"header": header(), "footer": footer()}
    files.update({name: heading(*args) for name, args in HEADINGS.items()})
    files.update({name: badge(*args) for name, args in BADGES.items()})
    for name, content in files.items():
        (out_dir / f"{name}.svg").write_text(content)


if __name__ == "__main__":
    build(Path(__file__).resolve().parent.parent / "assets")
