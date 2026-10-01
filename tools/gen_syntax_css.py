"""Generate static/css/syntax.css.

Takes Chroma's `nord` palette (the most muted dark style available) and repairs
the handful of token colours that are too dim to read against #2e3440, by
raising their lightness in HLS while preserving hue and saturation. The result
stays muted but is legible.
"""
import colorsys
import re
import subprocess

BG = (0x2E, 0x34, 0x40)
TARGET = 4.5          # WCAG AA for normal text
TARGET_LARGE = 3.0    # acceptable floor for incidental tokens


def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(fg, bg=BG):
    la, lb = sorted([lum(fg), lum(bg)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


def lift(rgb, target):
    """Raise lightness until the colour clears `target`, keeping hue/saturation."""
    h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in rgb])
    best = rgb
    lo, hi = l, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        cand = tuple(round(v * 255) for v in colorsys.hls_to_rgb(h, mid, s))
        if contrast(cand) >= target:
            best = cand
            hi = mid
        else:
            lo = mid
    return best


def cap_saturation(rgb, max_sat):
    """Never exceed the original saturation - lifting lightness must not
    make a colour louder than the palette it came from."""
    h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in rgb])
    if s <= max_sat:
        return rgb
    return tuple(round(v * 255) for v in colorsys.hls_to_rgb(h, l, max_sat))


css = subprocess.run(
    ["hugo", "gen", "chromastyles", "--style", "nord"],
    capture_output=True, text=True,
).stdout

# Token groups and how much contrast each needs.
GROUPS = {
    "comments": (["c", "ch", "cm", "cp", "cpf", "c1", "cs", "sd"], TARGET),
    "generic":  (["gp", "go", "gs", "gu", "gh", "ge", "gr", "gd", "gt", "gi"], TARGET_LARGE),
    "errors":   (["err", "ne", "nx"], TARGET),
    "diff":     (["gi", "gd", "gh", "gu"], TARGET),
    "numbers":  (["m", "mb", "mf", "mh", "mi", "mo", "mx", "il"], TARGET),
    "deco":     (["nd", "ni", "no", "nv", "py", "kc", "kd", "kt", "kn", "kp", "kr"], TARGET),
    "lines":    (["ln", "lnt"], TARGET_LARGE),
}

tokens = {}
for sel, col in re.findall(r"\.chroma\s+\.([a-zA-Z0-9_]+)\s*\{([^}]*)\}", css):
    cm = re.search(r"(?<!background-)color:\s*(#[0-9a-fA-F]{6})", col)
    if cm:
        tokens.setdefault(sel, tuple(int(cm.group(1).lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)))

fixes = {}
for group, (names, target) in GROUPS.items():
    for name in names:
        if name not in tokens:
            continue
        before = tokens[name]
        ctr = contrast(before)
        if ctr >= target:
            continue
        after = lift(before, target)
        after = cap_saturation(after, colorsys.rgb_to_hls(
            *[v / 255 for v in before])[2])
        if contrast(after) < target:
            after = cap_saturation(lift(after, target),
                                   colorsys.rgb_to_hls(*[v / 255 for v in before])[2])
        fixes[name] = (before, after, ctr, contrast(after))

print(f"repaired {len(fixes)} token colours\n")
print(f"  {'token':<8} {'was':<9} {'now':<9} {'ctr':>6} -> {'ctr':>6}")
print("  " + "-" * 46)
for name, (before, after, c1, c2) in sorted(fixes.items()):
    print(f"  .{name:<7} {to_hex(before):<9} {to_hex(after):<9} {c1:>6.2f} -> {c2:>6.2f}")

blocks = ["/*",
         " * Syntax highlighting.",
         " *",
         " * Generated from Chroma's `nord` palette - the most muted dark style",
         " * available - with dim token colours repaired for contrast.",
         " *",
         " * Regenerate with:",
         " *   python3 tools/gen_syntax_css.py",
         " *",
         " */",
         css.rstrip(), ""]

if fixes:
    blocks += ["", "/* Repaired for contrast: hue preserved, lightness raised. */"]
    rules = []
    for name, (_, after, _, _) in sorted(fixes.items()):
        rules.append(f".chroma .{name} {{ color: {to_hex(after)}; }}")
    # Fold into readable groups.
    for i in range(0, len(rules), 4):
        blocks.append(" ".join(rules[i:i + 4]))
    blocks.append("")

out = "\n".join(blocks)
with open("static/css/syntax.css", "w") as fh:
    fh.write(out)

print(f"\nwrote static/css/syntax.css ({len(out)} bytes)")
