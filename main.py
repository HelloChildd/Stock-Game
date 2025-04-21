import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import openai
from openai import OpenAI  # Add this import at the top
from typing import Tuple

# Set Streamlit theme and configure page
st.set_page_config(page_title="Future Trading Simulator", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for sleek modern look (keeping the white theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    .stButton>button {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0b5ed7;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .stock-card {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        border-radius: 8px;
        background-color: white;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .stock-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .positive {
        color: #198754;
    }
    .negative {
        color: #dc3545;
    }
    h1, h2, h3 {
        color: #212529;
    }
    .sidebar .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Add OpenAI API key configuration
try:
    openai.api_key = st.secrets["openai_api_key"]
except Exception as e:
    # Fallback to environment variable or hardcoded key (for development only)
    openai.api_key = "your-actual-api-key"  # Replace with your real API key

class Stock:
    def __init__(self, name, initial_price, volatility, trend):
        self.name = name
        self.price = initial_price
        self.history = [initial_price]
        self.dates = [datetime.now()]
        self.volatility = volatility
        self.trend = trend  # Overall market trend

# Near the top of the file, add these constants
MILESTONES = {
    100000: "First 100K - Buy a Luxury Car 🚗",
    250000: "250K - Buy a Vacation Home 🏖️",
    500000: "500K - Start Your Own Business 💼",
    1000000: "WINNER: You're a Millionaire! 🎉"
}

class StockMarketGame:
    def __init__(self):
        self.stocks = {
            'AAPL': Stock('Apple Inc.', random.uniform(165, 185), 0.02, 0.002),
            'GOOGL': Stock('Google', random.uniform(2700, 3000), 0.025, 0.003),
            'TSLA': Stock('Tesla', random.uniform(850, 950), 0.045, 0.004),
            'AMZN': Stock('Amazon', random.uniform(3100, 3400), 0.028, 0.002),
            'MSFT': Stock('Microsoft', random.uniform(280, 320), 0.022, 0.002),
            'META': Stock('Meta', random.uniform(260, 300), 0.035, 0.003),
            'NVDA': Stock('NVIDIA', random.uniform(420, 480), 0.04, 0.003),
            'JPM': Stock('JPMorgan', random.uniform(130, 150), 0.015, 0.001),
            'DIS': Stock('Disney', random.uniform(90, 100), 0.025, 0.002),
            'NFLX': Stock('Netflix', random.uniform(400, 440), 0.038, 0.003),
            'COIN': Stock('Coinbase', random.uniform(75, 95), 0.055, 0.005),
            'ADBE': Stock('Adobe', random.uniform(500, 540), 0.028, 0.002)
        }
        self.used_events = set()  # Track used events
        self.last_reset_day = 1   # Track when to reset used events

    # Fix the generate_event method to properly handle the nested try-except blocks
    def generate_event(self) -> Tuple[str, float]:
        # Reset used events every 30 days
        if st.session_state.day - self.last_reset_day >= 30:
            self.used_events.clear()
            self.last_reset_day = st.session_state.day
        
        try:
            company = random.choice(list(self.stocks.keys()))
            event_types = [
                f"announced a new {random.choice(['product launch', 'partnership', 'acquisition', 'technology breakthrough'])}",
                f"reported {random.choice(['better', 'worse'])} than expected {random.choice(['earnings', 'revenue', 'growth'])}",
                f"revealed plans for {random.choice(['expansion', 'restructuring', 'cost-cutting', 'innovation'])}",
                f"faced {random.choice(['regulatory challenges', 'market competition', 'supply chain issues', 'leadership changes'])}"
            ]
            
            # Create client instance
            client = OpenAI(api_key=openai.api_key)
            
            try:
                # Updated API call
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a financial news reporter. Generate a unique, specific news event about {company} that hasn't been reported before. Include specific details about products, numbers, or impacts."},
                        {"role": "user", "content": f"Generate a market event about {company} using one of these templates: {event_types}. Add specific details and impact value (between -0.15 and 0.15) in format: 'Event|impact_value'"}
                    ],
                    max_tokens=50,
                    temperature=0.9
                )
                
                event_text = response.choices[0].message.content.strip()
                event, impact = event_text.split('|')
                
                # Only use event if it's unique in the last 30 days
                if event not in self.used_events:
                    self.used_events.add(event)
                    return event, float(impact)
                else:
                    # Generate alternative event if duplicate
                    company_name = self.stocks[company].name
                    alt_event = f"{company_name} {random.choice(event_types)}"
                    return alt_event, random.uniform(-0.15, 0.15)
            except Exception as e:
                return self.generate_fallback_event()
        except Exception as e:
            return self.generate_fallback_event()

    def generate_fallback_event(self) -> Tuple[str, float]:
        company = random.choice(list(self.stocks.keys()))
        company_name = self.stocks[company].name
        
        events = [
            f"{company_name} stock moves on market sentiment",
            f"{company_name} responds to industry trends",
            f"{company_name} adjusts to market conditions",
            f"Investors react to {company_name} developments"
        ]
        
        # Fix potential empty list error
        unused_events = [e for e in events if e not in self.used_events]
        if not unused_events:
            # If all events are used, create a new unique event
            event = f"{company_name} stock fluctuates amid trading activity on day {st.session_state.day}"
        else:
            event = random.choice(unused_events)
            
        self.used_events.add(event)
        return event, random.uniform(-0.15, 0.15)

    def update_prices(self):
        event, event_impact = self.generate_event()
        for stock in self.stocks.values():
            trend = stock.trend * random.uniform(0.8, 1.2)
            volatility = random.uniform(-stock.volatility, stock.volatility)
            market_sentiment = random.uniform(-0.02, 0.02)
            
            total_change = trend + volatility + market_sentiment + event_impact
            stock.price *= (1 + total_change)
            stock.history.append(stock.price)
            stock.dates.append(datetime.now())
        return event

def create_stock_chart(stock):
    fig = go.Figure()
    
    # Custom color and style for each stock
    stock_styles = {
        'AAPL': {'color': '#FF6B6B', 'pattern': 'lines', 'dash': 'solid', 'symbol': 'circle'},
        'GOOGL': {'color': '#4ECDC4', 'pattern': 'lines+markers', 'dash': 'solid', 'symbol': 'diamond'},
        'TSLA': {'color': '#FFE66D', 'pattern': 'lines', 'dash': 'dash', 'symbol': 'x'},
        'AMZN': {'color': '#FF8B94', 'pattern': 'lines+markers', 'dash': 'solid', 'symbol': 'triangle-up'},
        'MSFT': {'color': '#96CEB4', 'pattern': 'lines', 'dash': 'dot', 'symbol': 'square'},
        'META': {'color': '#FFEEAD', 'pattern': 'lines+markers', 'dash': 'dashdot', 'symbol': 'star'},
        'NVDA': {'color': '#D4A5A5', 'pattern': 'lines', 'dash': 'longdash', 'symbol': 'pentagon'},
        'JPM': {'color': '#9AC1D9', 'pattern': 'lines+markers', 'dash': 'solid', 'symbol': 'hexagon'},
        'DIS': {'color': '#FFB6B9', 'pattern': 'lines', 'dash': 'dash', 'symbol': 'cross'},
        'NFLX': {'color': '#A8E6CF', 'pattern': 'lines+markers', 'dash': 'dot', 'symbol': 'triangle-down'},
        'COIN': {'color': '#DCEDC1', 'pattern': 'lines', 'dash': 'dashdot', 'symbol': 'hourglass'},
        'ADBE': {'color': '#FFD3B6', 'pattern': 'lines+markers', 'dash': 'longdashdot', 'symbol': 'octagon'}
    }
    
    # Get stock symbol from name (e.g., 'Apple Inc.' -> 'AAPL')
    symbol = next((s for s, stk in st.session_state.game.stocks.items() if stk.name == stock.name), '')
    style = stock_styles.get(symbol, {'color': '#64ffda', 'pattern': 'lines', 'dash': 'solid', 'symbol': 'circle'})
    
    # Add main price line
    fig.add_trace(go.Scatter(
        x=stock.dates,
        y=stock.history,
        mode=style['pattern'],
        name=stock.name,
        line=dict(
            color=style['color'],
            width=2,
            dash=style['dash']
        ),
        marker=dict(
            size=6,
            symbol=style['symbol']
        )
    ))
    
    # Add volume bars at the bottom
    fig.add_trace(go.Bar(
        x=stock.dates,
        y=[abs(stock.history[i] - stock.history[i-1]) if i > 0 else 0 for i in range(len(stock.history))],
        name='Volume',
        marker_color=style['color'],
        opacity=0.3,
        yaxis='y2'
    ))
    
    # Add moving average if we have enough data points
    if len(stock.history) > 5:
        ma_period = min(5, len(stock.history) - 1)
        ma_data = []
        for i in range(len(stock.history)):
            if i < ma_period:
                ma_data.append(None)
            else:
                ma_data.append(sum(stock.history[i-ma_period:i]) / ma_period)
        
        fig.add_trace(go.Scatter(
            x=stock.dates,
            y=ma_data,
            mode='lines',
            name=f'{ma_period}-Day MA',
            line=dict(
                color='rgba(255, 255, 255, 0.7)',
                width=1.5,
                dash='dot'
            )
        ))
    
    # Add trend channel (upper and lower bounds)
    if len(stock.history) > 3:
        # Simple trend channel based on recent volatility
        volatility = stock.volatility * stock.price
        upper_bound = [price + volatility for price in stock.history]
        lower_bound = [price - volatility for price in stock.history]
        
        fig.add_trace(go.Scatter(
            x=stock.dates,
            y=upper_bound,
            mode='lines',
            name='Upper Channel',
            line=dict(color='rgba(100, 255, 218, 0.3)', width=1, dash='dot'),
            fill=None
        ))
        
        fig.add_trace(go.Scatter(
            x=stock.dates,
            y=lower_bound,
            mode='lines',
            name='Lower Channel',
            line=dict(color='rgba(100, 255, 218, 0.3)', width=1, dash='dot'),
            fill='tonexty'  # Fill area between upper and lower bound
        ))
    
    # Update layout to match white theme
    fig.update_layout(
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ffffff',
        font=dict(color='#212529'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#e9ecef',
            gridwidth=0.5
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e9ecef',
            gridwidth=0.5,
            title='Price'
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        height=400,
        title=dict(
            text=f"{stock.name} Stock Performance",
            x=0.5,
            y=0.95
        ),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#0d6efd'
        ),
        hovermode='x unified'
    )
    
    return fig

def main():
    # Initialize game state
    if 'game' not in st.session_state:
        st.session_state.game = StockMarketGame()
        st.session_state.cash = 10000
        st.session_state.portfolio = {}
        st.session_state.day = 1
        st.session_state.events_history = []
        st.session_state.selected_stock = list(st.session_state.game.stocks.keys())[0]
        st.session_state.tab = "Dashboard"
    
    # Sidebar for navigation and controls
    with st.sidebar:
        st.title("🚀 Trading Simulator")
        
        # Portfolio Value Calculation
        total_portfolio_value = st.session_state.cash
        for symbol, shares in st.session_state.portfolio.items():
            total_portfolio_value += shares * st.session_state.game.stocks[symbol].price
        
        # User stats in sidebar
        st.markdown(f"""
        <div class="card">
            <h3>Day {st.session_state.day}</h3>
            <h2>${total_portfolio_value:.2f}</h2>
            <p>Cash: ${st.session_state.cash:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation tabs using radio buttons instead of multiple buttons
        st.session_state.tab = st.radio(
            "Navigation",
            ["Dashboard", "Portfolio", "Trading"],
            index=["Dashboard", "Portfolio", "Trading"].index(st.session_state.tab)
        )
        
        # Stock selector in sidebar
        st.markdown("### Select Stock")
        st.session_state.selected_stock = st.selectbox(
            "Choose a stock to view/trade",
            list(st.session_state.game.stocks.keys()),
            index=list(st.session_state.game.stocks.keys()).index(st.session_state.selected_stock)
        )
        
        # Trading controls in sidebar
        if st.session_state.tab == "Trading":
            stock = st.session_state.game.stocks[st.session_state.selected_stock]
            st.markdown(f"### {stock.name} (${stock.price:.2f})")
            
            # Buy with slider
            st.markdown("### Buy Shares")
            max_shares = int(st.session_state.cash / stock.price)
            buy_shares = st.slider("Shares to buy", 0, max(1, max_shares), 0)
            buy_cost = buy_shares * stock.price
            st.markdown(f"Cost: ${buy_cost:.2f}")
            
            if st.button("Execute Buy"):
                if buy_cost <= st.session_state.cash and buy_shares > 0:
                    st.session_state.cash -= buy_cost
                    st.session_state.portfolio[st.session_state.selected_stock] = st.session_state.portfolio.get(st.session_state.selected_stock, 0) + buy_shares
                    st.success(f"Bought {buy_shares} shares of {st.session_state.selected_stock}")
                    st.rerun()
                elif buy_shares > 0:
                    st.error("Insufficient funds!")
            
            # Fix the slider issue in the main function
            # Sell with slider
            st.markdown("### Sell Shares")
            owned_shares = st.session_state.portfolio.get(st.session_state.selected_stock, 0)
            if owned_shares > 0:
                sell_shares = st.slider("Shares to sell", 0, owned_shares, 0)
                sell_revenue = sell_shares * stock.price
                st.markdown(f"Revenue: ${sell_revenue:.2f}")
                
                if st.button("Execute Sell"):
                    if sell_shares > 0:
                        st.session_state.cash += sell_revenue
                        st.session_state.portfolio[st.session_state.selected_stock] -= sell_shares
                        if st.session_state.portfolio[st.session_state.selected_stock] == 0:
                            del st.session_state.portfolio[st.session_state.selected_stock]
                        st.success(f"Sold {sell_shares} shares of {st.session_state.selected_stock}")
                        st.rerun()
            else:
                st.info(f"You don't own any shares of {st.session_state.selected_stock}")
        
        # Next day button at bottom of sidebar
        if st.button("⏭️ Next Trading Day"):
            # Generate 1-3 company-specific events
            for _ in range(random.randint(1, 3)):
                try:
                    event = st.session_state.game.update_prices()
                    st.session_state.events_history.append(event)
                except Exception as e:
                    # Fallback if event generation fails
                    company = random.choice(list(st.session_state.game.stocks.keys()))
                    event = f"Market fluctuations affect {st.session_state.game.stocks[company].name}"
                    st.session_state.events_history.append(event)
            
            st.session_state.day += 1
            st.rerun()
    
    # Main content area based on selected tab
    if st.session_state.tab == "Dashboard":
        display_dashboard(total_portfolio_value)
    elif st.session_state.tab == "Portfolio":
        display_portfolio()
    elif st.session_state.tab == "Trading":
        display_trading()

def display_dashboard(total_portfolio_value):
    st.title("Market Dashboard")
    
    # Recent news at the top
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📰 Recent Market News")
    if st.session_state.events_history:
        for event in reversed(st.session_state.events_history[-3:]):
            st.markdown(f"• {event}")
    else:
        st.info("No market news yet. Start trading to see updates!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stock chart
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        create_stock_chart(st.session_state.game.stocks[st.session_state.selected_stock]), 
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Portfolio summary and milestones
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💰 Portfolio Summary")
        st.markdown(f"Cash: ${st.session_state.cash:.2f}")
        
        # Calculate portfolio value
        invested_value = total_portfolio_value - st.session_state.cash
        st.markdown(f"Invested: ${invested_value:.2f}")
        st.markdown(f"Total Value: ${total_portfolio_value:.2f}")
        
        # Simple portfolio performance chart
        if st.session_state.day > 1:
            st.markdown("### Portfolio Growth")
            # This would be better with historical data tracking
            st.progress(min(1.0, total_portfolio_value / 20000))
            st.markdown(f"Progress: {total_portfolio_value / 20000 * 100:.1f}% of $20,000 goal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Milestones")
        
        for value, milestone in MILESTONES.items():
            if total_portfolio_value >= value:
                st.markdown(f"✅ {milestone}")
            else:
                st.markdown(f"⭕ {milestone}")
                
        # Progress to next milestone
        next_milestone = min((m for m in MILESTONES.keys() if m > total_portfolio_value), default=None)
        if next_milestone:
            progress = total_portfolio_value / next_milestone  # Define progress variable here
            st.progress(progress)
            st.markdown(f"Progress to next milestone: {progress * 100:.1f}%")
        elif total_portfolio_value >= 1000000:
            st.balloons()
            st.markdown("### 🎉 Congratulations! You've won the game! 🎉")
        st.markdown('</div>', unsafe_allow_html=True)

def display_portfolio():
    st.title("Your Portfolio")
    
    # Portfolio holdings
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Your Holdings")
    
    if st.session_state.portfolio:
        # Create a dataframe for better display
        portfolio_data = []
        for symbol, shares in st.session_state.portfolio.items():
            stock = st.session_state.game.stocks[symbol]
            value = shares * stock.price
            
            # Calculate change if possible
            change_pct = 0
            if len(stock.history) > 1:
                change_pct = (stock.price - stock.history[-2]) / stock.history[-2] * 100
            
            portfolio_data.append({
                'Symbol': symbol,
                'Name': stock.name,
                'Shares': shares,
                'Price': f"${stock.price:.2f}",
                'Value': f"${value:.2f}",
                'Change': f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
            })
        
        df = pd.DataFrame(portfolio_data)
        st.dataframe(df, use_container_width=True)
        
        # Portfolio composition pie chart
        values = [shares * st.session_state.game.stocks[symbol].price 
                 for symbol, shares in st.session_state.portfolio.items()]
        labels = list(st.session_state.portfolio.keys())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        
        fig.update_layout(
            title="Portfolio Composition",
            height=400,
            margin=dict(t=40, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔍 No stocks owned yet! Head to the Trading tab to start investing.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_trading():
    st.title("Trading Floor")
    
    # Market overview with all stocks
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Market Overview")
    
    # Create a dataframe of all stocks
    market_data = []
    for symbol, stock in st.session_state.game.stocks.items():
        # Calculate change if possible
        change_pct = 0
        if len(stock.history) > 1:
            change_pct = (stock.price - stock.history[-2]) / stock.history[-2] * 100
        
        market_data.append({
            'Symbol': symbol,
            'Name': stock.name,
            'Price': f"${stock.price:.2f}",
            'Change': f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%",
            'Trend': '📈' if change_pct >= 0 else '📉'
        })
    
    df = pd.DataFrame(market_data)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Selected stock details and chart
    stock = st.session_state.game.stocks[st.session_state.selected_stock]
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {stock.name} ({st.session_state.selected_stock})")
    st.markdown(f"Current Price: ${stock.price:.2f}")
    
    # Show stock chart
    st.plotly_chart(
        create_stock_chart(stock),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Trading instructions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### How to Trade")
    st.markdown("""
    1. Select a stock from the sidebar dropdown
    2. Use the sliders in the sidebar to set buy/sell quantities
    3. Click Execute Buy/Sell to complete your trade
    4. Click Next Trading Day to advance time and see market changes
    """)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
