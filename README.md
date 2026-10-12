# All In One – website

A fast, mobile-friendly static website with 10 tools.

## What works right away (no server needed)
- Image Compressor, Image Converter, JPG to PDF, Merge PDF (run in the visitor's browser)
- Homepage search and category filter, SEO pages, sitemap, robots.txt

## What needs a backend
Instagram / YouTube / Facebook / TikTok downloaders and PDF <-> Word cannot run in a browser alone.
Host a small server and put its URL in `assets/config.js`:

    window.ALLINONE_API = "https://api.yourdomain.com";

Endpoints the pages call:
- `POST /download` with JSON `{url, platform}` -> `{title, links:[{label, url}]}`
- `POST /convert/pdf-to-word` and `POST /convert/word-to-pdf` with multipart `file` -> returns the converted file

Until this is set, those pages show a clear "backend not connected" message instead of failing silently.

## Publish
1. Open `build.py`, change `SITE_URL` to your real domain, run `python3 build.py`.
2. Upload the whole folder to any host (Cloudflare Pages, Netlify, Vercel, GitHub Pages, cPanel).
3. Add the site to Google Search Console and submit `https://yourdomain.com/sitemap.xml`.
4. Add your contact email to the Privacy page (edit `build.py`, rebuild).

## Ranking honestly
Nobody can guarantee a top-10 position. The site already has what search engines want: fast static pages, one page per search phrase, clean titles and descriptions, FAQ and app structured data, a sitemap and mobile-friendly layout. Ranking for "youtube downloader" style searches is very competitive and takes months of: new useful tool pages, quality backlinks, and fast, reliable tools.

## Legal note
Downloading from Instagram, YouTube, Facebook and TikTok can break their terms and copyright law. Every downloader page tells visitors to save only content they own or have permission to use. Review the rules of your country and your hosting provider before launching those pages.
