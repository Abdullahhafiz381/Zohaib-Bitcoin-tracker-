# app.py - GODZILLERS MATHEMATICAL SIGNALS - CLEAN VERSION
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
import ccxt

# GODZILLERS Streamlit setup
st.set_page_config(
    page_title="🔥 GODZILLERS MATHEMATICAL SIGNALS",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GODZILLERS CSS - Clean Premium Design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a000a 50%, #00001a 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a000a 50%, #00001a 100%);
    }
    
    .godzillers-header {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 0, 255, 0.7);
        letter-spacing: 3px;
    }
    
    .godzillers-subheader {
        color: #ff66ff;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* CLEAN SIGNAL CARDS */
    .clean-buy-signal {
        background: linear-gradient(135deg, 
            rgba(0, 255, 0, 0.05) 0%, 
            rgba(0, 150, 0, 0.15) 100%);
        border: 3px solid #00ff00;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.3),
                    inset 0 0 20px rgba(0, 255, 0, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .clean-buy-signal:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 50px rgba(0, 255, 0, 0.4),
                    inset 0 0 30px rgba(0, 255, 0, 0.1);
    }
    
    .clean-sell-signal {
        background: linear-gradient(135deg, 
            rgba(255, 0, 0, 0.05) 0%, 
            rgba(150, 0, 0, 0.15) 100%);
        border: 3px solid #ff0000;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.3),
                    inset 0 0 20px rgba(255, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .clean-sell-signal:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.4),
                    inset 0 0 30px rgba(255, 0, 0, 0.1);
    }
    
    /* CONFIDENCE BADGES */
    .clean-confidence-95 {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .clean-confidence-90 {
        background: linear-gradient(90deg, #99ff00, #66cc00);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 0 15px rgba(153, 255, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .clean-confidence-85 {
        background: linear-gradient(90deg, #ffff00, #cccc00);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 0 15px rgba(255, 255, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* LEVERAGE BADGES */
    .clean-leverage-max {
        background: linear-gradient(90deg, #ff00ff, #cc00cc);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .clean-leverage-low {
        background: linear-gradient(90deg, #ff9900, #cc6600);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 0 15px rgba(255, 153, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* LOGIN STYLES */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #000000 0%, #0a000a 50%, #00001a 100%);
        padding: 20px;
    }
    
    .login-card {
        background: rgba(10, 0, 20, 0.95);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 0, 255, 0.6);
        border-radius: 20px;
        padding: 3rem;
        width: 100%;
        max-width: 450px;
        box-shadow: 0 0 50px rgba(255, 0, 255, 0.5);
        text-align: center;
    }
    
    .login-header {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 0, 255, 0.7);
    }
    
    .login-subheader {
        color: #ff66ff;
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .login-input {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(255, 0, 255, 0.5);
        border-radius: 10px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        width: 100%;
        font-size: 1rem;
    }
    
    .login-button {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        border: none;
        border-radius: 25px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.75rem 2rem;
        margin: 1rem 0;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.1rem;
    }
    
    .logout-button {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        border: none;
        border-radius: 10px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        padding: 0.5rem 1rem;
        margin: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ff00ff 25%, #00ffff 75%, transparent 100%);
        margin: 2.5rem 0;
    }
    
    /* NO SIGNALS STYLE */
    .no-signals {
        background: rgba(20, 0, 40, 0.7);
        border: 2px dashed rgba(255, 0, 255, 0.3);
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* SCAN BUTTON */
    .scan-button {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron' !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.75rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .scan-button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MATHEMATICAL EQUATIONS CLASS ====================
class MathematicalEquations:
    """Implementation of ALL 8 mathematical equations - ONLY HIGH CONFIDENCE"""
    
    def __init__(self):
        # HIGH CONFIDENCE parameters
        self.HIGH_CONFIDENCE_THRESHOLD = 85  # Only show signals >= 85%
        self.ORDERBOOK_DEPTH = 15
        self.VOLATILITY_WINDOW = 25
        self.BASE_LEVERAGE = 6
        self.price_history = {}
        
        # Initialize exchange for order book data
        self.exchange = None
        self.init_exchange()
    
    def init_exchange(self):
        """Initialize exchange connection for order book data"""
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })
            self.exchange.load_markets()
        except:
            try:
                self.exchange = ccxt.okx({
                    'enableRateLimit': True,
                    'options': {'defaultType': 'swap'}
                })
                self.exchange.load_markets()
            except:
                self.exchange = None
    
    def fetch_orderbook_data(self, symbol):
        """Fetch order book data for mathematical equations"""
        if not self.exchange:
            return None
        
        try:
            # Try with the given symbol first
            try:
                orderbook = self.exchange.fetch_order_book(symbol, self.ORDERBOOK_DEPTH)
                ticker = self.exchange.fetch_ticker(symbol)
            except:
                # Try with USDT pair
                if not symbol.endswith('/USDT'):
                    symbol_usdt = symbol + '/USDT'
                    orderbook = self.exchange.fetch_order_book(symbol_usdt, self.ORDERBOOK_DEPTH)
                    ticker = self.exchange.fetch_ticker(symbol_usdt)
                else:
                    return None
            
            # Extract data for equations
            bid = ticker['bid'] if ticker['bid'] else orderbook['bids'][0][0]
            ask = ticker['ask'] if ticker['ask'] else orderbook['asks'][0][0]
            mid_price = (bid + ask) / 2
            
            # Calculate order book volumes (Equation 2)
            bids = orderbook['bids'][:self.ORDERBOOK_DEPTH]
            asks = orderbook['asks'][:self.ORDERBOOK_DEPTH]
            
            bid_volume = sum(b[1] for b in bids)
            ask_volume = sum(a[1] for a in asks)
            
            # Store price for volatility calculation
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            
            self.price_history[symbol].append(mid_price)
            if len(self.price_history[symbol]) > self.VOLATILITY_WINDOW:
                self.price_history[symbol] = self.price_history[symbol][-self.VOLATILITY_WINDOW:]
            
            return {
                'bid': bid,
                'ask': ask,
                'mid_price': mid_price,
                'bid_volume': bid_volume,
                'ask_volume': ask_volume,
                'spread': ask - bid,
                'price_history': self.price_history[symbol]
            }
        except Exception as e:
            return None
    
    def calculate_volatility(self, price_history):
        """Equation 6: σ̂_t = StdDev(returns)"""
        if len(price_history) < 2:
            return 0.01
        
        returns = np.diff(np.log(price_history))
        return float(np.std(returns, ddof=1))
    
    def generate_high_confidence_signal(self, symbol):
        """Generate HIGH CONFIDENCE signal using ALL 8 mathematical equations"""
        data = self.fetch_orderbook_data(symbol)
        
        if not data:
            return None
        
        # Equation 1: Mid Price (already calculated)
        P_t = data['mid_price']
        
        # Equation 2: Order Book Volumes (already calculated)
        V_bid = data['bid_volume']
        V_ask = data['ask_volume']
        
        # Equation 3: Order Book Imbalance
        total_volume = V_bid + V_ask
        if total_volume > 0:
            I_t = (V_bid - V_ask) / total_volume
        else:
            I_t = 0
        
        # Equation 4: Spread
        S_t = data['spread']
        
        # Equation 5: Relative Spread
        if P_t > 0:
            phi_t = S_t / P_t
        else:
            phi_t = 0.0001
        
        # Equation 6: Volatility
        sigma_t = self.calculate_volatility(data['price_history'])
        
        # Equation 7: Signal Strength
        if phi_t > 0 and sigma_t > 0:
            signal_strength = np.sign(I_t) * (abs(I_t) / (phi_t * sigma_t))
        else:
            signal_strength = 0
        
        # Determine direction
        if I_t > phi_t:
            direction = "BUY"
            action = "LONG"
        elif I_t < -phi_t:
            direction = "SELL"
            action = "SHORT"
        else:
            return None
        
        # Convert signal strength to percentage
        abs_signal = abs(signal_strength)
        if abs_signal < 1.0:
            strength_pct = 70 + int((abs_signal - 0.5) * 30) if abs_signal > 0.5 else 0
        else:
            strength_pct = 85 + min(14, int((abs_signal - 1.0) * 10))
        
        # ONLY RETURN HIGH CONFIDENCE SIGNALS (>= 85%)
        if strength_pct < self.HIGH_CONFIDENCE_THRESHOLD:
            return None
        
        # Equation 8: Max Leverage (for display only)
        if sigma_t > 0:
            max_leverage = 1 + (self.BASE_LEVERAGE / sigma_t)
            max_leverage = min(10, max_leverage)
        else:
            max_leverage = 3
        
        # Determine leverage indication
        if strength_pct >= 90:
            leverage_indication = "MAX LEVERAGE"
        else:
            leverage_indication = "LOW LEVERAGE"
        
        return {
            'direction': direction,
            'action': action,
            'strength_pct': strength_pct,
            'leverage': leverage_indication,
            'max_leverage_value': round(max_leverage, 1),
            'price': round(P_t, 4)
        }

# ==================== MATHEMATICAL SIGNAL SYSTEM ====================
class MathematicalSignalSystem:
    """Pure mathematical system showing only HIGH CONFIDENCE signals"""
    
    def __init__(self):
        self.math_equations = MathematicalEquations()
        # Your specific coins list
        self.trading_pairs = [
            "BTC/USDT", "ETH/USDT", "SUI/USDT", "LINK/USDT", "SOL/USDT",
            "XRP/USDT", "TAO/USDT", "ENA/USDT", "ADA/USDT", "DOGE/USDT", "BRETT/USDT"
        ]
    
    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            # Remove slash for Binance API
            binance_symbol = symbol.replace("/", "")
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
            else:
                return None
        except:
            return None
    
    def scan_all_coins(self):
        """Scan all 11 coins for HIGH CONFIDENCE mathematical signals"""
        high_confidence_signals = []
        
        for pair in self.trading_pairs:
            # Get mathematical signal
            math_signal = self.math_equations.generate_high_confidence_signal(pair)
            
            if math_signal:
                # Get current price
                current_price = self.get_current_price(pair)
                
                signal_data = {
                    'symbol': pair.replace("/", ""),
                    'display_symbol': pair,
                    'direction': math_signal['direction'],
                    'strength_pct': math_signal['strength_pct'],
                    'leverage': math_signal['leverage'],
                    'max_leverage_value': math_signal['max_leverage_value'],
                    'price': math_signal['price'],
                    'current_price': current_price if current_price else math_signal['price'],
                    'timestamp': datetime.now().isoformat()
                }
                high_confidence_signals.append(signal_data)
            
            time.sleep(0.1)  # Rate limiting
        
        # Sort by signal strength (highest first)
        high_confidence_signals.sort(key=lambda x: x['strength_pct'], reverse=True)
        
        return high_confidence_signals

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
            background: rgba(10, 0, 20, 0.95);
            border: 2px solid rgba(255, 0, 255, 0.6);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(255, 0, 255, 0.5);
            text-align: center;
            margin: 2rem 0;
        '>
            <h1 style='
                background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: Orbitron, monospace;
                font-weight: 900;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                text-shadow: 0 0 20px rgba(255, 0, 255, 0.7);
            '>🐲 GODZILLERS</h1>
            <p style='
                color: #ff66ff;
                font-family: Orbitron, monospace;
                font-size: 1rem;
                margin-bottom: 2rem;
                letter-spacing: 2px;
            '>MATHEMATICAL SIGNALS | HIGH CONFIDENCE ONLY</p>
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

# ==================== COIN INFORMATION ====================
def get_coin_info(symbol):
    """Get detailed coin information"""
    coin_info = {
        'BTCUSDT': {'name': 'Bitcoin', 'emoji': '🐲', 'color': '#FF9900'},
        'ETHUSDT': {'name': 'Ethereum', 'emoji': '🔥', 'color': '#3C3C3D'},
        'SUIUSDT': {'name': 'Sui', 'emoji': '💧', 'color': '#6FCF97'},
        'LINKUSDT': {'name': 'Chainlink', 'emoji': '🔗', 'color': '#2A5ADA'},
        'SOLUSDT': {'name': 'Solana', 'emoji': '☀️', 'color': '#00FFA3'},
        'XRPUSDT': {'name': 'Ripple', 'emoji': '✖️', 'color': '#23292F'},
        'TAOUSDT': {'name': 'Bittensor', 'emoji': '🧠', 'color': '#FF6B00'},
        'ENAUSDT': {'name': 'Ethena', 'emoji': '⚡', 'color': '#3A86FF'},
        'ADAUSDT': {'name': 'Cardano', 'emoji': '🔷', 'color': '#0033AD'},
        'DOGEUSDT': {'name': 'Dogecoin', 'emoji': '🐕', 'color': '#C2A633'},
        'BRETTUSDT': {'name': 'Brett', 'emoji': '🤖', 'color': '#FF6B6B'}
    }
    return coin_info.get(symbol, {'name': symbol, 'emoji': '💀', 'color': '#666666'})

def get_confidence_badge(strength_pct):
    """Get confidence badge based on strength percentage"""
    if strength_pct >= 95:
        return "clean-confidence-95"
    elif strength_pct >= 90:
        return "clean-confidence-90"
    else:
        return "clean-confidence-85"

def display_clean_signal(signal):
    """Display clean mathematical signal with beautiful interface"""
    coin_info = get_coin_info(signal['symbol'])
    
    # Signal container class
    signal_class = "clean-buy-signal" if signal['direction'] == "BUY" else "clean-sell-signal"
    
    # Confidence badge class
    confidence_class = get_confidence_badge(signal['strength_pct'])
    
    # Leverage badge class
    leverage_class = "clean-leverage-max" if "MAX" in signal['leverage'] else "clean-leverage-low"
    
    # Format price
    price_formatted = f"${signal['price']:,.2f}"
    
    st.markdown(f'''
    <div class="{signal_class}">
        <!-- HEADER -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div>
                <h3 style="font-family: Orbitron; font-size: 1.8rem; margin: 0; color: {coin_info['color']};">
                    {coin_info['emoji']} {coin_info['name']}
                </h3>
                <p style="color: #aaa; font-size: 0.9rem; margin: 0.2rem 0;">{signal['symbol']}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-family: Orbitron; font-size: 2.5rem; font-weight: 900; margin: 0; 
                   color: {'#00ff00' if signal['direction'] == 'BUY' else '#ff0000'};">
                    {signal['direction']}
                </p>
            </div>
        </div>
        
        <!-- CONFIDENCE & LEVERAGE -->
        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
            <div style="flex: 1;">
                <div class="{confidence_class}" style="text-align: center;">
                    {signal['strength_pct']}% CONFIDENCE
                </div>
            </div>
            <div style="flex: 1;">
                <div class="{leverage_class}" style="text-align: center;">
                    {signal['leverage']}
                </div>
            </div>
        </div>
        
        <!-- PRICE -->
        <div style="text-align: center;">
            <p style="color: {coin_info['color']}; font-family: Orbitron; font-size: 2rem; font-weight: 700; margin: 0;">
                {price_formatted}
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ==================== MAIN APP ====================
def main_app():
    """Main application after login"""
    # Initialize mathematical system
    if 'math_system' not in st.session_state:
        st.session_state.math_system = MathematicalSignalSystem()
    if 'signals' not in st.session_state:
        st.session_state.signals = []
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = None
    
    # Logout button
    if st.button("🚪 LOGOUT", key="logout", use_container_width=False):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Welcome message
    st.markdown(f'<p style="text-align: right; color: #ff00ff; font-family: Orbitron; margin: 0.5rem 1rem;">Welcome, {st.session_state.username}!</p>', unsafe_allow_html=True)
    
    # GODZILLERS Header
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS MATHEMATICAL SIGNALS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">HIGH CONFIDENCE ONLY | 8 EQUATIONS | CLEAN INTERFACE</p>', unsafe_allow_html=True)
    
    # Scan button
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scan_button = st.button("✨ SCAN FOR HIGH CONFIDENCE SIGNALS", 
                              key="scan_math", 
                              use_container_width=True, 
                              type="primary")
    
    if scan_button:
        with st.spinner("🔮 Calculating high-confidence mathematical signals..."):
            # Scan for signals
            st.session_state.signals = st.session_state.math_system.scan_all_coins()
            st.session_state.last_scan = datetime.now()
            
            if st.session_state.signals:
                st.success(f"🎯 Found {len(st.session_state.signals)} high-confidence signals!")
            else:
                st.warning("⚠️ No high-confidence signals found (≥85% confidence required)")
    
    # Last scan info
    if st.session_state.last_scan:
        scan_time = st.session_state.last_scan.strftime("%H:%M:%S")
        
        # Calculate time since last scan
        time_since = datetime.now() - st.session_state.last_scan
        minutes_ago = int(time_since.total_seconds() / 60)
        
        st.markdown(f'''
        <div style="background: rgba(20, 0, 40, 0.7); border: 1px solid rgba(255, 0, 255, 0.3); 
                 border-radius: 10px; padding: 1rem; text-align: center; margin: 1rem 0;">
            <p style="color: #ff66ff; font-family: Orbitron; margin: 0.2rem 0; font-size: 1rem;">
                Last scan: {scan_time} • {minutes_ago} minutes ago
            </p>
            <p style="color: #00ffff; font-family: Orbitron; margin: 0.2rem 0; font-size: 0.9rem;">
                11 coins analyzed • Only ≥85% confidence shown
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Display high-confidence signals
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.session_state.signals:
        st.markdown('<h2 class="section-header">🎯 HIGH CONFIDENCE SIGNALS FOUND</h2>', unsafe_allow_html=True)
        
        # Display signals in a responsive grid
        for signal in st.session_state.signals:
            display_clean_signal(signal)
    else:
        if st.session_state.last_scan:
            # No signals found
            st.markdown('<div class="no-signals">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #ff9900; font-family: Orbitron; text-align: center;">⚡ NO HIGH CONFIDENCE SIGNALS DETECTED</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #aaa; text-align: center;">Mathematical equations require ≥85% confidence threshold.</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #666; text-align: center; font-size: 0.9rem;">Try scanning again in a few minutes when market conditions improve.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Initial state
            st.info("✨ Click the button above to scan for high-confidence mathematical signals")
    
    # Coins being monitored
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 MONITORED COINS</h2>', unsafe_allow_html=True)
    
    # Display coins with status
    coins_list = [
        ("BTC", "Bitcoin", "🐲", "#FF9900"),
        ("ETH", "Ethereum", "🔥", "#3C3C3D"),
        ("SUI", "Sui", "💧", "#6FCF97"),
        ("LINK", "Chainlink", "🔗", "#2A5ADA"),
        ("SOL", "Solana", "☀️", "#00FFA3"),
        ("XRP", "Ripple", "✖️", "#23292F"),
        ("TAO", "Bittensor", "🧠", "#FF6B00"),
        ("ENA", "Ethena", "⚡", "#3A86FF"),
        ("ADA", "Cardano", "🔷", "#0033AD"),
        ("DOGE", "Dogecoin", "🐕", "#C2A633"),
        ("BRETT", "Brett", "🤖", "#FF6B6B")
    ]
    
    # Create columns for coin display
    cols = st.columns(4)
    for idx, (symbol, name, emoji, color) in enumerate(coins_list):
        with cols[idx % 4]:
            # Check if this coin has a signal
            has_signal = any(s['symbol'] == f"{symbol}USDT" for s in st.session_state.signals)
            
            status_color = "#00ff00" if has_signal else "#666666"
            status_text = "✅ ACTIVE" if has_signal else "📡 MONITORING"
            
            st.markdown(f'''
            <div style="background: rgba(20, 0, 40, 0.7); border: 2px solid {color}; 
                     border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 0.5rem;">
                <p style="font-family: Orbitron; color: {color}; margin: 0.2rem 0; font-size: 1.2rem;">{emoji} {name}</p>
                <p style="color: {color}; font-size: 0.9rem; margin: 0;">{symbol}/USDT</p>
                <div style="margin-top: 0.5rem;">
                    <p style="color: {status_color}; font-size: 0.8rem; font-family: Orbitron; margin: 0;">{status_text}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #ff66ff; padding: 2rem 1rem;">
        <p style="font-family: Orbitron; font-size: 1rem; margin-bottom: 0.5rem;">
            🔥 GODZILLERS MATHEMATICAL SIGNALS 🔥
        </p>
        <p style="color: #aaa; font-size: 0.8rem; margin-bottom: 0.3rem;">
            High Confidence Only • 8 Mathematical Equations • Clean Interface
        </p>
        <p style="color: #666; font-size: 0.7rem;">
            BTC • ETH • SUI • LINK • SOL • XRP • TAO • ENA • ADA • DOGE • BRETT
        </p>
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