# app.py - GODZILLERS INDEPENDENT SIGNAL BOT
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
    page_title="🔥 GODZILLERS INDEPENDENT SIGNALS",
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
    
    .bitnode-signal {
        background: linear-gradient(135deg, rgba(0, 0, 255, 0.15) 0%, rgba(0, 0, 100, 0.3) 100%);
        border: 3px solid #00aaff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 35px rgba(0, 170, 255, 0.6);
    }
    
    .math-signal {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.15) 0%, rgba(100, 0, 100, 0.3) 100%);
        border: 3px solid #ff00ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 35px rgba(255, 0, 255, 0.6);
    }
    
    .confirmed-signal {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 100, 0, 0.4) 100%);
        border: 3px solid #00ff00;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 35px rgba(0, 255, 0, 0.6);
        animation: pulse-confirmed 2s infinite;
    }
    
    @keyframes pulse-confirmed {
        0% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.9); }
        100% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
    }
    
    .bitnode-badge {
        display: inline-block;
        background: linear-gradient(90deg, #00aaff, #0088cc);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 0 10px rgba(0, 170, 255, 0.5);
    }
    
    .math-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff00ff, #cc00cc);
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

# ==================== BITNODE BOT ANALYSIS ====================
class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
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

# ==================== INDEPENDENT SIGNAL SYSTEMS ====================
class IndependentSignalSystems:
    """Both systems show their own independent signals"""
    
    def __init__(self):
        self.bitnode_analyzer = CryptoAnalyzer()
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
    
    def get_bitnode_signal(self):
        """Get independent Bitnode signal"""
        tor_signal = self.bitnode_analyzer.calculate_tor_signal()
        
        # Add timestamp and additional info
        if self.bitnode_analyzer.current_data:
            tor_percentage = self.bitnode_analyzer.current_data['tor_percentage']
            total_nodes = self.bitnode_analyzer.current_data['total_nodes']
        else:
            tor_percentage = 0
            total_nodes = 0
        
        return {
            'signal': tor_signal['signal'],
            'bias': tor_signal['bias'],
            'strength': tor_signal['strength'],
            'tor_change': tor_signal['tor_change'],
            'tor_percentage': tor_percentage,
            'total_nodes': total_nodes,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_mathematical_signals(self):
        """Get independent mathematical signals for all coins"""
        all_math_signals = []
        
        for pair in self.trading_pairs:
            # Get mathematical signal
            math_signal = self.math_equations.generate_mathematical_signal(pair)
            
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
                    'math_details': {
                        'signal_raw': math_signal['signal_raw'],
                        'imbalance': math_signal['imbalance'],
                        'phi': math_signal['phi'],
                        'sigma': math_signal['sigma']
                    },
                    'timestamp': datetime.now().isoformat()
                }
                all_math_signals.append(signal_data)
            
            time.sleep(0.1)  # Rate limiting
        
        # Sort by signal strength
        all_math_signals.sort(key=lambda x: x['strength_pct'], reverse=True)
        
        return all_math_signals
    
    def get_agreement_signals(self, bitnode_signal, math_signals):
        """Find where both systems agree"""
        confirmed_signals = []
        
        # Convert bitnode bias to direction
        bitnode_direction = "HOLD"
        if "BULLISH" in bitnode_signal['bias']:
            bitnode_direction = "BUY"
        elif "BEARISH" in bitnode_signal['bias']:
            bitnode_direction = "SELL"
        
        for math_signal in math_signals:
            if math_signal['direction'] == bitnode_direction and bitnode_direction != "HOLD":
                # They agree!
                confirmed_signal = math_signal.copy()
                confirmed_signal['bitnode_signal'] = bitnode_signal['signal']
                confirmed_signal['bitnode_bias'] = bitnode_signal['bias']
                confirmed_signals.append(confirmed_signal)
        
        return confirmed_signals

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
            '>INDEPENDENT SIGNAL SYSTEMS</p>
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

# ==================== MAIN APP ====================
def get_coin_display_name(symbol):
    """Get display name for crypto symbols"""
    names = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum',
        'SUIUSDT': 'Sui',
        'LINKUSDT': 'Chainlink',
        'SOLUSDT': 'Solana',
        'XRPUSDT': 'Ripple',
        'TAOUSDT': 'Bittensor',
        'ENAUSDT': 'Ethena',
        'ADAUSDT': 'Cardano',
        'DOGEUSDT': 'Dogecoin',
        'BRETTUSDT': 'Brett'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols - GODZILLERS theme"""
    emojis = {
        'BTCUSDT': '🐲',
        'ETHUSDT': '🔥',
        'SUIUSDT': '💧',
        'LINKUSDT': '🔗',
        'SOLUSDT': '☀️',
        'XRPUSDT': '✖️',
        'TAOUSDT': '🧠',
        'ENAUSDT': '⚡',
        'ADAUSDT': '🔷',
        'DOGEUSDT': '🐕',
        'BRETTUSDT': '🤖'
    }
    return emojis.get(symbol, '💀')

def display_bitnode_signal(bitnode_signal):
    """Display Bitnode signal"""
    bias_color = "#00aaff"  # Blue for Bitnode
    if "BEARISH" in bitnode_signal['bias']:
        bias_color = "#ff4444"
    elif "BULLISH" in bitnode_signal['bias']:
        bias_color = "#00ff00"
    
    st.markdown(f'''
    <div class="bitnode-signal">
        <div style="text-align: center;">
            <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.5rem;">🌐 BITNODE MARKET SIGNAL</h3>
            <p style="font-family: Orbitron; font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: {bias_color};">{bitnode_signal['signal']}</p>
            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.3rem; margin: 0.5rem 0;">STRENGTH: {bitnode_signal['strength']}</p>
            <p style="color: #ffffff; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">Tor Change: {bitnode_signal['tor_change']:.2f}%</p>
            <p style="color: #aaa; font-family: Orbitron; font-size: 0.9rem; margin: 0.5rem 0;">Tor Nodes: {bitnode_signal['tor_percentage']:.1f}% | Total Nodes: {bitnode_signal['total_nodes']:,}</p>
        </div>
        
        <div style="text-align: center; margin: 1rem 0;">
            <span class="bitnode-badge">BITNODE ANALYSIS</span>
            <span class="bitnode-badge">{bitnode_signal['bias']}</span>
            <span class="bitnode-badge">TOR SIGNAL</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def display_math_signal(signal):
    """Display mathematical signal"""
    display_name = get_coin_display_name(signal['symbol'])
    emoji = get_coin_emoji(signal['symbol'])
    
    direction_color = "#00ff00" if signal['direction'] == "BUY" else "#ff4444"
    
    st.markdown(f'''
    <div class="math-signal">
        <div style="text-align: center;">
            <h4 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.2rem;">{emoji} {display_name} ({signal['symbol']})</h4>
            <p style="font-family: Orbitron; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0; color: {direction_color};">{signal['direction']} {signal['direction']}</p>
            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.1rem; margin: 0.5rem 0;">STRENGTH: {signal['strength_pct']}%</p>
            <p style="color: #ff9900; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">LEVERAGE: {signal['leverage']}</p>
            <p style="color: #ffffff; font-family: Orbitron; font-size: 0.9rem; margin: 0.5rem 0;">PRICE: ${signal['price']:,.2f}</p>
        </div>
        
        <div style="text-align: center; margin: 0.5rem 0;">
            <span class="math-badge">MATHEMATICAL</span>
            <span class="math-badge">STRENGTH: {signal['strength_pct']}%</span>
            <span class="leverage-badge">{signal['leverage']}</span>
        </div>
        
        <div style="color: #aaa; font-size: 0.7rem; text-align: center; margin-top: 0.5rem;">
            Signal: {signal['math_details']['signal_raw']:.3f} | 
            I={signal['math_details']['imbalance']:.3f} | 
            φ={signal['math_details']['phi']:.6f}
        </div>
    </div>
    ''', unsafe_allow_html=True)

def display_confirmed_signal(signal):
    """Display confirmed signal (both systems agree)"""
    display_name = get_coin_display_name(signal['symbol'])
    emoji = get_coin_emoji(signal['symbol'])
    
    st.markdown(f'''
    <div class="confirmed-signal">
        <div style="text-align: center;">
            <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.5rem;">{emoji} {display_name} ({signal['symbol']})</h3>
            <p style="font-family: Orbitron; font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #00ff00;">{signal['direction']} {signal['direction']}</p>
            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.3rem; margin: 0.5rem 0;">STRENGTH: {signal['strength_pct']}%</p>
            <p style="color: #ff9900; font-family: Orbitron; font-size: 1.2rem; margin: 0.5rem 0;">LEVERAGE: {signal['leverage']}</p>
            <p style="color: #ffffff; font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">PRICE: ${signal['price']:,.2f}</p>
        </div>
        
        <div style="text-align: center; margin: 1rem 0;">
            <span class="confirmation-badge">✓ BOTH SYSTEMS AGREE</span>
            <span class="bitnode-badge">Bitnode: {signal['bitnode_signal']}</span>
            <span class="math-badge">Math: {signal['strength_pct']}%</span>
        </div>
        
        <div style="color: #aaa; font-size: 0.8rem; text-align: center; margin-top: 1rem;">
            Bitnode Bias: {signal['bitnode_bias']} | 
            Math Signal: {signal['math_details']['signal_raw']:.3f}
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main_app():
    """Main application after login"""
    # Initialize systems
    if 'signal_systems' not in st.session_state:
        st.session_state.signal_systems = IndependentSignalSystems()
    if 'bitnode_signal' not in st.session_state:
        st.session_state.bitnode_signal = None
    if 'math_signals' not in st.session_state:
        st.session_state.math_signals = []
    if 'confirmed_signals' not in st.session_state:
        st.session_state.confirmed_signals = []
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
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS INDEPENDENT SIGNALS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">BITNODE + MATHEMATICAL SYSTEMS - BOTH SHOW OWN SIGNALS</p>', unsafe_allow_html=True)
    
    # Scan button
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">📡 SCAN ALL SYSTEMS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🐉 SCAN ALL SYSTEMS", key="scan_all", use_container_width=True, type="primary"):
            with st.spinner("🔥 Scanning all systems..."):
                # Update Bitnodes data
                st.session_state.signal_systems.bitnode_analyzer.update_node_data()
                
                # Get Bitnode signal
                st.session_state.bitnode_signal = st.session_state.signal_systems.get_bitnode_signal()
                
                # Get Mathematical signals
                st.session_state.math_signals = st.session_state.signal_systems.get_mathematical_signals()
                
                # Get agreement signals
                st.session_state.confirmed_signals = st.session_state.signal_systems.get_agreement_signals(
                    st.session_state.bitnode_signal, st.session_state.math_signals
                )
                
                st.session_state.last_scan = datetime.now()
                st.success("✅ All systems scanned!")
    
    # Last scan time
    if st.session_state.last_scan:
        scan_time = st.session_state.last_scan.strftime("%H:%M:%S")
        st.markdown(f'<p style="color: #ff6666; text-align: center;">Last scan: {scan_time} | 11 coins analyzed</p>', unsafe_allow_html=True)
    
    # Display BITNODE SIGNAL (always show)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header" style="color: #00aaff;">🌐 BITNODE MARKET SIGNAL</h2>', unsafe_allow_html=True)
    
    if st.session_state.bitnode_signal:
        display_bitnode_signal(st.session_state.bitnode_signal)
    else:
        st.info("Click 'SCAN ALL SYSTEMS' to get Bitnode market signal")
    
    # Display MATHEMATICAL SIGNALS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header" style="color: #ff00ff;">🧮 MATHEMATICAL SIGNALS</h2>', unsafe_allow_html=True)
    
    if st.session_state.math_signals:
        # Display mathematical signals in columns
        cols = st.columns(2)
        for idx, signal in enumerate(st.session_state.math_signals):
            with cols[idx % 2]:
                display_math_signal(signal)
    else:
        st.info("Click 'SCAN ALL SYSTEMS' to get mathematical signals")
    
    # Display CONFIRMED SIGNALS (where both agree)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header" style="color: #00ff00;">✅ CONFIRMED SIGNALS (BOTH AGREE)</h2>', unsafe_allow_html=True)
    
    if st.session_state.confirmed_signals:
        for signal in st.session_state.confirmed_signals:
            display_confirmed_signal(signal)
    else:
        st.info("No confirmed signals found (systems don't agree yet)")
    
    # Coins being monitored
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 COINS BEING MONITORED</h2>', unsafe_allow_html=True)
    
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
    
    # Display coins in a grid
    cols = st.columns(4)
    for idx, (symbol, name, emoji, color) in enumerate(coins_list):
        with cols[idx % 4]:
            st.markdown(f'''
            <div style="background: rgba(30, 0, 0, 0.7); border: 2px solid {color}; 
                     border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 0.5rem;">
                <p style="font-family: Orbitron; color: {color}; margin: 0.2rem 0; font-size: 1.2rem;">{emoji} {name}</p>
                <p style="color: {color}; font-size: 0.9rem; margin: 0;">{symbol}/USDT</p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Systems info
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🤖 ACTIVE SYSTEMS</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(0, 0, 30, 0.8); border: 2px solid #00aaff; border-radius: 15px; padding: 1.5rem;">
            <h3 style="font-family: Orbitron; color: #00aaff; margin-bottom: 1rem;">🌐 BITNODE SYSTEM</h3>
            <p style="color: #aaa; font-size: 0.9rem;">
                • Analyzes Bitcoin network Tor nodes<br>
                • Tracks percentage of Tor nodes<br>
                • Signals based on Tor % changes<br>
                • Market-wide sentiment indicator<br>
                • Updates from bitnodes.io API
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(30, 0, 30, 0.8); border: 2px solid #ff00ff; border-radius: 15px; padding: 1.5rem;">
            <h3 style="font-family: Orbitron; color: #ff00ff; margin-bottom: 1rem;">🧮 MATHEMATICAL SYSTEM</h3>
            <p style="color: #aaa; font-size: 0.9rem;">
                • Uses 8 mathematical equations<br>
                • Analyzes order book data<br>
                • Per-coin signals (11 coins)<br>
                • Real-time price analysis<br>
                • Signal strength 70-100%<br>
                • Leverage: LOW or MAX only
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #ff6666; padding: 2rem 1rem;">
        <p style="font-family: Orbitron; font-size: 1rem;">🔥 GODZILLERS INDEPENDENT SIGNAL SYSTEMS 🔥</p>
        <p style="color: #aaa; font-size: 0.8rem;">Bitnode Market Analysis + Mathematical Equations | 11 Specific Coins</p>
        <p style="color: #666; font-size: 0.7rem;">Each system shows its own signals independently | Confirmed when both agree</p>
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