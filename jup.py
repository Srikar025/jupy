import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random

# Configure page
st.set_page_config(
    page_title="Jupiter Gaming Micro-Trading Platform",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_wallet' not in st.session_state:
    st.session_state.user_wallet = {
        'SOL': 100.0,
        'USDC': 500.0,
        'GAME_TOKENS': 1000.0
    }

if 'game_items' not in st.session_state:
    st.session_state.game_items = [
        {'name': 'Legendary Sword', 'rarity': 'Legendary', 'price': 50.0, 'token': 'SWORD'},
        {'name': 'Magic Shield', 'rarity': 'Epic', 'price': 30.0, 'token': 'SHIELD'},
        {'name': 'Health Potion', 'rarity': 'Common', 'price': 2.0, 'token': 'POTION'},
        {'name': 'Dragon Armor', 'rarity': 'Mythic', 'price': 100.0, 'token': 'ARMOR'},
        {'name': 'Speed Boots', 'rarity': 'Rare', 'price': 25.0, 'token': 'BOOTS'}
    ]

if 'guild_treasury' not in st.session_state:
    st.session_state.guild_treasury = {
        'SOL': 500.0,
        'USDC': 2000.0,
        'GAME_TOKENS': 5000.0
    }

if 'achievements' not in st.session_state:
    st.session_state.achievements = [
        {'name': 'First Kill', 'reward': 10, 'completed': False},
        {'name': 'Level 10 Reached', 'reward': 50, 'completed': False},
        {'name': 'Boss Defeated', 'reward': 100, 'completed': False},
        {'name': 'Arena Champion', 'reward': 200, 'completed': False}
    ]

# Sidebar
st.sidebar.title("🎮 Jupiter Gaming Hub")
st.sidebar.markdown("---")

# User Wallet Display
st.sidebar.subheader("💰 Your Wallet")
for token, balance in st.session_state.user_wallet.items():
    st.sidebar.metric(token, f"{balance:.2f}")

# Navigation
page = st.sidebar.selectbox("Navigate", [
    "🏠 Dashboard",
    "🛒 In-Game Asset Exchange", 
    "💎 Play-to-Earn Hub",
    "🏛️ Guild Treasury",
    "🏆 Achievement Rewards"
])

# Main content
st.title("🚀 Jupiter Micro-Trading for Gaming")
st.markdown("### Seamless blockchain integration for gaming economies")

if page == "🏠 Dashboard":
    # Dashboard Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Portfolio Value", "$1,250.00", "5.2%")
    
    with col2:
        st.metric("Active Trades", "12", "2")
    
    with col3:
        st.metric("Items Owned", "47", "3")
    
    with col4:
        st.metric("Achievements", "2/10", "1")
    
    # Recent Activity Chart
    st.subheader("📈 Trading Activity")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    trading_volume = np.random.uniform(50, 200, len(dates))
    
    fig = px.line(x=dates, y=trading_volume, title="Daily Trading Volume")
    fig.update_layout(xaxis_title="Date", yaxis_title="Volume (SOL)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Traded Items
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Top Traded Items")
        top_items = pd.DataFrame({
            'Item': ['Legendary Sword', 'Magic Shield', 'Dragon Armor', 'Speed Boots'],
            'Volume': [150, 120, 90, 75],
            'Price Change': ['+5.2%', '-2.1%', '+8.7%', '+1.3%']
        })
        st.dataframe(top_items, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Your Recent Trades")
        recent_trades = pd.DataFrame({
            'Time': ['2 min ago', '15 min ago', '1 hour ago', '3 hours ago'],
            'Action': ['Buy', 'Sell', 'Buy', 'Swap'],
            'Item': ['Health Potion', 'Magic Shield', 'Speed Boots', 'SOL → USDC'],
            'Amount': ['2.0 SOL', '30.0 SOL', '25.0 SOL', '50.0 SOL']
        })
        st.dataframe(recent_trades, use_container_width=True)

elif page == "🛒 In-Game Asset Exchange":
    st.header("🛒 In-Game Asset Exchange")
    st.markdown("Trade game items as tokens with automatic Jupiter swaps")
    
    tab1, tab2, tab3 = st.tabs(["🛍️ Marketplace", "💱 Swap Items", "📊 My Inventory"])
    
    with tab1:
        st.subheader("Available Items")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            rarity_filter = st.selectbox("Filter by Rarity", ["All", "Common", "Rare", "Epic", "Legendary", "Mythic"])
        with col2:
            price_range = st.slider("Price Range (SOL)", 0, 200, (0, 200))
        
        # Display items
        for item in st.session_state.game_items:
            if (rarity_filter == "All" or item['rarity'] == rarity_filter) and \
               (price_range[0] <= item['price'] <= price_range[1]):
                
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{item['name']}**")
                    st.write(f"Rarity: {item['rarity']}")
                with col2:
                    st.write(f"**{item['price']} SOL**")
                with col3:
                    if st.button(f"Buy {item['token']}", key=f"buy_{item['token']}"):
                        if st.session_state.user_wallet['SOL'] >= item['price']:
                            st.session_state.user_wallet['SOL'] -= item['price']
                            st.session_state.user_wallet[item['token']] = st.session_state.user_wallet.get(item['token'], 0) + 1
                            st.success(f"Purchased {item['name']} for {item['price']} SOL!")
                            st.rerun()
                        else:
                            st.error("Insufficient SOL balance!")
                with col4:
                    st.write(f"Token: {item['token']}")
                
                st.markdown("---")
    
    with tab2:
        st.subheader("💱 Item Swapping")
        st.markdown("Swap your items directly using Jupiter's routing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**From:**")
            from_token = st.selectbox("Select token to swap from", list(st.session_state.user_wallet.keys()))
            from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)
        
        with col2:
            st.write("**To:**")
            to_token = st.selectbox("Select token to swap to", [token for token in st.session_state.user_wallet.keys() if token != from_token])
            
            # Simulate exchange rate
            if from_token and to_token:
                rate = random.uniform(0.8, 1.2)
                estimated_amount = from_amount * rate
                st.write(f"Estimated: {estimated_amount:.2f} {to_token}")
        
        if st.button("🔄 Execute Swap"):
            if st.session_state.user_wallet[from_token] >= from_amount:
                st.session_state.user_wallet[from_token] -= from_amount
                st.session_state.user_wallet[to_token] += estimated_amount
                st.success(f"Swapped {from_amount} {from_token} for {estimated_amount:.2f} {to_token}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Insufficient {from_token} balance!")
    
    with tab3:
        st.subheader("📊 My Inventory")
        
        inventory_data = []
        for token, balance in st.session_state.user_wallet.items():
            if balance > 0:
                inventory_data.append({
                    'Token': token,
                    'Balance': balance,
                    'Estimated Value (SOL)': balance * random.uniform(0.5, 2.0)
                })
        
        if inventory_data:
            df = pd.DataFrame(inventory_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Your inventory is empty!")

elif page == "💎 Play-to-Earn Hub":
    st.header("💎 Play-to-Earn Integration")
    st.markdown("Automatic token swaps for game rewards")
    
    tab1, tab2 = st.tabs(["🎮 Game Rewards", "⚙️ Auto-Swap Settings"])
    
    with tab1:
        st.subheader("🎮 Active Game Sessions")
        
        # Simulate game sessions
        games = [
            {'name': 'Solana Quest', 'status': 'Playing', 'earnings': 45.2, 'time': '2h 15m'},
            {'name': 'NFT Warriors', 'status': 'Completed', 'earnings': 23.7, 'time': '1h 30m'},
            {'name': 'Crypto Legends', 'status': 'Paused', 'earnings': 12.1, 'time': '45m'}
        ]
        
        for game in games:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{game['name']}**")
            with col2:
                if game['status'] == 'Playing':
                    st.success(game['status'])
                elif game['status'] == 'Completed':
                    st.info(game['status'])
                else:
                    st.warning(game['status'])
            with col3:
                st.write(f"{game['earnings']} tokens")
            with col4:
                st.write(game['time'])
            with col5:
                if st.button(f"Claim", key=f"claim_{game['name']}"):
                    st.session_state.user_wallet['GAME_TOKENS'] += game['earnings']
                    st.success(f"Claimed {game['earnings']} tokens!")
                    st.rerun()
        
        st.markdown("---")
        
        # Earnings Chart
        st.subheader("📈 Daily Earnings")
        
        dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
        earnings = np.random.uniform(10, 80, len(dates))
        
        fig = px.bar(x=dates, y=earnings, title="Daily Token Earnings")
        fig.update_layout(xaxis_title="Date", yaxis_title="Tokens Earned")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("⚙️ Auto-Swap Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Auto-Swap Settings**")
            auto_swap_enabled = st.checkbox("Enable Auto-Swap", value=True)
            
            if auto_swap_enabled:
                swap_threshold = st.slider("Swap when balance exceeds", 50, 1000, 100)
                target_token = st.selectbox("Convert to", ["SOL", "USDC"])
                swap_percentage = st.slider("Percentage to swap", 10, 100, 50)
        
        with col2:
            st.write("**Swap History**")
            swap_history = pd.DataFrame({
                'Date': ['2024-01-28', '2024-01-27', '2024-01-26'],
                'From': ['100 GAME_TOKENS', '75 GAME_TOKENS', '120 GAME_TOKENS'],
                'To': ['5.2 SOL', '3.9 SOL', '6.1 SOL'],
                'Status': ['✅ Complete', '✅ Complete', '✅ Complete']
            })
            st.dataframe(swap_history, use_container_width=True)
        
        if st.button("💾 Save Settings"):
            st.success("Auto-swap settings saved!")

elif page == "🏛️ Guild Treasury":
    st.header("🏛️ Gaming Guild Treasury")
    st.markdown("Manage guild funds with Jupiter swaps")
    
    tab1, tab2, tab3 = st.tabs(["💰 Treasury Overview", "🔄 Guild Swaps", "👥 Member Management"])
    
    with tab1:
        st.subheader("💰 Guild Treasury Balance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("SOL", f"{st.session_state.guild_treasury['SOL']:.2f}", "12.5%")
        with col2:
            st.metric("USDC", f"{st.session_state.guild_treasury['USDC']:.2f}", "8.3%")
        with col3:
            st.metric("GAME_TOKENS", f"{st.session_state.guild_treasury['GAME_TOKENS']:.2f}", "15.7%")
        
        # Treasury allocation pie chart
        st.subheader("📊 Treasury Allocation")
        
        labels = list(st.session_state.guild_treasury.keys())
        values = list(st.session_state.guild_treasury.values())
        
        fig = px.pie(values=values, names=labels, title="Guild Treasury Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent transactions
        st.subheader("📋 Recent Guild Transactions")
        
        transactions = pd.DataFrame({
            'Date': ['2024-01-29', '2024-01-28', '2024-01-27', '2024-01-26'],
            'Type': ['Deposit', 'Reward Distribution', 'Swap', 'Tournament Prize'],
            'Amount': ['+100 SOL', '-50 GAME_TOKENS', '200 SOL → 1000 USDC', '+500 GAME_TOKENS'],
            'Member': ['Guild Leader', 'Auto-System', 'Guild Leader', 'Tournament Winner']
        })
        
        st.dataframe(transactions, use_container_width=True)
    
    with tab2:
        st.subheader("🔄 Guild Treasury Swaps")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Swap From Guild Treasury**")
            from_token = st.selectbox("From Token", list(st.session_state.guild_treasury.keys()), key="guild_from")
            from_amount = st.number_input("Amount to Swap", min_value=0.0, value=10.0, step=1.0, key="guild_amount")
            
            max_available = st.session_state.guild_treasury[from_token]
            st.write(f"Available: {max_available:.2f} {from_token}")
        
        with col2:
            st.write("**To Token**")
            to_token = st.selectbox("To Token", [token for token in st.session_state.guild_treasury.keys() if token != from_token], key="guild_to")
            
            # Simulate exchange rate
            if from_token and to_token:
                rate = random.uniform(0.8, 1.2)
                estimated_amount = from_amount * rate
                st.write(f"**Estimated Output:** {estimated_amount:.2f} {to_token}")
        
        # Swap authorization
        st.write("**Authorization Required**")
        col1, col2 = st.columns(2)
        
        with col1:
            guild_role = st.selectbox("Your Role", ["Guild Leader", "Officer", "Member"])
        with col2:
            if guild_role in ["Guild Leader", "Officer"]:
                if st.button("🔄 Execute Guild Swap"):
                    if st.session_state.guild_treasury[from_token] >= from_amount:
                        st.session_state.guild_treasury[from_token] -= from_amount
                        st.session_state.guild_treasury[to_token] += estimated_amount
                        st.success(f"Guild swap executed: {from_amount} {from_token} → {estimated_amount:.2f} {to_token}")
                        st.rerun()
                    else:
                        st.error("Insufficient guild treasury balance!")
            else:
                st.error("Only Guild Leaders and Officers can execute swaps")
    
    with tab3:
        st.subheader("👥 Guild Member Management")
        
        # Member list
        members = pd.DataFrame({
            'Member': ['GuildMaster', 'CryptoKnight', 'TokenWizard', 'BlockchainHero', 'SolanaWarrior'],
            'Role': ['Guild Leader', 'Officer', 'Officer', 'Member', 'Member'],
            'Contribution': [1500, 800, 600, 400, 350],
            'Rewards Earned': [300, 160, 120, 80, 70],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Inactive']
        })
        
        st.dataframe(members, use_container_width=True)
        
        # Reward distribution
        st.subheader("🎁 Reward Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            reward_type = st.selectbox("Reward Type", ["Achievement Bonus", "Tournament Prize", "Monthly Bonus"])
            total_reward = st.number_input("Total Reward Amount", min_value=0.0, value=100.0, step=10.0)
            reward_token = st.selectbox("Reward Token", list(st.session_state.guild_treasury.keys()))
        
        with col2:
            distribution_method = st.selectbox("Distribution Method", ["Equal Split", "Contribution Based", "Role Based"])
            
            if st.button("💸 Distribute Rewards"):
                if st.session_state.guild_treasury[reward_token] >= total_reward:
                    st.session_state.guild_treasury[reward_token] -= total_reward
                    st.success(f"Distributed {total_reward} {reward_token} to guild members!")
                    st.rerun()
                else:
                    st.error("Insufficient guild treasury balance!")

elif page == "🏆 Achievement Rewards":
    st.header("🏆 Achievement Token Rewards")
    st.markdown("Convert game achievements to tradeable tokens")
    
    tab1, tab2 = st.tabs(["🎯 Available Achievements", "🎁 Reward History"])
    
    with tab1:
        st.subheader("🎯 Achievement Progress")
        
        for i, achievement in enumerate(st.session_state.achievements):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{achievement['name']}**")
                if achievement['completed']:
                    st.success("✅ Completed")
                else:
                    st.warning("⏳ In Progress")
            
            with col2:
                st.write(f"**{achievement['reward']} tokens**")
            
            with col3:
                if not achievement['completed']:
                    if st.button(f"Complete", key=f"complete_{i}"):
                        st.session_state.achievements[i]['completed'] = True
                        st.success(f"Achievement '{achievement['name']}' completed!")
                        st.rerun()
                else:
                    st.write("✅ Done")
            
            with col4:
                if achievement['completed']:
                    if st.button(f"Claim", key=f"claim_achievement_{i}"):
                        st.session_state.user_wallet['GAME_TOKENS'] += achievement['reward']
                        st.success(f"Claimed {achievement['reward']} tokens!")
                        st.rerun()
                else:
                    st.write("🔒 Locked")
            
            st.markdown("---")
        
        # Achievement statistics
        completed_achievements = sum(1 for a in st.session_state.achievements if a['completed'])
        total_achievements = len(st.session_state.achievements)
        completion_rate = (completed_achievements / total_achievements) * 100
        
        st.subheader("📊 Achievement Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Completed", f"{completed_achievements}/{total_achievements}")
        with col2:
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        with col3:
            total_rewards = sum(a['reward'] for a in st.session_state.achievements if a['completed'])
            st.metric("Total Rewards Earned", f"{total_rewards} tokens")
    
    with tab2:
        st.subheader("🎁 Reward Claim History")
        
        # Sample reward history
        reward_history = pd.DataFrame({
            'Date': ['2024-01-29', '2024-01-28', '2024-01-27', '2024-01-26'],
            'Achievement': ['First Kill', 'Level 10 Reached', 'Boss Defeated', 'Arena Champion'],
            'Tokens Earned': [10, 50, 100, 200],
            'Converted To': ['5 SOL', '25 SOL', '50 SOL', '100 SOL'],
            'Status': ['✅ Claimed', '✅ Claimed', '✅ Claimed', '⏳ Pending']
        })
        
        st.dataframe(reward_history, use_container_width=True)
        
        # Conversion settings
        st.subheader("⚙️ Auto-Conversion Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_convert = st.checkbox("Auto-convert achievement tokens", value=True)
            if auto_convert:
                convert_to = st.selectbox("Convert to", ["SOL", "USDC"])
                conversion_rate = st.slider("Conversion rate (%)", 10, 100, 100)
        
        with col2:
            st.write("**Conversion Preview**")
            if auto_convert:
                pending_tokens = 50  # Example
                converted_amount = pending_tokens * (conversion_rate / 100) * 0.5  # Simulated rate
                st.write(f"Pending: {pending_tokens} tokens")
                st.write(f"Will convert: {converted_amount:.2f} {convert_to}")

# Footer
st.markdown("---")
st.markdown("**Jupiter Gaming Micro-Trading Platform** | Powered by Solana & Jupiter Protocol")
st.markdown("*Demo application for educational purposes*")
