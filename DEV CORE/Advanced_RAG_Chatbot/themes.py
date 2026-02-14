import streamlit as st

THEMES = {
    "Cyberpunk": {
        "primary": "#ff00ff",
        "secondary": "#00ffff",
        "bg": "#0a0a0a",
        "text": "#ffffff",
        "gradient": "linear-gradient(135deg, #ff00ff 0%, #00ffff 100%)",
        "card_bg": "rgba(20, 20, 20, 0.8)",
        "sidebar_bg": "#050505"
    },
    "Neon Nights": {
        "primary": "#39ff14",
        "secondary": "#ff00ff",
        "bg": "#000000",
        "text": "#ffffff",
        "gradient": "linear-gradient(135deg, #39ff14 0%, #ff00ff 100%)",
        "card_bg": "rgba(10, 10, 10, 0.9)",
        "sidebar_bg": "#080808"
    },
    "Deep Ocean": {
        "primary": "#0077be",
        "secondary": "#00d2ff",
        "bg": "#001219",
        "text": "#ffffff",
        "gradient": "linear-gradient(135deg, #001219 0%, #00d2ff 100%)",
        "card_bg": "rgba(0, 31, 44, 0.8)",
        "sidebar_bg": "#000a0f"
    },
    "Matrix": {
        "primary": "#00ff41",
        "secondary": "#008f11",
        "bg": "#000000",
        "text": "#00ff41",
        "gradient": "linear-gradient(180deg, #003b00 0%, #000000 100%)",
        "card_bg": "rgba(0, 20, 0, 0.9)",
        "sidebar_bg": "#000500"
    },
    "Sunset": {
        "primary": "#ff4e50",
        "secondary": "#f9d423",
        "bg": "#1a1a1a",
        "text": "#ffffff",
        "gradient": "linear-gradient(135deg, #ff4e50 0%, #f9d423 100%)",
        "card_bg": "rgba(30,30,30, 0.8)",
        "sidebar_bg": "#111111"
    }
}

def apply_theme(theme_name):
    theme = THEMES.get(theme_name, THEMES["Cyberpunk"])
    
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
            
            .stApp {{
                background-color: {theme['bg']};
                color: {theme['text']};
                font-family: 'Rajdhani', sans-serif;
            }}
            
            [data-testid="stSidebar"] {{
                background-color: {theme['sidebar_bg']};
                border-right: 1px solid {theme['primary']};
            }}
            
            .stHeader {{
                background: transparent;
            }}
            
            h1, h2, h3 {{
                font-family: 'Orbitron', sans-serif;
                color: {theme['primary']};
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 0 0 10px {theme['primary']}55;
            }}
            
            .stButton>button {{
                background: {theme['gradient']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0.5rem 2rem;
                font-weight: bold;
                text-transform: uppercase;
                transition: all 0.3s ease;
                box-shadow: 0 0 15px {theme['primary']}33;
            }}
            
            .stButton>button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 0 25px {theme['primary']}77;
            }}
            
            .chatbot-container {{
                background: {theme['card_bg']};
                backdrop-filter: blur(10px);
                border: 1px solid {theme['secondary']}33;
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
            }}
            
            .confidence-meter {{
                height: 10px;
                border-radius: 5px;
                background: #333;
                overflow: hidden;
                margin-top: 10px;
            }}
            
            .confidence-fill {{
                height: 100%;
                transition: width 0.5s ease;
            }}
            
            .cache-indicator {{
                font-size: 0.8rem;
                color: {theme['secondary']};
                font-style: italic;
            }}
            
            /* Chat Message Styling */
            .stChatMessage {{
                background: {theme['card_bg']};
                border-left: 3px solid {theme['primary']};
                margin-bottom: 1rem;
                border-radius: 0 10px 10px 0;
            }}
            
            .stChatMessage[data-testimonial="user"] {{
                border-left: none;
                border-right: 3px solid {theme['secondary']};
                border-radius: 10px 0 0 10px;
            }}
        </style>
    """, unsafe_allow_html=True)
