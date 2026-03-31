import os
import pandas as pd
import yfinance as yf


# ==========================
# DOWNLOAD FUNCTION
# ==========================

def download_stock(stock, start_date, end_date, data_folder):
    ticker = f"{stock}.JK"
    print(f"Downloading {ticker}...")
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False
    )

    if df.empty:
        print(f"No data for {stock}")
        return

    df.reset_index(inplace=True)

    # ==========================
    # BASIC COLUMNS
    # ==========================

    df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
    }, inplace=True)

    # ==========================
    # MIN / MAX PRICE
    # ==========================

    df["min_price"] = df["low"]
    df["max_price"] = df["high"]

    # ==========================
    # AVERAGE PRICE
    # ==========================

    df["avg_price"] = (
        df["open"] +
        df["high"] +
        df["low"] +
        df["close"]
    ) / 4

    # ==========================
    # TYPICAL PRICE
    # ==========================

    df["typical_price"] = (
        df["high"] +
        df["low"] +
        df["close"]
    ) / 3

    # ==========================
    # GROWTH %
    # ==========================
    df["daily_growth_pct"] = df["close"].pct_change() * 100
    df["intraday_growth_pct"] = (df["close"] - df["open"]) / df["open"] * 100

    # ==========================
    # EXTRA ANALYSIS FEATURES
    # ==========================
    df["Extra_range_pct"] = (df["high"] - df["low"]) / df["low"] * 100
    df["Extra_volume_change_pct"] = df["volume"].pct_change() * 100
    df["Extra_price_change"] = df["close"] - df["open"]

    # ==========================
    # CSV FILE PATH
    # ==========================
    file_path = os.path.join(data_folder, f"{stock}.csv")

    # ==========================
    # SMART UPDATE
    # ==========================

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        combined = pd.concat([old_df, df])
        combined.drop_duplicates(subset=["date"], inplace=True)
        combined.sort_values("date", inplace=True)
        combined.to_csv(file_path, index=False)
        print(f"Updated {file_path}")

    else:
        df.to_csv(file_path, index=False)
        print(f"Created {file_path}")


# ==========================
# RUN FOR ALL STOCKS
# ==========================
def main():
    # ==========================
    # USER PARAMETERS
    # ==========================
    stocks = ['BBCA','BBRI','BMRI','BBNI','BJBR','BJTM',
                'ANTM','MDKA','HRTA','BRMS',
                'ADRO','PTBA','ITMG','GEMS','INDY',
                'MEDC','PGAS','AKRA',
                'TLKM','TOWR','MTEL',
                'UNTR','HEXA',
                'ICBP','INDF','KLBF','SIDO',
                'DMAS','DUTI',
                'ASII'
              ]  # Stock codes (auto add .JK)
    start_date = "2023-01-01"
    end_date = "2026-01-01"
    data_folder = "stocks_data"

    # ==========================
    # CREATE FOLDER
    # ==========================
    os.makedirs(data_folder, exist_ok=True)

    for stock in stocks:
        download_stock(stock, start_date, end_date, data_folder)
    print("Done.")

if __name__ == "__main__":
    main()

