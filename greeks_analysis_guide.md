# Uniswap v3 Greeks Analysis: Complete Risk Model Guide

## Executive Summary

Uniswap v3 LP positions have options-like Greeks that determine their risk profile. Understanding these Greeks is **crucial** for managing LP positions effectively.

**Key Insight**: LP positions are **SHORT GAMMA + POSITIVE THETA (fees)**
- Profitable when: **Fee income > Impermanent loss from rebalancing**

---

## The Greeks: Detailed Breakdown

### 1. DELTA (Δ) - Position Sensitivity to Price

**Definition**: How much your position value changes for a $1 change in ETH price.

**For Options**:
- Call delta: 0 to 1 (increases as goes ITM)
- Put delta: -1 to 0 (becomes more negative as goes ITM)
- Straddle: Jumps from +1 to -1 at strike

**For Uniswap v3**:
```
Below range (P < Pa): Δ = constant (max ETH held)
In range (Pa < P < Pb): Δ = L * (1/√P - 1/√Pb)  [decreases smoothly]
Above range (P > Pb): Δ = 0 (all USDC, no ETH)
```

**Key Characteristics**:
- **Smooth transition** in range (vs sharp jumps in options)
- Delta naturally decreases as price rises (selling ETH)
- Delta increases as price falls (buying ETH)
- This is automatic rebalancing!

**Practical Use**:
- To **delta hedge**: Short Δ ETH in perpetual futures
- Example: If Δ = 2.5 ETH at current price, short 2.5 ETH perps to be delta-neutral
- Must rehedge as price moves (delta changes)

**Differences from Options**:
| Aspect | Options | Uniswap v3 LP |
|--------|---------|---------------|
| Transition | Sharp kink at strike | Smooth curve |
| Formula | Binary (ITM/OTM) | Continuous (√P function) |
| Rebalancing | At expiration/exercise | Continuous |

---

### 2. GAMMA (Γ) - The Source of Impermanent Loss

**Definition**: Rate of change of delta (∂Δ/∂P). Measures position convexity.

**Formula for LP in range**:
```
Γ = ∂Δ/∂P = -L * (1/(2*P^(3/2)))
```

**CRITICAL INSIGHT**: Gamma is **NEGATIVE** in range!

**What Negative Gamma Means**:
```
Price ↑ → Delta ↓ → You sell ETH (sell high) ✓
         BUT you sold at average price, not top

Price ↓ → Delta ↑ → You buy ETH (buy low) ✓
         BUT you bought at average price, not bottom

Net effect: BUY HIGH, SELL LOW (on average)
```

**This IS Impermanent Loss!**

**Gamma Profile**:
- **OUT of range**: Γ ≈ 0 (no rebalancing, no IL, no fees)
- **IN range**: Γ < 0 (negative gamma, continuous rebalancing)
- **At boundaries**: Γ has discontinuities (sharp transitions)

**Comparison to Options**:

| Strategy | Gamma Sign | Meaning |
|----------|------------|---------|
| Long options | Positive | Profit from volatility (buy low, sell high) |
| Short options | Negative | Loss from volatility (buy high, sell low) |
| **Uniswap v3 LP** | **Negative (in range)** | **Like selling options** |

**The Trade-off**:
- Negative gamma = You LOSE on price movement alone
- BUT you COLLECT fees from traders crossing your range
- Profitable if: **Fees > Gamma losses**

---

### 3. THETA (θ) - Time Value / Fee Income

**For Traditional Options**:
- Options lose value over time (time decay)
- Short options = positive theta (you collect this decay)

**For Uniswap v3**:
- NO expiration date → No traditional theta
- BUT you earn **fees over time** → Acts like positive theta!

**Fee Income as "Positive Theta"**:
```
Daily P&L = -Gamma losses + Fee income
          = Impermanent loss + Fees
          = (Negative Theta-like) + (Positive Theta-like)
```

**Key Metrics**:
- **Fee APR**: Annualized fee return (like theta in %/year)
- Higher fee tier (1% vs 0.05%) = Higher theta
- More volume = Higher realized theta

**Profitability Condition**:
```
Cumulative Fees > Cumulative Impermanent Loss
```

This is analogous to theta (fees) offsetting gamma losses in options selling strategies.

---

### 4. VEGA (ν) - Volatility Sensitivity

**For Options**:
- Value increases with implied volatility
- Long options = positive vega

**For Uniswap v3** (complex!):

**Positive Effect**:
- High volatility → More trading → More fees ✓

**Negative Effect**:
- High volatility → More rebalancing → More IL ✗

**Net Vega Effect**:
```
Net P&L sensitivity to volatility =
    (Fee rate × Trading volume × Volatility)
  - (Gamma exposure × Realized volatility²)
```

**Optimal Conditions**:
1. **High volatility + Tight spreads**: Lots of trading, lots of fees
2. **Range-bound price action**: Volatility without trending = fees without excessive IL
3. **High fee tier for high vol pairs**: 1% fee pools for volatile pairs

**Vega Analogy**:
- LP positions are **SHORT vega** in the gamma sense (IL increases with vol)
- But **LONG vega** in the fee sense (fees increase with vol)
- Net effect depends on fee tier and volume

---

### 5. RHO (ρ) - Interest Rate Sensitivity

**For Traditional Finance**:
- Measures sensitivity to risk-free rate changes

**For Crypto/DeFi**:
- Less relevant (no traditional risk-free rate)
- Could consider: Stablecoin yield as "risk-free" rate
- Opportunity cost: LP yield vs staking/lending yield

**Practical Consideration**:
- Compare LP APR to:
  - ETH staking yield (~3-4%)
  - Stablecoin lending (variable)
  - Other DeFi yield opportunities

---

## Greeks Summary Table

| Greek | Options (Long) | Options (Short) | Uniswap v3 LP (In Range) |
|-------|---------------|-----------------|--------------------------|
| **Delta (Δ)** | 0 to ±1 | 0 to ±1 | Smooth decrease: L*(1/√P - 1/√Pb) |
| **Gamma (Γ)** | Positive | Negative | **Negative (like short options)** |
| **Theta (θ)** | Negative | Positive | **Positive (fees act like theta)** |
| **Vega (ν)** | Positive | Negative | Mixed (fees+ vs IL-) |
| **Rho (ρ)** | Varies | Varies | Low relevance |

---

## Risk Management Using Greeks

### 1. Delta Hedging

**Goal**: Neutralize price exposure

**Method**:
```
Hedge Ratio = -Δ
If Δ = 2.5 ETH → Short 2.5 ETH perps
```

**Benefit**:
- Isolate fee income from price risk
- Pure yield strategy (fees only)

**Cost**:
- Funding rates on perps
- Rehedging costs as delta changes

### 2. Gamma Management

**Challenge**: Can't directly hedge negative gamma without closing position

**Strategies**:
1. **Wider ranges** = Lower gamma exposure (less rebalancing)
2. **Active range management** = Move range with price
3. **Multiple positions** = Different ranges, net lower gamma

**Accept the gamma** if:
```
Expected fee APR > Expected IL from gamma
```

### 3. Volatility-Based Position Sizing

**Use implied volatility to size positions**:

```python
Expected IL ≈ Gamma × Realized_Volatility²
Required Fee APR > Expected IL

If vol is high → Require higher fees → Choose:
  - Wider range (lower gamma)
  - Higher fee tier (more theta)
  - Smaller position size
```

---

## Profitability Framework

### The Core Equation

```
Total P&L = Price Change P&L + Fee Income + Gas Costs

Where:
  Price Change P&L = ∫(Δ * dP) + ½ * ∫(Γ * dP²)
                   = Delta effect + Gamma effect
                   = Delta effect + Impermanent Loss

  Fee Income = ∫(Fee Rate × Volume × Liquidity %)
```

**In English**:
1. You make/lose money from price changes (delta + gamma effects)
2. You make money from fees (theta-like income)
3. You lose money on gas (transaction costs)

### Break-Even Analysis

**Position is profitable if**:
```
Cumulative Fees > |Impermanent Loss| + Gas Costs
```

**Typical scenarios**:

| Volatility | Price Trend | Range | Outcome |
|------------|-------------|-------|---------|
| Low | Sideways | Narrow | ✓✓✓ Best (fees, low IL) |
| Low | Trending | Any | ✗ Low fees |
| High | Sideways | Wide | ✓✓ Good (fees > IL) |
| High | Trending | Narrow | ✗✗ Worst (high IL) |
| High | Sideways | Narrow | ✓ Fees offset IL if volume high |

---

## Advanced Greeks Topics

### Convexity (Gamma × Time)

**Realized P&L from gamma**:
```
Gamma P&L ≈ ½ * Γ * σ² * S² * t

Where:
  Γ = gamma
  σ = realized volatility
  S = spot price
  t = time
```

**Key insight**: IL scales with **volatility squared** and time

### Gamma Scalping (Impossible for LP)

**In options trading**:
- Long gamma → Profit by delta hedging (buy low, sell high)

**In LP**:
- Short gamma → Cannot profit from delta hedging
- Can only offset with fee income
- No way to "scalp" the gamma

### Cross-Greeks

**Delta-Gamma relationship**:
```
∂Δ/∂P = Γ

For LP: Δ = L * (1/√P - 1/√Pb)
       Γ = -L/(2*P^(3/2))
```

Notice: Gamma is always negative in range (derivative is negative)

---

## Practical Examples

### Example 1: ETH/USDC 0.05% Pool

**Setup**:
- Range: $1800 - $2200
- Entry: $2000
- Investment: $10,000
- Entry position: ~2.5 ETH + $5,000 USDC

**Greeks at entry ($2000)**:
- Delta: 2.5 ETH
- Gamma: -0.0125 (negative!)
- Theta (fees): ~20% APR (in high volume)

**Scenario: Price moves to $2200**:
- Delta change: 2.5 → 1.0 ETH (sold 1.5 ETH)
- Gamma loss: ~$50 (impermanent loss)
- Fee gain (7 days): ~$38 (at 20% APR)
- Net: -$12 (fees didn't cover IL yet)

**Scenario: Price oscillates $1900-$2100 for 30 days**:
- Impermanent loss: ~$80 (from rebalancing)
- Fee income: ~$165 (30 days at 20% APR)
- Net: +$85 ✓ (fees covered IL + profit)

### Example 2: Delta Hedging Strategy

**Goal**: Earn fees without price risk

**Method**:
1. Deposit $10k in LP (Δ = 2.5 ETH at $2000)
2. Short 2.5 ETH perps at $2000
3. Rehedge when Δ changes significantly

**Result**:
- Price moves don't affect total portfolio value
- Earn LP fees
- Pay perp funding rates
- Net = Fee APR - Funding APR - Rehedging costs

**When profitable**:
- LP fees > Perp costs (common in high-volume pools)

---

## Conclusion

Understanding Greeks transforms LP positions from "black box" to **quantifiable risk**:

1. **Delta** = Your ETH exposure (hedge-able)
2. **Gamma** = Your impermanent loss rate (accept or reduce)
3. **Theta** = Your fee income (maximize this!)
4. **Vega** = Your volatility exposure (complex, monitor closely)

**The LP Game**:
- You are SHORT gamma (bad for price moves)
- You collect fees (good, theta-like income)
- Win when: Theta > |Gamma losses|

**Optimal LP Strategy**:
1. Choose high-volume pools (high theta)
2. Size ranges appropriately for volatility (manage gamma)
3. Consider delta hedging for pure yield (eliminate delta risk)
4. Monitor and rebalance when Greeks shift unfavorably

Understanding Greeks lets you make **data-driven decisions** rather than guessing whether LP positions are profitable.
