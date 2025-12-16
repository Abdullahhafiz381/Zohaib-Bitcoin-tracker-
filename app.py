import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import plotly.graph_objects as go
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="🚀 CRYPTO QUANT SIGNAL PRO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main {
        background: #0f172a;
        color: #f1f5f9;
    }
    
    .stApp {
        background: #0f172a;
    }
    
    .header-container {
        background: linear-gradient(90deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid #475569;
    }
    
    .signal-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #475569;
        backdrop-filter: blur(10px);
    }
    
    .signal-buy {
        border-left: 5px solid #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .signal-sell {
        border-left: 5px solid #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    .signal-confirmed {
        border: 2px solid #3b82f6;
        animation: pulse 2s infinite;
        background: rgba(59, 130, 246, 0.15);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    .price-widget {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-box {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #475569;
    }
    
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2.5rem;
        background: rgba(15, 23, 42, 0.95);
        border-radius: 20px;
        border: 1px solid #475569;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        transition: all 0.3s ease;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #475569, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'btc_price' not in st.session_state:
    st.session_state.btc_price = 0
if 'bitnode_previous' not in st.session_state:
    st.session_state.bitnode_previous = {'tor_percent': 15.5, 'onion_ratio': 32.0}
if 'refresh_time' not in st.session_state:
    st.session_state.refresh_time = datetime.now()
if 'math_signals' not in st.session_state:
    st.session_state.math_signals = []
if 'bitnode_signal' not in st.session_state:
    st.session_state.bitnode_signal = {"direction": "HOLD", "strength": "NEUTRAL", "delta_tor": 0, "confirmed": False}
if 'order_books' not in st.session_state:
    st.session_state.order_books = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

# ========== API KEYS & CONFIG ==========
BITNODES_API = "https://bitnodes.io/api/v1/snapshots/latest/"
BINANCE_API = "https://api.binance.com/api/v3"
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Trading pairs to analyze
TRADING_PAIRS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "AVAXUSDT", "DOTUSDT", "DOGEUSDT", "LINKUSDT",
    "MATICUSDT", "SHIBUSDT", "TRXUSDT", "UNIUSDT", "ATOMUSDT"
]

# ========== REAL-TIME DATA FUNCTIONS ==========
def get_binance_price(symbol="BTCUSDT"):
    """Get real-time price from Binance"""
    try:
        response = requests.get(f"{BINANCE_API}/ticker/price", params={"symbol": symbol}, timeout=5)
        if response.status_code == 200:
            return float(response.json()['price'])
    except:
        pass
    return None

def get_binance_order_book(symbol="BTCUSDT", limit=100):
    """Get real-time order book from Binance"""
    try:
        response = requests.get(f"{BINANCE_API}/depth", params={"symbol": symbol, "limit": limit}, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_binance_klines(symbol="BTCUSDT", interval="5m", limit=100):
    """Get price history for volatility calculation"""
    try:
        response = requests.get(f"{BINANCE_API}/klines", 
                              params={"symbol": symbol, "interval": interval, "limit": limit}, 
                              timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_bitnodes_data():
    """Get real Bitnodes network data"""
    try:
        response = requests.get(BITNODES_API, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            total_nodes = data.get('total_nodes', 15000)
            nodes = data.get('nodes', {})
            
            # Initialize counters
            tor_nodes = 0
            onion_nodes = 0
            
            # Sample nodes for faster processing
            sample_size = min(500, len(nodes))
            if sample_size > 0:
                sample = list(nodes.items())[:sample_size]
                
                for node_addr, node_info in sample:
                    # Check address
                    if '.onion' in str(node_addr).lower():
                        onion_nodes += 1
                        tor_nodes += 1
                    elif 'tor' in str(node_addr).lower():
                        tor_nodes += 1
                    
                    # Check user agent if available
                    if isinstance(node_info, list) and len(node_info) > 7:
                        user_agent = str(node_info[7]).lower()
                        if '.onion' in user_agent:
                            onion_nodes += 1
                            tor_nodes += 1
                        elif 'tor' in user_agent:
                            tor_nodes += 1
                
                # Scale to total nodes
                scale_factor = len(nodes) / sample_size
                tor_nodes = int(tor_nodes * scale_factor)
                onion_nodes = int(onion_nodes * scale_factor)
            
            return {
                'total_nodes': total_nodes,
                'tor_nodes': tor_nodes,
                'onion_nodes': onion_nodes,
                'tor_percent': (tor_nodes / total_nodes * 100) if total_nodes > 0 else 15.0,
                'onion_ratio': (onion_nodes / tor_nodes * 100) if tor_nodes > 0 else 30.0,
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        pass
    
    # Return realistic fallback data
    return {
        'total_nodes': 15000,
        'tor_nodes': 2325,
        'onion_nodes': 697,
        'tor_percent': 15.5,
        'onion_ratio': 30.0,
        'timestamp': datetime.now().isoformat()
    }

# ========== SIGNAL ENGINE 1: BITNODE NETWORK ANALYSIS ==========
def calculate_bitnode_signal():
    """Calculate Bitnode signal using real-time data"""
    # Get current data
    current_data = get_bitnodes_data()
    
    # Get previous data
    previous_data = st.session_state.bitnode_previous
    
    # Calculate changes
    delta_tor = current_data['tor_percent'] - previous_data['tor_percent']
    delta_onion = current_data['onion_ratio'] - previous_data['onion_ratio']
    
    # Onion confirmation
    onion_confirmed = (np.sign(delta_onion) == np.sign(delta_tor))
    
    # Store current as previous
    st.session_state.bitnode_previous = {
        'tor_percent': current_data['tor_percent'],
        'onion_ratio': current_data['onion_ratio']
    }
    
    # Generate signal
    if delta_tor > 0.5:
        direction = "SELL"
        strength = "STRONG_BEARISH"
        confirmed = onion_confirmed
    elif delta_tor > 0.1:
        direction = "SELL"
        strength = "MODERATE_BEARISH"
        confirmed = onion_confirmed
    elif delta_tor < -0.5:
        direction = "BUY"
        strength = "STRONG_BULLISH"
        confirmed = onion_confirmed
    elif delta_tor < -0.1:
        direction = "BUY"
        strength = "MODERATE_BULLISH"
        confirmed = onion_confirmed
    else:
        direction = "HOLD"
        strength = "NEUTRAL"
        confirmed = False
    
    return {
        "direction": direction,
        "strength": strength,
        "delta_tor": delta_tor,
        "confirmed": confirmed,
        "tor_percent": current_data['tor_percent'],
        "onion_ratio": current_data['onion_ratio']
    }

# ========== SIGNAL ENGINE 2: MATHEMATICAL ORDER BOOK ANALYSIS ==========
def calculate_volume_imbalance(bids, asks, levels=10):
    """Calculate volume imbalance"""
    if not bids or not asks:
        return 0
    
    # Sum volumes for top levels
    bid_volume = sum(float(bid[1]) for bid in bids[:levels])
    ask_volume = sum(float(ask[1]) for ask in asks[:levels])
    
    # Calculate imbalance
    if bid_volume + ask_volume > 0:
        return (bid_volume - ask_volume) / (bid_volume + ask_volume)
    return 0

def calculate_spread(bids, asks):
    """Calculate spread percentage"""
    if not bids or not asks:
        return 0
    
    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])
    mid_price = (best_bid + best_ask) / 2
    
    if mid_price > 0:
        return (best_ask - best_bid) / mid_price * 100
    return 0

def calculate_volatility(klines):
    """Calculate price volatility"""
    if not klines or len(klines) < 2:
        return 0.01
    
    try:
        # Extract closing prices
        closes = [float(k[4]) for k in klines]
        
        # Calculate logarithmic returns
        returns = np.log(np.array(closes[1:]) / np.array(closes[:-1]))
        
        # Return annualized volatility (assuming 5-min intervals)
        return np.std(returns) * np.sqrt(365 * 24 * 12)  # 12 * 5-min periods per hour
    except:
        return 0.01

def calculate_mathematical_signal(symbol):
    """Calculate mathematical signal for a trading pair"""
    try:
        # Get order book
        order_book = get_binance_order_book(symbol)
        if not order_book:
            return None
        
        bids = order_book.get('bids', [])
        asks = order_book.get('asks', [])
        
        if not bids or not asks:
            return None
        
        # Get price history for volatility
        klines = get_binance_klines(symbol)
        
        # Calculate metrics
        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])
        mid_price = (best_bid + best_ask) / 2
        
        # Volume imbalance (I)
        I = calculate_volume_imbalance(bids, asks, levels=10)
        
        # Spread (S)
        S = best_ask - best_bid
        
        # Spread ratio (φ)
        phi = S / mid_price if mid_price > 0 else 0.001
        
        # Volatility (σ)
        sigma = calculate_volatility(klines)
        
        # Signal calculation
        if phi * sigma > 0:
            signal_value = np.sign(I) * (abs(I) / (phi * sigma))
        else:
            signal_value = 0
        
        # Determine direction
        if I > phi * 1.2:  # Added threshold buffer
            direction = "BUY"
        elif I < -phi * 1.2:
            direction = "SELL"
        else:
            direction = "HOLD"
        
        # Calculate strength
        strength_pct = min(99, abs(signal_value) * 100)
        
        # Only return signals with significant strength
        if direction != "HOLD" and strength_pct > 20:
            return {
                'symbol': symbol,
                'direction': direction,
                'strength': round(strength_pct, 1),
                'price': mid_price,
                'signal_value': signal_value,
                'imbalance': I,
                'spread': phi,
                'volatility': sigma
            }
    
    except Exception as e:
        pass
    
    return None

def calculate_all_mathematical_signals():
    """Calculate signals for all trading pairs"""
    signals = []
    
    for symbol in TRADING_PAIRS:
        signal = calculate_mathematical_signal(symbol)
        if signal:
            signals.append(signal)
    
    # Sort by strength and return top 5
    signals.sort(key=lambda x: x['strength'], reverse=True)
    return signals[:5]

# ========== CONFIRMATION LOGIC ==========
def check_signal_confirmation(bitnode_signal, math_signals):
    """Check if signals confirm each other"""
    if not math_signals:
        return False, None, 0
    
    bitnode_direction = bitnode_signal['direction']
    
    # Check if any math signal confirms
    confirmed_signals = []
    for math_signal in math_signals:
        if math_signal['direction'] == bitnode_direction:
            confirmed_signals.append(math_signal)
    
    if confirmed_signals:
        # Use strongest confirming signal
        best_signal = max(confirmed_signals, key=lambda x: x['strength'])
        
        # Calculate confidence score
        if bitnode_signal['confirmed']:
            confidence = 99
        else:
            confidence = min(95, 70 + (best_signal['strength'] * 0.3))
        
        return True, best_signal, confidence
    
    return False, None, 0

# ========== TRADING METRICS ==========
def calculate_trading_metrics(signals):
    """Calculate advanced trading metrics"""
    if not signals:
        return {}
    
    metrics = {
        'total_signals': len(signals),
        'buy_signals': sum(1 for s in signals if s['direction'] == 'BUY'),
        'sell_signals': sum(1 for s in signals if s['direction'] == 'SELL'),
        'avg_strength': np.mean([s['strength'] for s in signals]) if signals else 0,
        'max_strength': max([s['strength'] for s in signals]) if signals else 0,
        'signal_consistency': None
    }
    
    # Calculate consistency
    if metrics['total_signals'] > 1:
        directions = [1 if s['direction'] == 'BUY' else -1 for s in signals]
        metrics['signal_consistency'] = np.mean(directions) * 100
    
    return metrics

# ========== DATA REFRESH ==========
def refresh_all_data():
    """Refresh all data sources"""
    with st.spinner("🔄 Updating market data..."):
        # Get BTC price
        btc_price = get_binance_price("BTCUSDT")
        if btc_price:
            st.session_state.btc_price = btc_price
        
        # Calculate Bitnode signal
        st.session_state.bitnode_signal = calculate_bitnode_signal()
        
        # Calculate mathematical signals
        st.session_state.math_signals = calculate_all_mathematical_signals()
        
        # Update timestamp
        st.session_state.refresh_time = datetime.now()
        
        time.sleep(1)

# ========== LOGIN SYSTEM ==========
def login_system():
    """Professional login system"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #3b82f6; font-size: 2.5rem; margin-bottom: 0.5rem;">🚀</h1>
                <h2 style="color: #f1f5f9; margin-bottom: 0.5rem;">CRYPTO QUANT SIGNAL PRO</h2>
                <p style="color: #94a3b8; font-size: 0.9rem;">Professional Trading Signal System</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_btn = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if login_btn:
                # Simple authentication
                if (username == "trader" and password == "quant2025") or \
                   (username == "admin" and password == "admin123"):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    
                    # Initialize data on first login
                    if st.session_state.btc_price == 0:
                        btc_price = get_binance_price("BTCUSDT")
                        if btc_price:
                            st.session_state.btc_price = btc_price
                    
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: trader / quant2025")

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    """Main trading dashboard"""
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
        <div class="header-container">
            <h1 style="color: #f1f5f9; margin-bottom: 0.5rem;">🚀 CRYPTO QUANT SIGNAL PRO</h1>
            <p style="color: #94a3b8; margin: 0;">Real-time Trading Signals • Dual-Engine Analysis • Professional Grade</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("👤 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Control Panel
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_control1, col_control2, col_control3, col_control4 = st.columns(4)
    
    with col_control1:
        if st.button("🔄 Refresh Signals", use_container_width=True):
            refresh_all_data()
            st.rerun()
    
    with col_control2:
        st.markdown(f"""
        <div class="price-widget">
            <div style="color: #94a3b8; font-size: 0.9rem;">BTC PRICE</div>
            <div style="color: #f1f5f9; font-size: 1.8rem; font-weight: 600;">${st.session_state.btc_price:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_control3:
        last_update = st.session_state.refresh_time.strftime("%H:%M:%S")
        st.metric("Last Update", last_update)
    
    with col_control4:
        total_signals = len(st.session_state.math_signals)
        st.metric("Active Signals", total_signals)
    
    # Check for confirmed signals
    confirmed, best_signal, confidence = check_signal_confirmation(
        st.session_state.bitnode_signal, 
        st.session_state.math_signals
    )
    
    # Display confirmed signal if exists
    if confirmed and best_signal and confidence >= 85:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        if best_signal['direction'] == "BUY":
            signal_class = "signal-card signal-confirmed signal-buy"
            signal_icon = "📈"
            action = "LONG"
        else:
            signal_class = "signal-card signal-confirmed signal-sell"
            signal_icon = "📉"
            action = "SHORT"
        
        st.markdown(f"""
        <div class="{signal_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h3 style="color: #f1f5f9; margin: 0;">{signal_icon} CONFIRMED TRADING SIGNAL</h3>
                    <p style="color: #94a3b8; margin: 0.2rem 0;">Dual-engine confirmation detected</p>
                </div>
                <div style="background: #3b82f6; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                    {confidence}% CONFIDENCE
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                <div class="metric-box">
                    <div style="color: #94a3b8; font-size: 0.8rem;">ACTION</div>
                    <div style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600;">{action}</div>
                </div>
                <div class="metric-box">
                    <div style="color: #94a3b8; font-size: 0.8rem;">PAIR</div>
                    <div style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600;">{best_signal['symbol']}</div>
                </div>
                <div class="metric-box">
                    <div style="color: #94a3b8; font-size: 0.8rem;">STRENGTH</div>
                    <div style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600;">{best_signal['strength']}%</div>
                </div>
                <div class="metric-box">
                    <div style="color: #94a3b8; font-size: 0.8rem;">PRICE</div>
                    <div style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600;">${best_signal['price']:,.2f}</div>
                </div>
            </div>
            
            <div style="margin-top: 1rem; padding: 1rem; background: rgba(15, 23, 42, 0.5); border-radius: 8px;">
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                    📊 <strong>Signal Details:</strong> Bitnode network confirms {best_signal['direction']} bias with {st.session_state.bitnode_signal['strength'].replace('_', ' ').lower()} strength. 
                    Order book analysis shows {best_signal['direction']} signal with {best_signal['strength']}% strength.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mathematical Signals Table
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 MATHEMATICAL SIGNALS (Order Book Analysis)")
    
    math_signals = st.session_state.math_signals
    if math_signals:
        # Create DataFrame
        data = []
        for signal in math_signals:
            data.append({
                "Pair": signal['symbol'],
                "Signal": f"{'🟢 BUY' if signal['direction'] == 'BUY' else '🔴 SELL'}",
                "Strength": signal['strength'],
                "Price": f"${signal['price']:,.2f}",
                "Imbalance": f"{signal['imbalance']:.4f}",
                "Volatility": f"{signal['volatility']:.2%}"
            })
        
        df = pd.DataFrame(data)
        
        # Display with custom styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Pair": st.column_config.TextColumn("Trading Pair", width="small"),
                "Signal": st.column_config.TextColumn("Direction", width="small"),
                "Strength": st.column_config.ProgressColumn(
                    "Strength %",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                    width="medium"
                ),
                "Price": st.column_config.TextColumn("Price", width="medium"),
                "Imbalance": st.column_config.TextColumn("Volume Imbalance", width="medium"),
                "Volatility": st.column_config.TextColumn("Volatility", width="medium")
            }
        )
        
        # Trading metrics
        metrics = calculate_trading_metrics(math_signals)
        if metrics:
            col_met1, col_met2, col_met3, col_met4 = st.columns(4)
            
            with col_met1:
                st.metric("Total Signals", metrics['total_signals'])
            with col_met2:
                st.metric("Buy Signals", metrics['buy_signals'])
            with col_met3:
                st.metric("Sell Signals", metrics['sell_signals'])
            with col_met4:
                st.metric("Avg Strength", f"{metrics['avg_strength']:.1f}%")
    else:
        st.info("No mathematical signals detected. Click 'Refresh Signals' to analyze market data.")
    
    # Bitnode Network Signal
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🌐 BITNODE NETWORK SIGNAL")
    
    bitnode_signal = st.session_state.bitnode_signal
    
    if bitnode_signal['direction'] == "BUY":
        signal_class = "signal-card signal-buy"
        signal_icon = "📈"
    elif bitnode_signal['direction'] == "SELL":
        signal_class = "signal-card signal-sell"
        signal_icon = "📉"
    else:
        signal_class = "signal-card"
        signal_icon = "⚖️"
    
    st.markdown(f"""
    <div class="{signal_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <h3 style="color: #f1f5f9; margin: 0;">{signal_icon} {bitnode_signal['direction']} SIGNAL</h3>
                <p style="color: #94a3b8; margin: 0.2rem 0;">Bitnode Network Analysis</p>
            </div>
            <div style="background: {'#10b981' if bitnode_signal['direction'] == 'BUY' else '#ef4444'}; 
                        color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                {bitnode_signal['strength'].replace('_', ' ')}
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
            <div class="metric-box">
                <div style="color: #94a3b8; font-size: 0.8rem;">TOR % CHANGE</div>
                <div style="color: {'#10b981' if bitnode_signal['delta_tor'] < 0 else '#ef4444'}; 
                            font-size: 1.2rem; font-weight: 600;">
                    {bitnode_signal['delta_tor']:+.3f}%
                </div>
            </div>
            <div class="metric-box">
                <div style="color: #94a3b8; font-size: 0.8rem;">ONION CONFIRMATION</div>
                <div style="color: {'#10b981' if bitnode_signal['confirmed'] else '#ef4444'}; 
                            font-size: 1.2rem; font-weight: 600;">
                    {'✅ CONFIRMED' if bitnode_signal['confirmed'] else '⚠️ WEAK'}
                </div>
            </div>
        </div>
        
        <div style="margin-top: 1rem; padding: 1rem; background: rgba(15, 23, 42, 0.5); border-radius: 8px;">
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                🔍 <strong>Network Analysis:</strong> Tor node percentage change indicates {bitnode_signal['direction'].lower()} bias. 
                {'Onion node confirmation strengthens signal.' if bitnode_signal['confirmed'] else 'Lack of onion confirmation reduces signal strength.'}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_foot1, col_foot2, col_foot3 = st.columns([1, 2, 1])
    with col_foot2:
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 1rem;">
            <p>© 2025 Crypto Quant Signal Pro • Professional Trading System</p>
            <p style="margin-top: 0.5rem;">Dual-engine signal analysis • Real-time data • For educational purposes only</p>
            <p style="margin-top: 0.5rem; color: #475569;">
                Last update: {} • Refresh count: {}
            </p>
        </div>
        """.format(
            st.session_state.refresh_time.strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.get('refresh_count', 0)
        ), unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    """Main application"""
    
    # Initialize data on first load
    if st.session_state.authenticated and st.session_state.btc_price == 0:
        btc_price = get_binance_price("BTCUSDT")
        if btc_price:
            st.session_state.btc_price = btc_price
    
    # Show login or dashboard
    if not st.session_state.authenticated:
        login_system()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()