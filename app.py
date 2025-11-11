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
    
    .cyber-card:hover {
        border-color: #00ffff;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
        transform: translateY(-2px);
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
        position: relative;
        overflow: hidden;
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

class AltcoinSignalGenerator:
    def __init__(self):
        self.coins = [
            "ETH/USDT", "LTC/USDT", "SOL/USDT", "ADA/USDT", 
            "AVAX/USDT", "DOT/USDT", "LINK/USDT"
        ]
        self.binance_base_url = "https://api.binance.com/api/v3"
    
    def get_coin_price(self, symbol):
        """Get current price for a coin"""
        try:
            binance_symbol = symbol.replace("/", "")
            response = requests.get(f"{self.binance_base_url}/ticker/price?symbol={binance_symbol}", timeout=5)
            response.raise_for_status()
            return float(response.json()['price'])
        except:
            return None
    
    def get_klines_data(self, symbol, interval='1h', limit=100):
        """Get historical klines data for EMA calculation"""
        try:
            binance_symbol = symbol.replace("/", "")
            url = f"{self.binance_base_url}/klines"
            params = {
                'symbol': binance_symbol,
                'interval': interval,
                'limit': limit
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            klines = response.json()
            
            # Extract closing prices
            closes = [float(k[4]) for k in klines]
            volumes = [float(k[5]) for k in klines]
            
            return closes, volumes
        except Exception as e:
            print(f"Error fetching klines for {symbol}: {e}")
            return None, None
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        
        ema = []
        multiplier = 2 / (period + 1)
        
        # Start with SMA
        sma = sum(prices[:period]) / period
        ema.append(sma)
        
        # Calculate EMA for remaining prices
        for price in prices[period:]:
            ema_value = (price - ema[-1]) * multiplier + ema[-1]
            ema.append(ema_value)
        
        return ema[-1]  # Return latest EMA value
    
    def get_funding_rate(self, symbol):
        """Get funding rate for perpetual contracts"""
        try:
            # For demonstration, we'll simulate funding rates
            # In production, use Binance Futures API
            base_symbol = symbol.replace("/USDT", "").lower()
            funding_url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={base_symbol.upper()}USDT"
            response = requests.get(funding_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get('lastFundingRate', 0)) * 100  # Convert to percentage
            else:
                # Fallback: simulate realistic funding rates
                return np.random.uniform(-0.02, 0.03)
        except:
            # Fallback simulation
            return np.random.uniform(-0.02, 0.03)
    
    def analyze_coin_trend(self, symbol):
        """Analyze individual coin trend for confirmation"""
        try:
            closes, volumes = self.get_klines_data(symbol)
            if closes is None or len(closes) < 50:
                return None, None, None
            
            # Calculate EMAs
            ema_20 = self.calculate_ema(closes, 20)
            ema_50 = self.calculate_ema(closes, 50)
            
            # Calculate volume trend (current vs average)
            current_volume = volumes[-1] if volumes else 0
            avg_volume = np.mean(volumes[-20:]) if len(volumes) >= 20 else current_volume
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Get funding rate
            funding_rate = self.get_funding_rate(symbol)
            
            return ema_20, ema_50, volume_ratio, funding_rate
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None, None, None, None
    
    def generate_signals(self, global_signal, tor_percentage, network_trend):
        """Generate altcoin signals based on Bitnode global signal"""
        signals = []
        
        for coin in self.coins:
            try:
                # Get current price
                current_price = self.get_coin_price(coin)
                if current_price is None:
                    continue
                
                # Analyze coin-specific metrics
                ema_20, ema_50, volume_ratio, funding_rate = self.analyze_coin_trend(coin)
                
                if ema_20 is None:
                    continue
                
                signal_data = {
                    "coin": coin,
                    "current_price": current_price,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                
                # BITNODE SELL SIGNAL LOGIC
                if global_signal == "SELL":
                    confirmation_factors = 0
                    
                    # Check SELL confirmation factors
                    if ema_20 < ema_50:  # Death cross
                        confirmation_factors += 1
                    if volume_ratio < 0.8:  # Volume drop
                        confirmation_factors += 1
                    if funding_rate < 0:  # Negative funding
                        confirmation_factors += 1
                    if network_trend < 0 and tor_percentage > 5:  # Bitnode sell bias
                        confirmation_factors += 1
                    
                    if confirmation_factors >= 2:  # At least 2 confirmations
                        signal_data["signal"] = "SELL"
                        if confirmation_factors >= 3:
                            signal_data["confidence"] = "High"
                        else:
                            signal_data["confidence"] = "Medium"
                        signals.append(signal_data)
                
                # BITNODE BUY SIGNAL LOGIC  
                elif global_signal == "BUY":
                    confirmation_factors = 0
                    
                    # Check BUY confirmation factors
                    if ema_20 > ema_50:  # Golden cross
                        confirmation_factors += 1
                    if funding_rate > 0:  # Positive funding
                        confirmation_factors += 1
                    if volume_ratio > 1.2:  # Volume surge
                        confirmation_factors += 1
                    if network_trend > 0 and tor_percentage < 5:  # Bitnode buy bias
                        confirmation_factors += 1
                    
                    if confirmation_factors >= 2:  # At least 2 confirmations
                        signal_data["signal"] = "BUY"
                        if confirmation_factors >= 3:
                            signal_data["confidence"] = "High"
                        else:
                            signal_data["confidence"] = "Medium"
                        signals.append(signal_data)
                
            except Exception as e:
                print(f"Error processing {coin}: {e}")
                continue
        
        return signals

def get_btc_price():
    """Get BTC price from multiple sources with fallback"""
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        response.raise_for_status()
        return float(response.json()['price'])
    except:
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
            response.raise_for_status()
            return float(response.json()['bitcoin']['usd'])
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
                if node_info and isinstance(node_info, list) and len(node_info) > 0:
                    active_nodes += 1
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
        
        current_time = datetime.now()
        target_time = current_time - timedelta(hours=24)
        
        closest_snapshot = None
        min_time_diff = float('inf')
        
        for snapshot in self.historical_data[:-1]:
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
        """Get previous day's Tor percentage"""
        if len(self.historical_data) < 2:
            return None
        
        current_time = datetime.now()
        target_time = current_time - timedelta(hours=24)
        
        closest_snapshot = None
        min_time_diff = float('inf')
        
        for snapshot in self.historical_data[:-1]:
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
                'trend': 0,
                'signal': "NEUTRAL",
                'suggestion': "INSUFFICIENT_DATA"
            }
        
        active_ratio = current_data['active_ratio']
        trend = (current_data['total_nodes'] - previous_total) / previous_total
        signal_strength = active_ratio * trend
        
        # Determine Bitnode Global Signal
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
        previous_tor_percentage = self.get_previous_tor_percentage()
        
        if previous_tor_percentage is None or previous_tor_percentage == 0:
            return {
                'previous_tor': "No data",
                'current_tor': current_tor_percentage,
                'tor_trend': 0,
                'bias': "INSUFFICIENT_DATA"
            }
        
        tor_trend = (current_tor_percentage - previous_tor_percentage) / previous_tor_percentage
        
        # Abdullah's Formula for Market Bias
        network_trend_data = self.calculate_network_signal(self.historical_data[-1] if self.historical_data else {})
        network_trend = network_trend_data.get('trend', 0)
        
        if network_trend < 0 and current_tor_percentage > 5:
            bias = "BEARISH (Sell Bias)"
        elif network_trend > 0 and current_tor_percentage < 5:
            bias = "BULLISH (Buy Bias)"
        else:
            bias = "NEUTRAL"
        
        return {
            'previous_tor': round(previous_tor_percentage, 2),
            'current_tor': round(current_tor_percentage, 2),
            'tor_trend': round(tor_trend * 100, 2),
            'bias': bias,
            'network_trend': network_trend
        }
    
    def update_network_data(self):
        """Fetch new data and update historical records"""
        current_data = self.fetch_node_data()
        if not current_data:
            return False
        
        self.historical_data.append(current_data)
        if len(self.historical_data) > 1008:
            self.historical_data = self.historical_data[-1008:]
        
        self.save_historical_data()
        return True

def main():
    # Initialize analyzers
    analyzer = BitcoinNodeAnalyzer()
    altcoin_generator = AltcoinSignalGenerator()
    
    # Auto-refresh functionality
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    if 'last_altcoin_refresh' not in st.session_state:
        st.session_state.last_altcoin_refresh = datetime.now()
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
 
    if 'altcoin_signals' not in st.session_state:
        st.session_state.altcoin_signals = []
    
    current_time = datetime.now()
    
    # Auto-refresh logic (30 minutes for node data, 5 minutes for altcoins)
    node_refresh_interval = timedelta(minutes=30)
    altcoin_refresh_interval = timedelta(minutes=5)
    
    # Node data auto-refresh
    if st.session_state.auto_refresh and current_time - st.session_state.last_refresh > node_refresh_interval:
        with st.spinner("🔄 Auto-updating node data..."):
            if analyzer.update_network_data():
                st.session_state.last_refresh = current_time
                st.rerun()
    
    # Altcoin signals auto-refresh
    if st.session_state.auto_refresh and current_time - st.session_state.last_altcoin_refresh > altcoin_refresh_interval:
        with st.spinner("🔄 Updating altcoin signals..."):
            if len(analyzer.historical_data) > 0:
                current_data = analyzer.historical_data[-1]
                network_signal = analyzer.calculate_network_signal(current_data)
                tor_trend = analyzer.calculate_tor_trend(current_data['tor_percentage'])
                
                global_signal = network_signal.get('global_signal', 'NEUTRAL')
                tor_percentage = current_data['tor_percentage']
                network_trend = tor_trend.get('network_trend', 0)
                
                if global_signal in ['BUY', 'SELL']:
                    signals = altcoin_generator.generate_signals(global_signal, tor_percentage, network_trend)
                    st.session_state.altcoin_signals = signals
                    st.session_state.last_altcoin_refresh = current_time
                    st.rerun()
    
    # Futuristic Header
    st.markdown('<h1 class="cyber-header">🚀 BITNODE ALTCOIN FILTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cyber-subheader">BITCOIN-DIRECTION ALGORITHM • MAJOR ALTCOINS • AUTO-REFRESH</p>', unsafe_allow_html=True)
    
    # AUTO-REFRESH STATUS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        # Auto-refresh status
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
            with st.spinner("Updating node data..."):
                if analyzer.update_network_data():
                    st.session_state.last_refresh = datetime.now()
                    st.success("✅ Node data updated!")
                    st.rerun()
    
    with col4:
        if st.button("🎯 ALTCOINS", key="refresh_altcoins", use_container_width=True):
            with st.spinner("Updating altcoin signals..."):
                if len(analyzer.historical_data) > 0:
                    current_data = analyzer.historical_data[-1]
                    network_signal = analyzer.calculate_network_signal(current_data)
                    tor_trend = analyzer.calculate_tor_trend(current_data['tor_percentage'])
                    
                    global_signal = network_signal.get('global_signal', 'NEUTRAL')
                    tor_percentage = current_data['tor_percentage']
                    network_trend = tor_trend.get('network_trend', 0)
                    
                    if global_signal in ['BUY', 'SELL']:
                        signals = altcoin_generator.generate_signals(global_signal, tor_percentage, network_trend)
                        st.session_state.altcoin_signals = signals
                        st.session_state.last_altcoin_refresh = datetime.now()
                        st.success(f"✅ {len(signals)} altcoin signals updated!")
                        st.rerun()
    
    # BITNODE GLOBAL SIGNAL SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌐 BITNODE GLOBAL SIGNAL</h2>', unsafe_allow_html=True)
    
    if len(analyzer.historical_data) > 0:
        current_data = analyzer.historical_data[-1]
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
    
    # ALTCOIN SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 ALTCOIN FILTER SIGNALS</h2>', unsafe_allow_html=True)
    
    if st.session_state.altcoin_signals:
        st.markdown(f'<p style="color: #8892b0; text-align: center;">Filtered {len(st.session_state.altcoin_signals)} coins following Bitcoin direction</p>', unsafe_allow_html=True)
        
        for signal in st.session_state.altcoin_signals:
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
            mime="application/json"
        )
    else:
        st.info("🎯 No filtered altcoin signals yet. Waiting for Bitnode global signal confirmation...")
    
    # ALGORITHM EXPLANATION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("🔍 ALGORITHM LOGIC", expanded=False):
        st.markdown("""
        <div style="font-family: Rajdhani; color: #ffffff;">
        <h3 style="color: #00ffff; font-family: Orbitron;">🎯 ALTCOIN FILTER ALGORITHM</h3>
        
        <h4 style="color: #ff00ff; margin-top: 1rem;">BITNODE GLOBAL SIGNAL:</h4>
        <ul>
            <li><strong>BUY</strong>: Network expanding + Low Tor usage</li>
            <li><strong>SELL</strong>: Network contracting + High Tor usage</li>
        </ul>
        
        <h4 style="color: #00ff7f; margin-top: 1rem;">ALTCOIN CONFIRMATION:</h4>
        <ul>
            <li><strong>BUY Signals</strong>: Require 2+ confirmations from:
                <ul>
                    <li>EMA 20 > EMA 50 (Golden Cross)</li>
                    <li>Positive Funding Rate</li>
                    <li>Volume Surge (>20% above average)</li>
                    <li>Bitnode Buy Bias confirmed</li>
                </ul>
            </li>
            <li><strong>SELL Signals</strong>: Require 2+ confirmations from:
                <ul>
                    <li>EMA 20 < EMA 50 (Death Cross)</li>
                    <li>Negative Funding Rate</li>
                    <li>Volume Drop (<80% of average)</li>
                    <li>Bitnode Sell Bias confirmed</li>
                </ul>
            </li>
        </ul>
        
        <h4 style="color: #ffd700; margin-top: 1rem;">COVERED ALTCOINS:</h4>
        <p>ETH/USDT, LTC/USDT, SOL/USDT, ADA/USDT, AVAX/USDT, DOT/USDT, LINK/USDT</p>
        </div>
        """, unsafe_allow_html=True)
    
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
 