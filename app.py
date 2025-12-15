# app.py - GODZILLERS MATHEMATICAL SIGNALS - COMPACT & CLEAN
import streamlit as st
import requests
import json
import os
from datetime import datetime
import numpy as np
import time
import ccxt

# ==================== STREAMLIT SETUP ====================
st.set_page_config(
    page_title="🔥 GODZILLERS",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== COMPACT CSS ====================
st.markdown("""
<style>
    /* BASE STYLES */
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a000a 50%, #00001a 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* HEADER */
    .app-header {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
    }
    
    .app-subheader {
        color: #ff66ff;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    /* COMPACT SIGNAL CARDS */
    .signal-card {
        background: rgba(20, 0, 40, 0.7);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 2px solid;
        transition: all 0.3s ease;
    }
    
    .signal-buy {
        border-color: #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    
    .signal-sell {
        border-color: #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }
    
    /* COMPACT BADGES */
    .badge {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 10px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    
    .badge-confidence-95 {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000;
        box-shadow: 0 0 8px rgba(0, 255, 0, 0.6);
    }
    
    .badge-confidence-90 {
        background: linear-gradient(90deg, #99ff00, #66cc00);
        color: #000;
        box-shadow: 0 0 8px rgba(153, 255, 0, 0.6);
    }
    
    .badge-confidence-85 {
        background: linear-gradient(90deg, #ffff00, #cccc00);
        color: #000;
        box-shadow: 0 0 8px rgba(255, 255, 0, 0.6);
    }
    
    .badge-leverage-max {
        background: linear-gradient(90deg, #ff00ff, #cc00cc);
        color: #000;
        box-shadow: 0 0 8px rgba(255, 0, 255, 0.6);
    }
    
    .badge-leverage-low {
        background: linear-gradient(90deg, #ff9900, #cc6600);
        color: #000;
        box-shadow: 0 0 8px rgba(255, 153, 0, 0.6);
    }
    
    /* LOGIN STYLES */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    
    .login-card {
        background: rgba(10, 0, 20, 0.9);
        border: 2px solid rgba(255, 0, 255, 0.5);
        border-radius: 20px;
        padding: 3rem;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.4);
        text-align: center;
    }
    
    .login-header {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .logout-button {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border: none;
        border-radius: 8px;
        font-size: 0.7rem;
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    /* SECTION HEADERS */
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        color: #ff66ff;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
    }
    
    /* MONITORED COINS */
    .coin-card {
        background: rgba(30, 0, 60, 0.5);
        border: 1px solid rgba(255, 0, 255, 0.3);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .coin-card:hover {
        transform: translateY(-2px);
    }
    
    /* SCAN BUTTON */
    .stButton button {
        background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron' !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
    
    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* NO SIGNALS */
    .no-signals {
        background: rgba(20, 0, 40, 0.5);
        border: 2px dashed rgba(255, 0, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MATHEMATICAL EQUATIONS ====================
class MathematicalEquations:
    """8 mathematical equations for high-confidence signals"""
    
    def __init__(self):
        self.CONFIDENCE_THRESHOLD = 85  # Only ≥85% signals
        self.ORDERBOOK_DEPTH = 10
        self.VOLATILITY_WINDOW = 20
        self.price_history = {}
        
        # Initialize exchange
        try:
            self.exchange = ccxt.binance({'enableRateLimit': True})
            self.exchange.load_markets()
        except:
            self.exchange = None
    
    def fetch_orderbook_data(self, symbol):
        """Get order book data"""
        if not self.exchange:
            return None
        
        try:
            # Try with USDT pair
            if not symbol.endswith('/USDT'):
                symbol = symbol + '/USDT'
            
            orderbook = self.exchange.fetch_order_book(symbol, self.ORDERBOOK_DEPTH)
            ticker = self.exchange.fetch_ticker(symbol)
            
            # Extract data
            bid = ticker['bid'] or orderbook['bids'][0][0]
            ask = ticker['ask'] or orderbook['asks'][0][0]
            mid_price = (bid + ask) / 2
            
            # Order book volumes
            bids = orderbook['bids'][:self.ORDERBOOK_DEPTH]
            asks = orderbook['asks'][:self.ORDERBOOK_DEPTH]
            bid_volume = sum(b[1] for b in bids)
            ask_volume = sum(a[1] for a in asks)
            
            # Store price history
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
        except:
            return None
    
    def calculate_volatility(self, price_history):
        """Calculate volatility from price history"""
        if len(price_history) < 2:
            return 0.01
        
        returns = np.diff(np.log(price_history))
        return float(np.std(returns, ddof=1))
    
    def generate_signal(self, symbol):
        """Generate high-confidence signal"""
        data = self.fetch_orderbook_data(symbol)
        
        if not data:
            return None
        
        # Equation 1: Mid Price
        P_t = data['mid_price']
        
        # Equation 2: Order Book Volumes
        V_bid = data['bid_volume']
        V_ask = data['ask_volume']
        
        # Equation 3: Order Book Imbalance
        total_volume = V_bid + V_ask
        I_t = (V_bid - V_ask) / total_volume if total_volume > 0 else 0
        
        # Equation 4: Spread
        S_t = data['spread']
        
        # Equation 5: Relative Spread
        phi_t = S_t / P_t if P_t > 0 else 0.0001
        
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
        elif I_t < -phi_t:
            direction = "SELL"
        else:
            return None
        
        # Calculate confidence percentage
        abs_signal = abs(signal_strength)
        if abs_signal < 1.0:
            confidence = 70 + int((abs_signal - 0.5) * 30) if abs_signal > 0.5 else 0
        else:
            confidence = 85 + min(14, int((abs_signal - 1.0) * 10))
        
        # Only return high confidence signals
        if confidence < self.CONFIDENCE_THRESHOLD:
            return None
        
        # Determine leverage
        leverage = "MAX LEVERAGE" if confidence >= 90 else "LOW LEVERAGE"
        
        return {
            'direction': direction,
            'confidence': confidence,
            'leverage': leverage,
            'price': round(P_t, 2)
        }

# ==================== SIGNAL SYSTEM ====================
class SignalSystem:
    """System to scan and manage signals"""
    
    def __init__(self):
        self.math_engine = MathematicalEquations()
        self.coins = [
            "BTC", "ETH", "SUI", "LINK", "SOL",
            "XRP", "TAO", "ENA", "ADA", "DOGE", "BRETT"
        ]
    
    def scan_coins(self):
        """Scan all 11 coins for signals"""
        signals = []
        
        for coin in self.coins:
            signal = self.math_engine.generate_signal(coin)
            if signal:
                signal['coin'] = coin
                signals.append(signal)
            time.sleep(0.05)  # Rate limiting
        
        # Sort by confidence (highest first)
        signals.sort(key=lambda x: x['confidence'], reverse=True)
        return signals

# ==================== COIN DATA ====================
COIN_DATA = {
    'BTC': {'name': 'Bitcoin', 'emoji': '🐲', 'color': '#FF9900'},
    'ETH': {'name': 'Ethereum', 'emoji': '🔥', 'color': '#3C3C3D'},
    'SUI': {'name': 'Sui', 'emoji': '💧', 'color': '#6FCF97'},
    'LINK': {'name': 'Chainlink', 'emoji': '🔗', 'color': '#2A5ADA'},
    'SOL': {'name': 'Solana', 'emoji': '☀️', 'color': '#00FFA3'},
    'XRP': {'name': 'Ripple', 'emoji': '✖️', 'color': '#23292F'},
    'TAO': {'name': 'Bittensor', 'emoji': '🧠', 'color': '#FF6B00'},
    'ENA': {'name': 'Ethena', 'emoji': '⚡', 'color': '#3A86FF'},
    'ADA': {'name': 'Cardano', 'emoji': '🔷', 'color': '#0033AD'},
    'DOGE': {'name': 'Dogecoin', 'emoji': '🐕', 'color': '#C2A633'},
    'BRETT': {'name': 'Brett', 'emoji': '🤖', 'color': '#FF6B6B'}
}

def get_confidence_class(confidence):
    """Get CSS class for confidence badge"""
    if confidence >= 95:
        return "badge-confidence-95"
    elif confidence >= 90:
        return "badge-confidence-90"
    else:
        return "badge-confidence-85"

def get_leverage_class(leverage):
    """Get CSS class for leverage badge"""
    if "MAX" in leverage:
        return "badge-leverage-max"
    return "badge-leverage-low"

def display_signal_compact(signal):
    """Display compact signal card"""
    coin = signal['coin']
    coin_info = COIN_DATA[coin]
    
    card_class = "signal-buy" if signal['direction'] == "BUY" else "signal-sell"
    direction_color = "#00ff00" if signal['direction'] == "BUY" else "#ff0000"
    confidence_class = get_confidence_class(signal['confidence'])
    leverage_class = get_leverage_class(signal['leverage'])
    
    st.markdown(f'''
    <div class="signal-card {card_class}">
        <!-- Coin Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{coin_info['emoji']}</span>
                <div>
                    <div style="font-family: Orbitron; font-size: 1rem; color: {coin_info['color']};">
                        {coin}
                    </div>
                    <div style="font-size: 0.8rem; color: #aaa;">
                        {coin_info['name']}
                    </div>
                </div>
            </div>
            <div style="font-family: Orbitron; font-size: 1.2rem; color: {direction_color}; font-weight: 700;">
                {signal['direction']}
            </div>
        </div>
        
        <!-- Badges -->
        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem; justify-content: center;">
            <div class="badge {confidence_class}">
                {signal['confidence']}%
            </div>
            <div class="badge {leverage_class}">
                {signal['leverage']}
            </div>
        </div>
        
        <!-- Price -->
        <div style="text-align: center; font-family: Orbitron; font-size: 1.1rem; color: #ffd700;">
            ${signal['price']:,.2f}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ==================== AUTHENTICATION ====================
def check_login(username, password):
    """Simple login check"""
    users = {
        "godziller": "dragonfire2025",
        "admin": "cryptoking",
        "trader": "bullmarket"
    }
    return username in users and users[username] == password

def login_page():
    """Display login page"""
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <h1 class="login-header">🐲 GODZILLERS</h1>
            <p style="color: #ff66ff; font-family: Orbitron; margin-bottom: 2rem;">
                MATHEMATICAL SIGNALS
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login"):
            username = st.text_input("DRAGON NAME", placeholder="Enter username...")
            password = st.text_input("FIRE BREATH", type="password", placeholder="Enter password...")
            
            if st.form_submit_button("🔥 IGNITE", use_container_width=True):
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ==================== MAIN APP ====================
def main_app():
    """Main application interface"""
    # Initialize session state
    if 'signal_system' not in st.session_state:
        st.session_state.signal_system = SignalSystem()
    if 'signals' not in st.session_state:
        st.session_state.signals = []
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = None
    
    # Logout button
    st.markdown("""
    <button class="logout-button" onclick="window.location.href='?logout=true'">🚪 LOGOUT</button>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown(f"""
    <div style="text-align: right; padding: 0.5rem 1rem;">
        <span style="color: #ff66ff; font-family: Orbitron;">Welcome, {st.session_state.username}!</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="app-header">🔥 GODZILLERS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subheader">HIGH-CONFIDENCE MATHEMATICAL SIGNALS</p>', unsafe_allow_html=True)
    
    # Scan Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ SCAN 11 COINS", use_container_width=True):
            with st.spinner("Analyzing..."):
                st.session_state.signals = st.session_state.signal_system.scan_coins()
                st.session_state.last_scan = datetime.now()
                
                if st.session_state.signals:
                    st.success(f"Found {len(st.session_state.signals)} signals!")
                else:
                    st.info("No high-confidence signals found")
    
    # Last scan info
    if st.session_state.last_scan:
        scan_time = st.session_state.last_scan.strftime("%H:%M:%S")
        st.markdown(f"""
        <div style="text-align: center; color: #ff66ff; font-family: Orbitron; font-size: 0.9rem; margin: 1rem 0;">
            Last scan: {scan_time} | 11 coins monitored
        </div>
        """, unsafe_allow_html=True)
    
    # Signals Display
    if st.session_state.signals:
        st.markdown('<h2 class="section-header">🎯 ACTIVE SIGNALS</h2>', unsafe_allow_html=True)
        
        # Display in columns
        cols = st.columns(2)
        for idx, signal in enumerate(st.session_state.signals):
            with cols[idx % 2]:
                display_signal_compact(signal)
    else:
        if st.session_state.last_scan:
            st.markdown("""
            <div class="no-signals">
                <p style="color: #ff9900; font-family: Orbitron;">No high-confidence signals</p>
                <p style="color: #aaa; font-size: 0.9rem;">Confidence must be ≥85%</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Click SCAN to find high-confidence signals")
    
    # Monitored Coins
    st.markdown('<h2 class="section-header">📊 MONITORED COINS</h2>', unsafe_allow_html=True)
    
    # Display coins in grid
    cols = st.columns(4)
    for idx, coin in enumerate(st.session_state.signal_system.coins):
        with cols[idx % 4]:
            coin_info = COIN_DATA[coin]
            has_signal = any(s['coin'] == coin for s in st.session_state.signals)
            
            st.markdown(f"""
            <div class="coin-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{coin_info['emoji']}</div>
                <div style="font-family: Orbitron; color: {coin_info['color']}; font-size: 0.9rem;">
                    {coin}
                </div>
                <div style="font-size: 0.7rem; color: #aaa; margin-top: 0.2rem;">
                    {coin_info['name']}
                </div>
                <div style="font-size: 0.6rem; color: {'#00ff00' if has_signal else '#666'}; margin-top: 0.3rem;">
                    {'✅ SIGNAL' if has_signal else '📡 MONITORING'}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #666; font-size: 0.8rem;">
        <p>🔥 GODZILLERS MATHEMATICAL SIGNALS 🔥</p>
        <p style="font-size: 0.7rem;">11 Coins • High Confidence Only • 8 Equations</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN FUNCTION ====================
def main():
    """Main application controller"""
    # Check for logout
    query_params = st.query_params
    if "logout" in query_params:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.query_params.clear()
    
    # Initialize session
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Show appropriate page
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()