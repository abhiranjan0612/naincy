import streamlit as st
import time
import base64
import io
from pathlib import Path

try:
    from PIL import Image as _PILImage  # type: ignore[import-untyped]
except ImportError:
    _PILImage = None  # type: ignore[assignment]

APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"

st.set_page_config(
    page_title="Happy Birthday Naincy 🎀",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "gift_opened" not in st.session_state:
    st.session_state.gift_opened = False
if "candles_blown" not in st.session_state:
    st.session_state.candles_blown = False
if "cake_cut" not in st.session_state:
    st.session_state.cake_cut = False


def embed_audio(file_path: str):
    try:
        p = APP_DIR / file_path
        with open(p, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(
                f'<audio autoplay loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
                unsafe_allow_html=True,
            )
    except Exception:
        pass


def render_step_indicator():
    if not st.session_state.gift_opened:
        step = 1
    elif not st.session_state.candles_blown:
        step = 2
    elif not st.session_state.cake_cut:
        step = 3
    else:
        step = 4
    labels = ("Surprise", "Candles", "Cake", "Love")
    dots = []
    for i in range(1, 5):
        if i < step:
            cls = "step-dot done"
        elif i == step:
            cls = "step-dot active"
        else:
            cls = "step-dot"
        dots.append(f'<span class="{cls}" aria-hidden="true"></span>')
    st.markdown(
        f"""
<div class="step-rail-wrap" role="navigation" aria-label="Birthday surprise steps">
    <div class="step-rail">{"".join(dots)}</div>
    <div class="step-rail-label">Step {step} of 4 · {labels[step - 1]}</div>
</div>
""",
        unsafe_allow_html=True,
    )




def _img_to_b64(path: Path, max_px: int = 1000) -> str:
    """Resize to max_px on the longest side and return a base64 JPEG string."""
    if _PILImage is not None:
        try:
            with _PILImage.open(path) as img:
                img = img.convert("RGB")
                w, h = img.size
                scale = min(max_px / w, max_px / h, 1.0)
                if scale < 1.0:
                    img = img.resize((int(w * scale), int(h * scale)), _PILImage.LANCZOS)
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                return base64.b64encode(buf.getvalue()).decode()
        except Exception:
            pass
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def show_photo_gallery_naincy():
    st.markdown(
        '<div class="gallery-kicker">Our favourite frames with you ✨</div>',
        unsafe_allow_html=True,
    )

    photos = [
        ("20250519_231337-COLLAGE.jpg",   "Memories 💖"),
        ("IMG_20260102_020527.jpg",        "Radiating ✨"),
        ("IMG-20250413-WA0566.jpg",        "That smile 🌸"),
        ("IMG-20260412-WA0011.jpg",        "Pure vibes 💫"),
        ("IMG-20260412-WA0025.jpg",        "Forever favourite 🎀"),
        ("IMG20250315175740.jpg",          "Content queen 👑"),
        ("IMG20250503092700.jpg",          "A whole moment 🌟"),
        (
            "Screenshot_2025-05-19-14-17-25-81_1c337646f29875672b5a61192b9010f9.jpg",
            "Screenshots 📱",
        ),
    ]

    cards = []
    for fname, caption in photos:
        path = ASSETS_DIR / fname
        if not path.is_file():
            continue
        b64 = _img_to_b64(path)
        cards.append(
            f'<div class="m-item">'
            f'<img src="data:image/jpeg;base64,{b64}" alt="{caption}" loading="lazy">'
            f'<div class="m-cap">{caption}</div>'
            f'</div>'
        )

    gallery_html = f"""
<style>
.m-grid {{
    columns: 3 160px;
    column-gap: 10px;
    margin: 4px 0 28px 0;
}}
.m-item {{
    break-inside: avoid;
    margin-bottom: 10px;
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 24px rgba(0,0,0,0.45), 0 0 0 1px rgba(236,72,153,0.12);
    background: #100020;
}}
.m-item img {{
    width: 100%;
    height: auto;
    display: block;
}}
.m-cap {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(10,0,20,0.82) 0%, transparent 100%);
    color: #f0abfc;
    font-family: 'Poppins', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.09em;
    padding: 22px 10px 8px;
    text-align: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}}
.m-item:hover .m-cap {{ opacity: 1; }}
@media (max-width: 520px) {{
    .m-grid {{ columns: 2 130px; column-gap: 7px; }}
    .m-item {{ margin-bottom: 7px; }}
}}
</style>
<div class="m-grid">{"".join(cards)}</div>
"""
    st.markdown(gallery_html, unsafe_allow_html=True)


def show_fireworks():
    fireworks_html = """
<style>
.pyro { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
.pyro > .before, .pyro > .after {
    position:absolute; width:5px; height:5px; border-radius:50%;
    box-shadow: 0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff,
                0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff,0 0 #fff;
    animation: 1s bang ease-out infinite backwards,
               1s gravity ease-in infinite backwards,
               5s position linear infinite backwards;
}
.pyro > .after { animation-delay:1.25s,1.25s,1.25s; animation-duration:1.25s,1.25s,6.25s; }
@keyframes bang {
    to { box-shadow:-120px -30px #ff6eb4,80px -180px #c084fc,30px -80px #67e8f9,
                    -50px -120px #fde68a,-90px -80px #f9a8d4,60px -100px #a78bfa,
                    -110px -110px #fb7185,20px -160px #d8b4fe,100px -70px #fcd34d,
                    -80px -30px #ec4899; }
}
@keyframes gravity { to { transform:translateY(150px); opacity:0; } }
@keyframes position {
    0%,19.9%  { margin-top:10%; margin-left:40%; }
    20%,39.9% { margin-top:40%; margin-left:30%; }
    40%,59.9% { margin-top:20%; margin-left:70%; }
    60%,79.9% { margin-top:30%; margin-left:20%; }
    80%,99.9% { margin-top:30%; margin-left:80%; }
}
</style>
<div class="pyro"><div class="before"></div><div class="after"></div></div>
<script>setTimeout(function(){const p=document.querySelector('.pyro');if(p)p.remove();},4000);</script>
"""
    st.components.v1.html(fireworks_html, height=400, scrolling=False)


# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Poppins:wght@300;400;500;600&display=swap');

html { -webkit-text-size-adjust:100%; }

.stApp {
    overflow-x: hidden;
    background: radial-gradient(ellipse 160% 55% at 50% -5%, #3b0764 0%, #1a0030 38%, #050008 100%);
}
.main {
    background: radial-gradient(ellipse 160% 55% at 50% -5%, #3b0764 0%, #1a0030 38%, #050008 100%);
}
.main .block-container {
    padding-top: max(1.25rem, env(safe-area-inset-top)) !important;
    padding-left: max(0.75rem, env(safe-area-inset-left)) !important;
    padding-right: max(0.75rem, env(safe-area-inset-right)) !important;
    padding-bottom: 1rem !important;
    max-width: min(100vw, 1400px) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
}
@media (min-width: 640px) {
    .main .block-container {
        padding-left: max(1.5rem, env(safe-area-inset-left)) !important;
        padding-right: max(1.5rem, env(safe-area-inset-right)) !important;
    }
}
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.75rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        flex: 1 1 auto !important;
    }
}

#MainMenu { visibility:hidden; }
footer    { visibility:hidden; }
header    { visibility:hidden; }

/* ── Title ── */
.title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 7vw, 4.4rem);
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #ff6eb4 0%, #ff91c1 28%, #e879f9 58%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 28px rgba(236,72,153,0.45));
    margin: 0 0 12px 0;
    letter-spacing: 0.02em;
    line-height: 1.15;
}
.subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: clamp(10px, 2.5vw, 12px);
    text-align: center;
    color: #f0abfc;
    margin: 0 auto 20px auto;
    max-width: 28rem;
    font-weight: 400;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    line-height: 1.5;
    padding: 0 4px;
}
@media (max-width:480px) { .subtitle { letter-spacing:0.14em; max-width:100%; } }

/* ── Step rail ── */
.step-rail-wrap {
    display:flex; flex-direction:column; align-items:center;
    gap:10px; margin:0 auto 28px auto; max-width:100%; padding:0 4px;
}
.step-rail {
    display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:10px;
}
.step-dot {
    width:10px; height:10px; border-radius:50%;
    background:rgba(192,132,252,0.3);
    box-shadow:0 0 0 2px rgba(15,0,30,0.6);
    flex-shrink:0;
}
.step-dot.active {
    width:14px; height:14px;
    background:linear-gradient(135deg,#ec4899,#a855f7);
    box-shadow:0 0 0 2px rgba(236,72,153,0.5),0 0 18px rgba(236,72,153,0.45);
}
.step-dot.done {
    background:rgba(167,243,208,0.75);
    box-shadow:0 0 0 2px rgba(52,211,153,0.35);
}
.step-rail-label {
    font-family:'Poppins',sans-serif;
    font-size:clamp(11px,3vw,13px);
    color:#d8b4fe; letter-spacing:0.06em; text-align:center;
}

/* ── Big icon ── */
.big-icon {
    font-size:clamp(4.5rem,38vw,12.5rem); text-align:center;
    animation:floatIcon 3s ease-in-out infinite;
    filter:drop-shadow(0 10px 28px rgba(236,72,153,0.4));
    margin:24px 0 16px 0; user-select:none;
}
@keyframes floatIcon {
    0%,100% { transform:translateY(0px); }
    50%     { transform:translateY(-16px); }
}

/* ── Cake ── */
.cake-container {
    text-align:center;
    padding:clamp(12px,4vw,28px) 0;
    margin:clamp(8px,2vw,24px) 0 clamp(8px,2vw,16px) 0;
    min-height:min(52vh,320px);
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}
@media (max-width:480px) { .cake-container { min-height:auto; } }
.cake-emoji {
    font-size:clamp(4.5rem,38vw,12.5rem);
    filter:drop-shadow(0 10px 25px rgba(236,72,153,0.4));
    animation:float 4s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform:translateY(0px); }
    50%     { transform:translateY(-16px); }
}
.candles-wrapper {
    font-size:clamp(2rem,12vw,3.6rem);
    margin-bottom:clamp(-28px,-6vw,-36px);
    transition:all 0.5s ease; animation:flicker 2s infinite; text-align:center;
}
@keyframes flicker {
    0%,100% { opacity:1;    filter:drop-shadow(0 0 10px rgba(255,200,150,1)); }
    50%     { opacity:0.88; filter:drop-shadow(0 0 18px rgba(255,220,200,1)); }
}
.candles-blown { animation:blowOut 0.8s forwards; }
@keyframes blowOut {
    0%   { opacity:1; transform:scale(1); }
    100% { opacity:0; transform:scale(0.5) translateY(-40px); }
}
.knife-icon {
    font-size:clamp(3.5rem,28vw,9.5rem); text-align:center;
    animation:floatKnife 3.5s ease-in-out infinite;
    margin:24px 0 16px 0;
    filter:drop-shadow(0 10px 20px rgba(236,72,153,0.4));
}
@keyframes floatKnife {
    0%,100% { transform:translateY(0px) rotate(0deg); }
    50%     { transform:translateY(-12px) rotate(-5deg); }
}
.knife-cutting { animation:cutCake 0.8s forwards; }
@keyframes cutCake {
    0%   { transform:translateY(0) rotate(0deg); }
    50%  { transform:translateY(-36px) rotate(-40deg); }
    100% { transform:translateY(50px) rotate(-85deg); opacity:0; }
}

/* ── Instruction ── */
.instruction {
    font-family:'Poppins',sans-serif;
    font-size:clamp(15px,3.8vw,17px);
    text-align:center; color:#f0abfc;
    margin:18px auto; font-weight:400;
    letter-spacing:0.02em;
    text-shadow:0 2px 10px rgba(0,0,0,0.6);
    line-height:1.55; max-width:26rem;
}

/* ── Message section ── */
.message-hero {
    font-family:'Playfair Display',serif;
    font-size:clamp(1.8rem,5vw,2.9rem);
    background:linear-gradient(135deg,#ff6eb4 0%,#e879f9 50%,#c084fc 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    text-align:center; margin:12px 0 28px 0; font-weight:700;
    letter-spacing:0.02em;
    filter:drop-shadow(0 4px 22px rgba(236,72,153,0.4));
}

/* ── Individual message cards ── */
.msg-card {
    border-radius:clamp(18px,4vw,26px);
    padding:clamp(20px,4vw,32px) clamp(16px,4vw,28px);
    margin:0 0 20px 0;
    box-sizing:border-box;
    backdrop-filter:blur(20px);
    background:rgba(10,0,20,0.72);
    position:relative;
    overflow:hidden;
}
.msg-card.rose   { box-shadow:0 16px 48px rgba(236,72,153,0.22),  0 0 0 1px rgba(236,72,153,0.2); }
.msg-card.violet { box-shadow:0 16px 48px rgba(168,85,247,0.22),  0 0 0 1px rgba(168,85,247,0.2); }
.msg-card.gold   { box-shadow:0 16px 48px rgba(251,191,36,0.18),  0 0 0 1px rgba(251,191,36,0.18); }
.msg-card.teal   { box-shadow:0 16px 48px rgba(6,182,212,0.18),   0 0 0 1px rgba(6,182,212,0.18); }

.msg-sender { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.msg-avatar { font-size:2rem; line-height:1; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.4)); }
.msg-name {
    font-family:'Poppins',sans-serif;
    font-size:clamp(14px,3.5vw,16px); font-weight:600; letter-spacing:0.03em;
}
.msg-card.rose   .msg-name { color:#ff91c1; }
.msg-card.violet .msg-name { color:#c084fc; }
.msg-card.gold   .msg-name { color:#fcd34d; }
.msg-card.teal   .msg-name { color:#67e8f9; }
.msg-role {
    font-family:'Poppins',sans-serif;
    font-size:clamp(10px,2.5vw,11px); letter-spacing:0.12em;
    text-transform:uppercase; color:rgba(255,255,255,0.42);
}
.msg-body {
    font-family:'Poppins',sans-serif;
    font-size:clamp(14px,3.5vw,16px); line-height:1.88;
    color:#e2e8f0; font-weight:300; word-wrap:break-word;
}

/* ── Celebration row ── */
.celebration { font-size:clamp(28px,9vw,46px); text-align:center; margin:22px 0; }

/* ── Gallery ── */
.gallery-intro {
    font-family:'Playfair Display',serif;
    font-size:clamp(1.1rem,4vw,1.4rem);
    text-align:center; color:#f9a8d4;
    margin:8px 8px 20px 8px; letter-spacing:0.06em;
    line-height:1.35; font-style:italic;
}
.gallery-kicker {
    font-family:'Poppins',sans-serif;
    font-size:clamp(0.62rem,2.2vw,0.7rem); letter-spacing:0.14em;
    text-transform:uppercase; color:rgba(249,168,212,0.88);
    text-align:center; margin:8px 10px 16px 10px; line-height:1.45;
}
@media (min-width:640px) { .gallery-kicker { letter-spacing:0.22em; } }

div[data-testid="stImage"] img {
    border-radius:clamp(10px,2.5vw,16px);
    box-shadow:0 8px 28px rgba(0,0,0,0.45),0 0 0 1px rgba(236,72,153,0.12);
    max-width:100%; height:auto;
}

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,#be185d 0%,#ec4899 45%,#a855f7 100%) !important;
    color:#fff0f8 !important;
    font-family:'Poppins',sans-serif !important;
    font-size:clamp(14px,3.8vw,16px) !important;
    font-weight:600 !important; letter-spacing:0.06em !important;
    padding:16px 44px !important; min-height:48px !important;
    border-radius:999px !important;
    border:1px solid rgba(249,168,212,0.4) !important;
    box-shadow:0 14px 36px rgba(190,24,93,0.4) !important;
    transition:all 0.25s ease !important;
    text-transform:uppercase !important;
    width:100%; box-sizing:border-box;
}
@media (hover:hover) and (pointer:fine) {
    .stButton > button:hover {
        transform:translateY(-2px) scale(1.02) !important;
        box-shadow:0 20px 44px rgba(236,72,153,0.48) !important;
    }
}

div[data-testid="stCaption"] {
    text-align:center !important; color:#c084fc !important;
    font-family:'Poppins',sans-serif !important;
    font-size:clamp(0.72rem,2.8vw,0.8rem) !important;
    line-height:1.45 !important; padding:0 4px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="title">Happy Birthday, Naincy 🎀</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Colleague · Creator · Icon · Family By Choice</div>',
    unsafe_allow_html=True,
)

render_step_indicator()

if st.session_state.gift_opened:
    embed_audio("birthday.mp3")

# ─── Step 1: Gift Box ─────────────────────────────────────────────────────────
if not st.session_state.gift_opened:
    st.markdown('<div class="big-icon">🎁</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="instruction">Tap to unwrap your birthday surprise 🎀</div>',
        unsafe_allow_html=True,
    )
    if st.button("Open the gift", key="open_gift", use_container_width=True):
        st.session_state.gift_opened = True
        st.balloons()
        time.sleep(0.5)
        st.rerun()

# ─── Step 2: Candles ─────────────────────────────────────────────────────────
elif not st.session_state.candles_blown:
    candle_class = "candles-blown" if st.session_state.get("blowing", False) else ""
    st.markdown(
        f"""
<div class="cake-container">
    <div class="candles-wrapper {candle_class}">🕯️ 🕯️ 🕯️</div>
    <div class="cake-emoji">🎂</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="instruction">Make a wish — then blow the candles 🌸</div>',
        unsafe_allow_html=True,
    )
    if st.button("Blow the candles", key="blow_candles", use_container_width=True):
        st.session_state.blowing = True
        time.sleep(0.8)
        st.session_state.candles_blown = True
        st.balloons()
        time.sleep(0.5)
        st.rerun()

# ─── Step 3: Cut Cake ────────────────────────────────────────────────────────
elif not st.session_state.cake_cut:
    knife_class = "knife-cutting" if st.session_state.get("cutting", False) else ""
    st.markdown(
        '<div class="cake-container"><div class="cake-emoji">🎂</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="knife-icon {knife_class}">🔪</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="instruction">Now cut the cake — your messages and memories appear next 💖</div>',
        unsafe_allow_html=True,
    )
    if st.button("Cut the cake", key="cut_cake", use_container_width=True):
        st.session_state.cutting = True
        time.sleep(0.8)
        st.session_state.cake_cut = True
        st.balloons()
        time.sleep(0.5)
        st.rerun()

# ─── Step 4: Messages + Gallery ──────────────────────────────────────────────
else:
    st.markdown(
        '<div class="cake-container"><div class="cake-emoji">🍰</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="celebration">✨ 💖 🎂 🌸 🎀 🎊 ✨</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="message-hero">For You, With All Our Love 💖</div>',
        unsafe_allow_html=True,
    )

    _MESSAGES = [
        {
            "color": "rose",
            "avatar": "👧🏻",
            "name": "Divya",
            "role": "Your Sister From Another Mother",
            "body": (
                "<strong>Happy Birthday, Naincy! ❤️</strong><br><br>"
                "You are truly much more than just a colleague to me — you are like a sister. "
                "For the last 4 years, we've shared not only the same workplace but also endless memories, "
                "laughter, secrets, and all our <em>\"crime partner\"</em> moments that made every day so special. "
                "Thank you for always being there, for understanding me without even saying much, and for making "
                "work life so beautiful and fun.<br><br>"
                "Our bond means a lot to me, and I honestly cherish every moment we've spent together. "
                "May this birthday bring you endless happiness, success, love, and everything your heart desires. "
                "Stay the same amazing, caring, and crazy soul forever. "
                "So lucky to have you in my life! 🎂✨"
            ),
        },
        {
            "color": "violet",
            "avatar": "👦🏻",
            "name": "Ayan Bhaiya",
            "role": "Your Big Brother At Work",
            "body": (
                "Okay so here's the thing — some people you work <em>with</em>, and some people you "
                "actually look forward to seeing at work. You, Naincy, are very much the second type. 😄<br><br>"
                "You've made the office a place worth showing up to, not just because of the work but because "
                "of everything that happens around it — the laughs, the chaos, the <em>\"we'll handle it "
                "later\"</em> energy, all of it. Our crime partner moments are honestly some of the best memories "
                "I'll carry from this place.<br><br>"
                "I've watched you grow so much over these years and I couldn't be prouder. You bring heart and "
                "madness to everything you do in equal measure — and the world needs exactly that. "
                "Happy birthday! Keep being the brilliant, crazy soul you are ❤️"
            ),
        },
        {
            "color": "gold",
            "avatar": "🌟",
            "name": "Abhijot",
            "role": "Your Partner In Crime",
            "body": (
                "Happy birthday, Naincy! ✨<br><br>"
                "Some people come into your life through circumstances — like sharing a workplace — "
                "and end up staying because they're genuinely one of a kind. That's exactly you.<br><br>"
                "You have this rare ability to make every situation better just by being in it. Your energy, "
                "your warmth, your talent for finding fun in even the most mundane moments — it's a real "
                "superpower. The years we've spent together have given me some of the best memories, "
                "and I'm so glad our paths crossed the way they did.<br><br>"
                "Wishing you a year as bright, bold, and beautiful as you are. You deserve every bit of "
                "the happiness coming your way. Here's to you! 🎊"
            ),
        },
        {
            "color": "teal",
            "avatar": "🙌",
            "name": "Abhiranjan Bhaiya",
            "role": "Your Big Brother",
            "body": (
                "Naincy, some people start as colleagues and quietly become family — and that's exactly "
                "what happened here. Watching you over these years, your dedication, your creativity, "
                "the way you make every single day more colourful for everyone around you — it's been "
                "a privilege, genuinely.<br><br>"
                "You're not just a great colleague, you're an amazing human being. Your heart is big, "
                "your spirit is bigger, and the way you care for the people around you without making "
                "a big deal of it — that's rare and that's <strong>you</strong>.<br><br>"
                "On your birthday, I want you to know we see you — your hard work, your kindness, "
                "your dreams, all of it. Keep going, keep creating, keep being the wonderful person "
                "you are. This year belongs to you. Happy birthday! 🌸"
            ),
        },
    ]

    for msg in _MESSAGES:
        st.markdown(
            f"""
<div class="msg-card {msg['color']}">
    <div class="msg-sender">
        <div class="msg-avatar">{msg['avatar']}</div>
        <div>
            <div class="msg-name">{msg['name']}</div>
            <div class="msg-role">{msg['role']}</div>
        </div>
    </div>
    <div class="msg-body">{msg['body']}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="gallery-intro" style="margin:40px 0 6px 0;">Our favourite frames with you 📸</div>',
        unsafe_allow_html=True,
    )
    show_photo_gallery_naincy()

    if st.button("Feel the magic again ✨", use_container_width=True, type="primary"):
        show_fireworks()
        st.balloons()
        time.sleep(0.6)
        st.balloons()
        time.sleep(0.6)
        st.balloons()
        st.success("Happy Birthday, Naincy! 🎀💖")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="text-align:center; color:#c084fc; font-family:'Poppins',sans-serif;
            font-size:12px; letter-spacing:0.28em; padding:28px 16px;
            margin-top:24px; font-weight:400; text-transform:uppercase;">
    With Love · Divya, Ayan Bhaiya, Abhijot &amp; Abhiranjan Bhaiya
</div>
""",
    unsafe_allow_html=True,
)
