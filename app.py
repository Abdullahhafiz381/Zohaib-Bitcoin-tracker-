import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# ... (keep all your existing CSS and setup code) ...

class CryptoAnalyzer:
    def __init__(self, data_file="network_data.json"):
        self.data_file = data_file
        self.bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.load_node_data()
    
    def load_node_data(self):
        """Load only current and previous node data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.current_data = data.get('current_data')
                    self.previous_data = data.get('previous_data')
            else:
                self.current_data = None
                self.previous_data = None
        except:
            self.current_data = None
            self.previous_data = None
    
    def save_node_data(self):
        """Save current and previous node data"""
        try:
            data = {
                'current_data': self.current_data,
                'previous_data': self.previous_data,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
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
    
    def update_node_data(self):
        """Fetch new data and shift current to previous"""
        new_data = self.fetch_node_data()
        if not new_data:
            return False
        
        # Shift current to previous, set new data as current
        self.previous_data = self.current_data
        self.current_data = new_data
        
        self.save_node_data()
        return True
    
    def calculate_tor_signal(self):
        """Calculate signal based on difference between current and previous Tor nodes"""
        if not self.current_data or not self.previous_data:
            return {
                'current_tor': self.current_data['tor_nodes'] if self.current_data else 0,
                'previous_tor': self.previous_data['tor_nodes'] if self.previous_data else 0,
                'tor_change': 0,
                'signal': "INSUFFICIENT_DATA",
                'bias': "NEED MORE DATA"
            }
        
        current_tor = self.current_data['tor_nodes']
        previous_tor = self.previous_data['tor_nodes']
        
        # Calculate absolute change in Tor nodes
        tor_change = current_tor - previous_tor
        
        # Simple signal logic based on Tor node change
        if tor_change > 10:  # Tor nodes increased by more than 10
            signal = "STRONG SELL"
            bias = "BEARISH"
        elif tor_change > 5:  # Tor nodes increased by 6-10
            signal = "SELL" 
            bias = "SLIGHTLY BEARISH"
        elif tor_change < -10:  # Tor nodes decreased by more than 10
            signal = "STRONG BUY"
            bias = "BULLISH"
        elif tor_change < -5:  # Tor nodes decreased by 6-10
            signal = "BUY"
            bias = "SLIGHTLY BULLISH"
        else:  # Small change (-5 to +5)
            signal = "HOLD"
            bias = "NEUTRAL"
        
        return {
            'current_tor': current_tor,
            'previous_tor': previous_tor,
            'tor_change': tor_change,
            'signal': signal,
            'bias': bias
        }
    
    def calculate_network_signal(self):
        """Calculate signal based on total node changes"""
        if not self.current_data or not self.previous_data:
            return {
                'current_total': self.current_data['total_nodes'] if self.current_data else 0,
                'previous_total': self.previous_data['total_nodes'] if self.previous_data else 0,
                'total_change': 0,
                'network_signal': "INSUFFICIENT_DATA"
            }
        
        current_total = self.current_data['total_nodes']
        previous_total = self.previous_data['total_nodes']
        total_change = current_total - previous_total
        
        # Network health signal
        if total_change > 50:
            network_signal = "NETWORK GROWING"
        elif total_change > 0:
            network_signal = "NETWORK STABLE" 
        else:
            network_signal = "NETWORK SHRINKING"
        
        return {
            'current_total': current_total,
            'previous_total': previous_total,
            'total_change': total_change,
            'network_signal': network_signal
        }

def get_crypto_prices():
    """Get crypto prices from multiple sources with fallback"""
    coins = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum', 
        'LTCUSDT': 'litecoin',
        'BCHUSDT': 'bitcoin-cash',
        'SOLUSDT': 'solana',
        'ADAUSDT': 'cardano',
        'AVAXUSDT': 'avalanche-2',
        'DOGEUSDT': 'dogecoin',
        'DOTUSDT': 'polkadot',
        'LINKUSDT': 'chainlink',
        'BNBUSDT': 'binancecoin'
    }
    
    prices = {}
    
    try:
        # Try Binance first for all coins
        for symbol in coins.keys():
            try:
                response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5)
                response.raise_for_status()
                prices[symbol] = float(response.json()['price'])
            except:
                prices[symbol] = None
        
        # Fill missing prices with CoinGecko
        missing_coins = [coin_id for symbol, coin_id in coins.items() if prices.get(symbol) is None]
        if missing_coins:
            try:
                coin_ids = ','.join(missing_coins)
                response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd", timeout=5)
                response.raise_for_status()
                gecko_data = response.json()
                
                for symbol, coin_id in coins.items():
                    if prices.get(symbol) is None and coin_id in gecko_data:
                        prices[symbol] = float(gecko_data[coin_id]['usd'])
            except:
                pass
                
    except Exception as e:
        st.error(f"Error fetching prices: {e}")
    
    return prices

def get_coin_display_name(symbol):
    """Get display name for crypto symbols"""
    names = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum',
        'LTCUSDT': 'Litecoin',
        'BCHUSDT': 'Bitcoin Cash',
        'SOLUSDT': 'Solana',
        'ADAUSDT': 'Cardano',
        'AVAXUSDT': 'Avalanche',
        'DOGEUSDT': 'Dogecoin',
        'DOTUSDT': 'Polkadot',
        'LINKUSDT': 'Chainlink',
        'BNBUSDT': 'Binance Coin'
    }
    return names.get(symbol, symbol)

def get_coin_emoji(symbol):
    """Get emoji for crypto symbols"""
    emojis = {
        'BTCUSDT': '₿',
        'ETHUSDT': '🔷',
        'LTCUSDT': '🔶',
        'BCHUSDT': '💰',
        'SOLUSDT': '🔥',
        'ADAUSDT': '🔰',
        'AVAXUSDT': '❄️',
        'DOGEUSDT': '🐕',
        'DOTUSDT': '🔴',
        'LINKUSDT': '🔗',
        'BNBUSDT': '💎'
    }
    return emojis.get(symbol, '⚡')

def main():
    # Initialize analyzer
    analyzer = CryptoAnalyzer()
    
    # Futuristic Header
    st.markdown('<h1 class="cyber-header">🚀 ABDULLAH\'S CRYPTO TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cyber-subheader">REAL-TIME TOR NODE SIGNALS • LIVE PRICES • AUTO-REFRESH</p>', unsafe_allow_html=True)
    
    # LIVE CRYPTO PRICES SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💰 LIVE CRYPTO PRICES</h2>', unsafe_allow_html=True)
    
    # Get all crypto prices
    prices = get_crypto_prices()
    
    if prices:
        # Display BTC price prominently
        btc_price = prices.get('BTCUSDT')
        if btc_price:
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
        
        # Display all coins in a grid
        st.markdown('<h3 style="font-family: Orbitron; color: #00ffff; margin: 1rem 0;">📊 ALTCOIN MARKET</h3>', unsafe_allow_html=True)
        
        # Create columns for coin grid
        coins_to_display = {k: v for k, v in prices.items() if k != 'BTCUSDT'}
        cols = st.columns(4)
        
        for idx, (symbol, price) in enumerate(coins_to_display.items()):
            if price:
                with cols[idx % 4]:
                    emoji = get_coin_emoji(symbol)
                    name = get_coin_display_name(symbol)            
                    st.markdown(f'''
                    <div class="coin-card">
                        <div style="text-align: center;">
                            <h4 style="font-family: Orbitron; color: #00ffff; margin: 0.5rem 0; font-size: 1.1rem;">{emoji} {name}</h4>
                            <p style="font-family: Orbitron; font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">${price:,.2f}</p>
                            <p style="color: #8892b0; font-family: Rajdhani; font-size: 0.9rem; margin: 0;">{symbol}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani;">🕒 Prices updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch crypto prices")
    
    # AUTO-REFRESH NODE DATA SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="section-header">🔄 REAL-TIME NODE ANALYSIS</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 UPDATE NODE DATA", key="refresh_main", use_container_width=True):
            with st.spinner("🔄 Updating node data..."):
                if analyzer.update_node_data():
                    st.success("✅ Node data updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update node data")
    
    # Display current node data status
    if analyzer.current_data:
        current_time = datetime.fromisoformat(analyzer.current_data['timestamp'])
        st.markdown(f'<p style="text-align: center; color: #00ffff; font-family: Rajdhani;">📊 Current data from: {current_time.strftime("%Y-%m-%d %H:%M:%S")}</p>', unsafe_allow_html=True)
    
    # TOR NODE SIGNAL ANALYSIS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 TOR NODE SIGNAL ANALYSIS</h2>', unsafe_allow_html=True)
    
    # Main content in two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # TOR NODE COMPARISON
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Orbitron; color: #00ffff; text-align: center;">🔄 NODE COMPARISON</h3>', unsafe_allow_html=True)
        
        tor_signal = analyzer.calculate_tor_signal()
        network_signal = analyzer.calculate_network_signal()
        
        # Display node comparison
        if analyzer.previous_data:
            col1a, col2a = st.columns(2)
            
            with col1a:
                st.metric("🕒 PREVIOUS TOR NODES", f"{tor_signal['previous_tor']:,}")
                st.metric("🕒 PREVIOUS TOTAL NODES", f"{network_signal['previous_total']:,}")
            
            with col2a:
                st.metric("🟢 CURRENT TOR NODES", f"{tor_signal['current_tor']:,}")
                st.metric("🟢 CURRENT TOTAL NODES", f"{network_signal['current_total']:,}")
            
            # Display changes
            st.markdown('<div style="text-align: center; margin: 1rem 0;">', unsafe_allow_html=True)
            st.metric("📈 TOR NODE CHANGE", f"{tor_signal['tor_change']:+,}", delta="nodes")
            st.metric("📈 TOTAL NODE CHANGE", f"{network_signal['total_change']:+,}", delta="nodes")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔄 Update node data to see comparison (current → previous)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # SIGNAL RESULTS
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Orbitron; color: #00ffff; text-align: center;">📊 SIGNAL RESULTS</h3>', unsafe_allow_html=True)
        
        if analyzer.current_data:
            # Current network stats
            col1b, col2b = st.columns(2)
            
            with col1b:
                st.metric("🔒 TOR NODES", f"{analyzer.current_data['tor_nodes']:,}")
                st.metric("🌐 TOTAL NODES", f"{analyzer.current_data['total_nodes']:,}")
            
            with col2b:
                st.metric("⚡ ACTIVE NODES", f"{analyzer.current_data['active_nodes']:,}")
                st.metric("📊 ACTIVE RATIO", f"{analyzer.current_data['active_ratio']:.3f}")
            
            # Display signals
            st.markdown('<div style="text-align: center; margin: 1rem 0;">', unsafe_allow_html=True)
            st.metric("🎯 TOR SIGNAL", tor_signal['signal'])
            st.metric("📡 MARKET BIAS", tor_signal['bias'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔄 Update node data to see signals")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SIGNAL DISPLAY BASED ON TOR CHANGE
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Display main signal with cyber styling
        if "STRONG SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "Tor nodes increased significantly - Privacy demand rising (Bearish)"
        elif "SELL" in tor_signal_data['signal']:
            signal_class = "signal-sell"
            emoji = "🔴"
            explanation = "Tor nodes increased - Potential selling pressure"
        elif "STRONG BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🟢"
            explanation = "Tor nodes decreased significantly - Privacy demand dropping (Bullish)"
        elif "BUY" in tor_signal_data['signal']:
            signal_class = "signal-buy"
            emoji = "🟢" 
            explanation = "Tor nodes decreased - Potential buying opportunity"
        else:
            signal_class = "signal-neutral"
            emoji = "🟡"
            explanation = "Minimal change in Tor nodes - Market neutral"
        
        st.markdown(f'<div class="{signal_class}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family: Orbitron; text-align: center; margin: 0.5rem 0;">🚀 {tor_signal_data["signal"]} SIGNAL {emoji}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #8892b0; font-family: Rajdhani; margin: 0.5rem 0;">{explanation}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-family: Orbitron; color: #ffffff; margin: 0.5rem 0;">Tor Node Change: {tor_signal_data["tor_change"]:+,} nodes</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # MULTI-COIN SIGNALS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎯 MULTI-COIN TOR SIGNALS</h2>', unsafe_allow_html=True)
    
    if analyzer.current_data and analyzer.previous_data:
        tor_signal_data = analyzer.calculate_tor_signal()
        
        # Apply Tor trend analysis to all coins
        coins_list = [
            'BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'BCHUSDT', 'SOLUSDT', 
            'ADAUSDT', 'AVAXUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'BNBUSDT'
        ]
        
        # Create columns for coin signals
        signal_cols = st.columns(4)
        
        for idx, symbol in enumerate(coins_list):
            if prices.get(symbol):
                with signal_cols[idx % 4]:
                    emoji = get_coin_emoji(symbol)
                    name = get_coin_display_name(symbol)
                    price = prices[symbol]
                    
                    # Apply the same Tor signal to all coins
                    if "SELL" in tor_signal_data['signal']:
                        signal_class = "signal-sell"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🔴"
                    elif "BUY" in tor_signal_data['signal']:
                        signal_class = "signal-buy"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🟢"
                    else:
                        signal_class = "signal-neutral"
                        signal_text = tor_signal_data['signal']
                        signal_emoji = "🟡"
                    
                    st.markdown(f'''
                    <div class="{signal_class}" style="padding: 1rem; margin: 0.5rem 0;">
                        <div style="text-align: center;">
                            <h4 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.1rem;">{emoji} {name}</h4>
<p style="font-family: Orbitron; font-size: 1.2rem; font-weight: 700; margin: 0.5rem 0;">${price:,.2f}</p>
                            <p style="font-family: Orbitron; font-size: 1rem; margin: 0.5rem 0;">{signal_emoji} {signal_text}</p>
                            <p style="color: #8892b0; font-family: Rajdhani; font-size: 0.8rem; margin: 0;">Δ Tor: {tor_signal_data['tor_change']:+,}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    else:
        st.info("🔄 Update node data to see multi-coin signals")
    
    # HOW IT WORKS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cyber-card">
    <h3 style="font-family: Orbitron; color: #00ffff; text-align: center;">⚡ HOW IT WORKS</h3>
    <div style="text-align: center;">
        <p style="color: #8892b0; font-family: Rajdhani; margin: 0.5rem 0;">
        <strong>Current → Previous Shift:</strong> Every time you click UPDATE, current data becomes previous data<br>
        <strong>Signal Logic:</strong> Compare new current Tor nodes with previous Tor nodes<br>
        <strong>Bullish:</strong> Tor nodes decreasing (less privacy demand)<br>
        <strong>Bearish:</strong> Tor nodes increasing (more privacy demand)<br>
        <strong>Refresh:</strong> Current → Previous → New Current → New Signal
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Abdullah's Futuristic Trademark Footer
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="trademark">
    <p>⚡ REAL-TIME TOR NODE SIGNAL ANALYZER ⚡</p>
    <p>© 2025 ABDULLAH'S CRYPTO TRACKER • CURRENT→PREVIOUS SHIFT SYSTEM</p>
    <p style="font-size: 0.7rem; color: #556699;">CLICK UPDATE TO SHIFT DATA AND GENERATE NEW SIGNALS</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
                       