#!/usr/bin/env python3
"""Generates the All In One static website.
Edit SITE_URL below to your real domain, then run:  python3 build.py
"""
import html, json, os
from datetime import date

SITE_URL = "https://www.example.com"   # <-- change to your domain (no trailing slash)
SITE_NAME = "All In One"
OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()

TOOLS = [
 dict(slug="instagram-video-downloader", name="Instagram Downloader", h1="Instagram Video & Reel Downloader",
      icon="📷", color="#ec4899", cat="downloader", kind="downloader", platform="instagram",
      short="Save Instagram reels, videos and photos you have permission to download.",
      long="Paste the link of an Instagram reel, video or photo and get a download link in seconds. Works on phones, tablets and computers with no app to install. Only download content that is yours or that the owner has allowed you to save.",
      steps=["Open Instagram and copy the link of the post or reel.", "Paste the link in the box above.", "Press Fetch and choose the file you want to save."],
      faq=[("Is it free?", "Yes, it is free to use."), ("Does it work on mobile?", "Yes. Paste the link in your mobile browser and download directly to your phone."), ("Can I download private posts?", "No. Only public content that you have the right to save.")]),
 dict(slug="youtube-video-downloader", name="YouTube Downloader", h1="YouTube Video Downloader",
      icon="▶️", color="#ef4444", cat="downloader", kind="downloader", platform="youtube",
      short="Download YouTube videos you own or that are free to reuse.",
      long="Paste a YouTube link to get downloadable video or audio files in different qualities. Use it for your own uploads, Creative Commons videos or anything the creator allows you to save offline.",
      steps=["Copy the video link from YouTube.", "Paste it in the box above.", "Press Fetch and pick a quality."],
      faq=[("Which qualities are available?", "That depends on the video. Common choices are 360p, 720p and 1080p."), ("Can I get only the audio?", "If your backend supports it, audio-only files appear in the list."), ("Is it legal?", "Download only your own videos or content with a licence that permits it.")]),
 dict(slug="facebook-video-downloader", name="Facebook Downloader", h1="Facebook Video Downloader",
      icon="👍", color="#2563eb", cat="downloader", kind="downloader", platform="facebook",
      short="Save public Facebook videos that you are allowed to keep.",
      long="Copy the link of a public Facebook video, paste it here and download it for offline viewing. Great for saving your own clips and videos shared with permission.",
      steps=["Copy the Facebook video link.", "Paste it in the box above.", "Press Fetch and download."],
      faq=[("Why does a link fail?", "Private videos and videos from closed groups cannot be fetched."), ("Is there a limit?", "No limit on the website itself; your backend sets any limits."), ("Is it safe?", "We never ask for your Facebook password.")]),
 dict(slug="tiktok-video-downloader", name="TikTok Downloader", h1="TikTok Video Downloader",
      icon="🎵", color="#0f172a", cat="downloader", kind="downloader", platform="tiktok",
      short="Download your own TikTok videos or ones you have permission to save.",
      long="Paste a TikTok link to get the video file for offline use. Perfect for backing up your own TikToks. Please respect creators and only save videos you have permission to download.",
      steps=["Tap Share on the TikTok video and copy the link.", "Paste it in the box above.", "Press Fetch and download."],
      faq=[("Can I download my own videos?", "Yes, that is the best use of this tool."), ("Does it work on iPhone?", "Yes, use Safari or Chrome and save to Files."), ("Is a watermark added?", "No watermark is added by this website.")]),
 dict(slug="image-compressor", name="Image Compressor", h1="Compress Images Online",
      icon="🗜️", color="#22c55e", cat="image", kind="image-compress", platform="",
      short="Make JPG, PNG and WEBP photos much smaller. Private and instant.",
      long="Reduce the size of your pictures without a visible loss in quality. Everything happens inside your browser, so your photos are never uploaded to any server. Ideal for websites, email attachments and forms with file-size limits.",
      steps=["Drop one or many images into the box.", "Choose the quality and maximum width.", "Download each compressed image."],
      faq=[("Are my photos uploaded?", "No. Compression runs on your own device."), ("What quality should I pick?", "70–80% is a great balance of size and sharpness."), ("Can I compress many images at once?", "Yes, select or drop as many as you like.")]),
 dict(slug="image-converter", name="Image Converter", h1="Convert JPG, PNG & WEBP Images",
      icon="🔄", color="#f59e0b", cat="image", kind="image-convert", platform="",
      short="Switch images between JPG, PNG and WEBP formats in one click.",
      long="Need a WEBP for your website or a PNG for a design? Convert images between the most popular formats instantly. The conversion is done locally in your browser, so it is fast and private.",
      steps=["Drop your images in the box.", "Pick the output format.", "Download the converted files."],
      faq=[("Which formats are supported?", "JPG, PNG and WEBP."), ("Will quality drop?", "PNG is lossless; JPG and WEBP use high-quality settings."), ("Is it free?", "Yes, unlimited and free.")]),
 dict(slug="jpg-to-pdf", name="JPG to PDF", h1="Convert JPG & PNG Images to PDF",
      icon="🖼️", color="#8b5cf6", cat="pdf", kind="img2pdf", platform="",
      short="Turn photos into a single PDF. Reorder pages before you save.",
      long="Combine one or many pictures into a neat PDF document. Arrange the order, then download. The PDF is created on your device, so your images stay private.",
      steps=["Add your JPG or PNG images.", "Reorder with the arrows if needed.", "Press Create PDF."],
      faq=[("How many images can I add?", "As many as your device memory allows."), ("Can I change the order?", "Yes, use the up and down buttons."), ("Is the PDF stored anywhere?", "No, it is created on your device.")]),
 dict(slug="merge-pdf", name="Merge PDF", h1="Merge PDF Files Online",
      icon="📎", color="#0ea5e9", cat="pdf", kind="mergepdf", platform="",
      short="Join several PDF files into one document in seconds.",
      long="Combine multiple PDF files into a single file in the order you choose. Merging happens in your browser, so confidential documents never leave your computer.",
      steps=["Add two or more PDF files.", "Arrange them in the order you want.", "Press Merge PDF."],
      faq=[("Is there a page limit?", "No fixed limit; very large files depend on your device."), ("Are password-protected PDFs supported?", "Remove the password first, then merge."), ("Is it private?", "Yes, files are processed locally.")]),
 dict(slug="pdf-to-word", name="PDF to Word", h1="Convert PDF to Word (DOCX)",
      icon="📄", color="#2563eb", cat="pdf", kind="doc-convert", platform="", convert="pdf-to-word",
      short="Change a PDF into an editable Word document.",
      long="Turn PDF files into editable Word documents. This converter uses a secure conversion service connected to the website. Connect your backend in assets/config.js to enable it.",
      steps=["Drop your PDF in the box.", "Wait while it converts.", "Your DOCX file downloads automatically."],
      faq=[("Will the layout stay the same?", "Simple documents convert very well; complex layouts may need small fixes."), ("Can it read scanned PDFs?", "Only if your conversion service includes OCR."), ("Is it free?", "Yes.")]),
 dict(slug="word-to-pdf", name="Word to PDF", h1="Convert Word (DOC, DOCX) to PDF",
      icon="📝", color="#14b8a6", cat="pdf", kind="doc-convert", platform="", convert="word-to-pdf",
      short="Convert Word documents to PDF so they look the same everywhere.",
      long="Turn DOC and DOCX files into clean PDFs that open the same on every device. This converter uses a conversion service connected to the website. Connect your backend in assets/config.js to enable it.",
      steps=["Drop your Word file in the box.", "Wait while it converts.", "Your PDF downloads automatically."],
      faq=[("Which files work?", "DOC and DOCX."), ("Will fonts be kept?", "Fonts are embedded when your conversion service has them installed."), ("Is it free?", "Yes.")]),
]
CATS = [("all", "All tools"), ("downloader", "Video downloaders"), ("image", "Image tools"), ("pdf", "PDF & documents")]
E = html.escape


def head(title, desc, path, extra_ld=None, body_attrs=""):
    url = SITE_URL + path
    ld = ""
    if extra_ld:
        ld = '<script type="application/ld+json">' + json.dumps(extra_ld, ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<meta name="theme-color" content="#5b5bf0">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/logo.svg">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body{body_attrs}>
<header class="site-header"><div class="wrap nav">
  <a class="brand" href="/" aria-label="{SITE_NAME} home"><img src="/assets/logo.svg" alt="" width="44" height="44"><span>All <b>In One</b></span></a>
  <nav class="nav-links" aria-label="Main">
    <a href="/#downloaders">Downloaders</a><a href="/#image">Image tools</a><a href="/#pdf">PDF tools</a><a href="/#how">How it works</a>
  </nav>
</div></header>
"""


def foot(scripts=""):
    return f"""
<footer class="site-footer"><div class="wrap foot">
  <div><strong>{SITE_NAME}</strong> – free online tools for everyone.<br>© {date.today().year} {SITE_NAME}. All rights reserved.</div>
  <nav aria-label="Footer"><a href="/">Home</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></nav>
</div></footer>
<script src="/assets/config.js"></script>
{scripts}
<script src="/assets/app.js"></script>
</body></html>
"""


def card(t):
    return f"""<a class="tool" href="/{t['slug']}.html" data-cat="{t['cat']}">
  <div class="ico" style="background:{t['color']}" aria-hidden="true">{t['icon']}</div>
  <h3>{E(t['name'])}</h3><p>{E(t['short'])}</p><span class="go">Open tool →</span></a>"""


def build_index():
    cards = {c: "\n".join(card(t) for t in TOOLS if t["cat"] == c) for c, _ in CATS}
    chips = "".join(f'<button class="chip{" active" if c=="all" else ""}" data-cat="{c}">{E(n)}</button>' for c, n in CATS)
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/",
          "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/?q={query}", "query-input": "required name=query"}}
    s = head("All In One – Free Video Downloader, PDF Converter & Image Compressor",
             "Free online tools: Instagram, YouTube, Facebook and TikTok video downloaders, PDF to Word, Word to PDF, merge PDF, image compressor and converter. Fast, simple, no sign-up.",
             "/", ld)
    s += f"""
<main>
<section class="hero"><div class="wrap">
  <img class="hero-logo" src="/assets/logo.svg" alt="All In One logo: globe with app icons and a person downloading on a phone" width="150" height="150">
  <h1>Every tool you need, <b>all in one place</b></h1>
  <p class="lead">Download videos, convert PDF and Word files, and compress pictures. Free, fast and easy on any phone or computer.</p>
  <div class="search"><input id="toolSearch" type="search" placeholder="Search a tool… e.g. PDF, YouTube, compress" aria-label="Search tools"><span aria-hidden="true">🔍</span></div>
  <div class="chips" role="group" aria-label="Filter tools">{chips}</div>
</div></section>

<section class="section" id="downloaders"><div class="wrap">
  <h2>Video downloaders</h2><p class="sub">Save videos for offline viewing. Please download only content you own or have permission to use.</p>
  <div class="grid">{cards['downloader']}</div>
</div></section>

<section class="section" id="image"><div class="wrap">
  <h2>Image tools</h2><p class="sub">Private by design – your pictures are processed in your browser.</p>
  <div class="grid">{cards['image']}</div>
</div></section>

<section class="section" id="pdf"><div class="wrap">
  <h2>PDF &amp; document tools</h2><p class="sub">Convert, merge and create documents in a few clicks.</p>
  <div class="grid">{cards['pdf']}</div>
</div></section>

<section class="section" id="how"><div class="wrap">
  <h2>How it works</h2><p class="sub">Three simple steps for every tool.</p>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Choose a tool</h3><p>Pick what you need from the cards above, or search for it.</p></div>
    <div class="step"><div class="n">2</div><h3>Add your link or file</h3><p>Paste a link or drop a file. Each tool page explains exactly what to do.</p></div>
    <div class="step"><div class="n">3</div><h3>Download the result</h3><p>Get your file in seconds, with nothing to install and no sign-up.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap article">
  <h2>Why people use All In One</h2>
  <p>All In One brings the most-used online tools together: video downloaders for Instagram, YouTube, Facebook and TikTok, PDF and Word converters, a PDF merger, an image compressor and an image format converter. Every page is built to be quick, clear and friendly on mobile.</p>
  <p>Image and PDF tools run inside your browser, which keeps your files private. No account is needed and there is nothing to install.</p>
</div></section>
</main>
"""
    s += foot()
    write("index.html", s)


def panel(t):
    k = t["kind"]
    if k == "downloader":
        return f"""<div class="panel">
  <form id="dlForm" novalidate>
    <label for="dlUrl">Paste the {E(t['platform'].title())} link</label>
    <div class="row"><input id="dlUrl" type="url" placeholder="https://" autocomplete="off" required><button class="btn" type="submit">⬇ Fetch</button></div>
  </form>
  <div class="notice">Only download content that belongs to you or that the owner has given you permission to save. Respect copyright and each platform's terms.</div>
  <div id="status" class="status" role="status" aria-live="polite"></div>
  <div id="results" class="results"></div>
</div>"""
    drop = lambda accept, multi, text: f"""<div class="drop" tabindex="0" role="button" aria-label="Choose files">
    <strong>{text}</strong><small>or drag &amp; drop here</small>
    <input id="fileInput" type="file" accept="{accept}" {'multiple' if multi else ''} hidden></div>"""
    if k == "image-compress":
        return f"""<div class="panel">
  {drop("image/*", True, "📁 Choose images")}
  <div class="row">
    <label for="quality">Quality: <span id="qval">75%</span></label><input id="quality" type="range" min="20" max="95" value="75">
    <label for="maxw">Max width</label>
    <select id="maxw"><option value="0">Original</option><option value="3840">3840 px</option><option value="1920" selected>1920 px</option><option value="1280">1280 px</option><option value="800">800 px</option></select>
    <label for="format">Format</label>
    <select id="format"><option value="image/jpeg">JPG</option><option value="image/webp">WEBP</option></select>
  </div>
  <div id="status" class="status" role="status" aria-live="polite"></div>
  <div id="results" class="results"></div>
</div>"""
    if k == "image-convert":
        return f"""<div class="panel">
  {drop("image/*", True, "📁 Choose images")}
  <div class="row"><label for="format">Convert to</label>
    <select id="format"><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WEBP</option></select></div>
  <div id="status" class="status" role="status" aria-live="polite"></div>
  <div id="results" class="results"></div>
</div>"""
    if k in ("img2pdf", "mergepdf"):
        acc, label, btn = ("image/jpeg,image/png", "📁 Choose JPG or PNG images", "Create PDF") if k == "img2pdf" else ("application/pdf,.pdf", "📁 Choose PDF files", "Merge PDF")
        return f"""<div class="panel">
  {drop(acc, True, label)}
  <div id="results" class="results"></div>
  <div class="row"><button id="make" class="btn" disabled>{btn}</button></div>
  <div id="status" class="status" role="status" aria-live="polite"></div>
</div>"""
    acc = ".pdf,application/pdf" if t["convert"] == "pdf-to-word" else ".doc,.docx"
    return f"""<div class="panel">
  {drop(acc, False, "📁 Choose a file")}
  <div class="notice">This converter needs a conversion service. See the README to connect one.</div>
  <div id="status" class="status" role="status" aria-live="polite"></div>
</div>"""


def build_tool(t):
    title = f"{t['h1']} – Free & Fast | {SITE_NAME}"
    path = f"/{t['slug']}.html"
    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": SITE_URL + path,
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "description": t["short"],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": t["name"], "item": SITE_URL + path}]},
    ]
    attrs = ' data-tool="%s"' % {"image-compress": "image-compress", "image-convert": "image-convert",
                                  "img2pdf": "jpg-to-pdf", "mergepdf": "merge-pdf",
                                  "downloader": "downloader", "doc-convert": "doc-convert"}[t["kind"]]
    if t["platform"]:
        attrs += ' data-platform="%s"' % t["platform"]
    if t.get("convert"):
        attrs += ' data-convert="%s"' % t["convert"]
    s = head(title, t["short"] + " Free, fast and easy to use on mobile.", path, ld, attrs)
    steps = "".join(f"<li>{E(x)}</li>" for x in t["steps"])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in t["faq"])
    related = "".join(card(r) for r in TOOLS if r is not t and (r["cat"] == t["cat"]))[:]
    others = [r for r in TOOLS if r is not t][:3] if not related else None
    related_html = related or "".join(card(r) for r in others)
    s += f"""
<main class="wrap">
  <div class="crumbs"><a href="/">Home</a> › {E(t['name'])}</div>
  <div class="tool-hero"><div class="ico" style="background:{t['color']}" aria-hidden="true">{t['icon']}</div>
    <div><h1>{E(t['h1'])}</h1><p>{E(t['short'])}</p></div></div>
  {panel(t)}
  <section class="article">
    <h2>About this tool</h2><p>{E(t['long'])}</p>
    <h2>How to use it</h2><ol>{steps}</ol>
  </section>
  <section class="faq"><h2>Frequently asked questions</h2>{faq}</section>
  <section class="section"><h2>More tools</h2><div class="grid">{related_html}</div></section>
</main>
"""
    scripts = ""
    if t["kind"] in ("img2pdf", "mergepdf"):
        scripts = '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>'
    s += foot(scripts)
    write(t["slug"] + ".html", s)


def legal(slug, title, body):
    s = head(f"{title} | {SITE_NAME}", f"{title} for {SITE_NAME}.", f"/{slug}.html")
    s += f'<main class="wrap article"><div class="crumbs"><a href="/">Home</a> › {E(title)}</div><h1>{E(title)}</h1>{body}</main>'
    s += foot()
    write(slug + ".html", s)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def main():
    build_index()
    for t in TOOLS:
        build_tool(t)
    legal("privacy", "Privacy Policy", """
<p>Last updated: """ + TODAY + """.</p>
<p>The image compressor, image converter, JPG to PDF and Merge PDF tools process files inside your browser. Those files are not uploaded to our servers.</p>
<h2>Links and files sent to a service</h2><p>When you use a downloader or the PDF/Word converters, the link or file you provide is sent to the conversion service connected to this website so it can be processed. We do not keep it longer than needed to complete your request.</p>
<h2>Cookies and ads</h2><p>If advertising or analytics are added, they may use cookies. You can control cookies in your browser settings.</p>
<h2>Contact</h2><p>Add your contact email here.</p>""")
    legal("terms", "Terms of Use", """
<p>Last updated: """ + TODAY + """.</p>
<p>By using this website you agree to use it lawfully. Only download, convert or copy content that you own or that you have permission to use. You are responsible for respecting copyright and the terms of the platforms you download from.</p>
<p>The tools are provided "as is" without warranty. We may change or remove tools at any time.</p>""")

    urls = ["/"] + [f"/{t['slug']}.html" for t in TOOLS] + ["/privacy.html", "/terms.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod></url>\n"
    sm += "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("Built", len(urls), "pages")


if __name__ == "__main__":
    main()
