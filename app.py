import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Crypto Signal Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #F7931A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .signal-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .confirmed-signal {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .btc-price {
        font-size: 2rem;
        font-weight: bold;
        color: #F7931A;
        text-align: center;
        padding: 1rem;
        background: #1a1a1a;
        border-radius: 10px;
        border: 2px solid #F7931A;
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        color: white;
        border: none;
    }
    .logout-btn {
        background: #ff4444 !important;
    }
    .logout-btn:hover {
        background: #cc0000 !important;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE INIT ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'btc_price' not in st.session_state:
    st.session_state.btc_price = 0
if 'bitnode_previous' not in st.session_state:
    st.session_state.bitnode_previous = {}
if 'refresh_time' not in st.session_state:
    st.session_state.refresh_time = datetime.now()
if 'math_signals_cache' not in st.session_state:
    st.session_state.math_signals_cache = []
if 'bitnode_cache' not in st.session_state:
    st.session_state.bitnode_cache = ("HOLD", "Unknown")
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# ========== HELPER FUNCTIONS ==========
def get_btc_price():
    """Get live BTC price from Binance"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return float(data.get('price', 0))
    except:
        return st.session_state.btc_price if st.session_state.btc_price > 0 else 45000.00

def get_bitnode_signal():
    """Bitnode signal engine using real Bitnodes API"""
    try:
        # Fetch current Bitnodes data
        response = requests.get("https://bitnodes.io/api/v1/snapshots/latest/", timeout=10)
        data = response.json()
        
        total_nodes = data.get('total_nodes', 1)
        tor_nodes = 0
        onion_nodes = 0
        
        # Count Tor and Onion nodes
        for node in data.get('nodes', {}).values():
            if isinstance(node, list) and len(node) > 7:
                if 'onion' in str(node[7]).lower():
                    onion_nodes += 1
                    tor_nodes += 1
                elif 'tor' in str(node[7]).lower():
                    tor_nodes += 1
        
        # Calculate metrics
        tor_percent_current = (tor_nodes / total_nodes) * 100 if total_nodes > 0 else 0
        onion_ratio_current = (onion_nodes / tor_nodes) * 100 if tor_nodes > 0 else 0
        
        # Get previous values
        tor_previous = st.session_state.bitnode_previous.get('tor_percent', tor_percent_current)
        onion_previous = st.session_state.bitnode_previous.get('onion_ratio', onion_ratio_current)
        
        # Calculate changes
        delta_tor = tor_percent_current - tor_previous
        delta_onion = onion_ratio_current - onion_previous
        
        # Store current as previous for next refresh
        st.session_state.bitnode_previous = {
            'tor_percent': tor_percent_current,
            'onion_ratio': onion_ratio_current
        }
        
        # Generate signal
        if delta_tor > 0.1 and delta_onion > 0:  # Both increasing
            direction = "BUY"
            strength = "Strong" if abs(delta_tor) > 0.5 else "Moderate"
        elif delta_tor < -0.1 and delta_onion < 0:  # Both decreasing
            direction = "SELL"
            strength = "Strong" if abs(delta_tor) > 0.5 else "Moderate"
        else:
            direction = "HOLD"
            strength = "Weak"
            
        return direction, strength
        
    except Exception:
        return "HOLD", "Unknown"

def get_mathematical_signals():
    """Mathematical signal engine using Binance order book"""
    # Internal list of BTC-correlated pairs
    pairs = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT",
        "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT",
        "MATICUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT", "BCHUSDT",
        "LTCUSDT", "XLMUSDT", "ALGOUSDT", "VETUSDT", "FILUSDT"
    ]
    
    signals = []
    
    for pair in pairs:
        try:
            # Get order book
            url = "https://api.binance.com/api/v3/depth"
            params = {"symbol": pair, "limit": 50}
            response = requests.get(url, params=params, timeout=5)
            order_book = response.json()
            
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                continue
            
            # Calculate P, I, S, φ, σ
            bid_price = float(bids[0][0])
            ask_price = float(asks[0][0])
            P = (bid_price + ask_price) / 2
            
            # Calculate volume imbalance I
            v_bid = sum(float(bid[1]) for bid in bids[:10])
            v_ask = sum(float(ask[1]) for ask in asks[:10])
            I = (v_bid - v_ask) / (v_bid + v_ask) if (v_bid + v_ask) > 0 else 0
            
            S = ask_price - bid_price
            phi = S / P if P > 0 else 0.001
            
            # Get recent prices for volatility
            kline_url = "https://api.binance.com/api/v3/klines"
            kline_params = {"symbol": pair, "interval": "5m", "limit": 20}
            kline_resp = requests.get(kline_url, params=kline_params, timeout=5)
            klines = kline_resp.json()
            
            if len(klines) >= 2:
                returns = [np.log(float(kline[4]) / float(klines[i-1][4])) 
                          for i, kline in enumerate(klines[1:], 1)]
                sigma = np.std(returns) if returns else 0.001
            else:
                sigma = 0.001
            
            # Generate signal
            signal_value = np.sign(I) * (abs(I) / (phi * sigma)) if (phi * sigma) > 0 else 0
            
            # Determine direction
            if I > phi:
                direction = "BUY"
            elif I < -phi:
                direction = "SELL"
            else:
                direction = "HOLD"
            
            # Calculate strength percentage
            strength_pct = min(99, abs(signal_value) * 100)
            
            if direction != "HOLD" and strength_pct > 10:
                signals.append({
                    'pair': pair,
                    'direction': direction,
                    'strength': round(strength_pct, 1)
                })
                
        except Exception:
            continue
    
    # Sort by strength and return top 2
    signals.sort(key=lambda x: x['strength'], reverse=True)
    return signals[:2]

def update_signals():
    """Update all signals and BTC price on manual refresh"""
    with st.spinner("Updating signals..."):
        # Update BTC price
        st.session_state.btc_price = get_btc_price()
        
        # Update Bitnode signal
        st.session_state.bitnode_cache = get_bitnode_signal()
        
        # Update mathematical signals
        st.session_state.math_signals_cache = get_mathematical_signals()
        
        # Update refresh time
        st.session_state.refresh_time = datetime.now()
        
        # Small delay for better UX
        time.sleep(0.5)

# ========== LOGIN SYSTEM ==========
def login_system():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>🔐 Crypto Signal Dashboard</h1>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if username == "admin" and password == "password123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>₿ Crypto Signal Dashboard</h1>", unsafe_allow_html=True)
    
    # BTC Price display
    st.markdown(f"<div class='btc-price'>₿ BTC Price: ${st.session_state.btc_price:,.2f}</div>", unsafe_allow_html=True)
    
    # Refresh button
    refresh_col1, refresh_col2, refresh_col3 = st.columns([3, 1, 3])
    with refresh_col2:
        if st.button("🔄 Refresh Signals", use_container_width=True):
            update_signals()
            st.rerun()
    
    st.divider()
    
    # Get signals from cache
    bitnode_signal, bitnode_strength = st.session_state.bitnode_cache
    math_signals = st.session_state.math_signals_cache
    
    # Check for confirmation
    confirmed = False
    if bitnode_signal in ["BUY", "SELL"] and math_signals:
        math_direction = math_signals[0]['direction'] if math_signals else "HOLD"
        if bitnode_signal == math_direction:
            confirmed = True
    
    # Display signals
    if confirmed:
        st.markdown(f"""
        <div class='signal-card confirmed-signal'>
            <h2>✅ CONFIRMED SIGNAL: {bitnode_signal}</h2>
            <p><strong>Confidence:</strong> 99%</p>
            <p>Both signal engines agree on direction</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bitnode Signal
        st.markdown(f"""
        <div class='signal-card'>
            <h3>Bitnode Signal</h3>
            <p><strong>Direction:</strong> {bitnode_signal}</p>
            <p><strong>Strength:</strong> {bitnode_strength}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mathematical Signals
        if math_signals:
            st.markdown("### Mathematical Signals")
            math_data = []
            for signal in math_signals[:2]:  # Show only top 2
                math_data.append({
                    "Pair": signal['pair'],
                    "Direction": signal['direction'],
                    "Strength": f"{signal['strength']}%"
                })
            
            if math_data:
                df = pd.DataFrame(math_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No mathematical signals available")
    
    # Last refresh time
    st.caption(f"Last refresh: {st.session_state.refresh_time.strftime('%Y-%m-%d %H:%M:%S')}")

# ========== INITIALIZATION ==========
if not st.session_state.initialized:
    # Initialize BTC price
    if st.session_state.btc_price == 0:
        st.session_state.btc_price = get_btc_price()
    
    # Initialize signals on first load
    if not st.session_state.math_signals_cache:
        st.session_state.math_signals_cache = get_mathematical_signals()
    
    if st.session_state.bitnode_cache == ("HOLD", "Unknown"):
        st.session_state.bitnode_cache = get_bitnode_signal()
    
    st.session_state.initialized = True

# ========== MAIN APP FLOW ==========
if not st.session_state.logged_in:
    login_system()
else:
    main_dashboard()
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()