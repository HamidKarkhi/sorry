# python -m streamlit run hamchi.py

import streamlit as st
import time
import random
import base64
import os


PASSWORD = "sanchi14"          # <-- yahan apna password set karo
PAGE_TITLE = "Sanchi ❤️"
PAGE_ICON = "❤️"
MUSIC_FILE = "song.mp3"        # <-- isi folder me apni mp3 file ka naam yahan daalo
DEBUG_SHOW_MUSIC_PLAYER = True  # <-- True rakho testing ke liye (player dikhega), phir False kar dena

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
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Dancing+Script:wght@600;700&display=swap');

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        .stApp {{
            background: {gradient};
            background-size: 400% 400%;
            animation: gradientShift 12s ease infinite;
            font-family: 'Poppins', sans-serif;
        }}

        @keyframes gradientShift {{
            0% {{background-position: 0% 50%;}}
            50% {{background-position: 100% 50%;}}
            100% {{background-position: 0% 50%;}}
        }}

        .heart {{
            position: fixed;
            top: 100%;
            font-size: 22px;
            opacity: 0.75;
            animation: floatUp linear infinite;
            z-index: 0;
            pointer-events: none;
        }}

        @keyframes floatUp {{
            0% {{ transform: translateY(0) rotate(0deg); opacity: 0.8; }}
            100% {{ transform: translateY(-110vh) rotate(360deg); opacity: 0; }}
        }}

        .glass-card {{
            background: rgba(255, 255, 255, 0.55);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.25);
            padding: 42px 36px;
            margin: 18px auto 10px auto;
            max-width: 620px;
            animation: fadeInUp 0.7s ease;
            position: relative;
            z-index: 1;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(25px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .card-emoji {{
            font-size: 48px;
            text-align: center;
            margin-bottom: 6px;
            animation: pulse 1.8s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.12); }}
        }}

        .card-title {{
            font-family: 'Dancing Script', cursive;
            font-size: 38px;
            text-align: center;
            color: #6a1b4d;
            margin-bottom: 18px;
        }}

        .card-body {{
            font-size: 18px;
            line-height: 1.9;
            color: #3a2436;
            white-space: pre-line;
            text-align: center;
        }}

        .question-text {{
            font-family: 'Dancing Script', cursive;
            font-size: 30px;
            text-align: center;
            color: #6a1b4d;
            margin-top: 22px;
            margin-bottom: 6px;
        }}

        .progress-wrap {{
            max-width: 620px;
            margin: 0 auto;
            text-align: center;
        }}

        .lock-title {{
            font-family: 'Dancing Script', cursive;
            font-size: 50px;
            text-align: center;
            color: #6a1b4d;
            margin-top: 60px;
        }}

        div.stButton > button {{
            border-radius: 30px;
            border: none;
            padding: 10px 28px;
            font-weight: 600;
            background: linear-gradient(135deg, #ff6a88, #ff99ac);
            color: white;
            transition: transform 0.15s ease;
        }}
        div.stButton > button:hover {{
            transform: scale(1.06);
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


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

def render_card(slide: dict, extra_html: str = ""):
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-emoji">{slide['emoji']}</div>
            <div class="card-title">{slide['title']}</div>
            <div class="card-body">{slide['body']}</div>
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
    embed_background_music()

    # --- Ending already decided (Yes / No) ---
    if st.session_state.answered == "yes":
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
                st.rerun()
        with col3:
            if st.button("NO", use_container_width=True):
                st.session_state.answered = "no"
                st.rerun()
        return

    # --- Normal story slide ---
    slide = STORY_SLIDES[idx]
    render_card(slide)

    # progress dots
    dots = "".join(
        ["●" if i == idx else "○" for i in range(total)]
    )
    st.markdown(
        f'<div class="progress-wrap"><p style="letter-spacing:6px; color:#6a1b4d;">{dots}</p></div>',
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
    if not st.session_state.unlocked:
        password_gate()
    else:
        story_flow()


if __name__ == "__main__":
    main()
