import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

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
    
    .cyber-card:hover {
        border-color: #00ffff;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 127, 0.1) 0%, rgba(0, 100, 0, 0.3) 100%);
        border: 1px solid #00ff7f;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.3);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.1) 0%, rgba(100, 0, 0, 0.3) 100%);
        border: 1px solid #ff007f;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.3);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(100, 100, 0, 0.3) 100%);
        border: 1px solid #ffd700;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    .price-glow {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 255, 0.5);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
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
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        animation: shine 3s infinite linear;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .cyber-button {
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 100%);
        border: none;
        border-radius: 25px;
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .cyber-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.7);
    }
    
    .metric-cyber {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .trademark {
        text-align: center;
        color: #8892b0;
        font-family: 'Orbitron', monospace;
        font-size: 0.9rem;
        margin-top: 2rem;
        letter-spacing: 1px;
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
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def get_btc_price():
    """Get BTC price from multiple sources with fallback"""
    try:
        # Try Binance first
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        response.raise_for_status()
        return float(response.json()['price'])
    except:
        try:
            # Fallback to CoinGecko
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
            response.raise_for_status()
            return float(response.json()['bitcoin']['usd'])
        except:
            try:
                # Final fallback to Coinbase
                response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5)
                response.raise_for_status()
                return float(response.json()['data']['amount'])
            except:
                return None

class BitcoinNodeAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api ="https://bitnodes.io/api/v1/snapshots/latest/"
        self.load_historical_data()
    
    def load_historical_data(self):
        """Load historical node data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.historical_data = json.load(f)
            else:
                self.historical_data = []
        except:
            self.historical_data = []
    
    def save_historical_data(self):
        """Save current data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.historical_data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def fetch_node_data(self):
        """Fetch current node data from Bitnodes API"""
        try:
            response = requests.get(self.bitnodes_api, timeout=10)
            response.raise_for_status()
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
        except Exception as e:
            st.error(f"Error fetching node data: {e}")
            return None
    
    def get_previous_total_nodes(self):
        """Get previous day's total nodes"""
        if len(self.historical_data) < 2:
            return None
        
        # Get yesterday's data (look for data from ~24 hours ago)
        current_time = datetime.now()
        target_time = current_time - timedelta(hours=24)
        
        # Find the closest snapshot to 24 hours ago
        closest_snapshot = None
        min_time_diff = float('inf')
        
        for snapshot in self.historical_data[:-1]:  # Exclude current
            try:
                snapshot_time = datetime.fromisoformat(snapshot['timestamp'])
                time_diff = abs((snapshot_time - target_time).total_seconds())
                
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_snapshot = snapshot
            except:
                continue
        
        return closest_snapshot['total_nodes'] if closest_snapshot else None
    
    def get_previous_tor_percentage(self):
        """Get previous day's Tor percentage for trend analysis"""
        if len(self.historical_data) < 2:
            return None
        
        # Get yesterday's data (look for data from ~24 hours ago)
        current_time = datetime.now()
        target_time = current_time - timedelta(hours=24)
        
        # Find the closest snapshot to 24 hours ago
        closest_snapshot = None
        min_time_diff = float('inf')
        
        for snapshot in self.historical_data[:-1]:  # Exclude current
            try:
                snapshot_time = datetime.fromisoformat(snapshot['timestamp'])
                time_diff = abs((snapshot_time - target_time).total_seconds())
                
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_snapshot = snapshot
            except:
                continue
        
        return closest_snapshot['tor_percentage'] if closest_snapshot else None
    
    def calculate_network_signal(self, current_data):
        """Calculate trading signal based on network trends"""
        previous_total = self.get_previous_total_nodes()
        
        if previous_total is None or previous_total == 0:
            return {
                'active_nodes': current_data['active_nodes'],
                'total_nodes': current_data['total_nodes'],
                'previous_total': "No previous data",
                'active_ratio': current_data['active_ratio'],
                'trend': 0,
                'signal': 0,
                'suggestion': "INSUFFICIENT_DATA"
            }
        
        active_ratio = current_data['active_ratio']
        trend = (current_data['total_nodes'] - previous_total) / previous_total
        signal = active_ratio * trend
        
        # Determine suggestion
        if signal > 0.01:
            suggestion = "BUY"
        elif signal < -0.01:
            suggestion = "SELL"
        else:
            suggestion = "SIDEWAYS"
        
        return {
            'active_nodes': current_data['active_nodes'],
            'total_nodes': current_data['total_nodes'],
            'previous_total': previous_total,
            'active_ratio': round(active_ratio, 4),
            'trend': round(trend, 4),
            'signal': round(signal, 4),
            'suggestion': suggestion
        }
    
    def calculate_tor_trend(self, current_tor_percentage):
        """Calculate Tor trend and market bias"""
        previous_tor_percentage = self.get_previous_tor_percentage()
        
        if previous_tor_percentage is None or previous_tor_percentage == 0:
            return {
                'previous_tor': "No data",
                'current_tor': current_tor_percentage,
                'tor_trend': 0,
                'bias': "INSUFFICIENT_DATA"
            }
        
        # Calculate Tor Trend using your formula
        tor_trend = (current_tor_percentage - previous_tor_percentage) / previous_tor_percentage
        
        # Determine market bias based on your rules
        if tor_trend > 0.001:  # Small threshold to account for minor fluctuations
            bias = "BEARISH (Sell Bias)"
        elif tor_trend < -0.001:
            bias = "BULLISH (Buy Bias)"
        else:
            bias = "NEUTRAL"
        
        return {
            'previous_tor': round(previous_tor_percentage, 2),
            'current_tor': round(current_tor_percentage, 2),
            'tor_trend': round(tor_trend * 100, 2),  # Convert to percentage
            'bias': bias
        }
    
    def update_network_data(self):
        """Fetch new data and update historical records"""
        current_data = self.fetch_node_data()
        if not current_data:
            return False
        
        # Add to historical data
        self.historical_data.append(current_data)
        
        # Keep only last 7 days of data
        if len(self.historical_data) > 1008:
            self.historical_data = self.historical_data[-1008:]
        
        self.save_historical_data()
        return True
    
    def plot_tor_trend_chart(self):
        """Plot Tor percentage trend over time"""
        if len(self.historical_data) < 2:
            return None
        
        # Prepare data for plotting
        dates = []
        tor_percentages = []
        
        for entry in self.historical_data[-24:]:  # Last 24 data points
            try:
                date = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M')
                dates.append(date)
                tor_percentages.append(entry['tor_percentage'])
            except:
                continue
        
        if len(dates) < 2:
            return None
        
        # Create futuristic plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=tor_percentages,
            mode='lines+markers',
            name='Tor %',
            line=dict(color='#00ffff', width=4, shape='spline'),
            marker=dict(size=8, color='#ff00ff', line=dict(width=2, color='#ffffff')),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 255, 0.1)'
        ))
        
        fig.update_layout(
            title=dict(
                text="🕵️ Tor Percentage Trend (Last 24 Hours)",
                font=dict(family='Orbitron', size=20, color='#ffffff')
            ),
            xaxis=dict(
                title="Time",
                gridcolor='rgba(0, 255, 255, 0.1)',
                tickfont=dict(family='Rajdhani', color='#8892b0')
            ),
            yaxis=dict(
                title="Tor Percentage (%)",
                gridcolor='rgba(0, 255, 255, 0.1)',
                tickfont=dict(family='Rajdhani', color='#8892b0')
            ),
            plot_bgcolor='rgba(10, 15, 35, 0.5)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff'),
            height=400,
            showlegend=True
        )
        
        return fig

def main():
    # Initialize analyzer
    analyzer = BitcoinNodeAnalyzer()
    
    # Futuristic Header
    st.markdown('<h1 class="cyber-header">🚀 ABDULLAH\'S BITCOIN TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cyber-subheader">TOR NODE TREND ANALYZER • NETWORK SIGNALS • LIVE PRICE</p>', unsafe_allow_html=True)
    
    # LIVE BTC PRICE SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE BTC PRICE</h2>', unsafe_allow_html=True)
    
    # Get BTC price automatically
    btc_price = get_btc_price()
    
    if btc_price:
        # Display price in a futuristic glowing box
        st.markdown('<div class="price-glow">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f'<div style="text-align: center;"><span style="font-family: Orbitron; font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #00ffff, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${btc_price:,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">BITCOIN PRICE (USD)</p>', unsafe_allow_html=True)
        
        with col2:
            st.metric(
                label="24H STATUS",
                value="🟢 LIVE",
                delta="ACTIVE"
            )
        
        with col3:
            st.metric(
                label="DATA SOURCE", 
                value="BINANCE API",
                delta="PRIMARY"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">🕒 Price updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch BTC price")
    
    # Refresh button for node data
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">📊 NETWORK ANALYSIS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 UPDATE NODE DATA", key="refresh_main", use_container_width=True):
            with st.spinner("🔍 Analyzing network data..."):
                if analyzer.update_network_data():
                    st.success("✅ Node data updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Node data update failed")
    
    # Main content in two columns for better mobile layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Get current node data
        if len(analyzer.historical_data) > 0:
            current_data = analyzer.historical_data[-1]
            
            # TOR TREND ANALYZER SECTION
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="font-family: Orbitron; color: #00ffff; text-align: center;">🕵️ TOR TREND ANALYZER</h3>', unsafe_allow_html=True)
            
            # Calculate Tor trend
            tor_trend_data = analyzer.calculate_tor_trend(current_data['tor_percentage'])
            
            # Display Tor trend results in a grid
            col1a, col2a, col3a = st.columns(3)
            
            with col1a:
                st.metric("📊 PREVIOUS TOR %", f"{tor_trend_data['previous_tor']}%")
            
            with col2a:
                st.metric("🎯 CURRENT TOR %", f"{tor_trend_data['current_tor']}%")
            
            with col3a:
                trend_value = tor_trend_data['tor_trend']
                st.metric("📈 TOR TREND", f"{trend_value:+.2f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display market bias with cyber styling
            if tor_trend_data['bias'] == "BEARISH (Sell Bias)":
                bias_class = "signal-sell"
                emoji = "📉"
                bias_text = "SELL BIAS"
            elif tor_trend_data['bias'] == "BULLISH (Buy Bias)":
                bias_class = "signal-buy"
                emoji = "📈"
                bias_text = "BUY BIAS"
            else:
                bias_class = "signal-neutral"
                emoji = "➡️"
                bias_text = "NEUTRAL"
            
            st.markdown(f'<div class="{bias_class}">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-family: Orbitron; text-align: center; margin: 0;">🚀 MARKET BIAS: {bias_text} {emoji}</h3>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if len(analyzer.historical_data) > 0:
            # NETWORK TREND SIGNAL SECTION
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="font-family: Orbitron; color: #00ffff; text-align: center;">📈 NETWORK TREND SIGNAL</h3>', unsafe_allow_html=True)
            
            signal_data = analyzer.calculate_network_signal(current_data)
            
            # Display network metrics
            col1b, col2b = st.columns(2)
            
            with col1b:
                st.metric("🟢 ACTIVE NODES", f"{signal_data['active_nodes']:,}")
                st.metric("📊 TOTAL NODES", f"{signal_data['total_nodes']:,}")
                st.metric("🕒 PREVIOUS TOTAL", f"{signal_data['previous_total']:,}")
            
            with col2b:
                st.metric("⚡ ACTIVE RATIO", f"{signal_data['active_ratio']:.4f}")
                st.metric("📈 TREND", f"{signal_data['trend']:+.4f}")
                st.metric("🎯 FINAL SIGNAL", f"{signal_data['signal']:+.4f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display signal with cyber styling
            if signal_data['suggestion'] == "BUY":
                signal_class = "signal-buy"
                emoji = "🟢"
                signal_text = "STRONG BUY"
            elif signal_data['suggestion'] == "SELL":
                signal_class = "signal-sell"
                emoji = "🔴"
                signal_text = "STRONG SELL"
            else:
                signal_class = "signal-neutral"
                emoji = "🟡"
                signal_text = "NEUTRAL"
            
            st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-family: Orbitron; text-align: center; margin: 0;">🎯 {signal_text} SIGNAL {emoji}</h3>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # TOR TREND CHART
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 TOR TREND CHART</h2>', unsafe_allow_html=True)
    
    tor_chart = analyzer.plot_tor_trend_chart()
    if tor_chart:
        st.plotly_chart(tor_chart, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("🔄 Collecting more data for chart...")
    
    # NETWORK HEALTH SUMMARY
    if len(analyzer.historical_data) > 0:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🌐 NETWORK HEALTH SUMMARY</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_data['tor_percentage'] > 20:
                status = "🟢 EXCELLENT"
                delta = "HIGH PRIVACY"
            elif current_data['tor_percentage'] > 10:
                status = "🟡 GOOD"
                delta = "MODERATE"
            else:
                status = "🔴 LOW"
                delta = "LOW PRIVACY"
            st.metric("TOR PRIVACY", status, delta=delta)
        
        with col2:
            if signal_data['active_ratio'] > 0.8:
                status = "🟢 EXCELLENT"
                delta = "HIGH ACTIVITY"
            elif signal_data['active_ratio'] > 0.6:
                status = "🟡 GOOD"
                delta = "MODERATE"
            else:
                status = "🔴 LOW"
                delta = "LOW ACTIVITY"
            st.metric("NETWORK ACTIVITY", status, delta=delta)
        
        with col3:
            if signal_data['trend'] > 0.01:
                status = "🟢 GROWING"
                delta = "EXPANDING"
            elif signal_data['trend'] < -0.01:
                status = "🔴 SHRINKING"
                delta = "CONTRACTING"
            else:
                status = "🟡 STABLE"
                delta = "STEADY"
            st.metric("NETWORK TREND", status, delta=delta)
        
        # Last update time
        last_time = datetime.fromisoformat(current_data['timestamp'])
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">🕒 Node data updated: {last_time.strftime("%Y-%m-%d %H:%M:%S")}</p>', unsafe_allow_html=True)
        
        # Historical data info
        if len(analyzer.historical_data) > 1:
            st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">📊 Data points: {len(analyzer.historical_data)} snapshots collected</p>', unsafe_allow_html=True)
    
    else:
        st.info("📱 Tap 'UPDATE NODE DATA' above to load network analysis!")

    # Abdullah's Futuristic Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>⚡ CYBER BITCOIN ANALYTICS PLATFORM ⚡</p>
    <p>© 2025 ABDULLAH'S BITCOIN TRACKER • TOR NODE TREND ANALYZER</p>
    <p style="font-size: 0.7rem; color: #556699;">BUILT WITH STREAMLIT • POWERED BY BITNODES API</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()