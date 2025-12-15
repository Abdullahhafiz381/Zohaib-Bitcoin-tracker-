import streamlit as st
import pandas as pd
import numpy as np
import requests
from math import floor

# ------------------------------
# THEME & STYLE FROM REPO
# ------------------------------
st.set_page_config(page_title="Godzilla Trading Signals", page_icon="🦖", layout="wide")
st.markdown("""
<style>
body { background-color: #0a0a0a; color: white; }
.stButton>button { background-color: #e60000; color: white; font-weight: bold; }
.stTextInput>div>div>input { background-color: #1a1a1a; color: white; }
h1, h2, h3, h4 { color: #e60000; font-weight: bold; }
.dataframe, .stDataFrame { color: white !important; background-color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# LOGIN FROM REPO
# ------------------------------
def login():
    st.sidebar.title("Godzilla Trading Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "godzilla123":
            st.session_state.logged_in = True
        else:
            st.sidebar.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    login()
    st.stop()

# ------------------------------
# SETTINGS
# ------------------------------
pairs = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT", "XRPUSDT",
    "LTCUSDT", "DOTUSDT", "AVAXUSDT", "DOGEUSDT", "MATICUSDT",
    "SHIBUSDT", "LINKUSDT", "TRXUSDT", "UNIUSDT", "ATOMUSDT",
    "ALGOUSDT", "VETUSDT", "ICPUSDT", "FTMUSDT"
]

binance_book_api = "https://api.binance.com/api/v3/depth?limit=10&symbol={}"
binance_klines_api = "https://api.binance.com/api/v3/klines?symbol={}&interval=15m&limit=20"
bitnodes_api = "https://bitnodes.io/api/v1/snapshots/latest/"

# ------------------------------
# BITNODE ANALYZER FUNCTIONS (from repo)
# ------------------------------
def fetch_bitnodes_signal():
    try:
        resp = requests.get(bitnodes_api).json()
        total_nodes = resp['total_nodes']
        tor_nodes = [n for n in resp['nodes'] if 'tor' in n]
        tor_percentage = (len(tor_nodes)/total_nodes)*100 if total_nodes!=0 else 0
        previous_tor = tor_percentage - 1.5
        change = tor_percentage - previous_tor
        if change >= 1.0: return "🐲 GODZILLA DUMP", 100
        elif 0.5 <= change <1.0: return "🔥 STRONG SELL", 85
        elif 0.1 <= change <0.5: return "SELL", 70
        elif change <= -1.0: return "🐲 GODZILLA PUMP", 100
        elif -0.5 <= change < -0.1: return "🚀 STRONG BUY", 85
        elif -1.0 < change < -0.5: return "BUY", 70
        else: return "HOLD", 50
    except:
        return "HOLD", 50

# ------------------------------
# MATHEMATICAL FORMULAS
# ------------------------------
def fetch_orderbook(pair):
    try:
        resp = requests.get(binance_book_api.format(pair)).json()
        bids = [(float(price), float(qty)) for price, qty in resp['bids']]
        asks = [(float(price), float(qty)) for price, qty in resp['asks']]
        return bids, asks
    except:
        return [], []

def fetch_mid_price(bid, ask):
    return (bid + ask)/2 if bid !=0 and ask !=0 else 0

def calculate_volatility(prices):
    returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
    return np.std(returns) if len(returns) > 1 else 0.001

def order_book_signal(bids, asks):
    top_bid_price, top_bid_qty = bids[0] if bids else (0,0)
    top_ask_price, top_ask_qty = asks[0] if asks else (0,0)
    mid = fetch_mid_price(top_bid_price, top_ask_price)
    V_bid = sum([q for p,q in bids])
    V_ask = sum([q for p,q in asks])
    I_t = (V_bid - V_ask)/(V_bid + V_ask) if (V_bid + V_ask)!=0 else 0
    S_t = top_ask_price - top_bid_price
    phi_t = S_t / mid if mid !=0 else 0.001
    prices = [p for p,_ in bids] + [p for p,_ in asks]
    sigma = calculate_volatility(prices)
    Signal_t = np.sign(I_t) * (abs(I_t) / (phi_t * sigma)) if sigma !=0 else 0

    if abs(Signal_t) <1.0:
        Confidence = 70 + floor((abs(Signal_t)-0.5)*30)
    else:
        Confidence = 85 + min(14, floor((abs(Signal_t)-1.0)*10))
    
    Direction = "BUY" if I_t > phi_t else "SELL" if I_t < -phi_t else "HOLD"
    Strength = "STRONG" if abs(I_t)>0.3 else "MODERATE" if abs(I_t)>0.1 else "WEAK"
    
    return round(Signal_t,2), Confidence, Direction, Strength, mid

# ------------------------------
# HYBRID SIGNAL + LEVERAGE
# ------------------------------
def hybrid_signal(math_dir, math_conf, bitnode_dir, bitnode_conf):
    if (math_dir=="BUY" and bitnode_dir in ["🚀 STRONG BUY","BUY","🐲 GODZILLA PUMP"]):
        Combined = "CONFIRMED BUY"
    elif (math_dir=="SELL" and bitnode_dir in ["🔥 STRONG SELL","SELL","🐲 GODZILLA DUMP"]):
        Combined = "CONFIRMED SELL"
    else:
        Combined = "NO AGREEMENT"
    Combined_Confidence = math_conf*0.7 + bitnode_conf*0.3
    return Combined, round(Combined_Confidence,2)

def leverage_classification(combined_confidence):
    return "MAX LEVERAGE" if combined_confidence >= 90 else "LOW LEVERAGE"

# ------------------------------
# MAIN APP
# ------------------------------
st.title("🦖 Godzilla Trading Signal Generator")
st.subheader("Manual Update Mode")

if st.button("Update Signals"):
    st.info("Fetching real-time data...")
    all_data = []
    bitnode_dir, bitnode_strength = fetch_bitnodes_signal()
    
    for pair in pairs:
        bids, asks = fetch_orderbook(pair)
        Signal_t, Conf, Dir, Strength, mid = order_book_signal(bids, asks)
        Hybrid, HybridConf = hybrid_signal(Dir, Conf, bitnode_dir, bitnode_strength)
        Leverage = leverage_classification(HybridConf)
        all_data.append([pair, bids[0][0] if bids else 0, asks[0][0] if asks else 0, mid,
                         Signal_t, Conf, Dir, Strength, Hybrid, HybridConf, Leverage])
    
    df = pd.DataFrame(all_data, columns=["Pair","Bid","Ask","Mid","Signal_Strength","Confidence",
                                         "Direction","Strength","Hybrid_Signal","Hybrid_Confidence","Leverage"])
    
    top_signals = df.sort_values(by="Signal_Strength", ascending=False).head(2)
    
    st.subheader("📊 All 20 Pairs Signals")
    st.dataframe(df)
    
    st.subheader("🔥 Top 2 High Strength Signals")
    st.dataframe(top_signals)
    
    st.subheader("🧩 Bitnode Signal")
    st.markdown(f"**Signal:** {bitnode_dir} | **Strength:** {bitnode_strength}")
    
    st.success("Signals updated successfully!")