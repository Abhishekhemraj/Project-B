import streamlit as st
import json
import os
import base64
from phase4_integration.main import JokeGeneratorApp

# Set page config
st.set_page_config(
    page_title="AI Joke Generator",
    page_icon="😂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Function to encode local files to base64
@st.cache_data
def get_base64_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Initialize session state for audio trigger and joke storage
if "audio_sync" not in st.session_state:
    st.session_state.audio_sync = 0
if "current_joke" not in st.session_state:
    st.session_state.current_joke = None

# Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Arvo:wght@400;700&family=Pacifico&display=swap');

    /* 1. Remove Streamlit Header & Footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* 2. Warm 70s Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f4d35e 0%, #ee964b 50%, #f95738 100%);
        background-attachment: fixed;
        color: #3b2f2f;
    }

    /* Global font override */
    html, body, [class*="st-"] {
        font-family: 'Arvo', serif;
    }

    /* Branding Header - Banner Style */
    .branding-banner {
        background-color: #fff8e7;
        padding: 1.5rem 2rem;
        border-radius: 20px;
        border: 4px solid #3b2f2f;
        box-shadow: 8px 8px 0px #d62828;
        text-align: center;
        margin: 2rem auto;
        display: block;
        width: fit-content;
    }
    
    .title-text {
        font-family: 'Bungee', cursive;
        color: #3b2f2f;
        font-size: 3rem !important;
        margin: 0;
        line-height: 1.1;
    }

    /* Joke card styling - Positioned high */
    .joke-card {
        background-color: rgba(255, 248, 231, 0.95);
        padding: 2.5rem;
        border-radius: 40px;
        box-shadow: 12px 12px 0px #d62828;
        border: 5px solid #3b2f2f;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        z-index: 10;
        animation: slideDown 0.4s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .joke-text {
        font-size: 2rem;
        line-height: 1.3;
        color: #3b2f2f;
        font-weight: 800;
        margin: 0;
    }
    
    /* Input Container styling */
    div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background-color: rgba(255, 248, 231, 0.4);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #3b2f2f;
        backdrop-filter: blur(5px);
    }

    /* Button styling */
    div.stButton > button:first-child {
        background-color: #3b2f2f;
        color: #f4d35e;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 900;
        font-family: 'Bungee', cursive;
        font-size: 1.5rem;
        width: 100%;
        border: 3px solid #fff8e7;
        box-shadow: 6px 6px 0px #d62828;
        transition: all 0.1s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #d62828;
        color: #fff8e7;
        transform: translate(2px, 2px);
        box-shadow: 4px 4px 0px #3b2f2f;
    }

    /* Hide any possible audio UI */
    audio {
        display: none !important;
    }

    label {
        color: #3b2f2f !important;
        font-family: 'Bungee', cursive !important;
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # 1. Branding Header
    st.markdown("""
        <div class="branding-banner">
            <h1 class="title-text">😂 Joke Generator</h1>
        </div>
    """, unsafe_allow_html=True)

    # Instance the backend app
    @st.cache_resource
    def load_app():
        return JokeGeneratorApp()
    
    app = load_app()

    # 2. Output Section (Positioned Above Filters)
    joke_placeholder = st.container()

    # 3. Input Section
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            length = st.selectbox("📏 JOKE LENGTH", options=["short", "medium", "long"], index=1)
        with col2:
            lameness_options = {"Low": "witty", "Medium": "average", "High": "cringe"}
            lameness_user = st.selectbox("🥴 CRINGE METER", options=list(lameness_options.keys()), index=1)
            lameness_internal = lameness_options[lameness_user]

        st.write("") 
        generate_btn = st.button("🎤 Generate a Joke")

    # Handle Generation Logic
    if generate_btn:
        st.session_state.audio_sync += 1 # Important: ensures the audio HTML is unique and retriggers autoplay
        with st.spinner("Cooking up something funny..."):
            try:
                response_json = app.get_joke(length, lameness_internal)
                data = json.loads(response_json)
                
                if data["status"] == "success":
                    st.session_state.current_joke = data
                    st.balloons()
                else:
                    st.error(f"Error: {data['error']['message']}")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    # Display Current Joke and Background if available
    if st.session_state.current_joke:
        joke_data = st.session_state.current_joke
        joke = joke_data["joke"]
        
        # 🦥 Background Injection
        sloth_b64 = get_base64_bin_file("sloth-laugh.gif")
        if sloth_b64:
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: 
                        linear-gradient(rgba(244, 211, 94, 0.8), rgba(249, 87, 56, 0.8)),
                        url("data:image/gif;base64,{sloth_b64}");
                    background-repeat: repeat;
                    background-size: auto, 120px;
                    background-blend-mode: overlay;
                }}
                </style>
            """, unsafe_allow_html=True)

        # 🃏 Render Joke Card at the Top
        with joke_placeholder:
            st.markdown(f"""
                <div class="joke-card">
                    <div class="joke-text">
                        "{joke['text']}"
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 🔊 HIDDEN HTML AUDIO TRIGGER
            audio_b64 = get_base64_bin_file("Drums Audio.mp3")
            if audio_b64:
                # We inject an unique audio tag to force the browser to autoplay it on every click
                st.markdown(f"""
                    <audio autoplay style="display:none;">
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        <!-- trigger_id: {st.session_state.audio_sync} -->
                    </audio>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #3b2f2f; font-family: Pacifico, cursive; font-size: 1.2rem;'>"
        "Stay Groovy! • Built with ❤️ on Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
