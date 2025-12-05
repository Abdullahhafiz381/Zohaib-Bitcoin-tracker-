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
    
    .p-micro-signal-strong-buy {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 150, 0, 0.4) 100%);
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        animation: pulse-strong-buy 2s infinite;
    }
    
    @keyframes pulse-strong-buy {
        0% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
    }
    
    .p-micro-signal-buy {
        background: linear-gradient(135deg, rgba(100, 255, 100, 0.15) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 2px solid #64ff64;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(100, 255, 100, 0.5);
    }
    
    .p-micro-signal-strong-sell {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(150, 0, 0, 0.4) 100%);
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        animation: pulse-strong-sell 2s infinite;
    }
    
    @keyframes pulse-strong-sell {
        0% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.6); }
    }
    
    .p-micro-signal-sell {
        background: linear-gradient(135deg, rgba(255, 100, 100, 0.15) 0%, rgba(100, 0, 0, 0.3) 100%);
        border: 2px solid #ff6464;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(255, 100, 100, 0.5);
    }
    
    .p-micro-signal-neutral {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.15) 0%, rgba(150, 100, 0, 0.3) 100%);
        border: 2px solid #ffa500;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(255, 165, 0, 0.5);
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
    
    .order-book-card {
        background: rgba(10, 0, 0, 0.85);
        border: 1px solid rgba(255, 0, 0, 0.4);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .bid-row {
        background: linear-gradient(90deg, rgba(0, 255, 0, 0.1) 0%, rgba(0, 100, 0, 0.2) 100%);
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
    }
    
    .ask-row {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.1) 0%, rgba(100, 0, 0, 0.2) 100%);
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
        border-left: 3px solid #ff0000;
    }
    
    .wall-bid {
        background: linear-gradient(90deg, rgba(0, 255, 0, 0.3) 0%, rgba(0, 150, 0, 0.4) 100%);
        border-left: 4px solid #00ff00;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .wall-ask {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.3) 0%, rgba(150, 0, 0, 0.4) 100%);
        border-left: 4px solid #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
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
    
    .p-micro-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .p-micro-positive {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .p-micro-negative {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .p-micro-neutral {
        background: linear-gradient(90deg, #ffa500, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Simple authentication system
def check_credentials(username, password):
    """Check if username and password are correct"""
    valid_users = {
        "godziller": "dragonfire2025",
        "admin": "cryptoking",
        "trader": "bullmarket"
    }
    return username in valid_users and valid_users[username] == password

def login_page():
    """Display login page - SIMPLIFIED VERSION"""
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
            '>P-MICRO ORDER BOOK WARFARE SYSTEM</p>
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
    """Get crypto prices from Binance"""
    coins = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum',
        'BNBUSDT': 'binance-coin',
        'SOLUSDT': 'solana'
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
                
    except Exception as e:
        st.error(f"Error fetching prices: {str(e)}")
        for symbol in coins:
            prices[symbol] = 0.0
    
    return prices

class OrderBookAnalyzer:
    """Analyze order book data and calculate P-micro"""
    
    def __init__(self):
        self.order_books = {}
        self.p_micro_values = {}
        self.last_update = {}
        
    def fetch_order_book(self, symbol='BTCUSDT', limit=20):
        """Fetch order book data from Binance API"""
        try:
            url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get best bid and ask
                bids = [[float(bid[0]), float(bid[1])] for bid in data['bids']]
                asks = [[float(ask[0]), float(ask[1])] for ask in data['asks']]
                
                # Get current price
                ticker_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                ticker_response = requests.get(ticker_url, timeout=5)
                current_price = float(ticker_response.json()['price']) if ticker_response.status_code == 200 else 0
                
                return {
                    'symbol': symbol,
                    'bids': bids,
                    'asks': asks,
                    'current_price': current_price,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return None
                
        except Exception as e:
            st.error(f"Error fetching order book for {symbol}: {str(e)}")
            return None
    
    def calculate_p_micro(self, order_book_data, depth=5):
        """Calculate P-micro using the formula"""
        if not order_book_data:
            return None
            
        bids = order_book_data['bids'][:depth] if order_book_data['bids'] else []
        asks = order_book_data['asks'][:depth] if order_book_data['asks'] else []
        
        if not bids or not asks:
            return None
        
        # Calculate weighted average using top N levels
        total_bid_qty = sum(qty for _, qty in bids)
        total_ask_qty = sum(qty for _, qty in asks)
        
        weighted_bid = sum(price * qty for price, qty in bids) / total_bid_qty if total_bid_qty > 0 else 0
        weighted_ask = sum(price * qty for price, qty in asks) / total_ask_qty if total_ask_qty > 0 else 0
        
        # P-micro formula: (A * Qbid + B * Qask) / (Qbid + Qask)
        p_micro = (weighted_bid * total_bid_qty + weighted_ask * total_ask_qty) / (total_bid_qty + total_ask_qty)
        
        current_price = order_book_data.get('current_price', 0)
        
        # Calculate signal strength
        signal_strength = abs((p_micro - current_price) / current_price * 100) if current_price > 0 else 0
        
        # Determine market pressure
        market_pressure = "BUYERS_STRONG" if p_micro > current_price else "SELLERS_STRONG" if p_micro < current_price else "BALANCED"
        
        # Find large walls (orders significantly larger than average)
        avg_bid_qty = total_bid_qty / len(bids) if bids else 0
        avg_ask_qty = total_ask_qty / len(asks) if asks else 0
        
        large_bid_walls = [(price, qty) for price, qty in bids if qty > avg_bid_qty * 3] if avg_bid_qty > 0 else []
        large_ask_walls = [(price, qty) for price, qty in asks if qty > avg_ask_qty * 3] if avg_ask_qty > 0 else []
        
        return {
            'p_micro': p_micro,
            'current_price': current_price,
            'signal_strength': signal_strength,
            'market_pressure': market_pressure,
            'weighted_bid': weighted_bid,
            'weighted_ask': weighted_ask,
            'total_bid_qty': total_bid_qty,
            'total_ask_qty': total_ask_qty,
            'large_bid_walls': large_bid_walls[:3],  # Top 3 largest bid walls
            'large_ask_walls': large_ask_walls[:3],  # Top 3 largest ask walls
            'bid_ask_ratio': total_bid_qty / total_ask_qty if total_ask_qty > 0 else 0,
            'price_difference_percent': ((p_micro - current_price) / current_price * 100) if current_price > 0 else 0
        }
    
    def generate_trading_signal(self, p_micro_data):
        """Generate trading signal based on P-micro analysis"""
        if not p_micro_data:
            return {
                'signal': 'NO_DATA',
                'strength': 'NEUTRAL',
                'action': 'HOLD',
                'confidence': 0
            }
        
        price_diff_percent = p_micro_data['price_difference_percent']
        signal_strength = p_micro_data['signal_strength']
        
        # Generate signal based on P-micro vs current price
        if price_diff_percent > 0.5:  # P-micro significantly above current price
            if signal_strength > 0.3:
                signal = "🐲 GODZILLA STRONG BUY 🐲"
                strength = "EXTREME_BULLISH"
                action = "BUY_NOW"
                confidence = 90
            elif signal_strength > 0.1:
                signal = "🔥 STRONG BUY SIGNAL 🔥"
                strength = "VERY_BULLISH"
                action = "BUY"
                confidence = 75
            else:
                signal = "🟢 BUY SIGNAL"
                strength = "BULLISH"
                action = "CONSIDER_BUY"
                confidence = 60
                
        elif price_diff_percent > 0.05:  # P-micro slightly above current price
            signal = "📈 MILD BUY"
            strength = "SLIGHTLY_BULLISH"
            action = "WATCH"
            confidence = 40
            
        elif price_diff_percent < -0.5:  # P-micro significantly below current price
            if signal_strength > 0.3:
                signal = "🐲 GODZILLA STRONG SELL 🐲"
                strength = "EXTREME_BEARISH"
                action = "SELL_NOW"
                confidence = 90
            elif signal_strength > 0.1:
                signal = "🔥 STRONG SELL SIGNAL 🔥"
                strength = "VERY_BEARISH"
                action = "SELL"
                confidence = 75
            else:
                signal = "🔴 SELL SIGNAL"
                strength = "BEARISH"
                action = "CONSIDER_SELL"
                confidence = 60
                
        elif price_diff_percent < -0.05:  # P-micro slightly below current price
            signal = "📉 MILD SELL"
            strength = "SLIGHTLY_BEARISH"
            action = "WATCH"
            confidence = 40
            
        else:  # P-micro very close to current price
            signal = "⚖️ MARKET BALANCED"
            strength = "NEUTRAL"
            action = "HOLD"
            confidence = 50
        
        # Adjust confidence based on wall presence
        if p_micro_data['large_bid_walls'] and price_diff_percent > 0:
            confidence += 10
        if p_micro_data['large_ask_walls'] and price_diff_percent < 0:
            confidence += 10
        
        confidence = min(100, max(0, confidence))
        
        return {
            'signal': signal,
            'strength': strength,
            'action': action,
            'confidence': confidence,
            'reasoning': self.generate_signal_reasoning(p_micro_data, price_diff_percent)
        }
    
    def generate_signal_reasoning(self, p_micro_data, price_diff_percent):
        """Generate detailed reasoning for the signal"""
        reasoning = []
        
        if price_diff_percent > 0:
            reasoning.append(f"P-micro is {abs(price_diff_percent):.3f}% above current price")
            reasoning.append("Buyers are controlling the market")
            if p_micro_data['large_bid_walls']:
                reasoning.append(f"Large buy walls detected ({len(p_micro_data['large_bid_walls'])} major walls)")
        elif price_diff_percent < 0:
            reasoning.append(f"P-micro is {abs(price_diff_percent):.3f}% below current price")
            reasoning.append("Sellers are controlling the market")
            if p_micro_data['large_ask_walls']:
                reasoning.append(f"Large sell walls detected ({len(p_micro_data['large_ask_walls'])} major walls)")
        else:
            reasoning.append("Market is balanced")
            reasoning.append("No significant buyer/seller dominance")
        
        reasoning.append(f"Bid/Ask Ratio: {p_micro_data['bid_ask_ratio']:.2f}")
        reasoning.append(f"Signal Strength: {p_micro_data['signal_strength']:.3f}%")
        
        return " • ".join(reasoning)
    
    def update_all_order_books(self, symbols=None):
        """Update order books for all symbols"""
        if symbols is None:
            symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']
        
        for symbol in symbols:
            order_book = self.fetch_order_book(symbol)
            if order_book:
                self.order_books[symbol] = order_book
                p_micro_data = self.calculate_p_micro(order_book)
                if p_micro_data:
                    self.p_micro_values[symbol] = p_micro_data
                    self.last_update[symbol] = datetime.now()

class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.order_book_analyzer = OrderBookAnalyzer()
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

def get_coin_display_name(symbol):
    """Get display name for crypto symbols"""
    names = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum',
        'BNBUSDT': 'Binance Coin',
        'SOLUSDT': 'Solana'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols - GODZILLERS theme"""
    emojis = {
        'BTCUSDT': '🐲',
        'ETHUSDT': '🔥',
        'BNBUSDT': '💰',
        'SOLUSDT': '⚡'
    }
    return emojis.get(symbol, '💀')

def get_signal_class(p_micro_data):
    """Get CSS class for P-micro signal"""
    if not p_micro_data:
        return "p-micro-signal-neutral"
    
    price_diff = p_micro_data['price_difference_percent']
    
    if price_diff > 0.5:
        return "p-micro-signal-strong-buy"
    elif price_diff > 0.1:
        return "p-micro-signal-buy"
    elif price_diff < -0.5:
        return "p-micro-signal-strong-sell"
    elif price_diff < -0.1:
        return "p-micro-signal-sell"
    else:
        return "p-micro-signal-neutral"

def display_order_book(order_book_data, symbol):
    """Display order book with formatting"""
    if not order_book_data:
        return
    
    with st.expander(f"📊 {get_coin_display_name(symbol)} Order Book Details", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 style="color: #00ff00; font-family: Orbitron;">🏹 BIDS (BUY ORDERS)</h4>', unsafe_allow_html=True)
            st.markdown('<div class="order-book-card">', unsafe_allow_html=True)
            
            if order_book_data['bids']:
                for i, (price, qty) in enumerate(order_book_data['bids'][:10]):
                    wall_class = "wall-bid" if qty > sum(q for _, q in order_book_data['bids']) / len(order_book_data['bids']) * 3 else ""
                    st.markdown(f'''
                    <div class="bid-row {wall_class}">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #00ff00; font-family: Orbitron;">${price:,.2f}</span>
                            <span style="color: #ffffff; font-family: Rajdhani;">{qty:.4f}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h4 style="color: #ff0000; font-family: Orbitron;">🎯 ASKS (SELL ORDERS)</h4>', unsafe_allow_html=True)
            st.markdown('<div class="order-book-card">', unsafe_allow_html=True)
            
            if order_book_data['asks']:
                for i, (price, qty) in enumerate(order_book_data['asks'][:10]):
                    wall_class = "wall-ask" if qty > sum(q for _, q in order_book_data['asks']) / len(order_book_data['asks']) * 3 else ""
                    st.markdown(f'''
                    <div class="ask-row {wall_class}">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #ff0000; font-family: Orbitron;">${price:,.2f}</span>
                            <span style="color: #ffffff; font-family: Rajdhani;">{qty:.4f}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS P-MICRO WARFARE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">ORDER BOOK ANALYSIS • REAL-TIME P-MICRO SIGNALS • DRAGON FIRE PRECISION</p>', unsafe_allow_html=True)
    
    # UPDATE BUTTONS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">🎯 P-MICRO ORDER BOOK SIGNALS</h2>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🐲 UPDATE ORDER BOOKS", key="refresh_orderbooks", use_container_width=True, type="primary"):
            with st.spinner("🔥 Scanning order books..."):
                analyzer.order_book_analyzer.update_all_order_books()
                st.success("✅ Order books updated!")
    
    with col3:
        if st.button("📡 UPDATE BITNODES", key="refresh_bitnodes", use_container_width=True):
            with st.spinner("🔥 Connecting to network..."):
                if analyzer.update_node_data():
                    st.success("✅ Bitnodes data updated!")
                else:
                    st.error("❌ Failed to update Bitnodes")
    
    # Initialize order books if not already done
    if not hasattr(analyzer.order_book_analyzer, 'order_books') or not analyzer.order_book_analyzer.order_books:
        with st.spinner("🔥 Initializing order book analysis..."):
            analyzer.order_book_analyzer.update_all_order_books()
    
    # P-MICRO SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">⚡ REAL-TIME P-MICRO SIGNALS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">P-MICRO = (A×Qbid + B×Qask) ÷ (Qbid + Qask) • INSTANT ORDER BOOK ANALYSIS</p>', unsafe_allow_html=True)
    
    # Display P-micro signals for each coin
    symbols_to_display = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']
    
    for symbol in symbols_to_display:
        order_book = analyzer.order_book_analyzer.order_books.get(symbol)
        p_micro_data = analyzer.order_book_analyzer.p_micro_values.get(symbol)
        
        if order_book and p_micro_data:
            # Generate trading signal
            trading_signal = analyzer.order_book_analyzer.generate_trading_signal(p_micro_data)
            
            emoji = get_coin_emoji(symbol)
            name = get_coin_display_name(symbol)
            
            # Determine P-micro value color
            price_diff = p_micro_data['price_difference_percent']
            if price_diff > 0:
                p_micro_class = "p-micro-positive"
            elif price_diff < 0:
                p_micro_class = "p-micro-negative"
            else:
                p_micro_class = "p-micro-neutral"
            
            # Main P-micro signal display
            signal_class = get_signal_class(p_micro_data)
            
            st.markdown(f'''
            <div class="{signal_class}">
                <div style="text-align: center;">
                    <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.3rem;">{emoji} {name}</h3>
                    <p style="font-family: Orbitron; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">{trading_signal['signal']}</p>
                    
                    <div style="display: flex; justify-content: center; gap: 2rem; margin: 1rem 0;">
                        <div style="text-align: center;">
                            <p style="color: #ff8888; margin: 0; font-family: Rajdhani;">P-MICRO VALUE</p>
                            <p class="p-micro-value {p_micro_class}">${p_micro_data['p_micro']:,.2f}</p>
                        </div>
                        
                        <div style="text-align: center;">
                            <p style="color: #ff8888; margin: 0; font-family: Rajdhani;">CURRENT PRICE</p>
                            <p style="font-family: Orbitron; font-size: 1.8rem; font-weight: 700; color: #ffffff; margin: 0;">${p_micro_data['current_price']:,.2f}</p>
                        </div>
                    </div>
                    
                    <p style="color: #ffd700; font-family: Orbitron; font-size: 1rem; margin: 0.2rem 0;">
                        Δ: {p_micro_data['price_difference_percent']:+.3f}% • Strength: {p_micro_data['signal_strength']:.3f}%
                    </p>
                    <p style="color: #ffffff; font-family: Rajdhani; font-size: 0.8rem; margin: 0.2rem 0;">{trading_signal['reasoning']}</p>
                    <p style="color: #ff4444; font-family: Orbitron; font-size: 0.9rem; margin: 0.2rem 0;">Confidence: {trading_signal['confidence']}% • Action: {trading_signal['action']}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="WEIGHTED BID",
                    value=f"${p_micro_data['weighted_bid']:,.2f}",
                    delta=f"Bid Qty: {p_micro_data['total_bid_qty']:.2f}"
                )
            
            with col2:
                st.metric(
                    label="WEIGHTED ASK",
                    value=f"${p_micro_data['weighted_ask']:,.2f}",
                    delta=f"Ask Qty: {p_micro_data['total_ask_qty']:.2f}"
                )
            
            with col3:
                delta_value = f"{p_micro_data['bid_ask_ratio']:.2f} ratio"
                if p_micro_data['bid_ask_ratio'] > 1.2:
                    delta_color = "normal"
                elif p_micro_data['bid_ask_ratio'] < 0.8:
                    delta_color = "inverse"
                else:
                    delta_color = "off"
                
                st.metric(
                    label="MARKET PRESSURE",
                    value=p_micro_data['market_pressure'].replace('_', ' '),
                    delta=delta_value,
                    delta_color=delta_color
                )
            
            # Display order book details
            display_order_book(order_book, symbol)
            
            st.markdown('<div class="divider" style="margin: 1rem 0;"></div>', unsafe_allow_html=True)
    
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
                btc_p_micro = analyzer.order_book_analyzer.p_micro_values.get('BTCUSDT', {}).get('p_micro', 0)
                p_micro_diff = ((btc_p_micro - btc_price) / btc_price * 100) if btc_price > 0 else 0
                
                st.metric(
                    label="P-MICRO SIGNAL",
                    value="BUY" if p_micro_diff > 0 else "SELL" if p_micro_diff < 0 else "NEUTRAL",
                    delta=f"{p_micro_diff:+.2f}%"
                )
            
            with col3:
                st.metric(
                    label="ORDER BOOK", 
                    value="LIVE",
                    delta="Binance API"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display all coins in a grid
        st.markdown('<h3 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">📊 CRYPTO BATTLEGROUND</h3>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        for idx, symbol in enumerate(['ETHUSDT', 'BNBUSDT', 'SOLUSDT']):
            if prices.get(symbol):
                with cols[idx % 3 + 1]:
                    price = prices[symbol]
                    emoji = get_coin_emoji(symbol)
                    name = get_coin_display_name(symbol)
                    
                    # Get P-micro signal for this coin
                    p_micro_info = analyzer.order_book_analyzer.p_micro_values.get(symbol, {})
                    p_micro_value = p_micro_info.get('p_micro', 0)
                    p_micro_diff = ((p_micro_value - price) / price * 100) if price > 0 else 0
                    
                    signal_text = "↑BUY" if p_micro_diff > 0.1 else "↓SELL" if p_micro_diff < -0.1 else "↔HOLD"
                    signal_color = "#00ff00" if p_micro_diff > 0.1 else "#ff0000" if p_micro_diff < -0.1 else "#ffa500"
                    
                    st.markdown(f'''
                    <div class="coin-card">
                        <div style="text-align: center;">
                            <h4 style="font-family: Orbitron; color: #ff4444; margin: 0.5rem 0; font-size: 1.1rem;">{emoji} {name}</h4>
                            <p style="font-family: Orbitron; font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">${price:,.2f}</p>
                            <p style="color: {signal_color}; font-family: Orbitron; font-size: 0.9rem; margin: 0.2rem 0;">P-micro: {signal_text} ({p_micro_diff:+.2f}%)</p>
                            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.8rem; margin: 0;">{symbol}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani;">🕒 Prices updated: {datetime.now().strftime("%H:%M:%S")} • Order books: {len(analyzer.order_book_analyzer.order_books)} active</p>', unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch crypto prices")
    
    # BITNODES NETWORK SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌐 BITNODES NETWORK DATA</h2>', unsafe_allow_html=True)
    
    if analyzer.current_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="TOTAL NODES",
                value=f"{analyzer.current_data['total_nodes']:,}",
                delta="Bitcoin Network"
            )
        
        with col2:
            st.metric(
                label="ACTIVE NODES",
                value=f"{analyzer.current_data['active_nodes']:,}",
                delta=f"{analyzer.current_data['active_ratio']*100:.1f}% active"
            )
        
        with col3:
            st.metric(
                label="TOR NODES",
                value=f"{analyzer.current_data['tor_nodes']:,}",
                delta=f"{analyzer.current_data['tor_percentage']:.1f}%"
            )
        
        with col4:
            if analyzer.last_snapshot_check:
                last_update = datetime.fromisoformat(analyzer.last_snapshot_check.replace('Z', '+00:00'))
                time_diff = (datetime.now() - last_update).seconds
                st.metric(
                    label="LAST UPDATE",
                    value=f"{time_diff // 60}m ago",
                    delta="Network Status"
                )
    else:
        st.info("📡 Click 'UPDATE BITNODES' to get network data")
    
    # P-MICRO EXPLANATION SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.expander("📚 P-MICRO STRATEGY EXPLANATION", expanded=False):
        st.markdown("""
        ## 🐲 GODZILLERS P-MICRO ORDER BOOK ANALYSIS
        
        ### 📊 What is P-micro?
        P-micro is a sophisticated market microstructure indicator that analyzes the **real-time order book** to determine the true market pressure between buyers and sellers.
        
        ### 🔧 Formula:
        ```
        P_micro = (A × Qbid + B × Qask) / (Qbid + Qask)
        ```
        Where:
        - **A** = Best bid price (highest price buyers are willing to pay)
        - **Qbid** = Total quantity at bid side
        - **B** = Best ask price (lowest price sellers are willing to accept)
        - **Qask** = Total quantity at ask side
        
        ### 🎯 Trading Signals:
        1. **P-micro > Current Price** → Buyers are strong → **BUY SIGNAL** 🟢
        2. **P-micro < Current Price** → Sellers are strong → **SELL SIGNAL** 🔴
        3. **P-micro ≈ Current Price** → Market balanced → **HOLD/NEUTRAL** ⚖️
        
        ### 🏹 Large Order Walls:
        - **Buy Walls**: Large bid orders that support price
        - **Sell Walls**: Large ask orders that resist price increases
        - Walls significantly affect P-micro calculations
        
        ### 🐉 GODZILLERS ENHANCEMENTS:
        - Real-time Binance order book data
        - Multi-level depth analysis (top 20 orders)
        - Automatic wall detection
        - Confidence scoring system
        - Combined with Bitnodes network data
        """)
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS P-MICRO ORDER BOOK WARFARE 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • PROPRIETARY ORDER BOOK TECHNOLOGY</p>
    <p style="font-size: 0.7rem; color: #ff6666;">P-MICRO = (A×Qbid + B×Qask) ÷ (Qbid + Qask) • FORGE YOUR FORTUNE WITH ORDER BOOK PRECISION</p>
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