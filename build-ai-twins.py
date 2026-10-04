#!/usr/bin/env python3
"""Build AI-friendly text twins of every page on the Well (tools.dnsc.ai).

For each page folder with an index.html, writes <page>/index.md next to it
(the landing page writes ai.md at the repo root). Also writes llms.txt and
llms-full.txt at the repo root.

Python stdlib only. Run from anywhere:  python3 build-ai-twins.py
"""
import datetime
import html
import json
import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://tools.dnsc.ai/"
SKIP_DIRS = {".git", "assets", ".impeccable", "relay", "cook", "node_modules"}

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
DROP_TAGS = {"title", "script", "style", "noscript", "template", "head", "nav", "link",
             "meta", "iframe", "object", "audio", "video", "source"}
DROP_CLASSES = {"site-nav", "site-foot", "dnsc-back", "ai-twin", "crumb",
                "skip", "skip-link", "share"}
BLOCK = {"address", "article", "aside", "blockquote", "body", "dd", "details",
         "dialog", "div", "dl", "dt", "fieldset", "figcaption", "figure",
         "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
         "li", "main", "ol", "p", "pre", "section", "summary", "table", "ul",
         "html", "tr", "td", "th", "thead", "tbody", "tfoot", "caption",
         "label", "output", "svg", "canvas", "select", "textarea", "button",
         "input"}
CONTROLS = {"input", "select", "textarea", "button", "canvas"}
# opening one of these closes an open <p>
CLOSES_P = BLOCK - {"label", "output", "svg", "canvas", "select", "textarea",
                    "button", "input", "td", "th", "tr"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.children = []
        self.parent = parent

    def cls(self):
        return set((self.attrs.get("class") or "").split())

    def text(self):
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag not in ("script", "style"):
                out.append(c.text())
        return "".join(out)

    def find_all(self, pred):
        for c in self.children:
            if isinstance(c, Node):
                if pred(c):
                    yield c
                yield from c.find_all(pred)


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def _close(self, tag):
        n = self.cur
        while n is not self.root:
            if n.tag == tag:
                self.cur = n.parent
                return True
            n = n.parent
        return False

    def handle_starttag(self, tag, attrs):
        if tag in CLOSES_P and self._open("p"):
            self._close("p")
        if tag == "li" and self.cur.tag == "li":
            self._close("li")
        if tag in ("td", "th") and self.cur.tag in ("td", "th"):
            self._close(self.cur.tag)
        if tag == "tr" and self._open("tr", stop={"table"}):
            self._close("tr")
        if tag == "option" and self.cur.tag == "option":
            self._close("option")
        n = Node(tag, [(k, v if v is not None else "") for k, v in attrs], self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        n = Node(tag, [(k, v if v is not None else "") for k, v in attrs], self.cur)
        self.cur.children.append(n)

    def _open(self, tag, stop=None):
        n = self.cur
        while n is not self.root:
            if n.tag == tag:
                return True
            if stop and n.tag in stop:
                return False
            n = n.parent
        return False

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self._close(tag)

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(src):
    b = TreeBuilder()
    b.feed(src)
    b.close()
    return b.root


# ---------- rendering ----------

WS = re.compile(r"\s+")


def esc_md(s):
    return s.replace("|", "\\|") if False else s


class Renderer:
    def __init__(self, page_url, root):
        self.base = page_url
        self.root = root
        self.labels = {}
        for lab in root.find_all(lambda n: n.tag == "label" and n.attrs.get("for")):
            self.labels[lab.attrs["for"]] = clean(lab.text())
        self.ids = {}
        for n in root.find_all(lambda n: "id" in n.attrs):
            self.ids[n.attrs["id"]] = n

    # ---- helpers
    def dropped(self, n):
        if n.tag in DROP_TAGS:
            return True
        if n.cls() & DROP_CLASSES:
            return True
        if n.attrs.get("aria-hidden") == "true":
            return True
        if n.tag == "label" and n.attrs.get("for") in self.ids:
            # consumed by the control it labels, unless it wraps the control
            if not any(isinstance(c, Node) and c.tag in CONTROLS for c in n.children):
                return True
        if n.tag == "output":
            return True
        return False

    def label_for(self, n):
        lab = n.attrs.get("aria-label")
        if not lab and n.attrs.get("aria-labelledby"):
            ref = self.ids.get(n.attrs["aria-labelledby"].split()[0])
            if ref is not None:
                lab = ref.text()
        if not lab and n.attrs.get("id") in self.labels:
            lab = self.labels[n.attrs["id"]]
        if not lab:
            p = n.parent
            while p is not None and p.tag != "#root":
                if p.tag == "label":
                    lab = "".join(c if isinstance(c, str) else (c.text() if c.tag not in CONTROLS else "")
                                  for c in p.children)
                    break
                p = p.parent
        if not lab:
            lab = n.attrs.get("placeholder") or n.attrs.get("title") or n.attrs.get("name") or ""
        return clean(lab)

    def href(self, h):
        h = h.strip()
        if not h or h.startswith("#") or h.startswith("javascript:"):
            return None
        return urljoin(self.base, h)

    # ---- controls described in one line
    def describe_control(self, n):
        t = n.tag
        lab = self.label_for(n)
        if t == "input":
            typ = (n.attrs.get("type") or "text").lower()
            if typ in ("hidden", "submit"):
                return None
            if typ == "range":
                lo, hi = n.attrs.get("min", "0"), n.attrs.get("max", "100")
                v = n.attrs.get("value")
                s = f"A slider sets {lab or 'a value'} from {lo} to {hi}"
                return s + (f", starting at {v}." if v else ".")
            if typ in ("checkbox", "radio"):
                return f"A {'checkbox' if typ == 'checkbox' else 'radio choice'}: {lab}." if lab else None
            if typ == "file":
                acc = n.attrs.get("accept")
                return f"A file picker{': ' + lab if lab else ''}{' (' + acc + ')' if acc else ''}."
            kind = {"url": "web address", "number": "number", "email": "email",
                    "search": "search", "date": "date", "tel": "phone",
                    "text": "text"}.get(typ, typ)
            ph = n.attrs.get("placeholder")
            s = f"A {kind} field{': ' + lab if lab else ''}"
            if ph and ph != lab:
                s += f" (for example {ph})"
            elif n.attrs.get("value"):
                s += f", starting at {n.attrs['value']}"
            return s + "."
        if t == "select":
            opts = [clean(o.text()) for o in n.find_all(lambda x: x.tag == "option")]
            opts = [o for o in opts if o]
            s = f"A menu chooses {lab or 'an option'}"
            return s + (": " + ", ".join(opts) + "." if opts else ".")
        if t == "textarea":
            ph = n.attrs.get("placeholder")
            return f"A text box{': ' + lab if lab else ''}{' (' + ph + ')' if ph and ph != lab else ''}."
        if t == "canvas":
            return f"An interactive drawing{': ' + lab if lab else ''}."
        return None

    def button_text(self, n):
        txt = clean(n.text()) if n.attrs.get("aria-hidden") != "true" else ""
        lab = n.attrs.get("aria-label")
        return clean(lab) if lab and (not txt or len(txt) <= 2) else txt

    # ---- inline rendering
    def inline(self, n, plain=False):
        parts = []
        prev = None  # None, "text", "box" (layout element) or "el"
        for c in n.children:
            if isinstance(c, str):
                parts.append(WS.sub(" ", c))
                prev = "text" if c.strip() else None
                continue
            if self.dropped(c):
                continue
            s = self.inline_el(c, plain)
            if not s.strip():
                if s:
                    parts.append(s)
                continue
            kind = "box" if is_box(c) else "el"
            glued = parts and not parts[-1][-1:].isspace() and not s[:1].isspace()
            if glued and prev:
                last = parts[-1].rstrip()
                if kind == "box" and prev == "box" and not s.lstrip("*[")[:1].islower():
                    parts.append(" · ")
                elif kind == "box" and prev == "text" and last[-1:].isalpha() and s.lstrip("*[")[:1].isupper():
                    parts.append(" · ")
                elif prev in ("box", "el") and not s.startswith((",", ".", ";", ":", ")", "[")):
                    parts.append(" ")
            parts.append(s)
            prev = kind
        return "".join(parts)

    def inline_el(self, c, plain=False):
        t = c.tag
        if t == "br":
            return "\n" if not plain else " "
        if t == "img":
            alt = clean(c.attrs.get("alt", ""))
            return f"[Image: {alt}]" if alt else ""
        if t == "svg":
            if c.attrs.get("role") == "img" and c.attrs.get("aria-label"):
                return f"[Chart: {clean(c.attrs['aria-label'])}]"
            return ""
        if t in CONTROLS and t != "button":
            return ""
        if t == "button":
            return ""
        if t == "a" and "cite" in c.cls():
            return f"[{clean(c.text())}]"
        inner = self.inline(c, plain)
        core = inner.strip()
        if not core:
            return inner if inner and t not in ("i", "b", "em", "strong", "span", "a") else (" " if inner else "")
        lead = " " if inner[:1].isspace() else ""
        trail = " " if inner[-1:].isspace() else ""
        if plain:
            return lead + core + trail
        if t in ("b", "strong") and re.search(r"\w", core):
            return f"{lead}**{core}**{trail}"
        if t in ("i", "em", "cite") and "\n" not in core and not is_box(c) and re.search(r"\w", core):
            return f"{lead}*{core}*{trail}"
        if t == "code":
            return f"{lead}`{core}`{trail}"
        if t == "a":
            h = self.href(c.attrs.get("href", ""))
            if h:
                return f"{lead}[{core}]({h}){trail}"
        if t == "sup":
            return f"{lead}^{core}{trail}"
        return inner

    # ---- block rendering
    def has_block(self, n):
        for c in n.children:
            if isinstance(c, Node) and not self.dropped(c):
                if c.tag in BLOCK:
                    return True
                if self.has_block(c):
                    return True
        return False

    def blocks(self, n, ctx):
        """Return list of markdown blocks for node n's children."""
        out = []
        run = []  # inline run of children
        btns = []

        def flush():
            if run:
                tmp = Node("span", parent=n)
                tmp.children = list(run)
                s = clean_inline(self.inline(tmp))
                if s:
                    out.append(s)
                run.clear()

        def flush_btns():
            if btns:
                names = [b for b in btns if b]
                glab = n.attrs.get("aria-label") if n.attrs.get("role") in ("group", "radiogroup", "tablist") else None
                if glab and len(names) > 1:
                    out.append(end_dot(f"A choice ({clean(glab)}): " + ", ".join(names)))
                elif len(names) == 1:
                    out.append(end_dot(f"A button: {names[0]}"))
                elif names:
                    out.append(end_dot("Buttons: " + ", ".join(names)))
                btns.clear()

        for c in n.children:
            if isinstance(c, str):
                if c.strip() or run:
                    run.append(c)
                continue
            if self.dropped(c):
                continue
            if c.tag == "button":
                flush()
                bt = self.button_text(c)
                if bt:
                    btns.append(bt)
                continue
            if c.tag in BLOCK or self.has_block(c):
                flush()
                flush_btns()
                out.extend(self.block(c, ctx))
            else:
                flush_btns()
                run.append(c)
        flush()
        flush_btns()
        return out

    def block(self, n, ctx):
        t = n.tag
        if re.fullmatch(r"h[1-6]", t):
            lvl = min(6, int(t[1]) + 1)
            txt = clean(self.inline(n, plain=True))
            return [f"{'#' * lvl} {txt}"] if txt else []
        if t in CONTROLS:
            if t == "button":
                bt = self.button_text(n)
                return [end_dot(f"A button: {bt}")] if bt else []
            d = self.describe_control(n)
            return [d] if d else []
        if t == "svg":
            s = self.inline_el(n)
            return [s] if s else []
        if t == "hr":
            return []
        if t in ("ul", "ol"):
            return self.list_block(n, ctx)
        if t == "dl":
            return self.dl_block(n, ctx)
        if t == "table" or n.attrs.get("role") == "table":
            return self.table_block(n)
        if t == "label":
            ctrls = list(n.find_all(lambda x: x.tag in CONTROLS))
            if ctrls:
                return [d for d in (self.describe_control(c) for c in ctrls) if d]
        if t == "a" and self.href(n.attrs.get("href", "")):
            inner = self.blocks(n, ctx)
            url = self.href(n.attrs["href"])
            for i, b in enumerate(inner):
                m = re.match(r"(#+) (.+)$", b)
                if m:
                    inner[i] = f"{m.group(1)} [{m.group(2)}]({url})"
                    return inner
            if inner:
                inner[-1] = f"[{inner[-1]}]({url})" if "\n" not in inner[-1] and "](" not in inner[-1] else inner[-1] + f" ([link]({url}))"
            return inner
        if t == "details":
            return self.details_block(n, ctx)
        if t == "blockquote":
            inner = self.blocks(n, ctx)
            return ["\n".join("> " + l if l else ">" for l in "\n\n".join(inner).split("\n"))] if inner else []
        if t == "pre":
            return ["```\n" + n.text().strip("\n") + "\n```"]
        if t in ("p", "figcaption", "caption", "summary", "dt", "dd", "label") and not self.has_block(n):
            s = clean_inline(self.inline(n))
            return [s] if s else []
        # generic container
        inner = self.blocks(n, ctx)
        if not inner:
            role = n.attrs.get("role")
            lab = n.attrs.get("aria-label")
            if lab and (role in ("group", "grid", "application", "img", "radiogroup", "listbox") or t in ("ul", "ol")):
                return [f"[Interactive: {clean(lab)}, drawn by the page in your browser.]"]
        return inner

    def list_block(self, n, ctx, depth=0):
        items = []
        i = 0
        ordered = n.tag == "ol"
        for li in n.children:
            if not isinstance(li, Node) or li.tag != "li" or self.dropped(li):
                continue
            i += 1
            sub_lists = []
            body = []
            for c in li.children:
                if isinstance(c, Node) and c.tag in ("ul", "ol") and not self.dropped(c):
                    sub_lists.append(c)
            tmp = Node("li", parent=li)
            tmp.children = [c for c in li.children if not (isinstance(c, Node) and c.tag in ("ul", "ol"))]
            if self.has_block(tmp):
                body = self.blocks(tmp, ctx)
                text = " ".join(b.replace("\n", " ") for b in body)
            else:
                text = clean_inline(self.inline(tmp))
            if not text and not sub_lists:
                continue
            marker = f"{i}." if ordered else "-"
            ind = "   " * depth
            items.append(f"{ind}{marker} {text}".rstrip())
            for sl in sub_lists:
                items.extend(self.list_block(sl, ctx, depth + 1))
        if depth:
            return items
        if not items:
            lab = n.attrs.get("aria-label")
            return [f"[{clean(lab)}: filled in by the page in your browser.]"] if lab else []
        return ["\n".join(items)]

    def dl_block(self, n, ctx):
        lines = []
        term = None
        for c in n.find_all(lambda x: x.tag in ("dt", "dd")):
            s = clean_inline(self.inline(c))
            if not s:
                continue
            if c.tag == "dt":
                term = s
            else:
                lines.append(f"- **{term}**: {s}" if term else f"- {s}")
                term = None
        return ["\n".join(lines)] if lines else []

    def table_block(self, n):
        rows = []
        cap = None
        for c in n.find_all(lambda x: x.tag in ("tr", "caption") or x.attrs.get("role") == "row"):
            if c.tag == "caption":
                cap = clean_inline(self.inline(c))
                continue
            cells = []
            for td in c.children:
                if isinstance(td, Node) and not self.dropped(td) and (td.tag in ("td", "th") or td.attrs.get("role") in ("cell", "columnheader", "rowheader")):
                    s = clean_inline(self.inline(td)).replace("\n", " ").replace("|", "\\|")
                    cells.append(s)
                    for _ in range(int(td.attrs.get("colspan", "1") or 1) - 1):
                        cells.append("")
            if any(cells):
                rows.append(cells)
        if not rows:
            return []
        w = max(len(r) for r in rows)
        rows = [r + [""] * (w - len(r)) for r in rows]
        md = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w]
        md += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        out = []
        if cap:
            out.append(f"**{cap}**")
        out.append("\n".join(md))
        return out

    def details_block(self, n, ctx):
        summ = None
        rest = Node("div", parent=n)
        for c in n.children:
            if isinstance(c, Node) and c.tag == "summary" and summ is None:
                summ = clean(self.inline(c, plain=True))
            else:
                rest.children.append(c)
        out = []
        if summ:
            out.append(f"**{summ}**")
        out.extend(self.blocks(rest, ctx))
        return out


def end_dot(s):
    return s if s[-1:] in ".?!" else s + "."


def is_box(n):
    """Elements used as layout boxes rather than emphasis."""
    if n.tag in ("span", "small", "div", "label", "abbr", "time", "data"):
        return True
    if n.tag in ("i", "em", "b") and ("style" in n.attrs or "class" in n.attrs):
        return True
    return False


def clean(s):
    return WS.sub(" ", html.unescape(s or "")).strip()


def clean_inline(s):
    lines = [WS.sub(" ", l).strip() for l in s.split("\n")]
    s = "  \n".join(l for l in lines if l)
    s = re.sub(r"\*\*\s*\*\*", "", s)
    s = re.sub(r" +([,.;:)])(?=\s|$)", r"\1", s)
    s = s.replace("( ", "(")
    return s.strip()



# ---------- hydration: static data the page's own script draws ----------
# Some pages keep their data in a script and draw it in the browser. These
# hooks read that data out of the same page source and fill the empty
# containers, so the twin carries the numbers too.

def js_literal(src, name):
    """Parse `const NAME = [...]` (JS array/object literal) out of a script."""
    m = re.search(r"\b(?:const|let|var)\s+" + re.escape(name) + r"\s*=\s*", src)
    if not m:
        return None
    p = _JS(src, m.end())
    try:
        return p.value()
    except (ValueError, IndexError):
        return None


class _JS:
    def __init__(self, s, i):
        self.s, self.i = s, i

    def ws(self):
        while True:
            while self.s[self.i].isspace():
                self.i += 1
            if self.s.startswith("//", self.i):
                self.i = self.s.index("\n", self.i)
            elif self.s.startswith("/*", self.i):
                self.i = self.s.index("*/", self.i) + 2
            else:
                return

    def value(self):
        self.ws()
        c = self.s[self.i]
        if c == "[":
            self.i += 1
            out = []
            while True:
                self.ws()
                if self.s[self.i] == "]":
                    self.i += 1
                    return out
                out.append(self.value())
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
        if c == "{":
            self.i += 1
            out = {}
            while True:
                self.ws()
                if self.s[self.i] == "}":
                    self.i += 1
                    return out
                if self.s[self.i] in "\"'":
                    k = self.value()
                else:
                    m = re.compile(r"[\w$]+").match(self.s, self.i)
                    k = m.group(0)
                    self.i = m.end()
                self.ws()
                if self.s[self.i] != ":":
                    raise ValueError("object")
                self.i += 1
                out[k] = self.value()
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
        if c in "\"'":
            q = c
            self.i += 1
            buf = []
            while self.s[self.i] != q:
                if self.s[self.i] == "\\":
                    self.i += 1
                    buf.append({"n": "\n", "t": "\t"}.get(self.s[self.i], self.s[self.i]))
                else:
                    buf.append(self.s[self.i])
                self.i += 1
            self.i += 1
            return "".join(buf)
        m = re.compile(r"-?\d+(?:\.\d+)?(?:e-?\d+)?").match(self.s, self.i)
        if m:
            self.i = m.end()
            v = m.group(0)
            return float(v) if any(ch in v for ch in ".e") else int(v)
        for lit, val in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(lit, self.i):
                self.i += len(lit)
                return val
        raise ValueError("unsupported literal at %d" % self.i)


def fill(root, node_id, html_src, replace_parent_tag=None):
    for n in root.find_all(lambda x: x.attrs.get("id") == node_id):
        target = n
        if replace_parent_tag:
            while target.parent is not None and target.tag != replace_parent_tag:
                target = target.parent
        frag = parse(html_src)
        target.children = frag.children
        for c in frag.children:
            if isinstance(c, Node):
                c.parent = target
        return True
    return False


def esc(s):
    return html.escape(str(s), quote=False)


def hydrate_gas_tax(root, src, today):
    alloc = js_literal(src, "ALLOC")
    if not alloc:
        return
    rows = []
    for row in alloc:
        name, sub, v = row[0], row[1], row[2]
        kind = row[3] if len(row) > 3 else ""
        label = f"{name} (part of local governments)" if kind == "kid" else name
        rows.append(f"<tr><td>{esc(label)}</td><td>${v:.1f}M</td></tr>")
    fill(root, "alloc",
         "<thead><tr><th>Recipient</th><th>Estimated share of the $698.0M, 90 days</th></tr></thead><tbody>"
         + "".join(rows) + "<tr><td>Total</td><td>$698.0M</td></tr></tbody>",
         replace_parent_tag="table")


def hydrate_lunar(root, src, today):
    rows = js_literal(src, "rows")
    if rows:
        fill(root, "cycle", "".join(f"<li><b>{esc(r[1])}</b>: {esc(r[2])}</li>" for r in rows))
    astro = js_literal(src, "ASTRO_2026")
    types = js_literal(src, "TYPE") or {}
    if astro:
        iso = today.isoformat()

        def li(e):
            d = datetime.date.fromisoformat(e[0])
            kind = types.get(e[1], [e[1]])[0]
            extra = " ".join(x for x in e[3:5] if x)
            return f"<li><b>{d.strftime('%b %-d')} · {esc(e[2])}</b> ({esc(kind)}). {esc(extra)}</li>"
        up = [e for e in astro if e[0] >= iso]
        past = [e for e in astro if e[0] < iso]
        fill(root, "sky-up", "".join(li(e) for e in up))
        fill(root, "sky-more", "".join(li(e) for e in past))
        for n in root.find_all(lambda x: x.attrs.get("id") == "sky-more-wrap"):
            for c in n.children:
                if isinstance(c, Node) and c.tag == "summary":
                    c.children = ["Earlier in the year"]


HYDRATE = {"gas-tax/": hydrate_gas_tax, "well/lunar/": hydrate_lunar}


# ---------- pages ----------

def page_paths():
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        if "index.html" in filenames:
            rel = os.path.relpath(dirpath, ROOT)
            pages.append("" if rel == "." else rel.replace(os.sep, "/") + "/")
    return pages


def twin_name(rel):
    return "ai.md" if rel == "" else rel + "index.md"


def meta(root, name):
    for m in root.find_all(lambda n: n.tag == "meta"):
        if (m.attrs.get("name") or m.attrs.get("property")) == name:
            return clean(m.attrs.get("content", ""))
    return ""


def build_twin(rel, today, day):
    path = os.path.join(ROOT, rel, "index.html")
    src = open(path, encoding="utf-8").read()
    root = parse(src)
    if rel in HYDRATE:
        HYDRATE[rel](root, src, day)
    title_n = next(root.find_all(lambda n: n.tag == "title"), None)
    title = clean(title_n.text()) if title_n else rel.strip("/")
    desc = meta(root, "description") or meta(root, "og:description") or FALLBACK_DESC.get(rel, "")
    url = SITE + rel
    body = next(root.find_all(lambda n: n.tag == "body"), root)
    r = Renderer(url, root)
    blocks = r.blocks(body, {})
    # drop exact duplicate neighbours and a leading copy of the description
    tidy = []
    for b in blocks:
        if tidy and b == tidy[-1]:
            continue
        tidy.append(b)
    md = [f"# {title}", f"> {desc}" if desc else None, *tidy, "---",
          f"Source: {url} · Generated from the page on {today}"]
    text = "\n\n".join(x for x in md if x) + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return title, desc, text


# ---------- llms.txt ----------

SECTIONS = [
    ("Civic tools", ["follow-the-money/", "gas-tax/", "cannabis/"]),
    ("Daily games", ["well/", "well/daily-line/", "well/morning-edition/",
                     "well/one-word/", "well/one-word-advanced/", "well/five-moves/"]),
    ("Quiet rooms", ["well/walk-in/", "well/river/", "well/lunar/"]),
    ("Teaching", ["recipes/", "recipes/morning-inbox/", "ai-gauges/"]),
]
OPTIONAL = ["follow-the-money/v1-dustin/"]


def short_title(t):
    return re.sub(r"\s*·\s*((The Well\s*·\s*)?DNSC|Dustin Nimmo)$", "", t).strip()


# pieces.json: the shelf the landing page renders from. When a page has an entry, its
# llms.txt section and one-line description come from there, so the index and the page agree.
SECTION_NAMES = {"civic": "Civic tools", "games": "Daily games", "rooms": "Quiet rooms", "teaching": "Teaching"}


def load_pieces():
    try:
        data = json.load(open(os.path.join(ROOT, "pieces.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for p in data.get("pieces", []) if isinstance(data, dict) else []:
        href = (p or {}).get("href", "")
        if not href or "://" in href or href.startswith("/") or p.get("section") not in SECTION_NAMES:
            continue  # off-site cards (dnsc.ai) have no page here
        p = dict(p, rel=href if href.endswith("/") else href + "/")
        out.append(p)
    return out


# pages whose HTML carries no meta description
FALLBACK_DESC = {
    "follow-the-money/v1-dustin/": "The first edition of the Lakota bond calculator, kept for the record. The current edition is Issue 2, in Plain Numbers.",
}


def main():
    now = datetime.date.today()
    today = now.strftime("%b %-d, %Y")
    pages = page_paths()
    info = {}
    for rel in pages:
        title, desc, text = build_twin(rel, today, now)
        out = os.path.join(ROOT, twin_name(rel))
        open(out, "w", encoding="utf-8").write(text)
        info[rel] = (title, desc, text)
        print(f"wrote {twin_name(rel)}  ({len(text):,} chars)")

    pieces = load_pieces()
    by_rel = {p["rel"]: p for p in pieces}
    # section membership: the manifest first, then the lists above
    sections = [(name, [r for r in rels if r not in by_rel]) for name, rels in SECTIONS]
    newest = sorted(enumerate(pieces), key=lambda x: (x[1].get("date", ""), -x[0]), reverse=True)
    for _, p in newest:
        if p["rel"] in info or p.get("status") in ("coming", "live"):
            target = SECTION_NAMES[p["section"]]
            for name, rels in sections:
                if name == target:
                    rels.insert(sum(1 for r in rels if r in by_rel), p["rel"])
    placed = set(sum((s[1] for s in sections), [])) | set(OPTIONAL) | {""}
    extra = [p for p in pages if p not in placed]

    def line(rel):
        p = by_rel.get(rel)
        if rel not in info:  # a piece listed before its page lands here: no twin yet
            mark = " (coming)" if p.get("status") == "coming" else ""
            return f"- [{p['title']}]({SITE}{rel}){mark}: {p.get('line', '')}"
        title, desc, _ = info[rel]
        if p and p.get("line"):
            desc = p["line"]
        mark = " (coming)" if p and p.get("status") == "coming" else ""
        return f"- [{short_title(title)}]({SITE}{twin_name(rel)}){mark}: {desc}"

    L = ["# The Well, from DNSC", "",
         "> Free tools for the community from DNSC (Dustin Nimmo Strategic Consulting, West Chester, Ohio): "
         "civic tools that follow public money and public law from the record with every source linked, "
         "daily games that teach the vocabulary and the news of AI, quiet rooms, and teaching for working with AI. "
         "Every page has a plain text twin at index.md beside it.", "",
         f"Start at the landing page as text: [The Well]({SITE}ai.md). "
         "Teaching: https://dnsc.ai/teaching · The open method: https://github.com/theDTrain84/mise-en-place", ""]
    for name, rels in sections:
        rels = [r for r in rels if r in info or r in by_rel]
        if name == "Teaching":
            rels += extra
        if not rels:
            continue
        L.append(f"## {name}")
        L.append("")
        L += [line(r) for r in rels]
        L.append("")
    opt = [r for r in OPTIONAL if r in info]
    if opt:
        L += ["## Optional", ""] + [line(r) for r in opt] + [""]
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L).rstrip() + "\n")

    order = [""] + [r for _, rels in sections for r in rels if r in info] + extra + opt
    full = ["# The Well, from DNSC: every page as text", "",
            f"Generated {today} from {SITE}. Index: {SITE}llms.txt", ""]
    for rel in order:
        full.append(info[rel][2].rstrip())
        full.append("\n\n* * *\n")
    open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(full).rstrip() + "\n")
    print(f"wrote llms.txt, llms-full.txt ({len(pages)} pages)")


if __name__ == "__main__":
    main()
