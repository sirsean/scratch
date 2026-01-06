import matplotlib.pyplot as plt
import numpy as np

def uniswap_v3_value(P_current, P_a, P_b, Investment_Value, P_entry):
    """Calculates the value of a Uniswap v3 position"""
    sqrt_Pa = np.sqrt(P_a)
    sqrt_Pb = np.sqrt(P_b)
    sqrt_P_entry = np.sqrt(P_entry)

    if P_entry <= P_a:
        x_init = Investment_Value / P_entry
        y_init = 0
        L = x_init * (sqrt_Pa * sqrt_Pb) / (sqrt_Pb - sqrt_Pa)
    elif P_entry >= P_b:
        x_init = 0
        y_init = Investment_Value
        L = y_init / (sqrt_Pb - sqrt_Pa)
    else:
        L = Investment_Value / ( (sqrt_P_entry - sqrt_Pa) + (1/sqrt_P_entry - 1/sqrt_Pb)*P_entry )

    sqrt_P = np.sqrt(P_current)

    values = []
    for p, sp in zip(P_current, sqrt_P):
        if p <= P_a:
            val = L * ( (sqrt_Pb - sqrt_Pa) / (sqrt_Pa * sqrt_Pb) ) * p
        elif p >= P_b:
            val = L * (sqrt_Pb - sqrt_Pa)
        else:
            val = L * (sp - sqrt_Pa) + L * (1/sp - 1/sqrt_Pb) * p
        values.append(val)

    return np.array(values), L

def uniswap_v3_delta(P_current, P_a, P_b, Investment_Value, P_entry):
    """
    Calculate delta (∂V/∂P) for Uniswap v3 position
    Delta represents the amount of the underlying asset (ETH) held
    """
    sqrt_Pa = np.sqrt(P_a)
    sqrt_Pb = np.sqrt(P_b)
    sqrt_P_entry = np.sqrt(P_entry)

    if P_entry <= P_a:
        L = (Investment_Value / P_entry) * (sqrt_Pa * sqrt_Pb) / (sqrt_Pb - sqrt_Pa)
    elif P_entry >= P_b:
        L = Investment_Value / (sqrt_Pb - sqrt_Pa)
    else:
        L = Investment_Value / ( (sqrt_P_entry - sqrt_Pa) + (1/sqrt_P_entry - 1/sqrt_Pb)*P_entry )

    deltas = []
    for p in P_current:
        if p <= P_a:
            # Below range: delta = x_max (constant)
            delta = L * (sqrt_Pb - sqrt_Pa) / (sqrt_Pa * sqrt_Pb)
        elif p >= P_b:
            # Above range: delta = 0 (no ETH held)
            delta = 0
        else:
            # In range: delta = L * (1/sqrt(P) - 1/sqrt(Pb))
            delta = L * (1/np.sqrt(p) - 1/sqrt_Pb)
        deltas.append(delta)

    return np.array(deltas)

def uniswap_v3_gamma(prices, P_a, P_b, Investment_Value, P_entry):
    """
    Calculate gamma (∂²V/∂P² or ∂Δ/∂P) for Uniswap v3
    Numerical derivative of delta
    """
    delta = uniswap_v3_delta(prices, P_a, P_b, Investment_Value, P_entry)
    gamma = np.gradient(delta, prices)
    return gamma

def short_straddle_delta(prices, strike, investment, entry_price):
    """Delta for short straddle (short put + short call at same strike)"""
    eth_quantity = investment / (2 * entry_price)

    deltas = []
    for p in prices:
        if p < strike:
            # Short put delta: positive (forced to buy ETH if exercised)
            # Increases as we go deeper ITM
            delta = eth_quantity  # Simplified: assuming delta approaches 1 when ITM
        else:
            # Short call delta: negative (forced to sell ETH if exercised)
            delta = -eth_quantity

        deltas.append(delta)

    return np.array(deltas)

def covered_call_delta(prices, strike, investment, entry_price):
    """Delta for covered call (long ETH + short call)"""
    eth_amount = investment / entry_price

    deltas = []
    for p in prices:
        if p < strike:
            # Below strike: just hold ETH, delta = 1 (per ETH)
            delta = eth_amount
        else:
            # Above strike: short call reduces delta
            # Simplified: delta approaches 0 as call goes deep ITM
            delta = 0

        deltas.append(delta)

    return np.array(deltas)

def collar_delta(prices, put_strike, call_strike, investment, entry_price):
    """Delta for collar (long ETH + long put + short call)"""
    eth_amount = investment / entry_price

    deltas = []
    for p in prices:
        if p <= put_strike:
            # Protected by put: delta = 0
            delta = 0
        elif p >= call_strike:
            # Capped by call: delta = 0
            delta = 0
        else:
            # In between: full ETH exposure
            delta = eth_amount

        deltas.append(delta)

    return np.array(deltas)

# ========================================================================
# GRAPH G: Delta Comparison
# ========================================================================
print("Generating Graph G: Delta (Δ) Comparison...")

prices_G = np.linspace(1500, 2500, 1000)
P_a_G = 1800
P_b_G = 2200
P_entry_G = 2000
investment_G = 10000

# Calculate deltas
lp_delta = uniswap_v3_delta(prices_G, P_a_G, P_b_G, investment_G, P_entry_G)
straddle_delta = short_straddle_delta(prices_G, P_entry_G, investment_G, P_entry_G)
collar_delta_vals = collar_delta(prices_G, P_a_G, P_b_G, investment_G, P_entry_G)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Top plot: Delta profiles
ax1.plot(prices_G, lp_delta, label='Uniswap v3 LP', color='orange', linewidth=2.5)
ax1.plot(prices_G, straddle_delta, label='Short Straddle', linestyle='--', color='red', linewidth=2)
ax1.plot(prices_G, collar_delta_vals, label='Collar', linestyle='--', color='purple', linewidth=2)

ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=0.8)
ax1.axvline(x=P_entry_G, color='gray', linestyle=':', alpha=0.7, label=f'Entry (${P_entry_G})')
ax1.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange')

ax1.set_title('Delta (Δ) Profiles: Position Sensitivity to Price Changes', fontsize=14, fontweight='bold')
ax1.set_xlabel('ETH Price ($)', fontsize=12)
ax1.set_ylabel('Delta (ETH Quantity)', fontsize=12)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

ax1.annotate('LP: Smooth delta decay\nin range',
             xy=(2000, lp_delta[np.argmin(np.abs(prices_G - 2000))]),
             xytext=(2100, 3),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

ax1.annotate('Collar: Flat delta\noutside range',
             xy=(1700, 0),
             xytext=(1550, 1.5),
             arrowprops=dict(facecolor='purple', shrink=0.05, width=1.5),
             fontsize=9)

# Bottom plot: Zoom into LP delta
ax2.plot(prices_G, lp_delta, color='orange', linewidth=3)
ax2.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5, label='Range Boundaries')
ax2.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax2.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange', label='Active Range')

ax2.set_title('Uniswap v3 Delta Profile (Detail)', fontsize=12, fontweight='bold')
ax2.set_xlabel('ETH Price ($)', fontsize=12)
ax2.set_ylabel('Delta (ETH Quantity)', fontsize=12)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

ax2.annotate('Below range:\nConstant delta\n(max ETH)',
             xy=(1600, lp_delta[np.argmin(np.abs(prices_G - 1600))]),
             xytext=(1550, 5.5),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

ax2.annotate('In range:\nDelta decreases\nas price rises\n(selling ETH)',
             xy=(2000, lp_delta[np.argmin(np.abs(prices_G - 2000))]),
             xytext=(1950, 4.5),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

ax2.annotate('Above range:\nDelta = 0\n(all USDC)',
             xy=(2300, 0),
             xytext=(2350, 1),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_G_delta_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Graph G saved to plot_G_delta_comparison.png")

# ========================================================================
# GRAPH H: Gamma Comparison
# ========================================================================
print("\nGenerating Graph H: Gamma (Γ) Comparison...")

prices_H = np.linspace(1500, 2500, 1000)

# Calculate gammas
lp_gamma = uniswap_v3_gamma(prices_H, P_a_G, P_b_G, investment_G, P_entry_G)
straddle_gamma = np.gradient(straddle_delta, prices_G)  # Numerical derivative
collar_gamma = np.gradient(collar_delta_vals, prices_G)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Top plot: Gamma profiles
ax1.plot(prices_H, lp_gamma, label='Uniswap v3 LP', color='orange', linewidth=2.5)
ax1.plot(prices_G, straddle_gamma, label='Short Straddle', linestyle='--', color='red', linewidth=2, alpha=0.7)
ax1.plot(prices_G, collar_gamma, label='Collar', linestyle='--', color='purple', linewidth=2, alpha=0.7)

ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=0.8)
ax1.axvline(x=P_entry_G, color='gray', linestyle=':', alpha=0.7, label=f'Entry (${P_entry_G})')
ax1.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange')

ax1.set_title('Gamma (Γ) Profiles: Rate of Delta Change', fontsize=14, fontweight='bold')
ax1.set_xlabel('ETH Price ($)', fontsize=12)
ax1.set_ylabel('Gamma (∂Δ/∂P)', fontsize=12)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

ax1.annotate('Negative gamma:\nDelta decreases\nas price rises',
             xy=(2000, lp_gamma[np.argmin(np.abs(prices_H - 2000))]),
             xytext=(2100, -0.003),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

# Bottom plot: LP gamma detail with interpretation
ax2.plot(prices_H, lp_gamma, color='orange', linewidth=3)
ax2.fill_between(prices_H, 0, lp_gamma, where=(lp_gamma < 0), alpha=0.3, color='red', label='Short Gamma Zone')
ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)
ax2.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax2.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax2.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange', label='Active Range')

ax2.set_title('Uniswap v3 Gamma Profile: "Short Gamma" Exposure in Range', fontsize=12, fontweight='bold')
ax2.set_xlabel('ETH Price ($)', fontsize=12)
ax2.set_ylabel('Gamma (∂Δ/∂P)', fontsize=12)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

ax2.annotate('IN RANGE:\nNegative gamma\n= Bad for LP\n(sell low, buy high)',
             xy=(2000, lp_gamma[np.argmin(np.abs(prices_H - 2000))]),
             xytext=(2050, -0.0015),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5),
             fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.2))

ax2.annotate('OUT OF RANGE:\nGamma ≈ 0\n(no rebalancing)',
             xy=(1600, lp_gamma[np.argmin(np.abs(prices_H - 1600))]),
             xytext=(1550, 0.0005),
             arrowprops=dict(facecolor='orange', shrink=0.05, width=1.5),
             fontsize=9)

plt.tight_layout()
plt.savefig('/home/user/scratch/plot_H_gamma_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Graph H saved to plot_H_gamma_comparison.png")

# ========================================================================
# GRAPH I: Greeks Summary Dashboard
# ========================================================================
print("\nGenerating Graph I: Greeks Summary Dashboard...")

fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])  # Position Value (top, full width)
ax2 = fig.add_subplot(gs[1, 0])  # Delta (middle left)
ax3 = fig.add_subplot(gs[1, 1])  # Gamma (middle right)
ax4 = fig.add_subplot(gs[2, :])  # Greeks interpretation (bottom, full width)

prices_I = np.linspace(1500, 2500, 1000)

# Position Value
lp_vals, _ = uniswap_v3_value(prices_I, P_a_G, P_b_G, investment_G, P_entry_G)
ax1.plot(prices_I, lp_vals, color='orange', linewidth=3)
ax1.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax1.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange')
ax1.set_title('Uniswap v3 Position Value (Range $1800-$2200)', fontsize=12, fontweight='bold')
ax1.set_xlabel('ETH Price ($)')
ax1.set_ylabel('Value ($)')
ax1.grid(True, alpha=0.3)

# Delta
lp_delta_I = uniswap_v3_delta(prices_I, P_a_G, P_b_G, investment_G, P_entry_G)
ax2.plot(prices_I, lp_delta_I, color='blue', linewidth=3)
ax2.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax2.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax2.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange')
ax2.set_title('Delta (Δ): ETH Exposure', fontsize=11, fontweight='bold')
ax2.set_xlabel('ETH Price ($)')
ax2.set_ylabel('Delta (ETH)')
ax2.grid(True, alpha=0.3)

# Gamma
lp_gamma_I = uniswap_v3_gamma(prices_I, P_a_G, P_b_G, investment_G, P_entry_G)
ax3.plot(prices_I, lp_gamma_I, color='red', linewidth=3)
ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax3.axvline(x=P_a_G, color='orange', linestyle=':', alpha=0.5)
ax3.axvline(x=P_b_G, color='orange', linestyle=':', alpha=0.5)
ax3.axvspan(P_a_G, P_b_G, alpha=0.1, color='orange')
ax3.fill_between(prices_I, 0, lp_gamma_I, where=(lp_gamma_I < 0), alpha=0.3, color='red')
ax3.set_title('Gamma (Γ): Delta Change Rate', fontsize=11, fontweight='bold')
ax3.set_xlabel('ETH Price ($)')
ax3.set_ylabel('Gamma')
ax3.grid(True, alpha=0.3)

# Greeks Interpretation Panel
ax4.axis('off')
interpretation_text = """
GREEKS INTERPRETATION FOR UNISWAP V3 LP POSITIONS:

DELTA (Δ) - Position Sensitivity & Hedging:
  • Represents amount of ETH held at each price
  • Below range: Maximum delta (all ETH) - acts like HODL
  • In range: Delta decreases as price rises (continuously selling ETH for USDC)
  • Above range: Zero delta (all USDC) - no ETH exposure
  • Hedging: To delta-hedge, short Δ amount of ETH perpetuals/futures

GAMMA (Γ) - Rebalancing Cost & Profitability:
  • Negative gamma IN RANGE = "Short gamma" exposure (like selling options)
  • Negative gamma means: buy high, sell low (bad for price movement alone)
  • This is the SOURCE of impermanent loss!
  • Positive: You collect fees from traders (compensates for negative gamma)
  • Zero gamma OUT OF RANGE = no rebalancing, no IL, but also no fees

THETA (θ) - Time Value:
  • Traditional options: Negative for buyers, positive for sellers (time decay)
  • LP positions: NO EXPIRATION, but earn fees over time (like positive theta)
  • Fee APR acts like "positive theta" that offsets negative gamma losses

VEGA (ν) - Volatility Sensitivity:
  • High volatility → More trading → More fees (GOOD)
  • High volatility → More rebalancing → More IL (BAD)
  • Net effect depends on fee tier and range width vs realized volatility

KEY INSIGHT: LP positions are SHORT GAMMA + POSITIVE THETA (fees)
             Profitable when: Fee income > Impermanent loss from rebalancing
"""

ax4.text(0.05, 0.95, interpretation_text,
         transform=ax4.transAxes,
         fontsize=9,
         verticalalignment='top',
         fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.savefig('/home/user/scratch/plot_I_greeks_dashboard.png', dpi=150, bbox_inches='tight')
print("✓ Graph I saved to plot_I_greeks_dashboard.png")

print("\n" + "="*60)
print("All Greeks visualization graphs generated successfully!")
print("="*60)
