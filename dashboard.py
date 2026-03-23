import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data(ttl=3600)
def load_data():
    import os
    import yfinance as yf
    from fredapi import Fred
    from dotenv import load_dotenv
    
    load_dotenv()
    fred = Fred(api_key=os.getenv("FRED_API_KEY"))
    
    # Fetch fresh data directly
    nifty = yf.download("^NSEI", period="1y")["Close"]
    nifty.columns = ["Nifty50"]
    sp500 = yf.download("^GSPC", period="1y")["Close"]
    sp500.columns = ["SP500"]
    usdinr = yf.download("USDINR=X", period="1y")["Close"]
    usdinr.columns = ["USDINR"]
    us_bond = fred.get_series("DGS10", observation_start="2025-01-01")
    us_bond.name = "US_Bond_Yield"
    india_bond = fred.get_series("INDIRLTLT01STM", observation_start="2025-01-01")
    india_bond.name = "India_Bond_Yield"

    # Merge
    master = pd.concat([nifty, sp500, usdinr, us_bond], axis=1, sort=True)
    master["India_Bond_Yield"] = india_bond.reindex(master.index, method="ffill")
    master = master.dropna(how="all").ffill()

    # Moving averages
    master["Nifty50_MA50"] = master["Nifty50"].rolling(window=50).mean()
    master["SP500_MA50"] = master["SP500"].rolling(window=50).mean()
    master["Nifty50_MA200"] = master["Nifty50"].rolling(window=200).mean()
    master["SP500_MA200"] = master["SP500"].rolling(window=200).mean()
    master["Nifty50_Volatility"] = master["Nifty50"].rolling(window=30).std()
    master["SP500_Volatility"] = master["SP500"].rolling(window=30).std()

    # Giants
    indian_tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS",
        "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "M&M.NS", "MARUTI.NS",
        "SUNPHARMA.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "POWERGRID.NS",
        "NTPC.NS", "ONGC.NS", "BAJFINANCE.NS", "HCLTECH.NS", "TITAN.NS"
    ]
    us_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "BRK-B", "JPM",
        "JNJ", "XOM", "BAC", "WMT", "PG", "MA", "HD", "CVX", "ABBV",
        "MRK", "PFE", "KO", "PEP", "TSLA", "DIS", "NFLX", "BA"
    ]
    indian_giants = yf.download(indian_tickers, period="1y")["Close"].dropna(how="all").ffill()
    us_giants = yf.download(us_tickers, period="1y")["Close"].dropna(how="all").ffill()
    unicorns = pd.read_csv("unicorns.csv")

    return master, unicorns, indian_giants, us_giants

#Page config
st.set_page_config(page_title="Market Pulse India", layout="wide")
market, unicorns, indian_giants, us_giants = load_data()


# DISCLAIMER
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style="max-width:900px; margin:5px auto; background:#0d0d1a; 
                padding:40px; border-radius:10px; border:1px solid #ff4444;
                text-align:center; font-family:Arial;">
        <h1 style="color:white;">Market Pulse India</h1>
        <p style="color:#888; letter-spacing:2px;">
            FINANCIAL MARKETS, EXPLAINED FOR EVERYONE
        </p>
        <div style="background:rgba(255,68,68,0.1); border:1px solid rgba(255,68,68,0.3);
                    border-radius:12px; padding:20px; margin:25px 0; text-align:left;">
            <p style="color:#ff6666; font-weight:bold;">Important Disclaimer</p>
            <p style="color:#ccc; font-size:14px; line-height:1.8;">
                This dashboard is a student research project for educational purposes only.<br><br>
                Data from Yahoo Finance and FRED may be delayed or inaccurate.<br><br>
                Nothing here is financial advice or investment recommendations.<br><br>
                <span style="color:#ff4444;">Market Pulse India is NOT SEBI registered.</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("I Understand - Enter Dashboard", use_container_width=True):
            st.session_state.disclaimer_accepted = True
            st.rerun()
    st.stop()

# SIDEBAR
with st.sidebar:
    st.markdown("### Market Pulse India")
    st.markdown("---")
    st.markdown("**Mode**")
    mode = st.radio(
        "Select Mode",
        ["Select Mode", "Beginner", "Expert"],
        label_visibility="collapsed"
    )
    beginner = mode == "Beginner"
    st.markdown("---")
    st.markdown("**Navigate**")
    page = st.radio(
        "Go to",
        ["🏠 Home", "🇮🇳 Indian Markets", "🇺🇸 US Markets",
         "💱 Forex", "🔗 Cross Market", "🦄 Unicorns",
         "📰 News Feed", "💥 Market Crashes", "ℹ️ About"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    if mode == "Beginner":
        st.info("Beginner mode: Plain English explanations throughout.")
    elif mode == "Expert":
        st.info("Expert mode: Technical data and deeper analysis.")

# PAGE ROUTING
if page == "🏠 Home":
    st.markdown("""
    <div style="background:linear-gradient(135deg, #0d0d1a, #1a1a2e);
                padding:40px; border-radius:20px; margin-bottom:30px;
                text-align:center; font-family:Arial;">
        <h1 style="color:white; font-size:42px;">Market Pulse India</h1>
        <p style="color:#888; letter-spacing:3px; font-size:13px;">
            FINANCIAL MARKETS, EXPLAINED FOR EVERYONE
        </p>
        <p style="color:#ccc; font-size:16px; margin-top:20px; line-height:1.8;">
            Right now, markets across India and the US are moving.<br>
            Every number tells a story. This dashboard explains it simply.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Live Market Snapshot")
    col1, col2, col3, col4, col5 = st.columns(5)
    latest = market.iloc[-1]
    prev = market.iloc[-2]
    with col1:
        change = latest["Nifty50"] - prev["Nifty50"]
        st.metric("Nifty 50", f"{latest['Nifty50']:,.0f}", f"{change:+.0f}")
    with col2:
        change = latest["SP500"] - prev["SP500"]
        st.metric("S&P 500", f"{latest['SP500']:,.0f}", f"{change:+.0f}")
    with col3:
        change = latest["USDINR"] - prev["USDINR"]
        st.metric("USD/INR", f"{latest['USDINR']:.2f}", f"{change:+.3f}")
    with col4:
        st.metric("US Bond Yield", f"{latest['US_Bond_Yield']:.2f}%")
    with col5:
        st.metric("India Bond Yield", f"{latest['India_Bond_Yield']:.2f}%")

    if beginner:
        st.markdown("""
        <div style="background:rgba(255,153,51,0.1); border-left:3px solid #ff9933;
                    padding:15px; border-radius:8px; margin:10px 0;">
            <p style="color:#ccc; font-size:14px; margin:0; line-height:1.8;">
                <b style="color:#ff9933;">What am I looking at?</b><br><br>
                <b style="color:white;">Nifty 50</b> — India's top 50 companies combined. Higher = healthier.<br><br>
                <b style="color:white;">S&P 500</b> — America's top 500 companies. When this falls, global investors get nervous.<br><br>
                <b style="color:white;">USD/INR</b> — How many rupees buy 1 US dollar. Higher = rupee is weaker.<br><br>
                <b style="color:white;">US Bond Yield</b> — When this rises, stock markets usually fall.<br><br>
                <b style="color:white;">India Bond Yield</b> — Higher than US because India is a higher risk market.<br><br>
                <span style="color:#ff9933;">Green arrow = up today. Red arrow = down today.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── FEAR & GREED INDICATOR ──
    st.markdown("---")
    st.markdown("### Market Mood")
    
    volatility = market["Nifty50_Volatility"].iloc[-1]
    
    if volatility < 300:
        mood = "CALM"
        color = "#00cc44"
        score = 75
        desc = "Markets are stable. Low volatility means investors are confident."
    elif volatility < 600:
        mood = "CAUTIOUS"
        color = "#ffaa00"
        score = 45
        desc = "Markets are uncertain. Volatility is rising — watch carefully."
    else:
        mood = "PANIC"
        color = "#ff4444"
        score = 20
        desc = "Markets are in panic mode. High volatility = fear is driving decisions."

    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown(f"""
        <div style="background:#0d0d1a; border:2px solid {color};
                    border-radius:15px; padding:30px; text-align:center;">
            <h1 style="color:{color}; font-size:48px; margin:0;">{score}</h1>
            <h3 style="color:{color}; margin:5px 0;">{mood}</h3>
            <p style="color:#888; font-size:12px;">Market Mood Score / 100</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#0d0d1a; border:1px solid #333;
                    border-radius:15px; padding:30px;">
            <p style="color:#ccc; font-size:16px; line-height:1.8;">
                {desc}<br><br>
                <b style="color:white;">Current Nifty Volatility:</b> 
                <span style="color:{color};">{volatility:.0f}</span><br>
                <b style="color:white;">What this means:</b> 
                <span style="color:#aaa;">The market has been moving 
                {volatility:.0f} points up or down on average each day.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── DID YOU KNOW ──
    st.markdown("---")
    st.markdown("""
    <div style="background:linear-gradient(135deg, #0d0d1a, #1a1a2e);
                border:1px solid #333; border-radius:15px; padding:25px;">
        <h4 style="color:#ff9933; margin-bottom:15px;">Did You Know?</h4>
        <p style="color:#ccc; font-size:15px; line-height:1.8;">
            Nifty 50 and S&P 500 move together <b style="color:white;">72% of the time.</b>
            When the US market sneezes, India catches a cold — 
            foreign investors pull money out of both markets simultaneously.<br><br>
            The USD/INR has weakened by <b style="color:white;">~8.5%</b> in the last year — 
            from 86 to 93 rupees per dollar. That means your imports got 8.5% more expensive.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "🇮🇳 Indian Markets":
    st.markdown("## Indian Markets")
    
    if beginner:
        st.info("India's stock market is one of the fastest growing in the world. Nifty 50 tracks its 50 biggest companies.")
    
    # Nifty 50 chart with moving averages
    st.markdown("### Nifty 50 — Price & Moving Averages")
    fig = px.line(
        market.dropna(subset=["Nifty50"]),
        y=["Nifty50", "Nifty50_MA50", "Nifty50_MA200"],
        template="plotly_dark",
        color_discrete_map={
            "Nifty50": "#ff9933",
            "Nifty50_MA50": "#ffffff",
            "Nifty50_MA200": "#4a90d9"
        }
    )
    fig.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        hovermode="x unified",
        legend_title="Line"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if beginner:
        st.markdown("""
        <div style="background:rgba(255,153,51,0.1); border-left:3px solid #ff9933;
                    padding:12px; border-radius:8px;">
            <p style="color:#ccc; font-size:13px; margin:0;">
                <b style="color:#ff9933;">What are these lines?</b><br>
                Orange = actual daily Nifty price. 
                White = 50-day average (short term trend). 
                Blue = 200-day average (long term trend).<br>
                When orange is BELOW blue — market is in a downtrend.
                Right now Nifty is below its 200-day average — bearish signal.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # India Bond Yield
    st.markdown("### India 10Y Bond Yield")
    fig2 = px.line(
        market.dropna(subset=["India_Bond_Yield"]),
        y="India_Bond_Yield",
        template="plotly_dark",
        color_discrete_sequence=["#00cc44"]
    )
    fig2.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Indian Giants table
    # Indian Giants table
    st.markdown("### 25 Indian Giants — Latest Prices")
    
    # Get latest prices
    latest_prices = indian_giants.tail(1).T
    latest_prices.columns = ["Latest Price (INR)"]
    latest_prices.index = latest_prices.index.str.replace(".NS", "").str.replace(".BO", "")
    latest_prices["Latest Price (INR)"] = latest_prices["Latest Price (INR)"].round(2)
    
    st.dataframe(
        latest_prices,
        use_container_width=True,
        column_config={
            "Latest Price (INR)": st.column_config.NumberColumn(
                "Latest Price (INR)",
                format="₹%.2f"
            )
        }
    )

elif page == "🇺🇸 US Markets":
    st.markdown("## US Markets")
    
    if beginner:
        st.info("The US stock market is the largest in the world. What happens here affects every market globally.")

    # S&P 500 chart
    st.markdown("### S&P 500 — Price & Moving Averages")
    fig = px.line(
        market.dropna(subset=["SP500"]),
        y=["SP500", "SP500_MA50", "SP500_MA200"],
        template="plotly_dark",
        color_discrete_map={
            "SP500": "#4a90d9",
            "SP500_MA50": "#ffffff",
            "SP500_MA200": "#ff9933"
        }
    )
    fig.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # US Bond Yield
    st.markdown("### US 10Y Bond Yield")
    fig2 = px.line(
        market.dropna(subset=["US_Bond_Yield"]),
        y="US_Bond_Yield",
        template="plotly_dark",
        color_discrete_sequence=["#4a90d9"]
    )
    fig2.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # US Giants table
    st.markdown("### 25 US Giants — Latest Prices")
    latest_us = us_giants.tail(1).T
    latest_us.columns = ["Latest Price (USD)"]
    latest_us["Latest Price (USD)"] = latest_us["Latest Price (USD)"].round(2)
    st.dataframe(
        latest_us,
        use_container_width=True,
        column_config={
            "Latest Price (USD)": st.column_config.NumberColumn(
                "Latest Price (USD)",
                format="$%.2f"
            )
        }
    )

elif page == "💱 Forex":
    st.markdown("## Forex — Currency Markets")

    if beginner:
        st.info("Forex shows how currencies trade against each other. USD/INR tells you how many rupees equal 1 US dollar.")

    # USD/INR chart
    st.markdown("### USD/INR — Last 1 Year")
    fig = px.line(
        market.dropna(subset=["USDINR"]),
        y="USDINR",
        template="plotly_dark",
        color_discrete_sequence=["#ff9933"]
    )
    fig.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        hovermode="x unified",
        yaxis_title="Rupees per 1 USD"
    )
    fig.add_hline(
        y=market["USDINR"].mean(),
        line_dash="dash",
        line_color="white",
        annotation_text="1 Year Average"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Key stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Rate", f"₹{market['USDINR'].iloc[-1]:.2f}")
    with col2:
        st.metric("1 Year Low", f"₹{market['USDINR'].min():.2f}")
    with col3:
        st.metric("1 Year High", f"₹{market['USDINR'].max():.2f}")

    if beginner:
        st.markdown("""
        <div style="background:rgba(255,153,51,0.1); border-left:3px solid #ff9933;
                    padding:12px; border-radius:8px; margin-top:15px;">
            <p style="color:#ccc; font-size:13px; margin:0; line-height:1.8;">
                <b style="color:#ff9933;">What does this mean?</b><br>
                The rupee has weakened from ~86 to ~93 in one year — an 8.5% drop.
                This means everything India imports (oil, electronics, machinery) 
                got 8.5% more expensive. But Indian IT companies earned 8.5% more 
                rupees on the same dollar revenue.
            </p>
        </div>
        """, unsafe_allow_html=True)

elif page == "🔗 Cross Market":
    st.markdown("## Cross Market Analysis")

    if beginner:
        st.info("This page shows how different markets around the world affect each other. This is the most powerful section of the dashboard.")

    # Nifty vs S&P chart
    st.markdown("### Nifty 50 vs S&P 500 — Do they move together?")
    fig = px.line(
        market.dropna(subset=["Nifty50", "SP500"]),
        y=["Nifty50", "SP500"],
        template="plotly_dark",
        color_discrete_map={
            "Nifty50": "#ff9933",
            "SP500": "#4a90d9"
        }
    )
    fig.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.markdown("### Correlation Matrix — How markets relate")
    corr = market[["Nifty50", "SP500", "USDINR", "US_Bond_Yield", "India_Bond_Yield"]].corr()
    fig2 = px.imshow(
        corr.round(2),
        template="plotly_dark",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        text_auto=True
    )
    fig2.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a"
    )
    st.plotly_chart(fig2, use_container_width=True)

    if beginner:
        st.markdown("""
        <div style="background:rgba(255,153,51,0.1); border-left:3px solid #ff9933;
                    padding:12px; border-radius:8px;">
            <p style="color:#ccc; font-size:13px; margin:0; line-height:1.8;">
                <b style="color:#ff9933;">How to read this heatmap?</b><br>
                Dark blue = markets move together strongly.<br>
                Dark red = markets move in opposite directions.<br>
                White = no relationship.<br><br>
                Key finding: Nifty50 and SP500 score 0.72 — they move together 
                strongly. When US sneezes, India catches a cold!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Volatility comparison
    st.markdown("### Volatility — Which market is more nervous?")
    fig3 = px.line(
        market.dropna(subset=["Nifty50_Volatility", "SP500_Volatility"]),
        y=["Nifty50_Volatility", "SP500_Volatility"],
        template="plotly_dark",
        color_discrete_map={
            "Nifty50_Volatility": "#ff9933",
            "SP500_Volatility": "#4a90d9"
        }
    )
    fig3.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        hovermode="x unified"
    )
    st.plotly_chart(fig3, use_container_width=True)

elif page == "🦄 Unicorns":
    st.markdown("## Unicorn Tracker")

    if beginner:
        st.info("Unicorns are private startups valued at $1 billion or more. They are NOT listed on any stock exchange — their value comes from investor funding rounds.")

    # India vs US comparison
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Indian Unicorns Tracked", "10")
    with col2:
        st.metric("US Unicorns Tracked", "10")

    # Valuation bar chart
    st.markdown("### Valuation Comparison — India vs US")
    fig = px.bar(
        unicorns.sort_values("valuation_billion_usd", ascending=True),
        x="valuation_billion_usd",
        y="name",
        color="country",
        orientation="h",
        template="plotly_dark",
        color_discrete_map={"India": "#ff9933", "USA": "#4a90d9"},
        labels={"valuation_billion_usd": "Valuation ($ Billion)", "name": "Company"}
    )
    fig.update_layout(
        plot_bgcolor="#0d0d1a",
        paper_bgcolor="#0d0d1a",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # Sector breakdown
    st.markdown("### Sector Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Indian Unicorns")
        india_u = unicorns[unicorns["country"] == "India"]
        fig2 = px.pie(
            india_u,
            values="valuation_billion_usd",
            names="sector",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        fig2.update_layout(paper_bgcolor="#0d0d1a")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("#### US Unicorns")
        us_u = unicorns[unicorns["country"] == "USA"]
        fig3 = px.pie(
            us_u,
            values="valuation_billion_usd",
            names="sector",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig3.update_layout(paper_bgcolor="#0d0d1a")
        st.plotly_chart(fig3, use_container_width=True)

    # Full table
    st.markdown("### Full Unicorn Data")
    st.dataframe(
        unicorns.sort_values("valuation_billion_usd", ascending=False),
        use_container_width=True
    )

elif page == "📰 News Feed":
    st.markdown("## Market News Feed")

    if beginner:
        st.info("Latest financial news affecting Indian and global markets.")

    st.markdown("""
    <div style="background:#0d0d1a; border:1px solid #333;
                border-radius:15px; padding:25px; text-align:center;">
        <h3 style="color:#ff9933;">Coming Soon</h3>
        <p style="color:#888;">
            Live news feed will be connected via NewsAPI in the next version.<br>
            It will show real-time headlines for Nifty, S&P 500, RBI, Fed, and Forex.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # For now show key market links
    st.markdown("### Key Market Resources")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Indian Markets**
        - [NSE India](https://www.nseindia.com)
        - [BSE India](https://www.bseindia.com)
        - [RBI](https://www.rbi.org.in)
        - [SEBI](https://www.sebi.gov.in)
        """)
    with col2:
        st.markdown("""
        **Global Markets**
        - [Yahoo Finance](https://finance.yahoo.com)
        - [FRED Economic Data](https://fred.stlouisfed.org)
        - [Bloomberg](https://www.bloomberg.com)
        - [Reuters](https://www.reuters.com)
        """)

elif page == "💥 Market Crashes":
    st.markdown("## Historical Market Crashes")

    if beginner:
        st.info("Every few years markets crash — here's what happened, why, and how India was affected each time.")

    crashes = [
        {
            "year": "2008",
            "name": "Global Financial Crisis",
            "cause": "US housing market collapse. Lehman Brothers went bankrupt.",
            "sp500": "-56%",
            "nifty": "-60%",
            "color": "#ff4444"
        },
        {
            "year": "2015-16",
            "name": "China Market Crash",
            "cause": "Chinese stock market bubble burst. Global panic followed.",
            "sp500": "-14%",
            "nifty": "-26%",
            "color": "#ff8800"
        },
        {
            "year": "2020",
            "name": "COVID-19 Crash",
            "cause": "Global pandemic. Fastest crash in market history — 34% in 33 days.",
            "sp500": "-34%",
            "nifty": "-38%",
            "color": "#ff4444"
        },
        {
            "year": "2022",
            "name": "Rate Hike Selloff",
            "cause": "US Fed raised rates aggressively to fight inflation. Bonds became attractive.",
            "sp500": "-25%",
            "nifty": "-17%",
            "color": "#ff8800"
        },
        {
            "year": "2025-26",
            "name": "Current Downturn",
            "cause": "Global uncertainty, high US yields, rupee weakness pulling FII money out of India.",
            "sp500": "-8%",
            "nifty": "-14%",
            "color": "#ffaa00"
        }
    ]

    for crash in crashes:
        st.markdown(f"""
        <div style="background:#0d0d1a; border:1px solid {crash['color']};
                    border-left:4px solid {crash['color']};
                    border-radius:12px; padding:20px; margin-bottom:15px;">
            <h3 style="color:{crash['color']}; margin:0;">
                {crash['year']} — {crash['name']}
            </h3>
            <p style="color:#ccc; margin:10px 0;">{crash['cause']}</p>
            <span style="color:#ff4444; margin-right:20px;">
                S&P 500: {crash['sp500']}
            </span>
            <span style="color:#ff9933;">
                Nifty 50: {crash['nifty']}
            </span>
        </div>
        """, unsafe_allow_html=True)

    if beginner:
        st.markdown("""
        <div style="background:rgba(255,153,51,0.1); border-left:3px solid #ff9933;
                    padding:12px; border-radius:8px; margin-top:15px;">
            <p style="color:#ccc; font-size:13px; margin:0; line-height:1.8;">
                <b style="color:#ff9933;">Key pattern:</b> Every time the US market 
                crashes, India crashes too — usually by a bigger percentage. 
                This is because foreign investors sell Indian stocks first when 
                they need emergency cash.
            </p>
        </div>
        """, unsafe_allow_html=True)

elif page == "ℹ️ About":
    st.markdown("## About Market Pulse India")

    st.markdown("""
    <div style="background:#0d0d1a; border:1px solid #333;
                border-radius:15px; padding:30px; margin-bottom:20px;">
        <h3 style="color:#ff9933;">The Project</h3>
        <p style="color:#ccc; line-height:1.8;">
            Market Pulse India is a personal portfolio project built to track 
            and visualize cross-market trends across Indian equities, US equities, 
            forex, debt markets, and unicorn valuations — all in one place.<br><br>
            It was a personal project by me as i wanted to understand how global markets are interconnected and how they affect each other within the context of India. I wanted to create a simple, visually appealing dashboard that anyone could use to get a quick pulse on the markets without needing to read complex financial news or analysis.
            It's built using Python, Streamlit, and Plotly, and pulls data from Yahoo Finance and FRED. The goal is to make financial markets more accessible and understandable for everyone — whether you're a beginner or an expert.
            I got to learn so many thing on my way — from data fetching and cleaning to interactive visualizations and UI design. It was a fun and rewarding journey, and I'm excited to keep improving the dashboard with more features and data in the future!
            I took help from AI tools like ChatGPT to brainstorm ideas, write code snippets, and debug issues. But the overall vision, design, and implementation were entirely my own work. I wanted to create something that reflects my personal style and approach to data storytelling — simple, clear, and visually engaging.
        </p>
    </div>

    <div style="background:#0d0d1a; border:1px solid #333;
                border-radius:15px; padding:30px; margin-bottom:20px;">
        <h3 style="color:#ff9933;">Data Sources</h3>
        <p style="color:#ccc; line-height:1.8;">
            - Yahoo Finance (via yfinance) — Stock prices, forex, indices<br>
            - FRED (US Federal Reserve) — Bond yields, macro data<br>
            - Manual research — Unicorn valuations and sectors
        </p>
    </div>

    <div style="background:#0d0d1a; border:1px solid #333;
                border-radius:15px; padding:30px; margin-bottom:20px;">
        <h3 style="color:#ff9933;">Tech Stack</h3>
        <p style="color:#ccc; line-height:1.8;">
            - Python 3.13<br>
            - pandas — Data manipulation<br>
            - yfinance — Market data fetching<br>
            - fredapi — Economic data<br>
            - plotly — Interactive charts<br>
            - streamlit — Dashboard framework
        </p>
    </div>

    <div style="background:#0d0d1a; border:1px solid #333;
                border-radius:15px; padding:30px; margin-bottom:20px;">
        <h3 style="color:#ff9933;">Key Findings</h3>
        <p style="color:#ccc; line-height:1.8;">
            1. Nifty 50 and S&P 500 are 72% correlated — global markets move together<br>
            2. USD/INR has weakened 8.5% in 1 year — rupee at historic lows<br>
            3. Market volatility has doubled in March 2026 — panic mode active<br>
            4. US bond yields rising while Indian markets falling — classic signal
        </p>
    </div>

    <div style="background:rgba(255,68,68,0.1); border:1px solid rgba(255,68,68,0.3);
                border-radius:15px; padding:20px;">
        <p style="color:#ff6666; font-size:13px; margin:0; line-height:1.8;">
            <b>Disclaimer:</b> This is a student research project for educational 
            purposes only. Not financial advice. Not SEBI registered. 
            Data may be delayed or inaccurate.
        </p>
    </div>
                
    """, unsafe_allow_html=True)
    # FOOTER MARQUEE
st.markdown("---")
nifty_val = market["Nifty50"].iloc[-1]
sp500_val = market["SP500"].iloc[-1]
usdinr_val = market["USDINR"].iloc[-1]
us_bond_val = market["US_Bond_Yield"].iloc[-1]
india_bond_val = market["India_Bond_Yield"].iloc[-1]

st.markdown(f"""
<div style="background:#0d0d1a; padding:10px; border-radius:8px;
            border:1px solid #333; overflow:hidden;">
    <marquee behavior="scroll" direction="left" scrollamount="4"
             style="color:#ff9933; font-family:monospace; font-size:14px;">
        Nifty 50: {nifty_val:,.0f} &nbsp;|&nbsp;
        S&P 500: {sp500_val:,.0f} &nbsp;|&nbsp;
        USD/INR: {usdinr_val:.2f} &nbsp;|&nbsp;
        US Bond: {us_bond_val:.2f}% &nbsp;|&nbsp;
        India Bond: {india_bond_val:.2f}% &nbsp;|&nbsp;
        Market Pulse India — Financial markets, explained for everyone.
    </marquee>
</div>
""", unsafe_allow_html=True)
