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

# ========================================================================
# Greeks Dashboard - Clean Version (Graphs Only, No Text)
# ========================================================================
print("Generating Greeks Dashboard (graphs only)...")

# Parameters
prices = np.linspace(1500, 2500, 1000)
P_a = 1800
P_b = 2200
P_entry = 2000
investment = 10000

# Create figure with 3 subplots
fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(2, 2, hspace=0.25, wspace=0.25)

ax1 = fig.add_subplot(gs[0, :])  # Position Value (top, full width)
ax2 = fig.add_subplot(gs[1, 0])  # Delta (bottom left)
ax3 = fig.add_subplot(gs[1, 1])  # Gamma (bottom right)

# Position Value
lp_vals, _ = uniswap_v3_value(prices, P_a, P_b, investment, P_entry)
ax1.plot(prices, lp_vals, color='orange', linewidth=3)
ax1.axvline(x=P_a, color='orange', linestyle=':', alpha=0.5)
ax1.axvline(x=P_b, color='orange', linestyle=':', alpha=0.5)
ax1.axvspan(P_a, P_b, alpha=0.1, color='orange')
ax1.set_title('Uniswap v3 Position Value (Range $1800-$2200)', fontsize=13, fontweight='bold')
ax1.set_xlabel('ETH Price ($)', fontsize=11)
ax1.set_ylabel('Position Value ($)', fontsize=11)
ax1.grid(True, alpha=0.3)

# Delta
lp_delta = uniswap_v3_delta(prices, P_a, P_b, investment, P_entry)
ax2.plot(prices, lp_delta, color='blue', linewidth=3)
ax2.axvline(x=P_a, color='orange', linestyle=':', alpha=0.5)
ax2.axvline(x=P_b, color='orange', linestyle=':', alpha=0.5)
ax2.axvspan(P_a, P_b, alpha=0.1, color='orange')
ax2.set_title('Delta (Δ): ETH Exposure', fontsize=12, fontweight='bold')
ax2.set_xlabel('ETH Price ($)', fontsize=11)
ax2.set_ylabel('Delta (ETH Quantity)', fontsize=11)
ax2.grid(True, alpha=0.3)

# Gamma
lp_gamma = uniswap_v3_gamma(prices, P_a, P_b, investment, P_entry)
ax3.plot(prices, lp_gamma, color='red', linewidth=3)
ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax3.axvline(x=P_a, color='orange', linestyle=':', alpha=0.5)
ax3.axvline(x=P_b, color='orange', linestyle=':', alpha=0.5)
ax3.axvspan(P_a, P_b, alpha=0.1, color='orange')
ax3.fill_between(prices, 0, lp_gamma, where=(lp_gamma < 0), alpha=0.3, color='red', label='Negative Gamma')
ax3.set_title('Gamma (Γ): Rate of Delta Change', fontsize=12, fontweight='bold')
ax3.set_xlabel('ETH Price ($)', fontsize=11)
ax3.set_ylabel('Gamma (∂Δ/∂P)', fontsize=11)
ax3.legend(fontsize=9, loc='upper left')
ax3.grid(True, alpha=0.3)

plt.savefig('/home/user/scratch/plot_I_greeks_dashboard.png', dpi=150, bbox_inches='tight')
print("✓ Greeks Dashboard saved to plot_I_greeks_dashboard.png")
print("  (Clean version with graphs only, no text interpretation)")
