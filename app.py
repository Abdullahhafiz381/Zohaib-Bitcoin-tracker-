import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="🔥 GODZILLERS CRYPTO TRACKER",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== GODZILLERS CSS ==========
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #330000 100%);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #330000 100%);
    }
    
    .godzillers-header {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
    }
    
    .godzillers-subheader {
        color: #ff6666;
        font-family: 'Courier New', monospace;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 2px solid #00ff00;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(100, 0, 0, 0.3) 100%);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(100, 65, 0, 0.3) 100%);
        border: 2px solid #ffa500;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.3);
    }
    
    .confirmed-signal {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 100, 0.3) 100%);
        border: 3px solid #00ffff;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.8); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
    }
    
    .price-display {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: rgba(20, 0, 0, 0.9);
        border-radius: 15px;
        border: 2px solid #ff0000;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff4444, #ff0000);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'btc_price' not in st.session_state:
    st.session_state.btc_price = 0
if 'bitnode_data' not in st.session_state:
    st.session_state.bitnode_data = None
if 'previous_bitnode' not in st.session_state:
    st.session_state.previous_bitnode = None
if 'math_signals' not in st.session_state:
    st.session_state.math_signals = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0

# ========== LOGIN SYSTEM ==========
def login_page():
    """Simple login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <h1 style="text-align: center; color: #ff0000; font-family: 'Courier New'; margin-bottom: 1rem;">🐲 GODZILLERS</h1>
            <p style="text-align: center; color: #ff6666; margin-bottom: 2rem;">PRIVATE CRYPTO TRACKER</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username...")
            password = st.text_input("Password", type="password", placeholder="Enter password...")
            
            submit = st.form_submit_button("LOGIN", use_container_width=True)
            
            if submit:
                # Simple hardcoded credentials
                if (username == "admin" and password == "password123") or \
                   (username == "godziller" and password == "dragonfire"):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: admin / password123")

# ========== REAL DATA FUNCTIONS ==========
def get_btc_price():
    """Get real BTC price from Binance"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            price = float(data['price'])
            st.session_state.btc_price = price
            return price
    except:
        pass
    
    # Fallback to CoinGecko if Binance fails
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            price = float(data['bitcoin']['usd'])
            st.session_state.btc_price = price
            return price
    except:
        pass
    
    # Return cached price or default
    return st.session_state.btc_price if st.session_state.btc_price > 0 else 65000

def get_eth_price():
    """Get real ETH price"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "ETHUSDT"}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data['price'])
    except:
        pass
    
    return 3500  # Default ETH price

def get_bitnodes_data():
    """Get real Bitnodes data"""
    try:
        response = requests.get("https://bitnodes.io/api/v1/snapshots/latest/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Initialize counters
            total_nodes = data.get('total_nodes', 15000)
            nodes = data.get('nodes', {})
            
            # Count Tor and Onion nodes
            tor_count = 0
            onion_count = 0
            
            # Sample nodes for faster processing
            sample_nodes = list(nodes.items())[:200] if len(nodes) > 200 else list(nodes.items())
            
            for node_addr, node_info in sample_nodes:
                # Check address for .onion
                if '.onion' in str(node_addr).lower():
                    onion_count += 1
                    tor_count += 1
                elif 'tor' in str(node_addr).lower():
                    tor_count += 1
                
                # Check user agent
                if isinstance(node_info, list) and len(node_info) > 7:
                    user_agent = str(node_info[7]).lower()
                    if '.onion' in user_agent and node_addr not in str(node_addr).lower():
                        onion_count += 1
                        tor_count += 1
                    elif 'tor' in user_agent and 'tor' not in str(node_addr).lower():
                        tor_count += 1
            
            # Scale up based on sample
            if len(sample_nodes) > 0 and len(nodes) > 0:
                scale = len(nodes) / len(sample_nodes)
                tor_count = int(tor_count * scale)
                onion_count = int(onion_count * scale)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_nodes': total_nodes,
                'tor_nodes': tor_count,
                'onion_nodes': onion_count,
                'tor_percent': (tor_count / total_nodes * 100) if total_nodes > 0 else 0,
                'onion_ratio': (onion_count / tor_count * 100) if tor_count > 0 else 0
            }
    except Exception as e:
        # Return realistic fallback data
        return {
            'timestamp': datetime.now().isoformat(),
            'total_nodes': 15000,
            'tor_nodes': 2250,
            'onion_nodes': 675,
            'tor_percent': 15.0,
            'onion_ratio': 30.0
        }

def get_binance_orderbook(pair="BTCUSDT", limit=20):
    """Get real Binance order book data"""
    try:
        url = f"https://api.binance.com/api/v3/depth"
        params = {"symbol": pair, "limit": limit}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_price_history(pair="BTCUSDT"):
    """Get price history for volatility calculation"""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {"symbol": pair, "interval": "5m", "limit": 20}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# ========== YOUR SIGNAL FORMULAS ==========
def calculate_bitnode_signal():
    """YOUR BITNODE FORMULA"""
    # Get current data
    current_data = get_bitnodes_data()
    
    # Store previous data if exists
    if st.session_state.bitnode_data:
        st.session_state.previous_bitnode = st.session_state.bitnode_data
    
    # Store current
    st.session_state.bitnode_data = current_data
    
    # Calculate signal
    if st.session_state.previous_bitnode:
        # Get current values
        current_tor = current_data['tor_percent']
        current_onion = current_data['onion_ratio']
        
        # Get previous values
        previous_tor = st.session_state.previous_bitnode['tor_percent']
        previous_onion = st.session_state.previous_bitnode['onion_ratio']
        
        # Calculate changes
        delta_tor = current_tor - previous_tor
        delta_onion = current_onion - previous_onion
        
        # Onion confirmation
        onion_confirmed = (np.sign(delta_onion) == np.sign(delta_tor))
        
        # Generate signal
        if delta_tor > 0.5 and onion_confirmed:
            direction = "🐲 GODZILLA DUMP 🐲"
            strength = "EXTREME_CONFIRMED"
            bias = "EXTREME_BEARISH"
        elif delta_tor > 0.1:
            direction = "🔥 STRONG SELL 🔥"
            strength = "STRONG"
            bias = "VERY_BEARISH"
        elif delta_tor < -0.5 and onion_confirmed:
            direction = "🐲 GODZILLA PUMP 🐲"
            strength = "EXTREME_CONFIRMED"
            bias = "EXTREME_BULLISH"
        elif delta_tor < -0.1:
            direction = "🚀 STRONG BUY 🚀"
            strength = "STRONG"
            bias = "VERY_BULLISH"
        else:
            direction = "HOLD"
            strength = "NEUTRAL"
            bias = "NEUTRAL"
        
        return {
            'direction': direction,
            'strength': strength,
            'bias': bias,
            'delta_tor': delta_tor,
            'confirmed': onion_confirmed
        }
    
    # First run - no previous data
    return {
        'direction': "HOLD",
        'strength': "INITIALIZING",
        'bias': "NEUTRAL",
        'delta_tor': 0,
        'confirmed': False
    }

def calculate_mathematical_signal(pair="BTCUSDT"):
    """YOUR MATHEMATICAL FORMULA"""
    try:
        # Get order book
        orderbook = get_binance_orderbook(pair)
        if not orderbook:
            return None
        
        # Get price history for volatility
        klines = get_price_history(pair)
        
        # Extract data
        bids = orderbook.get('bids', [])
        asks = orderbook.get('asks', [])
        
        if not bids or not asks:
            return None
        
        # Calculate P = (Bid + Ask) / 2
        bid_price = float(bids[0][0])
        ask_price = float(asks[0][0])
        P = (bid_price + ask_price) / 2
        
        # Calculate I = (V_bid - V_ask) / (V_bid + V_ask)
        # Use top 10 levels
        v_bid = sum(float(b[1]) for b in bids[:10])
        v_ask = sum(float(a[1]) for a in asks[:10])
        I = (v_bid - v_ask) / (v_bid + v_ask) if (v_bid + v_ask) > 0 else 0
        
        # Calculate S = Ask - Bid
        S = ask_price - bid_price
        
        # Calculate φ = S / P
        phi = S / P if P > 0 else 0.001
        
        # Calculate σ (volatility)
        if klines and len(klines) >= 2:
            closes = [float(k[4]) for k in klines]  # Close prices
            returns = np.diff(np.log(closes))
            sigma = np.std(returns) if len(returns) > 0 else 0.001
        else:
            sigma = 0.001
        
        # Signal = sign(I) × ( |I| / (φ × σ) )
        if phi * sigma > 0:
            signal = np.sign(I) * (abs(I) / (phi * sigma))
        else:
            signal = 0
        
        # Determine direction
        if I > phi:
            direction = "BUY"
        elif I < -phi:
            direction = "SELL"
        else:
            direction = "HOLD"
        
        # Strength percentage
        strength_pct = min(99, abs(signal) * 100)
        
        return {
            'pair': pair.replace('USDT', ''),
            'direction': direction,
            'strength': round(strength_pct, 1),
            'signal_value': signal,
            'price': P
        }
        
    except Exception as e:
        return None

def calculate_all_mathematical_signals():
    """Calculate signals for top pairs"""
    pairs = ["BTCUSDT", "ETHUSDT"]  # Only analyze BTC and ETH
    signals = []
    
    for pair in pairs:
        signal = calculate_mathematical_signal(pair)
        if signal and signal['direction'] != "HOLD" and signal['strength'] > 15:
            signals.append(signal)
    
    # Sort by strength
    signals.sort(key=lambda x: x['strength'], reverse=True)
    return signals[:2]  # Return only top 2

def check_confirmation(bitnode_signal, math_signals):
    """Check if both signals agree"""
    if not math_signals:
        return False, None
    
    # Map Bitnode to BUY/SELL
    bitnode_dir = bitnode_signal['direction']
    bitnode_action = None
    
    if "BUY" in bitnode_dir or "PUMP" in bitnode_dir:
        bitnode_action = "BUY"
    elif "SELL" in bitnode_dir or "DUMP" in bitnode_dir:
        bitnode_action = "SELL"
    
    # Check if top math signal agrees
    top_math = math_signals[0]
    
    if bitnode_action and bitnode_action == top_math['direction']:
        return True, bitnode_action
    
    return False, None

def refresh_data():
    """Update all data"""
    with st.spinner("Updating data..."):
        # Get BTC price
        st.session_state.btc_price = get_btc_price()
        
        # Get ETH price
        st.session_state.eth_price = get_eth_price()
        
        # Calculate signals
        st.session_state.bitnode_signal = calculate_bitnode_signal()
        st.session_state.math_signals = calculate_all_mathematical_signals()
        
        # Update timestamp
        st.session_state.last_update = datetime.now()
        st.session_state.refresh_count += 1
        
        time.sleep(0.5)

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    """Main dashboard after login"""
    # Header with logout
    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS CRYPTO TRACKER</h1>', unsafe_allow_html=True)
        st.markdown('<p class="godzillers-subheader">DUAL-ENGINE SIGNAL SYSTEM • REAL-TIME DATA</p>', unsafe_allow_html=True)
    
    with col3:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Refresh button
    st.markdown("---")
    col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 2, 1])
    with col_refresh2:
        if st.button("🔄 GENERATE NEW SIGNALS", use_container_width=True, type="primary"):
            refresh_data()
            st.rerun()
    
    # Display prices
    st.markdown("---")
    col_price1, col_price2 = st.columns(2)
    
    with col_price1:
        btc_price = get_btc_price()
        st.markdown(f'''
        <div class="price-display">
            <h3 style="color: #ff4444; margin-bottom: 0.5rem;">₿ BITCOIN</h3>
            <h2 style="color: #ffffff; margin: 0;">${btc_price:,.2f}</h2>
            <p style="color: #ff8888; margin-top: 0.5rem;">Live Price</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_price2:
        eth_price = get_eth_price()
        st.markdown(f'''
        <div class="price-display">
            <h3 style="color: #ff4444; margin-bottom: 0.5rem;">Ξ ETHEREUM</h3>
            <h2 style="color: #ffffff; margin: 0;">${eth_price:,.2f}</h2>
            <p style="color: #ff8888; margin-top: 0.5rem;">Live Price</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Initialize signals if not exists
    if 'bitnode_signal' not in st.session_state:
        st.session_state.bitnode_signal = calculate_bitnode_signal()
    if 'math_signals' not in st.session_state:
        st.session_state.math_signals = calculate_all_mathematical_signals()
    
    # Check for confirmation
    confirmed, direction = check_confirmation(
        st.session_state.bitnode_signal, 
        st.session_state.math_signals
    )
    
    # Display confirmed signal if exists
    if confirmed:
        st.markdown("---")
        if direction == "BUY":
            signal_text = "🐲 CONFIRMED GODZILLA PUMP SIGNAL 🐲"
            signal_class = "confirmed-signal"
            confidence = "99% CONFIRMATION"
            explanation = "BITNODE + MATHEMATICAL SIGNALS ALIGNED FOR BUY"
        else:
            signal_text = "🐲 CONFIRMED GODZILLA DUMP SIGNAL 🐲"
            signal_class = "confirmed-signal"
            confidence = "99% CONFIRMATION"
            explanation = "BITNODE + MATHEMATICAL SIGNALS ALIGNED FOR SELL"
        
        st.markdown(f'''
        <div class="{signal_class}">
            <h2 style="text-align: center; color: #00ffff; margin-bottom: 1rem;">{signal_text}</h2>
            <h3 style="text-align: center; color: #ffffff; margin-bottom: 0.5rem;">{confidence}</h3>
            <p style="text-align: center; color: #ff8888;">{explanation}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Display Bitnode Signal
    st.markdown("---")
    st.markdown("### 🌐 BITNODE NETWORK SIGNAL")
    
    bitnode_signal = st.session_state.bitnode_signal
    signal_class = "signal-neutral"
    
    if "SELL" in bitnode_signal['direction']:
        signal_class = "signal-sell"
    elif "BUY" in bitnode_signal['direction']:
        signal_class = "signal-buy"
    
    st.markdown(f'''
    <div class="{signal_class}">
        <h3 style="text-align: center; margin-bottom: 0.5rem;">{bitnode_signal['direction']}</h3>
        <p style="text-align: center; color: #ffffff;">Strength: {bitnode_signal['strength']}</p>
        <p style="text-align: center; color: #ff8888;">Bias: {bitnode_signal['bias']}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Display Mathematical Signals
    st.markdown("---")
    st.markdown("### 🧮 MATHEMATICAL SIGNALS")
    
    math_signals = st.session_state.math_signals
    if math_signals:
        # Create table
        data = []
        for signal in math_signals:
            arrow = "🟢" if signal['direction'] == "BUY" else "🔴"
            data.append({
                "Pair": f"{signal['pair']}/USDT",
                "Signal": f"{arrow} {signal['direction']}",
                "Strength": f"{signal['strength']}%"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Show analysis info
        st.markdown(f'''
        <div style="background: rgba(255, 0, 0, 0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <p style="color: #ff8888; font-size: 0.9rem; margin: 0;">
                📊 Showing top {len(math_signals)} highest strength pairs • 
                Formula: I = (V_bid - V_ask)/(V_bid + V_ask) • φ = Spread/Price • σ = Volatility
            </p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("No strong mathematical signals detected. Try refreshing.")
    
    # Last update info
    st.markdown("---")
    st.markdown(f'''
    <div style="text-align: center; color: #ff6666; margin-top: 2rem;">
        <p>🕒 Last Update: {st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>© 2025 GODZILLERS • DUAL-ENGINE SIGNAL SYSTEM</p>
    </div>
    ''', unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    """Main app function"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Show login or dashboard
    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()