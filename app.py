# app.py - GODZILLERS HYBRID MATHEMATICAL CONFIRMATION BOT
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
import ccxt  # Added for mathematical equations

# GODZILLERS Streamlit setup
st.set_page_config(
    page_title="🔥 GODZILLERS MATHEMATICAL HYBRID",
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
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.15) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(0, 255, 0, 0.4);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(100, 0, 0, 0.4) 100%);
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(100, 65, 0, 0.3) 100%);
        border: 1px solid #ffa500;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.3);
    }
    
    .confirmed-signal {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 100, 0, 0.4) 100%);
        border: 3px solid #00ff00;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 35px rgba(0, 255, 0, 0.6);
        animation: pulse-confirmed 2s infinite;
    }
    
    @keyframes pulse-confirmed {
        0% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
    }
    
    .warning-signal {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(100, 0, 0, 0.4) 100%);
        border: 3px solid #ff0000;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 35px rgba(255, 0, 0, 0.6);
        animation: pulse-warning 2s infinite;
    }
    
    @keyframes pulse-warning {
        0% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.6); }
    }
    
    .math-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff00ff, #00ffff);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
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
    
    .leverage-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff9900, #ff5500);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 10px rgba(255, 153, 0, 0.5);
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== MATHEMATICAL EQUATIONS CLASS ====================
class MathematicalEquations:
    """Implementation of ALL 8 mathematical equations"""
    
    def __init__(self):
        # Mathematical parameters
        self.SIGNAL_THRESHOLD = 0.5
        self.ORDERBOOK_DEPTH = 10
        self.VOLATILITY_WINDOW = 20
        self.BASE_LEVERAGE = 5
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
            orderbook = self.exchange.fetch_order_book(symbol, self.ORDERBOOK_DEPTH)
            ticker = self.exchange.fetch_ticker(symbol)
            
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
    
    def generate_mathematical_signal(self, symbol):
        """Generate signal using ALL 8 mathematical equations"""
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
        
        # Threshold filtering (θ = 0.5)
        if abs(signal_strength) < self.SIGNAL_THRESHOLD:
            return None
        
        # Determine direction
        if I_t > phi_t:
            direction = "BUY"
            action = "LONG"
        elif I_t < -phi_t:
            direction = "SELL"
            action = "SHORT"
        else:
            return None
        
        # Equation 8: Max Leverage (for display only)
        if sigma_t > 0:
            max_leverage = 1 + (self.BASE_LEVERAGE / sigma_t)
            max_leverage = min(10, max_leverage)
        else:
            max_leverage = 3
        
        # Convert signal strength to percentage
        abs_signal = abs(signal_strength)
        if abs_signal < 1.0:
            strength_pct = 70 + int((abs_signal - 0.5) * 30) if abs_signal > 0.5 else 0
        else:
            strength_pct = 85 + min(14, int((abs_signal - 1.0) * 10))
        
        if strength_pct < 70:
            return None
        
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
            'price': round(P_t, 2),
            'signal_raw': round(signal_strength, 3),
            'imbalance': round(I_t, 4),
            'phi': round(phi_t, 6),
            'sigma': round(sigma_t, 4)
        }

# ==================== ORIGINAL BOT CLASSES (KEPT SAME) ====================
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
            '>MATHEMATICAL HYBRID CONFIRMATION</p>
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

# EMAScalpingAnalyzer (Original - Kept Same)
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
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                closes = [float(candle[4]) for candle in data]
                return closes
            else:
                return None
        except Exception as e:
            return None
    
    def generate_scalp_signal(self, symbol, current_price):
        """Generate 1-minute scalp signal based on EMA crossover"""
        try:
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
            
            # Determine trend
            if current_price > signal_ema * 1.002:
                trend = "STRONG_BULLISH"
            elif current_price > signal_ema:
                trend = "BULLISH"
            elif current_price < signal_ema * 0.998:
                trend = "STRONG_BEARISH"
            elif current_price < signal_ema:
                trend = "BEARISH"
            else:
                trend = "SIDEWAYS"
            
            # Generate signal
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

# CryptoAnalyzer (Original - Kept Same)
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
            pass
    
    def fetch_node_data(self):
        """Fetch current node data from Bitnodes API"""
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
                return None
        except Exception as e:
            return None
    
    def update_node_data(self):
        """Fetch new data and shift current to previous"""
        new_data = self.fetch_node_data()
        if not new_data:
            return False
        
        self.last_snapshot_check = datetime.now().isoformat()
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
                'tor_change': 0,
                'momentum': 0
            }
        
        current_tor_pct = self.current_data['tor_percentage']
        previous_tor_pct = self.previous_data['tor_percentage']
        
        tor_pct_change = current_tor_pct - previous_tor_pct
        
        # TOR SIGNAL LOGIC
        if tor_pct_change >= 1.0:
            signal = "🐲 GODZILLA DUMP 🐲"
            bias = "EXTREME_BEARISH"
            strength = "EXTREME"
        elif tor_pct_change >= 0.5:
            signal = "🔥 STRONG SELL 🔥"
            bias = "VERY_BEARISH"
            strength = "STRONG"
        elif tor_pct_change >= 0.1:
            signal = "SELL"
            bias = "BEARISH"
            strength = "MODERATE"
        elif tor_pct_change <= -1.0:
            signal = "🐲 GODZILLA PUMP 🐲"
            bias = "EXTREME_BULLISH"
            strength = "EXTREME"
        elif tor_pct_change <= -0.5:
            signal = "🚀 STRONG BUY 🚀"
            bias = "VERY_BULLISH"
            strength = "STRONG"
        elif tor_pct_change <= -0.1:
            signal = "BUY"
            bias = "BULLISH"
            strength = "MODERATE"
        else:
            signal = "HOLD"
            bias = "NEUTRAL"
            strength = "WEAK"
        
        return {
            'signal': signal,
            'bias': bias,
            'strength': strength,
            'tor_change': tor_pct_change,
            'momentum': tor_pct_change * 100
        }

# ==================== HYBRID CONFIRMATION SYSTEM ====================
class HybridConfirmationSystem:
    """Combine Original Bot + Mathematical Equations for confirmation"""
    
    def __init__(self):
        self.original_analyzer = CryptoAnalyzer()
        self.math_equations = MathematicalEquations()
        self.trading_pairs = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
            "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "LINK/USDT", "DOT/USDT",
            "MATIC/USDT", "LTC/USDT", "BCH/USDT", "ATOM/USDT", "OP/USDT",
            "ARB/USDT", "APE/USDT", "SUI/USDT", "NEAR/USDT", "FIL/USDT"
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
    
    def generate_hybrid_signal(self, symbol):
        """Generate hybrid signal using both systems"""
        # Get current price
        current_price = self.get_current_price(symbol)
        if not current_price:
            return None
        
        # Get original bot signal (EMA + Bitnodes)
        ema_signal = self.original_analyzer.scalp_analyzer.generate_scalp_signal(
            symbol.replace("/", ""), current_price
        )
        tor_signal = self.original_analyzer.calculate_tor_signal()
        
        # Get mathematical signal
        math_signal = self.math_equations.generate_mathematical_signal(symbol)
        
        if not math_signal:
            return None
        
        # Determine if signals agree
        signals_agree = False
        
        # Convert all signals to simple BUY/SELL/HOLD
        original_direction = "HOLD"
        if ema_signal['signal'] == 'SCALP_LONG' and 'BULLISH' in tor_signal['bias']:
            original_direction = "BUY"
        elif ema_signal['signal'] == 'SCALP_SHORT' and 'BEARISH' in tor_signal['bias']:
            original_direction = "SELL"
        
        math_direction = math_signal['direction']
        
        # Check agreement
        if original_direction == math_direction and original_direction != "HOLD":
            signals_agree = True
            confirmation = "✅ CONFIRMED"
            signal_class = "confirmed-signal"
        elif original_direction == "HOLD" and math_direction != "HOLD":
            confirmation = "⚠️ MATH ONLY"
            signal_class = "warning-signal"
            signals_agree = False
        elif math_direction == "HOLD" and original_direction != "HOLD":
            confirmation = "⚠️ ORIGINAL ONLY"
            signal_class = "warning-signal"
            signals_agree = False
        else:
            confirmation = "❌ CONFLICT"
            signal_class = "warning-signal"
            signals_agree = False
        
        # Get leverage indication from mathematical signal
        leverage_indication = math_signal['leverage']
        
        return {
            'symbol': symbol.replace("/", ""),
            'display_symbol': symbol,
            'original_direction': original_direction,
            'math_direction': math_direction,
            'confirmation': confirmation,
            'signals_agree': signals_agree,
            'signal_class': signal_class,
            'strength_pct': math_signal['strength_pct'],
            'leverage': leverage_indication,
            'max_leverage_value': math_signal['max_leverage_value'],
            'price': math_signal['price'],
            'current_price': current_price,
            'math_details': {
                'signal_raw': math_signal['signal_raw'],
                'imbalance': math_signal['imbalance'],
                'phi': math_signal['phi'],
                'sigma': math_signal['sigma']
            },
            'original_details': {
                'ema_signal': ema_signal['signal'],
                'ema_strength': ema_signal['strength'],
                'tor_signal': tor_signal['signal'],
                'tor_bias': tor_signal['bias']
            }
        }
    
    def scan_all_pairs(self):
        """Scan all 20 trading pairs"""
        all_signals = []
        
        for pair in self.trading_pairs:
            signal = self.generate_hybrid_signal(pair)
            if signal:
                all_signals.append(signal)
            time.sleep(0.1)  # Rate limiting
        
        # Sort by signal strength
        all_signals.sort(key=lambda x: x['strength_pct'], reverse=True)
        
        # Only take top 5 signals
        return all_signals[:5]

# ==================== MAIN APP ====================
def get_crypto_prices():
    """Get crypto prices from multiple sources with fallback"""
    coins = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum',
        'BNBUSDT': 'binancecoin',
        'SOLUSDT': 'solana',
        'XRPUSDT': 'ripple',
        'ADAUSDT': 'cardano',
        'DOGEUSDT': 'dogecoin',
        'AVAXUSDT': 'avalanche-2',
        'LINKUSDT': 'chainlink',
        'DOTUSDT': 'polkadot'
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
        'ETHUSDT': 'Ethereum',
        'BNBUSDT': 'Binance Coin',
        'SOLUSDT': 'Solana',
        'XRPUSDT': 'Ripple',
        'ADAUSDT': 'Cardano',
        'DOGEUSDT': 'Dogecoin',
        'AVAXUSDT': 'Avalanche',
        'LINKUSDT': 'Chainlink',
        'DOTUSDT': 'Polkadot'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols - GODZILLERS theme"""
    emojis = {
        'BTCUSDT': '🐲',
        'ETHUSDT': '🔥',
        'BNBUSDT': '💰',
        'SOLUSDT': '☀️',
        'XRPUSDT': '✖️',
        'ADAUSDT': '🔷',
        'DOGEUSDT': '🐕',
        'AVAXUSDT': '❄️',
        'LINKUSDT': '🔗',
        'DOTUSDT': '⚫'
    }
    return emojis.get(symbol, '💀')

def main_app():
    """Main application after login"""
    # Initialize hybrid system
    if 'hybrid_system' not in st.session_state:
        st.session_state.hybrid_system = HybridConfirmationSystem()
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
    st.markdown(f'<p style="text-align: right; color: #ff4444; font-family: Orbitron; margin: 0.5rem 1rem;">Welcome, {st.session_state.username}!</p>', unsafe_allow_html=True)
    
    # GODZILLERS Header
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS MATHEMATICAL HYBRID</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">ORIGINAL BOT + 8 MATHEMATICAL EQUATIONS CONFIRMATION</p>', unsafe_allow_html=True)
    
    # Update data button
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">🧮 HYBRID SIGNAL CONFIRMATION</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🐉 SCAN 20 PAIRS", key="scan_hybrid", use_container_width=True, type="primary"):
            with st.spinner("🔥 Activating hybrid analysis..."):
                # Update Bitnodes data
                st.session_state.hybrid_system.original_analyzer.update_node_data()
                # Scan all pairs
                st.session_state.signals = st.session_state.hybrid_system.scan_all_pairs()
                st.session_state.last_scan = datetime.now()
                st.success("✅ Hybrid scan completed!")
    
    # Last scan time
    if st.session_state.last_scan:
        scan_time = st.session_state.last_scan.strftime("%H:%M:%S")
        st.markdown(f'<p style="color: #ff6666; text-align: center;">Last scan: {scan_time} | 20 pairs analyzed</p>', unsafe_allow_html=True)
    
    # Display hybrid signals
    if st.session_state.signals:
        # Display confirmed signals first
        confirmed_signals = [s for s in st.session_state.signals if s['signals_agree']]
        other_signals = [s for s in st.session_state.signals if not s['signals_agree']]
        
        if confirmed_signals:
            st.markdown('<h3 style="font-family: Orbitron; color: #00ff00; margin: 1rem 0;">✅ CONFIRMED SIGNALS (BOTH SYSTEMS AGREE)</h3>', unsafe_allow_html=True)
            
            for signal in confirmed_signals:
                display_name = get_coin_display_name(signal['symbol'])
                emoji = get_coin_emoji(signal['symbol'])
                
                st.markdown(f'''
                <div class="{signal['signal_class']}">
                    <div style="text-align: center;">
                        <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.5rem;">{emoji} {display_name} ({signal['symbol']})</h3>
                        <p style="font-family: Orbitron; font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #00ff00;">{signal['math_direction']} {signal['math_direction']}</p>
                        <p style="color: #ffd700; font-family: Orbitron; font-size: 1.3rem; margin: 0.5rem 0;">STRENGTH: {signal['strength_pct']}%</p>
                        <p style="color: #ff9900; font-family: Orbitron; font-size: 1.2rem; margin: 0.5rem 0;">LEVERAGE: {signal['leverage']}</p>
                        <p style="color: #ffffff; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">PRICE: ${signal['price']:,.2f}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 1rem 0;">
                        <span class="confirmation-badge">✓ BOTH SYSTEMS CONFIRM</span>
                        <span class="math-badge">MATH: {signal['math_direction']}</span>
                        <span class="leverage-badge">{signal['leverage']}</span>
                    </div>
                    
                    <div style="color: #aaa; font-size: 0.8rem; text-align: center; margin-top: 1rem;">
                        I={signal['math_details']['imbalance']:.3f} | φ={signal['math_details']['phi']:.6f} | σ={signal['math_details']['sigma']:.4f}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        if other_signals:
            st.markdown('<h3 style="font-family: Orbitron; color: #ff9900; margin: 1rem 0;">⚠️ OTHER SIGNALS (NO AGREEMENT)</h3>', unsafe_allow_html=True)
            
            for signal in other_signals:
                display_name = get_coin_display_name(signal['symbol'])
                emoji = get_coin_emoji(signal['symbol'])
                
                st.markdown(f'''
                <div class="{signal['signal_class']}">
                    <div style="text-align: center;">
                        <h4 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.2rem;">{emoji} {display_name}</h4>
                        <p style="font-family: Orbitron; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">{signal['confirmation']}</p>
                        <p style="color: #ffd700; font-family: Orbitron; font-size: 1.1rem; margin: 0.5rem 0;">MATH: {signal['math_direction']} ({signal['strength_pct']}%)</p>
                        <p style="color: #ff6666; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">ORIGINAL: {signal['original_direction']}</p>
                        <p style="color: #ff9900; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">LEVERAGE: {signal['leverage']}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 0.5rem 0;">
                        <span class="warning-badge">{signal['confirmation']}</span>
                        <span class="math-badge">MATH: {signal['math_direction']}</span>
                        <span class="leverage-badge">{signal['leverage']}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("🔥 Click 'SCAN 20 PAIRS' to get hybrid confirmation signals")
    
    # Live prices section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE PRICES</h2>', unsafe_allow_html=True)
    
    prices = get_crypto_prices()
    if prices:
        # Create columns for price grid
        cols = st.columns(5)
        
        for idx, (symbol, price) in enumerate(prices.items()):
            if price and price > 0:
                with cols[idx % 5]:
                    display_name = get_coin_display_name(symbol)
                    emoji = get_coin_emoji(symbol)
                    
                    st.markdown(f'''
                    <div style="background: rgba(30, 0, 0, 0.7); border: 1px solid rgba(255, 0, 0, 0.3); border-radius: 10px; padding: 1rem; text-align: center;">
                        <p style="font-family: Orbitron; color: #ff4444; margin: 0.2rem 0; font-size: 1rem;">{emoji} {display_name}</p>
                        <p style="font-family: Orbitron; font-size: 1.2rem; font-weight: 700; color: #ffffff; margin: 0.2rem 0;">${price:,.2f}</p>
                        <p style="color: #ff8888; font-size: 0.8rem; margin: 0;">{symbol}</p>
                    </div>
                    ''', unsafe_allow_html=True)
    
    # Mathematical equations info
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🧮 MATHEMATICAL EQUATIONS ACTIVE</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(20, 0, 0, 0.8); border: 1px solid rgba(255, 0, 0, 0.5); border-radius: 15px; padding: 1.5rem;">
        <p style="color: #ff6666; font-family: Orbitron; font-size: 1.1rem;">✅ ALL 8 EQUATIONS IMPLEMENTED:</p>
        <p style="color: #aaa; font-size: 0.9rem; margin: 0.5rem 0;">
            1. P_t = (Bid_t + Ask_t)/2<br>
            2. V_t^{bid} = Σ BidVolume_i, V_t^{ask} = Σ AskVolume_i<br>
            3. I_t = (V_t^{bid} - V_t^{ask})/(V_t^{bid} + V_t^{ask})<br>
            4. S_t = Ask_t - Bid_t<br>
            5. φ_t = S_t/P_t<br>
            6. σ̂_t = StdDev(returns)<br>
            7. Signal_t = sign(I_t) × |I_t|/(φ_t × σ̂_t)<br>
            8. L_max = 1 + L₀/σ̂_t (display only)
        </p>
        <p style="color: #ff9900; font-size: 0.9rem; margin-top: 1rem;">
            ⚡ Signals shown only when both systems agree<br>
            ⚡ Leverage: LOW LEVERAGE or MAX LEVERAGE only<br>
            ⚡ No specific leverage numbers suggested
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #ff6666; padding: 2rem 1rem;">
        <p style="font-family: Orbitron; font-size: 1rem;">🔥 GODZILLERS MATHEMATICAL HYBRID CONFIRMATION 🔥</p>
        <p style="color: #aaa; font-size: 0.8rem;">Original Bot + 8 Mathematical Equations | 20 Trading Pairs</p>
        <p style="color: #666; font-size: 0.7rem;">Signals shown only when both systems agree | Leverage: LOW or MAX only</p>
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