from flask import Flask
import json
import os

app = Flask(__name__)

CLOUD = "djk42jm3p"
BASE  = f"https://res.cloudinary.com/{CLOUD}/image/upload"

CLOUDINARY_HERO = f"{BASE}/hero.png"
CLOUDINARY_LOGO = f"{BASE}/logo.png?v=2"

def load_properties():
   path = os.path.join(os.path.dirname(__file__), "properties.json")
   with open(path, encoding="utf-8") as f:
       return json.load(f)

def img_url(img):
   if img.startswith("http"):
       return img
   # נתיב יחסי → Cloudinary
   return f"{BASE}/static/{img}"

@app.route("/")
def home():
   properties = load_properties()

   cards = ""
   for idx, p in enumerate(properties):
       images = p.get("images", ["hero"])
       full_images = [img_url(img) for img in images]
       images_json = json.dumps(full_images)
       slides = ""
       dots = ""
       for i, img in enumerate(full_images):
           active = "active" if i == 0 else ""
           slides += f'<div class="slide {active}"><img src="{img}" alt="תמונה {i+1}" data-images=\'{images_json}\' data-index="{i}"></div>'
           dots += f'<button class="dot {active}" onclick="goTo({idx},{i})" aria-label="תמונה {i+1}"></button>'

       arrows = ""
       if len(images) > 1:
           arrows = f"""
           <button class="arrow arrow-r" onclick="move({idx},-1)">&#8250;</button>
           <button class="arrow arrow-l" onclick="move({idx}, 1)">&#8249;</button>
           """

       cards += f"""
       <div class="card" data-rooms="{p['rooms']}">
           <div class="carousel" id="carousel-{idx}">
               {slides}
               {arrows}
               <div class="dots">{dots}</div>
           </div>
           <div class="card-content">
               <h3>{p['title']}</h3>
               <p>{p['rooms']} חדרים | {p['sqm']} מ״ר | {p.get('outdoor_type','מרפסת')} {p['balcony']} מ״ר</p>
               <div class="price">₪ {p['price']}</div>
               <a href="https://wa.me/972505959053" target="_blank">לפרטים בווצאפ</a>
           </div>
       </div>
       """

   return f"""
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARI נדל״ן ויזמות</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800;900&display=swap');

*, *::before, *::after {{
   box-sizing: border-box;
   margin: 0;
   padding: 0;
}}

body {{
   font-family: 'Heebo', Arial, sans-serif;
   background: #f7f3ea;
}}

.hero {{
   background:
       linear-gradient(rgba(4,35,27,.78), rgba(4,35,27,.88)),
       url('{CLOUDINARY_HERO}') center/cover no-repeat;
   color: white;
   text-align: center;
   border-bottom: 3px solid #b89445;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   padding: 36px 24px 32px;
   gap: 0;
}}

.logo-wrap {{
   width: 620px;
   max-width: 78vw;
   overflow: visible;
   line-height: 0;
   margin-bottom: 8px;
   background: transparent;
}}

.logo-wrap img {{
   width: 100%;
   display: block;
   mix-blend-mode: screen;
   filter: brightness(1.4) contrast(1.1);
   background: transparent;
}}

.line {{
   width: 260px;
   max-width: 60vw;
   height: 1px;
   background: #b89445;
   margin-bottom: 14px;
}}

h1 {{
   font-size: 46px;
   line-height: 1.2;
   font-weight: 900;
   text-shadow: 0 3px 10px rgba(0,0,0,.5);
   margin-bottom: 8px;
}}

h1 span {{
   display: block;
   color: #c9a24b;
}}

.subtitle {{
   font-size: 18px;
   font-weight: 600;
   opacity: 0.85;
   margin-bottom: 20px;
}}

.features {{
   width: 100%;
   max-width: 680px;
   display: grid;
   grid-template-columns: repeat(3, 1fr);
   border: 1px solid rgba(184,148,69,.4);
   border-radius: 9px;
   overflow: hidden;
   background: rgba(0,0,0,.3);
   backdrop-filter: blur(6px);
}}

.feature {{
   padding: 12px 10px;
   text-align: center;
   border-left: 1px solid rgba(184,148,69,.3);
}}

.feature:last-child {{ border-left: none; }}

.feature .icon {{
   font-size: 24px;
   color: #c9a24b;
   line-height: 1;
   margin-bottom: 4px;
}}

.feature strong {{
   display: block;
   font-size: 13px;
   font-weight: 800;
   margin-bottom: 1px;
}}

.feature span {{
   font-size: 11px;
   opacity: 0.78;
}}

.section-title {{
   text-align: center;
   padding: 32px 0 4px;
   font-size: 22px;
   font-weight: 900;
   color: #073d2c;
}}

.section-line {{
   width: 60px;
   height: 2px;
   background: #b89445;
   margin: 8px auto 0;
}}

.grid {{
   padding: 24px 4vw 60px;
   display: grid;
   grid-template-columns: repeat(3, 1fr);
   gap: 22px;
   max-width: 1200px;
   margin: 0 auto;
}}

.card {{
   background: white;
   border-radius: 12px;
   overflow: hidden;
   box-shadow: 0 5px 18px rgba(0,0,0,.10);
   transition: transform .2s, box-shadow .2s;
}}

.card:hover {{
   transform: translateY(-4px);
   box-shadow: 0 12px 28px rgba(0,0,0,.16);
}}

.carousel {{
   position: relative;
   overflow: hidden;
}}

.slide {{
   display: none;
   width: 100%;
}}

.slide.active {{ display: block; }}

.slide img {{
   width: 100%;
   height: 260px;
   display: block;
   object-fit: cover;
   cursor: zoom-in;
}}

.arrow {{
   position: absolute;
   top: 50%;
   transform: translateY(-50%);
   background: rgba(0,0,0,.45);
   color: white;
   border: none;
   width: 28px;
   height: 28px;
   border-radius: 50%;
   font-size: 18px;
   cursor: pointer;
   display: flex;
   align-items: center;
   justify-content: center;
   z-index: 2;
   transition: background .15s;
}}

.arrow:hover {{ background: rgba(184,148,69,.8); }}
.arrow-r {{ right: 8px; }}
.arrow-l {{ left: 8px; }}

.dots {{
   position: absolute;
   bottom: 6px;
   left: 50%;
   transform: translateX(-50%);
   display: flex;
   gap: 5px;
   z-index: 2;
}}

.dot {{
   width: 7px;
   height: 7px;
   border-radius: 50%;
   background: rgba(255,255,255,.5);
   border: none;
   cursor: pointer;
   padding: 0;
   transition: background .15s;
}}

.dot.active {{ background: #c9a24b; }}

.card-content {{
   text-align: center;
   padding: 14px 12px;
}}

.card h3 {{
   font-size: 17px;
   font-weight: 900;
   margin-bottom: 5px;
}}

.card p {{
   font-size: 12px;
   color: #555;
   line-height: 1.5;
}}

.price {{
   margin: 9px 0 11px;
   font-size: 20px;
   font-weight: 900;
   color: #b77d17;
}}

.card a {{
   display: block;
   border: 1.5px solid #b89445;
   border-radius: 7px;
   padding: 7px;
   color: #073d2c;
   text-decoration: none;
   font-weight: 800;
   font-size: 13px;
   transition: background .15s, color .15s;
}}

.card a:hover {{
   background: #b89445;
   color: white;
}}

.lightbox {{
   display: none;
   position: fixed;
   inset: 0;
   background: rgba(0,0,0,.92);
   z-index: 1000;
   align-items: center;
   justify-content: center;
}}

.lightbox.open {{
   display: flex;
}}

.lightbox img {{
   max-width: 90vw;
   max-height: 88vh;
   object-fit: contain;
   border-radius: 6px;
   user-select: none;
}}

.lb-close {{
   position: fixed;
   top: 18px;
   left: 22px;
   color: white;
   font-size: 36px;
   cursor: pointer;
   line-height: 1;
   z-index: 1001;
   background: none;
   border: none;
   opacity: 0.85;
   transition: opacity .15s;
}}

.lb-close:hover {{ opacity: 1; }}

.lb-counter {{
   position: fixed;
   bottom: 20px;
   left: 50%;
   transform: translateX(-50%);
   color: rgba(255,255,255,.7);
   font-size: 14px;
   font-family: 'Heebo', sans-serif;
}}

.lb-arrow {{
   position: fixed;
   top: 50%;
   transform: translateY(-50%);
   background: rgba(255,255,255,.15);
   color: white;
   border: none;
   width: 48px;
   height: 48px;
   border-radius: 50%;
   font-size: 28px;
   cursor: pointer;
   display: flex;
   align-items: center;
   justify-content: center;
   z-index: 1001;
   transition: background .15s;
}}

.lb-arrow:hover {{ background: rgba(184,148,69,.7); }}
.lb-arrow-r {{ right: 20px; }}
.lb-arrow-l {{ left: 20px; }}

.filter-bar {{
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 10px;
   padding: 20px 0 10px;
}}

.filter-label {{
   font-size: 13px;
   font-weight: 700;
   color: #888;
   font-family: 'Heebo', sans-serif;
   letter-spacing: 1px;
}}

.filter-pills {{
   display: flex;
   gap: 0;
   border: 2px solid #b89445;
   border-radius: 30px;
   overflow: hidden;
   background: white;
   box-shadow: 0 2px 8px rgba(0,0,0,.07);
}}

.filter-btn {{
   background: white;
   border: none;
   border-left: 1.5px solid #b89445;
   padding: 12px 28px;
   font-size: 17px;
   font-weight: 800;
   color: #073d2c;
   cursor: pointer;
   font-family: 'Heebo', sans-serif;
   transition: background .15s, color .15s;
   min-width: 64px;
}}

.filter-btn:last-child {{ border-left: none; }}

.filter-btn:hover {{
   background: #f7f0de;
}}

.filter-btn.active {{
   background: #b89445;
   color: white;
}}

@media (max-width: 900px) {{
   .grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

@media (max-width: 600px) {{
   .hero {{ padding: 28px 16px 26px; }}
   .logo-wrap {{ width: 90vw; }}
   h1 {{ font-size: 32px; }}
   .subtitle {{ font-size: 15px; }}

   .features {{
       grid-template-columns: 1fr;
       max-width: 300px;
   }}
   .feature {{ border-left: none; border-bottom: 1px solid rgba(184,148,69,.3); }}
   .feature:last-child {{ border-bottom: none; }}

   .section-title {{ font-size: 18px; padding-top: 24px; }}

   .grid {{
       grid-template-columns: 1fr;
       padding: 18px 14px 40px;
       gap: 18px;
   }}

   .slide img {{ height: 220px; }}

   .lb-arrow {{ width: 38px; height: 38px; font-size: 22px; }}
   .lb-arrow-r {{ right: 8px; }}
   .lb-arrow-l {{ left: 8px; }}
}}
</style>
</head>
<body>

<section class="hero">
   <div class="logo-wrap">
       <img src="{CLOUDINARY_LOGO}" alt="ARI נדלן">
   </div>
   <div class="line"></div>
   <h1>
       כל הדירות למכירה
       <span>במורשת במקום אחד</span>
   </h1>
   <div class="subtitle">נכסים זמינים למכירה מתעדכנים בזמן אמת</div>
   <div class="features">
       <div class="feature">
           <div class="icon">🔑</div>
           <strong>זמינים עבורך</strong>
           <span>עד שלב קבלת המפתח</span>
       </div>
       <div class="feature">
           <div class="icon">⭐</div>
           <strong>נכסים בלעדיים</strong>
           <span>במחירים אטרקטיביים</span>
       </div>
       <div class="feature">
           <div class="icon">📍</div>
           <strong>בשכונה המבוקשת ביותר</strong>
           <span>במודיעין</span>
       </div>
   </div>
</section>

<div class="section-title">נכסים זמינים</div>
<div class="section-line"></div>

<div class="filter-bar">
   <span class="filter-label">חדרים</span>
   <div class="filter-pills">
       <button class="filter-btn active" data-rooms="all">הכל</button>
       <button class="filter-btn" data-rooms="3">3</button>
       <button class="filter-btn" data-rooms="4">4</button>
       <button class="filter-btn" data-rooms="5">5</button>
       <button class="filter-btn" data-rooms="6">6</button>
   </div>
</div>

<section class="grid">
   {cards}
</section>

<div class="lightbox" id="lightbox">
   <button class="lb-close" id="lb-close">✕</button>
   <button class="lb-arrow lb-arrow-r" id="lb-prev">&#8250;</button>
   <img id="lb-img" src="" alt="">
   <button class="lb-arrow lb-arrow-l" id="lb-next">&#8249;</button>
   <div class="lb-counter" id="lb-counter"></div>
</div>

<script>
const carousels = {{}};
let lbImages = [];
let lbIndex = 0;

function init() {{
   document.querySelectorAll('.carousel').forEach(c => {{
       const id = c.id.replace('carousel-','');
       carousels[id] = 0;
   }});

   document.querySelectorAll('.slide img').forEach(img => {{
       img.addEventListener('click', function(e) {{
           e.stopPropagation();
           const images = JSON.parse(this.dataset.images);
           const idx = parseInt(this.dataset.index);
           openLightbox(images, idx);
       }});
   }});

   document.getElementById('lb-close').addEventListener('click', closeLightbox);
   document.getElementById('lb-prev').addEventListener('click', function(e) {{ e.stopPropagation(); lbMove(-1); }});
   document.getElementById('lb-next').addEventListener('click', function(e) {{ e.stopPropagation(); lbMove(1); }});
   document.getElementById('lightbox').addEventListener('click', function(e) {{
       if (e.target === this) closeLightbox();
   }});
}}

function goTo(id, idx) {{
   const c = document.getElementById('carousel-' + id);
   const slides = c.querySelectorAll('.slide');
   const dots = c.querySelectorAll('.dot');
   slides[carousels[id]].classList.remove('active');
   dots[carousels[id]].classList.remove('active');
   carousels[id] = idx;
   slides[idx].classList.add('active');
   dots[idx].classList.add('active');
}}

function move(id, dir) {{
   const c = document.getElementById('carousel-' + id);
   const total = c.querySelectorAll('.slide').length;
   let next = (carousels[id] - dir + total) % total;
   goTo(id, next);
}}

function openLightbox(images, idx) {{
   lbImages = images;
   lbIndex = idx;
   updateLightbox();
   document.getElementById('lightbox').classList.add('open');
   document.body.style.overflow = 'hidden';
}}

function updateLightbox() {{
   document.getElementById('lb-img').src = lbImages[lbIndex];
   document.getElementById('lb-counter').textContent = (lbIndex + 1) + ' / ' + lbImages.length;
}}

function lbMove(dir) {{
   lbIndex = (lbIndex - dir + lbImages.length) % lbImages.length;
   updateLightbox();
}}

function closeLightbox() {{
   document.getElementById('lightbox').classList.remove('open');
   document.body.style.overflow = '';
}}

function filterRooms(rooms) {{
   document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
   document.querySelectorAll('.card').forEach(card => {{
       if (rooms === 'all' || card.dataset.rooms === rooms) {{
           card.style.display = '';
       }} else {{
           card.style.display = 'none';
       }}
   }});
}}

document.querySelectorAll('.filter-btn').forEach(btn => {{
   btn.addEventListener('click', function() {{
       document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
       this.classList.add('active');
       filterRooms(this.dataset.rooms);
   }});
}});

document.addEventListener('keydown', e => {{
   if (!document.getElementById('lightbox').classList.contains('open')) return;
   if (e.key === 'Escape') closeLightbox();
   if (e.key === 'ArrowRight') lbMove(-1);
   if (e.key === 'ArrowLeft') lbMove(1);
}});

init();
</script>
</body>
</html>
"""

if __name__ == "__main__":
   app.run(debug=True)