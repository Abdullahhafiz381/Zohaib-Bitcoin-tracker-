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

# GODZILLERS CSS with red and black theme - UPDATED FOR BETTER LOGIN
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

# Simple authentication system
def check_credentials(username, password):
    """Check if username and password are correct"""
    # In a real application, use proper password hashing and secure storage
    valid_users = {
        "godziller": "dragonfire2025",
        "admin": "cryptoking",
        "trader": "bullmarket"
    }
    return username in valid_users and valid_users[username] == password

def login_page():
    """Display login page - SIMPLIFIED VERSION"""
    # Clear any existing content
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create centered login form directly
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

def get_crypto_prices():
    """Get crypto prices from multiple sources with fallback"""
    coins = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum'
    }
    
    prices = {}
    
    try:
        # Try Binance first for all coins
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
        
        # Fill missing prices with CoinGecko
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
                # If CoinGecko fails, set default prices
                for symbol in coins:
                    if prices.get(symbol) is None:
                        prices[symbol] = 0.0
                
    except Exception as e:
        st.error(f"Error fetching prices: {str(e)}")
        # Set default prices if everything fails
        for symbol in coins:
            prices[symbol] = 0.0
    
    return prices

class EMAScalpingAnalyzer:
    def __init__(self):
        self.ema_fast = 9
        self.ema_slow = 21
        self.ema_signal = 50
        self.price_history = {}
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        
        alpha = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = price * alpha + ema * (1 - alpha)
        
        return ema
    
    def get_historical_data(self, symbol, limit=100):
        """Get historical price data for EMA calculation"""
        try:
            # Using Binance API for historical data
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                closes = [float(candle[4]) for candle in data]  # Close prices
                return closes
            else:
                return None
        except Exception as e:
            return None
    
    def generate_scalp_signal(self, symbol, current_price):
        """Generate 1-minute scalp signal based on EMA crossover"""
        try:
            # Get historical data
            historical_data = self.get_historical_data(symbol, 100)
            
            if not historical_data or len(historical_data) < self.ema_signal:
                return {
                    'signal': 'NO_DATA',
                    'strength': 'NEUTRAL',
                    'fast_ema': 0,
                    'slow_ema': 0,
                    'signal_ema': 0,
                    'trend': 'SIDEWAYS',
                    'crossover_strength': 0
                }
            
            # Get historical data
            historical_data = self.get_historical_data(symbol, 100)
            
            if not historical_data or len(historical_data) < self.ema_signal:
                return {
                    'signal': 'NO_DATA',
                    'strength': 'NEUTRAL',
                    'fast_ema': 0,
                    'slow_ema': 0,
                    'signal_ema': 0,
                    'trend': 'SIDEWAYS',
                    'crossover_strength': 0
                }
            
            # Calculate EMAs
            fast_ema = self.calculate_ema(historical_data[-self.ema_fast:], self.ema_fast)
            slow_ema = self.calculate_ema(historical_data[-self.ema_slow:], self.ema_slow)
            signal_ema = self.calculate_ema(historical_data[-self.ema_signal:], self.ema_signal)
            
            if not all([fast_ema, slow_ema, signal_ema]):
                return {
                    'signal': 'NO_DATA',
                    'strength': 'NEUTRAL',
                    'fast_ema': 0,
                    'slow_ema': 0,
                    'signal_ema': 0,
                    'trend': 'SIDEWAYS',
                    'crossover_strength': 0
                }
            
            # Calculate crossover strength
            crossover_strength = abs(fast_ema - slow_ema) / slow_ema * 100
            
            # Determine trend based on signal EMA
            if current_price > signal_ema * 1.002:  # 0.2% above signal EMA
                trend = "STRONG_BULLISH"
            elif current_price > signal_ema:
                trend = "BULLISH"
            elif current_price < signal_ema * 0.998:  # 0.2% below signal EMA
                trend = "STRONG_BEARISH"
            elif current_price < signal_ema:
                trend = "BEARISH"
            else:
                trend = "SIDEWAYS"
            
            # Generate scalp signal with strength
            if fast_ema > slow_ema and trend in ["BULLISH", "STRONG_BULLISH"]:
                signal = "SCALP_LONG"
                if crossover_strength > 0.15 and trend == "STRONG_BULLISH":
                    strength = "VERY_STRONG"
                elif crossover_strength > 0.08:
                    strength = "STRONG"
                else:
                    strength = "MODERATE"
            elif fast_ema < slow_ema and trend in ["BEARISH", "STRONG_BEARISH"]:
                signal = "SCALP_SHORT"
                if crossover_strength > 0.15 and trend == "STRONG_BEARISH":
                    strength = "VERY_STRONG"
                elif crossover_strength > 0.08:
                    strength = "STRONG"
                else:
                    strength = "MODERATE"
            else:
                signal = "NO_SCALP"
                strength = "NEUTRAL"
            
            return {
                'signal': signal,
                'strength': strength,
                'fast_ema': fast_ema,
                'slow_ema': slow_ema,
                'signal_ema': signal_ema,
                'trend': trend,
                'price_vs_fast': current_price - fast_ema,
                'crossover_strength': crossover_strength
            }
            
        except Exception as e:
            return {
                'signal': 'ERROR',
                'strength': 'NEUTRAL',
                'fast_ema': 0,
                'slow_ema': 0,
                'signal_ema': 0,
                'trend': 'SIDEWAYS',
                'crossover_strength': 0
            }

class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.scalp_analyzer = EMAScalpingAnalyzer()
        self.load_node_data()
    
    def load_node_data(self):
        """Load only current and previous node data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.current_data = data.get('current_data')
                    self.previous_data = data.get('previous_data')
                    self.last_snapshot_check = data.get('last_snapshot_check')
            else:
                self.current_data = None
                self.previous_data = None
                self.last_snapshot_check = None
        except Exception as e:
            self.current_data = None
            self.previous_data = None
            self.last_snapshot_check = None
    
    def save_node_data(self):
        """Save current and previous node data"""
        try:
            data = {
                'current_data': self.current_data,
                'previous_data': self.previous_data,
                'last_snapshot_check': self.last_snapshot_check,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def fetch_node_data(self):
        """Fetch current node data from Bitnodes API"""
        try:
            response = requests.get(self.bitnodes_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_nodes = data['total_nodes']
                
                # Count active nodes (nodes that responded)
                active_nodes = 0
                tor_nodes = 0
                
                for node_address, node_info in data['nodes'].items():
                    # Check if node is active (has response data)
                    if node_info and isinstance(node_info, list) and len(node_info) > 0:
                        active_nodes += 1
                    
                    # Count Tor nodes
                    if '.onion' in str(node_address) or '.onion' in str(node_info):
                        tor_nodes += 1
                
                tor_percentage = (tor_nodes / total_nodes) * 100 if total_nodes > 0 else 0
                active_ratio = active_nodes / total_nodes if total_nodes > 0 else 0
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_nodes': total_nodes,
                    'active_nodes': active_nodes,
                    'tor_nodes': tor_nodes,
                    'tor_percentage': tor_percentage,
                    'active_ratio': active_ratio
                }
            else:
                st.error(f"API returned status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching node data: {e}")
            return None
    
    def update_node_data(self):
        """Fetch new data and shift current to previous"""
        new_data = self.fetch_node_data()
        if not new_data:
            return False
        
        # Update snapshot check time
        self.last_snapshot_check = datetime.now().isoformat()
        
        # Shift current to previous, set new data as current
        self.previous_data = self.current_data
        self.current_data = new_data
        
        self.save_node_data()
        return True
    
    def calculate_tor_signal(self):
        """Calculate signal based on Tor percentage changes - HIDDEN ANALYSIS"""
        if not self.current_data or not self.previous_data:
            return {
                'signal': "🔄 NEED DATA",
                'bias': "UPDATE_REQUIRED",
                'strength': "NEUTRAL",
                'tor_change': 0,
                'momentum': 0
            }
        
        current_tor_pct = self.current_data['tor_percentage']
        previous_tor_pct = self.previous_data['tor_percentage']
        
        # Calculate percentage change in Tor nodes
        tor_pct_change = current_tor_pct - previous_tor_pct
        
        # Calculate momentum (rate of change)
        tor_momentum = tor_pct_change * 100  # Amplify for scoring
        
        # TOR PERCENTAGE SIGNAL LOGIC (HIDDEN FROM USER)
        if tor_pct_change >= 1.0:  # Tor percentage increased by 1.0% or more
            signal = "🐲 GODZILLA DUMP 🐲"
            bias = "EXTREME_BEARISH"
            strength = "EXTREME"
        elif tor_pct_change >= 0.5:  # Tor percentage increased by 0.5-0.99%
            signal = "🔥 STRONG SELL 🔥"
            bias = "VERY_BEARISH"
            strength = "STRONG"
        elif tor_pct_change >= 0.1:  # Tor percentage increased by 0.1-0.49%
            signal = "SELL"
            bias = "BEARISH"
            strength = "MODERATE"
        elif tor_pct_change <= -1.0:  # Tor percentage decreased by 1.0% or more
            signal = "🐲 GODZILLA PUMP 🐲"
            bias = "EXTREME_BULLISH"
            strength = "EXTREME"
        elif tor_pct_change <= -0.5:  # Tor percentage decreased by 0.5-0.99%
            signal = "🚀 STRONG BUY 🚀"
            bias = "VERY_BULLISH"
            strength = "STRONG"
        elif tor_pct_change <= -0.1:  # Tor percentage decreased by 0.1-0.49%
            signal = "BUY"
            bias = "BULLISH"
            strength = "MODERATE"
        else:  # Change between -0.1% and +0.1%
            signal = "HOLD"
            bias = "NEUTRAL"
            strength = "WEAK"
        
        return {
            'signal': signal,
            'bias': bias,
            'strength': strength,
            'tor_change': tor_pct_change,
            'momentum': tor_momentum
        }
    
    def calculate_confirmation_score(self, ema_signal, tor_signal):
        """Calculate confirmation score between EMA and Bitnodes signals"""
        score = 0
        confirmations = []
        
        # EMA Signal Analysis
        if ema_signal['signal'] == 'SCALP_LONG':
            score += 25
            confirmations.append("EMA Bullish")
        elif ema_signal['signal'] == 'SCALP_SHORT':
            score += 25
            confirmations.append("EMA Bearish")
        
        # EMA Strength Bonus
        if ema_signal['strength'] == 'VERY_STRONG':
            score += 20
            confirmations.append("Very Strong EMA")
        elif ema_signal['strength'] == 'STRONG':
            score += 15
            confirmations.append("Strong EMA")
        elif ema_signal['strength'] == 'MODERATE':
            score += 10
            confirmations.append("Moderate EMA")
        
        # Bitnodes Signal Analysis
        if 'BULLISH' in tor_signal['bias'] and ema_signal['signal'] == 'SCALP_LONG':
            score += 30
            confirmations.append("Bitnodes Confirmed")
        elif 'BEARISH' in tor_signal['bias'] and ema_signal['signal'] == 'SCALP_SHORT':
            score += 30
            confirmations.append("Bitnodes Confirmed")
        elif tor_signal['bias'] == 'NEUTRAL':
            score += 10
            confirmations.append("Bitnodes Neutral")
        else:
            score -= 20
            confirmations.append("Bitnodes Conflict!")
        
        # Trend Alignment Bonus
        if (ema_signal['trend'] in ['STRONG_BULLISH', 'BULLISH'] and 
            'BULLISH' in tor_signal['bias']):
            score += 15
            confirmations.append("Trend Aligned")
        elif (ema_signal['trend'] in ['STRONG_BEARISH', 'BEARISH'] and 
              'BEARISH' in tor_signal['bias']):
            score += 15
            confirmations.append("Trend Aligned")
        
        return min(100, max(0, score)), confirmations
    
    def generate_composite_scalp_signal(self, symbol, current_price):
        """Generate combined EMA + Bitnodes scalp signal with confirmation scoring"""
        # Get individual signals
        ema_signal = self.scalp_analyzer.generate_scalp_signal(symbol, current_price)
        tor_signal = self.calculate_tor_signal()
        
        # Calculate confirmation score
        confirmation_score, confirmations = self.calculate_confirmation_score(ema_signal, tor_signal)
        
        # Determine composite signal based on score and alignment
        if confirmation_score >= 80:
            if ema_signal['signal'] == 'SCALP_LONG':
                composite_signal = "🚨 CONFIRMED LONG"
                signal_class = "scalp-signal-confirmed"
                urgency = "EXTREME"
            else:
                composite_signal = "🚨 CONFIRMED SHORT"
                signal_class = "scalp-signal-confirmed"
                urgency = "EXTREME"
        elif confirmation_score >= 60:
            if ema_signal['signal'] == 'SCALP_LONG':
                composite_signal = "🔥 STRONG LONG"
                signal_class = "scalp-signal-urgent"
                urgency = "HIGH"
            else:
                composite_signal = "🔥 STRONG SHORT"
                signal_class = "scalp-signal-urgent"
                urgency = "HIGH"
        elif confirmation_score >= 40:
            if ema_signal['signal'] == 'SCALP_LONG':
                composite_signal = "🟢 SCALP LONG"
                signal_class = "signal-buy"
                urgency = "MEDIUM"
            else:
                composite_signal = "🔴 SCALP SHORT"
                signal_class = "signal-sell"
                urgency = "MEDIUM"
        else:
            if ema_signal['signal'] != 'NO_SCALP' and confirmation_score < 30:
                composite_signal = "⚠️ CONFLICT SIGNAL"
                signal_class = "scalp-signal-warning"
                urgency = "LOW"
            else:
                composite_signal = "⚡ NO SCALP"
                signal_class = "signal-neutral"
                urgency = "LOW"
        
        return {
            'composite_signal': composite_signal,
            'signal_class': signal_class,
            'urgency': urgency,
            'confirmation_score': confirmation_score,
            'confirmations': confirmations,
            'ema_signal': ema_signal['signal'],
            'ema_strength': ema_signal['strength'],
            'tor_bias': tor_signal['bias'],
            'tor_strength': tor_signal['strength'],
            'trend': ema_signal['trend'],
            'fast_ema': ema_signal['fast_ema'],
            'slow_ema': ema_signal['slow_ema'],
            'crossover_strength': ema_signal['crossover_strength'],
            'reasoning': self.generate_reasoning(ema_signal, tor_signal, confirmations)
        }
    
    def generate_reasoning(self, ema_signal, tor_signal, confirmations):
        """Generate detailed reasoning for the signal"""
        reasoning = []
        
        # EMA Analysis
        if ema_signal['signal'] == 'SCALP_LONG':
            reasoning.append(f"EMA Bullish Crossover (Strength: {ema_signal['crossover_strength']:.3f}%)")
        elif ema_signal['signal'] == 'SCALP_SHORT':
            reasoning.append(f"EMA Bearish Crossover (Strength: {ema_signal['crossover_strength']:.3f}%)")
        
        # Trend Analysis
        reasoning.append(f"Trend: {ema_signal['trend']}")
        
        # Bitnodes Analysis
        reasoning.append(f"Bitnodes: {tor_signal['bias']} ({tor_signal['strength']})")
        
        # Add confirmations
        reasoning.extend(confirmations)
        
        return " • ".join(reasoning)

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

def main_app():
    """Main application after login"""
    # Initialize analyzer
    analyzer = CryptoAnalyzer()
    
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
            with st.spinner("🔥 Activating dragon fire analysis..."):
                if analyzer.update_node_data():
                    st.success("✅ Signals updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update signals")
    
    # LIVE CRYPTO PRICES SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 DRAGON FIRE PRICES</h2>', unsafe_allow_html=True)
    
    # Get all crypto prices
    prices = get_crypto_prices()
    
    if prices:
        # Display BTC price prominently
        btc_price = prices.get('BTCUSDT')
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
            # Use 2 columns for cleaner layout with fewer coins
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
    
    # ENHANCED EMA SCALPING SECTION WITH CONFIRMATION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">⚡ DRAGON SCALPING SIGNALS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">EMA + BITNODES CONFIRMATION SYSTEM • 1-MINUTE TIMEFRAME</p>', unsafe_allow_html=True)
    
    if analyzer.current_data and analyzer.previous_data and prices:
        # Display scalp signals for each coin
        scalp_cols = st.columns(2)
        
        for idx, symbol in enumerate(['BTCUSDT', 'ETHUSDT']):
            if prices.get(symbol):
                with scalp_cols[idx % 2]:
                    current_price = prices[symbol]
                    composite_signal = analyzer.generate_composite_scalp_signal(symbol, current_price)
                    
                    emoji = get_coin_emoji(symbol)
                    name = get_coin_display_name(symbol)
                    
                    # Display main signal card
                    st.markdown(f'''
                    <div class="{composite_signal['signal_class']}">
                        <div style="text-align: center;">
                            <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.3rem;">{emoji} {name}</h3>
                            <p style="font-family: Orbitron; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">{composite_signal['composite_signal']}</p>
                            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.1rem; margin: 0.2rem 0;">CONFIRMATION: {composite_signal['confirmation_score']}%</p>
                            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.9rem; margin: 0.2rem 0;">Urgency: {composite_signal['urgency']}</p>
                            <p style="color: #ffffff; font-family: Rajdhani; font-size: 0.8rem; margin: 0.2rem 0;">{composite_signal['reasoning']}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Display confirmation badges
                    st.markdown('<div style="text-align: center; margin: 0.5rem 0;">', unsafe_allow_html=True)
                    for confirmation in composite_signal['confirmations']:
                        if "Confirmed" in confirmation or "Aligned" in confirmation:
                            st.markdown(f'<span class="confirmation-badge">✓ {confirmation}</span>', unsafe_allow_html=True)
                        elif "Conflict" in confirmation:
                            st.markdown(f'<span class="warning-badge">⚠ {confirmation}</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<span style="display: inline-block; background: #444; color: #fff; padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.7rem; margin: 0.1rem;">{confirmation}</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display EMA values and metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            label="FAST EMA (9)",
                            value=f"${composite_signal['fast_ema']:,.2f}" if composite_signal['fast_ema'] > 0 else "N/A",
                            delta=f"{composite_signal['crossover_strength']:.3f}% strength"
                        )
                    with col2:
                        st.metric(
                            label="SLOW EMA (21)", 
                            value=f"${composite_signal['slow_ema']:,.2f}" if composite_signal['slow_ema'] > 0 else "N/A",
                            delta=composite_signal['ema_strength']
                        )
                    with col3:
                        st.metric(
                            label="BITNODES BIAS",
                            value=composite_signal['tor_bias'].replace('_', ' '),
                            delta=composite_signal['tor_strength']
                        )
    else:
        st.info("🔥 Generate signals to see EMA + Bitnodes confirmed scalping opportunities")
    
    # MAIN SIGNAL DISPLAY WITH GODZILLERS THEME
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 GODZILLERS AI SIGNALS</h2>', unsafe_allow_html=True)
    
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Display main signal with GODZILLERS styling
        if "GODZILLA DUMP" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲💀🔥"
            explanation = "EXTREME BEARISH SIGNAL - Market conditions indicate strong selling pressure"
        elif "STRONG SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲🔥"
            explanation = "STRONG SELL SIGNAL - Significant bearish momentum detected"
        elif "SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "SELL SIGNAL - Bearish conditions forming"
        elif "GODZILLA PUMP" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀🌟"
            explanation = "EXTREME BULLISH SIGNAL - Strong buying pressure detected"
        elif "STRONG BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀"
            explanation = "STRONG BUY SIGNAL - Significant bullish momentum building"
        elif "BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🟢"
            explanation = "BUY SIGNAL - Bullish conditions forming"
        else:
            signal_class = "signal-neutral"
            emoji = "🐲⚡"
            explanation = "MARKET NEUTRAL - Awaiting stronger directional signals"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">{emoji} {tor_signal_data["signal"]} {emoji}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">{explanation}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-family: Orbitron; color: #ffffff; margin: 0.5rem 0;">Signal Strength: {tor_signal_data["strength"]} • Tor Change: {tor_signal_data["tor_change"]:+.3f}%</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔥 Click 'GENERATE SIGNALS' to get AI-powered trading signals")
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • PROPRIETARY AI TECHNOLOGY</p>
    <p style="font-size: 0.7rem; color: #ff6666;">FORGE YOUR FORTUNE WITH DRAGON FIRE PRECISION</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main function with login check"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()  