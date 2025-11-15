import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

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
    
    def check_snapshot_alert(self):
        """Check for significant changes that should trigger alerts"""
        if not self.current_data or not self.previous_data:
            return None
        
        current = self.current_data
        previous = self.previous_data
        
        alerts = []
        
        # Check for major Tor percentage changes
        tor_percentage_change = current['tor_percentage'] - previous['tor_percentage']
        if abs(tor_percentage_change) > 1.0:
            alerts.append({
                'type': 'TOR_PERCENTAGE_SURGE' if tor_percentage_change > 0 else 'TOR_PERCENTAGE_DROP',
                'message': f"🚨 MAJOR TOR PERCENTAGE {'SURGE' if tor_percentage_change > 0 else 'DROP'}! {tor_percentage_change:+.2f}%",
                'severity': 'HIGH',
                'change': tor_percentage_change
            })
        
        # Check for network size changes
        total_change = current['total_nodes'] - previous['total_nodes']
        if abs(total_change) > 100:
            alerts.append({
                'type': 'NETWORK_GROWTH' if total_change > 0 else 'NETWORK_DECLINE',
                'message': f"🌐 NETWORK {'EXPANSION' if total_change > 0 else 'SHRINKAGE'}! {abs(total_change):+} total nodes",
                'severity': 'MEDIUM',
                'change': total_change
            })
        
        # Check for significant active ratio changes
        active_ratio_change = current['active_ratio'] - previous['active_ratio']
        if abs(active_ratio_change) > 0.1:
            alerts.append({
                'type': 'ACTIVITY_SURGE' if active_ratio_change > 0 else 'ACTIVITY_DROP',
                'message': f"⚡ NETWORK ACTIVITY {'SURGE' if active_ratio_change > 0 else 'DROP'}! {active_ratio_change:+.3f} ratio change",
                'severity': 'HIGH',
                'change': active_ratio_change
            })
        
        return alerts if alerts else None
    
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
            current_tor_pct = self.current_data['tor_percentage'] if self.current_data else 0
            previous_tor_pct = self.previous_data['tor_percentage'] if self.previous_data else 0
            return {
                'current_tor_pct': current_tor_pct,
                'previous_tor_pct': previous_tor_pct,
                'tor_pct_change': 0,
                'signal': "INSUFFICIENT_DATA",
                'bias': "NEED MORE DATA"
            }
        
        current_tor_pct = self.current_data['tor_percentage']
        previous_tor_pct = self.previous_data['tor_percentage']
        
        # Calculate percentage change in Tor nodes
        tor_pct_change = current_tor_pct - previous_tor_pct
        
        # NEW TOR PERCENTAGE SIGNAL LOGIC
        if tor_pct_change >= 1.0:  # Tor percentage increased by 1.0% or more
            signal = "🐲 GODZILLA DUMP 🐲"
            bias = "EXTREME BEARISH"
        elif tor_pct_change >= 0.5:  # Tor percentage increased by 0.5-0.99%
            signal = "🔥 STRONG SELL 🔥"
            bias = "VERY BEARISH"
        elif tor_pct_change >= 0.1:  # Tor percentage increased by 0.1-0.49%
            signal = "SELL"
            bias = "BEARISH"
        elif tor_pct_change <= -1.0:  # Tor percentage decreased by 1.0% or more
            signal = "🐲 GODZILLA PUMP 🐲"
            bias = "EXTREME BULLISH"
        elif tor_pct_change <= -0.5:  # Tor percentage decreased by 0.5-0.99%
            signal = "🚀 STRONG BUY 🚀"
            bias = "VERY BULLISH"
        elif tor_pct_change <= -0.1:  # Tor percentage decreased by 0.1-0.49%
            signal = "BUY"
            bias = "BULLISH"
        else:  # Change between -0.1% and +0.1%
            signal = "HOLD"
            bias = "NEUTRAL"
        
        return {
            'current_tor_pct': current_tor_pct,
            'previous_tor_pct': previous_tor_pct,
            'tor_pct_change': tor_pct_change,
            'signal': signal,
            'bias': bias
        }
    
    def calculate_network_signal(self):
        """Calculate signal based on total node changes"""
        if not self.current_data or not self.previous_data:
            current_total = self.current_data['total_nodes'] if self.current_data else 0
            previous_total = self.previous_data['total_nodes'] if self.previous_data else 0
            return {
                'current_total': current_total,
                'previous_total': previous_total,
                'total_change': 0,
                'network_signal': "INSUFFICIENT_DATA"
            }
        
        current_total = self.current_data['total_nodes']
        previous_total = self.previous_data['total_nodes']
        total_change = current_total - previous_total
        
        # Network health signal
        if total_change > 50:
            network_signal = "NETWORK GROWING"
        elif total_change > 0:
            network_signal = "NETWORK STABLE" 
        else:
            network_signal = "NETWORK SHRINKING"
        
        return {
            'current_total': current_total,
            'previous_total': previous_total,
            'total_change': total_change,
            'network_signal': network_signal
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
    st.markdown('<p class="godzillers-subheader">Godzillers Eye SIGNALS • TOR PERCENTAGE ANALYSIS • RED HOT PRICES</p>', unsafe_allow_html=True)
    
    # BITNODE SNAPSHOT ALERTS SECTION
    if analyzer.current_data and analyzer.previous_data:
        alerts = analyzer.check_snapshot_alert()
        if alerts:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-header">🚨 GODZILLERS ALERT SYSTEM</h2>', unsafe_allow_html=True)
            
            for alert in alerts:
                if alert['severity'] == 'HIGH':
                    alert_color = "#ff0000"
                    alert_emoji = "🚨"
                else:
                    alert_color = "#ff4444"
                    alert_emoji = "⚠️"
                
                st.markdown(f'''
                <div class="alert-banner" style="border-color: {alert_color};">
                    <div style="text-align: center;">
                        <h3 style="font-family: Orbitron; color: {alert_color}; margin: 0.5rem 0; font-size: 1.5rem;">
                            {alert_emoji} {alert['message']} {alert_emoji}
                        </h3>
                        <p style="color: #ffffff; font-family: Rajdhani; margin: 0.5rem 0;">
                            Godzillers Eye detected significant network movement!
                        </p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
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
    
    # AUTO-REFRESH NODE DATA SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">🔄 Godzillers EYE ANALYSIS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🐉 Godzillers signal", key="refresh_main", use_container_width=True, type="primary"):
            with st.spinner("🔥 Scanning network with dragon fire..."):
                if analyzer.update_node_data():
                    st.success("✅ Node data updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update node data")
    
    # Display current node data status
    if analyzer.current_data:
        current_time = datetime.fromisoformat(analyzer.current_data['timestamp'])
        st.markdown(f'<p style="text-align: center; color: #ff4444; font-family: Rajdhani;">📊 Current data from: {current_time.strftime("%Y-%m-%d %H:%M:%S")}</p>', unsafe_allow_html=True)
    
    # TOR PERCENTAGE SIGNAL ANALYSIS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 Godzillers Eye SIGNALS</h2>', unsafe_allow_html=True)
    
    # Main content in two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # TOR PERCENTAGE COMPARISON
        st.markdown('<div class="godzillers-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Orbitron; color: #ff4444; text-align: center;">🔄 TOR PERCENTAGE BATTLE</h3>', unsafe_allow_html=True)
        
        tor_signal = analyzer.calculate_tor_signal()
        network_signal = analyzer.calculate_network_signal()
        
        # Display percentage comparison
        if analyzer.previous_data:
            col1a, col2a = st.columns(2)
            
            with col1a:
                st.metric("🕒 PREVIOUS TOR %", f"{tor_signal['previous_tor_pct']:.2f}%")
                st.metric("🕒 PREVIOUS TOTAL NODES", f"{network_signal['previous_total']:,}")
            
            with col2a:
                st.metric("🔥 CURRENT TOR %", f"{tor_signal['current_tor_pct']:.2f}%")
                st.metric("🔥 CURRENT TOTAL NODES", f"{network_signal['current_total']:,}")
            
            # Display changes
            st.markdown('<div style="text-align: center; margin: 1rem 0;">', unsafe_allow_html=True)
            st.metric("📈 TOR % CHANGE", f"{tor_signal['tor_pct_change']:+.2f}%", delta="percentage points")
            st.metric("📈 TOTAL NODE CHANGE", f"{network_signal['total_change']:+,}", delta="nodes")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔥 Update node data to see percentage comparison")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # SIGNAL RESULTS
        st.markdown('<div class="godzillers-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Orbitron; color: #ff4444; text-align: center;">📊 WAR ROOM SIGNALS</h3>', unsafe_allow_html=True)
        
        if analyzer.current_data:
            # Current network stats
            col1b, col2b = st.columns(2)
            
            with col1b:
                st.metric("🔒 TOR NODES", f"{analyzer.current_data['tor_nodes']:,}")
                st.metric("🌐 TOTAL NODES", f"{analyzer.current_data['total_nodes']:,}")
            
            with col2b:
                st.metric("⚡ ACTIVE NODES", f"{analyzer.current_data['active_nodes']:,}")
                st.metric("📊 ACTIVE RATIO", f"{analyzer.current_data['active_ratio']:.3f}")
            
            # Display signals
            st.markdown('<div style="text-align: center; margin: 1rem 0;">', unsafe_allow_html=True)
            st.metric("🎯 Godzillers SIGNAL", tor_signal['signal'])
            st.metric("📡 BATTLE BIAS", tor_signal['bias'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔥 Godzillers signal to see war room signals")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # MAIN SIGNAL DISPLAY WITH GODZILLERS THEME
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Display main signal with GODZILLERS styling
        if "GODZILLA DUMP" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲💀🔥"
            explanation = "GODZILLA DUMP - Tor percentage exploding upward (Extreme Bearish)"
        elif "STRONG SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🐲🔥"
            explanation = "Strong Sell - Tor percentage raging upward (Very Bearish)"
        elif "SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "Sell - Tor percentage increasing (Bearish)"
        elif "GODZILLA PUMP" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀🌟"
            explanation = "GODZILLA PUMP - Tor percentage collapsing (Extreme Bullish)"
        elif "STRONG BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🐲🚀"
            explanation = "Strong Buy - Tor percentage retreating (Very Bullish)"
        elif "BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🟢"
            explanation = "Buy - Tor percentage decreasing (Bullish)"
        else:
            signal_class = "signal-neutral"
            emoji = "🐲⚡"
            explanation = "Battlefield calm - Tor percentage stable (Neutral)"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">{emoji} {tor_signal_data["signal"]} {emoji}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #ff8888; font-family: Rajdhani; margin: 0.5rem 0;">{explanation}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-family: Orbitron; color: #ffffff; margin: 0.5rem 0;">Tor % Change: {tor_signal_data["tor_pct_change"]:+.2f}%</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # MULTI-COIN SIGNALS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 Godzillers ARMY SIGNALS</h2>', unsafe_allow_html=True)
    
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Apply Tor percentage trend analysis to remaining coins
        coins_list = [
            'BTCUSDT', 'ETHUSDT'
        ]
        
        # Create columns for coin signals (2 columns for cleaner layout)
        signal_cols = st.columns(2)
        
        for idx, symbol in enumerate(coins_list):
            if prices.get(symbol):
                with signal_cols[idx % 2]:
                    emoji = get_coin_emoji(symbol)
                    name = get_coin_display_name(symbol)
                    price = prices[symbol]
                    
                    # Apply the same Tor percentage signal to all coins
                    if "SELL" in tor_signal_data['signal']:
                        signal_class = "signal-sell"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🔴"
                    elif "BUY" in tor_signal_data['signal']:
                        signal_class = "signal-buy"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🟢"
                    else:
                        signal_class = "signal-neutral"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🟡"
                    
                    st.markdown(f'''
                    <div class="{signal_class}" style="padding: 1rem; margin: 0.5rem 0;">
                        <div style="text-align: center;">
                            <h4 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.1rem;">{emoji} {name}</h4>
                            <p style="font-family: Orbitron; font-size: 1.2rem; font-weight: 700; margin: 0.5rem 0;">${price:,.2f}</p>
                            <p style="font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">{signal_emoji} {signal_text}</p>
                            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.8rem; margin: 0;">Δ Tor %: {tor_signal_data['tor_pct_change']:+.2f}%</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    else:
        st.info("🔥 Update node data to see dragon army signals")
    
    # GODZILLERS Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥</p>
    <p>© 2025 GODZILLERS CRYPTO TRACKER • TOR PERCENTAGE SIGNAL TECHNOLOGY</p>
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