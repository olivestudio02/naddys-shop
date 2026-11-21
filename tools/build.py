#!/usr/bin/env python3
"""Generates the static pages. Run: python3 tools/build.py  (output is committed; Netlify needs no build)."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://naddysstudio.com"
IG = "https://www.instagram.com/naddys_studio/"
YT = "https://www.youtube.com/@Naddys_Studio"

CSS = """:root{--bg:#0b0b0c;--card:#151517;--line:#2a2a2d;--red:#6ec4ff;--txt:#f4eeea;--mut:#a09a96}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 400px at 50% -100px,#0f2a3d,transparent),var(--bg);color:var(--txt);font:17px/1.6 -apple-system,system-ui,Segoe UI,Roboto,sans-serif;padding:0 16px env(safe-area-inset-bottom)}
.wrap{max-width:720px;margin:0 auto}a{color:var(--red)}
nav{display:flex;align-items:center;justify-content:space-between;padding:14px 0;border-bottom:1px solid var(--line);gap:8px}
nav .brand{display:flex;align-items:center;gap:8px;text-decoration:none}nav .brand img.i{width:34px;height:auto}nav .brand img.n{width:104px;height:auto}
nav .links{display:flex;gap:14px;font-size:15px}nav .links a{color:var(--txt);text-decoration:none;padding:6px 0}nav .links a.on{color:var(--red);font-weight:700}
h1{font-size:30px;line-height:1.2;margin:28px 0 8px}h2{font-size:22px;margin:32px 0 8px}h3{font-size:18px;margin:20px 0 4px}
p,li{color:#e6e0dc}.mut{color:var(--mut)}.lead{font-size:19px;color:var(--txt)}
.btn{display:inline-block;margin-top:8px;padding:12px 20px;border-radius:12px;background:var(--red);color:#06121a;font-weight:700;text-decoration:none}
.btn.o{background:transparent;border:1px solid var(--red);color:var(--red)}
.box{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--red);border-radius:12px;padding:14px 16px;margin:20px 0;font-size:15.5px}
.box b.t{display:block;color:var(--red);font-size:12px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px}
.cards{display:grid;gap:12px;margin:16px 0}.cards a.c{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;text-decoration:none;color:var(--txt)}
.cards a.c b{display:block;font-size:18px;margin-bottom:4px}.cards a.c span{color:var(--mut);font-size:14.5px}
.tag{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--red);font-weight:700}
.hero{padding:28px 0 8px;text-align:center}.hero img{width:110px;height:auto}
.meta{color:var(--mut);font-size:14px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:20px 0 32px;color:var(--mut);font-size:13.5px;text-align:center}footer a{color:var(--txt)}footer p{margin:6px 0}
"""

NAV = [("Home","/"),("Articles","/articles/"),("Shop","/shop/"),("About","/about/")]

def page(path, title, desc, body, active="", extra_head="", article=None, og_title=None):
    url = SITE + path
    nav = "".join(f'<a href="{h}"{" class=on" if n==active else ""}>{n}</a>' for n,h in NAV)
    ld = ""
    if article:
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":%s,"description":%s,"datePublished":"%s","author":{"@type":"Person","name":"Naddy"},"publisher":{"@type":"Organization","name":"Naddys Studio","logo":{"@type":"ImageObject","url":"%s/logo.png"}},"mainEntityOfPage":"%s","image":"%s/og.png"}</script>'
              % (jsq(title), jsq(desc), article, SITE, url, SITE))
    out = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0b0b0c">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:site_name" content="Naddys Studio">
<meta property="og:title" content="{html.escape(og_title or title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<!-- GOOGLE_SITE_VERIFICATION -->
{ld}{extra_head}
<style>{CSS}</style></head><body><div class="wrap">
<nav><a class="brand" href="/"><img class="i" src="/logo-icon.png" alt=""><img class="n" src="/logo-name.png" alt="Naddys Studio"></a><div class="links">{nav}</div></nav>
<main>
{body}
</main>
<footer>
<p>As an Amazon Associate I earn from qualifying purchases.</p>
<p>Not medical advice. Check with your doctor before starting any supplement or new exercise plan.</p>
<p><a href="{IG}">Instagram</a> &middot; <a href="{YT}">YouTube</a></p>
<p><a href="/about/">About</a> &middot; <a href="/disclosure/">Disclosure</a> &middot; <a href="/privacy/">Privacy</a> &middot; <a href="/contact/">Contact</a></p>
</footer></div></body></html>"""
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)

def jsq(s):
    import json; return json.dumps(s)

ARTICLES = []

def article(slug, title, desc, date, body, tagline):
    path = f"/articles/{slug}/"
    ARTICLES.append((slug, title, tagline, date))
    inner = f"""<p class="tag" style="margin-top:28px">Article</p><h1 style="margin-top:6px">{html.escape(title)}</h1>
<p class="meta">By Naddy &middot; {date_h(date)}</p>
<div class="box"><b class="t">Quick note</b>This is general information from my own research and experience, not medical advice. Talk to your doctor before starting a new supplement, especially if you have a health condition or take medicines.</div>
{body}
<div class="box"><b class="t">Disclosure</b>Some links on this page go to Amazon. As an Amazon Associate I earn from qualifying purchases, at no extra cost to you. I only list products I would take myself. <a href="/disclosure/">More here</a>.</div>
<p><a class="btn o" href="/articles/">More articles</a> <a class="btn" href="/shop/">See my picks</a></p>"""
    page(path, title + " | Naddys Studio", desc, inner, active="Articles", article=date)

def date_h(d):
    import datetime; return datetime.date.fromisoformat(d).strftime("%-d %B %Y")

# ---------- ARTICLE 1 ----------
article("magnesium-for-sleep-and-recovery",
 "Magnesium for Sleep and Recovery: What It Does and How to Choose One",
 "A plain-English look at magnesium for sleep and muscle recovery: what the research suggests, which forms exist, and how to pick a supplement without wasting money.",
 "2026-11-22", """
<p class="lead">If you train hard, sit at a desk all day and still wake up feeling flat, magnesium is one of the cheapest things worth understanding. Here is what it actually does, what the research does and does not say, and how I choose one.</p>
<h2>What magnesium does in your body</h2>
<p>Magnesium is a mineral involved in hundreds of reactions in the body. That includes how muscles contract and relax, how nerves signal, and how your body makes energy. Hard training, sweat and a rushed diet can leave you on the lower side, and a lot of people simply do not eat much of it.</p>
<h2>Magnesium and sleep: what the research suggests</h2>
<p>Some small studies, mostly in older adults or people with low intake, found that magnesium supplements helped people fall asleep a bit faster or sleep slightly better. The results are mixed and the effect is modest. It is not a sleeping pill and it will not fix a bad routine. Think of it as one small helper, not a cure.</p>
<h2>Magnesium and recovery</h2>
<p>Because magnesium is part of normal muscle function, getting enough supports recovery and helps with occasional cramps in people who were short on it. If your intake is already fine, extra may not do much. That is why I look at food first.</p>
<h2>Food first</h2>
<p>Pumpkin seeds, almonds, cashews, spinach, beans and whole grains are good sources. If your plate rarely has any of these, start there. A supplement fills a gap, it does not replace a decent diet.</p>
<h2>Which form should you pick?</h2>
<ul>
<li><b>Magnesium glycinate (bisglycinate):</b> gentle on the stomach, the form most people choose for evening use. This is what I take.</li>
<li><b>Magnesium citrate:</b> well absorbed, but can loosen the stomach in some people.</li>
<li><b>Magnesium oxide:</b> cheap and common, but poorly absorbed and the most likely to upset the stomach.</li>
</ul>
<h2>How I choose and take it</h2>
<ul>
<li>Check the label for the actual elemental magnesium per serving, not just the big number on the front.</li>
<li>Pick a brand that shows clear ingredients and lab testing. Fake and diluted supplements are a real problem online, so I buy only from the brand's official store on Amazon.</li>
<li>Start with the dose on the label and take it in the evening, with or after food.</li>
<li>Give it two to three weeks before judging. If your stomach complains, lower the dose or try another form.</li>
</ul>
<h2>Who should check with a doctor first</h2>
<p>If you have kidney problems, a heart condition, or you take regular medicines (including some antibiotics and blood pressure tablets), ask your doctor before starting magnesium. Too much can cause loose stools and other problems.</p>
<div class="box" id="my-pick"><b class="t">The one I use</b>I take a magnesium bisglycinate supplement in the evening. You can see it with my other picks on the shop page: <a href="/shop/#magnesium">my magnesium pick</a>.</div>
<h2>The short version</h2>
<p>Eat magnesium-rich food first. If you still want a supplement, choose a gentle form like glycinate, check the label, give it a few weeks, and keep your expectations realistic. Good sleep still comes from the basics: a regular bedtime, a dark room, and no phone in your face.</p>
""", "What it does for sleep and recovery, which form to pick, and what the research really says.")

# ---------- ARTICLE 2 ----------
article("how-to-choose-a-whey-protein",
 "How to Choose a Whey Protein (Without Getting Fooled)",
 "Whey concentrate, isolate or blend? A simple guide to reading a whey protein label, spotting weak products and choosing one that suits your stomach and budget.",
 "2026-11-26", """
<p class="lead">Walk into any supplement aisle and every tub claims to be the best. Most of the difference comes down to four things on the label. Here is how I check them.</p>
<h2>First: do you even need whey?</h2>
<p>Whey is just a convenient protein source. If your meals already hit your protein target, you do not need it. It earns its place when food falls short, like busy workdays or after training.</p>
<h2>Concentrate vs isolate vs blend</h2>
<ul>
<li><b>Concentrate:</b> the most common and usually cheapest. It has a little more lactose and fat, so it can bother sensitive stomachs.</li>
<li><b>Isolate:</b> filtered further, so it is lower in lactose and often lighter on the stomach. Costs more per tub.</li>
<li><b>Blend:</b> a mix. Check the order of ingredients: whey protein should come first.</li>
</ul>
<h2>The four label checks</h2>
<h3>1. Protein per scoop</h3>
<p>Divide the grams of protein by the scoop size. Around 24 to 27 g protein in a 30 to 33 g scoop is a healthy range. Much lower means more filler.</p>
<h3>2. The ingredient list</h3>
<p>Whey protein should be the first ingredient. Be careful with long lists of thickeners, sweeteners and "proprietary blends" that hide what is actually inside.</p>
<h3>3. Third-party testing</h3>
<p>Look for lab test reports or authenticity details on the brand's page. Reports are the simplest way to see that the protein number on the tub is real.</p>
<h3>4. Real seller, real batch</h3>
<p>Fake tubs are a genuine problem online. Buy from the brand's official store or a seller Amazon itself lists as authorised, check the seal and the batch and expiry details when it arrives.</p>
<h2>Price per gram of protein</h2>
<p>The cheapest tub is not always the cheapest protein. Divide the price by total grams of protein in the tub. That one number makes brands easy to compare.</p>
<h2>If whey upsets your stomach</h2>
<p>Try an isolate, mix with water instead of milk, and start with a half scoop. If it still bothers you, a lactose-free option or food protein is fine too.</p>
<div class="box"><b class="t">What I use</b>I have listed the whey options I trust, with a short note on why, on my shop page: <a href="/shop/">see my protein picks</a>.</div>
<h2>The short version</h2>
<p>Pick a whey where protein is first on the label, the protein per scoop is solid, the brand shows testing, and you buy from a real seller. Match isolate or concentrate to your stomach and budget, then stop overthinking it and train.</p>
""", "Concentrate, isolate or blend? Four label checks that matter, and how to avoid fake tubs.")

# ---------- ARTICLES INDEX ----------
cards = "".join(f'<a class="c" href="/articles/{s}/"><span class="tag">{date_h(d)}</span><b>{html.escape(t)}</b><span>{html.escape(g)}</span></a>' for s,t,g,d in ARTICLES)
page("/articles/", "Fitness Articles | Naddys Studio",
 "Simple, research-backed fitness articles on supplements, nutrition and training. New articles every week.",
 f'<h1>Articles</h1><p class="lead">Simple, science-backed fitness. New articles every week.</p><div class="cards">{cards}</div>', active="Articles")

# ---------- HOME ----------
cards_home = "".join(f'<a class="c" href="/articles/{s}/"><b>{html.escape(t)}</b><span>{html.escape(g)}</span></a>' for s,t,g,d in ARTICLES)
page("/", "Naddys Studio | Science-backed fitness, made simple",
 "Science-backed fitness, made simple. Articles on training, nutrition and supplements, plus the products I actually use.",
 f"""<div class="hero"><img src="/logo-icon.png" alt="Naddys Studio"></div>
<h1 style="text-align:center">Science-backed fitness, made simple</h1>
<p class="lead" style="text-align:center">I am a corporate employee by day and a fitness addict for life. I lost 20 kg in 6 months and got a six-pack twice. Here I share what actually worked, in plain words.</p>
<p style="text-align:center"><a class="btn" href="/articles/">Read the articles</a> <a class="btn o" href="/shop/">See my picks</a></p>
<h2>Latest articles</h2><div class="cards">{cards_home}</div>
<h2>What I am building</h2>
<p>My goal is a place where anyone with a busy job can find honest, simple fitness advice that is backed by research, with no hype and no fake promises. Weekly articles, short videos on <a href="{IG}">Instagram</a> and <a href="{YT}">YouTube</a>, and a short list of products I trust.</p>
<div class="box"><b class="t">Why trust this site</b>I test every product on my own body first. I only recommend brands I have checked for credibility and screened for fakes, and only what I am willing to take myself.</div>
<script>if(location.hash){{location.replace("/shop/"+location.hash)}}</script>""", active="Home")

# ---------- ABOUT ----------
page("/about/", "About Naddy | Naddys Studio",
 "Corporate by day, fitness addict for life. How I lost 20 kg in 6 months and why I share simple, science-backed fitness.",
 f"""<h1>About me</h1>
<p class="lead">Hi, I am Naddy. Corporate by day, fitness addict for life.</p>
<p>I lost 20 kg in 6 months and have built a six-pack twice. Doing it with a full-time desk job taught me that most fitness advice is either too complicated or too good to be true.</p>
<h2>What this site is</h2>
<p>A simple place for fitness information I would give a friend: what the research says, what I do myself, and the few products I trust. I share short videos on <a href="{IG}">Instagram</a> and <a href="{YT}">YouTube</a>, and the longer versions here.</p>
<h2>How I choose products</h2>
<p>I test every product on my own body first. I check the brand, look for fakes, and recommend only what I am willing to take myself. Some links go to Amazon and I earn a small commission if you buy, at no extra cost to you. <a href="/disclosure/">Read the full disclosure</a>.</p>
<h2>Where to find me</h2>
<p><a href="{IG}">Instagram @naddys_studio</a><br><a href="{YT}">YouTube @Naddys_Studio</a><br><a href="/contact/">Contact</a></p>""", active="About")

# ---------- LEGAL ----------
page("/disclosure/", "Disclosure | Naddys Studio", "How this site earns money and how I choose what to recommend.",
 """<h1>Disclosure</h1>
<p>As an Amazon Associate I earn from qualifying purchases.</p>
<p>Some links on this site go to Amazon. If you buy through them, I may earn a small commission at no extra cost to you. This helps keep the site and my content going.</p>
<p>It never changes what I recommend. I only list products I am willing to use myself, and I say so when I have concerns.</p>
<p>The information here is general and is not medical advice. Check with your doctor before starting any supplement or new exercise plan.</p>""")
page("/privacy/", "Privacy | Naddys Studio", "What data this site collects and how it is used.",
 """<h1>Privacy</h1>
<p>This site does not ask you to create an account and does not collect your name or email.</p>
<p>It may use basic, privacy-friendly traffic counts (page views, not personal profiles) to see which articles are useful. When you click a link to Amazon, Amazon's own policies apply on their site and they may use cookies to credit the referral.</p>
<p>If you message me through Instagram or email, I use your message only to reply to you.</p>""")
page("/contact/", "Contact | Naddys Studio", "How to reach Naddys Studio.",
 f"""<h1>Contact</h1>
<p>The best way to reach me is a direct message on <a href="{IG}">Instagram @naddys_studio</a>. You can also leave a comment on my <a href="{YT}">YouTube</a> videos.</p>
<p>I read everything and reply when I can.</p>""")

# ---------- SHOP (from old index) ----------
old = open(os.path.join(ROOT, "tools", "shop_template.html")).read()
os.makedirs(os.path.join(ROOT, "shop"), exist_ok=True)
open(os.path.join(ROOT, "shop", "index.html"), "w").write(old)

# ---------- sitemap / robots ----------
urls = ["/", "/articles/", "/shop/", "/about/", "/disclosure/", "/privacy/", "/contact/"] + [f"/articles/{s}/" for s,_,_,_ in ARTICLES]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(urls), "urls")
