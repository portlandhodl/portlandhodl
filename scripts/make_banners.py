#!/usr/bin/env python3
"""Generate the SVG banners used in README.md.

    python scripts/make_banners.py      # writes assets/banners/*.svg

Edit the PROJECTS / SECTIONS tables below and re-run. Everything is plain SVG
(no web fonts, no scripts) so GitHub's image proxy renders it as-is.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "banners"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
BG1, BG2 = "#1c1240", "#0a0c24"   # deep purple -> midnight blue
TEXT2, TEXT3 = "#b8b4e6", "#8f8bc4"

# Accent per category.
ACCENT = {
    "btc": ("#8b5cf6", "#c4b5fd"),   # violet
    "hw": ("#6366f1", "#a5b4fc"),    # indigo
    "rust": ("#3b82f6", "#93c5fd"),  # blue
    "edu": ("#0ea5e9", "#7dd3fc"),   # sky
    "biz": ("#c026d3", "#f0abfc"),   # fuchsia
}

# Icons: drawn in a 64x64 box, stroked with currentColor-equivalent (filled in by caller).
ICONS = {
    "bitcoin": '<circle cx="32" cy="32" r="27"/><path d="M24 19v26M28 13v6M35 13v6M28 45v6M35 45v6M21 19h14a6.5 6.5 0 0 1 0 13H24M24 32h13a6.5 6.5 0 0 1 0 13H21"/>',
    "gpu": '<rect x="6" y="18" width="52" height="28" rx="4"/><circle cx="24" cy="32" r="8"/><circle cx="44" cy="32" r="8"/><path d="M12 46v6M20 46v6M28 46v6M36 46v6M6 22H2"/>',
    "blocks": '<rect x="8" y="8" width="20" height="20" rx="3"/><rect x="36" y="8" width="20" height="20" rx="3"/><rect x="22" y="36" width="20" height="20" rx="3"/><path d="M18 28v8h4M46 28v8h-4"/>',
    "shield": '<path d="M32 6l22 8v16c0 14-10 24-22 28C20 54 10 44 10 30V14z"/><path d="M22 32l7 7 13-14"/>',
    "terminal": '<rect x="6" y="10" width="52" height="44" rx="5"/><path d="M6 20h52M16 32l8 6-8 6M30 44h14"/>',
    "bug": '<ellipse cx="32" cy="36" rx="13" ry="17"/><path d="M32 19v34M19 30H8M19 42H8M45 30h11M45 42h11M24 16l-5-7M40 16l5-7"/>',
    "key": '<circle cx="20" cy="32" r="12"/><path d="M32 32h26M48 32v10M56 32v7"/><circle cx="20" cy="32" r="4"/>',
    "tree": '<circle cx="32" cy="10" r="6"/><circle cx="14" cy="34" r="6"/><circle cx="50" cy="34" r="6"/><circle cx="6" cy="56" r="4"/><circle cx="24" cy="56" r="4"/><path d="M28 14L17 29M36 14l11 15M12 40l-4 12M17 40l5 12"/>',
    "forge": '<path d="M10 22h34l10 8H44v8H18c-6 0-8-4-8-8z"/><path d="M24 38v8h-8v6h32v-6h-8v-8"/>',
    "keyboard": '<rect x="4" y="16" width="56" height="32" rx="5"/><path d="M12 25h4M22 25h4M32 25h4M42 25h4M52 25h0M12 33h4M22 33h4M32 33h4M42 33h4M20 41h24"/>',
    "chip": '<rect x="16" y="16" width="32" height="32" rx="3"/><rect x="24" y="24" width="16" height="16"/><path d="M24 16V8M32 16V8M40 16V8M24 56v-8M32 56v-8M40 56v-8M16 24H8M16 32H8M16 40H8M56 24h-8M56 32h-8M56 40h-8"/>',
    "qr": '<rect x="8" y="8" width="18" height="18" rx="2"/><rect x="38" y="8" width="18" height="18" rx="2"/><rect x="8" y="38" width="18" height="18" rx="2"/><path d="M38 38h6v6h-6zM50 38h6M38 50h6M50 50h6v6M44 44h6v6"/>',
    "pen": '<path d="M44 8l12 12-30 30H14V38z"/><path d="M38 14l12 12M8 56h48"/>',
    "book": '<path d="M32 14C24 8 14 8 6 10v40c8-2 18-2 26 4 8-6 18-6 26-4V10c-8-2-18-2-26 4zM32 14v40"/>',
}

# id, category, icon, title, tagline (<= ~2 lines), chips, cta
PROJECTS = [
    ("sats-per-silicon", "btc", "gpu", "Sats per Silicon",
     "How many GPUs does one bitcoin buy? Live BTC/GPU ratio dashboard for 23 GPUs, gaming to H100.",
     ["Live data", "Hourly", "gpupairs.com"], "LIVE"),
    ("miniscript-studio", "btc", "blocks", "Miniscript Studio",
     "Visual, block-based Miniscript policy and descriptor designer with LifeHash identicons.",
     ["rust-miniscript", "WASM", "Descriptors"], "LIVE"),
    ("xproof", "btc", "shield", "xproof",
     "Prove two Bitcoin keys share a BIP32 xpub without revealing it. Zero-knowledge, in your browser.",
     ["Noir", "UltraHonk", "SP1 zkVM"], "LIVE"),
    ("wasm-bitcoin-tools", "btc", "terminal", "WASM Bitcoin Tools",
     "Run an unmodified Bitcoin Core offline in your browser on a v86_64 WebAssembly emulator.",
     ["Bitcoin Core", "WASM", "Offline"], "LIVE"),
    ("btcdeb-wasm", "btc", "bug", "btcdeb-wasm",
     "Bitcoin Script debugger in the browser, with live transactions pulled from mempool.space.",
     ["rust-bitcoin", "Script", "Debugger"], "LIVE"),
    ("north-pol", "btc", "key", "North Pol",
     "Lock bitcoin behind a spending policy committed into the Taproot output key (pay-to-contract).",
     ["Taproot", "PSBT", "P2C"], "LIVE"),
    ("miniscript-ast-viewer", "btc", "tree", "Miniscript AST Viewer",
     "Matrix-themed browser for Miniscript policy and descriptor syntax trees, fully client-side.",
     ["rust-miniscript", "WASM", "AST"], "LIVE"),
    ("descriptor-forge", "btc", "forge", "Descriptor Forge",
     "Decode and rebuild Bitcoin Core importdescriptors commands. One self-contained HTML file.",
     ["Descriptors", "Rust", "WASM"], "LIVE"),
    ("nyan-keys", "hw", "keyboard", "Nyan Keys",
     "FPGA mechanical keyboard: true USB 2.0 High Speed, 8000 Hz polling, full NKRO, sub-ms latency.",
     ["iCE40 FPGA", "STM32F723", "NyanOS"], "OPEN HW"),
    ("qrsnap", "biz", "qr", "QR Snap",
     "Dynamic QR code platform for automotive, powersports and retail with deep scan analytics.",
     ["SaaS", "Analytics", "qrsnap.io"], "LIVE"),
    ("inkwell", "rust", "pen", "Inkwell",
     "Fast Markdown editor powered by Rust + WebAssembly: live preview, math, diagrams, themes.",
     ["Rust", "WASM", "Markdown"], "LIVE"),
    ("bitcoin-bootcamp", "edu", "book", "Bitcoin Bootcamp",
     "Jupyter notebooks working through elliptic curves, serialization, transactions and Script.",
     ["Python", "ECC", "Script"], "LEARN"),
]

SECTIONS = [
    ("bitcoin-tools", "btc", "bitcoin", "Bitcoin Tools", "Miniscript · Descriptors · Taproot · PSBT · Zero-knowledge · in-browser WASM"),
    ("bitcoin-libraries", "btc", "chip", "Bitcoin Libraries & Research", "Rust · C++ · Lean 4 · Bitcoin Core · hardware wallet security"),
    ("hardware", "hw", "keyboard", "Hardware & Firmware", "FPGA · STM32 · ESP32 e-paper · USB 2.0 High Speed"),
    ("rust-wasm", "rust", "terminal", "Rust, WASM & Other Builds", "Emulators · dev tools · GameCube homebrew · terminals"),
    ("education", "edu", "book", "Bitcoin Education", "Notebooks · BIP lecture series · slideshows"),
    ("contributions", "btc", "bitcoin", "Upstream Contributions", "Bitcoin Core · BIPs · rust-bitcoin · rust-miniscript · mempool"),
]


def wrap(text: str, width: int) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur] if cur else lines


def icon(name: str, x: float, y: float, size: float, color: str, sw: float = 3.2) -> str:
    s = size / 64
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def defs(uid: str, a1: str, a2: str) -> str:
    return f'''<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="#3b82f6"/>
  </linearGradient>
  <radialGradient id="gb{uid}" cx="0.95" cy="1" r="0.8">
    <stop offset="0" stop-color="#2563eb" stop-opacity="0.20"/><stop offset="1" stop-color="#2563eb" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gl{uid}" cx="0.12" cy="0.2" r="0.7">
    <stop offset="0" stop-color="{a1}" stop-opacity="0.30"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="gr{uid}" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity="0.035"/>
  </pattern>
</defs>'''


def card(pid, cat, ic, title, tagline, chips, cta) -> str:
    W, H = 800, 300
    a1, a2 = ACCENT[cat]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}: {escape(tagline)}">',
           f"<title>{escape(title)}</title>", defs(pid, a1, a2),
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg{pid})"/>',
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#gr{pid})"/>',
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#gl{pid})"/>',
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#gb{pid})"/>',
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="{a1}" stroke-opacity="0.35" stroke-width="2"/>',
           f'<rect x="0" y="0" width="{W}" height="6" rx="3" fill="url(#ac{pid})"/>',
           # icon tile
           f'<rect x="40" y="44" width="104" height="104" rx="22" fill="{a1}" fill-opacity="0.12" stroke="{a1}" stroke-opacity="0.5" stroke-width="2"/>',
           icon(ic, 60, 64, 64, a2),
           f'<text x="172" y="94" font-family="{SANS}" font-size="42" font-weight="700" fill="#f0f6fc">{escape(title)}</text>']
    # status pill
    pw = 44 + len(cta) * 10
    out.append(f'<g transform="translate({W-40-pw} 40)"><rect width="{pw}" height="30" rx="15" fill="{a1}" fill-opacity="0.16" stroke="{a1}" stroke-opacity="0.6"/>'
               f'<circle cx="17" cy="15" r="4.5" fill="{a2}"/>'
               f'<text x="30" y="20" font-family="{MONO}" font-size="14" font-weight="700" fill="{a2}">{escape(cta)}</text></g>')
    for i, line in enumerate(wrap(tagline, 40)[:3]):
        out.append(f'<text x="172" y="{134 + i*30}" font-family="{SANS}" font-size="21" fill="{TEXT2}">{escape(line)}</text>')
    x = 40
    for c in chips:
        w = 26 + len(c) * 10.2
        out.append(f'<g transform="translate({x} 238)"><rect width="{w:.0f}" height="34" rx="8" fill="#ffffff" fill-opacity="0.05" stroke="#ffffff" stroke-opacity="0.12"/>'
                   f'<text x="{w/2:.0f}" y="23" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{TEXT2}">{escape(c)}</text></g>')
        x += w + 12
    out.append(f'<text x="{W-40}" y="261" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="600" fill="{a2}">Open →</text>')
    out.append("</svg>")
    return "\n".join(out)


def section(sid, cat, ic, title, sub) -> str:
    W, H = 1600, 140
    a1, a2 = ACCENT[cat]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}: {escape(sub)}">',
        f"<title>{escape(title)}</title>", defs(sid, a1, a2),
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#bg{sid})"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#gr{sid})"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#gl{sid})"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#gb{sid})"/>',
        f'<rect x="0" y="{H-6}" width="{W}" height="6" rx="3" fill="url(#ac{sid})"/>',
        icon(ic, 44, 30, 72, a2, 3.6),
        f'<text x="148" y="76" font-family="{SANS}" font-size="50" font-weight="800" fill="#f0f6fc">{escape(title)}</text>',
        f'<text x="150" y="112" font-family="{MONO}" font-size="22" fill="{TEXT3}">{escape(sub)}</text>',
        "</svg>"])


def hero() -> str:
    W, H = 1600, 420
    a1, a2 = ACCENT["btc"]
    tags = ["Bitcoin Core", "Miniscript", "Taproot", "PSBT", "Zero-knowledge", "Rust", "WebAssembly", "FPGA"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Portland.HODL: Bitcoin developer, Bitcoin Core contributor, builder of in-browser Bitcoin tools, Nyan Keys and QR Snap">',
           "<title>Portland.HODL</title>", defs("hero", a1, a2),
           f'<rect width="{W}" height="{H}" rx="24" fill="url(#bghero)"/>',
           f'<rect width="{W}" height="{H}" rx="24" fill="url(#grhero)"/>',
           f'<rect width="{W}" height="{H}" rx="24" fill="url(#glhero)"/>',
           f'<rect width="{W}" height="{H}" rx="24" fill="url(#gbhero)"/>',
           f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="23" fill="none" stroke="{a1}" stroke-opacity="0.35" stroke-width="3"/>']
    # big faint bitcoin mark on the right
    out.append(f'<g opacity="0.10">{icon("bitcoin", 1180, 40, 340, a1, 2.4)}</g>')
    # block chain strip
    for i in range(7):
        x = 1010 + i * 82
        out.append(f'<rect x="{x}" y="330" width="58" height="58" rx="8" fill="{a1}" fill-opacity="{0.08 + i*0.05:.2f}" stroke="{a1}" stroke-opacity="0.6" stroke-width="2"/>')
        if i:
            out.append(f'<path d="M{x-24} 359h24" stroke="{a1}" stroke-opacity="0.6" stroke-width="2"/>')
    out += [icon("bitcoin", 72, 70, 96, a1, 3.4),
            f'<text x="196" y="132" font-family="{SANS}" font-size="78" font-weight="800" fill="#f0f6fc">Portland<tspan fill="{a1}">.</tspan>HODL</text>',
            f'<text x="200" y="182" font-family="{SANS}" font-size="30" fill="{TEXT2}">Bitcoin developer · Bitcoin Core contributor · hardware hacker</text>',
            f'<text x="200" y="226" font-family="{SANS}" font-size="24" fill="{TEXT3}">In-browser Bitcoin tools, Rust + WASM, FPGA keyboards and the QR Snap platform.</text>']
    x = 72
    for t in tags:
        w = 30 + len(t) * 12.6
        if x + w > 990:
            break
        out.append(f'<g transform="translate({x} 330)"><rect width="{w:.0f}" height="44" rx="22" fill="{a1}" fill-opacity="0.12" stroke="{a1}" stroke-opacity="0.55"/>'
                   f'<text x="{w/2:.0f}" y="29" text-anchor="middle" font-family="{MONO}" font-size="19" fill="{a2}">{escape(t)}</text></g>')
        x += w + 12
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    for p in PROJECTS:
        (OUT / f"{p[0]}.svg").write_text(card(*p))
    for s in SECTIONS:
        (OUT / f"section-{s[0]}.svg").write_text(section(*s))
    print(f"wrote {1 + len(PROJECTS) + len(SECTIONS)} banners to {OUT}")


if __name__ == "__main__":
    main()
