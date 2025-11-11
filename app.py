import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import logging
from typing import Dict, List, Tuple, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitnodeTracker:
    def __init__(self):
        self.coins = ["BTC", "ETH", "LTC", "BCH", "SOL", "ADA", "AVAX", "DOGE", "DOT", "LINK", "BNB"]
        self.bitnode_api_url = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.price_api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.snapshots_history = []
        self.cache_duration = 600  # 10 minutes in seconds
        self.last_fetch_time = 0
        self.price_cache = {}
        self.price_cache_time = 0
        
    def fetch_bitnode_data(self) -> Optional[Dict]:
        """Fetch data from Bitnodes API with caching and error handling"""
        current_time = time.time()
        
        # Check cache
        if current_time - self.last_fetch_time < self.cache_duration and hasattr(self, 'cached_data'):
            logger.info("Using cached Bitnode data")
            return self.cached_data
            
        try:
            logger.info("Fetching fresh Bitnode data")
            response = requests.get(self.bitnode_api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.cached_data = data
            self.last_fetch_time = current_time
            
            # Store in history (keep last 2 snapshots)
            self.snapshots_history.append({
                'timestamp': datetime.now(),
                'data': data
            })
            
            # Keep only last 2 snapshots for trend calculation
            if len(self.snapshots_history) > 2:
                self.snapshots_history = self.snapshots_history[-2:]
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Bitnode data: {e}")
            return getattr(self, 'cached_data', None)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return getattr(self, 'cached_data', None)
    
    def fetch_prices(self) -> Dict:
        """Fetch current prices from CoinGecko API"""
        current_time = time.time()
        
        # Cache prices for 1 minute
        if current_time - self.price_cache_time < 60 and self.price_cache:
            return self.price_cache
            
        try:
            coin_ids = {
                "BTC": "bitcoin",
                "ETH": "ethereum", 
                "LTC": "litecoin",
                "BCH": "bitcoin-cash",
                "SOL": "solana",
                "ADA": "cardano",
                "AVAX": "avalanche-2",
                "DOGE": "dogecoin",
                "DOT": "polkadot",
                "LINK": "chainlink",
                "BNB": "binancecoin"
            }
            
            ids_param = ",".join(coin_ids.values())
            url = f"{self.price_api_url}?ids={ids_param}&vs_currencies=usd&include_24hr_change=true"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Transform to our format
            prices = {}
            for coin, coin_id in coin_ids.items():
                if coin_id in data:
                    prices[coin] = {
                        'price': data[coin_id].get('usd', 0),
                        'change_24h': data[coin_id].get('usd_24h_change', 0)
                    }
            
            self.price_cache = prices
            self.price_cache_time = current_time
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching prices: {e}")
            return self.price_cache  # Return cached data even if stale
    
    def calculate_tor_trend(self) -> Tuple[float, str, str]:
        """Calculate Tor Trend and return value, signal, and trend"""
        if len(self.snapshots_history) < 2:
            return 0.0, "NEUTRAL", "➡️"
            
        current_data = self.snapshots_history[-1]['data']
        previous_data = self.snapshots_history[-2]['data']
        
        try:
            # Calculate Tor percentages
            current_total = current_data.get('total_nodes', 1)
            previous_total = previous_data.get('total_nodes', 1)
            
            current_tor_nodes = current_data.get('total_nodes', 0) - current_data.get('clearnet_nodes', 0)
            previous_tor_nodes = previous_data.get('total_nodes', 0) - previous_data.get('clearnet_nodes', 0)
            
            current_tor_pct = (current_tor_nodes / current_total) * 100 if current_total > 0 else 0
            previous_tor_pct = (previous_tor_nodes / previous_total) * 100 if previous_total > 0 else 0
            
            # Avoid division by zero
            if previous_tor_pct == 0:
                return 0.0, "NEUTRAL", "➡️"
                
            tor_trend = ((current_tor_pct - previous_tor_pct) / previous_tor_pct) * 100
            
            # Determine signal
            if tor_trend > 0.1:  # Small threshold for stability
                signal = "BEARISH"
                emoji = "📉"
            elif tor_trend < -0.1:
                signal = "BULLISH" 
                emoji = "📈"
            else:
                signal = "NEUTRAL"
                emoji = "➡️"
                
            return tor_trend, signal, emoji
            
        except Exception as e:
            logger.error(f"Error calculating Tor trend: {e}")
            return 0.0, "NEUTRAL", "➡️"
    
    def calculate_network_signal(self) -> Tuple[float, str]:
        """Calculate Network Signal and return value and signal"""
        if len(self.snapshots_history) < 2:
            return 0.0, "SIDEWAYS"
            
        current_data = self.snapshots_history[-1]['data']
        previous_data = self.snapshots_history[-2]['data']
        
        try:
            current_total = current_data.get('total_nodes', 0)
            previous_total = previous_data.get('total_nodes', 0)
            current_active = current_data.get('active_nodes', current_total * 0.6)  # Estimate if not available
            
            # Avoid division by zero
            if previous_total == 0 or current_total == 0:
                return 0.0, "SIDEWAYS"
            
            active_ratio = current_active / current_total
            node_growth = (current_total - previous_total) / previous_total
            
            signal_value = active_ratio * node_growth
            
            # Determine signal
            if signal_value > 0.01:
                signal = "BUY"
            elif signal_value < -0.01:
                signal = "SELL"
            else:
                signal = "SIDEWAYS"
                
            return signal_value, signal
            
        except Exception as e:
            logger.error(f"Error calculating network signal: {e}")
            return 0.0, "SIDEWAYS"
    
    def get_bitcoin_signal(self) -> Dict:
        """Get overall Bitcoin signal by combining both metrics"""
        tor_trend, tor_signal, tor_emoji = self.calculate_tor_trend()
        network_signal_value, network_signal = self.calculate_network_signal()
        
        # Combine signals (Network Signal takes priority, Tor Trend as bias)
        if network_signal == "BUY":
            final_signal = "BUY"
        elif network_signal == "SELL":
            final_signal = "SELL" 
        else:
            # If network is sideways, use Tor trend bias
            if tor_signal == "BULLISH":
                final_signal = "BUY"
            elif tor_signal == "BEARISH":
                final_signal = "SELL"
            else:
                final_signal = "SIDEWAYS"
        
        return {
            'tor_trend': tor_trend,
            'tor_signal': tor_signal,
            'tor_emoji': tor_emoji,
            'network_signal': network_signal_value,
            'network_signal_type': network_signal,
            'final_signal': final_signal,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_all_signals(self) -> Tuple[List[Dict], Dict]:
        """Get signals for all coins based on Bitcoin's signal"""
        bitcoin_signal = self.get_bitcoin_signal()
        prices = self.fetch_prices()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        signals = []
        for coin in self.coins:
            coin_price = prices.get(coin, {}).get('price', 0)
            change_24h = prices.get(coin, {}).get('change_24h', 0)
            
            signals.append({
                "coin": coin,
                "signal": bitcoin_signal['final_signal'],
                "price": coin_price,
                "change_24h": change_24h,
                "time": current_time
            })
            
        return signals, bitcoin_signal

def create_network_visualization(bitcoin_signal: Dict, current_data: Dict) -> go.Figure:
    """Create futuristic network visualization"""
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=("Network Health", "Privacy Metric")
    )
    
    # Network Health Gauge
    network_value = bitcoin_signal['network_signal'] * 1000  # Scale for better visualization
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = network_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "NETWORK SIGNAL"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-15, 15]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-15, -5], 'color': "red"},
                {'range': [-5, 5], 'color': "yellow"},
                {'range': [5, 15], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': network_value
            }
        }
    ), row=1, col=1)
    
    # Tor Trend Gauge
    tor_value = bitcoin_signal['tor_trend']
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = tor_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "TOR TREND"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-2, 2]},
            'bar': {'color': "purple"},
            'steps': [
                {'range': [-2, -0.5], 'color': "green"},
                {'range': [-0.5, 0.5], 'color': "gray"},
                {'range': [0.5, 2], 'color': "red"}
            ]
        }
    ), row=1, col=2)
    
    fig.update_layout(
        height=300,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Abdullah's Bitnode Tracker",
        page_icon="₿",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Futuristic CSS with dark theme
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        .main-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            background: linear-gradient(45deg, #00D4FF, #0099FF, #0066FF, #0033FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 900;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }
        
        .sub-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: #00D4FF;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #00D4FF;
            padding-bottom: 0.5rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            border: 1px solid #00D4FF;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .buy-signal { 
            color: #00FF88 !important; 
            font-weight: 900;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        .sell-signal { 
            color: #FF4B4B !important; 
            font-weight: 900;
            text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
        }
        .sideways-signal { 
            color: #FFD700 !important; 
            font-weight: 900;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }
        
        .stDataFrame {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
            border-radius: 15px;
            border: 1px solid #00D4FF;
        }
        
        .stButton>button {
            background: linear-gradient(45deg, #00D4FF, #0099FF);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 2rem;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
        }
        
        .positive-change { color: #00FF88; }
        .negative-change { color: #FF4B4B; }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .main-header { font-size: 2.5rem; }
            .sub-header { font-size: 1.4rem; }
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown('<h1 class="main-header">ABDULLAH\'S BITNODE TRACKER</h1>', unsafe_allow_html=True)
    
    # Initialize tracker
    if 'tracker' not in st.session_state:
        st.session_state.tracker = BitnodeTracker()
        st.session_state.last_update = None
    
    tracker = st.session_state.tracker
    
    # Auto-refresh logic
    refresh_interval = 300  # 5 minutes
    current_time = time.time()
    
    if (st.session_state.last_update is None or 
        current_time - st.session_state.last_update > refresh_interval):
        
        with st.spinner("🔄 CONNECTING TO BITNODE NETWORK..."):
            tracker.fetch_bitnode_data()
        st.session_state.last_update = current_time
    
    # Fetch data
    signals, bitcoin_signal = tracker.get_all_signals()
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 MASTER SIGNAL", bitcoin_signal['final_signal'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌐 TOTAL NODES", 
                 f"{tracker.snapshots_history[-1]['data'].get('total_nodes', 'N/A') if tracker.snapshots_history else 'N/A':,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        network_change = bitcoin_signal['network_signal'] * 100
        st.metric("📡 NETWORK TREND", f"{network_change:+.4f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🕶️ TOR TREND", f"{bitcoin_signal['tor_trend']:+.4f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Network Visualization
    st.markdown('<div class="sub-header">NETWORK ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)
    if tracker.snapshots_history:
        fig = create_network_visualization(bitcoin_signal, tracker.snapshots_history[-1]['data'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Trading Signals Table
    st.markdown('<div class="sub-header">CRYPTO SIGNALS MATRIX</div>', unsafe_allow_html=True)
    
    # Create enhanced DataFrame
    df_data = []
    for signal in signals:
        change_color = "positive-change" if signal['change_24h'] > 0 else "negative-change"
        change_emoji = "🟢" if signal['change_24h'] > 0 else "🔴"
        
        df_data.append({
            'COIN': f"🪙 {signal['coin']}",
            'PRICE': f"${signal['price']:,.2f}" if signal['price'] > 0 else "N/A",
            '24H CHANGE': f"<span class='{change_color}'>{change_emoji} {signal['change_24h']:+.2f}%</span>",
            'SIGNAL': signal['signal'],
            'TIME': signal['time']
        })
    
    df = pd.DataFrame(df_data)
    
    # Display styled table
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Signal Distribution
    st.markdown('<div class="sub-header">SIGNAL DISTRIBUTION</div>', unsafe_allow_html=True)
    
    buy_count = len([s for s in signals if s['signal'] == 'BUY'])
    sell_count = len([s for s in signals if s['signal'] == 'SELL'])
    sideways_count = len([s for s in signals if s['signal'] == 'SIDEWAYS'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="metric-card" style="text-align: center;"><h3 class="buy-signal">BUY SIGNALS</h3><h2>{buy_count}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="text-align: center;"><h3 class="sell-signal">SELL SIGNALS</h3><h2>{sell_count}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="text-align: center;"><h3 class="sideways-signal">SIDEWAYS</h3><h2>{sideways_count}</h2></div>', unsafe_allow_html=True)
    
    # Raw JSON output
    with st.expander("📊 RAW DATA EXPORT"):
        st.json(signals)
    
    # Footer
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.write(f"**LAST UPDATE:** {bitcoin_signal['timestamp']}")
    with footer_col2:
        st.write("**REFRESH CYCLE:** 5 MINUTES")
    with footer_col3:
        st.write("**NETWORK STATUS:** 🟢 LIVE")
    
    # Manual refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 FORCE REFRESH DATA", use_container_width=True):
            with st.spinner("SYNCING WITH BITNODE NETWORK..."):
                tracker.fetch_bitnode_data()
            st.session_state.last_update = time.time()
            st.rerun()
    
    # System Info
    with st.expander("🔧 SYSTEM INFORMATION"):
        st.markdown("""
        ### TRADING LOGIC
        
        **BITCOIN MASTER SIGNAL (DETERMINES ALL COINS):**
        
        **TOR TREND FORMULA:**
        ```
        Tor Trend = (Current Tor % - Previous Tor %) ÷ Previous Tor %
        • 📉 BEARISH/SELL: Tor Trend > 0 (More privacy usage)
        • 📈 BULLISH/BUY: Tor Trend < 0 (Less privacy usage)  
        • ➡️ NEUTRAL: Tor Trend ≈ 0 (Stable privacy)
        ```
        
        **NETWORK SIGNAL FORMULA:**
        ```
        Signal = (Active Nodes ÷ Total Nodes) × ((Current Total Nodes − Previous Total Nodes) ÷ Previous Total Nodes)
        • BUY: Signal > +0.01
        • SELL: Signal < -0.01
        ```
        
        **ABDULLAH'S ALGORITHM:**
        - All coins strictly follow Bitcoin's Bitnode signal
        - Pure Bitcoin network metrics only
        - Real-time price integration
        - Automated 5-minute refresh cycles
        """)

if __name__ == "__main__":
    main()  
  