import streamlit as st
import ollama

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DarkVerse AI",
    page_icon="🦇",
    layout="wide"
)

# ---------------- STYLE + ANIMATION ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background:
    radial-gradient(circle at 20% 20%, #1a0000, transparent 40%),
    radial-gradient(circle at 80% 70%, #000000, transparent 40%),
    linear-gradient(135deg,#000000,#0a0a0a,#140000);
}

/* Center chat container */
.block-container {
    max-width: 750px;
    margin: auto;
}

/* Title */
h1 {
    text-align:center;
    color:#ff1a1a;
    text-shadow:0 0 30px red;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(20,0,0,0.85);
    border-radius:18px;
    padding:14px;
    border:1px solid crimson;
    box-shadow:0 0 15px rgba(255,0,0,0.2);
    animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px)}
    to {opacity:1; transform:translateY(0)}
}

/* Buttons */
.stButton>button {
    background:linear-gradient(45deg,#3a0000,#8b0000);
    color:white;
    border-radius:12px;
    font-weight:bold;
    border:1px solid red;
}

/* Slider */
.stSlider label { color:white !important; }

/* ---------- ANIMATION BACKGROUND ---------- */

.floating-container{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    pointer-events:none;
    z-index:0;
}

/* glowing orbs */
.orb{
    position:absolute;
    border-radius:50%;
    filter:blur(40px);
    animation: float 12s infinite ease-in-out;
}

.orb1{ width:200px;height:200px;background:red;left:10%;top:70%; }
.orb2{ width:150px;height:150px;background:purple;left:80%;top:20%;animation-delay:2s; }
.orb3{ width:180px;height:180px;background:darkred;left:40%;top:10%;animation-delay:4s; }

@keyframes float{
    0%{transform:translateY(0px)}
    50%{transform:translateY(-60px)}
    100%{transform:translateY(0px)}
}

/* floating symbols */
.hero{
    position:absolute;
    width:120px;
    opacity:0.15;
    animation: drift 25s linear infinite;
}

.hero1{ left:-150px; top:60%; }
.hero2{ left:-200px; top:20%; animation-delay:10s;}

@keyframes drift{
    from{ transform:translateX(0)}
    to{ transform:translateX(120vw)}
}

</style>

<div class="floating-container">

<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>

<img class="hero hero1" src="hd-superman-s-logo-symbol-sign-png-701751694774174o3dnjsjthc.png">
<img class="hero hero2" src="the_boys__billy_butcher___transparent__by_speedcam_dgf20da-pre.png">

</div>
""", unsafe_allow_html=True)

st.title("🩸 DARKVERSE AI")

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are a dark comic universe AI.

STYLE:
- Dramatic
- Mythic
- Dark poetic tone

RULES:
- Always include dark emojis 😈🩸⚡🌑🔥
- Short cinematic replies
- Never casual tone
"""

# ---------------- MODEL FETCH ----------------
def get_models():
    try:
        data = ollama.list()
        models = []

        for m in data.get("models", []):
            if isinstance(m, dict):
                models.append(m.get("name") or m.get("model"))
            else:
                models.append(getattr(m, "model", None))

        return [m for m in models if m]
    except:
        return []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙ Dark Controls")

    models = get_models()
    if not models:
        st.warning("Run: ollama pull llama3")
        st.stop()

    model = st.selectbox("Choose Mind", models)
    temperature = st.slider("Chaos Level", 0.0, 1.5, 0.9, 0.1)

    if st.button("🧹 Wipe Memory"):
        st.session_state.messages=[{"role":"system","content":SYSTEM_PROMPT}]
        st.rerun()

# ---------------- MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages=[{"role":"system","content":SYSTEM_PROMPT}]

# ---------------- AVATARS (WORKING LINKS) ----------------
USER_AVATAR="d4bf12bdd3a9a8cb1af0ddbfab40fcb1.jpg"
BOT_AVATAR="Hot-Stuff-Enterprise-Z44-24x36-NA-Batman-Logo-Poster-24-x-36_8a6dba34-ac3b-496c-b72f-bba84311929c.0022e669a8ad1fbeeaae332e378eb179.webp"

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"]!="system":
        avatar = USER_AVATAR if msg["role"]=="user" else BOT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Speak into the abyss...")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_input)

    # ---------- RESPONSE ----------
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        placeholder = st.empty()
        reply=""

        try:
            stream = ollama.chat(
                model=model,
                messages=st.session_state.messages,
                stream=True,
                options={"temperature":temperature}
            )

            for chunk in stream:
                text = chunk.get("message",{}).get("content","")
                reply+=text
                placeholder.markdown(reply)

        except Exception as e:
            reply=f"Dark signal lost… {e}"
            placeholder.markdown(reply)

    st.session_state.messages.append({"role":"assistant","content":reply})
