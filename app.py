import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitnodeTracker:
    def __init__(self):
        self.coins = ["ETH", "LTC", "BCH", "SOL", "ADA", "AVAX", "DOGE", "DOT", "LINK", "BNB"]
        self.bitnode_api_url = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.snapshots_history = []
        self.cache_duration = 600  # 10 minutes in seconds
        self.last_fetch_time = 0
        
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
    
    def get_all_signals(self) -> List[Dict]:
        """Get signals for all follower coins based on Bitcoin's signal"""
        bitcoin_signal = self.get_bitcoin_signal()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        signals = []
        for coin in self.coins:
            signals.append({
                "coin": coin,
                "signal": bitcoin_signal['final_signal'],
                "time": current_time
            })
            
        return signals, bitcoin_signal

def main():
    st.set_page_config(
        page_title="Abdullah's Bitnode Follower Tracker",
        page_icon="₿",
        layout="wide"
    )
    
    # Custom CSS for better mobile experience
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        .buy-signal { color: #00D100; font-weight: bold; }
        .sell-signal { color: #FF4B4B; font-weight: bold; }
        .sideways-signal { color: #808080; font-weight: bold; }
        @media (max-width: 768px) {
            .main-header { font-size: 2rem; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">Abdullah\'s Bitnode Follower Tracker</h1>', unsafe_allow_html=True)
    
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
        
        with st.spinner("Fetching latest Bitnode data..."):
            tracker.fetch_bitnode_data()
        st.session_state.last_update = current_time
    
    # Display Bitcoin Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bitcoin Network Metrics")
        
        if tracker.snapshots_history:
            current_data = tracker.snapshots_history[-1]['data']
            st.metric("Total Nodes", current_data.get('total_nodes', 'N/A'))
            st.metric("Clearnet Nodes", current_data.get('clearnet_nodes', 'N/A'))
            
            tor_nodes = current_data.get('total_nodes', 0) - current_data.get('clearnet_nodes', 0)
            st.metric("Tor Nodes", tor_nodes)
        else:
            st.info("Waiting for Bitnode data...")
    
    with col2:
        st.subheader("📈 Bitcoin Signal Analysis")
        bitcoin_signal = tracker.get_bitcoin_signal()
        
        # Tor Trend
        tor_col1, tor_col2 = st.columns([2, 1])
        with tor_col1:
            st.write("**Tor Trend:**")
        with tor_col2:
            st.write(f"{bitcoin_signal['tor_emoji']} {bitcoin_signal['tor_signal']}")
        
        st.write(f"Trend Value: {bitcoin_signal['tor_trend']:.4f}%")
        
        # Network Signal
        network_col1, network_col2 = st.columns([2, 1])
        with network_col1:
            st.write("**Network Signal:**")
        with network_col2:
            st.write(f"{bitcoin_signal['network_signal_type']}")
        
        st.write(f"Signal Value: {bitcoin_signal['network_signal']:.6f}")
        
        # Final Bitcoin Signal
        st.markdown("---")
        signal_class = ""
        if bitcoin_signal['final_signal'] == "BUY":
            signal_class = "buy-signal"
        elif bitcoin_signal['final_signal'] == "SELL":
            signal_class = "sell-signal"
        else:
            signal_class = "sideways-signal"
            
        st.markdown(f'<h3 class="{signal_class}">Bitcoin Master Signal: {bitcoin_signal["final_signal"]}</h3>', 
                   unsafe_allow_html=True)
    
    # Display Follower Coins Signals
    st.subheader("🎯 Follower Coins Trading Signals")
    
    signals, bitcoin_info = tracker.get_all_signals()
    
    # Create DataFrame for better display
    df = pd.DataFrame(signals)
    
    # Style the DataFrame
    def color_signal(val):
        if val == "BUY":
            return 'color: #00D100'
        elif val == "SELL":
            return 'color: #FF4B4B'
        else:
            return 'color: #808080'
    
    styled_df = df.style.applymap(color_signal, subset=['signal'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Raw JSON output (as requested)
    st.subheader("📋 Raw Signal Output")
    st.json(signals)
    
    # Last update info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Last Update:** {bitcoin_info['timestamp']}")
    with col2:
        st.write("**Refresh Interval:** 5 minutes")
    with col3:
        st.write("**Data Source:** Bitnodes.io")
    
    # Manual refresh button
    if st.button("🔄 Manual Refresh"):
        with st.spinner("Refreshing data..."):
            tracker.fetch_bitnode_data()
        st.session_state.last_update = time.time()
        st.rerun()
    
    # Explanation
    with st.expander("ℹ️ How This System Works"):
        st.markdown("""
        ### Trading Logic
        
        **Bitcoin Master Signal (Determines ALL follower coins):**
        
        **Tor Trend Formula:**
        ```
        Tor Trend = (Current Tor % - Previous Tor %) ÷ Previous Tor %
        • 📉 BEARISH/SELL: Tor Trend > 0 (More privacy usage)
        • 📈 BULLISH/BUY: Tor Trend < 0 (Less privacy usage)  
        • ➡️ NEUTRAL: Tor Trend ≈ 0 (Stable privacy)
        ```
        
        **Network Signal Formula:**
        ```
        Signal = (Active Nodes ÷ Total Nodes) × ((Current Total Nodes − Previous Total Nodes) ÷ Previous Total Nodes)
        • BUY: Signal > +0.01
        • SELL: Signal < -0.01  
        • SIDEWAYS: -0.01 ≤ Signal ≤ +0.01
        ```
        
        **Follower Coin Rule:**
        - All 10 coins strictly follow Bitcoin's Bitnode signal
        - No technical indicators, charts, or price analysis used
        - Pure Bitcoin network metrics only
        """)

if __name__ == "__main__":
    main()