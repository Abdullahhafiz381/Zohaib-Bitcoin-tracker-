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
import math

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
        animation: pulse-buy 2s infinite;
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(100, 0, 0, 0.4) 100%);
        border: 1px solid #ff0000;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
        animation: pulse-sell 2s infinite;
    }
    
    @keyframes pulse-buy {
        0% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.3); }
        50% { box-shadow: 0 0 35px rgba(0, 255, 0, 0.6); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.3); }
    }
    
    @keyframes pulse-sell {
        0% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.4); }
        50% { box-shadow: 0 0 35px rgba(255, 0, 0, 0.7); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.4); }
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
    
    /* Confidence bar styles */
    .confidence-bar {
        height: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
        position: relative;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .confidence-high {
        background: linear-gradient(90deg, #00ff00, #00cc00);
    }
    
    .confidence-medium {
        background: linear-gradient(90deg, #ffa500, #ff8c00);
    }
    
    .confidence-low {
        background: linear-gradient(90deg, #ff0000, #cc0000);
    }
    
    .confidence-text {
        position: absolute;
        width: 100%;
        text-align: center;
        font-family: 'Orbitron', monospace;
        font-size: 0.8rem;
        color: white;
        line-height: 20px;
        text-shadow: 1px 1px 2px black;
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
    
    .signal-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.2rem;
    }
    
    .buy-badge {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000000;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .sell-badge {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: #ffffff;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }
    
    .neutral-badge {
        background: linear-gradient(90deg, #ffa500, #ff8c00);
        color: #000000;
        box-shadow: 0 0 10px rgba(255, 165, 0, 0.5);
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
    """Display login page"""
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

# ========== INTERNAL FORMULAS (NEVER DISPLAYED) ==========
def calc_tor_percentage(tor_nodes, total_nodes):
    """Internal formula: TOR percentage - NEVER DISPLAYED"""
    if total_nodes > 0:
        return (tor_nodes / total_nodes) * 100
    return 0

def calc_onion_percentage(onion_nodes, total_nodes):
    """Internal formula: .onion percentage - NEVER DISPLAYED"""
    if total_nodes > 0:
        return (onion_nodes / total_nodes) * 100
    return 0

def calc_mid_price(best_bid, best_ask):
    """Internal formula: Mid price - NEVER DISPLAYED"""
    return (best_bid + best_ask) / 2

def calc_p_micro(best_bid, best_ask, bid_size, ask_size):
    """Internal formula: Micro price (P_micro) - NEVER DISPLAYED"""
    # P_micro = (A * Qbid + B * Qask) / (Qbid + Qask)
    if bid_size + ask_size > 0:
        return (best_bid * bid_size + best_ask * ask_size) / (bid_size + ask_size)
    return (best_bid + best_ask) / 2

# ========== CRYPTO ANALYZER ==========
class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.coins = {
            'BTC': {'symbol': 'BTCUSDT', 'name': 'Bitcoin', 'emoji': '🐲'},
            'ETH': {'symbol': 'ETHUSDT', 'name': 'Ethereum', 'emoji': '🔥'},
            'SUI': {'symbol': 'SUIUSDT', 'name': 'Sui', 'emoji': '⚡'},
            'LINK': {'symbol': 'LINKUSDT', 'name': 'Chainlink', 'emoji': '🔗'},
            'SOL': {'symbol': 'SOLUSDT', 'name': 'Solana', 'emoji': '🌟'},
            'XRP': {'symbol': 'XRPUSDT', 'name': 'XRP', 'emoji': '✈️'},
            'TAO': {'symbol': 'TAOUSDT', 'name': 'Bittensor', 'emoji': '🧠'},
            'ENA': {'symbol': 'ENAUSDT', 'name': 'Ethena', 'emoji': '🌀'},
            'ADA': {'symbol': 'ADAUSDT', 'name': 'Cardano', 'emoji': '🔶'},
            'DOGE': {'symbol': 'DOGEUSDT', 'name': 'Dogecoin', 'emoji': '🐕'},
            'BRETT': {'symbol': 'BRETTUSDT', 'name': 'Brett', 'emoji': '🤖'}
        }
        
        # State tracking variables (internal - never displayed)
        self.current_tor = 0
        self.previous_tor = 0
        self.current_onion = 0
        self.previous_onion = 0
        self.current_pmicro = {}
        self.previous_pmicro = {}
        
        self.load_state()
    
    def load_state(self):
        """Load previous state from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    # Load state variables
                    self.current_tor = data.get('current_tor', 0)
                    self.previous_tor = data.get('previous_tor', 0)
                    self.current_onion = data.get('current_onion', 0)
                    self.previous_onion = data.get('previous_onion', 0)
                    self.current_pmicro = data.get('current_pmicro', {})
                    self.previous_pmicro = data.get('previous_pmicro', {})
                    
        except Exception as e:
            # Initialize with defaults
            self.current_tor = 0
            self.previous_tor = 0
            self.current_onion = 0
            self.previous_onion = 0
            self.current_pmicro = {}
            self.previous_pmicro = {}
    
    def save_state(self):
        """Save current state to file"""
        try:
            data = {
                'current_tor': self.current_tor,
                'previous_tor': self.previous_tor,
                'current_onion': self.current_onion,
                'previous_onion': self.previous_onion,
                'current_pmicro': self.current_pmicro,
                'previous_pmicro': self.previous_pmicro,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            st.error(f"Error saving state: {e}")
    
    def fetch_node_data(self):
        """Fetch current node data from Bitnodes API"""
        try:
            response = requests.get(self.bitnodes_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_nodes = data['total_nodes']
                tor_nodes = 0
                onion_nodes = 0
                
                # Count Tor and .onion nodes
                for node_address, node_info in data['nodes'].items():
                    node_address_str = str(node_address).lower()
                    
                    # Count .onion nodes
                    if '.onion' in node_address_str:
                        onion_nodes += 1
                    
                    # Count Tor nodes (including .onion and other tor indicators)
                    if '.onion' in node_address_str or any(tor_indicator in node_address_str 
                                                          for tor_indicator in ['tor', 'torserver']):
                        tor_nodes += 1
                
                # Calculate percentages using internal formulas
                tor_pct = calc_tor_percentage(tor_nodes, total_nodes)
                onion_pct = calc_onion_percentage(onion_nodes, total_nodes)
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_nodes': total_nodes,
                    'tor_nodes': tor_nodes,
                    'onion_nodes': onion_nodes,
                    'tor_percentage': tor_pct,  # Already calculated, never display formula
                    'onion_percentage': onion_pct,  # Already calculated, never display formula
                    'active_nodes': sum(1 for node in data['nodes'].values() if node and isinstance(node, list) and len(node) > 0)
                }
            else:
                return None
        except Exception as e:
            return None
    
    def get_order_book_data(self, symbol):
        """Get order book data from Binance"""
        try:
            url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get best bid and ask
                best_bid = float(data['bids'][0][0]) if data['bids'] else 0
                best_ask = float(data['asks'][0][0]) if data['asks'] else 0
                bid_size = float(data['bids'][0][1]) if data['bids'] else 0
                ask_size = float(data['asks'][0][1]) if data['asks'] else 0
                
                return {
                    'best_bid': best_bid,
                    'best_ask': best_ask,
                    'bid_size': bid_size,
                    'ask_size': ask_size
                }
            else:
                return None
        except Exception as e:
            return None
    
    def classify_signal(self, pmicro, mid_price):
        """Classify signal as BUY, SELL, or NEUTRAL based on P_micro vs mid_price"""
        epsilon = 0.001 * mid_price  # Small threshold
        
        if pmicro > mid_price + epsilon:
            return 'BUY'
        elif pmicro < mid_price - epsilon:
            return 'SELL'
        else:
            return 'NEUTRAL'
    
    def get_global_signal(self):
        """Get global TOR/.onion signal (NEVER display internal logic)"""
        # Internal logic only
        tor_rising = self.current_tor > self.previous_tor
        tor_falling = self.current_tor < self.previous_tor
        onion_rising = self.current_onion > self.previous_onion
        onion_falling = self.current_onion < self.previous_onion
        
        # Apply signal decision rules (internal)
        if tor_rising and onion_rising:
            return 'SELL', 'TOR rising + .onion rising → SELL pressure'
        elif tor_falling and onion_falling:
            return 'BUY', 'TOR falling + .onion falling → BUY pressure'
        elif tor_rising and onion_falling:
            return 'NEUTRAL', 'TOR rising but .onion falling → conflicting signals'
        elif tor_falling and onion_rising:
            return 'NEUTRAL', 'TOR falling but .onion rising → conflicting signals'
        else:
            return 'NEUTRAL', 'No clear TOR/.onion signal'
    
    def get_btc_signal(self, global_signal, btc_pmicro_class):
        """Get BTC signal based on full confirmation rules"""
        # Internal logic only
        if global_signal == 'BUY' and btc_pmicro_class == 'BUY':
            return 'BUY'
        elif global_signal == 'SELL' and btc_pmicro_class == 'SELL':
            return 'SELL'
        else:
            return 'NEUTRAL'
    
    def get_altcoin_signal(self, global_signal, altcoin_pmicro_class):
        """Get altcoin signal based on exact rules"""
        # Internal logic only - applying exact rules
        if altcoin_pmicro_class == 'SELL' and global_signal == 'BUY':
            return 'NEUTRAL'  # Rule 1
        elif altcoin_pmicro_class == 'SELL' and global_signal == 'SELL':
            return 'SELL'  # Rule 2
        elif altcoin_pmicro_class == 'SELL' and global_signal == 'NEUTRAL':
            return 'SELL'  # Rule 3
        elif altcoin_pmicro_class == 'BUY' and global_signal == 'BUY':
            return 'BUY'  # Rule 4
        elif altcoin_pmicro_class == 'BUY' and global_signal == 'SELL':
            return 'SELL'  # Rule 5
        elif altcoin_pmicro_class == 'NEUTRAL':
            return global_signal  # Rule 6 (follow TOR direction)
        else:
            return 'NEUTRAL'
    
    def calculate_confidence(self, signals):
        """Calculate confidence percentage from agreement"""
        # Count agreements
        agreement_count = 0
        total_count = 0
        
        if 'TOR_signal' in signals and 'onion_signal' in signals:
            total_count += 2
            if signals['TOR_signal'] == signals['onion_signal']:
                agreement_count += 2
        
        if 'pmicro_class' in signals:
            total_count += 1
            if signals.get('pmicro_class') == signals.get('final_signal'):
                agreement_count += 1
        
        if total_count > 0:
            confidence = (agreement_count / total_count) * 100
            return min(100, max(0, int(confidence)))
        return 50
    
    def update_signals(self):
        """Update all signals (main function called on refresh)"""
        # Fetch new node data
        node_data = self.fetch_node_data()
        if not node_data:
            return False
        
        # Update state tracking (internal - never displayed)
        self.previous_tor = self.current_tor
        self.current_tor = node_data['tor_percentage']
        self.previous_onion = self.current_onion
        self.current_onion = node_data['onion_percentage']
        
        # Get global signal
        global_signal, global_reason = self.get_global_signal()
        
        # Update all coin signals
        all_signals = {'BTC': {}, 'altcoins': {}}
        
        for coin_key, coin_info in self.coins.items():
            symbol = coin_info['symbol']
            
            # Get order book data
            order_book = self.get_order_book_data(symbol)
            if not order_book:
                continue
            
            # Calculate mid price (internal)
            mid_price = calc_mid_price(order_book['best_bid'], order_book['best_ask'])
            
            # Calculate P_micro (internal)
            pmicro = calc_p_micro(
                order_book['best_bid'], 
                order_book['best_ask'],
                order_book['bid_size'],
                order_book['ask_size']
            )
            
            # Classify P_micro signal (internal)
            pmicro_class = self.classify_signal(pmicro, mid_price)
            
            # Update state tracking for P_micro (internal)
            if coin_key in self.current_pmicro:
                self.previous_pmicro[coin_key] = self.current_pmicro[coin_key]
            self.current_pmicro[coin_key] = pmicro
            
            # Get final signal
            if coin_key == 'BTC':
                final_signal = self.get_btc_signal(global_signal, pmicro_class)
                signals = {
                    'TOR_signal': 'SELL' if self.current_tor > self.previous_tor else 'BUY' if self.current_tor < self.previous_tor else 'NEUTRAL',
                    'onion_signal': 'SELL' if self.current_onion > self.previous_onion else 'BUY' if self.current_onion < self.previous_onion else 'NEUTRAL',
                    'pmicro_class': pmicro_class,
                    'final_signal': final_signal
                }
                confidence = self.calculate_confidence(signals)
                
                all_signals['BTC'] = {
                    'price': mid_price,
                    'signal': final_signal,
                    'confidence': confidence,
                    'pmicro': pmicro,
                    'mid_price': mid_price,
                    'global_signal': global_signal,
                    'global_reason': global_reason
                }
            else:
                # Altcoin
                final_signal = self.get_altcoin_signal(global_signal, pmicro_class)
                
                # Only include if signal is BUY or SELL (NEUTRAL altcoins are hidden)
                if final_signal in ['BUY', 'SELL']:
                    signals = {
                        'TOR_signal': 'SELL' if self.current_tor > self.previous_tor else 'BUY' if self.current_tor < self.previous_tor else 'NEUTRAL',
                        'pmicro_class': pmicro_class,
                        'final_signal': final_signal
                    }
                    confidence = self.calculate_confidence(signals)
                    
                    all_signals['altcoins'][coin_key] = {
                        'price': mid_price,
                        'signal': final_signal,
                        'confidence': confidence,
                        'pmicro': pmicro,
                        'mid_price': mid_price,
                        'name': coin_info['name'],
                        'emoji': coin_info['emoji']
                    }
        
        # Save state
        self.save_state()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'global_signal': global_signal,
            'global_reason': global_reason,
            'node_data': node_data,
            'signals': all_signals,
            'current_tor': self.current_tor,
            'current_onion': self.current_onion,
            'tor_change': self.current_tor - self.previous_tor,
            'onion_change': self.current_onion - self.previous_onion
        }

def get_confidence_bar_html(confidence, signal):
    """Generate HTML for confidence bar"""
    if confidence >= 70:
        fill_class = "confidence-high"
    elif confidence >= 40:
        fill_class = "confidence-medium"
    else:
        fill_class = "confidence-low"
    
    signal_color = "#00ff00" if signal == "BUY" else "#ff0000" if signal == "SELL" else "#ffa500"
    
    return f'''
    <div class="confidence-bar">
        <div class="confidence-fill {fill_class}" style="width: {confidence}%; background: {signal_color};"></div>
        <div class="confidence-text">{confidence}% confidence</div>
    </div>
    '''

def display_btc_panel(btc_data):
    """Display BTC price panel with signal"""
    if not btc_data:
        return
    
    signal = btc_data['signal']
    price = btc_data['price']
    confidence = btc_data['confidence']
    
    # Determine signal styling
    if signal == 'BUY':
        signal_emoji = '🚀'
        signal_text = 'BUY SIGNAL'
        signal_color = '#00ff00'
    elif signal == 'SELL':
        signal_emoji = '💀'
        signal_text = 'SELL SIGNAL'
        signal_color = '#ff0000'
    else:
        signal_emoji = '⚡'
        signal_text = 'NEUTRAL'
        signal_color = '#ffa500'
    
    st.markdown('<div class="price-glow">', unsafe_allow_html=True)
    
    # Header with signal
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'''
        <div style="text-align: center;">
            <h1 style="font-family: Orbitron; font-size: 2.5rem; color: {signal_color}; margin: 0;">
                {signal_emoji} {signal_text} {signal_emoji}
            </h1>
        </div>
        ''', unsafe_allow_html=True)
    
    # Price and confidence
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'''
        <div style="text-align: center;">
            <p style="font-family: Orbitron; font-size: 3rem; font-weight: 900; 
               background: linear-gradient(90deg, #ff0000, #ff4444); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               margin: 0.5rem 0;">
               ${price:,.2f}
            </p>
            <p style="color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">BITCOIN (BTC)</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Confidence bar
        st.markdown(get_confidence_bar_html(confidence, signal), unsafe_allow_html=True)
        
        # Additional info
        st.markdown(f'''
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.9rem; margin: 0.2rem 0;">
                Signal confidence: {confidence}%
            </p>
            <p style="color: #ff6666; font-family: Rajdhani; font-size: 0.8rem; margin: 0.2rem 0;">
                Last update: {datetime.now().strftime("%H:%M:%S")}
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_altcoin_signal(coin_data, coin_key):
    """Display altcoin signal card"""
    if coin_data['signal'] == 'BUY':
        card_class = "signal-buy"
        badge_class = "buy-badge"
        badge_text = "BUY"
    else:
        card_class = "signal-sell"
        badge_class = "sell-badge"
        badge_text = "SELL"
    
    st.markdown(f'''
    <div class="{card_class}">
        <div style="text-align: center;">
            <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.3rem;">
                {coin_data['emoji']} {coin_data['name']} ({coin_key})
            </h3>
            <p style="font-family: Orbitron; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">
                ${coin_data['price']:,.4f}
            </p>
            <span class="signal-badge {badge_class}">{badge_text}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Confidence bar
    st.markdown(get_confidence_bar_html(coin_data['confidence'], coin_data['signal']), unsafe_allow_html=True)
    
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
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS CRYPTO TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">TOR/.onion + P_micro SIGNALS • REAL-TIME PRICES • DRAGON FIRE PRECISION</p>', unsafe_allow_html=True)
    
    # UPDATE SIGNALS BUTTON
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">🎯 TOR/.onion + P_micro SIGNALS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🐉 GENERATE SIGNALS", key="refresh_main", use_container_width=True, type="primary"):
            with st.spinner("🔥 Activating dragon fire analysis..."):
                result = analyzer.update_signals()
                if result:
                    st.session_state.last_analysis = result
                    st.success("✅ Signals updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update signals")
    
    # Check if we have analysis data
    if 'last_analysis' not in st.session_state:
        st.info("🔥 Click 'GENERATE SIGNALS' to get TOR/.onion + P_micro trading signals")
        return
    
    analysis = st.session_state.last_analysis
    
    # BTC PANEL (always visible)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 BITCOIN SIGNAL</h2>', unsafe_allow_html=True)
    
    btc_data = analysis['signals']['BTC']
    if btc_data:
        display_btc_panel(btc_data)
        
        # Show global signal reasoning
        with st.expander("📊 Global Signal Analysis", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    label="TOR %",
                    value=f"{analysis['current_tor']:.2f}%",
                    delta=f"{analysis['tor_change']:+.2f}%"
                )
            with col2:
                st.metric(
                    label=".onion %",
                    value=f"{analysis['current_onion']:.2f}%",
                    delta=f"{analysis['onion_change']:+.2f}%"
                )
            with col3:
                st.metric(
                    label="Total Nodes",
                    value=f"{analysis['node_data']['total_nodes']:,}",
                    delta="Bitnodes"
                )
            with col4:
                st.metric(
                    label="Global Signal",
                    value=analysis['global_signal'],
                    delta=analysis['global_reason'][:20] + "..."
                )
            
            st.markdown(f'''
            <div style="background: rgba(255, 0, 0, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <p style="color: #ff8888; font-family: Rajdhani; margin: 0;">
                    <strong>Analysis:</strong> {analysis['global_reason']}
                </p>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.error("❌ No BTC signal data available")
    
    # ALTCOIN SIGNALS (only BUY/SELL, never NEUTRAL)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">⚡ ALTCOIN BATTLEFIELD</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">Showing only active BUY/SELL signals (NEUTRAL signals hidden)</p>', unsafe_allow_html=True)
    
    altcoins_data = analysis['signals']['altcoins']
    if altcoins_data:
        # Group altcoins by signal type
        buy_signals = {k: v for k, v in altcoins_data.items() if v['signal'] == 'BUY'}
        sell_signals = {k: v for k, v in altcoins_data.items() if v['signal'] == 'SELL'}
        
        # Display BUY signals
        if buy_signals:
            st.markdown('<h3 style="font-family: Orbitron; color: #00ff00; margin: 1rem 0;">🟢 BUY SIGNALS</h3>', unsafe_allow_html=True)
            buy_cols = st.columns(min(3, len(buy_signals)))
            
            for idx, (coin_key, coin_data) in enumerate(buy_signals.items()):
                with buy_cols[idx % len(buy_cols)]:
                    display_altcoin_signal(coin_data, coin_key)
        
        # Display SELL signals
        if sell_signals:
            st.markdown('<h3 style="font-family: Orbitron; color: #ff0000; margin: 1rem 0;">🔴 SELL SIGNALS</h3>', unsafe_allow_html=True)
            sell_cols = st.columns(min(3, len(sell_signals)))
            
            for idx, (coin_key, coin_data) in enumerate(sell_signals.items()):
                with sell_cols[idx % len(sell_cols)]:
                    display_altcoin_signal(coin_data, coin_key)
        
        # Show count summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Total Signals",
                value=len(altcoins_data),
                delta="Active only"
            )
        with col2:
            st.metric(
                label="BUY Signals",
                value=len(buy_signals),
                delta="Long positions"
            )
        with col3:
            st.metric(
                label="SELL Signals",
                value=len(sell_signals),
                delta="Short positions"
            )
    else:
        st.info("ℹ️ No active altcoin signals at this time (all NEUTRAL)")
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • PROPRIETARY TOR/.onion + P_micro TECHNOLOGY</p>
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
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()