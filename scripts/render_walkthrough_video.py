#!/usr/bin/env python3
"""Render an animated walkthrough video for the burnt_toast.js demo.

The script uses only Python's standard library plus the system ffmpeg binary.
It creates SVG frames and asks ffmpeg to encode them into an MP4.
"""

from __future__ import annotations

import html
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


WIDTH = 1280
HEIGHT = 720
FPS = 24
DURATION_SECONDS = 28
OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "burnt_toast_walkthrough.mp4"


def ease_out_cubic(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return 1 - pow(1 - value, 3)


def ease_in_out(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return 0.5 - 0.5 * math.cos(math.pi * value)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


class Canvas:
    def __init__(self) -> None:
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
            "<defs>",
            '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#05070a" flood-opacity="0.35"/>',
            "</filter>",
            '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
            '<stop offset="0%" stop-color="#172331"/>',
            '<stop offset="100%" stop-color="#263849"/>',
            "</linearGradient>",
            "</defs>",
        ]

    def rect(self, x: float, y: float, w: float, h: float, fill: str, rx: float = 0, opacity: float = 1.0, stroke: str | None = None, sw: float = 2) -> None:
        stroke_part = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" opacity="{opacity:.3f}"{stroke_part}/>'
        )

    def circle(self, x: float, y: float, r: float, fill: str, opacity: float = 1.0) -> None:
        self.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" opacity="{opacity:.3f}"/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str, sw: float = 4, opacity: float = 1.0) -> None:
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw:.1f}" stroke-linecap="round" opacity="{opacity:.3f}"/>'
        )

    def text(self, x: float, y: float, value: str, size: int = 32, fill: str = "#ffffff", weight: int = 400, family: str = "Inter, Arial, sans-serif", opacity: float = 1.0) -> None:
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" opacity="{opacity:.3f}">{esc(value)}</text>'
        )

    def code_block(self, x: float, y: float, lines: list[str], highlight: int | None = None, width: float = 570) -> None:
        line_h = 34
        height = 36 + line_h * len(lines)
        self.rect(x, y, width, height, "#101820", 18, stroke="#3c5368", sw=2)
        self.circle(x + 26, y + 24, 7, "#ff6b6b")
        self.circle(x + 50, y + 24, 7, "#ffd166")
        self.circle(x + 74, y + 24, 7, "#06d6a0")
        for index, line in enumerate(lines):
            ty = y + 62 + index * line_h
            if highlight == index:
                self.rect(x + 18, ty - 25, width - 36, 32, "#203a4c", 8, opacity=0.95)
            self.text(x + 28, ty, line, 21, "#d7edf7", family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace")

    def browser_shell(self, x: float, y: float, w: float, h: float) -> None:
        self.parts.append(f'<g filter="url(#shadow)">')
        self.rect(x, y, w, h, "#eef3f8", 22)
        self.rect(x, y, w, 54, "#d8e2eb", 22)
        self.rect(x + 20, y + 18, 16, 16, "#ff6b6b", 8)
        self.rect(x + 46, y + 18, 16, 16, "#ffd166", 8)
        self.rect(x + 72, y + 18, 16, 16, "#06d6a0", 8)
        self.rect(x + 120, y + 14, w - 150, 26, "#ffffff", 13)
        self.text(x + 145, y + 34, "index.html - Burnt Toast Lib", 15, "#526271")
        self.rect(x, y + 54, w, h - 54, "#1e2a38", 0)
        self.parts.append("</g>")

    def button(self, x: float, y: float, label: str, active: bool = False) -> None:
        color = "#ffffff" if not active else "#ffe7a8"
        self.rect(x, y, 210, 54, color, 18, stroke="#c8d1dc", sw=2)
        self.text(x + 24, y + 35, label, 22, "#162331", weight=700)

    def cursor(self, x: float, y: float, scale: float = 1.0) -> None:
        pts = [
            (x, y),
            (x + 0 * scale, y + 42 * scale),
            (x + 11 * scale, y + 32 * scale),
            (x + 19 * scale, y + 54 * scale),
            (x + 33 * scale, y + 49 * scale),
            (x + 25 * scale, y + 28 * scale),
            (x + 40 * scale, y + 28 * scale),
        ]
        point_data = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        self.parts.append(f'<polygon points="{point_data}" fill="#ffffff" stroke="#172331" stroke-width="3"/>')

    def toast(self, x: float, y: float, label: str, progress: float | None = None, closing: bool = False) -> None:
        fill = "#008080" if not closing else "#176666"
        self.parts.append(f'<g filter="url(#shadow)">')
        self.rect(x, y, 300, 86, fill, 12)
        if progress is not None:
            self.rect(x, y, 300, 8, "#cbd5df", 4)
            self.rect(x, y, 300 * max(0.0, min(1.0, progress)), 8, "#ffffff", 4)
        self.text(x + 24, y + 54, label, 30, "#ffffff", weight=700)
        self.rect(x + 252, y + 44, 34, 34, "#ffffff", 10)
        self.text(x + 262, y + 68, "x", 24, "#172331", weight=800)
        self.parts.append("</g>")

    def flow_node(self, x: float, y: float, title: str, note: str) -> None:
        self.rect(x, y, 230, 92, "#f4fbff", 18, stroke="#8bb8d2", sw=2)
        self.text(x + 22, y + 36, title, 22, "#172331", weight=800)
        self.text(x + 22, y + 68, note, 17, "#526271")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts)


def draw_base(canvas: Canvas) -> None:
    canvas.rect(0, 0, WIDTH, HEIGHT, "url(#bg)")
    canvas.circle(1060, 100, 250, "#36566d", opacity=0.22)
    canvas.circle(120, 620, 290, "#0f1820", opacity=0.25)


def draw_demo(canvas: Canvas, t: float, mode: str) -> None:
    canvas.browser_shell(610, 115, 560, 430)
    canvas.button(655, 205, "sendToast()", active=mode == "manual")
    canvas.button(655, 285, "sendTimedToast()", active=mode == "timed")
    canvas.text(655, 405, "Demo page buttons call the public API.", 24, "#d7edf7")
    canvas.text(655, 442, "Toasts slide in from the right.", 20, "#aebdca")

    if mode == "manual":
        slide = ease_out_cubic((t - 11.2) / 1.0)
        x = 1175 - 320 * slide
        canvas.toast(x, 455, "toast")
        if 11.0 <= t <= 11.7:
            canvas.cursor(735, 230, 1.0)
    elif mode == "timed":
        slide = ease_out_cubic((t - 16.5) / 1.0)
        close = ease_in_out((t - 20.6) / 1.2)
        x = 1175 - 320 * slide + 330 * close
        progress = max(0.0, min(1.0, (t - 17.1) / 3.8))
        canvas.toast(x, 455, "Timed", progress=progress, closing=close > 0.1)
        if 16.1 <= t <= 16.8:
            canvas.cursor(760, 310, 1.0)


def draw_frame(t: float) -> str:
    c = Canvas()
    draw_base(c)

    if t < 4:
        fade = min(1.0, t / 0.8)
        c.text(80, 130, "How to use burnt_toast.js", 56, "#ffffff", 900, opacity=fade)
        c.text(84, 184, "A visual model for the demo JavaScript app", 30, "#b8d2e4", opacity=fade)
        c.flow_node(86, 290, "1. Load", "script tag")
        c.flow_node(370, 290, "2. Configure", "set colors/layout")
        c.flow_node(654, 290, "3. Init", "on page load")
        c.flow_node(938, 290, "4. Send", "toast message")
        for x in (316, 600, 884):
            c.line(x, 336, x + 48, 336, "#8bb8d2", 5)
            c.text(x + 50, 344, ">", 25, "#8bb8d2", weight=800)
        c.text(90, 540, "Use the API from buttons, event handlers, or any client-side script after init.", 28, "#eef6fb")

    elif t < 8:
        c.text(70, 88, "Step 1: add the library to your page", 42, "#ffffff", 900)
        c.code_block(
            70,
            145,
            [
                "<head>",
                '  <script src="burnt_toast.js"></script>',
                "</head>",
            ],
            highlight=1,
        )
        c.text(90, 390, "Place burnt_toast.js in your web directory.", 26, "#eef6fb")
        c.text(90, 430, "Then load it before your custom script runs.", 26, "#eef6fb")
        draw_demo(c, t, "idle")

    elif t < 12:
        c.text(70, 88, "Step 2: configure first, then initialize", 42, "#ffffff", 900)
        c.code_block(
            70,
            145,
            [
                'burnt_toast.setPlateParams("25vh", "8vh", "2vw", "teal");',
                'burnt_toast.setButtonColors("white", "black");',
                "burnt_toast.setIsProgressBarTop(true);",
                'addEventListener("load", burnt_toast.init);',
            ],
            highlight=3,
            width=690,
        )
        c.text(90, 385, "Call customization helpers before init.", 25, "#eef6fb")
        c.text(90, 424, "init creates the toast layer and applies styles.", 25, "#eef6fb")
        draw_demo(c, t, "manual" if t > 11 else "idle")

    elif t < 16:
        c.text(70, 88, "Step 3: show a toast until the user closes it", 40, "#ffffff", 900)
        c.code_block(
            70,
            145,
            [
                '<button onclick="burnt_toast.sendToast(\'toast\')">',
                "  sendToast()",
                "</button>",
            ],
            highlight=0,
            width=660,
        )
        c.text(90, 352, "Clicking the button calls sendToast(text).", 25, "#eef6fb")
        c.text(90, 391, "The toast slides in and stays visible.", 25, "#eef6fb")
        c.text(90, 430, "The x button calls the built-in close handler.", 25, "#eef6fb")
        draw_demo(c, 12, "manual")

    elif t < 22:
        c.text(70, 88, "Step 4: show a timed toast with progress", 40, "#ffffff", 900)
        c.code_block(
            70,
            145,
            [
                '<button onclick="burnt_toast.sendTimedToast(\'Timed\', 4000)">',
                "  sendTimedToast()",
                "</button>",
            ],
            highlight=0,
            width=725,
        )
        c.text(90, 352, "sendTimedToast(text, milliseconds) adds a progress bar.", 25, "#eef6fb")
        c.text(90, 391, "When time expires, the toast closes automatically.", 25, "#eef6fb")
        draw_demo(c, t, "timed")

    else:
        c.text(70, 88, "Usage model recap", 46, "#ffffff", 900)
        c.flow_node(86, 165, "HTML", "loads script")
        c.flow_node(370, 165, "Config", "sets CSS")
        c.flow_node(654, 165, "init", "adds cover")
        c.flow_node(938, 165, "API call", "creates toast")
        for x in (316, 600, 884):
            c.line(x, 211, x + 48, 211, "#8bb8d2", 5)
            c.text(x + 50, 219, ">", 25, "#8bb8d2", weight=800)
        c.text(90, 360, "Main functions to remember:", 30, "#eef6fb", weight=800)
        c.text(120, 415, "burnt_toast.init()", 25, "#d7edf7", family="ui-monospace, Menlo, Consolas, monospace")
        c.text(120, 455, "burnt_toast.sendToast(text)", 25, "#d7edf7", family="ui-monospace, Menlo, Consolas, monospace")
        c.text(120, 495, "burnt_toast.sendTimedToast(text, time)", 25, "#d7edf7", family="ui-monospace, Menlo, Consolas, monospace")
        c.toast(855, 455, "Ready")

    return c.finish()


def main() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required to render the walkthrough video")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    total_frames = DURATION_SECONDS * FPS

    with tempfile.TemporaryDirectory(prefix="burnt_toast_video_") as temp_dir:
        frame_dir = Path(temp_dir)
        for frame in range(total_frames):
            t = frame / FPS
            (frame_dir / f"frame_{frame:04d}.svg").write_text(draw_frame(t), encoding="utf-8")

        cmd = [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-framerate",
            str(FPS),
            "-i",
            str(frame_dir / "frame_%04d.svg"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(OUTPUT),
        ]
        subprocess.run(cmd, check=True)

    print(f"Wrote {OUTPUT.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
