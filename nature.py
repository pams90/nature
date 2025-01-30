import streamlit as st
import numpy as np
from scipy.io.wavfile import write
from io import BytesIO
import random

# Configure page
st.set_page_config(page_title="Ultimate Nature Generator", page_icon="🌍")

# Expanded sound profiles with layered ecosystems
NATURE_SOUNDS = {
    "Thunderstorm": {
        "components": {
            "rain": {"intensity": 0.8, "drop_size": 0.6},
            "thunder": {"frequency": 0.1, "boom_duration": 2.0},
            "wind": {"speed": 0.9, "gust_frequency": 0.5},
            "lightning": {"crackle_intensity": 0.7}
        },
        "bg_color": "#2c3e50"
    },
    "Heavy Rain": {
        "components": {
            "rain": {"intensity": 1.0, "drop_size": 0.8},
            "thunder": {"frequency": 0.05, "boom_duration": 1.0},
            "wind": {"speed": 0.4, "gust_frequency": 0.2}
        },
        "bg_color": "#34495e"
    },
    "Birdsong Meadow": {
        "components": {
            "birds": {"density": 0.9, "pitch_variance": 0.7},
            "wind": {"speed": 0.3, "gust_frequency": 0.1},
            "stream": {"flow_rate": 0.5, "bubbles": 0.4}
        },
        "bg_color": "#27ae60"
    },
    "Ocean Waves": {
        "components": {
            "waves": {"interval": 4.0, "crash_intensity": 0.7},
            "seagulls": {"density": 0.1},
            "wind": {"speed": 0.6, "gust_frequency": 0.3}
        },
        "bg_color": "#2980b9"
    },
    "Starry Night": {
        "components": {
            "crickets": {"density": 0.8, "rhythm": 0.6},
            "wind": {"speed": 0.2, "gust_frequency": 0.05},
            "stars": {"twinkle_frequency": 0.1, "intensity": 0.4}
        },
        "bg_color": "#2c3e50"
    },
    "Quiet Night": {
        "components": {
            "wind": {"speed": 0.1, "gust_frequency": 0.02},
            "owls": {"frequency": 0.03, "pitch": 0.5},
            "rustling_leaves": {"intensity": 0.3}
        },
        "bg_color": "#34495e"
    },
    "Ambient Forest": {
        "components": {
            "wind": {"speed": 0.5, "gust_frequency": 0.2},
            "birds": {"density": 0.4, "pitch_variance": 0.6},
            "water_drips": {"reverb": 0.7, "interval": 0.5}
        },
        "bg_color": "#1e8449"
    },
    "Campfire Night": {
        "components": {
            "campfire": {"crackle_intensity": 0.8, "smoke": 0.5},
            "crickets": {"density": 0.7, "rhythm": 0.6},
            "wind": {"speed": 0.3, "gust_frequency": 0.1}
        },
        "bg_color": "#e67e22"
    },
    "Cozy Fireplace": {
        "components": {
            "fireplace": {"crackle_intensity": 0.9, "embers": 0.6},
            "wind": {"speed": 0.1, "gust_frequency": 0.05},
            "wood_creaks": {"frequency": 0.02, "intensity": 0.4}
        },
        "bg_color": "#d35400"
    }
}

# Advanced sound synthesis functions
def generate_rain(intensity, drop_size, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    rain = np.random.randn(len(t)) * intensity
    drop_pattern = np.random.poisson(20 + 50 * drop_size, len(t))
    rain = np.convolve(rain, drop_pattern, mode='same')
    return 0.5 * rain / np.max(np.abs(rain))

def generate_thunder(frequency, boom_duration, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    thunder = np.zeros(len(t))
    num_booms = int(frequency * duration)
    for _ in range(num_booms):
        start = random.randint(0, len(t) - int(boom_duration * sample_rate))
        boom = np.random.randn(int(boom_duration * sample_rate))
        boom *= np.linspace(1, 0, len(boom))  # Exponential decay
        thunder[start:start+len(boom)] += boom
    return 0.7 * thunder / np.max(np.abs(thunder))

def generate_birds(density, pitch_variance, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    birds = np.zeros(len(t))
    num_calls = int(density * duration * 10)
    for _ in range(num_calls):
        freq = 1000 + 2000 * random.random() * pitch_variance
        duration_call = 0.1 + 0.3 * random.random()
        bird = np.sin(2 * np.pi * freq * t) * np.exp(-5*t/duration_call)
        birds += bird * 0.2
    return birds / np.max(np.abs(birds))

def generate_fire(crackle_intensity, embers, duration, sample_rate=44100):
    t = np.linspace(0, duration, sample_rate * duration)
    crackle = np.random.randn(len(t)) * crackle_intensity
    ember_pattern = np.random.poisson(10 + 20 * embers, len(t))
    fire = np.convolve(crackle, ember_pattern, mode='same')
    return 0.6 * fire / np.max(np.abs(fire))

# Main generation function
def generate_environment(duration_sec, profile):
    sample_rate = 44100
    t = np.linspace(0, duration_sec, sample_rate * duration_sec)
    audio = np.zeros(len(t))
    
    # Component routing
    if "rain" in profile["components"]:
        params = profile["components"]["rain"]
        audio += generate_rain(params["intensity"], params["drop_size"], duration_sec)
    
    if "thunder" in profile["components"]:
        params = profile["components"]["thunder"]
        audio += generate_thunder(params["frequency"], params["boom_duration"], duration_sec)
    
    if "birds" in profile["components"]:
        params = profile["components"]["birds"]
        audio += generate_birds(params["density"], params["pitch_variance"], duration_sec)
    
    if "campfire" in profile["components"]:
        params = profile["components"]["campfire"]
        audio += generate_fire(params["crackle_intensity"], params["smoke"], duration_sec)
    
    # Normalize and convert
    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)
    return audio

# Streamlit UI
st.title("🌍 Ultimate Nature Sound Generator")
st.markdown("Procedurally generated environments with dynamic sound physics")

# Environment selection
selected_env = st.selectbox(
    "Choose Environment",
    options=list(NATURE_SOUNDS.keys()),
    format_func=lambda x: f"{x} {'⛈️' if 'Thunder' in x else '🔥' if 'Fire' in x else '🌊' if 'Ocean' in x else '🌲'}"
)

# Parameter controls
with st.expander("Advanced Sound Parameters"):
    col1, col2 = st.columns(2)
    with col1:
        rain_control = st.slider("Rain Intensity", 0.0, 1.0, 0.5)
        thunder_control = st.slider("Thunder Intensity", 0.0, 1.0, 0.3)
    with col2:
        animal_density = st.slider("Animal Activity", 0.0, 1.0, 0.3)
        fire_intensity = st.slider("Fire Intensity", 0.0, 1.0, 0.0)

# Generate audio
duration = st.slider("Duration (minutes)", 1, 180, 30)
if st.button("Generate Environment"):
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
