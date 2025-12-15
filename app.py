# app.py - GODZILLERS DUAL SYSTEM BOT
import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time
import ccxt

# ==================== STREAMLIT SETUP ====================
st.set_page_config(
    page_title="🔥 GODZILLERS DUAL SYSTEM",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== PREMIUM CSS ====================
st.markdown("""
<style>
    /* BASE */
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a0000 50%, #00001a 100%);
        font-family: 'Rajdhani', sans-serif;
        color: white;
    }
    
    /* HEADERS */
    .header-main {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.7);
    }
    
    .header-sub {
        color: #ff6666;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    /* BITNODE SIGNAL CARD */
    .bitnode-card {
        background: linear-gradient(135deg, rgba(0, 100, 200, 0.1), rgba(0, 50, 150, 0.2));
        border: 3px solid #0088ff;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 0 40px rgba(0, 136, 255, 0.4);
        animation: pulse-blue 2s infinite;
    }
    
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 30px rgba(0, 136, 255, 0.4); }
        50% { box-shadow: 0 0 50px rgba(0, 136, 255, 0.6); }
        100% { box-shadow: 0 0 30px rgba(0, 136, 255, 0.4); }
    }
    
    /* MATHEMATICAL SIGNAL CARD */
    .math-card {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(150, 0, 150, 0.2));
        border: 3px solid #ff00ff;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.4);
    }
    
    .math-buy {
        border-color: #00ff00;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.4);
    }
    
    .math-sell {
        border-color: #ff0000;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
    }
    
    /* CONFIRMED SIGNAL CARD */
    .confirmed-card {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.15), rgba(0, 150, 0, 0.25));
        border: 3px solid #00ff00;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 0 50px rgba(0, 255, 0, 0.5);
        animation: pulse-green 2s infinite;
    }
    
    @keyframes pulse-green {
        0% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.5); }
        50% { box-shadow: 0 0 60px rgba(0, 255, 0, 0.7); }
        100% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.5); }
    }
    
    /* BADGES */
    .badge {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .badge-bitnode {
        background: linear-gradient(90deg, #0088ff, #0066cc);
        color: white;
        box-shadow: 0 0 10px rgba(0, 136, 255, 0.6);
    }
    
    .badge-math {
        background: linear-gradient(90deg, #ff00ff, #cc00cc);
        color: white;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.6);
    }
    
    .badge-confidence-95 {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: black;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.6);
    }
    
    .badge-confidence-90 {
        background: linear-gradient(90deg, #99ff00, #66cc00);
        color: black;
        box-shadow: 0 0 10px rgba(153, 255, 0, 0.6);
    }
    
    .badge-confidence-85 {
        background: linear-gradient(90deg, #ffff00, #cccc00);
        color: black;
        box-shadow: 0 0 10px rgba(255, 255, 0, 0.6);
    }
    
    .badge-confidence-80 {
        background: linear-gradient(90deg, #ff9900, #cc6600);
        color: black;
        box-shadow: 0 0 10px rgba(255, 153, 0, 0.6);
    }
    
    .badge-confidence-75 {
        background: linear-gradient(90deg, #ff5500, #cc4400);
        color: white;
        box-shadow: 0 0 10px rgba(255, 85, 0, 0.6);
    }
    
    .badge-confidence-70 {
        background: linear-gradient(90deg, #ff0000, #cc0000);
        color: white;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.6);
    }
    
    .badge-leverage-max {
        background: linear-gradient(90deg, #ff00ff, #cc00cc);
        color: white;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.6);
    }
    
    .badge-leverage-low {
        background: linear-gradient(90deg, #ff9900, #cc6600);
        color: black;
        box-shadow: 0 0 10px rgba(255, 153, 0, 0.6);
    }
    
    /* LOGIN */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    
    .login-card {
        background: rgba(20, 0, 0, 0.9);
        border: 2px solid rgba(255, 0, 0, 0.6);
        border-radius: 20px;
        padding: 3rem;
        width: 100%;
        max-width: 450px;
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.5);
        text-align: center;
    }
    
    .login-header {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .logout-btn {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%);
        color: black;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 10px;
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    /* SECTIONS */
    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    .section-bitnode {
        color: #0088ff;
    }
    
    .section-math {
        color: #ff00ff;
    }
    
    .section-confirmed {
        color: #00ff00;
    }
    
    /* DIVIDER */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff0000, transparent);
        margin: 2rem 0;
    }
    
    /* HIDE STREAMLIT */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== BITNODE ANALYZER ====================
class BitnodeAnalyzer:
    """Analyzes Bitcoin network Tor nodes for market sentiment"""
    
    def __init__(self, data_file="bitnode_data.json"):
        self.data_file = data_file
        self.api_url = "https://bitnodes.io/api/v1/snapshots/latest/"
        self.load_data()
    
    def load_data(self):
        """Load current and previous node data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.current = data.get('current')
                    self.previous = data.get('previous')
                    self.last_update = data.get('last_update')
            else:
                self.current = None
                self.previous = None
                self.last_update = None
        except:
            self.current = None
            self.previous = None
            self.last_update = None
    
    def save_data(self):
        """Save node data"""
        try:
            data = {
                'current': self.current,
                'previous': self.previous,
                'last_update': self.last_update,
                'saved': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def fetch_node_data(self):
        """Fetch latest node data from Bitnodes API"""
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_nodes = data.get('total_nodes', 0)
                tor_nodes = 0
                
                # Count Tor nodes
                for node_address, node_info in data.get('nodes', {}).items():
                    if '.onion' in str(node_address).lower():
                        tor_nodes += 1
                    elif node_info and isinstance(node_info, list):
                        for info in node_info:
                            if '.onion' in str(info).lower():
                                tor_nodes += 1
                                break
                
                tor_percentage = (tor_nodes / total_nodes * 100) if total_nodes > 0 else 0
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_nodes': total_nodes,
                    'tor_nodes': tor_nodes,
                    'tor_percentage': tor_percentage
                }
            return None
        except:
            return None
    
    def update_data(self):
        """Update node data"""
        new_data = self.fetch_node_data()
        if not new_data:
            return False
        
        self.last_update = datetime.now().isoformat()
        self.previous = self.current
        self.current = new_data
        
        self.save_data()
        return True
    
    def generate_signal(self):
        """Generate Bitnode market signal based on Tor percentage changes"""
        if not self.current or not self.previous:
            return {
                'signal': "🔄 NEED DATA",
                'direction': "NEUTRAL",
                'strength': "UPDATE REQUIRED",
                'tor_change': 0,
                'current_tor': 0
            }
        
        current_tor = self.current['tor_percentage']
        previous_tor = self.previous['tor_percentage']
        tor_change = current_tor - previous_tor
        
        # SIGNAL LOGIC
        if tor_change >= 1.0:
            return {
                'signal': "🐲 GODZILLA DUMP 🐲",
                'direction': "STRONG SELL",
                'strength': "EXTREME BEARISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        elif tor_change >= 0.5:
            return {
                'signal': "🔥 STRONG SELL 🔥",
                'direction': "SELL",
                'strength': "VERY BEARISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        elif tor_change >= 0.1:
            return {
                'signal': "SELL",
                'direction': "SELL",
                'strength': "BEARISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        elif tor_change <= -1.0:
            return {
                'signal': "🐲 GODZILLA PUMP 🐲",
                'direction': "STRONG BUY",
                'strength': "EXTREME BULLISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        elif tor_change <= -0.5:
            return {
                'signal': "🚀 STRONG BUY 🚀",
                'direction': "BUY",
                'strength': "VERY BULLISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        elif tor_change <= -0.1:
            return {
                'signal': "BUY",
                'direction': "BUY",
                'strength': "BULLISH",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }
        else:
            return {
                'signal': "HOLD",
                'direction': "NEUTRAL",
                'strength': "NEUTRAL",
                'tor_change': tor_change,
                'current_tor': current_tor,
                'total_nodes': self.current['total_nodes']
            }

# ==================== MATHEMATICAL EQUATIONS ====================
class MathematicalEquations:
    """8 Mathematical Equations with 70% confidence threshold"""
    
    def __init__(self):
        # CONFIDENCE THRESHOLD = 70% (Changed from 85%)
        self.CONFIDENCE_THRESHOLD = 70
        self.ORDERBOOK_DEPTH = 10
        self.VOLATILITY_WINDOW = 20
        self.BASE_LEVERAGE = 5
        self.price_history = {}
        
        # Initialize exchange
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })
            self.exchange.load_markets()
        except:
            self.exchange = None
    
    def fetch_orderbook_data(self, symbol):
        """Fetch order book data for equations"""
        if not self.exchange:
            return None
        
        try:
            # Add USDT if not present
            if not symbol.endswith('/USDT'):
                symbol = symbol + '/USDT'
            
            orderbook = self.exchange.fetch_order_book(symbol, self.ORDERBOOK_DEPTH)
            ticker = self.exchange.fetch_ticker(symbol)
            
            # Extract data
            bid = ticker['bid'] if ticker['bid'] else orderbook['bids'][0][0]
            ask = ticker['ask'] if ticker['ask'] else orderbook['asks'][0][0]
            mid_price = (bid + ask) / 2
            
            # Order book volumes
            bids = orderbook['bids'][:self.ORDERBOOK_DEPTH]
            asks = orderbook['asks'][:self.ORDERBOOK_DEPTH]
            bid_volume = sum(b[1] for b in bids)
            ask_volume = sum(a[1] for a in asks)
            
            # Store price history
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            
            self.price_history[symbol].append(mid_price)
            if len(self.price_history[symbol]) > self.VOLATILITY_WINDOW:
                self.price_history[symbol] = self.price_history[symbol][-self.VOLATILITY_WINDOW:]
            
            return {
                'bid': bid,
                'ask': ask,
                'mid_price': mid_price,
                'bid_volume': bid_volume,
                'ask_volume': ask_volume,
                'spread': ask - bid,
                'price_history': self.price_history[symbol]
            }
        except:
            return None
    
    def calculate_volatility(self, price_history):
        """Equation 6: σ̂_t = StdDev(returns)"""
        if len(price_history) < 2:
            return 0.01
        
        returns = np.diff(np.log(price_history))
        return float(np.std(returns, ddof=1))
    
    def generate_signal(self, symbol):
        """Generate mathematical signal using 8 equations"""
        data = self.fetch_orderbook_data(symbol)
        
        if not data:
            return None
        
        # Equation 1: Mid Price
        P_t = data['mid_price']
        
        # Equation 2: Order Book Volumes
        V_bid = data['bid_volume']
        V_ask = data['ask_volume']
        
        # Equation 3: Order Book Imbalance
        total_volume = V_bid + V_ask
        I_t = (V_bid - V_ask) / total_volume if total_volume > 0 else 0
        
        # Equation 4: Spread
        S_t = data['spread']
        
        # Equation 5: Relative Spread
        phi_t = S_t / P_t if P_t > 0 else 0.0001
        
        # Equation 6: Volatility
        sigma_t = self.calculate_volatility(data['price_history'])
        
        # Equation 7: Signal Strength
        if phi_t > 0 and sigma_t > 0:
            signal_strength = np.sign(I_t) * (abs(I_t) / (phi_t * sigma_t))
        else:
            signal_strength = 0
        
        # Determine direction
        if I_t > phi_t:
            direction = "BUY"
        elif I_t < -phi_t:
            direction = "SELL"
        else:
            return None
        
        # Calculate confidence (70-100%)
        abs_signal = abs(signal_strength)
        if abs_signal < 1.0:
            confidence = 70 + int((abs_signal - 0.5) * 30) if abs_signal > 0.5 else 0
        else:
            confidence = 85 + min(15, int((abs_signal - 1.0) * 10))
        
        # Apply 70% threshold
        if confidence < self.CONFIDENCE_THRESHOLD:
            return None
        
        # Equation 8: Max Leverage
        if sigma_t > 0:
            max_leverage = 1 + (self.BASE_LEVERAGE / sigma_t)
            max_leverage = min(10, max_leverage)
        else:
            max_leverage = 3
        
        # Determine leverage
        leverage = "MAX LEVERAGE" if confidence >= 90 else "LOW LEVERAGE"
        
        return {
            'symbol': symbol,
            'direction': direction,
            'confidence': confidence,
            'leverage': leverage,
            'max_leverage': round(max_leverage, 1),
            'price': round(P_t, 2)
        }

# ==================== DUAL SYSTEM ====================
class DualSystem:
    """Combines Bitnode and Mathematical systems"""
    
    def __init__(self):
        self.bitnode = BitnodeAnalyzer()
        self.mathematical = MathematicalEquations()
        self.coins = [
            "BTC", "ETH", "SUI", "LINK", "SOL",
            "XRP", "TAO", "ENA", "ADA", "DOGE", "BRETT"
        ]
    
    def update_all(self):
        """Update both systems"""
        self.bitnode.update_data()
    
    def get_bitnode_signal(self):
        """Get Bitnode market signal"""
        return self.bitnode.generate_signal()
    
    def get_mathematical_signals(self):
        """Get mathematical signals for all coins"""
        signals = []
        
        for coin in self.coins:
            signal = self.mathematical.generate_signal(coin)
            if signal:
                signals.append(signal)
            time.sleep(0.05)  # Rate limiting
        
        # Sort by confidence
        signals.sort(key=lambda x: x['confidence'], reverse=True)
        return signals
    
    def get_confirmed_signals(self, bitnode_signal, math_signals):
        """Get signals where both systems agree"""
        confirmed = []
        
        # Extract Bitnode direction
        bitnode_direction = bitnode_signal['direction']
        
        for math_signal in math_signals:
            math_direction = math_signal['direction']
            
            # Check if directions match (ignoring strength modifiers)
            if ("BUY" in bitnode_direction and math_direction == "BUY") or \
               ("SELL" in bitnode_direction and math_direction == "SELL"):
                
                confirmed.append({
                    **math_signal,
                    'bitnode_signal': bitnode_signal['signal'],
                    'bitnode_direction': bitnode_direction
                })
        
        return confirmed

# ==================== COIN DATA ====================
COIN_DATA = {
    'BTC': {'name': 'Bitcoin', 'emoji': '🐲', 'color': '#FF9900'},
    'ETH': {'name': 'Ethereum', 'emoji': '🔥', 'color': '#3C3C3D'},
    'SUI': {'name': 'Sui', 'emoji': '💧', 'color': '#6FCF97'},
    'LINK': {'name': 'Chainlink', 'emoji': '🔗', 'color': '#2A5ADA'},
    'SOL': {'name': 'Solana', 'emoji': '☀️', 'color': '#00FFA3'},
    'XRP': {'name': 'Ripple', 'emoji': '✖️', 'color': '#23292F'},
    'TAO': {'name': 'Bittensor', 'emoji': '🧠', 'color': '#FF6B00'},
    'ENA': {'name': 'Ethena', 'emoji': '⚡', 'color': '#3A86FF'},
    'ADA': {'name': 'Cardano', 'emoji': '🔷', 'color': '#0033AD'},
    'DOGE': {'name': 'Dogecoin', 'emoji': '🐕', 'color': '#C2A633'},
    'BRETT': {'name': 'Brett', 'emoji': '🤖', 'color': '#FF6B6B'}
}

def get_confidence_badge(confidence):
    """Get confidence badge class"""
    if confidence >= 95:
        return "badge-confidence-95"
    elif confidence >= 90:
        return "badge-confidence-90"
    elif confidence >= 85:
        return "badge-confidence-85"
    elif confidence >= 80:
        return "badge-confidence-80"
    elif confidence >= 75:
        return "badge-confidence-75"
    else:
        return "badge-confidence-70"

# ==================== DISPLAY FUNCTIONS ====================
def display_bitnode_signal(signal):
    """Display Bitnode signal"""
    st.markdown(f'''
    <div class="bitnode-card">
        <div style="text-align: center;">
            <h2 style="font-family: Orbitron; color: #0088ff; margin-bottom: 0.5rem;">🌐 BITNODE MARKET SIGNAL</h2>
            <p style="font-family: Orbitron; font-size: 2rem; font-weight: 900; color: #ffffff; margin: 0.5rem 0;">
                {signal['signal']}
            </p>
            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.2rem; margin: 0.5rem 0;">
                {signal['strength']}
            </p>
            
            <div style="margin: 1rem 0;">
                <span class="badge badge-bitnode">Tor Change: {signal['tor_change']:.2f}%</span>
                <span class="badge badge-bitnode">Current Tor: {signal['current_tor']:.1f}%</span>
                <span class="badge badge-bitnode">Nodes: {signal['total_nodes']:,}</span>
            </div>
            
            <p style="color: #aaa; font-size: 0.9rem; margin-top: 1rem;">
                Bitcoin Network Analysis • Real-time Tor Node Monitoring
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def display_math_signal(signal):
    """Display mathematical signal"""
    coin = signal['symbol']
    coin_info = COIN_DATA.get(coin, {'name': coin, 'emoji': '💀', 'color': '#666'})
    
    card_class = "math-card math-buy" if signal['direction'] == "BUY" else "math-card math-sell"
    direction_color = "#00ff00" if signal['direction'] == "BUY" else "#ff0000"
    confidence_class = get_confidence_badge(signal['confidence'])
    
    st.markdown(f'''
    <div class="{card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 1.8rem;">{coin_info['emoji']}</span>
                <div>
                    <p style="font-family: Orbitron; font-size: 1.2rem; color: {coin_info['color']}; margin: 0;">
                        {coin}
                    </p>
                    <p style="color: #aaa; font-size: 0.8rem; margin: 0;">{coin_info['name']}</p>
                </div>
            </div>
            <div style="font-family: Orbitron; font-size: 1.5rem; color: {direction_color}; font-weight: 700;">
                {signal['direction']}
            </div>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 0.8rem;">
            <div class="badge {confidence_class}">
                {signal['confidence']}% CONFIDENCE
            </div>
            <div class="badge badge-leverage-{'max' if 'MAX' in signal['leverage'] else 'low'}">
                {signal['leverage']}
            </div>
        </div>
        
        <div style="text-align: center;">
            <p style="color: #ffd700; font-family: Orbitron; font-size: 1.3rem; font-weight: 700; margin: 0;">
                ${signal['price']:,.2f}
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def display_confirmed_signal(signal):
    """Display confirmed signal (both systems agree)"""
    coin = signal['symbol']
    coin_info = COIN_DATA.get(coin, {'name': coin, 'emoji': '💀', 'color': '#666'})
    confidence_class = get_confidence_badge(signal['confidence'])
    
    st.markdown(f'''
    <div class="confirmed-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3 style="font-family: Orbitron; color: #00ff00; margin-bottom: 0.5rem;">
                ✅ BOTH SYSTEMS CONFIRM
            </h3>
            <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 2.5rem;">{coin_info['emoji']}</span>
                <div>
                    <p style="font-family: Orbitron; font-size: 1.5rem; color: {coin_info['color']}; margin: 0;">
                        {coin} - {coin_info['name']}
                    </p>
                    <p style="color: #ffd700; font-family: Orbitron; font-size: 1.8rem; margin: 0.3rem 0;">
                        {signal['direction']} {signal['direction']}
                    </p>
                </div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 0.8rem; margin-bottom: 1rem;">
            <div class="badge {confidence_class}">
                {signal['confidence']}% MATHEMATICAL
            </div>
            <div class="badge badge-bitnode">
                BITNODE: {signal['bitnode_signal']}
            </div>
        </div>
        
        <div style="text-align: center;">
            <p style="color: #ffffff; font-family: Orbitron; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">
                ${signal['price']:,.2f}
            </p>
            <p style="color: #ff9900; font-size: 1rem; margin: 0.3rem 0;">
                Max Leverage: {signal['max_leverage']}x
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ==================== AUTHENTICATION ====================
def check_login(username, password):
    """Check login credentials"""
    users = {
        "godziller": "dragonfire2025",
        "admin": "cryptoking",
        "trader": "bullmarket"
    }
    return username in users and users[username] == password

def login_page():
    """Display login page"""
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <h1 class="login-header">🐲 GODZILLERS</h1>
            <p style="color: #ff6666; font-family: Orbitron; margin-bottom: 2rem;">
                BITNODE + MATHEMATICAL DUAL SYSTEM
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login"):
            username = st.text_input("DRAGON NAME", placeholder="Enter username...")
            password = st.text_input("FIRE BREATH", type="password", placeholder="Enter password...")
            
            if st.form_submit_button("🔥 IGNITE SYSTEMS", use_container_width=True):
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ==================== MAIN APP ====================
def main_app():
    """Main application"""
    # Initialize session state
    if 'dual_system' not in st.session_state:
        st.session_state.dual_system = DualSystem()
    if 'bitnode_signal' not in st.session_state:
        st.session_state.bitnode_signal = None
    if 'math_signals' not in st.session_state:
        st.session_state.math_signals = []
    if 'confirmed_signals' not in st.session_state:
        st.session_state.confirmed_signals = []
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = None
    
    # Logout button
    if st.button("🚪 LOGOUT", key="logout", use_container_width=False):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Welcome
    st.markdown(f'''
    <div style="text-align: right; padding: 0.5rem 1rem;">
        <span style="color: #ff6666; font-family: Orbitron;">Welcome, {st.session_state.username}!</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="header-main">🔥 GODZILLERS DUAL SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-sub">BITNODE + MATHEMATICAL EQUATIONS | 70% CONFIDENCE THRESHOLD</p>', unsafe_allow_html=True)
    
    # Scan button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 SCAN ALL SYSTEMS", use_container_width=True, type="primary"):
            with st.spinner("Activating dual systems..."):
                # Update systems
                st.session_state.dual_system.update_all()
                
                # Get signals
                st.session_state.bitnode_signal = st.session_state.dual_system.get_bitnode_signal()
                st.session_state.math_signals = st.session_state.dual_system.get_mathematical_signals()
                st.session_state.confirmed_signals = st.session_state.dual_system.get_confirmed_signals(
                    st.session_state.bitnode_signal, 
                    st.session_state.math_signals
                )
                
                st.session_state.last_scan = datetime.now()
                
                # Show results
                total_signals = len(st.session_state.math_signals)
                total_confirmed = len(st.session_state.confirmed_signals)
                
                if total_signals > 0:
                    st.success(f"✅ Found {total_signals} mathematical signals ({total_confirmed} confirmed)")
                else:
                    st.warning("⚠️ No mathematical signals found (70% confidence required)")
    
    # Last scan info
    if st.session_state.last_scan:
        scan_time = st.session_state.last_scan.strftime("%H:%M:%S")
        st.markdown(f'''
        <div style="text-align: center; color: #ff6666; font-family: Orbitron; margin: 1rem 0;">
            Last scan: {scan_time} | 11 coins monitored | 70% confidence threshold
        </div>
        ''', unsafe_allow_html=True)
    
    # BITNODE SIGNAL SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title section-bitnode">🌐 BITNODE MARKET SIGNAL</h2>', unsafe_allow_html=True)
    
    if st.session_state.bitnode_signal:
        display_bitnode_signal(st.session_state.bitnode_signal)
    else:
        st.info("Click 'SCAN ALL SYSTEMS' to get Bitnode market signal")
    
    # CONFIRMED SIGNALS SECTION
    if st.session_state.confirmed_signals:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title section-confirmed">✅ CONFIRMED SIGNALS (BOTH SYSTEMS AGREE)</h2>', unsafe_allow_html=True)
        
        for signal in st.session_state.confirmed_signals:
            display_confirmed_signal(signal)
    
    # MATHEMATICAL SIGNALS SECTION
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title section-math">🧮 MATHEMATICAL SIGNALS (≥70% CONFIDENCE)</h2>', unsafe_allow_html=True)
    
    if st.session_state.math_signals:
        # Display in columns
        cols = st.columns(2)
        for idx, signal in enumerate(st.session_state.math_signals):
            with cols[idx % 2]:
                display_math_signal(signal)
    else:
        if st.session_state.last_scan:
            st.warning("No mathematical signals found (70% confidence threshold not met)")
        else:
            st.info("Click 'SCAN ALL SYSTEMS' to get mathematical signals")
    
    # COINS MONITORED
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">📊 COINS MONITORED</h2>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, coin in enumerate(st.session_state.dual_system.coins):
        with cols[idx % 4]:
            coin_info = COIN_DATA[coin]
            has_math = any(s['symbol'] == coin for s in st.session_state.math_signals)
            has_confirmed = any(s['symbol'] == coin for s in st.session_state.confirmed_signals)
            
            status_color = "#00ff00" if has_confirmed else "#ff9900" if has_math else "#666666"
            status_text = "✅ CONFIRMED" if has_confirmed else "📡 ACTIVE" if has_math else "⚙️ MONITORING"
            
            st.markdown(f'''
            <div style="background: rgba(30, 0, 60, 0.5); border: 2px solid {coin_info['color']}; 
                     border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">{coin_info['emoji']}</div>
                <div style="font-family: Orbitron; color: {coin_info['color']}; font-size: 1rem;">
                    {coin}
                </div>
                <div style="color: #aaa; font-size: 0.8rem; margin: 0.2rem 0;">
                    {coin_info['name']}
                </div>
                <div style="color: {status_color}; font-family: Orbitron; font-size: 0.7rem; margin-top: 0.3rem;">
                    {status_text}
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # FOOTER
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #ff6666; padding: 2rem 0;">
        <p style="font-family: Orbitron; font-size: 1rem;">🔥 GODZILLERS DUAL SYSTEM 🔥</p>
        <p style="color: #aaa; font-size: 0.8rem;">Bitnode Market Analysis + 8 Mathematical Equations</p>
        <p style="color: #666; font-size: 0.7rem;">70% Confidence Threshold • 11 Specific Coins • Real-time Signals</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    """Main function"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()