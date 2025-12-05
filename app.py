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
import websocket
import threading
import queue
from collections import deque

# GODZILLERS Streamlit setup
st.set_page_config(
    page_title="🔥 GODZILLERS CRYPTO TRACKER",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GODZILLERS CSS with red and black theme - UPDATED
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
    
    .pmicro-buy-signal {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 150, 0, 0.4) 100%);
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        animation: pulse-buy 2s infinite;
    }
    
    @keyframes pulse-buy {
        0% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.5); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.8); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.5); }
    }
    
    .pmicro-sell-signal {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(150, 0, 0, 0.4) 100%);
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        animation: pulse-sell 2s infinite;
    }
    
    @keyframes pulse-sell {
        0% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
    }
    
    .pmicro-neutral-signal {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2) 0%, rgba(150, 100, 0, 0.4) 100%);
        border: 2px solid #ffa500;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 165, 0, 0.5);
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
    
    .orderbook-buy-row {
        background: linear-gradient(90deg, rgba(0, 255, 0, 0.1) 0%, transparent 100%);
        border-left: 3px solid #00ff00;
        padding: 0.5rem;
        margin: 0.1rem 0;
        border-radius: 5px;
    }
    
    .orderbook-sell-row {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.1) 0%, transparent 100%);
        border-left: 3px solid #ff0000;
        padding: 0.5rem;
        margin: 0.1rem 0;
        border-radius: 5px;
    }
    
    .orderbook-wall-buy {
        background: linear-gradient(90deg, rgba(0, 255, 0, 0.3) 0%, transparent 100%);
        border-left: 4px solid #00ff00;
        font-weight: bold;
        animation: wall-pulse 3s infinite;
    }
    
    .orderbook-wall-sell {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.3) 0%, transparent 100%);
        border-left: 4px solid #ff0000;
        font-weight: bold;
        animation: wall-pulse 3s infinite;
    }
    
    @keyframes wall-pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
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
    
    /* Login Page Styles */
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
    
    .pmicro-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff0000, #ff4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
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

class OrderBookAnalyzer:
    """P-micro analyzer using Binance order book data"""
    def __init__(self):
        self.binance_api = "https://api.binance.com/api/v3/depth"
        self.pmicro_history = {}
        self.wall_threshold_btc = 10.0  # 10 BTC is considered a wall
        self.wall_threshold_eth = 100.0  # 100 ETH is considered a wall
    
    def fetch_order_book(self, symbol, limit=50):
        """Fetch order book data from Binance"""
        try:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            response = requests.get(self.binance_api, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'bids': [[float(price), float(quantity)] for price, quantity in data['bids']],
                    'asks': [[float(price), float(quantity)] for price, quantity in data['asks']],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return None
        except Exception as e:
            return None
    
    def calculate_pmicro(self, order_book_data):
        """Calculate P-micro using the formula"""
        if not order_book_data or not order_book_data['bids'] or not order_book_data['asks']:
            return None
        
        # Get top bid and ask
        top_bid_price = order_book_data['bids'][0][0]
        top_bid_qty = order_book_data['bids'][0][1]
        
        top_ask_price = order_book_data['asks'][0][0]
        top_ask_qty = order_book_data['asks'][0][1]
        
        # Calculate P-micro
        pmicro = ((top_bid_price * top_bid_qty) + (top_ask_price * top_ask_qty)) / (top_bid_qty + top_ask_qty)
        
        return {
            'pmicro': pmicro,
            'bid_price': top_bid_price,
            'bid_qty': top_bid_qty,
            'ask_price': top_ask_price,
            'ask_qty': top_ask_qty,
            'spread': top_ask_price - top_bid_price,
            'spread_percent': ((top_ask_price - top_bid_price) / top_bid_price) * 100,
            'timestamp': order_book_data['timestamp']
        }
    
    def detect_walls(self, order_book_data, symbol):
        """Detect large buy/sell walls in order book"""
        walls = {
            'buy_walls': [],
            'sell_walls': []
        }
        
        # Set threshold based on symbol
        if 'BTC' in symbol:
            threshold = self.wall_threshold_btc
        else:
            threshold = self.wall_threshold_eth
        
        # Check buy walls (bids)
        for price, quantity in order_book_data['bids'][:20]:  # Check top 20 bids
            if quantity >= threshold:
                walls['buy_walls'].append({
                    'price': price,
                    'quantity': quantity,
                    'size_ratio': quantity / threshold
                })
        
        # Check sell walls (asks)
        for price, quantity in order_book_data['asks'][:20]:  # Check top 20 asks
            if quantity >= threshold:
                walls['sell_walls'].append({
                    'price': price,
                    'quantity': quantity,
                    'size_ratio': quantity / threshold
                })
        
        return walls
    
    def analyze_order_book_imbalance(self, order_book_data, levels=10):
        """Analyze order book imbalance"""
        if not order_book_data:
            return None
        
        # Calculate total bid and ask volume for top N levels
        total_bid_volume = sum([qty for _, qty in order_book_data['bids'][:levels]])
        total_ask_volume = sum([qty for _, qty in order_book_data['asks'][:levels]])
        
        total_volume = total_bid_volume + total_ask_volume
        
        if total_volume > 0:
            bid_ratio = total_bid_volume / total_volume
            ask_ratio = total_ask_volume / total_volume
        else:
            bid_ratio = ask_ratio = 0.5
        
        imbalance = bid_ratio - ask_ratio
        
        return {
            'bid_volume': total_bid_volume,
            'ask_volume': total_ask_volume,
            'bid_ratio': bid_ratio,
            'ask_ratio': ask_ratio,
            'imbalance': imbalance,
            'imbalance_percent': imbalance * 100
        }
    
    def generate_pmicro_signal(self, pmicro_data, current_price):
        """Generate trading signal based on P-micro vs current price"""
        if not pmicro_data or not current_price:
            return {
                'signal': 'NO_DATA',
                'strength': 'NEUTRAL',
                'pmicro_diff': 0,
                'pmicro_diff_percent': 0
            }
        
        pmicro = pmicro_data['pmicro']
        pmicro_diff = pmicro - current_price
        pmicro_diff_percent = (pmicro_diff / current_price) * 100
        
        # Generate signal based on P-micro vs current price
        if pmicro_diff_percent >= 0.5:  # P-micro > current price by 0.5% or more
            signal = "🚀 STRONG BUY"
            strength = "VERY_STRONG"
        elif pmicro_diff_percent >= 0.2:  # P-micro > current price by 0.2-0.49%
            signal = "🟢 BUY"
            strength = "STRONG"
        elif pmicro_diff_percent >= 0.05:  # P-micro > current price by 0.05-0.19%
            signal = "🟡 WEAK BUY"
            strength = "MODERATE"
        elif pmicro_diff_percent <= -0.5:  # P-micro < current price by 0.5% or more
            signal = "💀 STRONG SELL"
            strength = "VERY_STRONG"
        elif pmicro_diff_percent <= -0.2:  # P-micro < current price by 0.2-0.49%
            signal = "🔴 SELL"
            strength = "STRONG"
        elif pmicro_diff_percent <= -0.05:  # P-micro < current price by 0.05-0.19%
            signal = "🟠 WEAK SELL"
            strength = "MODERATE"
        else:  # Within ±0.05%
            signal = "⚪ NEUTRAL"
            strength = "NEUTRAL"
        
        # Add explanation
        if "BUY" in signal:
            explanation = "Buyers are stronger - P-micro indicates buying pressure"
        elif "SELL" in signal:
            explanation = "Sellers are stronger - P-micro indicates selling pressure"
        else:
            explanation = "Market is balanced - No clear directional bias"
        
        return {
            'signal': signal,
            'strength': strength,
            'pmicro_diff': pmicro_diff,
            'pmicro_diff_percent': pmicro_diff_percent,
            'explanation': explanation,
            'current_price': current_price,
            'pmicro': pmicro
        }

class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.orderbook_analyzer = OrderBookAnalyzer()
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
        """Calculate signal based on Tor percentage changes"""
        if not self.current_data or not self.previous_data:
            return {
                'signal': "🔄 NEED DATA",
                'bias': "UPDATE_REQUIRED",
                'strength': "NEUTRAL",
                'tor_change': 0
            }
        
        current_tor_pct = self.current_data['tor_percentage']
        previous_tor_pct = self.previous_data['tor_percentage']
        
        # Calculate percentage change in Tor nodes
        tor_pct_change = current_tor_pct - previous_tor_pct
        
        # TOR PERCENTAGE SIGNAL LOGIC
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
            'tor_change': tor_pct_change
        }
    
    def generate_composite_signal(self, symbol, current_price, pmicro_signal, tor_signal):
        """Combine P-micro and Bitnodes signals for enhanced accuracy"""
        if not pmicro_signal or pmicro_signal['signal'] == 'NO_DATA':
            return {
                'composite_signal': 'WAITING_FOR_DATA',
                'confidence': 'LOW',
                'reasoning': 'Waiting for order book data...'
            }
        
        # Score components (0-100)
        pmicro_score = 0
        tor_score = 0
        
        # Score P-micro signal
        pmicro_strength = pmicro_signal['strength']
        if pmicro_strength == 'VERY_STRONG':
            pmicro_score = 50
        elif pmicro_strength == 'STRONG':
            pmicro_score = 40
        elif pmicro_strength == 'MODERATE':
            pmicro_score = 30
        else:
            pmicro_score = 20
        
        # Score Tor signal
        tor_strength = tor_signal['strength']
        if tor_strength == 'EXTREME':
            tor_score = 50
        elif tor_strength == 'STRONG':
            tor_score = 40
        elif tor_strength == 'MODERATE':
            tor_score = 30
        else:
            tor_score = 20
        
        # Check alignment
        pmicro_direction = "BULLISH" if "BUY" in pmicro_signal['signal'] else "BEARISH" if "SELL" in pmicro_signal['signal'] else "NEUTRAL"
        tor_direction = "BULLISH" if "BULLISH" in tor_signal['bias'] else "BEARISH" if "BEARISH" in tor_signal['bias'] else "NEUTRAL"
        
        alignment_bonus = 0
        if pmicro_direction == tor_direction and pmicro_direction != "NEUTRAL":
            alignment_bonus = 30
        elif pmicro_direction != "NEUTRAL" and tor_direction != "NEUTRAL" and pmicro_direction != tor_direction:
            alignment_bonus = -20
        
        total_score = pmicro_score + tor_score + alignment_bonus
        
        # Generate composite signal
        if total_score >= 100:
            if pmicro_direction == "BULLISH":
                signal = "🚨 GODZILLA CONFIRMED BUY 🚨"
                signal_class = "pmicro-buy-signal"
            else:
                signal = "🚨 GODZILLA CONFIRMED SELL 🚨"
                signal_class = "pmicro-sell-signal"
            confidence = "EXTREME"
        elif total_score >= 80:
            if pmicro_direction == "BULLISH":
                signal = "🔥 DRAGON FIRE BUY 🔥"
                signal_class = "pmicro-buy-signal"
            else:
                signal = "🔥 DRAGON FIRE SELL 🔥"
                signal_class = "pmicro-sell-signal"
            confidence = "VERY_HIGH"
        elif total_score >= 60:
            if pmicro_direction == "BULLISH":
                signal = "🟢 STRONG BUY SIGNAL"
                signal_class = "signal-buy"
            else:
                signal = "🔴 STRONG SELL SIGNAL"
                signal_class = "signal-sell"
            confidence = "HIGH"
        elif total_score >= 40:
            if pmicro_direction == "BULLISH":
                signal = "🟡 WEAK BUY"
                signal_class = "signal-neutral"
            else:
                signal = "🟠 WEAK SELL"
                signal_class = "signal-neutral"
            confidence = "MEDIUM"
        else:
            signal = "⚪ MARKET NEUTRAL"
            signal_class = "signal-neutral"
            confidence = "LOW"
        
        # Generate reasoning
        reasoning_parts = []
        reasoning_parts.append(f"P-micro: {pmicro_signal['signal']} ({pmicro_strength})")
        reasoning_parts.append(f"Bitnodes: {tor_signal['signal']}")
        
        if alignment_bonus > 0:
            reasoning_parts.append("✅ SIGNALS ALIGNED")
        elif alignment_bonus < 0:
            reasoning_parts.append("⚠️ SIGNAL CONFLICT")
        
        reasoning_parts.append(f"Confidence Score: {total_score}/100")
        
        return {
            'composite_signal': signal,
            'signal_class': signal_class,
            'confidence': confidence,
            'reasoning': " • ".join(reasoning_parts),
            'pmicro_signal': pmicro_signal['signal'],
            'tor_signal': tor_signal['signal'],
            'total_score': total_score,
            'pmicro_score': pmicro_score,
            'tor_score': tor_score,
            'alignment': "ALIGNED" if alignment_bonus > 0 else "CONFLICT" if alignment_bonus < 0 else "NEUTRAL"
        }

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

def display_order_book_table(order_book_data, symbol, title="Order Book"):
    """Display order book as a table with styling"""
    if not order_book_data:
        return
    
    st.markdown(f'<h3 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">{title}</h3>', unsafe_allow_html=True)
    
    # Create two columns for bids and asks
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 style="color: #00ff00; font-family: Rajdhani;">🟢 BUY ORDERS (Bids)</h4>', unsafe_allow_html=True)
        
        # Display top 10 bids
        for i, (price, qty) in enumerate(order_book_data['bids'][:10]):
            # Check if this is a wall
            is_wall = False
            if ('BTC' in symbol and qty >= 10) or ('ETH' in symbol and qty >= 100):
                is_wall = True
            
            row_class = "orderbook-wall-buy" if is_wall else "orderbook-buy-row"
            
            st.markdown(f'''
            <div class="{row_class}">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #ffffff; font-family: Rajdhani;">${price:,.2f}</span>
                    <span style="color: #00ff00; font-family: Orbitron;">{qty:.4f}</span>
                    <span style="color: #888888; font-family: Rajdhani;">${price*qty:,.0f}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h4 style="color: #ff0000; font-family: Rajdhani;">🔴 SELL ORDERS (Asks)</h4>', unsafe_allow_html=True)
        
        # Display top 10 asks
        for i, (price, qty) in enumerate(order_book_data['asks'][:10]):
            # Check if this is a wall
            is_wall = False
            if ('BTC' in symbol and qty >= 10) or ('ETH' in symbol and qty >= 100):
                is_wall = True
            
            row_class = "orderbook-wall-sell" if is_wall else "orderbook-sell-row"
            
            st.markdown(f'''
            <div class="{row_class}">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #ffffff; font-family: Rajdhani;">${price:,.2f}</span>
                    <span style="color: #ff0000; font-family: Orbitron;">{qty:.4f}</span>
                    <span style="color: #888888; font-family: Rajdhani;">${price*qty:,.0f}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

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
    st.markdown('<p class="godzillers-subheader">P-MICRO ORDER BOOK ANALYSIS • BITNODES INTEGRATION • DRAGON FIRE PRECISION</p>', unsafe_allow_html=True)
    
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
    
    # P-MICRO ORDER BOOK ANALYZER SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 P-MICRO ORDER BOOK ANALYSIS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">P-micro = (Bid Price × Bid Qty + Ask Price × Ask Qty) ÷ (Bid Qty + Ask Qty)</p>', unsafe_allow_html=True)
    
    if prices:
        # P-micro analysis for each coin
        for symbol in ['BTCUSDT', 'ETHUSDT']:
            current_price = prices.get(symbol)
            if current_price:
                st.markdown(f'<div class="divider"></div>', unsafe_allow_html=True)
                
                # Get order book data
                order_book_data = analyzer.orderbook_analyzer.fetch_order_book(symbol, limit=50)
                
                if order_book_data:
                    # Calculate P-micro
                    pmicro_data = analyzer.orderbook_analyzer.calculate_pmicro(order_book_data)
                    
                    if pmicro_data:
                        # Generate P-micro signal
                        pmicro_signal = analyzer.orderbook_analyzer.generate_pmicro_signal(pmicro_data, current_price)
                        
                        # Get Bitnodes signal
                        tor_signal = analyzer.calculate_tor_signal()
                        
                        # Generate composite signal
                        composite_signal = analyzer.generate_composite_signal(symbol, current_price, pmicro_signal, tor_signal)
                        
                        emoji = get_coin_emoji(symbol)
                        name = get_coin_display_name(symbol)
                        
                        # Display main P-micro analysis
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            # P-micro value with styling
                            st.markdown(f'''
                            <div style="text-align: center; padding: 1rem;">
                                <p style="color: #ff8888; font-family: Rajdhani; margin-bottom: 0.5rem;">{emoji} {name} P-MICRO VALUE</p>
                                <p class="pmicro-value">${pmicro_data["pmicro"]:,.2f}</p>
                                <p style="color: #ff8888; font-family: Rajdhani; margin-top: 0.5rem;">
                                    vs Current: ${current_price:,.2f} 
                                    • Diff: {pmicro_signal["pmicro_diff_percent"]:+.3f}%
                                </p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col2:
                            st.metric(
                                label="BID PRICE",
                                value=f"${pmicro_data['bid_price']:,.2f}",
                                delta=f"Qty: {pmicro_data['bid_qty']:.4f}"
                            )
                        
                        with col3:
                            st.metric(
                                label="ASK PRICE",
                                value=f"${pmicro_data['ask_price']:,.2f}",
                                delta=f"Qty: {pmicro_data['ask_qty']:.4f}",
                                delta_color="inverse"
                            )
                        
                        # Display composite signal
                        st.markdown(f'<div class="{composite_signal["signal_class"]}">', unsafe_allow_html=True)
                        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">{composite_signal["composite_signal"]}</h2>', unsafe_allow_html=True)
                        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">{composite_signal["reasoning"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p style="text-align: center; color: #ffffff; font-family: Rajdhani; margin: 0.5rem 0;">Confidence: {composite_signal["confidence"]} • Score: {composite_signal["total_score"]}/100</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display order book table
                        display_order_book_table(order_book_data, symbol, f"{emoji} {name} Order Book - Top 10 Levels")
                        
                        # Display order book imbalance analysis
                        imbalance = analyzer.orderbook_analyzer.analyze_order_book_imbalance(order_book_data, levels=20)
                        if imbalance:
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric(
                                    label="BUY VOLUME",
                                    value=f"{imbalance['bid_volume']:.2f}",
                                    delta=f"{imbalance['bid_ratio']*100:.1f}%"
                                )
                            
                            with col2:
                                st.metric(
                                    label="SELL VOLUME",
                                    value=f"{imbalance['ask_volume']:.2f}",
                                    delta=f"{imbalance['ask_ratio']*100:.1f}%",
                                    delta_color="inverse"
                                )
                            
                            with col3:
                                imbalance_color = "normal" if imbalance['imbalance'] > 0 else "inverse"
                                st.metric(
                                    label="ORDER BOOK IMBALANCE",
                                    value=f"{imbalance['imbalance_percent']:+.2f}%",
                                    delta="Buyers Dominant" if imbalance['imbalance'] > 0 else "Sellers Dominant"
                                )
                            
                            with col4:
                                st.metric(
                                    label="SPREAD",
                                    value=f"${pmicro_data['spread']:.2f}",
                                    delta=f"{pmicro_data['spread_percent']:.3f}%"
                                )
                        
                        # Detect and display walls
                        walls = analyzer.orderbook_analyzer.detect_walls(order_book_data, symbol)
                        if walls['buy_walls'] or walls['sell_walls']:
                            st.markdown('<h4 style="color: #ffd700; font-family: Orbitron; margin: 1rem 0;">🚨 LARGE ORDER WALLS DETECTED</h4>', unsafe_allow_html=True)
                            
                            if walls['buy_walls']:
                                st.markdown('<p style="color: #00ff00; font-family: Rajdhani;">🟢 BUY WALLS (Support):</p>', unsafe_allow_html=True)
                                for wall in walls['buy_walls']:
                                    st.markdown(f'''
                                    <div class="orderbook-wall-buy">
                                        <div style="display: flex; justify-content: space-between;">
                                            <span style="color: #ffffff; font-family: Rajdhani;">${wall["price"]:,.2f}</span>
                                            <span style="color: #00ff00; font-family: Orbitron;">{wall["quantity"]:.2f}</span>
                                            <span style="color: #ffd700; font-family: Rajdhani;">{wall["size_ratio"]:.1f}x Wall</span>
                                        </div>
                                    </div>
                                    ''', unsafe_allow_html=True)
                            
                            if walls['sell_walls']:
                                st.markdown('<p style="color: #ff0000; font-family: Rajdhani;">🔴 SELL WALLS (Resistance):</p>', unsafe_allow_html=True)
                                for wall in walls['sell_walls']:
                                    st.markdown(f'''
                                    <div class="orderbook-wall-sell">
                                        <div style="display: flex; justify-content: space-between;">
                                            <span style="color: #ffffff; font-family: Rajdhani;">${wall["price"]:,.2f}</span>
                                            <span style="color: #ff0000; font-family: Orbitron;">{wall["quantity"]:.2f}</span>
                                            <span style="color: #ffd700; font-family: Rajdhani;">{wall["size_ratio"]:.1f}x Wall</span>
                                        </div>
                                    </div>
                                    ''', unsafe_allow_html=True)
    
    # MAIN SIGNAL DISPLAY WITH GODZILLERS THEME
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 BITNODES NETWORK SIGNALS</h2>', unsafe_allow_html=True)
    
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Display main signal with GODZILLERS styling
        if "GODZILLA DUMP" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲💀🔥"
            explanation = "EXTREME BEARISH - Tor nodes increasing significantly"
        elif "STRONG SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲🔥"
            explanation = "STRONG SELL - Tor nodes increasing"
        elif "SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "SELL - Tor nodes slightly increasing"
        elif "GODZILLA PUMP" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀🌟"
            explanation = "EXTREME BULLISH - Tor nodes decreasing significantly"
        elif "STRONG BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀"
            explanation = "STRONG BUY - Tor nodes decreasing"
        elif "BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🟢"
            explanation = "BUY - Tor nodes slightly decreasing"
        else:
            signal_class = "signal-neutral"
            emoji = "🐲⚡"
            explanation = "MARKET NEUTRAL - Tor nodes stable"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">{emoji} {tor_signal_data["signal"]} {emoji}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">{explanation}</p>', unsafe_allow_html=True)
        
        # Display Bitnodes metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="TOTAL NODES",
                value=f"{analyzer.current_data['total_nodes']:,}",
                delta="Network Size"
            )
        
        with col2:
            st.metric(
                label="TOR NODES",
                value=f"{analyzer.current_data['tor_nodes']:,}",
                delta=f"{analyzer.current_data['tor_percentage']:.2f}%"
            )
        
        with col3:
            st.metric(
                label="ACTIVE NODES",
                value=f"{analyzer.current_data['active_nodes']:,}",
                delta=f"{analyzer.current_data['active_ratio']*100:.1f}%"
            )
        
        with col4:
            delta_value = f"{tor_signal_data['tor_change']:+.3f}%"
            delta_color = "normal" if tor_signal_data['tor_change'] < 0 else "inverse"
            st.metric(
                label="TOR CHANGE",
                value=f"{analyzer.current_data['tor_percentage']:.3f}%",
                delta=delta_value,
                delta_color=delta_color
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔥 Click 'GENERATE SIGNALS' to get Bitnodes network signals")
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS P-MICRO ORDER BOOK ANALYZER 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • PROPRIETARY AI TECHNOLOGY</p>
    <p style="font-size: 0.7rem; color: #ff6666;">P-micro = (Bid×Qbid + Ask×Qask) ÷ (Qbid + Qask) • Real-time Order Book Intelligence</p>
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