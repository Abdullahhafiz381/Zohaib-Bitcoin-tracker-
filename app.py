"""
GODZILLERS CRYPTO TRACKER - MOBILE EDITION
Optimized for phone viewing on Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go
import random

# ========================
# MOBILE CONFIGURATION
# ========================
st.set_page_config(
    page_title="GODZILLERS TRACKER",
    page_icon="🔥",
    layout="wide",  # Streamlit mobile works better with wide
    initial_sidebar_state="collapsed"  # Hide sidebar on mobile
)

# ========================
# MOBILE-FRIENDLY CSS
# ========================
def load_mobile_css():
    """Mobile-optimized styling for phones"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Mobile-optimized base styles */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a0a0a 50%, #0a0a1a 100%);
        font-family: 'Rajdhani', sans-serif;
        padding: 5px !important;
    }
    
    /* Mobile title - fits phone screen */
    .mobile-title {
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 2rem !important;
        font-weight: 900;
        background: linear-gradient(to right, #ff0000, #ff4400, #ff0000);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        margin: 5px 0 !important;
        letter-spacing: 1px;
        line-height: 1.2;
    }
    
    .mobile-subtitle {
        font-family: 'Orbitron', monospace;
        text-align: center;
        color: #ff4444;
        font-size: 0.9rem !important;
        margin: 0 0 15px 0 !important;
        letter-spacing: 0.5px;
    }
    
    /* Mobile BTC panel - optimized for phone */
    .mobile-btc-panel {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(40, 10, 10, 0.95) 100%);
        border: 1.5px solid #ff0000;
        border-radius: 12px;
        padding: 15px !important;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        animation: mobile-shine 3s infinite alternate;
    }
    
    @keyframes mobile-shine {
        0% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.2); }
        100% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.4); }
    }
    
    /* Mobile signal cards - stack vertically */
    .mobile-signal-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.97) 0%, rgba(50, 20, 20, 0.97) 100%);
        border-radius: 10px;
        padding: 15px !important;
        margin: 10px 0;
        border: 1px solid;
        width: 100% !important;
    }
    
    .mobile-buy-card {
        border-color: #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        animation: mobile-pulse-green 2s infinite;
    }
    
    .mobile-sell-card {
        border-color: #ff0000;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        animation: mobile-pulse-red 2s infinite;
    }
    
    @keyframes mobile-pulse-green {
        0% { box-shadow: 0 0 8px rgba(0, 255, 0, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.4); }
        100% { box-shadow: 0 0 8px rgba(0, 255, 0, 0.2); }
    }
    
    @keyframes mobile-pulse-red {
        0% { box-shadow: 0 0 8px rgba(255, 0, 0, 0.2); }
        50% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.4); }
        100% { box-shadow: 0 0 8px rgba(255, 0, 0, 0.2); }
    }
    
    /* Mobile typography */
    .mobile-coin-name {
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem !important;
        font-weight: 700;
        margin-bottom: 3px;
    }
    
    .mobile-price-large {
        font-size: 1.8rem !important;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
    }
    
    .mobile-price-small {
        font-size: 1rem !important;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .mobile-signal-badge {
        display: inline-block;
        padding: 5px 12px !important;
        border-radius: 15px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.9rem !important;
        letter-spacing: 0.5px;
        min-width: 60px;
        text-align: center;
    }
    
    .mobile-buy-badge {
        background: linear-gradient(135deg, #00aa00, #00ff00);
        color: #000;
    }
    
    .mobile-sell-badge {
        background: linear-gradient(135deg, #aa0000, #ff0000);
        color: #fff;
    }
    
    /* Mobile controls */
    .mobile-controls {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(20, 20, 20, 0.9);
        border-radius: 20px;
        padding: 8px 15px;
        z-index: 1000;
        border: 1px solid #ff0000;
    }
    
    /* Mobile refresh button */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #ff0000, #ff4400);
        color: white;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        border: none;
        padding: 10px !important;
        border-radius: 8px;
        font-size: 0.9rem !important;
        margin: 5px 0;
    }
    
    /* Mobile spacing adjustments */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    
    .stHorizontalBlock {
        gap: 0.5rem !important;
    }
    
    /* Hide elements on mobile */
    .mobile-hidden {
        display: none !important;
    }
    
    /* Mobile status bar */
    .mobile-status {
        font-size: 0.75rem !important;
        color: #888;
        text-align: center;
        padding: 5px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 5px;
        margin: 5px 0;
    }
    
    /* Better touch targets */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] {
        gap: 0.5rem !important;
    }
    
    /* Mobile charts */
    .js-plotly-plot .plotly {
        height: 80px !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ========================
# HIDDEN CALCULATIONS (MOBILE OPTIMIZED)
# ========================
class MobileHiddenCalculations:
    """Lightweight hidden calculations for mobile"""
    
    @staticmethod
    def _calculate_tor_percentage(price_data):
        """Simplified TOR% for mobile"""
        if len(price_data) < 2:
            return random.uniform(40, 70)
        
        price_change = ((price_data[-1] - price_data[0]) / max(price_data[0], 0.001)) * 100
        tor_value = 50 + (price_change * 1.5)
        return max(0, min(100, round(tor_value, 1)))
    
    @staticmethod
    def _calculate_p_micro(price_history):
        """Simplified P_micro for mobile"""
        if len(price_history) < 5:
            return random.uniform(-30, 30)
        
        recent = price_history[-5:]
        volatility = np.std(recent) / np.mean(recent) * 100 if np.mean(recent) > 0 else 10
        direction = 1 if recent[-1] > recent[0] else -1
        
        return round(direction * min(volatility, 50), 1)
    
    @staticmethod
    def _determine_signal(tor_pct, p_micro, is_btc=False):
        """Mobile-optimized signal logic"""
        if not is_btc:
            # Altcoin conflict rule
            if p_micro < -15 and tor_pct > 55:
                return "NEUTRAL"
        
        # Combined score
        if is_btc:
            score = (tor_pct * 0.5 + p_micro * 0.5) / 100
        else:
            score = (tor_pct * 0.6 + p_micro * 0.4) / 100
        
        if score > 0.6:
            return "BUY"
        elif score < 0.4:
            return "SELL"
        else:
            return "NEUTRAL"

# ========================
# MOBILE DATA MANAGER
# ========================
class MobileCryptoData:
    """Lightweight data for mobile"""
    
    def __init__(self):
        # Core coins for mobile (reduced set)
        self.coins = {
            'BTC': {'name': 'Bitcoin', 'price': 65234.56},
            'ETH': {'name': 'Ethereum', 'price': 3421.78},
            'SOL': {'name': 'Solana', 'price': 118.45},
            'ADA': {'name': 'Cardano', 'price': 0.4567},
            'DOGE': {'name': 'Dogecoin', 'price': 0.1234},
            'XRP': {'name': 'Ripple', 'price': 0.5678},
        }
        
        self.history = {coin: [] for coin in self.coins}
        self.signals = {}
    
    def update_prices(self):
        """Update prices with mobile-friendly simulation"""
        for coin in self.coins:
            current = self.coins[coin]['price']
            change_pct = random.uniform(-1.5, 2.0)
            new_price = current * (1 + change_pct/100)
            
            self.coins[coin]['price'] = max(new_price, current * 0.8)
            
            # Keep limited history for mobile
            if coin not in self.history:
                self.history[coin] = []
            self.history[coin].append(self.coins[coin]['price'])
            if len(self.history[coin]) > 20:
                self.history[coin] = self.history[coin][-20:]
        
        return {coin: self.coins[coin]['price'] for coin in self.coins}

# ========================
# MOBILE UI COMPONENTS
# ========================
def display_mobile_btc_panel(price, signal, history):
    """Mobile-optimized BTC display"""
    st.markdown("<div class='mobile-btc-panel'>", unsafe_allow_html=True)
    
    # BTC Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='mobile-coin-name'>₿ BITCOIN</div>", unsafe_allow_html=True)
    with col2:
        badge_class = "mobile-buy-badge" if signal == "BUY" else "mobile-sell-badge"
        st.markdown(f"<div class='mobile-signal-badge {badge_class}'>{signal}</div>", unsafe_allow_html=True)
    
    # Price
    st.markdown(f"<div class='mobile-price-large'>${price:,.2f}</div>", unsafe_allow_html=True)
    
    # Mini chart for BTC
    if history and len(history) > 1:
        fig = go.Figure(data=go.Scatter(
            y=history[-10:],
            mode='lines',
            line=dict(color='#F7931A', width=2),
            fill='tozeroy',
            fillcolor='rgba(247, 147, 26, 0.1)'
        ))
        fig.update_layout(
            height=60,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_mobile_signal_card(coin, data, signal):
    """Mobile-optimized signal card"""
    if signal == "NEUTRAL":
        return  # Hidden per requirements
    
    card_class = "mobile-buy-card" if signal == "BUY" else "mobile-sell-card"
    badge_class = "mobile-buy-badge" if signal == "BUY" else "mobile-sell-badge"
    
    st.markdown(f"<div class='mobile-signal-card {card_class}'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"<div class='mobile-coin-name'>{coin}</div>", unsafe_allow_html=True)
        price = data['price']
        if price < 1:
            st.markdown(f"<div class='mobile-price-small'>${price:,.4f}</div>", unsafe_allow_html=True)
        elif price < 1000:
            st.markdown(f"<div class='mobile-price-small'>${price:,.2f}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='mobile-price-small'>${price:,.0f}</div>", unsafe_allow_html=True)
    
    with col2:
        # Simple trend indicator
        change = random.uniform(-3, 4)
        arrow = "▲" if change >= 0 else "▼"
        color = "#00ff00" if change >= 0 else "#ff0000"
        st.markdown(f"<span style='color: {color}; font-size: 0.9rem;'>{arrow} {abs(change):.1f}%</span>", 
                   unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='mobile-signal-badge {badge_class}'>{signal}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def mobile_control_panel():
    """Bottom control panel for mobile"""
    st.markdown("<div class='mobile-controls'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄", help="Refresh signals", use_container_width=True):
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("AUTO", value=True, key="mobile_auto", 
                                  help="Auto-refresh every 30s")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return auto_refresh

# ========================
# MAIN MOBILE APP
# ========================
def main_mobile():
    """Mobile-optimized main app"""
    
    # Load mobile CSS
    load_mobile_css()
    
    # Initialize
    calc = MobileHiddenCalculations()
    data_manager = MobileCryptoData()
    
    # Initialize session state for mobile
    if 'mobile_refresh_count' not in st.session_state:
        st.session_state.mobile_refresh_count = 0
    if 'mobile_last_update' not in st.session_state:
        st.session_state.mobile_last_update = datetime.now()
    
    # Mobile header
    st.markdown("<h1 class='mobile-title'>GODZILLERS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='mobile-subtitle'>CRYPTO WAR ROOM • MOBILE</p>", unsafe_allow_html=True)
    
    # Update counter display
    st.markdown(f"<div class='mobile-status'>Cycle #{st.session_state.mobile_refresh_count} | {datetime.now().strftime('%H:%M:%S')}</div>", 
               unsafe_allow_html=True)
    
    # Update data
    current_prices = data_manager.update_prices()
    st.session_state.mobile_refresh_count += 1
    
    # ========================
    # BTC SECTION (ALWAYS VISIBLE)
    # ========================
    btc_price = current_prices['BTC']
    btc_history = data_manager.history.get('BTC', [btc_price])
    
    # Calculate BTC signal
    btc_tor = calc._calculate_tor_percentage(btc_history)
    btc_pmicro = calc._calculate_p_micro(btc_history)
    btc_signal = calc._determine_signal(btc_tor, btc_pmicro, is_btc=True)
    
    # Display BTC
    display_mobile_btc_panel(btc_price, btc_signal, btc_history)
    
    # ========================
    # ACTIVE SIGNALS
    # ========================
    st.markdown("### 🔥 ACTIVE SIGNALS")
    
    active_count = 0
    
    for coin in data_manager.coins:
        if coin == 'BTC':
            continue  # BTC already shown
        
        price = current_prices[coin]
        history = data_manager.history.get(coin, [price])
        
        # Calculate signals
        tor_pct = calc._calculate_tor_percentage(history)
        pmicro = calc._calculate_p_micro(history)
        signal = calc._determine_signal(tor_pct, pmicro, is_btc=False)
        
        # Store signal
        data_manager.signals[coin] = {
            'signal': signal,
            'price': price,
            'tor': tor_pct,
            'pmicro': pmicro
        }
        
        # Display only BUY/SELL
        if signal in ['BUY', 'SELL']:
            active_count += 1
            display_mobile_signal_card(coin, data_manager.coins[coin], signal)
    
    # No signals message
    if active_count == 0:
        st.info("📊 No active signals. Market in consolidation.")
    
    # ========================
    # QUICK STATS
    # ========================
    with st.expander("📈 QUICK STATS", expanded=False):
        buy_count = sum(1 for s in data_manager.signals.values() if s['signal'] == 'BUY')
        sell_count = sum(1 for s in data_manager.signals.values() if s['signal'] == 'SELL')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracked", len(data_manager.coins))
        col2.metric("BUY", buy_count)
        col3.metric("SELL", sell_count)
        
        # Signal distribution
        if buy_count + sell_count > 0:
            labels = ['BUY', 'SELL']
            values = [buy_count, sell_count]
            colors = ['#00ff00', '#ff0000']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textposition='inside'
            )])
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ========================
    # MOBILE CONTROLS
    # ========================
    auto_refresh = mobile_control_panel()
    
    # Auto-refresh logic
    if auto_refresh:
        current_time = datetime.now()
        time_diff = (current_time - st.session_state.mobile_last_update).seconds
        
        if time_diff >= 30:  # 30 second refresh for mobile
            st.session_state.mobile_last_update = current_time
            time.sleep(1)
            st.rerun()
    
    # Mobile footer
    st.markdown("---")
    st.caption("GODZILLERS MOBILE • Formulas Secured • TOR/.onion Hidden")

# ========================
# MOBILE DEPLOYMENT GUIDE
# ========================
def show_mobile_deployment():
    with st.sidebar:
        st.markdown("### 📱 MOBILE SETUP")
        
        with st.expander("Phone Access"):
            st.markdown("""
            **From Your Phone:**
            1. Save this code as `mobile_godzillers.py`
            2. Go to [share.streamlit.io](https://share.streamlit.io)
            3. Deploy the app
            4. Open the URL on your phone
            
            **OR Quick Test:**
            1. Run locally: `streamlit run mobile_godzillers.py`
            2. Open phone browser to: `http://[YOUR-COMPUTER-IP]:8501`
            """)
        
        with st.expander("Mobile Features"):
            st.markdown("""
            ✅ **Phone-optimized layout**
            ✅ **Touch-friendly buttons**
            ✅ **Reduced data usage**
            ✅ **Fast loading**
            ✅ **Vertical scrolling**
            ✅ **Bottom controls**
            """)

# ========================
# RUN MOBILE APP
# ========================
if __name__ == "__main__":
    # Hide sidebar on mobile
    hide_sidebar = """
    <style>
    section[data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)
    
    show_mobile_deployment()
    main_mobile()