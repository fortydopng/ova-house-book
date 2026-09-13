#!/usr/bin/env python3
"""Build the OVA-HOUSE interior book into docs/ (served by GitHub Pages).

    python build.py

Reads content/book.yaml, renders templates/*.html, copies static/ assets.
Images are produced separately by ingest.py and live in docs/img/.
"""
import datetime as dt
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def ru_date(d) -> str:
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def ru_area(a) -> str:
    return f"{a:.2f}".replace(".", ",") + " м²"


def prepare(book: dict) -> dict:
    statuses = book["statuses"]
    kinds = book.get("kinds", {})
    rooms = book["rooms"]
    for r in rooms:
        r["area_text"] = ru_area(r["area"])
        r["status_text"] = statuses.get(r["status"], "")
        versions = r.get("versions") or []
        r["visualized"] = bool(versions)
        if versions:
            cur = versions[-1]
            r["current"] = cur
            cur["date_text"] = ru_date(cur["date"])
            slides = []          # flat list for the lightbox: day and evening variants alike
            for img in cur["images"]:
                base = f"img/{r['slug']}/v{cur['n']}/{img['id']}"
                img["src"] = f"{base}-1600.webp"
                img["src_small"] = f"{base}-900.webp"
                img["kind_text"] = kinds.get(img.get("kind"), "")
                if img.get("evening"):
                    ev = f"img/{r['slug']}/v{cur['n']}/{img['evening']}"
                    img["src_evening"] = f"{ev}-1600.webp"
                    img["src_small_evening"] = f"{ev}-900.webp"
                    img["slide_day"] = len(slides)
                    slides.append({"src": img["src"], "caption": f"{img['caption']}, день"})
                    img["slide_evening"] = len(slides)
                    slides.append({"src": img["src_evening"], "caption": f"{img['caption']}, вечер"})
                else:
                    img["slide_day"] = len(slides)
                    slides.append({"src": img["src"], "caption": img["caption"]})
            cur["slides"] = slides
            r["cover"] = cur["images"][0]
            r["url"] = f"rooms/{r['slug']}/"
        # plan overlay: polygon points in percent (from plan_poly, or derived from plan_box)
        if r.get("plan_poly"):
            r["plan_points"] = " ".join(f"{x},{y}" for x, y in r["plan_poly"])
        elif r.get("plan_box"):
            b = r["plan_box"]
            l, t, w, h = b["left"], b["top"], b["width"], b["height"]
            r["plan_points"] = f"{l},{t} {l+w},{t} {l+w},{t+h} {l},{t+h}"
        # composition: status labels (group-level default, item-level override)
        labels = book.get("item_statuses", {})
        for g in r.get("composition") or []:
            g["status_text"] = labels.get(g.get("status"), "")
            for it in g["items"]:
                st = it.get("status")
                it["status_text"] = labels.get(st, "") if st and st != g.get("status") else ""
    site = book["site"]
    site["updated_text"] = ru_date(site["updated"])
    hero_room = next(x for x in rooms if x["code"] == site["hero"]["room"])
    hero_img = next(i for i in hero_room["current"]["images"] if i["id"] == site["hero"]["image"])
    site["hero_src"] = hero_img.get("src_evening") if site["hero"].get("light") == "evening" else hero_img["src"]
    book["visualized"] = [r for r in rooms if r["visualized"]]
    book["progress"] = f"Визуализировано помещений: {len(book['visualized'])} из {len(rooms)}"
    return book


def build() -> None:
    book = prepare(yaml.safe_load((ROOT / "content" / "book.yaml").read_text(encoding="utf-8")))
    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    build_id = dt.datetime.now().strftime("%Y%m%d%H%M")

    # static assets
    out_static = DOCS / "static"
    if out_static.exists():
        shutil.rmtree(out_static)
    shutil.copytree(ROOT / "static", out_static)

    # pages
    (DOCS / "index.html").write_text(
        env.get_template("index.html").render(book=book, site=book["site"], root="", build_id=build_id),
        encoding="utf-8")
    for r in book["visualized"]:
        d = DOCS / "rooms" / r["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            env.get_template("room.html").render(book=book, site=book["site"], room=r, root="../../",
                                                 build_id=build_id),
            encoding="utf-8")
    (DOCS / "404.html").write_text(
        env.get_template("404.html").render(book=book, site=book["site"], root="/ova-house-book/",
                                            build_id=build_id),
        encoding="utf-8")

    # service files
    (DOCS / ".nojekyll").write_text("")
    (DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print(f"built {len(book['visualized'])} room page(s) + index, build {build_id}")


if __name__ == "__main__":
    build()
