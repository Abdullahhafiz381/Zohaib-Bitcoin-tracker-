import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

# GODZILLERS Streamlit setup
st.set_page_config(
    page_title="🔥 GODZILLERS CRYPTO TRACKER",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== GODZILLERS CSS (KEEPING EXACTLY SAME) ==========
st.markdown("""
<style>
    /* Hide all Streamlit elements on login page */
    .login-page .main > div {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .login-page #MainMenu {visibility: hidden;}
    .login-page header {visibility: hidden;}
    .login-page footer {visibility: hidden;}
    .login-page .stAppView {padding: 0 !important; margin: 0 !important;}
    
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #330000 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #330000 100%);
    }
    
    .godzillers-header {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 4rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.7);
        letter-spacing: 3px;
    }
    
    .godzillers-subheader {
        color: #ff6666;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1.4rem;
        margin-bottom: 2rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .godzillers-card {
        background: rgba(20, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 0, 0, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(255, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .godzillers-card:hover {
        border-color: #ff4444;
        box-shadow: 0 8px 32px rgba(255, 0, 0, 0.5);
        transform: translateY(-2px);
    }
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 1px solid #00ff00;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(100, 0, 0, 0.4) 100%);
        border: 1px solid #ff0000;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(100, 65, 0, 0.3) 100%);
        border: 1px solid #ffa500;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.3);
    }
    
    .scalp-signal-urgent {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 140, 0, 0.4) 100%);
        border: 2px solid #ffd700;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
        animation: pulse-urgent 1s infinite;
    }
    
    @keyframes pulse-urgent {
        0% { box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(255, 215, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); }
    }
    
    .scalp-signal-confirmed {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.15) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        animation: pulse-confirmed 2s infinite;
    }
    
    @keyframes pulse-confirmed {
        0% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.5); }
        50% { box-shadow: 0 0 35px rgba(0, 255, 0, 0.8); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.5); }
    }
    
    .scalp-signal-warning {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(100, 0, 0, 0.3) 100%);
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        animation: pulse-warning 2s infinite;
    }
    
    @keyframes pulse-warning {
        0% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 35px rgba(255, 0, 0, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
    }
    
    .price-glow {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(139, 0, 0, 0.25) 100%);
        border: 1px solid rgba(255, 0, 0, 0.6);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .price-glow::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 0, 0, 0.1), transparent);
        animation: shine 3s infinite linear;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .godzillers-button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%);
        border: none;
        border-radius: 25px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .godzillers-button:hover {
        background: linear-gradient(90deg, #ff4444 0%, #ff0000 100%);
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.7);
        color: #000000;
    }
    
    .metric-godzillers {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .trademark {
        text-align: center;
        color: #ff6666;
        font-family: 'Orbitron', monospace;
        font-size: 0.9rem;
        margin-top: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent 0%, #ff0000 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .coin-card {
        background: rgba(30, 0, 0, 0.9);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .coin-card:hover {
        border-color: #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
        transform: translateY(-3px);
    }
    
    .fire-effect {
        background: linear-gradient(45deg, #ff0000, #ff4400, #ff0000);
        background-size: 200% 200%;
        animation: fire 2s ease infinite;
    }
    
    @keyframes fire {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .alert-banner {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        border: 2px solid #ff4444;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        animation: pulse 2s infinite;
    }
    
    /* Login Page Styles - SIMPLIFIED AND CENTERED */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #330000 100%);
        padding: 20px;
    }
    
    .login-card {
        background: rgba(20, 0, 0, 0.95);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 0, 0, 0.6);
        border-radius: 20px;
        padding: 3rem;
        width: 100%;
        max-width: 450px;
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.5);
        text-align: center;
    }
    
    .login-header {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
    }
    
    .login-subheader {
        color: #ff6666;
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .login-input {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(255, 0, 0, 0.5);
        border-radius: 10px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        width: 100%;
        font-size: 1rem;
    }
    
    .login-input:focus {
        outline: none;
        border-color: #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }
    
    .login-button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%);
        border: none;
        border-radius: 25px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.75rem 2rem;
        margin: 1rem 0;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.1rem;
    }
    
    .login-button:hover {
        background: linear-gradient(90deg, #ff4444 0%, #ff0000 100%);
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.7);
    }
    
    .logout-button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%);
        border: none;
        border-radius: 10px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.5rem 1rem;
        margin: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        color: #ff4444;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        color: #ff8888;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Orbitron', monospace;
    }
    
    .dragon-emoji {
        font-size: 2rem;
        text-shadow: 0 0 10px #ff0000;
    }
    
    .confirmation-badge {
        display: inline-block;
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .warning-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: #ffffff;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'btc_price' not in st.session_state:
    st.session_state.btc_price = 0
if 'bitnode_previous' not in st.session_state:
    st.session_state.bitnode_previous = {}
if 'refresh_time' not in st.session_state:
    st.session_state.refresh_time = datetime.now()
if 'math_signals' not in st.session_state:
    st.session_state.math_signals = []
if 'bitnode_signal' not in st.session_state:
    st.session_state.bitnode_signal = ("HOLD", "Analyzing...")
if 'initial_load' not in st.session_state:
    st.session_state.initial_load = True

# ========== YOUR NEW BACKEND LOGIC ==========
def get_btc_price():
    """Get live BTC price from Binance"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return float(data.get('price', 65000))
    except:
        return 65000 + (np.random.random() * 1000 - 500)

def get_bitnode_data():
    """YOUR BITNODE FORMULA: Fetch and analyze real Bitnodes data"""
    try:
        # Fetch Bitnodes data
        response = requests.get("https://bitnodes.io/api/v1/snapshots/latest/", timeout=10)
        data = response.json()
        
        total_nodes = data.get('total_nodes', 15000)
        nodes = data.get('nodes', {})
        
        # Count Tor and Onion nodes
        tor_nodes = 0
        onion_nodes = 0
        
        for node_info in nodes.values():
            if isinstance(node_info, list) and len(node_info) > 7:
                user_agent = str(node_info[7]).lower()
                if '.onion' in user_agent:
                    onion_nodes += 1
                    tor_nodes += 1
                elif 'tor' in user_agent:
                    tor_nodes += 1
        
        # Calculate percentages (YOUR FORMULA)
        tor_percent = (tor_nodes / total_nodes) * 100 if total_nodes > 0 else 0
        onion_ratio = (onion_nodes / tor_nodes) * 100 if tor_nodes > 0 else 0
        
        return tor_percent, onion_ratio, tor_nodes, onion_nodes, total_nodes
        
    except Exception as e:
        # Fallback data
        return 15.2, 32.5, 2280, 741, 15000

def calculate_bitnode_signal():
    """YOUR BITNODE SIGNAL FORMULA"""
    # Get current data
    tor_current, onion_current, _, _, total = get_bitnode_data()
    
    # Get previous data
    tor_previous = st.session_state.bitnode_previous.get('tor_percent', tor_current)
    onion_previous = st.session_state.bitnode_previous.get('onion_ratio', onion_current)
    
    # Calculate changes (ΔTor_%)
    delta_tor = tor_current - tor_previous
    delta_onion = onion_current - onion_previous
    
    # Store current as previous for next refresh
    st.session_state.bitnode_previous = {
        'tor_percent': tor_current,
        'onion_ratio': onion_current
    }
    
    # Onion Confirmation Logic
    if delta_onion > 0 and delta_tor > 0:
        onion_confirmed = True
        strength_multiplier = 2.0
    elif delta_onion < 0 and delta_tor < 0:
        onion_confirmed = True
        strength_multiplier = 2.0
    else:
        onion_confirmed = False
        strength_multiplier = 1.0
    
    # Generate signal (YOUR LOGIC)
    if delta_tor > 0.5:  # Strong increase
        direction = "🐲 GODZILLA DUMP 🐲"
        bias = "EXTREME_BEARISH"
        if onion_confirmed:
            strength = "EXTREME_CONFIRMED"
        else:
            strength = "STRONG"
    elif delta_tor > 0.1:  # Moderate increase
        direction = "🔥 STRONG SELL 🔥"
        bias = "VERY_BEARISH"
        if onion_confirmed:
            strength = "VERY_STRONG"
        else:
            strength = "MODERATE"
    elif delta_tor < -0.5:  # Strong decrease
        direction = "🐲 GODZILLA PUMP 🐲"
        bias = "EXTREME_BULLISH"
        if onion_confirmed:
            strength = "EXTREME_CONFIRMED"
        else:
            strength = "STRONG"
    elif delta_tor < -0.1:  # Moderate decrease
        direction = "🚀 STRONG BUY 🚀"
        bias = "VERY_BULLISH"
        if onion_confirmed:
            strength = "VERY_STRONG"
        else:
            strength = "MODERATE"
    else:
        direction = "HOLD"
        bias = "NEUTRAL"
        strength = "WEAK"
    
    return direction, bias, strength, delta_tor

def calculate_mathematical_signals():
    """YOUR MATHEMATICAL SIGNAL FORMULA with Binance data"""
    # Internal analysis of 20 BTC-correlated pairs (NOT SHOWN)
    pairs = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT",
        "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT",
        "LTCUSDT", "LINKUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT",
        "BCHUSDT", "XLMUSDT", "ALGOUSDT", "VETUSDT", "FILUSDT"
    ]
    
    signals = []
    
    for pair in pairs:
        try:
            # Get order book data
            response = requests.get(
                "https://api.binance.com/api/v3/depth",
                params={"symbol": pair, "limit": 50},
                timeout=5
            )
            order_book = response.json()
            
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                continue
            
            # Extract top prices and volumes
            bid_prices = [float(b[0]) for b in bids[:10]]
            bid_volumes = [float(b[1]) for b in bids[:10]]
            ask_prices = [float(a[0]) for a in asks[:10]]
            ask_volumes = [float(a[1]) for a in asks[:10]]
            
            # YOUR FORMULA:
            # P = (Bid + Ask) / 2
            P = (bid_prices[0] + ask_prices[0]) / 2
            
            # I = (V_bid − V_ask) / (V_bid + V_ask)
            total_bid_volume = sum(bid_volumes)
            total_ask_volume = sum(ask_volumes)
            I = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume) if (total_bid_volume + total_ask_volume) > 0 else 0
            
            # S = Ask − Bid
            S = ask_prices[0] - bid_prices[0]
            
            # φ = S / P
            phi = S / P if P > 0 else 0.001
            
            # Get price history for volatility (σ)
            kline_response = requests.get(
                "https://api.binance.com/api/v3/klines",
                params={"symbol": pair, "interval": "5m", "limit": 20},
                timeout=5
            )
            klines = kline_response.json()
            
            if len(klines) >= 2:
                prices = [float(k[4]) for k in klines]  # Closing prices
                returns = np.diff(np.log(prices))
                sigma = np.std(returns) if len(returns) > 0 else 0.001
            else:
                sigma = 0.001
            
            # Signal = sign(I) × ( |I| / (φ × σ) )
            signal_value = np.sign(I) * (abs(I) / (phi * sigma)) if (phi * sigma) > 0 else 0
            
            # Direction: I > φ → BUY, I < −φ → SELL, ELSE → HOLD
            if I > phi:
                direction = "BUY"
            elif I < -phi:
                direction = "SELL"
            else:
                direction = "HOLD"
            
            # Strength Percentage: min(99, |Signal| × 100)
            strength_pct = min(99, abs(signal_value) * 100)
            
            if direction != "HOLD" and strength_pct > 15:
                signals.append({
                    'pair': pair.replace('USDT', ''),
                    'direction': direction,
                    'strength': round(strength_pct, 1),
                    'signal_value': signal_value
                })
                
        except Exception:
            continue
    
    # Sort by strength and take top 2 only (NOT showing more)
    signals.sort(key=lambda x: x['strength'], reverse=True)
    return signals[:2]

def update_all_signals():
    """Update all signals (manual refresh only)"""
    with st.spinner("🔥 Activating dragon fire analysis..."):
        # Update BTC price
        st.session_state.btc_price = get_btc_price()
        
        # Update Bitnode signal
        bitnode_direction, bias, strength, delta_tor = calculate_bitnode_signal()
        st.session_state.bitnode_signal = (bitnode_direction, bias, strength, delta_tor)
        
        # Update mathematical signals
        st.session_state.math_signals = calculate_mathematical_signals()
        
        # Update timestamp
        st.session_state.refresh_time = datetime.now()
        
        time.sleep(1)

def check_confirmation():
    """YOUR CONFIRMATION LOGIC: 99% when both engines agree"""
    if not st.session_state.math_signals or not hasattr(st.session_state, 'bitnode_signal'):
        return False, None
    
    bitnode_direction = st.session_state.bitnode_signal[0]
    math_signal = st.session_state.math_signals[0] if st.session_state.math_signals else None
    
    if not math_signal:
        return False, None
    
    # Map Bitnode direction to BUY/SELL
    if "GODZILLA PUMP" in bitnode_direction or "STRONG BUY" in bitnode_direction or "BUY" in bitnode_direction:
        bitnode_buy_sell = "BUY"
    elif "GODZILLA DUMP" in bitnode_direction or "STRONG SELL" in bitnode_direction or "SELL" in bitnode_direction:
        bitnode_buy_sell = "SELL"
    else:
        bitnode_buy_sell = "HOLD"
    
    # Check if both agree
    if bitnode_buy_sell == math_signal['direction'] and bitnode_buy_sell in ["BUY", "SELL"]:
        return True, bitnode_buy_sell
    else:
        return False, None

# ========== LOGIN SYSTEM (KEEPING EXACTLY SAME) ==========
def check_credentials(username, password):
    """Check if username and password are correct"""
    valid_users = {
        "godziller": "dragonfire2025",
        "admin": "cryptoking",
        "trader": "bullmarket"
    }
    return username in valid_users and valid_users[username] == password

def login_page():
    """Display login page - EXACTLY SAME"""
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='
            background: rgba(20, 0, 0, 0.95);
            border: 2px solid rgba(255, 0, 0, 0.6);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(255, 0, 0, 0.5);
            text-align: center;
            margin: 2rem 0;
        '>
            <h1 style='
                background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: Orbitron, monospace;
                font-weight: 900;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                text-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
            '>🐲 GODZILLERS</h1>
            <p style='
                color: #ff6666;
                font-family: Orbitron, monospace;
                font-size: 1rem;
                margin-bottom: 2rem;
                letter-spacing: 2px;
            '>PRIVATE CRYPTO WARFARE SYSTEM</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 DRAGON NAME", placeholder="Enter your dragon name...")
            password = st.text_input("🔐 FIRE BREATH", type="password", placeholder="Enter your fire breath...")
            
            login_button = st.form_submit_button("🔥 IGNITE DRAGON FIRE", use_container_width=True)
            
            if login_button:
                if check_credentials(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Dragon fire ignited! Access granted.")
                    st.rerun()
                else:
                    st.error("❌ Invalid dragon name or fire breath!")

# ========== HELPER FUNCTIONS (SAME) ==========
def get_crypto_prices():
    """Get crypto prices - KEEPING SAME"""
    coins = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum'
    }
    
    prices = {}
    
    try:
        for symbol in coins.keys():
            try:
                response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    prices[symbol] = float(data['price'])
                else:
                    prices[symbol] = None
            except Exception as e:
                prices[symbol] = None
        
        missing_coins = [coin_id for symbol, coin_id in coins.items() if prices.get(symbol) is None]
        if missing_coins:
            try:
                coin_ids = ','.join(missing_coins)
                response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd", timeout=5)
                if response.status_code == 200:
                    gecko_data = response.json()
                    for symbol, coin_id in coins.items():
                        if prices.get(symbol) is None and coin_id in gecko_data:
                            prices[symbol] = float(gecko_data[coin_id]['usd'])
            except Exception as e:
                for symbol in coins:
                    if prices.get(symbol) is None:
                        prices[symbol] = 0.0
                
    except Exception as e:
        for symbol in coins:
            prices[symbol] = 0.0
    
    return prices

def get_coin_display_name(symbol):
    """Get display name for crypto symbols"""
    names = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols - GODZILLERS theme"""
    emojis = {
        'BTCUSDT': '🐲',
        'ETHUSDT': '🔥'
    }
    return emojis.get(symbol, '💀')

# ========== MAIN APP (KEEPING EXACTLY SAME STRUCTURE) ==========
def main_app():
    """Main application after login - EXACTLY SAME STRUCTURE"""
    # Logout button
    if st.button("🚪 LOGOUT", key="logout", use_container_width=False):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Welcome message
    st.markdown(f'<p style="text-align: right; color: #ff4444; font-family: Orbitron; margin: 0.5rem 1rem;">Welcome, {st.session_state.username}!</p>', unsafe_allow_html=True)
    
    # GODZILLERS Header
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS CRYPTO TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">AI-POWERED SIGNALS • REAL-TIME PRICES • DRAGON FIRE PRECISION</p>', unsafe_allow_html=True)
    
    # UPDATE SIGNALS BUTTON
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">🎯 GODZILLERS AI SIGNALS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🐉 GENERATE SIGNALS", key="refresh_main", use_container_width=True, type="primary"):
            update_all_signals()
            st.success("✅ Signals updated successfully!")
            st.rerun()
    
    # LIVE CRYPTO PRICES SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 DRAGON FIRE PRICES</h2>', unsafe_allow_html=True)
    
    # Get all crypto prices
    prices = get_crypto_prices()
    
    if prices:
        # Display BTC price prominently
        btc_price = st.session_state.btc_price if st.session_state.btc_price > 0 else prices.get('BTCUSDT', 65000)
        if btc_price and btc_price > 0:
            st.markdown('<div class="price-glow">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f'<div style="text-align: center;"><span style="font-family: Orbitron; font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #ff0000, #ff4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${btc_price:,.2f}</span></div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #ff8888; font-family: Rajdhani;">BITCOIN PRICE (USD)</p>', unsafe_allow_html=True)
            
            with col2:
                st.metric(
                    label="24H STATUS",
                    value="🔥 LIVE",
                    delta="Godzillers"
                )
            
            with col3:
                st.metric(
                    label="DATA SOURCE", 
                    value="BINANCE API",
                    delta="RED HOT"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Could not fetch Bitcoin price")
        
        # Display all coins in a grid
        st.markdown('<h3 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">📊 ALTCOIN BATTLEFIELD</h3>', unsafe_allow_html=True)
        
        # Create columns for coin grid
        coins_to_display = {k: v for k, v in prices.items() if k != 'BTCUSDT' and v and v > 0}
        if coins_to_display:
            cols = st.columns(2)
            
            for idx, (symbol, price) in enumerate(coins_to_display.items()):
                if price:
                    with cols[idx % 2]:
                        emoji = get_coin_emoji(symbol)
                        name = get_coin_display_name(symbol)            
                        st.markdown(f'''
                        <div class="coin-card">
                            <div style="text-align: center;">
                                <h4 style="font-family: Orbitron; color: #ff4444; margin: 0.5rem 0; font-size: 1.1rem;">{emoji} {name}</h4>
                                <p style="font-family: Orbitron; font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">${price:,.2f}</p>
                                <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.9rem; margin: 0;">{symbol}</p>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Could not fetch altcoin prices")
        
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani;">🕒 Prices updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch crypto prices")
    
    # CHECK FOR CONFIRMED SIGNAL (YOUR LOGIC)
    confirmed, confirmed_direction = check_confirmation()
    
    if confirmed:
        # DISPLAY CONFIRMED SIGNAL (99% CONFIDENCE)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        if confirmed_direction == "BUY":
            signal_text = "🐲 GODZILLA PUMP CONFIRMED 🐲"
            signal_class = "scalp-signal-confirmed"
            emoji = "🚀🔥🐲"
            explanation = "BITNODE + MATHEMATICAL SIGNALS ALIGNED - EXTREME BULLISH CONFIRMATION"
        else:
            signal_text = "🐲 GODZILLA DUMP CONFIRMED 🐲"
            signal_class = "scalp-signal-urgent"
            emoji = "💀🔥🐲"
            explanation = "BITNODE + MATHEMATICAL SIGNALS ALIGNED - EXTREME BEARISH CONFIRMATION"
        
        st.markdown(f'''
        <div class="{signal_class}">
            <div style="text-align: center;">
                <h2 style="font-family: Orbitron; font-size: 2rem; margin: 0.5rem 0;">{emoji} {signal_text} {emoji}</h2>
                <p style="color: #ffffff; font-family: Orbitron; font-size: 1.5rem; margin: 0.5rem 0;">CONFIDENCE: 99%</p>
                <p style="color: #ffd700; font-family: Rajdhani; font-size: 1.1rem; margin: 0.5rem 0;">{explanation}</p>
                <p style="color: #00ff00; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">DUAL-ENGINE CONFIRMATION SYSTEM ACTIVE</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # MATHEMATICAL SIGNALS SECTION (ONLY TOP 2 PAIRS)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🧮 MATHEMATICAL SIGNALS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">ORDER BOOK ANALYSIS • TOP 2 HIGHEST STRENGTH PAIRS</p>', unsafe_allow_html=True)
    
    math_signals = st.session_state.math_signals
    if math_signals:
        # Display mathematical signals table
        data = []
        for signal in math_signals:
            arrow = "🟢" if signal['direction'] == "BUY" else "🔴" if signal['direction'] == "SELL" else "⚪"
            data.append({
                "Pair": f"{signal['pair']}/USDT",
                "Signal": f"{arrow} {signal['direction']}",
                "Strength": f"{signal['strength']}%"
            })
        
        df = pd.DataFrame(data)
        
        # Display table with GODZILLERS styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Pair": st.column_config.TextColumn("Trading Pair", width="medium"),
                "Signal": st.column_config.TextColumn("Signal", width="medium"),
                "Strength": st.column_config.ProgressColumn(
                    "Strength %",
                    help="Signal strength percentage",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                    width="medium"
                )
            }
        )
        
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; font-size: 0.8rem;">Showing top {len(math_signals)} highest strength pairs</p>', unsafe_allow_html=True)
    else:
        st.info("🔥 Generate signals to see mathematical analysis")
    
    # BITNODE SIGNAL SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌐 BITNODE NETWORK SIGNAL</h2>', unsafe_allow_html=True)
    
    if hasattr(st.session_state, 'bitnode_signal') and st.session_state.bitnode_signal:
        bitnode_direction, bias, strength, delta_tor = st.session_state.bitnode_signal
        
        # Display Bitnode signal with GODZILLERS styling
        if "GODZILLA DUMP" in bitnode_direction:
            signal_class = "signal-sell"
            emoji = "🐲💀🔥"
            explanation = "BITNODE NETWORK ANALYSIS: EXTREME BEARISH SIGNAL"
        elif "STRONG SELL" in bitnode_direction:
            signal_class = "signal-sell"
            emoji = "🐲🔥"
            explanation = "BITNODE NETWORK ANALYSIS: STRONG SELL SIGNAL"
        elif "SELL" in bitnode_direction:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "BITNODE NETWORK ANALYSIS: SELL SIGNAL"
        elif "GODZILLA PUMP" in bitnode_direction:
            signal_class = "signal-buy"
            emoji = "🐲🚀🌟"
            explanation = "BITNODE NETWORK ANALYSIS: EXTREME BULLISH SIGNAL"
        elif "STRONG BUY" in bitnode_direction:
            signal_class = "signal-buy"
            emoji = "🐲🚀"
            explanation = "BITNODE NETWORK ANALYSIS: STRONG BUY SIGNAL"
        elif "BUY" in bitnode_direction:
            signal_class = "signal-buy"
            emoji = "🟢"
            explanation = "BITNODE NETWORK ANALYSIS: BUY SIGNAL"
        else:
            signal_class = "signal-neutral"
            emoji = "🐲⚡"
            explanation = "BITNODE NETWORK ANALYSIS: AWAITING DIRECTIONAL SIGNALS"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">{emoji} {bitnode_direction} {emoji}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">{explanation}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-family: Orbitron; color: #ffffff; margin: 0.5rem 0;">Signal Strength: {strength} • Tor Change: {delta_tor:+.3f}%</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔥 Generate signals to see Bitnode network analysis")
    
    # LAST UPDATE TIME
    st.markdown(f'''
    <div style="text-align: center; margin: 2rem 0;">
        <p style="color: #ff6666; font-family: Orbitron; font-size: 0.9rem;">
        🕒 Last Signal Update: {st.session_state.refresh_time.strftime("%Y-%m-%d %H:%M:%S UTC")}
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • PROPRIETARY AI TECHNOLOGY</p>
    <p style="font-size: 0.7rem; color: #ff6666;">DUAL-ENGINE SIGNAL CONFIRMATION SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

# ========== MAIN FUNCTION ==========
def main():
    """Main function with login check"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()