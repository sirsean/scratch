import matplotlib.pyplot as plt
import numpy as np

def uniswap_v3_value(P_current, P_a, P_b, Investment_Value, P_entry):
    """
    Calculates the value of a Uniswap v3 position relative to the initial investment.
    """
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
        # In range
        L = Investment_Value / ( (sqrt_P_entry - sqrt_Pa) + (1/sqrt_P_entry - 1/sqrt_Pb)*P_entry )

    # Calculate Value at Current Price P_current
    sqrt_P = np.sqrt(P_current)

    values = []
    for p, sp in zip(P_current, sqrt_P):
        if p <= P_a:
            # Position is all ETH
            val = L * ( (sqrt_Pb - sqrt_Pa) / (sqrt_Pa * sqrt_Pb) ) * p
        elif p >= P_b:
            # Position is all USDC
            val = L * (sqrt_Pb - sqrt_Pa)
        else:
            # Position is Mix
            val = L * (sp - sqrt_Pa) + L * (1/sp - 1/sqrt_Pb) * p
        values.append(val)

    return np.array(values), L

def get_initial_amounts(L, P_entry, P_a, P_b):
    """Get initial ETH and USDC amounts for a position"""
    sqrt_Pa = np.sqrt(P_a)
    sqrt_Pb = np.sqrt(P_b)
    sqrt_P_entry = np.sqrt(P_entry)

    if P_entry <= P_a:
        x_init = L * (sqrt_Pb - sqrt_Pa) / (sqrt_Pa * sqrt_Pb)
        y_init = 0
    elif P_entry >= P_b:
        x_init = 0
        y_init = L * (sqrt_Pb - sqrt_Pa)
    else:
        x_init = L * (1/sqrt_P_entry - 1/sqrt_Pb)
        y_init = L * (sqrt_P_entry - sqrt_Pa)

    return x_init, y_init

def short_strangle_value(prices, put_strike, call_strike, entry_price, investment):
    """
    Short strangle: Sell put at lower strike + sell call at upper strike
    Start with 50/50 position in assets, value changes based on option payoffs
    For visualization, we'll show the position value similar to LP
    """
    # Initial position: 50/50 split
    eth_amount = investment / (2 * entry_price)
    usdc_amount = investment / 2

    values = []
    for p in prices:
        # Base value of holdings
        base_value = eth_amount * p + usdc_amount

        # Short put payoff (we owe money if price < put_strike)
        if p < put_strike:
            put_loss = (put_strike - p) * (investment / (2 * entry_price))
        else:
            put_loss = 0

        # Short call payoff (we owe money if price > call_strike)
        if p > call_strike:
            call_loss = (p - call_strike) * (investment / (2 * entry_price))
        else:
            call_loss = 0

        values.append(base_value - put_loss - call_loss)

    return np.array(values)

def bull_put_spread_value(prices, short_put_strike, long_put_strike, entry_price, investment):
    """
    Bull Put Spread: Sell put at higher strike + buy put at lower strike
    Defined risk strategy - profit if price stays above short strike
    """
    values = []
    max_profit = investment  # Assume we collected this much in net premium (simplified)
    max_loss_width = short_put_strike - long_put_strike

    for p in prices:
        if p >= short_put_strike:
            # Above short strike: keep all premium
            val = max_profit
        elif p <= long_put_strike:
            # Below long strike: max loss
            val = max_profit - max_loss_width * (investment / short_put_strike)
        else:
            # Between strikes: linear loss
            loss = (short_put_strike - p) * (investment / short_put_strike)
            val = max_profit - loss
        values.append(val)

    return np.array(values)

def bear_call_spread_value(prices, short_call_strike, long_call_strike, entry_price, investment):
    """
    Bear Call Spread: Sell call at lower strike + buy call at higher strike
    Defined risk strategy - profit if price stays below short strike
    """
    values = []
    max_profit = investment
    max_loss_width = long_call_strike - short_call_strike

    for p in prices:
        if p <= short_call_strike:
            # Below short strike: keep all premium
            val = max_profit
        elif p >= long_call_strike:
            # Above long strike: max loss
            val = max_profit - max_loss_width * (investment / short_call_strike)
        else:
            # Between strikes: linear loss
            loss = (p - short_call_strike) * (investment / short_call_strike)
            val = max_profit - loss
        values.append(val)

    return np.array(values)

def collar_value(prices, put_strike, call_strike, entry_price, investment):
    """
    Collar: Own ETH + buy protective put + sell covered call
    Bounded position with defined min and max values
    """
    eth_amount = investment / entry_price

    values = []
    for p in prices:
        if p <= put_strike:
            # Protected by long put
            val = put_strike * eth_amount
        elif p >= call_strike:
            # Capped by short call
            val = call_strike * eth_amount
        else:
            # In between: track ETH price
            val = p * eth_amount
        values.append(val)

    return np.array(values)

# ========================================================================
# GRAPH D: Short Strangle vs LP
# ========================================================================
print("Generating Graph D: Short Strangle vs LP...")

prices_D = np.linspace(1500, 2500, 500)
put_strike_D = 1800
call_strike_D = 2200
entry_price_D = 2000
investment_D = 10000

# LP Position with same range as strangle strikes
lp_vals_D, L_D = uniswap_v3_value(prices_D, put_strike_D, call_strike_D, investment_D, entry_price_D)

# Short Strangle
strangle_vals_D = short_strangle_value(prices_D, put_strike_D, call_strike_D, entry_price_D, investment_D)

# Calculate PnL (relative to investment)
lp_pnl_D = lp_vals_D - investment_D
strangle_pnl_D = strangle_vals_D - investment_D

plt.figure(figsize=(12, 7))
plt.plot(prices_D, strangle_pnl_D, label=f'Short Strangle (Put ${put_strike_D} / Call ${call_strike_D})',
         linestyle='--', color='red', linewidth=2)
plt.plot(prices_D, lp_pnl_D, label=f'Uniswap v3 LP (${put_strike_D}-${call_strike_D})',
         color='orange', linewidth=2.5)

plt.title('Comparison: Short Strangle vs Uniswap v3 LP', fontsize=14, fontweight='bold')
plt.xlabel('ETH Price ($)', fontsize=12)
plt.ylabel('Profit/Loss vs Entry ($)', fontsize=12)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=0.8)
plt.axvline(x=entry_price_D, color='gray', linestyle=':', alpha=0.7, label=f'Entry Price (${entry_price_D})')
plt.axvline(x=put_strike_D, color='orange', linestyle=':', alpha=0.5)
plt.axvline(x=call_strike_D, color='orange', linestyle=':', alpha=0.5)

plt.axvspan(put_strike_D, call_strike_D, alpha=0.1, color='orange', label='LP Active Range')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.annotate('Both lose when\nprice moves away',
             xy=(1650, lp_pnl_D[np.argmin(np.abs(prices_D - 1650))]),
             xytext=(1550, -500),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('Strangle: Linear losses\nLP: Curved losses',
             xy=(2300, lp_pnl_D[np.argmin(np.abs(prices_D - 2300))]),
             xytext=(2200, -800),
             fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_D_short_strangle_vs_lp.png', dpi=150, bbox_inches='tight')
print("✓ Graph D saved to plot_D_short_strangle_vs_lp.png")

# ========================================================================
# GRAPH E: Bull Put Spread & Bear Call Spread vs LP
# ========================================================================
print("\nGenerating Graph E: Put/Call Spreads vs LP...")

prices_E = np.linspace(1500, 2700, 500)
lower_strike_E = 1800
upper_strike_E = 2200
entry_price_E = 2000
investment_E = 10000

# LP Position
lp_vals_E, L_E = uniswap_v3_value(prices_E, lower_strike_E, upper_strike_E, investment_E, entry_price_E)

# Bull Put Spread (profit if price stays above 2200)
bull_put_vals_E = bull_put_spread_value(prices_E, upper_strike_E, lower_strike_E, entry_price_E, investment_E)

# Bear Call Spread (profit if price stays below 1800)
bear_call_vals_E = bear_call_spread_value(prices_E, lower_strike_E, upper_strike_E, entry_price_E, investment_E)

plt.figure(figsize=(12, 7))
plt.plot(prices_E, bull_put_vals_E, label=f'Bull Put Spread (${lower_strike_E}-${upper_strike_E})',
         linestyle='--', color='green', linewidth=2)
plt.plot(prices_E, bear_call_vals_E, label=f'Bear Call Spread (${lower_strike_E}-${upper_strike_E})',
         linestyle='--', color='red', linewidth=2)
plt.plot(prices_E, lp_vals_E, label=f'Uniswap v3 LP (${lower_strike_E}-${upper_strike_E})',
         color='orange', linewidth=2.5)

plt.title('Comparison: Bull Put / Bear Call Spreads vs Uniswap v3 LP', fontsize=14, fontweight='bold')
plt.xlabel('ETH Price ($)', fontsize=12)
plt.ylabel('Position Value ($)', fontsize=12)
plt.axhline(y=investment_E, color='black', linestyle='-', alpha=0.3, linewidth=0.8)
plt.axvline(x=entry_price_E, color='gray', linestyle=':', alpha=0.7, label=f'Entry Price (${entry_price_E})')
plt.axvline(x=lower_strike_E, color='gray', linestyle=':', alpha=0.5)
plt.axvline(x=upper_strike_E, color='gray', linestyle=':', alpha=0.5)

plt.axvspan(lower_strike_E, upper_strike_E, alpha=0.1, color='orange', label='Strike/Range Zone')
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)

plt.annotate('Bull Put: Max profit\nabove upper strike',
             xy=(2400, bull_put_vals_E[np.argmin(np.abs(prices_E - 2400))]),
             xytext=(2450, 11000),
             arrowprops=dict(facecolor='green', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('Bear Call: Max profit\nbelow lower strike',
             xy=(1600, bear_call_vals_E[np.argmin(np.abs(prices_E - 1600))]),
             xytext=(1500, 11000),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('LP: Best value\nin middle of range',
             xy=(2000, lp_vals_E[np.argmin(np.abs(prices_E - 2000))]),
             xytext=(2100, 8500),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_E_spreads_vs_lp.png', dpi=150, bbox_inches='tight')
print("✓ Graph E saved to plot_E_spreads_vs_lp.png")

# ========================================================================
# GRAPH F: Collar vs LP
# ========================================================================
print("\nGenerating Graph F: Collar vs LP...")

prices_F = np.linspace(1500, 3000, 500)
put_strike_F = 2000
call_strike_F = 2500
entry_price_F = 2250
investment_F = 10000

# LP Position (entered in middle)
lp_vals_F, L_F = uniswap_v3_value(prices_F, put_strike_F, call_strike_F, investment_F, entry_price_F)

# Collar Strategy
collar_vals_F = collar_value(prices_F, put_strike_F, call_strike_F, entry_price_F, investment_F)

# Pure ETH HODL for reference
eth_amount_F = investment_F / entry_price_F
eth_hodl_F = eth_amount_F * prices_F

plt.figure(figsize=(12, 7))
plt.plot(prices_F, eth_hodl_F, label='Pure ETH HODL',
         linestyle=':', color='blue', linewidth=2, alpha=0.6)
plt.plot(prices_F, collar_vals_F, label=f'Collar (Put ${put_strike_F} / Call ${call_strike_F})',
         linestyle='--', color='purple', linewidth=2)
plt.plot(prices_F, lp_vals_F, label=f'Uniswap v3 LP (${put_strike_F}-${call_strike_F})',
         color='orange', linewidth=2.5)

plt.title('Comparison: Collar Strategy vs Uniswap v3 LP', fontsize=14, fontweight='bold')
plt.xlabel('ETH Price ($)', fontsize=12)
plt.ylabel('Position Value ($)', fontsize=12)
plt.axvline(x=entry_price_F, color='gray', linestyle=':', alpha=0.7, label=f'Entry Price (${entry_price_F})')
plt.axvline(x=put_strike_F, color='orange', linestyle=':', alpha=0.5)
plt.axvline(x=call_strike_F, color='orange', linestyle=':', alpha=0.5)

plt.axvspan(put_strike_F, call_strike_F, alpha=0.1, color='orange', label='LP Active Range')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.annotate('Collar: Sharp boundaries\n(option strikes)',
             xy=(put_strike_F, collar_vals_F[np.argmin(np.abs(prices_F - put_strike_F))]),
             xytext=(1750, 10500),
             arrowprops=dict(facecolor='purple', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('LP: Smooth transitions\n(continuous rebalancing)',
             xy=(2200, lp_vals_F[np.argmin(np.abs(prices_F - 2200))]),
             xytext=(2050, 8500),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('Both strategies create\nbounded risk profiles',
             xy=(2700, lp_vals_F[np.argmin(np.abs(prices_F - 2700))]),
             xytext=(2650, 12500),
             fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_F_collar_vs_lp.png', dpi=150, bbox_inches='tight')
print("✓ Graph F saved to plot_F_collar_vs_lp.png")

print("\n" + "="*60)
print("All additional comparison graphs generated successfully!")
print("="*60)
