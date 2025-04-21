

# Stock Trading Simulator

A realistic stock market trading simulator built with Streamlit that allows users to practice trading strategies in a risk-free environment.

## Features

- Real-time stock price simulation with volatility and trends
- Portfolio management with buy/sell capabilities
- Interactive charts and visualizations
- Market news events generated with AI
- Progress tracking with milestones
- Responsive, modern UI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Stock\ Game
```

2. Install the required dependencies:
```bash
pip install streamlit pandas plotly numpy openai
```

3. Set up your OpenAI API key:
   - Create a `.streamlit` directory in the project folder:
   ```bash
   mkdir -p .streamlit
   ```
   - Create a `secrets.toml` file inside the `.streamlit` directory:
   ```bash
   touch .streamlit/secrets.toml
   ```
   - Add your OpenAI API key to the `secrets.toml` file:
   ```toml
   openai_api_key = "your-actual-api-key"
   ```
   **Important**: Replace "your-actual-api-key" with your real OpenAI API key. This is required for the market news generation feature.

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. The application will open in your default web browser.

3. How to play:
   - Start with $10,000 in virtual cash
   - Use the sidebar to navigate between Dashboard, Portfolio, and Trading views
   - Select stocks to view their performance charts
   - Buy and sell shares using the sliders in the Trading tab
   - Advance to the next trading day to see market changes
   - Try to reach the milestones and become a virtual millionaire!

## Game Mechanics

- Each stock has its own volatility and trend characteristics
- Market events affect stock prices
- AI-generated news provides context for market movements
- Progress through financial milestones from $100K to $1M

## Tips for Success

- Diversify your portfolio to manage risk
- Pay attention to market news events
- Look for patterns in stock price movements
- Use the trend channels to identify potential buy/sell points
- Be patient and think long-term

## License

[MIT License](LICENSE)

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Market events powered by [OpenAI](https://openai.com/)
- Visualizations created with [Plotly](https://plotly.com/)
```
