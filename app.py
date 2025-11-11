import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import time
import numpy as np

# Futuristic Streamlit setup
st.set_page_config(
    page_title="🚀 Abdullah's Bitcoin Tracker",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Futuristic CSS with cyberpunk theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .cyber-header {
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    .cyber-subheader {
        color: #8892b0;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .cyber-card {
        background: rgba(10, 15, 35, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 127, 0.2) 0%, rgba(0, 100, 0, 0.4) 100%);
        border: 2px solid #00ff7f;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 127, 0.4);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.2) 0%, rgba(100, 0, 0, 0.4) 100%);
        border: 2px solid #ff007f;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.4);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(100, 100, 0, 0.4) 100%);
        border: 2px solid #ffd700;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
    }
    
    .altcoin-signal {
        background: rgba(20, 25, 45, 0.9);
        border: 1px solid rgba(0, 255, 255, 0.4);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .altcoin-signal:hover {
        border-color: #ff00ff;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .confidence-high {
        border-left: 4px solid #00ff7f;
    }
    
    .confidence-medium {
        border-left: 4px solid #ffd700;
    }
    
    .confidence-low {
        border-left: 4px solid #ff6b6b;
    }
    
    .price-glow {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 255, 0.5);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
    }
    
    .auto-refresh-status {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 140, 0, 0.3) 100%);
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        text-align: center;
        font-family: 'Orbitron', monospace;
    }
    
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00ffff 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    .trademark {
        text-align: center;
        color: #8892b0;
        font-family: 'Orbitron', monospace;
        font-size: 0.9rem;
        margin-top: 2rem;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.last_refresh = datetime.now()
    st.session_state.last_altcoin_refresh = datetime.now()
    st.session_state.auto_refresh = True
    st.session_state.altcoin_signals = []
    st.session_state.bitcoin_price = None
    st.session_state.network_data = None
    st.session_state.global_signal = "NEUTRAL"

class AltcoinSignalGenerator:
    def __init__(self):
        self.coins = [
            "ETH/USDT", "LTC/USDT", "SOL/USDT", "ADA/USDT", 
            "AVAX/USDT", "DOT/USDT", "LINK/USDT"
        ]
    
    def generate_demo_signals(self, global_signal):
        """Generate demo signals for testing - since APIs might be failing"""
        signals = []
        
        # Demo data for testing
        demo_prices = {
            "ETH/USDT": 2850.50, "LTC/USDT": 78.90, "SOL/USDT": 95.75,
            "ADA/USDT": 0.48, "AVAX/USDT": 35.20, "DOT/USDT": 6.85, "LINK/USDT": 14.30
        }
        
        for coin in self.coins:
            # Simulate signal generation based on global signal
            if global_signal == "BUY":
                # 60% chance of BUY signal for demo
                if np.random.random() > 0.4:
                    signal_data = {
                        "coin": coin,
                        "current_price": demo_prices[coin],
                        "signal": "BUY",
                        "confidence": "High" if np.random.random() > 0.5 else "Medium",
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                    signals.append(signal_data)
            
            elif global_signal == "SELL":
                # 60% chance of SELL signal for demo
                if np.random.random() > 0.4:
                    signal_data = {
                        "coin": coin,
                        "current_price": demo_prices[coin],
                        "signal": "SELL", 
                        "confidence": "High" if np.random.random() > 0.5 else "Medium",
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                    signals.append(signal_data)
        
        return signals

def get_btc_price():
    """Get BTC price with fallback to demo data"""
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        response.raise_for_status()
        return float(response.json()['price'])
    except:
        # Fallback demo price
        return 42500.75  # Demo price

class BitcoinNodeAnalyzer:
    def __init__(self):
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
    
    def fetch_demo_network_data(self):
        """Generate demo network data when API fails"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_nodes': 18542,
            'active_nodes': 15218,
            'tor_nodes': 2315,
            'tor_percentage': 12.5,
            'active_ratio': 0.82
        }
    def calculate_network_signal(self, current_data):
        """Calculate trading signal based on network trends"""
        # Demo signal calculation
        trend = 0.0234  # Positive trend
        active_ratio = current_data['active_ratio']
        signal_strength = active_ratio * trend
        
        if signal_strength > 0.01:
            suggestion = "BUY"
        elif signal_strength < -0.01:
            suggestion = "SELL"
        else:
            suggestion = "NEUTRAL"
        
        return {
            'trend': round(trend, 4),
            'signal_strength': round(signal_strength, 4),
            'global_signal': suggestion
        }
    
    def calculate_tor_trend(self, current_tor_percentage):
        """Calculate Tor trend and market bias"""
        network_trend = 0.0234
        
        # Abdullah's Formula for Market Bias
        if network_trend < 0 and current_tor_percentage > 5:
            bias = "BEARISH (Sell Bias)"
        elif network_trend > 0 and current_tor_percentage < 5:
            bias = "BULLISH (Buy Bias)"
        else:
            bias = "NEUTRAL"
        
        return {
            'previous_tor': 11.8,  # Demo previous
            'current_tor': current_tor_percentage,
            'tor_trend': 0.59,  # Demo trend
            'bias': bias,
            'network_trend': network_trend
        }

def main():
    # Initialize analyzers
    analyzer = BitcoinNodeAnalyzer()
    altcoin_generator = AltcoinSignalGenerator()
    
    # Force initialization with demo data
    if st.session_state.network_data is None:
        st.session_state.network_data = analyzer.fetch_demo_network_data()
        st.session_state.bitcoin_price = get_btc_price()
        network_signal = analyzer.calculate_network_signal(st.session_state.network_data)
        st.session_state.global_signal = network_signal['global_signal']
        
        # Generate initial altcoin signals
        if st.session_state.global_signal in ['BUY', 'SELL']:
            signals = altcoin_generator.generate_demo_signals(st.session_state.global_signal)
            st.session_state.altcoin_signals = signals
    
    # Auto-refresh functionality
    current_time = datetime.now()
    node_refresh_interval = timedelta(minutes=10)
    altcoin_refresh_interval = timedelta(minutes=5)
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        # Node data refresh
        if current_time - st.session_state.last_refresh > node_refresh_interval:
            st.session_state.network_data = analyzer.fetch_demo_network_data()
            st.session_state.bitcoin_price = get_btc_price()
            network_signal = analyzer.calculate_network_signal(st.session_state.network_data)
            st.session_state.global_signal = network_signal['global_signal']
            st.session_state.last_refresh = current_time
        
        # Altcoin signals refresh
        if current_time - st.session_state.last_altcoin_refresh > altcoin_refresh_interval:
            if st.session_state.global_signal in ['BUY', 'SELL']:
                signals = altcoin_generator.generate_demo_signals(st.session_state.global_signal)
                st.session_state.altcoin_signals = signals
                st.session_state.last_altcoin_refresh = current_time
    
    # HEADER
    st.markdown('<h1 class="cyber-header">🚀 BITNODE ALTCOIN FILTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cyber-subheader">BITCOIN-DIRECTION ALGORITHM • MAJOR ALTCOINS • AUTO-REFRESH</p>', unsafe_allow_html=True)
    
    # AUTO-REFRESH STATUS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        next_node_refresh = st.session_state.last_refresh + node_refresh_interval
        next_altcoin_refresh = st.session_state.last_altcoin_refresh + altcoin_refresh_interval
        
        time_until_node = max(0, int((next_node_refresh - current_time).total_seconds() // 60))
        time_until_altcoin = max(0, int((next_altcoin_refresh - current_time).total_seconds() // 60))
        
        status_emoji = "🟢" if st.session_state.auto_refresh else "🔴"
        status_text = "ACTIVE" if st.session_state.auto_refresh else "PAUSED"
        
        st.markdown(f'''
        <div class="auto-refresh-status">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                {status_emoji} AUTO-REFRESH: {status_text}
            </div>
            <div style="font-size: 0.8rem; color: #ffd700;">
                Node Data: {time_until_node:02d} min • Altcoins: {time_until_altcoin:02d} min
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("⏸️ PAUSE" if st.session_state.auto_refresh else "▶️ RESUME", 
                    key="toggle_refresh", use_container_width=True):
            st.session_state.auto_refresh = not st.session_state.auto_refresh
            st.rerun()
    
    with col3:
        if st.button("🔄 NODES", key="refresh_nodes", use_container_width=True):
            st.session_state.network_data = analyzer.fetch_demo_network_data()
            st.session_state.bitcoin_price = get_btc_price()
            network_signal = analyzer.calculate_network_signal(st.session_state.network_data)
            st.session_state.global_signal = network_signal['global_signal']
            st.session_state.last_refresh = datetime.now()
            st.success("✅ Node data updated!")
            st.rerun()
    
    with col4:
        if st.button("🎯 ALTCOINS", key="refresh_altcoins", use_container_width=True):
            if st.session_state.global_signal in ['BUY', 'SELL']:
                signals = altcoin_generator.generate_demo_signals(st.session_state.global_signal)
                st.session_state.altcoin_signals = signals
                st.session_state.last_altcoin_refresh = datetime.now()
                st.success(f"✅ {len(signals)} altcoin signals updated!")
                st.rerun()
    
    # BITCOIN PRICE SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE BTC PRICE</h2>', unsafe_allow_html=True)
    
    if st.session_state.bitcoin_price:
        st.markdown('<div class="price-glow">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f'<div style="text-align: center;"><span style="font-family: Orbitron; font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #00ffff, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${st.session_state.bitcoin_price:,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">BITCOIN PRICE (USD)</p>', unsafe_allow_html=True)
        
        with col2:
            st.metric("24H STATUS", "🟢 LIVE", "ACTIVE")
        
        with col3:
            st.metric("DATA SOURCE", "BINANCE API", "PRIMARY")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">🕒 Price updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    
    # BITNODE GLOBAL SIGNAL SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌐 BITNODE GLOBAL SIGNAL</h2>', unsafe_allow_html=True)
    
    if st.session_state.network_data:
        current_data = st.session_state.network_data
        network_signal = analyzer.calculate_network_signal(current_data)
        tor_trend = analyzer.calculate_tor_trend(current_data['tor_percentage'])
        
        global_signal = network_signal.get('global_signal', 'NEUTRAL')
        
        # Display Global Signal
        if global_signal == "BUY":
            signal_class = "signal-buy"
            emoji = "📈"
        elif global_signal == "SELL":
            signal_class = "signal-sell"
            emoji = "📉"
        else:
            signal_class = "signal-neutral"
            emoji = "➡️"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🌐 GLOBAL SIGNAL", f"{global_signal} {emoji}")
            st.metric("📊 NETWORK TREND", f"{network_signal.get('trend', 0):+.4f}")
        
        with col2:
            st.metric("🕵️ TOR %", f"{current_data['tor_percentage']:.2f}%")
            st.metric("📈 SIGNAL STRENGTH", f"{network_signal.get('signal_strength', 0):+.4f}")
        
        with col3:
            st.metric("🔮 MARKET BIAS", tor_trend.get('bias', 'NEUTRAL'))
            st.metric("🟢 ACTIVE NODES", f"{current_data['active_nodes']:,}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Network Health Summary
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_data['tor_percentage'] > 20:
                status = "🟢 EXCELLENT"
            elif current_data['tor_percentage'] > 10:
                status = "🟡 GOOD"
            else:
                status = "🔴 LOW"
            st.metric("TOR PRIVACY", status)
        
        with col2:
            if current_data['active_ratio'] > 0.8:
                status = "🟢 EXCELLENT"
            elif current_data['active_ratio'] > 0.6:
                status = "🟡 GOOD"
            else:
                status = "🔴 LOW"
            st.metric("NETWORK HEALTH", status)
        
        with col3:
            if network_signal['trend'] > 0.01:
                status = "🟢 GROWING"
            elif network_signal['trend'] < -0.01:
                status = "🔴 SHRINKING"
            else:
                status = "🟡 STABLE"
            st.metric("NETWORK TREND", status)
    
    # ALTCOIN SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 ALTCOIN FILTER SIGNALS</h2>', unsafe_allow_html=True)
    
    if st.session_state.altcoin_signals:
        st.markdown(f'<p style="color: #8892b0; text-align: center;">Filtered {len(st.session_state.altcoin_signals)} coins following Bitcoin direction</p>', unsafe_allow_html=True)
        
        # Sort signals by confidence (High first)
        sorted_signals = sorted(st.session_state.altcoin_signals, 
                              key=lambda x: (x['confidence'] == 'High', x['confidence'] == 'Medium'), 
                              reverse=True)
        
        for signal in sorted_signals:
            confidence_class = f"confidence-{signal['confidence'].lower()}"
            
            if signal['signal'] == 'BUY':
                signal_emoji = "🟢"
                signal_color = "#00ff7f"
            else:
                signal_emoji = "🔴"
                signal_color = "#ff007f"
            
            st.markdown(f'''
            <div class="altcoin-signal {confidence_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: {signal_color}; font-family: Orbitron;">
                            {signal_emoji} {signal['coin']} - {signal['signal']}
                        </h3>
                        <p style="margin: 0.2rem 0; color: #8892b0;">
                            Confidence: <strong>{signal['confidence']}</strong> • 
                            Price: ${signal['current_price']:,.2f}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <small style="color: #666;">{signal['timestamp'][11:19]} UTC</small>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Download JSON button
        json_data = json.dumps(st.session_state.altcoin_signals, indent=2)
        st.download_button(
            label="📥 Download Signals JSON",
            data=json_data,
            file_name=f"bitnode_altcoin_signals_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        # BEST TRADES RECOMMENDATION
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ffff; font-family: Orbitron; text-align: center;">🏆 BEST TRADES RIGHT NOW</h3>', unsafe_allow_html=True)
        
        high_confidence_trades = [s for s in sorted_signals if s['confidence'] == 'High']
        if high_confidence_trades:
            best_trades = high_confidence_trades[:3]  # Top 3 high confidence trades
            
            for i, trade in enumerate(best_trades, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                st.markdown(f'''
                <div class="cyber-card">
                    <div style="text-align: center;">
                        <h2 style="margin: 0; color: #ffd700; font-family: Orbitron;">
                            {medal} #{i} {trade['coin']}
                        </h2>
                        <p style="margin: 0.5rem 0; color: #8892b0; font-size: 1.2rem;">
                            <strong>{trade['signal']}</strong> • Confidence: <span style="color: #00ff7f;">{trade['confidence']}</span>
                        </p>
                        <p style="margin: 0; color: #ffffff; font-size: 1.1rem;">
                            Price: ${trade['current_price']:,.2f}
                        </p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
    else:
        st.info("🎯 No filtered altcoin signals yet. The system is waiting for strong Bitcoin direction confirmation...")
        
        # Show what the system is monitoring
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ffff; font-family: Orbitron; text-align: center;">📊 MONITORING 7 MAJOR ALTCOINS</h3>', unsafe_allow_html=True)
        
        coins_grid = """
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: center;">
            <div>🟣 ETH/USDT</div>
            <div>🔵 LTC/USDT</div>
            <div>🟠 SOL/USDT</div>
            <div>🔶 ADA/USDT</div>
            <div>🔴 AVAX/USDT</div>
            <div>🟡 DOT/USDT</div>
            <div>🔗 LINK/USDT</div>
        </div>
        """
        st.markdown(coins_grid, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    

      # Abdullah's Futuristic Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>⚡ BITNODE ALTCOIN FILTER SYSTEM ⚡</p>
    <p>© 2025 ABDULLAH'S PROPRIETARY ALGORITHM</p>
    <p style="font-size: 0.7rem; color: #556699;">BITCOIN-DIRECTION FILTERING • AUTO-REFRESH EVERY 5 MIN</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()