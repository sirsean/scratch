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

def covered_call_value(prices, strike, initial_price, investment):
    """
    Covered call: Own ETH + sell call option
    Buy ETH with investment, value capped at strike price worth
    """
    eth_amount = investment / initial_price

    # Value = min(current_price, strike) * eth_amount
    # If price > strike, we get called away at strike
    # If price < strike, we have our ETH worth current price
    values = []
    for p in prices:
        if p > strike:
            # Called away: get strike * eth_amount
            val = strike * eth_amount
        else:
            # Keep ETH: worth p * eth_amount
            val = p * eth_amount
        values.append(val)

    return np.array(values)

# ========================================================================
# GRAPH A: LP vs HODL vs Uniswap v2
# ========================================================================
print("Generating Graph A: LP vs HODL vs Uniswap v2...")

prices_A = np.linspace(1500, 3000, 500)
range_lower = 2000
range_upper = 2500
P_entry = 2250  # Enter in middle of range
investment = 10000

# Uniswap v3 Position (concentrated)
v3_vals, L_v3 = uniswap_v3_value(prices_A, range_lower, range_upper, investment, P_entry)
x_v3, y_v3 = get_initial_amounts(L_v3, P_entry, range_lower, range_upper)

# HODL (just hold the initial amounts)
hodl_vals = y_v3 + x_v3 * prices_A

# Uniswap v2 (full range: 0 to infinity)
# For v2, it's like v3 with Pa=0 and Pb=∞, which simplifies to constant product formula
# At any price P, with initial x and y: value = 2*sqrt(x*y*P)
# Actually, for v2 starting with value V at price P0, at price P: value = V * sqrt(P/P0) + V * sqrt(P0/P)
# Wait, let me think more carefully...
# In v2, if you start with x ETH and y USDC at price P0 where x*P0 + y = V
# At price P, you'll have x' and y' where x'*y' = x*y (constant product)
# and x'*P + y' = value
# From x'*y' = k and the price relationship, we get:
# x' = sqrt(k/P), y' = sqrt(k*P)
# value = x'*P + y' = sqrt(k*P) + sqrt(k*P) = 2*sqrt(k*P)
# At entry: x*P_entry + y = V and x*y = k
# For 50/50 entry: x*P_entry = V/2 and y = V/2
# So x = V/(2*P_entry) and y = V/2
# k = x*y = V^2/(4*P_entry)
# value = 2*sqrt(k*P) = 2*sqrt(V^2/(4*P_entry) * P) = V*sqrt(P/P_entry)

# Actually cleaner formula: for v2 with initial value V at price P_entry split 50/50:
# value(P) = V * (sqrt(P/P_entry) + sqrt(P_entry/P)) / 2
# Hmm, let me reconsider. The standard IL formula for v2 is:
# V(P) = V0 * 2*sqrt(price_ratio) / (1 + price_ratio)

# Let me use the proper formula:
# Initial position: x_v2 = V/(2*P_entry), y_v2 = V/2 (50/50 split)
x_v2_init = investment / (2 * P_entry)
y_v2_init = investment / 2
k_v2 = x_v2_init * y_v2_init

v2_vals = 2 * np.sqrt(k_v2 * prices_A)

plt.figure(figsize=(12, 7))
plt.plot(prices_A, hodl_vals, label='HODL (50/50 Split)', linestyle=':', color='green', linewidth=2)
plt.plot(prices_A, v2_vals, label='Uniswap v2 (Full Range)', linestyle='--', color='purple', linewidth=2)
plt.plot(prices_A, v3_vals, label='Uniswap v3 ($2000-$2500 Range)', color='orange', linewidth=2.5)

plt.title('Comparison: Uniswap v3 vs v2 vs HODL', fontsize=14, fontweight='bold')
plt.xlabel('ETH Price ($)', fontsize=12)
plt.ylabel('Position Value ($)', fontsize=12)
plt.axvline(x=P_entry, color='gray', linestyle=':', alpha=0.7, label=f'Entry Price (${P_entry})')
plt.axvline(x=range_lower, color='orange', linestyle=':', alpha=0.5)
plt.axvline(x=range_upper, color='orange', linestyle=':', alpha=0.5)

# Add shaded region for v3 range
plt.axvspan(range_lower, range_upper, alpha=0.1, color='orange', label='v3 Active Range')

plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# Annotations
plt.annotate('v3 goes "out of range"\n(100% ETH)',
             xy=(1700, v3_vals[np.argmin(np.abs(prices_A - 1700))]),
             xytext=(1550, 11000),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('HODL: No IL',
             xy=(2700, hodl_vals[np.argmin(np.abs(prices_A - 2700))]),
             xytext=(2600, 14000),
             arrowprops=dict(facecolor='green', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('v2: Always active\nbut lower effective liquidity',
             xy=(2300, v2_vals[np.argmin(np.abs(prices_A - 2300))]),
             xytext=(2500, 9500),
             arrowprops=dict(facecolor='purple', shrink=0.05, width=1.5),
             fontsize=9)

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_A_lp_vs_hodl_vs_v2.png', dpi=150, bbox_inches='tight')
print("✓ Graph A saved to plot_A_lp_vs_hodl_vs_v2.png")

# ========================================================================
# GRAPH C: Covered Call vs LP (Entry at Lower Bound)
# ========================================================================
print("\nGenerating Graph C: Covered Call vs LP...")

prices_C = np.linspace(1500, 3000, 500)
range_lower_C = 2000
range_upper_C = 2500
P_entry_C = 2000  # Enter at lower bound (all ETH)
investment_C = 10000

# LP Position (entered at lower bound, so we have all ETH)
lp_vals_C, L_C = uniswap_v3_value(prices_C, range_lower_C, range_upper_C, investment_C, P_entry_C)

# Covered Call (buy ETH, sell call at upper bound)
cc_vals_C = covered_call_value(prices_C, range_upper_C, P_entry_C, investment_C)

# Also show pure ETH HODL for reference
eth_amount = investment_C / P_entry_C
eth_hodl_vals = eth_amount * prices_C

plt.figure(figsize=(12, 7))
plt.plot(prices_C, eth_hodl_vals, label='Pure ETH HODL', linestyle=':', color='blue', linewidth=2)
plt.plot(prices_C, cc_vals_C, label=f'Covered Call (Strike ${range_upper_C})', linestyle='--', color='red', linewidth=2)
plt.plot(prices_C, lp_vals_C, label=f'Uniswap v3 LP (${range_lower_C}-${range_upper_C})', color='orange', linewidth=2.5)

plt.title('Comparison: Covered Call vs Uniswap v3 LP (Entry at Lower Bound)', fontsize=14, fontweight='bold')
plt.xlabel('ETH Price ($)', fontsize=12)
plt.ylabel('Position Value ($)', fontsize=12)
plt.axvline(x=P_entry_C, color='gray', linestyle=':', alpha=0.7, label=f'Entry Price (${P_entry_C})')
plt.axvline(x=range_upper_C, color='orange', linestyle=':', alpha=0.5)

# Add shaded region
plt.axvspan(range_lower_C, range_upper_C, alpha=0.1, color='orange', label='LP Active Range')

plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# Annotations
plt.annotate('Capped upside\n(converted to USDC)',
             xy=(range_upper_C, lp_vals_C[np.argmin(np.abs(prices_C - range_upper_C))]),
             xytext=(2650, 11500),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('Covered call:\nupside capped at strike',
             xy=(range_upper_C, cc_vals_C[np.argmin(np.abs(prices_C - range_upper_C))]),
             xytext=(2400, 13500),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5),
             fontsize=9)

plt.annotate('Both strategies\ncap upside gains',
             xy=(2800, lp_vals_C[np.argmin(np.abs(prices_C - 2800))]),
             xytext=(2750, 9000),
             fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

plt.annotate('LP has curved payoff\n(gamma exposure)',
             xy=(2200, lp_vals_C[np.argmin(np.abs(prices_C - 2200))]),
             xytext=(2250, 14000),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_C_covered_call_vs_lp.png', dpi=150, bbox_inches='tight')
print("✓ Graph C saved to plot_C_covered_call_vs_lp.png")

print("\n" + "="*60)
print("All graphs generated successfully!")
print("="*60)
