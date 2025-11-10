import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Mobile-friendly setup
st.set_page_config(
    page_title="Zohaib's Bitcoin Tracker",
    page_icon="₿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile styling with Zohaib's trademark
st.markdown("""
<style>
    .main > div {
        padding: 0.5rem;
    }
    .stMetric {
        padding: 0.5rem;
    }
    .signal-buy {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .signal-sell {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    .signal-neutral {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    .trademark {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 1rem;
    }
    .feature-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0d6efd;
    }
    .price-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 2px solid #e9ecef;
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
        
        # Create plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=tor_percentages,
            mode='lines+markers',
            name='Tor %',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Tor Percentage Trend (Last 24 Hours)",
            xaxis_title="Time",
            yaxis_title="Tor Percentage (%)",
            height=300,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig

def main():
    # Initialize analyzer
    analyzer = BitcoinNodeAnalyzer()
    
    # Header with Zohaib's trademark
    st.title("₿ Zohaib's Bitcoin Tracker")
    st.markdown("Tor Node Trend Analyzer • Network Signals • Live Price")
    
    # ALWAYS SHOW BTC PRICE - No button needed
    st.markdown("---")
    st.subheader("💰 Live BTC Price")
    
    # Get BTC price automatically (no button required)
    btc_price = get_btc_price()
    
    if btc_price:
        # Display price in a nice box
        st.markdown('<div class="price-box">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.metric(
                label="Bitcoin Price (USD)",
                value=f"${btc_price:,.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="24h Change",
                value="Live",  # You can add actual 24h change if needed
                delta=None
            )
        
        with col3:
            st.metric(
                label="Status", 
                value="🟢 Live",
                delta=None
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"🕒 Price updated: {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.error("❌ Could not fetch BTC price")
    
    # Refresh button for node data only
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📊 Network Analysis")
    with col2:
        if st.button("🔄 Update Node Data", key="refresh_main"):
            with st.spinner("Analyzing network data..."):
                if analyzer.update_network_data():
                    st.success("Node data updated!")
                    st.rerun()
                else:
                    st.error("Node data update failed")
    
    # Get current node data
    if len(analyzer.historical_data) > 0:
        current_data = analyzer.historical_data[-1]
        
        # TOR TREND ANALYZER SECTION
        st.markdown("---")
        st.subheader("🕵️ Tor Node Trend Analyzer")
        
        # Calculate Tor trend
        tor_trend_data = analyzer.calculate_tor_trend(current_data['tor_percentage'])
        
        # Display Tor trend results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Previous Tor %", f"{tor_trend_data['previous_tor']}%")
        
        with col2:
            st.metric("Current Tor %", f"{tor_trend_data['current_tor']}%")
        
        with col3:
            trend_value = tor_trend_data['tor_trend']
            st.metric("Tor Trend", f"{trend_value:+.2f}%")
        
        # Display market bias with color coding
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
        st.markdown(f"### → Market Bias: {bias_text} {emoji}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # NETWORK TREND SIGNAL SECTION
        st.markdown("---")
        st.subheader("📈 Network Trend Signal")
        
        signal_data = analyzer.calculate_network_signal(current_data)
        
        # Display signal with color coding
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
        
        st.markdown(f'<div class="{bias_class}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Active Nodes", f"{signal_data['active_nodes']:,}")
            st.metric("Total Nodes", f"{signal_data['total_nodes']:,}")
            st.metric("Previous Total", f"{signal_data['previous_total']:,}")
        
        with col2:
            st.metric("Active Ratio", f"{signal_data['active_ratio']:.4f}")
            st.metric("Trend", f"{signal_data['trend']:+.4f}")
            st.metric("Final Signal", f"{signal_data['signal']:+.4f}")
        
        st.markdown(f"### → {signal_text} SIGNAL {emoji}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # TOR TREND CHART
        st.markdown("---")
        st.subheader("📊 Tor Trend Chart")
        
        tor_chart = analyzer.plot_tor_trend_chart()
        if tor_chart:
            st.plotly_chart(tor_chart, use_container_width=True)
        else:
            st.info("Collecting more data for chart...")
        
        # NETWORK HEALTH SUMMARY
        st.markdown("---")
        st.subheader("🌐 Network Health Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_data['tor_percentage'] > 20:
                status = "🟢 Excellent"
            elif current_data['tor_percentage'] > 10:
                status = "🟡 Good"
            else:
                status = "🔴 Low"
            st.metric("Tor Privacy", status)
        
        with col2:
            if signal_data['active_ratio'] > 0.8:
                status = "🟢 Excellent"
            elif signal_data['active_ratio'] > 0.6:
                status = "🟡 Good"
            else:
                status = "🔴 Low"
            st.metric("Network Activity", status)
        
        with col3:
            if signal_data['trend'] > 0.01:
                status = "🟢 Growing"
            elif signal_data['trend'] < -0.01:
                status = "🔴 Shrinking"
            else:
                status = "🟡 Stable"
            st.metric("Network Trend", status)
        
        # Last update time
        last_time = datetime.fromisoformat(current_data['timestamp'])
        st.caption(f"🕒 Node data updated: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Historical data info
        if len(analyzer.historical_data) > 1:
            st.caption(f"📊 Data points: {len(analyzer.historical_data)} snapshots")
    
    else:
        st.info("📱 Tap 'Update Node Data' above to load network analysis!")
    
    # Explanation Section
    with st.expander("ℹ️ Understanding Tor Trend Analysis", expanded=True):
        st.markdown("""
        **Tor Trend Analyzer Formula:**
        ```
        Tor Trend = (Current Tor % - Previous Tor %) ÷ Previous Tor %
        ```
        
        **Market Bias Interpretation:**
        - **BEARISH/SELL BIAS (📉)**: Tor Trend > 0 (More privacy = Sell signal)
        - **BULLISH/BUY BIAS (📈)**: Tor Trend < 0 (Less privacy = Buy signal)  
        - **NEUTRAL (➡️)**: Tor Trend ≈ 0 (Stable privacy = Neutral)
        
        **Why This Works:**
        - Increasing Tor % = More privacy = Often precedes price drops
        - Decreasing Tor % = Less privacy = Often precedes price rises
        - Based on the observation that privacy spikes correlate with bearish sentiment
        
        **Network Trend Signal Formula:**
        ```
        Signal = (Active Nodes ÷ Total Nodes) × ((Current Total Nodes − Previous Total Nodes) ÷ Previous Total Nodes)
        ```
        """)
    
    # Auto-refresh suggestion
    st.markdown("---")
    st.info("💡 **Pro Tip:** The BTC price updates automatically every time you load the page. Node data updates when you click the button.")
    
    # Zohaib's Trademark Footer
    st.markdown("---")
    st.markdown('<div class="trademark">© 2025 Zohaib\'s Bitcoin Tracker • Tor Node Trend Analyzer</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
