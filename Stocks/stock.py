import yfinance as yf

def get_comprehensive_stock_info(ticker_symbol):
    """
    Fetch and analyze stock for the given ticker symbol, covering basic stock info, 
    financial metrics, extended info, and determine if it's a buy.
    """
    try:
        # Fetch stock info
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info

        # Basic Stock Info
        print("\n### Basic Stock Information ###")
        name = stock_info.get('longName', 'N/A')
        sector = stock_info.get('sector', 'N/A')
        current_price = stock_info.get('currentPrice', 'N/A')
        market_cap = stock_info.get('marketCap', 'N/A')
        print(f"Name: {name}")
        print(f"Sector: {sector}")
        print(f"Current Price: {current_price}")
        print(f"Market Cap: {market_cap}")

        # Key Financial Metrics
        pe_ratio = stock_info.get('trailingPE', None)
        pb_ratio = stock_info.get('priceToBook', None)
        revenue_growth = stock_info.get('revenueGrowth', None)
        profit_margin = stock_info.get('profitMargins', None)
        roe = stock_info.get('returnOnEquity', None)
        debt_to_equity = stock_info.get('debtToEquity', None)

        # Analyst Recommendations
        analyst_recommendations = stock_info.get('recommendationKey', 'N/A')

        # Assess valuation, growth, profitability, and risk
        buy_score = 0
        # Valuation Score
        if pe_ratio and pe_ratio < 15:
            buy_score += 3
        elif pe_ratio and pe_ratio < 25:
            buy_score += 2
        elif pe_ratio:
            buy_score += 1

        if pb_ratio and pb_ratio < 1:
            buy_score += 3
        elif pb_ratio and pb_ratio < 3:
            buy_score += 2
        elif pb_ratio:
            buy_score += 1

        # Growth Score
        if revenue_growth and revenue_growth > 0.1:
            buy_score += 3
        elif revenue_growth and revenue_growth > 0:
            buy_score += 2
        elif revenue_growth:
            buy_score += 1

        # Profitability Score
        if profit_margin and profit_margin > 0.2:
            buy_score += 3
        elif profit_margin and profit_margin > 0.1:
            buy_score += 2
        elif profit_margin:
            buy_score += 1

        if roe and roe > 0.15:
            buy_score += 3
        elif roe and roe > 0.1:
            buy_score += 2
        elif roe:
            buy_score += 1

        # Risk Score (Debt-to-Equity)
        if debt_to_equity and debt_to_equity < 0.5:
            buy_score += 3
        elif debt_to_equity and debt_to_equity < 1:
            buy_score += 2
        elif debt_to_equity:
            buy_score += 1

        # Analyst Sentiment
        if analyst_recommendations == 'buy':
            buy_score += 3
        elif analyst_recommendations == 'hold':
            buy_score += 2
        else:
            buy_score += 1

        # Extended Stock Information
        print("\n### Extended Stock Information ###")

        # Company Fundamentals
        revenue = stock_info.get('totalRevenue', 'N/A')
        net_income = stock_info.get('netIncomeToCommon', 'N/A')
        total_debt = stock_info.get('totalDebt', 'N/A')
        cash_flow = stock_info.get('freeCashflow', 'N/A')
        print("\n#### Company Fundamentals ####")
        print(f"Revenue: {revenue}")
        print(f"Net Income: {net_income}")
        print(f"Total Debt: {total_debt}")
        print(f"Free Cash Flow: {cash_flow}")

        # Industry Performance (general info based on sector)
        industry = stock_info.get('industry', 'N/A')
        print("\n#### Industry Performance ####")
        print(f"Sector: {sector}")
        print(f"Industry: {industry}")

        # Valuation Metrics
        dividend_yield = stock_info.get('dividendYield', 'N/A')
        print("\n#### Valuation Metrics ####")
        print(f"P/E Ratio: {pe_ratio}")
        print(f"P/B Ratio: {pb_ratio}")
        print(f"Dividend Yield: {dividend_yield}")

        # Management
        ceo_name = stock_info.get('ceo', 'N/A')
        ceo_tenure = stock_info.get('ceoTenure', 'N/A')
        print("\n#### Management ####")
        print(f"CEO: {ceo_name}")
        print(f"CEO Tenure: {ceo_tenure} years")

        # Market Sentiment (using recommendation key)
        print("\n#### Market Sentiment ####")
        print(f"Analyst Recommendations: {analyst_recommendations}")

        # Dividend Yield (additional information)
        payout_ratio = stock_info.get('payoutRatio', 'N/A')
        print("\n#### Dividend Yield ####")
        print(f"Payout Ratio: {payout_ratio}")

        # Risk (Beta)
        beta = stock_info.get('beta', 'N/A')
        print("\n#### Risk ####")
        print(f"Beta: {beta}")
        print(f"Debt-to-Equity Ratio: {debt_to_equity}")

        # Final Decision
        print("\n### Stock Analysis Summary ###")
        print(f"Buy Score: {buy_score}/21")
        if buy_score >= 15:
            print("Recommendation: Strong Buy")
        elif buy_score >= 10:
            print("Recommendation: Buy")
        else:
            print("Recommendation: Hold or Sell")

    except Exception as e:
        print(f"An error occurred: {e}")


# Main script execution
if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL, MSFT): ")
    get_comprehensive_stock_info(ticker)
