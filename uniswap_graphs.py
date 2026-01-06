import matplotlib.pyplot as plt
import numpy as np

def uniswap_v3_value(P_current, P_a, P_b, Investment_Value, P_entry):
    """
    Calculates the value of a Uniswap v3 position relative to the initial investment.
    Using simplified formulas for visual comparison.
    """
    # Calculate Liquidity L based on initial investment at P_entry
    sqrt_Pa = np.sqrt(P_a)
    sqrt_Pb = np.sqrt(P_b)
    sqrt_P_entry = np.sqrt(P_entry)

    # Determine initial x (ETH) and y (USDC) amounts at entry
    if P_entry <= P_a:
        x_init = Investment_Value / P_entry
        y_init = 0
        L = x_init * (sqrt_Pa * sqrt_Pb) / (sqrt_Pb - sqrt_Pa)
    elif P_entry >= P_b:
        x_init = 0
        y_init = Investment_Value
        L = y_init / (sqrt_Pb - sqrt_Pa)
    else:
        # In range calculation is complex for fixed Investment Value,
        # simplifying by assuming we derive L from the "virtual" amounts needed.
        # This is a visual approximation.
        # L derived from y portion:
        L = Investment_Value / ( (sqrt_P_entry - sqrt_Pa) + (1/sqrt_P_entry - 1/sqrt_Pb)*P_entry )

    # Calculate Value at Current Price P_current
    sqrt_P = np.sqrt(P_current)

    values = []
    for p, sp in zip(P_current, sqrt_P):
        if p <= P_a:
            # Position is all ETH
            val = L * (1/sqrt_Pa - 1/sqrt_Pb) * p # Wait, this is effectively x_max * p
            # Correction: Real x is L * (1/sqrt_Pa - 1/sqrt_Pb)
            val = L * ( (sqrt_Pb - sqrt_Pa) / (sqrt_Pa * sqrt_Pb) ) * p
        elif p >= P_b:
            # Position is all USDC
            val = L * (sqrt_Pb - sqrt_Pa)
        else:
            # Position is Mix
            val = L * (sp - sqrt_Pa) + L * (1/sp - 1/sqrt_Pb) * p
        values.append(val)
    return np.array(values)

def cash_secured_put_value(prices, strike, investment):
    # If price < strike, we own the asset (value = price * quantity)
    # If price > strike, we own cash (value = strike * quantity)
    # Quantity = investment / strike
    quantity = investment / strike
    return np.minimum(prices, strike) * quantity

def short_straddle_pnl(prices, strike, premium):
    # Payoff = Premium - abs(Price - Strike)
    return premium - np.abs(prices - strike)

# --- Plot 1: Short Put vs Uniswap v3 ---
prices = np.linspace(1500, 3000, 500)
strike = 2500
range_lower = 2000
range_upper = 2500
investment = 10000

# Value of Cash Secured Put (Strike 2500)
put_vals = cash_secured_put_value(prices, strike, investment)

# Value of Uniswap Position (Range 2000-2500, Entry at 2500 i.e., all USDC)
# This mimics "Sold Put" because we start with USDC and buy ETH as it drops.
uni_vals = uniswap_v3_value(prices, range_lower, range_upper, investment, P_entry=2500)

plt.figure(figsize=(10, 6))
plt.plot(prices, put_vals, label='Standard Cash-Secured Put (Strike $2500)', linestyle='--', color='blue')
plt.plot(prices, uni_vals, label='Uniswap v3 Position ($2000-$2500)', color='orange', linewidth=2.5)
plt.title('Comparison: Uniswap v3 Range vs. Cash-Secured Put')
plt.xlabel('ETH Price ($)')
plt.ylabel('Position Value ($)')
plt.axvline(x=2500, color='gray', linestyle=':', label='Strike/Upper Tick')
plt.axvline(x=2000, color='gray', linestyle=':', label='Lower Tick')
plt.legend()
plt.grid(True, alpha=0.3)
plt.annotate('Linear Loss', xy=(1800, 7200), xytext=(1600, 8500), arrowprops=dict(facecolor='blue', shrink=0.05))
plt.annotate('Convex Loss (Curved)', xy=(2200, 9200), xytext=(2100, 7500), arrowprops=dict(facecolor='orange', shrink=0.05))
plt.savefig('/home/user/scratch/plot1_uniswap_vs_put.png', dpi=150, bbox_inches='tight')
print("Plot 1 saved to plot1_uniswap_vs_put.png")

# --- Plot 2: Short Straddle vs Uniswap v3 PnL ---
# Comparison centered at 2000
center_price = 2000
prices_2 = np.linspace(1500, 2500, 500)
range_width = 400 # Range 1800-2200
uni_straddle_vals = uniswap_v3_value(prices_2, center_price - range_width/2, center_price + range_width/2, investment, P_entry=center_price)

# Calculate HODL 50/50 value (Benchmark for IL)
# HODL 50/50 means we held the initial X and Y amounts from the entry.
# At entry 2000 (mid range), we hold approx 50/50.
# We calculate exact amounts at entry to benchmark properly.
# (Recalculating L for correct initial mix)
sqrt_Pa_2 = np.sqrt(center_price - range_width/2)
sqrt_Pb_2 = np.sqrt(center_price + range_width/2)
sqrt_P_entry_2 = np.sqrt(center_price)
L_2 = investment / ( (sqrt_P_entry_2 - sqrt_Pa_2) + (1/sqrt_P_entry_2 - 1/sqrt_Pb_2)*center_price )
x_hodl = L_2 * (1/sqrt_P_entry_2 - 1/sqrt_Pb_2)
y_hodl = L_2 * (sqrt_P_entry_2 - sqrt_Pa_2)
hodl_vals = y_hodl + x_hodl * prices_2

# Uniswap PnL relative to entry (Capital Value Change)
# Note: This does not include Fees.
uni_pnl = uni_straddle_vals - investment

# Standard Straddle PnL (Approximation for visual shape)
# Premium is arbitrary for visual comparison, setting to match peak of Uniswap (which is 0 IL at center)
# Actually, Straddle has linear loss. Uniswap has curved loss (IL).
# To compare shapes, we shift Straddle to start at 0 PnL at center (ignoring premium for moment to show risk shape)
straddle_pnl = -np.abs(prices_2 - center_price) * (investment / center_price) # Normalized slope

plt.figure(figsize=(10, 6))
plt.plot(prices_2, uni_pnl, label='Uniswap v3 PnL (Impermanent Loss only)', color='orange', linewidth=2.5)
plt.plot(prices_2, straddle_pnl, label='Standard Straddle PnL (Linear Risk)', linestyle='--', color='blue')
plt.title('Risk Profile: Uniswap v3 vs. Short Straddle')
plt.xlabel('ETH Price ($)')
plt.ylabel('Profit/Loss vs Entry ($)')
plt.axvline(x=center_price, color='gray', linestyle=':', label='Entry Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.annotate('Rounded Top (Gamma)', xy=(2000, 0), xytext=(2100, 50), arrowprops=dict(facecolor='orange', shrink=0.05))
plt.annotate('Sharp Peak', xy=(2000, 0), xytext=(1900, -200), arrowprops=dict(facecolor='blue', shrink=0.05))
plt.savefig('/home/user/scratch/plot2_uniswap_vs_straddle.png', dpi=150, bbox_inches='tight')
print("Plot 2 saved to plot2_uniswap_vs_straddle.png")
