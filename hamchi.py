# =====================================================================================
# SANCHI ❤️  —  Ek Interactive Love Story (Streamlit App)
# =====================================================================================
# Run karne ke liye (VS Code terminal me):
#   pip install streamlit
#   streamlit run sanchi_app.py
#
# Password change karne ke liye niche "CONFIG" section me PASSWORD variable badlo.
# =====================================================================================

import streamlit as st
import time
import random
import base64
import os

# =====================================================================================
# SECTION 1: CONFIG
# =====================================================================================

PASSWORD = "sanchi14"          # <-- yahan apna password set karo
PAGE_TITLE = "Sanchi ❤️"
PAGE_ICON = "❤️"
MUSIC_FILE = "song.mp3"        # <-- isi folder me apni mp3 file ka naam yahan daalo
DEBUG_SHOW_MUSIC_PLAYER = False  # <-- True rakho testing ke liye (player dikhega), phir False kar dena

# Response dekhne ke liye secret key (URL me ?admin=<ye_key> daalkar response dekh sakte ho)
ADMIN_KEY = "hamid-only-2026"   # <-- isko apne hisaab se ek unique/mushkil sa keyword bana do
RESPONSE_FILE = "response.txt"

# Agar URL me ?admin=<ADMIN_KEY> hai, toh admin page dikhega — warna normal love-story page config
_is_admin_request = st.query_params.get("admin", "") == ADMIN_KEY

if _is_admin_request:
    st.set_page_config(page_title="Response 🔒", page_icon="🔒", layout="centered")
else:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="centered",
        initial_sidebar_state="collapsed",
    )

# =====================================================================================
# SECTION 2: CONTENT DATA  (seedha tumhare messages se liya gaya, order same rakha hai)
# =====================================================================================

STORY_SLIDES = [
    {
        "emoji": "❤️",
        "title": "Sanchi",
        "body": """Ek message...

jo shayad mujhe bahut pehle keh dena chahiye tha.

Ye koi normal message nahi hai.

Na koi excuse hai,
na koi justification.

Bas Hamid ke dil ki kuch baatein hain...
jo shayad saamne kehne ki himmat nahi hui.""",
    },
    {
        "emoji": "🎂",
        "title": "Happy Birthday, Sanchi",
        "body": """Sabse pehle...
I genuinely hope ki tum hamesha khush raho.

Tum jo chahti ho, wo achieve karo.

Tumhari life mein bahut saari achhi cheezein aayein.
Aur tumhare face par ye smile hamesha rahe.

Aaj tumhara special day hai.
Isliye meri taraf se bas ek simple si wish hai —

Khush rehna. Hamesha. ❤️""",
    },
    {
        "emoji": "😔",
        "title": "I'm Sorry",
        "body": """Sanchi...
Mujhe pata hai maine galtiyan ki hain.

Aur main apni galtiyon ko kisi excuse ke peeche hide nahi karna chahta.
Jo galat kiya, wo galat tha.

Shayad us waqt mujhe samajh nahi tha
ki meri kuch baatein, mera behaviour
aur meri kuch decisions tumhe kitna hurt kar rahe the.

Aaj jab peeche mudkar dekhta hoon,
toh kaafi cheezein samajh aati hain.

Kaash main kuch cheezein us waqt samajh pata.

I'm genuinely sorry. ❤️""",
    },
    {
        "emoji": "🤍",
        "title": "No Pressure",
        "body": """Main tumse kuch force nahi karna chahta.
Na koi answer chahiye.
Na koi explanation.

Na ye chahta hoon ki tum sirf meri feelings ki wajah se kuch decide karo.

Tum jo feel karti ho, wo tumhara hai.
Aur tumhara decision tumhara hi rahega.

Main bas chahta tha ki meri kuch baatein
ek baar tum tak pahunch jaayein.""",
    },
    {
        "emoji": "💭",
        "title": "Kuch Baatein",
        "body": """Kabhi kabhi hum kisi insaan ki value
tab samajhte hain jab wo pehle ki tarah paas nahi hota.

Baatein wahi hoti hain...
yaadein wahi hoti hain...
bas insaan ki presence missing hoti hai.

Aur tab samajh aata hai
ki kuch log hamari life mein kitni important jagah bana chuke the.""",
    },
    {
        "emoji": "🌙",
        "title": "Ab Samajh Aata Hai",
        "body": """Tumhari importance mujhe pehle bhi thi.
Lekin shayad main usse us tarah samajh nahi paya
jis tarah samajhna chahiye tha.

Maine ye seekha hai ki kisi ke saath hona
sirf feelings ka naam nahi hai.

Uski baat sunna...
uski feelings samajhna...
respect dena...
aur apni galti accept karna...
ye sab bhi utna hi important hai.

Aur ye cheezein mujhe samajhne mein der hui.""",
    },
    {
        "emoji": "📸",
        "title": "Kuch Yaadein",
        "body": """Kuch moments bahut ordinary hote hain.
Us waqt lagta hai bas ek normal day hai...
normal conversation hai...
normal photo hai.

Lekin baad mein wahi chhoti-chhoti cheezein
sabse zyada yaad aati hain.

Tumhare saath bitaye hue kuch moments bhi
mere liye waise hi hain.

Photos dekhne par sirf photo nahi dikhti.
Us time ki feeling yaad aa jaati hai.

Aur shayad isi liye kuch memories ko
bhoolna itna easy nahi hota.""",
    },
    {
        "emoji": "✨",
        "title": "Ek Realization",
        "body": """Mujhe realize hua hai
ki kisi ko love karna sirf usse apne paas rakhna nahi hai.

Kabhi kabhi uski feelings ko samajhna bhi love hai.
Uski boundaries ko respect karna bhi love hai.
Apni mistakes ko accept karna bhi love hai.

Aur jab zarurat ho, apne ego ko side rakhna bhi.""",
    },
    {
        "emoji": "🌱",
        "title": "Maine Kya Seekha",
        "body": """Maine ye seekha hai ki words bolna easy hai.
Lekin change dikhana difficult.

Promises karna easy hai.
Lekin unhe actions mein lana difficult.

Main ye promise nahi karunga ki mujhse kabhi galti nahi hogi.
Kyuki main perfect nahi hoon.

Lekin agar kabhi mujhe kuch sahi karne ka chance mila...
toh main us chance ko lightly nahi lunga.""",
    },
    {
        "emoji": "👋",
        "title": "Hi",
        "body": """Pata hai, kabhi kabhi lagta hai
ki hum dono ke beech bahut kuch kehna baaki reh gaya.

Shayad conversations khatam ho gayi hain...
lekin mere liye baat karne ki possibility
kabhi completely khatam nahi hui.

Main bas itna chahta hoon ki agar kabhi tumhe lage
ki normal tareeke se baat ho sakti hai...
toh main yahin hoon.

No pressure. No expectations.
Bas ek simple sa... Hi. ❤️""",
    },
    {
        "emoji": "📝",
        "title": "Ek Shayari",
        "body": """Kuch baatein adhuri reh gayi,
kuch lafz kehne se reh gaye.

Tum paas thi toh samajh na paaya,
door hui toh sab samajh aa gaye.

Galti meri thi,
ye maan ne mein der hui.

Tumhari kadar thi dil mein,
bas dikhane mein der hui. ❤️""",
    },
]

QUESTION_SLIDE = {
    "emoji": "❓",
    "title": "Bas Ek Sawaal",
    "body": """Main tumse koi bada promise nahi maang raha.
Na past ko erase karne ko keh raha hoon.
Na ye keh raha hoon ki sab kuch pehle jaisa ho jaana chahiye.

Bas ek sawaal hai...""",
    "question": "Kya tum mere se pyaar karti ho?",
}

YES_SLIDE = {
    "emoji": "💞",
    "title": "I Love You Too, Sanchi",
    "body": """Sach kahun...
ye words dekhna shayad mere liye
is poori story ka sabse beautiful moment hai.

Thank you.

Main is chance ko sirf words tak nahi rakhna chahta.
Jo bhi hoga, slowly hoga.
Bina unnecessary expectations ke.
Bina pressure ke.

Aur is baar actions words se zyada bolenge.

I Love You, Sanchi. ❤️

— From Hamid ❤️""",
}

NO_SLIDE = {
    "emoji": "🤍",
    "title": "It's okay.",
    "body": """Agar tumhara answer NO hai...
toh bhi it's okay.

Main tumhe guilty feel nahi karwana chahta.
Na hi tumhe apna decision explain karne ki zarurat hai.

Tumne jo decide kiya hai, main uski respect karta hoon.

Maine ye sab tumhe convince karne ke liye nahi likha tha.
Bas kuch baatein thi jo main kehna chahta tha.

I genuinely wish you the best.
Khush rehna. ❤️""",
}

# Gradient theme rotates across slides so every screen feels fresh
GRADIENTS = [
    "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
    "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
    "linear-gradient(135deg, #ff6a88 0%, #ff99ac 100%)",
    "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
    "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)",
    "linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%)",
    "linear-gradient(135deg, #c471f5 0%, #fa71cd 100%)",
    "linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)",
]

# =====================================================================================
# SECTION 3: STYLING (CSS)
# =====================================================================================

def inject_css(gradient: str):
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Dancing+Script:wght@600;700&family=Great+Vibes&display=swap');

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .block-container {{ padding-top: 2rem !important; padding-bottom: 2rem !important; }}

        .stApp {{
            background: {gradient};
            background-size: 400% 400%;
            animation: gradientShift 14s ease infinite;
            font-family: 'Poppins', sans-serif;
        }}

        @keyframes gradientShift {{
            0% {{background-position: 0% 50%;}}
            50% {{background-position: 100% 50%;}}
            100% {{background-position: 0% 50%;}}
        }}

        /* ---------- floating hearts + sparkles ---------- */
        .heart, .sparkle {{
            position: fixed;
            top: 100%;
            opacity: 0.8;
            z-index: 0;
            pointer-events: none;
        }}
        .heart {{ animation: floatUp linear infinite; font-size: 22px; }}
        .sparkle {{ animation: sparkleUp linear infinite; font-size: 14px; filter: drop-shadow(0 0 4px #fff); }}

        @keyframes floatUp {{
            0% {{ transform: translateY(0) rotate(0deg) scale(1); opacity: 0.85; }}
            100% {{ transform: translateY(-115vh) rotate(360deg) scale(0.8); opacity: 0; }}
        }}
        @keyframes sparkleUp {{
            0% {{ transform: translateY(0) scale(0.4); opacity: 0; }}
            10% {{ opacity: 1; }}
            100% {{ transform: translateY(-100vh) scale(1.1); opacity: 0; }}
        }}

        /* ---------- glowing glass card ---------- */
        .glass-card {{
            background: rgba(255, 255, 255, 0.58);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: clamp(18px, 4vw, 28px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0 8px 40px rgba(120, 30, 90, 0.28), 0 0 0 1px rgba(255,255,255,0.3) inset;
            padding: clamp(26px, 6vw, 46px) clamp(20px, 5vw, 40px);
            margin: 14px auto 10px auto;
            max-width: 620px;
            width: 100%;
            box-sizing: border-box;
            animation: cardIn 0.75s cubic-bezier(.2,.9,.25,1);
            position: relative;
            z-index: 1;
            overflow: hidden;
        }}
        .glass-card::before {{
            content: "";
            position: absolute;
            inset: -2px;
            border-radius: inherit;
            padding: 2px;
            background: linear-gradient(120deg, #ff6a88, #ffd6e8, #c471f5, #ff6a88);
            background-size: 300% 300%;
            animation: borderGlow 6s ease infinite;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0.55;
            pointer-events: none;
        }}
        @keyframes borderGlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes cardIn {{
            from {{ opacity: 0; transform: translateY(30px) scale(0.96); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .card-emoji {{
            font-size: clamp(38px, 9vw, 50px);
            text-align: center;
            margin-bottom: 6px;
            animation: pulse 1.8s ease-in-out infinite;
            filter: drop-shadow(0 4px 10px rgba(200,50,100,0.35));
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.12); }}
        }}

        .card-title {{
            font-family: 'Dancing Script', cursive;
            font-size: clamp(30px, 7vw, 40px);
            text-align: center;
            color: #6a1b4d;
            margin-bottom: 16px;
            text-shadow: 0 2px 10px rgba(255,255,255,0.6);
        }}

        .card-body {{
            font-size: clamp(15px, 4vw, 18px);
            line-height: 1.95;
            color: #3a2436;
            white-space: pre-line;
            text-align: center;
        }}

        .reveal-line {{
            display: block;
            opacity: 0;
            transform: translateY(10px);
            animation: lineIn 0.6s ease forwards;
        }}
        @keyframes lineIn {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .question-text {{
            font-family: 'Dancing Script', cursive;
            font-size: clamp(24px, 6vw, 32px);
            text-align: center;
            color: #6a1b4d;
            margin-top: 20px;
            margin-bottom: 4px;
            animation: pulse 2.2s ease-in-out infinite;
        }}

        .progress-wrap {{
            max-width: 620px;
            margin: 4px auto 14px auto;
            text-align: center;
            padding: 0 8px;
        }}

        .progress-track {{
            width: 100%;
            height: 8px;
            border-radius: 20px;
            background: rgba(255,255,255,0.45);
            overflow: hidden;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.15);
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 20px;
            background: linear-gradient(90deg, #ff6a88, #c471f5, #ff9a9e);
            background-size: 200% 100%;
            animation: progressShine 2.5s linear infinite;
            transition: width 0.5s ease;
        }}
        @keyframes progressShine {{
            0% {{ background-position: 0% 0%; }}
            100% {{ background-position: 200% 0%; }}
        }}
        .progress-label {{
            font-size: 12px;
            color: #6a1b4d;
            opacity: 0.8;
            margin-top: 6px;
            letter-spacing: 1px;
        }}

        .lock-title {{
            font-family: 'Great Vibes', 'Dancing Script', cursive;
            font-size: clamp(38px, 10vw, 54px);
            text-align: center;
            color: #6a1b4d;
            margin-top: 60px;
            text-shadow: 0 2px 12px rgba(255,255,255,0.7);
            animation: pulse 2.5s ease-in-out infinite;
        }}

        div.stButton > button {{
            border-radius: 30px;
            border: none;
            padding: 12px 30px;
            font-weight: 600;
            font-size: clamp(14px, 3.6vw, 16px);
            background: linear-gradient(135deg, #ff6a88, #ff99ac);
            background-size: 200% 200%;
            color: white;
            box-shadow: 0 6px 20px rgba(255, 100, 140, 0.4);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background-position 0.4s ease;
        }}
        div.stButton > button:hover {{
            transform: scale(1.06) translateY(-2px);
            background-position: 100% 100%;
            box-shadow: 0 10px 28px rgba(255, 90, 130, 0.55);
            color: white;
        }}
        div.stButton > button:active {{
            transform: scale(0.97);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def floating_sparkles(n: int = 10):
    sparkle_html = ""
    for _ in range(n):
        left = random.randint(0, 100)
        duration = random.randint(6, 14)
        delay = random.randint(0, 8)
        icon = random.choice(["✨", "⭐", "💫"])
        sparkle_html += (
            f'<div class="sparkle" style="left:{left}%; '
            f'animation-duration:{duration}s; animation-delay:{delay}s;">{icon}</div>'
        )
    st.markdown(sparkle_html, unsafe_allow_html=True)


def celebration_burst(n: int = 26):
    """YES ke baad ek bada heart/confetti burst dikhata hai."""
    icons = ["❤️", "💕", "💖", "💗", "🎉", "✨", "💞"]
    html = ""
    for _ in range(n):
        left = random.randint(0, 100)
        duration = random.uniform(3.5, 7)
        delay = random.uniform(0, 1.2)
        size = random.randint(18, 34)
        icon = random.choice(icons)
        html += (
            f'<div class="heart" style="left:{left}%; font-size:{size}px; '
            f'animation-duration:{duration}s; animation-delay:{delay}s;">{icon}</div>'
        )
    st.markdown(html, unsafe_allow_html=True)


def floating_hearts(n: int = 14):
    hearts_html = ""
    for _ in range(n):
        left = random.randint(0, 100)
        duration = random.randint(8, 18)
        delay = random.randint(0, 10)
        size = random.choice(["❤️", "💕", "💗", "💖"])
        hearts_html += (
            f'<div class="heart" style="left:{left}%; '
            f'animation-duration:{duration}s; animation-delay:{delay}s;">{size}</div>'
        )
    st.markdown(hearts_html, unsafe_allow_html=True)


# =====================================================================================
# SECTION 3B: BACKGROUND MUSIC
# =====================================================================================

# Script jis folder me hai, usi ke andar music file dhoondega — chahe terminal kahin se bhi chalao
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_audio_bytes(file_name: str):
    """mp3 file ko raw bytes me padhta hai. File na mile toh (None, path) return karta hai."""
    file_path = os.path.join(SCRIPT_DIR, file_name)
    if not os.path.exists(file_path):
        return None, file_path
    with open(file_path, "rb") as f:
        data = f.read()
    return data, file_path


def get_audio_base64(file_name: str):
    """mp3 file ko base64 me convert karta hai. File na mile toh (None, path) return karta hai."""
    data, file_path = get_audio_bytes(file_name)
    if data is None:
        return None, file_path
    return base64.b64encode(data).decode(), file_path


def embed_background_music():
    """Song ko autoplay + loop mode me bajata hai. File na mile toh warning dikhata hai."""
    if DEBUG_SHOW_MUSIC_PLAYER:
        # Testing mode: raw bytes seedhe Streamlit ke apne player ko diye jaate hain
        raw_bytes, resolved_path = get_audio_bytes(MUSIC_FILE)
        if raw_bytes is None:
            st.warning(f"🎵 Song file nahi mili yahan: {resolved_path}\n\nCheck karo ki file isi naam aur isi folder me hai.")
            return
        st.markdown("**🔧 Debug mode: neeche wala player manually try karo 👇**")
        st.caption(f"File size: {len(raw_bytes) / (1024*1024):.2f} MB — path: {resolved_path}")
        st.audio(raw_bytes, format="audio/mp3")
        return

    audio_b64, resolved_path = get_audio_base64(MUSIC_FILE)
    if audio_b64 is None:
        st.warning(f"🎵 Song file nahi mili yahan: {resolved_path}\n\nCheck karo ki file isi naam aur isi folder me hai.")
        return

    st.markdown(
        f"""
        <audio autoplay loop style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================================
# SECTION 3C: RESPONSE SAVING (sirf tumhe dikhega, kisi aur ko nahi)
# =====================================================================================

def save_response(answer: str):
    """Jab Sanchi YES ya NO dabaye, response ko ek file me save karta hai."""
    try:
        file_path = os.path.join(SCRIPT_DIR, RESPONSE_FILE)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{answer}\n{time.strftime('%d-%m-%Y %I:%M %p')}")
    except Exception:
        pass  # kabhi fail ho toh bhi Sanchi ka experience na tute


def load_response():
    """Saved response padhta hai. Kuch save nahi hai toh None deta hai."""
    file_path = os.path.join(SCRIPT_DIR, RESPONSE_FILE)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n")
    if len(content) < 2:
        return None
    return {"answer": content[0], "time": content[1]}


def admin_view():
    """Sirf tumhare liye — secret URL se khulta hai, Sanchi ko is page ka pata nahi hoga."""
    st.title("🔒 Sanchi ka Response")
    result = load_response()
    if result is None:
        st.info("Abhi tak koi response nahi aaya. Jab Sanchi YES ya NO dabayegi, yahan dikhega.")
    elif result["answer"] == "yes":
        st.success(f"💞 Sanchi ne **YES** bola hai!")
        st.caption(f"Time: {result['time']}")
        st.balloons()
    else:
        st.warning(f"Sanchi ne **NO** bola hai.")
        st.caption(f"Time: {result['time']}")
    if st.button("🔄 Refresh"):
        st.rerun()


# =====================================================================================
# SECTION 4: SESSION STATE INIT
# =====================================================================================

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0
if "answered" not in st.session_state:
    st.session_state.answered = None  # None | "yes" | "no"


# =====================================================================================
# SECTION 5: PASSWORD GATE
# =====================================================================================

def password_gate():
    inject_css(GRADIENTS[0])
    floating_hearts(10)
    floating_sparkles(10)
    st.markdown(f'<div class="lock-title">Ek Chhota Sa Secret {PAGE_ICON}</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center; color:#5a3a4d; font-size:16px;">'
        "Ye sirf tumhare liye hai...</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Password", type="password", label_visibility="collapsed",
                             placeholder="Password daalo...")
        if st.button("Unlock ❤️", use_container_width=True):
            if pwd == PASSWORD:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.error("Galat password... ek baar phir try karo 🤍")


# =====================================================================================
# SECTION 6: CARD RENDERER
# =====================================================================================

def build_reveal_html(text: str, base_delay: float = 0.15, step: float = 0.11):
    """Har line ko chhote se delay ke saath fade-in karwata hai — typewriter jaisa feel."""
    lines = text.split("\n")
    parts = []
    delay = base_delay
    for line in lines:
        if line.strip() == "":
            parts.append('<span class="reveal-line" style="height:10px;"></span>')
        else:
            parts.append(f'<span class="reveal-line" style="animation-delay:{delay:.2f}s;">{line}</span>')
            delay = min(delay + step, base_delay + 2.2)  # zyada lamba text ho toh bhi delay cap rahe
    return "".join(parts)


def render_card(slide: dict, extra_html: str = ""):
    body_html = build_reveal_html(slide["body"])
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-emoji">{slide['emoji']}</div>
            <div class="card-title">{slide['title']}</div>
            <div class="card-body">{body_html}</div>
            {extra_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================================
# SECTION 7: MAIN STORY FLOW
# =====================================================================================

def story_flow():
    total = len(STORY_SLIDES)
    idx = st.session_state.slide_index

    gradient = GRADIENTS[idx % len(GRADIENTS)]
    inject_css(gradient)
    floating_hearts(12)
    floating_sparkles(8)
    embed_background_music()

    # --- Ending already decided (Yes / No) ---
    if st.session_state.answered == "yes":
        celebration_burst(30)
        render_card(YES_SLIDE)
        st.balloons()
        st.markdown('<div class="progress-wrap">', unsafe_allow_html=True)
        if st.button("🔁 Dobara Se Padhna Hai", use_container_width=False):
            st.session_state.slide_index = 0
            st.session_state.answered = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.session_state.answered == "no":
        render_card(NO_SLIDE)
        st.markdown('<div class="progress-wrap">', unsafe_allow_html=True)
        if st.button("🔁 Dobara Se Padhna Hai", use_container_width=False):
            st.session_state.slide_index = 0
            st.session_state.answered = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # --- Final question slide (after last story slide) ---
    if idx >= total:
        render_card(QUESTION_SLIDE, extra_html=f'<div class="question-text">{QUESTION_SLIDE["question"]}</div>')
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col2:
            if st.button("YES ❤️", use_container_width=True):
                st.session_state.answered = "yes"
                save_response("yes")
                st.rerun()
        with col3:
            if st.button("NO", use_container_width=True):
                st.session_state.answered = "no"
                save_response("no")
                st.rerun()
        return

    # --- Normal story slide ---
    slide = STORY_SLIDES[idx]
    render_card(slide)

    # animated progress bar
    percent = int(((idx + 1) / total) * 100)
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-track"><div class="progress-fill" style="width:{percent}%;"></div></div>
            <div class="progress-label">{idx + 1} / {total}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if idx > 0:
            if st.button("⬅️ Peeche", use_container_width=True):
                st.session_state.slide_index -= 1
                st.rerun()
    with col3:
        label = "Aage ➡️" if idx < total - 1 else "Continue ❤️"
        if st.button(label, use_container_width=True):
            st.session_state.slide_index += 1
            st.rerun()


# =====================================================================================
# SECTION 8: APP ENTRY POINT
# =====================================================================================

def main():
    if _is_admin_request:
        admin_view()
        return
    if not st.session_state.unlocked:
        password_gate()
    else:
        story_flow()


if __name__ == "__main__":
    main()
