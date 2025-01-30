import streamlit as st
import numpy as np
from scipy.io.wavfile import write
from io import BytesIO
import random

# Configure page
st.set_page_config(page_title="Advanced Nature Generator", page_icon="🌍")

# Expanded sound profiles with layered ecosystems
NATURE_SOUNDS = {
    "Tropical Rainforest": {
        "components": {
            "rain": {"intensity": 0.6, "drop_size": 0.4},
            "thunder": {"frequency": 0.03, "boom_duration": 1.5},
            "jungle_birds": {"density": 0.1, "pitch_variance": 0.8},
            "insects": {"type": "cicadas", "density": 0.7},
            "waterfall": {"distance": 0.3, "spray_intensity": 0.2}
        },
        "bg_color": "#1e3b22"
    },
    "Arctic Winds": {
        "components": {
            "wind": {"speed": 0.9, "gust_frequency": 0.4},
            "ice_cracks": {"frequency": 0.05, "intensity": 0.3},
            "snowfall": {"intensity": 0.8, "crystal_size": 0.5},
            "aurora": {"hum_frequency": 45, "modulation": 0.1}
        },
        "bg_color": "#a8d0e6"
    },
    "Desert Night": {
        "components": {
            "wind": {"speed": 0.4, "sand_grain": 0.7},
            "coyote": {"frequency": 0.02, "pitch": 0.3},
            "cricket": {"density": 0.9, "rhythm": 0.8},
            "campfire": {"crackle_intensity": 0.6, "smoke": 0.4}
        },
        "bg_color": "#c2b280"
    },
    "Mystical Cave": {
        "components": {
            "water_drips": {"reverb": 0.8, "interval": 0.7},
            "crystal_hum": {"frequency": 174, "harmonics": 5},
            "echoing_steps": {"frequency": 0.05, "distance": 0.4},
            "subterranean_wind": {"pressure": 0.5, "tunnel_length": 0.6}
        },
        "bg_color": "#4a3b6a"
    }
}

# Advanced sound synthesis functions
def generate_wind(speed, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    base = 0.3 * np.random.randn(len(t))
    
    # Add gust patterns
    gusts = np.zeros(len(t))
    num_gusts = int(speed * duration * 10)
    for _ in range(num_gusts):
        start = random.randint(0, len(t)-1000)
        gust = np.random.randn(1000) * np.linspace(0,1,1000)
        gusts[start:start+1000] += gust * speed
    
    # Low-pass filter for wind effect
    wind = np.convolve(base + gusts, np.ones(100)/100, mode='same')
    return 0.5 * wind / np.max(np.abs(wind))

def generate_waterfall(distance, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    main_flow = 0.4 * np.random.randn(len(t))
    
    # White noise with modulated amplitude
    spray = np.random.randn(len(t)) * (1 - distance)
    spray *= np.sin(2 * np.pi * 0.5 * t) ** 2
    
    # Low-frequency rumble
    rumble = 0.1 * np.sin(2 * np.pi * 45 * t + 10 * np.sin(2 * np.pi * 0.2 * t))
    
    return 0.6 * (main_flow + spray + rumble)

def generate_insects(density, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    insects = np.zeros(len(t))
    
    # Create swarming pattern
    num_swarms = int(density * 20)
    for _ in range(num_swarms):
        freq = 3000 + 5000 * random.random()
        swarm = np.sin(2 * np.pi * freq * t) 
        swarm *= np.random.rand(len(t)) < density/10
        insects += swarm
    
    return 0.2 * insects / np.max(np.abs(insects))

# Main generation function
def generate_environment(duration_sec, profile):
    sample_rate = 44100
    t = np.linspace(0, duration_sec, sample_rate * duration_sec)
    audio = np.zeros(len(t))
    
    # Component routing
    if "wind" in profile["components"]:
        params = profile["components"]["wind"]
        audio += 0.5 * generate_wind(params["speed"], duration_sec)
    
    if "waterfall" in profile["components"]:
        params = profile["components"]["waterfall"]
        audio += 0.7 * generate_waterfall(params["distance"], duration_sec)
    
    if "insects" in profile["components"]:
        params = profile["components"]["insects"]
        audio += generate_insects(params["density"], duration_sec)
    
    # Normalize and convert
    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)
    return audio

# Streamlit UI
st.title("🌍 Advanced Nature Sound Generator")
st.markdown("Procedurally generated ecosystems with dynamic sound physics")

# Environment selection
selected_env = st.selectbox(
    "Choose Ecosystem",
    options=list(NATURE_SOUNDS.keys()),
    format_func=lambda x: f"{x} {'❄️' if 'Arctic' in x else '🏜️' if 'Desert' in x else '🌴'}"
)

# Parameter controls
with st.expander("Advanced Sound Parameters"):
    col1, col2 = st.columns(2)
    with col1:
        wind_control = st.slider("Wind Intensity", 0.0, 1.0, 0.5)
        water_control = st.slider("Water Presence", 0.0, 1.0, 0.7)
    with col2:
        animal_density = st.slider("Animal Activity", 0.0, 1.0, 0.3)
        mystical_elements = st.slider("Mystical Effects", 0.0, 1.0, 0.0)

# Generate audio
duration = st.slider("Duration (minutes)", 1, 180, 30)
if st.button("Generate Ecosystem"):
    profile = NATURE_SOUNDS[selected_env]
    with st.spinner(f"Rendering {selected_env} Soundscape..."):
        audio = generate_environment(duration * 60, profile)
        buffer = BytesIO()
        write(buffer, 44100, audio)
        
        st.audio(buffer.getvalue(), format='audio/wav')
        st.download_button(
            label="Download Soundscape",
            data=buffer.getvalue(),
            file_name=f"{selected_env.replace(' ', '_')}.wav",
            mime="audio/wav"
        )

# Style customization
st.markdown(f"""
<style>
.stSelectbox:first-child > div {{
    border: 2px solid {NATURE_SOUNDS[selected_env]['bg_color']} !important;
}}
[data-testid="stExpander"] {{
    background: {NATURE_SOUNDS[selected_env]['bg_color']}20;
}}
</style>
""", unsafe_allow_html=True)
