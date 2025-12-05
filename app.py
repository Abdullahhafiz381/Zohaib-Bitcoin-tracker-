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

# GODZILLERS CSS with red and black theme
st.markdown("""
<style>
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
    
    .combined-signal-perfect {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 150, 0, 0.4) 100%);
        border: 3px solid #00ff00;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.7);
        animation: pulse-perfect 1.5s infinite;
    }
    
    @keyframes pulse-perfect {
        0% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.7); }
        50% { box-shadow: 0 0 60px rgba(0, 255, 0, 0.9); }
        100% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.7); }
    }
    
    .combined-signal-strong {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.15) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 2px solid #00ff00;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
    }
    
    .combined-signal-moderate {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.15) 0%, rgba(150, 100, 0, 0.3) 100%);
        border: 2px solid #ffa500;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(255, 165, 0, 0.5);
    }
    
    .combined-signal-weak {
        background: linear-gradient(135deg, rgba(255, 100, 100, 0.1) 0%, rgba(100, 0, 0, 0.2) 100%);
        border: 1px solid #ff6464;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 100, 100, 0.3);
    }
    
    .combined-signal-conflict {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(100, 0, 0, 0.3) 100%);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        animation: pulse-conflict 2s infinite;
    }
    
    @keyframes pulse-conflict {
        0% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 45px rgba(255, 0, 0, 0.7); }
        100% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.5); }
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
    
    .hidden-analysis-card {
        background: rgba(10, 0, 0, 0.9);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .analysis-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 8px rgba(255, 0, 0, 0.3);
    }
    
    .badge-buy {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000000;
    }
    
    .badge-sell {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: #ffffff;
    }
    
    .badge-neutral {
        background: linear-gradient(90deg, #ffa500, #ff8c00);
        color: #000000;
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
    
    .confidence-bar {
        height: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
        border: 1px solid rgba(255, 0, 0, 0.3);
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    .confidence-high {
        background: linear-gradient(90deg, #00ff00, #00cc00);
    }
    
    .confidence-medium {
        background: linear-gradient(90deg, #ffa500, #ff8c00);
    }
    
    .confidence-low {
        background: linear-gradient(90deg, #ff4444, #cc0000);
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
    
    .coin-card {
        background: rgba(30, 0, 0, 0.9);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .signal-emoji {
        font-size: 2.5rem;
        text-shadow: 0 0 15px currentColor;
    }
    
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
    """Display login page"""
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
            '>HIDDEN AI SIGNAL WARFARE SYSTEM</p>
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
        for symbol in coins:
            prices[symbol] = 0.0
    
    return prices

class HiddenOrderBookAnalyzer:
    """Hidden Order Book P-micro Analyzer"""
    
    def __init__(self):
        self.order_books = {}
        self.p_micro_values = {}
        self.last_update = {}
        self.analysis_history = {}
    
    def fetch_order_book(self, symbol='BTCUSDT', limit=20):
        """Fetch order book data from Binance API"""
        try:
            url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                bids = [[float(bid[0]), float(bid[1])] for bid in data['bids']]
                asks = [[float(ask[0]), float(ask[1])] for ask in data['asks']]
                
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
            return None
    
    def calculate_p_micro(self, order_book_data, depth=5):
        """Calculate hidden P-micro signal"""
        if not order_book_data:
            return None
            
        bids = order_book_data['bids'][:depth] if order_book_data['bids'] else []
        asks = order_book_data['asks'][:depth] if order_book_data['asks'] else []
        
        if not bids or not asks:
            return None
        
        total_bid_qty = sum(qty for _, qty in bids)
        total_ask_qty = sum(qty for _, qty in asks)
        
        weighted_bid = sum(price * qty for price, qty in bids) / total_bid_qty if total_bid_qty > 0 else 0
        weighted_ask = sum(price * qty for price, qty in asks) / total_ask_qty if total_ask_qty > 0 else 0
        
        p_micro = (weighted_bid * total_bid_qty + weighted_ask * total_ask_qty) / (total_bid_qty + total_ask_qty)
        current_price = order_book_data.get('current_price', 0)
        
        price_diff_percent = ((p_micro - current_price) / current_price * 100) if current_price > 0 else 0
        
        # Hidden P-micro signal logic
        if price_diff_percent > 1.0:
            signal = "STRONG_BUY"
            strength = 95
            reasoning = "P-micro significantly above price (buyers dominant)"
        elif price_diff_percent > 0.2:
            signal = "BUY"
            strength = 75
            reasoning = "P-micro above price (buyers in control)"
        elif price_diff_percent < -1.0:
            signal = "STRONG_SELL"
            strength = 95
            reasoning = "P-micro significantly below price (sellers dominant)"
        elif price_diff_percent < -0.2:
            signal = "SELL"
            strength = 75
            reasoning = "P-micro below price (sellers in control)"
        else:
            signal = "NEUTRAL"
            strength = 50
            reasoning = "P-micro near price (market balanced)"
        
        return {
            'signal': signal,
            'strength': strength,
            'p_micro': p_micro,
            'current_price': current_price,
            'price_diff_percent': price_diff_percent,
            'weighted_bid': weighted_bid,
            'weighted_ask': weighted_ask,
            'total_bid_qty': total_bid_qty,
            'total_ask_qty': total_ask_qty,
            'reasoning': reasoning,
            'timestamp': datetime.now().isoformat()
        }
    
    def update_all_order_books(self, symbols=None):
        """Update hidden order books for all symbols"""
        if symbols is None:
            symbols = ['BTCUSDT', 'ETHUSDT']
        
        for symbol in symbols:
            order_book = self.fetch_order_book(symbol)
            if order_book:
                self.order_books[symbol] = order_book
                p_micro_data = self.calculate_p_micro(order_book)
                if p_micro_data:
                    self.p_micro_values[symbol] = p_micro_data
                    self.last_update[symbol] = datetime.now()
                    
                    # Store in history
                    if symbol not in self.analysis_history:
                        self.analysis_history[symbol] = []
                    self.analysis_history[symbol].append(p_micro_data)
                    
                    # Keep only last 10 analyses
                    if len(self.analysis_history[symbol]) > 10:
                        self.analysis_history[symbol] = self.analysis_history[symbol][-10:]

class HiddenTorAnalyzer:
    """Hidden Tor Network Analyzer"""
    
    def __init__(self, data_file="hidden_network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.current_data = None
        self.previous_data = None
        self.last_update = None
        self.analysis_history = []
        self.load_hidden_data()
    
    def load_hidden_data(self):
        """Load hidden network data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.current_data = data.get('current_data')
                    self.previous_data = data.get('previous_data')
                    self.last_update = data.get('last_update')
                    self.analysis_history = data.get('analysis_history', [])
        except Exception as e:
            self.current_data = None
            self.previous_data = None
            self.last_update = None
            self.analysis_history = []
    
    def save_hidden_data(self):
        """Save hidden network data"""
        try:
            data = {
                'current_data': self.current_data,
                'previous_data': self.previous_data,
                'last_update': self.last_update,
                'analysis_history': self.analysis_history[-20:],  # Keep last 20
                'last_saved': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            pass  # Silent save
    
    def fetch_hidden_network_data(self):
        """Fetch hidden network data"""
        try:
            response = requests.get(self.bitnodes_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_nodes = data['total_nodes']
                active_nodes = 0
                tor_nodes = 0
                
                for node_address, node_info in data['nodes'].items():
                    if node_info and isinstance(node_info, list) and len(node_info) > 0:
                        active_nodes += 1
                    if '.onion' in str(node_address) or '.onion' in str(node_info):
                        tor_nodes += 1
                
                tor_percentage = (tor_nodes / total_nodes) * 100 if total_nodes > 0 else 0
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_nodes': total_nodes,
                    'active_nodes': active_nodes,
                    'tor_nodes': tor_nodes,
                    'tor_percentage': tor_percentage
                }
            return None
        except Exception as e:
            return None
    
    def analyze_hidden_tor_signal(self):
        """Generate hidden Tor signal"""
        if not self.current_data or not self.previous_data:
            return {
                'signal': 'NEUTRAL',
                'strength': 50,
                'reasoning': 'Insufficient data for analysis',
                'tor_change': 0,
                'tor_percentage': 0
            }
        
        current_tor = self.current_data['tor_percentage']
        previous_tor = self.previous_data['tor_percentage']
        tor_change = current_tor - previous_tor
        
        # Hidden Tor signal logic (reverse of what users might expect)
        if tor_change > 2.0:  # Large increase in Tor nodes
            signal = "STRONG_SELL"
            strength = 90
            reasoning = f"Tor nodes increased sharply ({tor_change:+.2f}%) - Hidden selling pressure"
        elif tor_change > 0.5:  # Moderate increase
            signal = "SELL"
            strength = 70
            reasoning = f"Tor nodes increasing ({tor_change:+.2f}%) - Bearish hidden activity"
        elif tor_change < -2.0:  # Large decrease
            signal = "STRONG_BUY"
            strength = 90
            reasoning = f"Tor nodes decreased sharply ({tor_change:+.2f}%) - Hidden buying pressure"
        elif tor_change < -0.5:  # Moderate decrease
            signal = "BUY"
            strength = 70
            reasoning = f"Tor nodes decreasing ({tor_change:+.2f}%) - Bullish hidden activity"
        else:
            signal = "NEUTRAL"
            strength = 50
            reasoning = f"Tor nodes stable ({tor_change:+.2f}%) - No hidden signals"
        
        return {
            'signal': signal,
            'strength': strength,
            'tor_change': tor_change,
            'tor_percentage': current_tor,
            'reasoning': reasoning,
            'timestamp': datetime.now().isoformat()
        }
    
    def update_hidden_analysis(self):
        """Update hidden Tor analysis"""
        new_data = self.fetch_hidden_network_data()
        if not new_data:
            return False
        
        self.previous_data = self.current_data
        self.current_data = new_data
        self.last_update = datetime.now().isoformat()
        
        # Generate signal
        tor_signal = self.analyze_hidden_tor_signal()
        self.analysis_history.append(tor_signal)
        
        self.save_hidden_data()
        return True

class HiddenSignalCombiner:
    """Combine hidden signals from Order Book and Tor analyzers"""
    
    def __init__(self):
        self.order_book_analyzer = HiddenOrderBookAnalyzer()
        self.tor_analyzer = HiddenTorAnalyzer()
        self.combined_signals = {}
    
    def update_all_hidden_data(self):
        """Update all hidden analyzers"""
        # Update order books
        self.order_book_analyzer.update_all_order_books(['BTCUSDT', 'ETHUSDT'])
        
        # Update Tor analysis
        self.tor_analyzer.update_hidden_analysis()
        
        # Generate combined signals
        self.generate_combined_signals()
    
    def generate_combined_signals(self):
        """Generate combined hidden signals"""
        symbols = ['BTCUSDT', 'ETHUSDT']
        
        for symbol in symbols:
            p_micro_signal = self.order_book_analyzer.p_micro_values.get(symbol)
            tor_signal = self.tor_analyzer.analyze_hidden_tor_signal()
            
            if not p_micro_signal or not tor_signal:
                continue
            
            # Calculate combined confidence
            if p_micro_signal['signal'] == tor_signal['signal']:
                # Both agree - perfect signal
                if "STRONG" in p_micro_signal['signal'] and "STRONG" in tor_signal['signal']:
                    confidence = 100
                    combined_signal = "PERFECT_CONFIRMED_" + p_micro_signal['signal']
                else:
                    confidence = 85
                    combined_signal = "CONFIRMED_" + p_micro_signal['signal']
                
                signal_class = "perfect" if confidence >= 95 else "strong"
                
            elif (p_micro_signal['signal'] in ["BUY", "STRONG_BUY"] and 
                  tor_signal['signal'] in ["SELL", "STRONG_SELL"]) or \
                 (p_micro_signal['signal'] in ["SELL", "STRONG_SELL"] and 
                  tor_signal['signal'] in ["BUY", "STRONG_BUY"]):
                # Complete conflict
                confidence = 30
                combined_signal = "CONFLICT_SIGNAL"
                signal_class = "conflict"
                
            else:
                # Partial agreement or neutral
                avg_strength = (p_micro_signal['strength'] + tor_signal['strength']) / 2
                confidence = int(avg_strength * 0.8)  # Reduce confidence for partial agreement
                
                if "STRONG" in p_micro_signal['signal']:
                    combined_signal = "LEANING_" + p_micro_signal['signal']
                else:
                    combined_signal = "MODERATE_" + p_micro_signal['signal']
                
                signal_class = "moderate" if confidence >= 60 else "weak"
            
            # Generate final action signal
            if "BUY" in combined_signal:
                action_signal = "🚀 STRONG BUY" if confidence >= 90 else "🟢 BUY" if confidence >= 70 else "📈 MILD BUY"
                action_emoji = "🚀" if confidence >= 90 else "🟢" if confidence >= 70 else "📈"
            elif "SELL" in combined_signal:
                action_signal = "💀 STRONG SELL" if confidence >= 90 else "🔴 SELL" if confidence >= 70 else "📉 MILD SELL"
                action_emoji = "💀" if confidence >= 90 else "🔴" if confidence >= 70 else "📉"
            else:
                action_signal = "⚖️ HOLD/NEUTRAL"
                action_emoji = "⚖️"
            
            self.combined_signals[symbol] = {
                'symbol': symbol,
                'action_signal': action_signal,
                'action_emoji': action_emoji,
                'confidence': confidence,
                'signal_class': signal_class,
                'p_micro_signal': p_micro_signal['signal'],
                'p_micro_strength': p_micro_signal['strength'],
                'tor_signal': tor_signal['signal'],
                'tor_strength': tor_signal['strength'],
                'p_micro_reasoning': p_micro_signal['reasoning'],
                'tor_reasoning': tor_signal['reasoning'],
                'current_price': p_micro_signal.get('current_price', 0),
                'p_micro_value': p_micro_signal.get('p_micro', 0),
                'timestamp': datetime.now().isoformat()
            }

def get_coin_display_name(symbol):
    """Get display name for crypto symbols"""
    names = {
        'BTCUSDT': 'BITCOIN',
        'ETHUSDT': 'ETHEREUM'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols"""
    emojis = {
        'BTCUSDT': '🐲',
        'ETHUSDT': '🔥'
    }
    return emojis.get(symbol, '💀')

def display_hidden_analysis_metrics(combined_signal):
    """Display hidden analysis metrics in collapsed view"""
    with st.expander("🔍 VIEW HIDDEN ANALYSIS DETAILS", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏹 ORDER BOOK ANALYSIS")
            st.markdown(f"**Signal:** `{combined_signal['p_micro_signal']}`")
            st.markdown(f"**Strength:** `{combined_signal['p_micro_strength']}%`")
            st.markdown(f"**P-micro Value:** `${combined_signal['p_micro_value']:,.2f}`")
            st.markdown(f"**Current Price:** `${combined_signal['current_price']:,.2f}`")
            st.markdown(f"**Reasoning:** {combined_signal['p_micro_reasoning']}")
        
        with col2:
            st.markdown("### 🌐 TOR NETWORK ANALYSIS")
            st.markdown(f"**Signal:** `{combined_signal['tor_signal']}`")
            st.markdown(f"**Strength:** `{combined_signal['tor_strength']}%`")
            st.markdown(f"**Reasoning:** {combined_signal['tor_reasoning']}")

def display_confidence_bar(confidence):
    """Display confidence bar"""
    st.markdown(f"**AI CONFIDENCE:** {confidence}%")
    
    if confidence >= 90:
        fill_class = "confidence-high"
        fill_width = "100%"
    elif confidence >= 70:
        fill_class = "confidence-medium"
        fill_width = f"{confidence}%"
    else:
        fill_class = "confidence-low"
        fill_width = f"{confidence}%"
    
    st.markdown(f'''
    <div class="confidence-bar">
        <div class="confidence-fill {fill_class}" style="width: {fill_width};"></div>
    </div>
    ''', unsafe_allow_html=True)

def main_app():
    """Main application after login"""
    # Initialize hidden signal combiner
    if 'hidden_combiner' not in st.session_state:
        st.session_state.hidden_combiner = HiddenSignalCombiner()
    
    hidden_combiner = st.session_state.hidden_combiner
    
    # Logout button
    if st.button("🚪 LOGOUT", key="logout", use_container_width=False):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Welcome message
    st.markdown(f'<p style="text-align: right; color: #ff4444; font-family: Orbitron; margin: 0.5rem 1rem;">DRAGON COMMANDER: {st.session_state.username}</p>', unsafe_allow_html=True)
    
    # GODZILLERS Header
    st.markdown('<h1 class="godzillers-header">🐲 GODZILLERS HIDDEN AI WARFARE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">DUAL-ANALYSIS SYSTEM • HIDDEN SIGNALS • 100% AI CONFIDENCE</p>', unsafe_allow_html=True)
    
    # UPDATE SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 HIDDEN AI ANALYSIS SYSTEM</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("⚡ ACTIVATE HIDDEN ANALYSIS", key="activate_analysis", use_container_width=True, type="primary"):
            with st.spinner("🔥 Activating hidden AI warfare systems..."):
                hidden_combiner.update_all_hidden_data()
                st.success("✅ Hidden analysis complete!")
                st.rerun()
    
    # Check if analysis has been run
    if not hidden_combiner.combined_signals:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h3 style="color: #ff4444; font-family: Orbitron;">🚨 NO HIDDEN ANALYSIS DETECTED</h3>
            <p style="color: #ff8888; font-family: Rajdhani;">Click "ACTIVATE HIDDEN ANALYSIS" to unleash the dragon fire signals</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # COMBINED AI SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">⚡ COMBINED AI WARFARE SIGNALS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ff8888; font-family: Rajdhani; text-align: center;">ORDER BOOK + TOR NETWORK HIDDEN ANALYSIS • REAL-TIME AI INTELLIGENCE</p>', unsafe_allow_html=True)
    
    # Display combined signals
    for symbol in ['BTCUSDT', 'ETHUSDT']:
        combined_signal = hidden_combiner.combined_signals.get(symbol)
        
        if not combined_signal:
            continue
        
        emoji = get_coin_emoji(symbol)
        name = get_coin_display_name(symbol)
        signal_class = combined_signal['signal_class']
        
        # Determine CSS class
        if signal_class == "perfect":
            css_class = "combined-signal-perfect"
        elif signal_class == "strong":
            css_class = "combined-signal-strong"
        elif signal_class == "moderate":
            css_class = "combined-signal-moderate"
        elif signal_class == "conflict":
            css_class = "combined-signal-conflict"
        else:
            css_class = "combined-signal-weak"
        
        # Display main signal
        st.markdown(f'''
        <div class="{css_class}">
            <div style="text-align: center;">
                <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <span class="signal-emoji" style="color: {'#00ff00' if 'BUY' in combined_signal['action_signal'] else '#ff0000' if 'SELL' in combined_signal['action_signal'] else '#ffa500'}">
                        {combined_signal['action_emoji']}
                    </span>
                    <h3 style="font-family: Orbitron; margin: 0; font-size: 1.8rem;">{emoji} {name}</h3>
                    <span class="signal-emoji" style="color: {'#00ff00' if 'BUY' in combined_signal['action_signal'] else '#ff0000' if 'SELL' in combined_signal['action_signal'] else '#ffa500'}">
                        {combined_signal['action_emoji']}
                    </span>
                </div>
                
                <h2 style="font-family: Orbitron; font-size: 2.5rem; margin: 0.5rem 0; color: {'#00ff00' if 'BUY' in combined_signal['action_signal'] else '#ff0000' if 'SELL' in combined_signal['action_signal'] else '#ffa500'}">
                    {combined_signal['action_signal']}
                </h2>
                
                <div style="margin: 1.5rem 0;">
                    <p style="color: #ffd700; font-family: Orbitron; font-size: 1.2rem; margin: 0.5rem 0;">
                        🐲 HIDDEN AI CONFIDENCE LEVEL 🐲
                    </p>
                    {display_confidence_bar(combined_signal['confidence'])}
                </div>
                
                <div style="display: flex; justify-content: center; gap: 1rem; margin: 1rem 0;">
                    <span class="analysis-badge {'badge-buy' if 'BUY' in combined_signal['p_micro_signal'] else 'badge-sell' if 'SELL' in combined_signal['p_micro_signal'] else 'badge-neutral'}">
                        ORDER BOOK: {combined_signal['p_micro_signal']}
                    </span>
                    <span class="analysis-badge {'badge-buy' if 'BUY' in combined_signal['tor_signal'] else 'badge-sell' if 'SELL' in combined_signal['tor_signal'] else 'badge-neutral'}">
                        TOR NETWORK: {combined_signal['tor_signal']}
                    </span>
                </div>
                
                <p style="color: #ffffff; font-family: Rajdhani; font-size: 1rem; margin: 1rem 0; padding: 0 2rem;">
                    💎 Current Price: <strong>${combined_signal['current_price']:,.2f}</strong> • 
                    🏹 P-micro: <strong>${combined_signal['p_micro_value']:,.2f}</strong>
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Display hidden analysis details
        display_hidden_analysis_metrics(combined_signal)
        
        st.markdown('<div class="divider" style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    
    # LIVE PRICES SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE BATTLEFIELD PRICES</h2>', unsafe_allow_html=True)
    
    prices = get_crypto_prices()
    
    if prices:
        # Display BTC price
        btc_price = prices.get('BTCUSDT')
        if btc_price:
            # Get BTC signal
            btc_signal = hidden_combiner.combined_signals.get('BTCUSDT', {})
            signal_color = "#00ff00" if "BUY" in btc_signal.get('action_signal', '') else "#ff0000" if "SELL" in btc_signal.get('action_signal', '') else "#ffa500"
            
            st.markdown(f'''
            <div class="price-glow">
                <div style="text-align: center;">
                    <h3 style="font-family: Orbitron; color: #ff4444; margin: 0.5rem 0;">🐲 BITCOIN</h3>
                    <p style="font-family: Orbitron; font-size: 3.5rem; font-weight: 900; margin: 0.5rem 0; background: linear-gradient(90deg, #ff0000, #ff4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        ${btc_price:,.2f}
                    </p>
                    <p style="color: {signal_color}; font-family: Orbitron; font-size: 1.2rem; margin: 0.5rem 0;">
                        {btc_signal.get('action_signal', '⚡ NO SIGNAL')}
                    </p>
                    <p style="color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">
                        AI Confidence: {btc_signal.get('confidence', 0)}%
                    </p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Display other coins
        cols = st.columns(3)
        other_coins = [
            ('ETHUSDT', '🔥'),
            ('BNBUSDT', '💰'),
            ('SOLUSDT', '⚡')
        ]
        
        for idx, (symbol, coin_emoji) in enumerate(other_coins):
            price = prices.get(symbol)
            if price:
                with cols[idx]:
                    st.markdown(f'''
                    <div class="coin-card">
                        <div style="text-align: center;">
                            <h4 style="font-family: Orbitron; color: #ff4444; margin: 0.5rem 0;">{coin_emoji} {get_coin_display_name(symbol) if symbol in ['BTCUSDT', 'ETHUSDT'] else symbol.replace('USDT', '')}</h4>
                            <p style="font-family: Orbitron; font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">${price:,.2f}</p>
                            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.9rem; margin: 0;">{symbol}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    
    # HIDDEN SYSTEM STATUS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.expander("🔧 HIDDEN SYSTEM STATUS", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            # Order Book Status
            btc_order_book = hidden_combiner.order_book_analyzer.order_books.get('BTCUSDT')
            if btc_order_book:
                last_update = hidden_combiner.order_book_analyzer.last_update.get('BTCUSDT')
                time_diff = (datetime.now() - last_update).seconds if last_update else "N/A"
                
                st.metric(
                    label="ORDER BOOK SYSTEM",
                    value="ACTIVE",
                    delta=f"Updated {time_diff}s ago"
                )
            else:
                st.metric(
                    label="ORDER BOOK SYSTEM",
                    value="INACTIVE",
                    delta="Awaiting activation"
                )
        
        with col2:
            # Tor Network Status
            if hidden_combiner.tor_analyzer.current_data:
                tor_percentage = hidden_combiner.tor_analyzer.current_data.get('tor_percentage', 0)
                st.metric(
                    label="TOR NETWORK SYSTEM",
                    value="ANALYZING",
                    delta=f"{tor_percentage:.1f}% Tor nodes"
                )
            else:
                st.metric(
                    label="TOR NETWORK SYSTEM",
                    value="INACTIVE",
                    delta="Awaiting activation"
                )
        
        # Combined System Status
        if hidden_combiner.combined_signals:
            btc_signal = hidden_combiner.combined_signals.get('BTCUSDT', {})
            confidence = btc_signal.get('confidence', 0)
            
            if confidence >= 90:
                status = "PERFECT ALIGNMENT"
                color = "#00ff00"
            elif confidence >= 70:
                status = "STRONG ALIGNMENT"
                color = "#00ff00"
            elif confidence >= 50:
                status = "MODERATE ALIGNMENT"
                color = "#ffa500"
            else:
                status = "WEAK/CONFLICT"
                color = "#ff0000"
            
            st.markdown(f'''
            <div style="text-align: center; margin-top: 1rem;">
                <p style="color: {color}; font-family: Orbitron; font-size: 1.2rem;">
                    🛡️ COMBINED SYSTEM STATUS: {status}
                </p>
                <p style="color: #ff8888; font-family: Rajdhani;">
                    Systems aligned for maximum signal accuracy
                </p>
            </div>
            ''', unsafe_allow_html=True)
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS HIDDEN AI WARFARE SYSTEM 🔥</p>
    <p>© 2025 GODZILLERS • PROPRIETARY HIDDEN ANALYSIS TECHNOLOGY</p>
    <p style="font-size: 0.7rem; color: #ff6666;">DUAL-ANALYSIS: ORDER BOOK P-micro + TOR NETWORK • 100% AI CONFIDENCE WHEN ALIGNED</p>
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