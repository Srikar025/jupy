import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import base64
from dataclasses import dataclass
import asyncio

# Configuration using Streamlit secrets
@st.cache_data
def get_config():
    """Get configuration from Streamlit secrets"""
    try:
        return {
            "JUPITER_API_BASE": st.secrets.get("JUPITER_API_BASE", "https://quote-api.jup.ag/v6"),
            "SOLANA_RPC_URL": st.secrets.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
            "HELIUS_API_KEY": st.secrets.get("HELIUS_API_KEY", "")
        }
    except Exception as e:
        st.error(f"Error loading secrets: {e}")
        # Return default values if secrets are not available
        return {
            "JUPITER_API_BASE": "https://quote-api.jup.ag/v6",
            "SOLANA_RPC_URL": "https://api.mainnet-beta.solana.com",
            "HELIUS_API_KEY": ""
        }

@dataclass
class GameItem:
    id: str
    name: str
    rarity: str
    token_mint: str
    price_sol: float
    description: str
    game: str

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    token_reward: str
    reward_amount: float
    unlocked: bool

@dataclass
class GuildMember:
    wallet: str
    role: str
    contribution_score: int
    joined_date: str

class JupiterAPI:
    def __init__(self):
        self.config = get_config()
    
    def get_token_price(self, mint_address: str) -> float:
        """Get token price from Jupiter API"""
        try:
            response = requests.get(f"{self.config['JUPITER_API_BASE']}/price?ids={mint_address}")
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get(mint_address, {}).get('price', 0.0)
        except Exception as e:
            st.error(f"Error fetching price: {e}")
        return 0.0
    
    def get_swap_quote(self, input_mint: str, output_mint: str, amount: int):
        """Get swap quote from Jupiter"""
        try:
            params = {
                'inputMint': input_mint,
                'outputMint': output_mint,
                'amount': amount,
                'slippageBps': 50  # 0.5% slippage
            }
            response = requests.get(f"{self.config['JUPITER_API_BASE']}/quote", params=params)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error getting swap quote: {e}")
        return None

class HeliusAPI:
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config['HELIUS_API_KEY']
        self.base_url = f"https://api.helius.xyz/v0"
    
    def get_wallet_assets(self, wallet_address: str):
        """Get wallet assets using Helius API"""
        if not self.api_key:
            st.warning("Helius API key not configured")
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(
                f"{self.base_url}/addresses/{wallet_address}/balances?api-key={self.api_key}",
                headers=headers
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error fetching wallet assets: {e}")
        return []

# Removed unnecessary API classes - keeping only Jupiter and Helius

class SolanaWallet:
    def __init__(self):
        self.connected = False
        self.public_key = None
        self.balance = 0.0
        self.helius_api = HeliusAPI()
    
    def connect_wallet(self, wallet_type: str = "Phantom"):
        """Simulate wallet connection - In production, use Streamlit JS bridge"""
        if wallet_type in st.session_state.get('available_wallets', []):
            self.connected = True
            self.public_key = st.session_state.get('wallet_address', 'Demo_Wallet_Address')
            self.balance = st.session_state.get('wallet_balance', 5.0)
            return True
        return False
    
    def disconnect_wallet(self):
        """Disconnect wallet"""
        self.connected = False
        self.public_key = None
        self.balance = 0.0
    
    def get_wallet_assets(self):
        """Get wallet assets using Helius API"""
        if self.connected and self.public_key:
            return self.helius_api.get_wallet_assets(self.public_key)
        return []

class GameItemMarketplace:
    def __init__(self):
        self.items = self._initialize_items()
        self.jupiter_api = JupiterAPI()
    
    def _initialize_items(self) -> List[GameItem]:
        """Initialize demo game items"""
        return [
            GameItem("sword_001", "Legendary Fire Sword", "Legendary", "So11111111111111111111111111111111111111112", 2.5, "A powerful sword that burns enemies", "Fantasy RPG"),
            GameItem("shield_001", "Diamond Shield", "Epic", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 1.8, "Unbreakable diamond shield", "Fantasy RPG"),
            GameItem("bow_001", "Elven Longbow", "Rare", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", 1.2, "Precise elven craftsmanship", "Fantasy RPG"),
            GameItem("skin_001", "Cosmic Warrior Skin", "Legendary", "So11111111111111111111111111111111111111112", 3.0, "Exclusive cosmic themed skin", "Battle Arena"),
            GameItem("car_001", "Speed Demon Vehicle", "Epic", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 2.2, "Fastest car in the racing game", "Racing World"),
        ]
    
    def get_items_by_game(self, game: str) -> List[GameItem]:
        return [item for item in self.items if item.game == game]
    
    def get_real_time_price(self, token_mint: str) -> float:
        """Get real-time price using Jupiter API"""
        return self.jupiter_api.get_token_price(token_mint)

class AchievementSystem:
    def __init__(self):
        self.achievements = self._initialize_achievements()
    
    def _initialize_achievements(self) -> List[Achievement]:
        return [
            Achievement("ach_001", "First Victory", "Win your first match", "GAME", 10.0, True),
            Achievement("ach_002", "Speed Demon", "Complete 10 races under 2 minutes", "SPEED", 25.0, False),
            Achievement("ach_003", "Treasure Hunter", "Find 50 hidden treasures", "TREASURE", 50.0, True),
            Achievement("ach_004", "Guild Leader", "Lead a guild for 30 days", "LEADER", 100.0, False),
            Achievement("ach_005", "Master Trader", "Complete 100 item trades", "TRADE", 75.0, False),
        ]

class GuildTreasury:
    def __init__(self):
        self.guild_name = ""
        self.treasury_balance = 0.0
        self.members = []
        self.transactions = []
    
    def add_member(self, wallet: str, role: str = "Member"):
        member = GuildMember(wallet, role, 0, datetime.now().strftime("%Y-%m-%d"))
        self.members.append(member)
    
    def deposit_to_treasury(self, amount: float, from_wallet: str):
        self.treasury_balance += amount
        transaction = {
            "type": "Deposit",
            "amount": amount,
            "from": from_wallet,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
    
    def withdraw_from_treasury(self, amount: float, to_wallet: str, purpose: str):
        if amount <= self.treasury_balance:
            self.treasury_balance -= amount
            transaction = {
                "type": "Withdrawal",
                "amount": amount,
                "to": to_wallet,
                "purpose": purpose,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(transaction)
            return True
        return False

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = SolanaWallet()
    st.session_state.marketplace = GameItemMarketplace()
    st.session_state.achievements = AchievementSystem()
    st.session_state.guild = GuildTreasury()
    st.session_state.available_wallets = ["Phantom", "Solflare", "Backpack"]
    st.session_state.wallet_address = None
    st.session_state.wallet_balance = 5.0

def check_api_keys():
    """Check if API keys are configured properly"""
    config = get_config()
    api_status = {}
    
    # Check which APIs are configured
    api_status['Jupiter'] = True  # Jupiter doesn't require API key for basic functionality
    api_status['Helius'] = bool(config['HELIUS_API_KEY'])
    
    return api_status

def display_api_status():
    """Display API configuration status"""
    with st.expander("🔑 API Configuration Status"):
        api_status = check_api_keys()
        
        for api_name, is_configured in api_status.items():
            status_icon = "✅" if is_configured else "❌"
            st.write(f"{status_icon} {api_name}")
        
        unconfigured_apis = [api for api, status in api_status.items() if not status]
        if unconfigured_apis:
            st.warning(f"⚠️ Unconfigured APIs: {', '.join(unconfigured_apis)}")
            st.info("Add HELIUS_API_KEY to Streamlit secrets for wallet data")

def main():
    st.set_page_config(
        page_title="Jupiter Gaming Micro-Trading Platform",
        page_icon="🎮",
        layout="wide"
    )
    
    # Header
    st.title("🎮 Jupiter Gaming Micro-Trading Platform")
    st.markdown("Trade game assets, earn tokens, and manage guild treasuries on Solana")
    
    # Display API status
    display_api_status()
    
    # Wallet Connection Sidebar
    with st.sidebar:
        st.header("🔗 Wallet Connection")
        
        if not st.session_state.wallet.connected:
            wallet_type = st.selectbox("Select Wallet", st.session_state.available_wallets)
            
            if st.button("Connect Wallet", type="primary"):
                if st.session_state.wallet.connect_wallet(wallet_type):
                    st.success(f"Connected to {wallet_type}!")
                    st.rerun()
                else:
                    st.error("Failed to connect wallet")
        else:
            st.success("✅ Wallet Connected")
            st.write(f"**Address:** {st.session_state.wallet.public_key[:8]}...{st.session_state.wallet.public_key[-8:]}")
            st.write(f"**Balance:** {st.session_state.wallet.balance} SOL")
            
            if st.button("Disconnect"):
                st.session_state.wallet.disconnect_wallet()
                st.rerun()
        
        st.divider()
        
        # Quick Stats
        st.header("📊 Quick Stats")
        st.metric("Items Owned", 12)
        st.metric("Achievements", 3)
        st.metric("Guild Treasury", "2.4 SOL")
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🛒 Item Marketplace", 
        "🏆 Achievements", 
        "💰 Play-to-Earn", 
        "🏛️ Guild Treasury",
        "📈 Trading Analytics"
    ])
    
    # Tab 1: Item Marketplace
    with tab1:
        st.header("🛒 In-Game Asset Exchange")
        
        if not st.session_state.wallet.connected:
            st.warning("Please connect your wallet to access the marketplace")
            return
        
        # Game selection
        games = ["All Games", "Fantasy RPG", "Battle Arena", "Racing World"]
        selected_game = st.selectbox("Filter by Game", games)
        
        # Display items
        items = st.session_state.marketplace.items
        if selected_game != "All Games":
            items = st.session_state.marketplace.get_items_by_game(selected_game)
        
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"### {item.name}")
                    st.markdown(f"**Rarity:** {item.rarity}")
                    st.markdown(f"**Game:** {item.game}")
                    
                    # Try to get real-time price
                    real_time_price = st.session_state.marketplace.get_real_time_price(item.token_mint)
                    display_price = real_time_price if real_time_price > 0 else item.price_sol
                    st.markdown(f"**Price:** {display_price:.4f} SOL")
                    
                    st.markdown(f"*{item.description}*")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Buy", key=f"buy_{item.id}"):
                            if st.session_state.wallet.balance >= display_price:
                                st.session_state.wallet.balance -= display_price
                                st.success(f"Purchased {item.name}!")
                                st.rerun()
                            else:
                                st.error("Insufficient balance")
                    
                    with col2:
                        if st.button(f"Swap", key=f"swap_{item.id}"):
                            st.info("Opening swap interface...")
        
        # Swap Interface
        st.divider()
        st.subheader("🔄 Token Swap Interface")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            input_token = st.selectbox("From Token", ["SOL", "USDC", "USDT"])
        with col2:
            output_token = st.selectbox("To Token", ["GAME", "SPEED", "TREASURE"])
        with col3:
            amount = st.number_input("Amount", min_value=0.1, value=1.0, step=0.1)
        
        if st.button("Get Quote"):
            with st.spinner("Getting quote from Jupiter..."):
                # Use Jupiter API for real quote if available
                jupiter_api = JupiterAPI()
                # For demo purposes, we'll simulate the quote
                time.sleep(1)
                estimated_output = amount * 100  # Mock conversion rate
                st.success(f"Quote: {amount} {input_token} → {estimated_output:.2f} {output_token}")
                
                if st.button("Execute Swap"):
                    st.success("Swap executed successfully!")
    
    # Tab 2: Achievements
    with tab2:
        st.header("🏆 Achievement Token Rewards")
        
        if not st.session_state.wallet.connected:
            st.warning("Please connect your wallet to view achievements")
            return
        
        for achievement in st.session_state.achievements.achievements:
            with st.expander(f"{'✅' if achievement.unlocked else '⏳'} {achievement.name}"):
                st.write(f"**Description:** {achievement.description}")
                st.write(f"**Reward:** {achievement.reward_amount} {achievement.token_reward}")
                st.write(f"**Status:** {'Unlocked' if achievement.unlocked else 'Locked'}")
                
                if achievement.unlocked:
                    if st.button(f"Claim {achievement.reward_amount} {achievement.token_reward}", key=f"claim_{achievement.id}"):
                        st.success(f"Claimed {achievement.reward_amount} {achievement.token_reward} tokens!")
                        # Add tokens to wallet balance simulation
                        st.session_state.wallet.balance += achievement.reward_amount * 0.01  # Convert to SOL equivalent
    
    # Tab 3: Play-to-Earn
    with tab3:
        st.header("💰 Play-to-Earn Integration")
        
        if not st.session_state.wallet.connected:
            st.warning("Please connect your wallet to access play-to-earn features")
            return
        
        # Game session simulator
        st.subheader("🎮 Active Game Session")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Score", "2,450")
        with col2:
            st.metric("Tokens Earned", "124 GAME")
        with col3:
            st.metric("Session Time", "23:45")
        
        # Auto-swap settings
        st.subheader("⚙️ Auto-Swap Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            auto_swap = st.checkbox("Enable Auto-Swap")
            threshold = st.number_input("Swap when earning exceeds", value=100, step=10)
        with col2:
            swap_to = st.selectbox("Auto-swap to", ["SOL", "USDC", "Keep as GAME"])
            swap_percentage = st.slider("Percentage to swap", 0, 100, 50)
        
        if auto_swap:
            st.info(f"Auto-swap enabled: {swap_percentage}% of earnings will be swapped to {swap_to} when threshold of {threshold} tokens is reached")
        
        # Manual claim
        st.subheader("💎 Claim Rewards")
        pending_rewards = 124
        
        if st.button(f"Claim {pending_rewards} GAME Tokens"):
            st.success(f"Claimed {pending_rewards} GAME tokens!")
            if auto_swap and pending_rewards >= threshold:
                swap_amount = pending_rewards * (swap_percentage / 100)
                st.info(f"Auto-swapping {swap_amount:.1f} GAME to {swap_to}")
    
    # Tab 4: Guild Treasury
    with tab4:
        st.header("🏛️ Gaming Guild Treasury")
        
        if not st.session_state.wallet.connected:
            st.warning("Please connect your wallet to access guild features")
            return
        
        # Guild setup
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Guild Information")
            guild_name = st.text_input("Guild Name", value="Crypto Warriors")
            st.session_state.guild.guild_name = guild_name
            
            st.metric("Treasury Balance", f"{st.session_state.guild.treasury_balance:.2f} SOL")
            st.metric("Total Members", len(st.session_state.guild.members))
        
        with col2:
            st.subheader("Treasury Actions")
            
            # Deposit
            deposit_amount = st.number_input("Deposit Amount (SOL)", min_value=0.1, value=1.0, step=0.1)
            if st.button("Deposit to Treasury"):
                if st.session_state.wallet.balance >= deposit_amount:
                    st.session_state.wallet.balance -= deposit_amount
                    st.session_state.guild.deposit_to_treasury(deposit_amount, st.session_state.wallet.public_key)
                    st.success(f"Deposited {deposit_amount} SOL to guild treasury!")
                    st.rerun()
                else:
                    st.error("Insufficient balance")
            
            # Withdraw
            withdraw_amount = st.number_input("Withdraw Amount (SOL)", min_value=0.1, value=0.5, step=0.1)
            withdraw_purpose = st.text_input("Purpose", placeholder="e.g., Tournament prize")
            if st.button("Withdraw from Treasury"):
                if st.session_state.guild.withdraw_from_treasury(withdraw_amount, st.session_state.wallet.public_key, withdraw_purpose):
                    st.session_state.wallet.balance += withdraw_amount
                    st.success(f"Withdrawn {withdraw_amount} SOL from guild treasury!")
                    st.rerun()
                else:
                    st.error("Insufficient treasury balance")
        
        # Guild Members
        st.subheader("👥 Guild Members")
        
        # Add member
        with st.expander("Add New Member"):
            new_member_wallet = st.text_input("Wallet Address")
            new_member_role = st.selectbox("Role", ["Member", "Officer", "Leader"])
            if st.button("Add Member"):
                st.session_state.guild.add_member(new_member_wallet, new_member_role)
                st.success("Member added successfully!")
                st.rerun()
        
        # Display members
        if st.session_state.guild.members:
            members_df = pd.DataFrame([
                {
                    "Wallet": member.wallet[:8] + "..." + member.wallet[-8:] if len(member.wallet) > 16 else member.wallet,
                    "Role": member.role,
                    "Contribution": member.contribution_score,
                    "Joined": member.joined_date
                }
                for member in st.session_state.guild.members
            ])
            st.dataframe(members_df, use_container_width=True)
        
        # Transaction History
        st.subheader("📊 Treasury Transactions")
        if st.session_state.guild.transactions:
            transactions_df = pd.DataFrame(st.session_state.guild.transactions)
            st.dataframe(transactions_df, use_container_width=True)
        else:
            st.info("No transactions yet")
    
    # Tab 5: Trading Analytics
    with tab5:
        st.header("📈 Trading Analytics & Insights")
        
        if not st.session_state.wallet.connected:
            st.warning("Please connect your wallet to view analytics")
            return
        
        # Portfolio overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Portfolio Value", "12.5 SOL", "↗️ +2.3%")
        with col2:
            st.metric("24h Trading Volume", "156 GAME", "↗️ +15%")
        with col3:
            st.metric("Items Traded", "23", "↗️ +3")
        with col4:
            st.metric("Profit/Loss", "+3.2 SOL", "↗️ +34%")
        
        # Price charts (mock data)
        st.subheader("📊 Token Price Charts")
        
        # Generate mock price data
        import numpy as np
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        game_prices = np.random.randn(len(dates)).cumsum() + 100
        
        chart_data = pd.DataFrame({
            'Date': dates,
            'GAME Token': game_prices,
            'SPEED Token': game_prices * 0.8 + np.random.randn(len(dates)) * 5,
            'TREASURE Token': game_prices * 1.2 + np.random.randn(len(dates)) * 8
        })
        
        st.line_chart(chart_data.set_index('Date'))
        
        # Trading opportunities
        st.subheader("🎯 Trading Opportunities")
        
        opportunities = [
            {"Item": "Legendary Fire Sword", "Current Price": "2.5 SOL", "Trend": "↗️ Rising", "Recommendation": "HOLD"},
            {"Item": "Diamond Shield", "Current Price": "1.8 SOL", "Trend": "↘️ Falling", "Recommendation": "BUY"},
            {"Item": "Elven Longbow", "Current Price": "1.2 SOL", "Trend": "→ Stable", "Recommendation": "HOLD"},
            {"Item": "Cosmic Warrior Skin", "Current Price": "3.0 SOL", "Trend": "↗️ Rising", "Recommendation": "SELL"},
        ]
        
        opportunities_df = pd.DataFrame(opportunities)
        st.dataframe(opportunities_df, use_container_width=True)

if __name__ == "__main__":
    main()