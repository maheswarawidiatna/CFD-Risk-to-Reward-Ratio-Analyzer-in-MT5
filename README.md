# MT5 Retracement and Risk-Reward Ratio Analyzer

![Python](https://img.shields.io/badge/Python-3.10-green.svg)
![MetaTrader5](https://img.shields.io/badge/MetaTrader5-Compatible-blue.svg)

This Python script is designed for analyzing retracement and risk-reward ratios (RRR) using MetaTrader 5 (MT5) historical price data. It utilizes the `MetaTrader5` library for data retrieval, `numpy` for mathematical operations, `pandas` for data manipulation, and `seaborn` and `matplotlib` for visualization.

## Prerequisites

1. **MetaTrader 5 Platform:**
   Ensure you have the MetaTrader 5 platform installed and configured. The script uses the `MetaTrader5` library, which is compatible with MT5.

2. **Python Libraries:**
   Install the required Python libraries using the following command:
   ```bash
   pip install MetaTrader5 numpy pandas seaborn matplotlib
   ```

## Usage

1. **Initialize MT5:**
   Make sure to initialize the MetaTrader 5 connection by running the script in an environment where MT5 is accessible.

2. **Configuration:**
   - Modify the `All_instrument` list to include the financial instruments you want to analyze (e.g., `["XAUUSD", "GBPUSD", "EURUSD", "USDJPY"]`).
   - Customize the `All_TF` list to include the desired timeframes (e.g., `["M1", "M5", "H1", "D1"]`).
   - Adjust the `batch` variable to set the number of data points per collection.

3. **Run the Script:**
   Execute the script, and it will compute expected retracement and suggested RRR tables for each instrument and timeframe combination.

4. **Results:**
   - The script will display the expected retracement and suggested RRR tables in the console, below is the example suggested RRR tables of XAUUSD.

   ![12](https://github.com/maheswarawidiatna/CFD-Risk-to-Reward-Ratio-Analyzer-in-MT5/assets/94330691/05c83c77-21f8-4f22-bcc2-d97819ac8741)

   - Heatmaps of the results will be generated and shown using `seaborn` and `matplotlib`.

5. **Analysis:**
   Interpret the heatmaps to identify potential entry and closing timeframes, as well as the suggested RRR values.

## Note

- The script uses historical price data from MetaTrader 5, and the results are based on the specified financial instruments and timeframes.
- Ensure that you have a stable connection to the MetaTrader 5 platform while running the script.

Feel free to customize the script to meet your specific requirements and integrate it into your trading analysis workflow.

---

*Note: This script is designed for educational purposes, and users are responsible for understanding and adhering to any trading regulations and risks associated with financial markets.*
