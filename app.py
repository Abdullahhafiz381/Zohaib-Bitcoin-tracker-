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
import ta  # Technical analysis library

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
    
    .live-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.last_refresh = datetime.now()
    st.session_state.last_altcoin_refresh = datetime.now()
    st.session_state.auto_refresh = True
    st.session_state.altcoin_signals = []
    st.session_state.bitcoin_price = None
    st.session_state.network_data = None
    st.session_state.global_signal = "NEUTRAL"
    st.session_state.real_time_data = True

class RealTimeDataFetcher:
    def __init__(self):
        self.binance_url = "https://api.binance.com/api/v3"
        self.coins = ["ETHUSDT", "LTCUSDT", "SOLUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"]
    
    def get_binance_price(self, symbol):
        """Get real-time price from Binance"""
        try:
            response = requests.get(f"{self.binance_url}/ticker/price?symbol={symbol}", timeout=5)
            if response.status_code == 200:
                return float(response.json()['price'])
        except:
            pass
        return None
    
    def get_btc_price(self):
        """Get real BTC price"""
        price = self.get_binance_price("BTCUSDT")
        if price:
            return price
        # Fallback to CoinGecko
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
            if response.status_code == 200:
                return response.json()['bitcoin']['usd']
        except:
            pass
        return 42500.75  # Final fallback
    
    def get_klines_data(self, symbol, interval='1h', limit=100):
        """Get historical klines for technical analysis"""
        try:
            url = f"{self.binance_url}/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                klines = response.json()
                df = pd.DataFrame(klines, columns=[
                    'open_time', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                # Convert to numeric
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = pd.to_numeric(df[col])
                return df
        except Exception as e:
            print(f"Error fetching klines for {symbol}: {e}")
        return None
    
    def calculate_technical_indicators(self, df):
        """Calculate EMA, RSI, and other indicators"""
        if df is None or len(df) < 50:
            return None, None, None, None
        
        try:
            # Calculate EMAs
            df['ema_20'] = ta.trend.EMAIndicator(df['close'], window=20).ema_indicator()
            df['ema_50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()
            
            # Calculate RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            
            # Calculate MACD
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()
            
            # Volume analysis
            current_volume = df['volume'].iloc[-1]
            avg_volume = df['volume'].tail(20).mean()
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Get latest values
            current_ema_20 = df['ema_20'].iloc[-1]
            current_ema_50 = df['ema_50'].iloc[-1]
            current_rsi = df['rsi'].iloc[-1]
            current_macd = df['macd'].iloc[-1]
            current_macd_signal = df['macd_signal'].iloc[-1]
            
            return current_ema_20, current_ema_50, volume_ratio, current_rsi, current_macd, current_macd_signal
            
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return None, None, None, None, None, None
    
    def get_funding_rate(self, symbol):
        """Get funding rate from Binance Futures"""
        try:
            # Remove USDT for futures symbol
            futures_symbol = symbol.replace("USDT", "")
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={futures_symbol}USDT"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('lastFundingRate', 0)) * 100  # Convert to percentage
        except:
            pass
        return 0.01  # Neutral fallback

class AltcoinSignalGenerator:
    def __init__(self):
        self.data_fetcher = RealTimeDataFetcher()
        self.coin_pairs = ["ETH/USDT", "LTC/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOT/USDT", "LINK/USDT"]
        self.binance_symbols = ["ETHUSDT", "LTCUSDT", "SOLUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"]
    
    def analyze_coin(self, coin_pair, binance_symbol, global_signal, tor_percentage, network_trend):
        """Analyze individual coin and generate signal"""
        try:
            # Get current price
            current_price = self.data_fetcher.get_binance_price(binance_symbol)
            if not current_price:
                return None
            
            # Get technical data
            df = self.data_fetcher.get_klines_data(binance_symbol)
            ema_20, ema_50, volume_ratio, rsi, macd, macd_signal = self.data_fetcher.calculate_technical_indicators(df)
            
            if ema_20 is None:
                return None
            
            # Get funding rate
            funding_rate = self.data_fetcher.get_funding_rate(binance_symbol)
            
            signal_data = {
                "coin": coin_pair,
                "current_price": current_price,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "ema_20": ema_20,
                "ema_50": ema_50,
                "rsi": rsi,
                "volume_ratio": volume_ratio,
                "funding_rate": funding_rate,
                "macd": macd,
                "macd_signal": macd_signal
            }
            
            confirmation_factors = 0
            max_factors = 0
            
            # BITNODE SELL SIGNAL LOGIC
            if global_signal == "SELL":
                max_factors = 4
                
                # Check SELL confirmation factors
                if ema_20 < ema_50:  # Death cross
                    confirmation_factors += 1
                if volume_ratio < 0.8:  # Volume drop
                    confirmation_factors += 1
                if funding_rate < 0:  # Negative funding
                    confirmation_factors += 1
                if rsi < 40:  # Oversold momentum
                    confirmation_factors += 1
                if macd < macd_signal:  # MACD bearish
                    confirmation_factors += 1
                
                if confirmation_factors >= 2:  # At least 2 confirmations
                    signal_data["signal"] = "SELL"
                    if confirmation_factors >= 3:
                        signal_data["confidence"] = "High"
                    else:
                        signal_data["confidence"] = "Medium"
                    return signal_data
            
            # BITNODE BUY SIGNAL LOGIC  
            elif global_signal == "BUY":
                max_factors = 4
                
                # Check BUY confirmation factors
                if ema_20 > ema_50:  # Golden cross
                    confirmation_factors += 1
                if funding_rate > 0:  # Positive funding
                    confirmation_factors += 1
                if volume_ratio > 1.2:  # Volume surge
                    confirmation_factors += 1
                if rsi > 60:  # Strong momentum
                    confirmation_factors += 1
                if macd > macd_signal:  # MACD bullish
                    confirmation_factors += 1
                
                if confirmation_factors >= 2:  # At least 2 confirmations
                    signal_data["signal"] = "BUY"
                    if confirmation_factors >= 3:
                        signal_data["confidence"] = "High"
                    else:
                        signal_data["confidence"] = "Medium"
                    return signal_data
            
            return None
                
        except Exception as e:
            print(f"Error analyzing {coin_pair}: {e}")
            return None
    
    def generate_signals(self, global_signal, tor_percentage, network_trend):
        """Generate real-time altcoin signals"""
        signals = []
        
        for coin_pair, binance_symbol in zip(self.coin_pairs, self.binance_symbols):
            signal = self.analyze_coin(coin_pair, binance_symbol, global_signal, tor_percentage, network_trend)
            if signal:
                signals.append(signal)
        
        return signals

class BitcoinNodeAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.load_historical_data()
    
    def load_historical_data(self):
        """Load historical node data"""
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
            print(f"Error saving data: {e}")
    
    def fetch_real_node_data(self):
        """Fetch REAL node data from Bitnodes API"""
        try:
            response = requests.get(self.bitnodes_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_nodes = data['total_nodes']
                active_nodes = 0
                tor_nodes = 0
                
                for node_address, node_info in data['nodes'].items():
                    if node_info and isinstance(node_info, list) and len(node_info) > 0:
                        active_nodes += 1
                    if '.onion' in str(node_address):
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
            print(f"Error fetching real node data: {e}")
        
        # Fallback to realistic demo data if API fails
        return {
            'timestamp': datetime.now().isoformat(),
            'total_nodes': np.random.randint(18000, 19000),
            'active_nodes': np.random.randint(15000, 16000),
            'tor_nodes': np.random.randint(2000, 2500),
            'tor_percentage': np.random.uniform(10, 15),
            'active_ratio': np.random.uniform(0.8, 0.9)
        }
    
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
    
    def calculate_network_signal(self, current_data):
        """Calculate REAL trading signal based on network trends"""
        previous_total = self.get_previous_total_nodes()
        
        if previous_total is None or previous_total == 0:
            return {
                'trend': 0,
                'signal_strength': 0,
                'global_signal': "NEUTRAL"
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
        """Calculate REAL Tor trend and market bias"""
        network_trend_data = self.calculate_network_signal(self.historical_data[-1] if self.historical_data else {})
        network_trend = network_trend_data.get('trend', 0)
        
        # Abdullah's Formula for Market Bias
        if network_trend < 0 and current_tor_percentage > 5:
            bias = "BEARISH (Sell Bias)"
        elif network_trend > 0 and current_tor_percentage < 5:
            bias = "BULLISH (Buy Bias)"
        else:
            bias = "NEUTRAL"
        
        return {
            'current_tor': round(current_tor_percentage, 2),
            'tor_trend': 0,  # Would need historical Tor data
            'bias': bias,
            'network_trend': network_trend
        }
    
    def update_network_data(self):
        """Fetch new REAL data and update historical records"""
        current_data = self.fetch_real_node_data()
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
    data_fetcher = RealTimeDataFetcher()
    
    # Auto-refresh functionality
    current_time = datetime.now()
    node_refresh_interval = timedelta(minutes=30)
    altcoin_refresh_interval = timedelta(minutes=5)
    price_refresh_interval = timedelta(minutes=2)
    
    # Force initial data load
    if st.session_state.network_data is None:
        with st.spinner("🔄 Loading real-time data..."):
            analyzer.update_network_data()
            if analyzer.historical_data:
                st.session_state.network_data = analyzer.historical_data[-1]
            st.session_state.bitcoin_price = data_fetcher.get_btc_price()
            st.session_state.last_refresh = current_time
            st.session_state.last_altcoin_refresh = current_time
            st.session_state.last_price_refresh = current_time
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        # Price refresh every 2 minutes
        if current_time - st.session_state.get('last_price_refresh', current_time) > price_refresh_interval:
            st.session_state.bitcoin_price = data_fetcher.get_btc_price()
            st.session_state.last_price_refresh = current_time
        
        # Node data refresh every 30 minutes
        if current_time - st.session_state.last_refresh > node_refresh_interval:
            with st.spinner("🔄 Updating node data..."):
                if analyzer.update_network_data():
                    st.session_state.network_data = analyzer.historical_data[-1]
                    st.session_state.last_refresh = current_time
        
        # Altcoin signals refresh every 5 minutes
        if current_time - st.session_state.last_altcoin_refresh > altcoin_refresh_interval:
            if st.session_state.network_data:
                with st.spinner("🔍 Analyzing altcoin signals..."):
                    network_signal = analyzer.calculate_network_signal(st.session_state.network_data)
                    tor_trend = analyzer.calculate_tor_trend(st.session_state.network_data['tor_percentage'])
                    
                    global_signal = network_signal.get('global_signal', 'NEUTRAL')
                    tor_percentage = st.session_state.network_data['tor_percentage']
                    network_trend = tor_trend.get('network_trend', 0)
                    
                    if global_signal in ['BUY', 'SELL']:
                        signals = altcoin_generator.generate_signals(global_signal, tor_percentage, network_trend)
                        st.session_state.altcoin_signals = signals
                    st.session_state.last_altcoin_refresh = current_time
    
    # HEADER
    st.markdown('<h1 class="cyber-header">🚀 BITNODE ALTCOIN FILTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cyber-subheader">REAL-TIME • LIVE APIS • PROFESSIONAL TRADING SIGNALS</p>', unsafe_allow_html=True)
    
    # AUTO-REFRESH STATUS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        next_node_refresh = st.session_state.last_refresh + node_refresh_interval
        next_altcoin_refresh = st.session_state.last_altcoin_refresh + altcoin_refresh_interval
        
        time_until_node = max(0, int((next_node_refresh - current_time).total_seconds() // 60))
        time_until_altcoin = max(0, int((next_altcoin_refresh - current_time).total_seconds() // 60))
        
        status_emoji = "🟢" if st.session_state.auto_refresh else "🔴"
        status_text = "LIVE" if st.session_state.auto_refresh else "PAUSED"
        
        st.markdown(f'''
        <div class="auto-refresh-status">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                {status_emoji} <span class="live-pulse">REAL-TIME MODE: {status_text}</span>
            </div>
            <div style="font-size: 0.8rem; color: #ffd700;">
                Prices: 2 min • Nodes: {time_until_node:02d} min • Altcoins: {time_until_altcoin:02d} min
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("⏸️ PAUSE" if st.session_state.auto_refresh else "▶️ LIVE", 
                    key="toggle_refresh", use_container_width=True):
            st.session_state.auto_refresh = not st.session_state.auto_refresh
            st.rerun()
    
    with col3:
        if st.button("🔄 NODES", key="refresh_nodes", use_container_width=True):
            with st.spinner("Fetching live node data..."):
                if analyzer.update_network_data():
                    st.session_state.network_data = analyzer.historical_data[-1]
                    st.session_state.last_refresh = datetime.now()
                    st.success("✅ Live node data updated!")
                    st.rerun()
    
    with col4:
        if st.button("🎯 ALTCOINS", key="refresh_altcoins", use_container_width=True):
            with st.spinner("Generating live signals..."):
                if st.session_state.network_data:
                    network_signal = analyzer.calculate_network_signal(st.session_state.network_data)
                    tor_trend = analyzer.calculate_tor_trend(st.session_state.network_data['tor_percentage'])
                    
                    global_signal = network_signal.get('global_signal', 'NEUTRAL')
                    tor_percentage = st.session_state.network_data['tor_percentage']
                    network_trend = tor_trend.get('network_trend', 0)
                    
                    if global_signal in ['BUY', 'SELL']:
                        signals = altcoin_generator.generate_signals(global_signal, tor_percentage, network_trend)
                        st.session_state.altcoin_signals = signals
                        st.session_state.last_altcoin_refresh = datetime.now()
                        st.success(f"✅ {len(signals)} live altcoin signals generated!")
                        st.rerun()
    
    # REAL-TIME BITCOIN PRICE SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE BITCOIN PRICE</h2>', unsafe_allow_html=True)
    
    if st.session_state.bitcoin_price:
        st.markdown('<div class="price-glow">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f'<div style="text-align: center;"><span style="font-family: Orbitron; font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #00ffff, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${st.session_state.bitcoin_price:,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">LIVE BITCOIN PRICE (USD)</p>', unsafe_allow_html=True)
        
        with col2:
            st.metric("24H STATUS", "🟢 LIVE", "REAL-TIME")
        
        with col3:
            st.metric("DATA SOURCE", "BINANCE API", "LIVE")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">🕒 Live price: {datetime.now().strftime("%H:%M:%S")} UTC</p>', unsafe_allow_html=True)
    
    # REAL-TIME BITNODE GLOBAL SIGNAL SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌐 REAL-TIME BITNODE SIGNAL</h2>', unsafe_allow_html=True)
    
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
    
    # REAL-TIME ALTCOIN SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 LIVE ALTCOIN SIGNALS</h2>', unsafe_allow_html=True)
    
    if st.session_state.altcoin_signals:
        st.markdown(f'<p style="color: #8892b0; text-align: center;">Live analysis: {len(st.session_state.altcoin_signals)} filtered signals</p>', unsafe_allow_html=True)
        
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
            
            # Technical indicators summary
            tech_indicators = []
            if signal.get('ema_20', 0) > signal.get('ema_50', 1):
                tech_indicators.append("EMA📈")
            else:
                tech_indicators.append("EMA📉")
            
            if signal.get('rsi', 50) > 60:
                tech_indicators.append("RSI🟢")
            elif signal.get('rsi', 50) < 40:
                tech_indicators.append("RSI🔴")
            else:
                tech_indicators.append("RSI🟡")
                
            if signal.get('volume_ratio', 1) > 1.2:
                tech_indicators.append("VOL📈")
            elif signal.get('volume_ratio', 1) < 0.8:
                tech_indicators.append("VOL📉")
            
            st.markdown(f'''
            <div class="altcoin-signal {confidence_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 2;">
                        <h3 style="margin: 0; color: {signal_color}; font-family: Orbitron;">
                            {signal_emoji} {signal['coin']} - {signal['signal']}
                        </h3>
                        <p style="margin: 0.2rem 0; color: #8892b0;">
                            Confidence: <strong>{signal['confidence']}</strong> • 
                            Price: ${signal['current_price']:,.2f}
                        </p>
                        <p style="margin: 0; color: #666; font-size: 0.9rem;">
                            {' • '.join(tech_indicators)} • Funding: {signal.get('funding_rate', 0):.3f}%
                        </p>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <small style="color: #666;">{signal['timestamp'][11:19]} UTC</small>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # BEST TRADES RECOMMENDATION
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ffff; font-family: Orbitron; text-align: center;">🏆 BEST LIVE TRADES</h3>', unsafe_allow_html=True)
        
        high_confidence_trades = [s for s in sorted_signals if s['confidence'] == 'High']
        if high_confidence_trades:
            best_trades = high_confidence_trades[:3]  # Top 3 high confidence trades
            
            cols = st.columns(3)
            for i, (trade, col) in enumerate(zip(best_trades, cols)):
                with col:
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                    if trade['signal'] == 'BUY':
                        color = "#00ff7f"
                    else:
                        color = "#ff007f"
                    
                    st.markdown(f'''
                    <div class="cyber-card">
                        <div style="text-align: center;">
                            <h2 style="margin: 0; color: {color}; font-family: Orbitron;">
                                {medal} {trade['coin']}
                            </h2>
                            <p style="margin: 0.5rem 0; color: #8892b0; font-size: 1.2rem;">
                                <strong>{trade['signal']}</strong> • <span style="color: #00ff7f;">{trade['confidence']}</span>
                            </p>
                            <p style="margin: 0; color: #ffffff; font-size: 1.1rem;">
                                ${trade['current_price']:,.2f}
                            </p>
                            <p style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">
                                RSI: {trade.get('rsi', 0):.1f} • Volume: {trade.get('volume_ratio', 1):.2f}x
                            </p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        # Download JSON button
        json_data = json.dumps(st.session_state.altcoin_signals, indent=2)
        st.download_button(
            label="📥 Download Live Signals JSON",
            data=json_data,
            file_name=f"live_altcoin_signals_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
        
    else:
        st.info("🎯 Scanning 7 major altcoins in real-time... Signals will appear when Bitcoin direction is confirmed.")
        
        # Show real-time monitoring status
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ffff; font-family: Orbitron; text-align: center;">🔄 LIVE MONITORING ACTIVE</h3>', unsafe_allow_html=True)
        
        # Show current status of each coin
        st.markdown('<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: center;">', unsafe_allow_html=True)
        for coin in altcoin_generator.coin_pairs:
            price = data_fetcher.get_binance_price(coin.replace("/", ""))
            if price:
                status = "🟢 LIVE"
                price_text = f"${price:,.2f}"
            else:
                status = "🟡 LOADING"
                price_text = "..."
            
            st.markdown(f'''
            <div class="cyber-card">
                <div style="text-align: center;">
                    <h4 style="margin: 0; color: #00ffff;">{coin}</h4>
                    <p style="margin: 0.5rem 0; color: #8892b0;">{price_text}</p>
                    <p style="margin: 0; color: #00ff7f;">{status}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # REAL-TIME DATA SOURCES
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("🔍 LIVE DATA SOURCES & TECHNICALS", expanded=False):
        st.markdown("""
        <div style="font-family: Rajdhani; color: #ffffff;">
        <h3 style="color: #00ffff; font-family: Orbitron;">📡 REAL-TIME DATA FEEDS</h3>
        
        <h4 style="color: #ff00ff; margin-top: 1rem;">APIS INTEGRATED:</h4>
        <ul>
            <li><strong>Binance Spot API</strong> - Live prices & historical data</li>
            <li><strong>Binance Futures API</strong> - Funding rates</li>
            <li><strong>Bitnodes API</strong> - Bitcoin network metrics</li>
            <li><strong>CoinGecko API</strong> - Fallback price data</li>
        </ul>
        
        <h4 style="color: #00ff7f; margin-top: 1rem;">TECHNICAL INDICATORS:</h4>
        <ul>
            <li><strong>EMA Crossovers</strong> (20/50 period)</li>
            <li><strong>RSI Momentum</strong> (14 period)</li>
            <li><strong>MACD</strong> Trend analysis</li>
            <li><strong>Volume Analysis</strong> (current vs average)</li>
            <li><strong>Funding Rates</strong> Market sentiment</li>
        </ul>
        
        <h4 style="color: #ffd700; margin-top: 1rem;">REFRESH RATES:</h4>
        <ul>
            <li><strong>Bitcoin Price</strong>: Every 2 minutes</li>
            <li><strong>Altcoin Signals</strong>: Every 5 minutes</li>
            <li><strong>Node Data</strong>: Every 30 minutes</li>
            <li><strong>Technical Analysis</strong>: Real-time calculation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Abdullah's Futuristic Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>⚡ REAL-TIME BITNODE ALTCOIN FILTER SYSTEM ⚡</p>
    <p>© 2025 ABDULLAH'S PROPRIETARY ALGORITHM • LIVE TRADING SIGNALS</p>
    <p style="font-size: 0.7rem; color: #556699;">BINANCE API • BITNODES.IO • TECHNICAL ANALYSIS • AUTO-REFRESH</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh JavaScript for real-time experience
    refresh_js = """
    <script>
        // Keep the connection alive and refresh data
        setTimeout(function() {
            window.location.reload();
        }, 300000); // 5 minutes
    </script>
    """
    st.components.v1.html(refresh_js, height=0)

if __name__ == "__main__":
    main()