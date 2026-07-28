#!/usr/bin/env python3
"""Scaffold, render, and audit consulting-grade infographic projects."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import mimetypes
import os
import re
import shutil
import struct
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"
DEFAULT_BRAND = ASSETS_DIR / "lovstudio-brand.json"
DEFAULT_USER_BRAND = Path("~/.lovstudio/skills/professional-infographic-brand.json")
DEFAULT_SHARED_PROFILE = Path("~/.lovstudio/skills/profile.json")

CANVASES: Dict[str, Tuple[int, int]] = {
    "4:5": (1080, 1350),
    "16:9": (1600, 900),
    "1:1": (1200, 1200),
    "A4": (1240, 1754),
}

REQUIRED_BRAND_FIELDS = (
    "name",
    "logo",
    "primary",
    "accent",
    "ink",
    "muted",
    "paper",
    "font_family",
    "copyright",
)

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|Lorem ipsum)\b|请替换|示例结构|占位",
    re.IGNORECASE,
)
EMOJI = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0000FE0F"
    "]"
)


class CliError(RuntimeError):
    """An actionable user-facing CLI error."""


def expand_path(value: str, base: Optional[Path] = None) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value))
    path = Path(expanded)
    if not path.is_absolute() and base is not None:
        path = base / path
    return path.resolve()


def read_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError as exc:
        raise CliError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CliError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def shared_profile_path() -> Path:
    raw = os.environ.get("LOVSTUDIO_SKILLS_PROFILE", str(DEFAULT_SHARED_PROFILE))
    return expand_path(raw)


def load_shared_profile() -> Dict[str, Any]:
    path = shared_profile_path()
    if not path.is_file():
        return {}
    return read_json(path)


def configured_brand_path(explicit: Optional[str]) -> Path:
    candidates: List[Optional[str]] = [
        explicit,
        os.environ.get("LOVSTUDIO_PROFESSIONAL_INFOGRAPHIC_BRAND_PROFILE"),
        os.environ.get("LOVSTUDIO_SKILLS_BRAND_PROFILE"),
    ]
    for candidate in candidates:
        if candidate:
            path = expand_path(candidate)
            if not path.is_file():
                raise CliError(f"Configured brand profile does not exist: {path}")
            return path

    profile = load_shared_profile()
    brand = profile.get("brand")
    if isinstance(brand, dict) and brand.get("profile"):
        path = expand_path(str(brand["profile"]), shared_profile_path().parent)
        if not path.is_file():
            raise CliError(
                "The shared profile points to a missing brand profile: "
                f"{path}. Run init-brand or fix brand.profile."
            )
        return path

    return DEFAULT_BRAND.resolve()


def validate_color(value: str, field: str) -> str:
    if not HEX_COLOR.fullmatch(value):
        raise CliError(f"{field} must be a six-digit hex color, got {value!r}")
    return value.upper()


def load_brand(explicit: Optional[str]) -> Tuple[Path, Dict[str, Any], Path]:
    profile_path = configured_brand_path(explicit)
    brand = read_json(profile_path)
    missing = [field for field in REQUIRED_BRAND_FIELDS if not brand.get(field)]
    if missing:
        raise CliError(
            f"Brand profile {profile_path} is missing: {', '.join(missing)}"
        )
    for field in ("primary", "accent", "ink", "muted", "paper"):
        brand[field] = validate_color(str(brand[field]), field)
    logo = expand_path(str(brand["logo"]), profile_path.parent)
    if not logo.is_file():
        raise CliError(f"Brand logo does not exist: {logo}")
    return profile_path, brand, logo


def logo_data_url(path: Path) -> str:
    media_type, _ = mimetypes.guess_type(path.name)
    if path.suffix.lower() == ".svg":
        media_type = "image/svg+xml"
    if not media_type or not media_type.startswith("image/"):
        raise CliError(f"Unsupported logo format: {path.suffix or path.name}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def safe_font_family(value: str) -> str:
    cleaned = value.replace("<", "").replace(">", "").replace("{", "")
    cleaned = cleaned.replace("}", "").replace(";", "")
    if not cleaned.strip():
        raise CliError("font_family cannot be empty")
    return cleaned


def semantic_units(value: str) -> int:
    cjk = len(
        re.findall(
            r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]",
            value,
        )
    )
    without_cjk = re.sub(
        r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]",
        " ",
        value,
    )
    latin_words = len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", without_cjk))
    return cjk + latin_words


def slugify(value: str) -> str:
    ascii_text = value.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    if slug:
        return slug[:48].rstrip("-")
    return f"infographic-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"


def resolve_output_root() -> Path:
    for key in (
        "LOVSTUDIO_PROFESSIONAL_INFOGRAPHIC_OUTPUT_DIR",
        "LOVSTUDIO_SKILLS_OUTPUT_DIR",
    ):
        if os.environ.get(key):
            return expand_path(os.environ[key])
    profile = load_shared_profile()
    workspace = profile.get("workspace")
    if isinstance(workspace, dict) and workspace.get("output_dir"):
        return expand_path(str(workspace["output_dir"]), shared_profile_path().parent)
    return (Path.cwd() / "professional-infographic").resolve()


def init_brand(args: argparse.Namespace) -> int:
    output = expand_path(args.output or str(DEFAULT_USER_BRAND))
    if output.exists() and not args.force:
        raise CliError(f"Refusing to overwrite existing brand profile: {output}")
    logo = expand_path(args.logo)
    if not logo.is_file():
        raise CliError(f"Logo does not exist: {logo}")

    brand = {
        "schema_version": 1,
        "name": args.name,
        "site": args.site or "",
        "logo": str(logo),
        "primary": validate_color(args.primary, "primary"),
        "accent": validate_color(args.accent, "accent"),
        "ink": validate_color(args.ink, "ink"),
        "muted": validate_color(args.muted, "muted"),
        "paper": validate_color(args.paper, "paper"),
        "font_family": safe_font_family(args.font_family),
        "copyright": args.copyright
        or f"Generated by {args.name}'s Professional Infographic Skill",
        "output_dir": args.output_dir or "$HOME/Documents/professional-infographic",
    }
    write_json(output, brand)
    print(f"Brand profile created: {output}")
    return 0


def render_template(template: str, replacements: Dict[str, str]) -> str:
    result = template
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", result)))
    if unresolved:
        raise CliError(f"Unresolved template variables: {', '.join(unresolved)}")
    return result


def scaffold_brief(title: str) -> str:
    return f"""# Infographic brief

Working title: {title}

## Audience and decision

- Audience:
- Decision or use moment:
- What should change after reading:

## Governing message

Write one answer-first sentence supported by the source.

## Supporting claims

1.
2.
3.

## Evidence ledger

- Claim:
  - Exact source:
  - Location:
  - Type: fact | estimate | assumption | interpretation
  - Unit / period:
  - Caveat:

## Assumptions and gaps

- None recorded yet.

## Visual job

- Primary relationship: compare | explain | locate | sequence | quantify | cause
- Recommended grammar:
- Secondary device, if any:

## Deliberate omissions

- List material excluded to preserve a single visual argument.
"""


def scaffold(args: argparse.Namespace) -> int:
    title = args.title.strip()
    if not title:
        raise CliError("--title cannot be empty")
    width, height = CANVASES[args.aspect]
    brand_path, brand, logo = load_brand(args.brand_profile)

    if args.output_dir:
        project_dir = expand_path(args.output_dir)
    else:
        project_dir = resolve_output_root() / slugify(title)
    if project_dir.exists() and any(project_dir.iterdir()):
        raise CliError(
            f"Refusing to write into non-empty project directory: {project_dir}"
        )
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "assets").mkdir(exist_ok=True)

    source_text = ""
    if args.source:
        source_path = expand_path(args.source)
        if not source_path.is_file():
            raise CliError(f"Source file does not exist: {source_path}")
        source_text = source_path.read_text(encoding="utf-8")
    if not source_text.strip():
        source_text = (
            "# Source\n\n"
            "Paste or preserve the exact source material here before authoring.\n"
        )

    template = (ASSETS_DIR / "poster-template.html").read_text(encoding="utf-8")
    replacements = {
        "TITLE": html.escape(title),
        "ASPECT": args.aspect,
        "CANVAS_WIDTH": str(width),
        "CANVAS_HEIGHT": str(height),
        "BRAND_NAME": html.escape(str(brand["name"])),
        "BRAND_LOGO_DATA_URL": logo_data_url(logo),
        "BRAND_PRIMARY": str(brand["primary"]),
        "BRAND_ACCENT": str(brand["accent"]),
        "BRAND_INK": str(brand["ink"]),
        "BRAND_MUTED": str(brand["muted"]),
        "BRAND_PAPER": str(brand["paper"]),
        "FONT_FAMILY": safe_font_family(str(brand["font_family"])),
        "COPYRIGHT": html.escape(str(brand["copyright"])),
        "SITE": html.escape(str(brand.get("site", ""))),
    }
    poster = render_template(template, replacements)

    (project_dir / "source.md").write_text(source_text, encoding="utf-8")
    (project_dir / "brief.md").write_text(
        scaffold_brief(title),
        encoding="utf-8",
    )
    (project_dir / "poster.html").write_text(poster, encoding="utf-8")
    project = {
        "schema_version": 1,
        "title": title,
        "aspect": args.aspect,
        "canvas": {"width": width, "height": height},
        "brand_profile": str(brand_path),
        "brand_name": brand["name"],
        "source": "source.md",
        "brief": "brief.md",
        "poster": "poster.html",
    }
    write_json(project_dir / "project.json", project)
    print(f"Project scaffolded: {project_dir}")
    print(f"Editable source: {project_dir / 'poster.html'}")
    return 0


def find_chrome() -> Optional[str]:
    candidates = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    return None


def import_playwright() -> Tuple[Any, Any]:
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise CliError(
            "Playwright is required. Install it with: "
            'python3 -m pip install "playwright>=1.45,<2" && '
            "python3 -m playwright install chromium"
        ) from exc
    return sync_playwright, PlaywrightError


def launch_browser(playwright: Any, playwright_error: Any) -> Any:
    try:
        return playwright.chromium.launch(
            headless=True,
            args=["--font-render-hinting=none"],
        )
    except playwright_error as first_error:
        chrome = find_chrome()
        if not chrome:
            raise CliError(
                "Chromium is unavailable. Run `python3 -m playwright install "
                "chromium` or set CHROME_PATH."
            ) from first_error
        try:
            return playwright.chromium.launch(
                headless=True,
                executable_path=chrome,
                args=["--font-render-hinting=none"],
            )
        except playwright_error as second_error:
            raise CliError(f"Could not launch Chromium or Chrome: {second_error}") from second_error


def detect_aspect(markup: str) -> str:
    poster_tag = re.search(
        r"<[^>]*\bclass=[\"'][^\"']*\bposter\b[^\"']*[\"'][^>]*>",
        markup,
        re.IGNORECASE,
    )
    match = (
        re.search(r'data-aspect=["\']([^"\']+)["\']', poster_tag.group(0))
        if poster_tag
        else None
    )
    if not match or match.group(1) not in CANVASES:
        raise CliError(
            "poster.html must set .poster data-aspect to one of: "
            + ", ".join(CANVASES)
        )
    return match.group(1)


def wait_until_ready(page: Any, timeout_ms: int) -> None:
    try:
        page.wait_for_function(
            "window.__INFOGRAPHIC_READY__ === true",
            timeout=timeout_ms,
        )
    except Exception as exc:
        raise CliError(
            "The poster did not set window.__INFOGRAPHIC_READY__ = true "
            f"within {timeout_ms} ms."
        ) from exc


def render(args: argparse.Namespace) -> int:
    input_path = expand_path(args.input)
    if not input_path.is_file():
        raise CliError(f"Input HTML does not exist: {input_path}")
    output_path = expand_path(args.output)
    if output_path.suffix.lower() != ".png":
        raise CliError("--output must end in .png")
    markup = input_path.read_text(encoding="utf-8")
    aspect = detect_aspect(markup)
    width, height = CANVASES[aspect]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sync_playwright, playwright_error = import_playwright()
    with sync_playwright() as playwright:
        browser = launch_browser(playwright, playwright_error)
        try:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=args.scale,
            )
            page = context.new_page()
            page.goto(input_path.as_uri(), wait_until="load", timeout=args.timeout)
            wait_until_ready(page, args.timeout)
            poster = page.locator(".poster")
            if poster.count() != 1:
                raise CliError("poster.html must contain exactly one .poster element")
            poster.screenshot(
                path=str(output_path),
                animations="disabled",
                type="png",
            )
        finally:
            browser.close()

    image_width, image_height = png_dimensions(output_path)
    print(
        f"Rendered: {output_path} "
        f"({image_width}x{image_height}, {args.scale}x)"
    )
    return 0


def png_dimensions(path: Path) -> Tuple[int, int]:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
    except FileNotFoundError as exc:
        raise CliError(f"PNG does not exist: {path}") from exc
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise CliError(f"Not a valid PNG: {path}")
    return struct.unpack(">II", header[16:24])


def browser_audit(input_path: Path, timeout_ms: int) -> Dict[str, Any]:
    markup = input_path.read_text(encoding="utf-8")
    aspect = detect_aspect(markup)
    width, height = CANVASES[aspect]
    sync_playwright, playwright_error = import_playwright()

    with sync_playwright() as playwright:
        browser = launch_browser(playwright, playwright_error)
        try:
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()
            page.goto(input_path.as_uri(), wait_until="load", timeout=timeout_ms)
            wait_until_ready(page, timeout_ms)
            result = page.evaluate(
                """() => {
                  const poster = document.querySelector('.poster');
                  if (!poster) return {missingPoster: true};
                  const posterRect = poster.getBoundingClientRect();

                  function rgba(value) {
                    const match = value.match(
                      /rgba?\\(\\s*([\\d.]+)[, ]+([\\d.]+)[, ]+([\\d.]+)(?:\\s*[,/]\\s*([\\d.]+))?\\s*\\)/
                    );
                    if (!match) return null;
                    return [
                      Number(match[1]), Number(match[2]), Number(match[3]),
                      match[4] === undefined ? 1 : Number(match[4])
                    ];
                  }

                  function backgroundFor(element) {
                    let node = element;
                    while (node) {
                      const parsed = rgba(getComputedStyle(node).backgroundColor);
                      if (parsed && parsed[3] > 0.01) return parsed;
                      node = node.parentElement;
                    }
                    return [255, 255, 255, 1];
                  }

                  function luminance(rgb) {
                    const channels = rgb.slice(0, 3).map((v) => {
                      const n = v / 255;
                      return n <= 0.03928 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4);
                    });
                    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
                  }

                  function contrast(fg, bg) {
                    if (!fg || !bg) return null;
                    const l1 = luminance(fg);
                    const l2 = luminance(bg);
                    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
                  }

                  const audited = [...document.querySelectorAll('[data-audit]')].map((el) => {
                    const rect = el.getBoundingClientRect();
                    const style = getComputedStyle(el);
                    const fg = rgba(style.color);
                    const bg = backgroundFor(el);
                    return {
                      kind: el.dataset.audit,
                      text: (el.innerText || el.textContent || '').trim(),
                      fontSize: Number.parseFloat(style.fontSize),
                      outside: rect.left < posterRect.left - 1 ||
                               rect.top < posterRect.top - 1 ||
                               rect.right > posterRect.right + 1 ||
                               rect.bottom > posterRect.bottom + 1,
                      contrast: contrast(fg, bg)
                    };
                  });

                  const containerNodes = [
                    ...poster.querySelectorAll(
                      '[data-audit-container], [data-region="visual"], [data-primary-block]'
                    )
                  ];
                  const containers = containerNodes.map((el) => {
                    const rect = el.getBoundingClientRect();
                    const name = el.hasAttribute('data-region')
                        ? `[data-region="${el.getAttribute('data-region')}"]`
                        : el.hasAttribute('data-primary-block')
                          ? '[data-primary-block]'
                          : '[data-audit-container]';
                    return {
                      name,
                      text: (el.innerText || '').trim().slice(0, 80),
                      overflow: el.scrollWidth > el.clientWidth + 2 ||
                                el.scrollHeight > el.clientHeight + 2,
                      outside: rect.left < posterRect.left - 1 ||
                               rect.top < posterRect.top - 1 ||
                               rect.right > posterRect.right + 1 ||
                               rect.bottom > posterRect.bottom + 1
                    };
                  });

                  const images = [...poster.querySelectorAll('img')].map((img) => ({
                    alt: img.alt,
                    src: img.getAttribute('src') || '',
                    complete: img.complete,
                    naturalWidth: img.naturalWidth,
                    naturalHeight: img.naturalHeight
                  }));

                  return {
                    missingPoster: false,
                    width: Math.round(posterRect.width),
                    height: Math.round(posterRect.height),
                    titleCount: poster.querySelectorAll('.poster__title[data-audit="title"]').length,
                    visualCount: poster.querySelectorAll('[data-region="visual"]').length,
                    sourceCount: poster.querySelectorAll('.source-note[data-audit="source"]').length,
                    attributionCount: poster.querySelectorAll('.generation-note[data-audit="attribution"]').length,
                    brandLogoCount: poster.querySelectorAll('.brand-lockup img').length,
                    primaryBlocks: poster.querySelectorAll('[data-primary-block]').length,
                    text: poster.innerText.trim(),
                    audited,
                    containers,
                    images
                  };
                }"""
            )
            if not isinstance(result, dict):
                raise CliError("Browser audit returned an invalid result")
            result["aspect"] = aspect
            return result
        finally:
            browser.close()


def add_issue(
    items: List[Dict[str, str]],
    code: str,
    message: str,
    selector: str = "",
) -> None:
    item = {"code": code, "message": message}
    if selector:
        item["selector"] = selector
    items.append(item)


def audit(args: argparse.Namespace) -> int:
    input_path = expand_path(args.input)
    if not input_path.is_file():
        raise CliError(f"Input HTML does not exist: {input_path}")
    markup = input_path.read_text(encoding="utf-8")
    aspect = detect_aspect(markup)
    expected_width, expected_height = CANVASES[aspect]
    result = browser_audit(input_path, args.timeout)
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    if result.get("missingPoster"):
        add_issue(errors, "missing-poster", "Missing .poster canvas")
    if result.get("width") != expected_width or result.get("height") != expected_height:
        add_issue(
            errors,
            "canvas-size",
            "Canvas is "
            f"{result.get('width')}x{result.get('height')}; expected "
            f"{expected_width}x{expected_height} for {aspect}",
            ".poster",
        )

    required_counts = {
        "titleCount": (".poster__title[data-audit='title']", "title"),
        "visualCount": ("[data-region='visual']", "main visual"),
        "sourceCount": (".source-note[data-audit='source']", "source note"),
        "attributionCount": (
            ".generation-note[data-audit='attribution']",
            "generation attribution",
        ),
        "brandLogoCount": (".brand-lockup img", "brand logo"),
    }
    for key, (selector, label) in required_counts.items():
        if result.get(key) != 1:
            add_issue(
                errors,
                f"required-{key}",
                f"Expected exactly one {label}; found {result.get(key, 0)}",
                selector,
            )

    primary_blocks = int(result.get("primaryBlocks", 0))
    if primary_blocks < 2 or primary_blocks > 7:
        add_issue(
            errors,
            "primary-block-count",
            f"Primary visual blocks must be between 2 and 7; found {primary_blocks}",
            "[data-primary-block]",
        )
    elif primary_blocks < 3 or primary_blocks > 5:
        add_issue(
            warnings,
            "primary-block-count",
            f"Primary visual blocks are strongest at 3–5; found {primary_blocks}",
            "[data-primary-block]",
        )

    full_text = str(result.get("text", ""))
    if PLACEHOLDER.search(full_text):
        add_issue(
            errors,
            "placeholder-copy",
            "Visible placeholder or demonstration copy remains in the poster",
            ".poster",
        )
    if EMOJI.search(full_text):
        add_issue(
            errors,
            "emoji",
            "Emoji detected; use a restrained icon or typographic label",
            ".poster",
        )

    text_limits = {
        "title": (24, 34),
        "takeaway": (55, 85),
        "label": (10, 16),
        "description": (32, 48),
    }
    for item in result.get("audited", []):
        kind = str(item.get("kind", ""))
        text_value = str(item.get("text", "")).strip()
        units = semantic_units(text_value)
        if not text_value:
            add_issue(errors, "empty-copy", f"Empty audited {kind}", f"[data-audit='{kind}']")
        if kind in text_limits:
            recommended, hard = text_limits[kind]
            if units > hard:
                add_issue(
                    errors,
                    f"{kind}-length",
                    f"{kind} has {units} semantic units; hard ceiling is {hard}",
                    f"[data-audit='{kind}']",
                )
            elif units > recommended:
                add_issue(
                    warnings,
                    f"{kind}-length",
                    f"{kind} has {units} semantic units; recommended maximum is {recommended}",
                    f"[data-audit='{kind}']",
                )
        if item.get("outside"):
            add_issue(
                errors,
                "out-of-bounds",
                f"Content extends beyond the poster: {text_value[:80]}",
                f"[data-audit='{kind}']",
            )
        font_size = float(item.get("fontSize") or 0)
        if font_size < 12:
            add_issue(
                errors,
                "font-size",
                f"Audited text is {font_size:.1f}px; minimum is 12px",
                f"[data-audit='{kind}']",
            )
        contrast = item.get("contrast")
        if isinstance(contrast, (int, float)):
            threshold = 3.0 if font_size >= 24 else 4.5
            if contrast + 0.01 < threshold:
                add_issue(
                    errors,
                    "contrast",
                    f"Contrast ratio {contrast:.2f}:1 is below {threshold:.1f}:1",
                    f"[data-audit='{kind}']",
                )

    for container in result.get("containers", []):
        if container.get("overflow"):
            add_issue(
                errors,
                "container-overflow",
                f"Content overflows {container.get('name')}: "
                f"{str(container.get('text', ''))[:80]}",
                str(container.get("name", "")),
            )
        if container.get("outside"):
            add_issue(
                errors,
                "container-out-of-bounds",
                f"{container.get('name')} extends beyond the poster canvas",
                str(container.get("name", "")),
            )

    total_limits = {"4:5": 520, "16:9": 420, "1:1": 420, "A4": 680}
    total_units = semantic_units(full_text)
    if total_units > total_limits[aspect]:
        add_issue(
            warnings,
            "copy-density",
            f"Poster has {total_units} semantic units; target maximum is "
            f"{total_limits[aspect]} for {aspect}",
            ".poster",
        )

    images = result.get("images", [])
    for index, image in enumerate(images):
        if not image.get("complete") or int(image.get("naturalWidth") or 0) <= 0:
            add_issue(
                errors,
                "broken-image",
                f"Image {index + 1} did not load",
                f".poster img:nth-of-type({index + 1})",
            )
        if not str(image.get("alt", "")).strip():
            add_issue(
                warnings,
                "missing-alt",
                f"Image {index + 1} has no alt text",
                f".poster img:nth-of-type({index + 1})",
            )

    logo_images = [
        image for image in images if str(image.get("src", "")).startswith("data:image/")
    ]
    if result.get("brandLogoCount") == 1 and not logo_images:
        add_issue(
            errors,
            "logo-portability",
            "Brand logo must be embedded as a data URL in the generated project",
            ".brand-lockup img",
        )

    image_info: Optional[Dict[str, Any]] = None
    if args.image:
        image_path = expand_path(args.image)
        image_width, image_height = png_dimensions(image_path)
        image_info = {
            "path": str(image_path),
            "width": image_width,
            "height": image_height,
        }
        if (
            image_width % expected_width != 0
            or image_height % expected_height != 0
            or image_width // expected_width != image_height // expected_height
        ):
            add_issue(
                errors,
                "png-size",
                f"PNG is {image_width}x{image_height}; expected an integer scale "
                f"of {expected_width}x{expected_height}",
            )
        else:
            image_info["scale"] = image_width // expected_width

    report: Dict[str, Any] = {
        "schema_version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "input": str(input_path),
        "aspect": aspect,
        "canvas": {"width": expected_width, "height": expected_height},
        "image": image_info,
        "metrics": {
            "primary_blocks": primary_blocks,
            "semantic_units": total_units,
            "audited_elements": len(result.get("audited", [])),
            "images": len(images),
        },
        "errors": errors,
        "warnings": warnings,
        "status": "fail" if errors or (args.strict and warnings) else "pass",
        "strict": bool(args.strict),
    }

    if args.report:
        write_json(expand_path(args.report), report)

    print(
        f"Audit {report['status'].upper()}: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    for label, issues in (("ERROR", errors), ("WARN", warnings)):
        for issue in issues:
            selector = f" [{issue['selector']}]" if issue.get("selector") else ""
            print(f"{label} {issue['code']}: {issue['message']}{selector}")

    if errors:
        return 2
    if args.strict and warnings:
        return 1
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Create, render, and audit professional infographic projects."
    )
    subparsers = root.add_subparsers(dest="command", required=True)

    brand_parser = subparsers.add_parser(
        "init-brand",
        help="Create a portable user brand profile.",
    )
    brand_parser.add_argument("--name", required=True, help="Brand name.")
    brand_parser.add_argument("--logo", required=True, help="SVG, PNG, JPEG, or WebP logo.")
    brand_parser.add_argument("--site", default="", help="Brand website.")
    brand_parser.add_argument("--primary", default="#24324A")
    brand_parser.add_argument("--accent", default="#D97757")
    brand_parser.add_argument("--ink", default="#172033")
    brand_parser.add_argument("--muted", default="#697386")
    brand_parser.add_argument("--paper", default="#F7F4EF")
    brand_parser.add_argument(
        "--font-family",
        default="Inter, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif",
    )
    brand_parser.add_argument("--copyright", help="Attribution printed on every image.")
    brand_parser.add_argument("--output-dir", help="Default infographic output directory.")
    brand_parser.add_argument("--output", help="Brand-profile JSON path.")
    brand_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing profile.",
    )
    brand_parser.set_defaults(handler=init_brand)

    scaffold_parser = subparsers.add_parser(
        "scaffold",
        help="Create a non-destructive editable infographic project.",
    )
    scaffold_parser.add_argument("--title", required=True, help="Working action title.")
    scaffold_parser.add_argument("--source", help="UTF-8 source Markdown/text file.")
    scaffold_parser.add_argument(
        "--aspect",
        choices=list(CANVASES),
        default="4:5",
    )
    scaffold_parser.add_argument(
        "--output-dir",
        help="Exact project directory; must be empty or absent.",
    )
    scaffold_parser.add_argument("--brand-profile", help="Brand-profile JSON path.")
    scaffold_parser.set_defaults(handler=scaffold)

    render_parser = subparsers.add_parser(
        "render",
        help="Render .poster from HTML to a high-resolution PNG.",
    )
    render_parser.add_argument("--input", required=True, help="poster.html path.")
    render_parser.add_argument("--output", required=True, help="Output .png path.")
    render_parser.add_argument("--scale", type=int, choices=(1, 2, 3), default=2)
    render_parser.add_argument("--timeout", type=int, default=15000, help="Timeout in ms.")
    render_parser.set_defaults(handler=render)

    audit_parser = subparsers.add_parser(
        "audit",
        help="Audit structure, copy budgets, overflow, contrast, assets, and PNG size.",
    )
    audit_parser.add_argument("--input", required=True, help="poster.html path.")
    audit_parser.add_argument("--image", help="Rendered PNG path to verify.")
    audit_parser.add_argument("--report", help="Write JSON audit report.")
    audit_parser.add_argument("--timeout", type=int, default=15000, help="Timeout in ms.")
    audit_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat editorial warnings as a non-zero result.",
    )
    audit_parser.set_defaults(handler=audit)
    return root


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
