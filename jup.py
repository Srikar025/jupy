import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random
import requests

# Configure page
st.set_page_config(
    page_title="🎮 Jupiter Gaming Demo",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for gaming theme
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .game-item {
        background: rgba(255,255,255,0.1);
        border: 1px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    .success-alert {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_wallet' not in st.session_state:
    st.session_state.user_wallet = {
        'SOL': 10.0,
        'USDC': 500.0,
        'GAME_TOKENS': 1000.0
    }

if 'game_items' not in st.session_state:
    st.session_state.game_items = [
        {'name': '⚔️ Legendary Sword', 'rarity': 'Legendary', 'price_sol': 2.5, 'price_usdc': 125.0, 'owned': 0},
        {'name': '🛡️ Magic Shield', 'rarity': 'Epic', 'price_sol': 1.2, 'price_usdc': 60.0, 'owned': 0},
        {'name': '🧪 Health Potion', 'rarity': 'Common', 'price_sol': 0.1, 'price_usdc': 5.0, 'owned': 3},
        {'name': '🐲 Dragon Armor', 'rarity': 'Mythic', 'price_sol': 5.0, 'price_usdc': 250.0, 'owned': 0},
        {'name': '👢 Speed Boots', 'rarity': 'Rare', 'price_sol': 0.8, 'price_usdc': 40.0, 'owned': 1}
    ]

if 'achievements' not in st.session_state:
    st.session_state.achievements = [
        {'name': '🎯 First Kill', 'reward': 10, 'completed': True, 'claimed': False},
        {'name': '📈 Level 10 Reached', 'reward': 50, 'completed': True, 'claimed': False},
        {'name': '👑 Boss Defeated', 'reward': 100, 'completed': False, 'claimed': False},
        {'name': '🏆 Arena Champion', 'reward': 200, 'completed': False, 'claimed': False}
    ]

if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

# Simulate Jupiter API (for demo purposes)
def get_jupiter_quote(input_token, output_token, amount):
    """Simulate Jupiter price quote"""
    rates = {
        ('SOL', 'USDC'): 50.0 + random.uniform(-2, 2),
        ('USDC', 'SOL'): 0.02 + random.uniform(-0.001, 0.001),
        ('GAME_TOKENS', 'SOL'): 0.005 + random.uniform(-0.0005, 0.0005),
        ('SOL', 'GAME_TOKENS'): 200 + random.uniform(-10, 10)
    }
    
    rate = rates.get((input_token, output_token), 1.0)
    output_amount = amount * rate
    slippage = random.uniform(0.1, 0.5)
    
    return {
        'inputAmount': amount,
        'outputAmount': output_amount,
        'priceImpact': slippage,
        'route': f"{input_token} → {output_token}",
        'estimatedGas': 0.0001
    }

def execute_jupiter_swap(input_token, output_token, amount):
    """Simulate Jupiter swap execution"""
    if st.session_state.user_wallet[input_token] < amount:
        return False, "Insufficient balance"
    
    quote = get_jupiter_quote(input_token, output_token, amount)
    
    # Update balances
    st.session_state.user_wallet[input_token] -= amount
    st.session_state.user_wallet[output_token] += quote['outputAmount']
    
    # Add to trade history
    st.session_state.trade_history.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': 'Swap',
        'details': f"{amount:.4f} {input_token} → {quote['outputAmount']:.4f} {output_token}",
        'status': '✅ Success'
    })
    
    return True, f"Swapped {amount:.4f} {input_token} for {quote['outputAmount']:.4f} {output_token}"

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;'>
    <h1 style='color: white; font-size: 3rem; margin: 0;'>🎮 Jupiter Gaming Hub</h1>
    <p style='color: white; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>Trade Gaming Assets with Jupiter's Swap Aggregation</p>
</div>
""", unsafe_allow_html=True)

# Wallet Display
st.sidebar.markdown("## 💰 Your Gaming Wallet")
for token, balance in st.session_state.user_wallet.items():
    if token == 'SOL':
        st.sidebar.metric(f"{token}", f"{balance:.4f}", f"~${balance*50:.2f}")
    elif token == 'USDC':
        st.sidebar.metric(f"{token}", f"{balance:.2f}", f"${balance:.2f}")
    else:
        st.sidebar.metric(f"{token}", f"{int(balance)}", f"~{balance*0.005:.2f} SOL")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 **Item Trading**", 
    "🔄 **Jupiter Swaps**", 
    "🏆 **Achievements**", 
    "📊 **Portfolio**"
])

with tab1:
    st.header("🛒 Gaming Item Marketplace")
    st.markdown("*Trade in-game items powered by Jupiter Protocol*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Available Items")
        
        for i, item in enumerate(st.session_state.game_items):
            with st.container():
                item_col1, item_col2, item_col3, item_col4 = st.columns([2, 1, 1, 1])
                
                with item_col1:
                    st.markdown(f"**{item['name']}**")
                    rarity_colors = {
                        'Common': '🟢', 'Rare': '🔵', 'Epic': '🟣', 
                        'Legendary': '🟠', 'Mythic': '🔴'
                    }
                    st.markdown(f"{rarity_colors[item['rarity']]} {item['rarity']}")
                
                with item_col2:
                    st.markdown(f"**{item['price_sol']:.2f} SOL**")
                    st.markdown(f"${item['price_usdc']:.0f} USDC")
                
                with item_col3:
                    st.markdown(f"**Owned: {item['owned']}**")
                
                with item_col4:
                    if st.button(f"Buy with SOL", key=f"buy_sol_{i}"):
                        if st.session_state.user_wallet['SOL'] >= item['price_sol']:
                            st.session_state.user_wallet['SOL'] -= item['price_sol']
                            st.session_state.game_items[i]['owned'] += 1
                            st.session_state.trade_history.append({
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'type': 'Purchase',
                                'details': f"Bought {item['name']} for {item['price_sol']} SOL",
                                'status': '✅ Success'
                            })
                            st.success(f"Purchased {item['name']}! 🎉")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Insufficient SOL balance!")
                    
                    if item['owned'] > 0:
                        if st.button(f"Sell", key=f"sell_{i}"):
                            st.session_state.user_wallet['SOL'] += item['price_sol'] * 0.95  # 5% market fee
                            st.session_state.game_items[i]['owned'] -= 1
                            st.session_state.trade_history.append({
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'type': 'Sale',
                                'details': f"Sold {item['name']} for {item['price_sol']*0.95:.4f} SOL",
                                'status': '✅ Success'
                            })
                            st.success(f"Sold {item['name']}! 💰")
                            time.sleep(1)
                            st.rerun()
                
                st.markdown("---")
    
    with col2:
        st.subheader("🔥 Market Stats")
        
        # Mock market data
        market_data = {
            'Total Volume (24h)': '$12,450',
            'Active Traders': '1,247',
            'Items Listed': '8,923',
            'Avg Price': '1.2 SOL'
        }
        
        for stat, value in market_data.items():
            st.metric(stat, value)
        
        st.subheader("📈 Price Trends")
        
        # Generate mock price chart
        dates = pd.date_range(start='2024-01-20', end='2024-01-30', freq='D')
        prices = np.cumsum(np.random.randn(len(dates)) * 0.1) + 50
        
        fig = px.line(x=dates, y=prices, title="SOL/USD Price")
        fig.update_layout(height=200, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🔄 Jupiter Swap Aggregation")
    st.markdown("*Powered by Jupiter Protocol - Best rates across all Solana DEXs*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💱 Swap Tokens")
        
        # Swap interface
        from_token = st.selectbox("From Token", list(st.session_state.user_wallet.keys()))
        from_amount = st.number_input(
            f"Amount ({from_token})", 
            min_value=0.0001, 
            max_value=float(st.session_state.user_wallet[from_token]), 
            value=1.0, 
            step=0.1,
            format="%.4f"
        )
        
        to_token = st.selectbox("To Token", [t for t in st.session_state.user_wallet.keys() if t != from_token])
        
        if st.button("🔍 Get Jupiter Quote"):
            with st.spinner("Fetching best routes from Jupiter..."):
                time.sleep(1)  # Simulate API call
                quote = get_jupiter_quote(from_token, to_token, from_amount)
                
                st.success("Quote received! 📋")
                st.json({
                    "Route": quote['route'],
                    "Input": f"{quote['inputAmount']:.4f} {from_token}",
                    "Output": f"{quote['outputAmount']:.4f} {to_token}",
                    "Price Impact": f"{quote['priceImpact']:.2f}%",
                    "Estimated Gas": f"{quote['estimatedGas']:.6f} SOL"
                })
                
                if st.button("⚡ Execute Swap"):
                    with st.spinner("Executing swap via Jupiter..."):
                        time.sleep(2)  # Simulate transaction
                        success, message = execute_jupiter_swap(from_token, to_token, from_amount)
                        
                        if success:
                            st.success(f"🎉 {message}")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
    
    with col2:
        st.subheader("📊 Jupiter Stats")
        
        jupiter_stats = {
            'Total Volume (24h)': '$45.2M',
            'Best Price Routes': '847',
            'Average Slippage': '0.12%',
            'Successful Swaps': '99.8%'
        }
        
        for stat, value in jupiter_stats.items():
            st.metric(stat, value)
        
        st.subheader("🔄 Recent Swaps")
        
        if st.session_state.trade_history:
            recent_trades = pd.DataFrame(st.session_state.trade_history[-5:])
            st.dataframe(recent_trades, use_container_width=True)
        else:
            st.info("No recent swaps. Make your first trade above! 👆")

with tab3:
    st.header("🏆 Achievement Rewards")
    st.markdown("*Convert your gaming achievements into tradeable tokens*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Your Achievements")
        
        for i, achievement in enumerate(st.session_state.achievements):
            with st.container():
                ach_col1, ach_col2, ach_col3 = st.columns([2, 1, 1])
                
                with ach_col1:
                    st.markdown(f"**{achievement['name']}**")
                    if achievement['completed']:
                        st.markdown("✅ **Completed**")
                    else:
                        st.markdown("⏳ In Progress")
                
                with ach_col2:
                    st.markdown(f"**Reward: {achievement['reward']} tokens**")
                
                with ach_col3:
                    if achievement['completed'] and not achievement['claimed']:
                        if st.button(f"Claim Reward", key=f"claim_{i}"):
                            st.session_state.user_wallet['GAME_TOKENS'] += achievement['reward']
                            st.session_state.achievements[i]['claimed'] = True
                            st.session_state.trade_history.append({
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'type': 'Achievement',
                                'details': f"Claimed {achievement['reward']} tokens from {achievement['name']}",
                                'status': '🏆 Claimed'
                            })
                            st.success(f"Claimed {achievement['reward']} tokens! 🎉")
                            time.sleep(1)
                            st.rerun()
                    elif achievement['claimed']:
                        st.markdown("✅ **Claimed**")
                    elif not achievement['completed']:
                        if st.button(f"Complete", key=f"complete_{i}"):
                            st.session_state.achievements[i]['completed'] = True
                            st.success(f"Achievement completed! 🎯")
                            time.sleep(1)
                            st.rerun()
                
                st.markdown("---")
    
    with col2:
        st.subheader("📈 Achievement Progress")
        
        completed = sum(1 for a in st.session_state.achievements if a['completed'])
        total = len(st.session_state.achievements)
        progress = completed / total
        
        st.metric("Completion Rate", f"{progress*100:.0f}%", f"{completed}/{total}")
        
        total_rewards = sum(a['reward'] for a in st.session_state.achievements if a['claimed'])
        st.metric("Total Rewards Claimed", f"{total_rewards} tokens")
        
        # Auto-convert settings
        st.subheader("⚙️ Auto-Convert")
        auto_convert = st.checkbox("Auto-convert to SOL", value=True)
        if auto_convert:
            threshold = st.slider("Convert when balance >", 50, 500, 100)
            st.info(f"Will auto-convert {threshold}+ tokens to SOL")

with tab4:
    st.header("📊 Portfolio Dashboard")
    st.markdown("*Your complete gaming asset overview*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Portfolio Value")
        
        # Calculate total portfolio value in USD
        sol_price = 50.0  # Mock SOL price
        total_value = (
            st.session_state.user_wallet['SOL'] * sol_price +
            st.session_state.user_wallet['USDC'] +
            st.session_state.user_wallet['GAME_TOKENS'] * 0.25  # Mock token value
        )
        
        st.metric("Total Portfolio Value", f"${total_value:.2f}", "↗️ +12.5%")
        
        # Portfolio breakdown
        portfolio_data = {
            'Asset': ['SOL', 'USDC', 'GAME_TOKENS'],
            'Balance': [
                st.session_state.user_wallet['SOL'],
                st.session_state.user_wallet['USDC'],
                st.session_state.user_wallet['GAME_TOKENS']
            ],
            'Value (USD)': [
                st.session_state.user_wallet['SOL'] * sol_price,
                st.session_state.user_wallet['USDC'],
                st.session_state.user_wallet['GAME_TOKENS'] * 0.25
            ]
        }
        
        df_portfolio = pd.DataFrame(portfolio_data)
        st.dataframe(df_portfolio, use_container_width=True)
        
        # Portfolio pie chart
        fig_pie = px.pie(
            values=df_portfolio['Value (USD)'], 
            names=df_portfolio['Asset'],
            title="Portfolio Allocation"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Performance")
        
        # Mock performance data
        dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
        portfolio_values = 1000 + np.cumsum(np.random.randn(len(dates)) * 20)
        
        fig_performance = px.line(
            x=dates, 
            y=portfolio_values,
            title="Portfolio Value Over Time",
            labels={'y': 'Value (USD)', 'x': 'Date'}
        )
        st.plotly_chart(fig_performance, use_container_width=True)
        
        st.subheader("🎮 Gaming Stats")
        
        gaming_stats = {
            'Items Owned': sum(item['owned'] for item in st.session_state.game_items),
            'Achievements': f"{sum(1 for a in st.session_state.achievements if a['completed'])}/4",
            'Total Trades': len(st.session_state.trade_history),
            'Favorite Game': 'Solana Quest'
        }
        
        for stat, value in gaming_stats.items():
            st.metric(stat, value)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 Powered by Jupiter")
    st.markdown("Best rates across all Solana DEXs")

with col2:
    st.markdown("### ⚡ Built on Solana")
    st.markdown("Fast, cheap, and scalable")

with col3:
    st.markdown("### 🎮 For Gamers")
    st.markdown("Seamless Web3 gaming experience")

# Live demo indicator
st.markdown("""
<div style='position: fixed; top: 10px; right: 10px; background: #28a745; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; z-index: 999;'>
    🟢 LIVE DEMO
</div>
""", unsafe_allow_html=True)
