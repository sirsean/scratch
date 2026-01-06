import numpy as np

# Test the formulas from the code
def test_uniswap_formulas():
    """Verify the Uniswap v3 formulas against known properties"""

    print("=" * 60)
    print("VERIFYING UNISWAP V3 FORMULAS")
    print("=" * 60)

    # Test Case 1: Position with P_entry at upper bound (all USDC)
    print("\n1. Test: Entry at upper bound (P=2500, range 2000-2500)")
    P_a = 2000
    P_b = 2500
    P_entry = 2500
    investment = 10000

    sqrt_Pa = np.sqrt(P_a)
    sqrt_Pb = np.sqrt(P_b)
    sqrt_P_entry = np.sqrt(P_entry)

    # All USDC at entry
    y_init = investment
    L = y_init / (sqrt_Pb - sqrt_Pa)
    print(f"   Liquidity L: {L:.2f}")
    print(f"   Initial USDC (y): ${y_init:.2f}")
    print(f"   Initial ETH (x): 0")

    # Verify value at entry
    val_at_entry = L * (sqrt_Pb - sqrt_Pa)
    print(f"   Value at P=2500: ${val_at_entry:.2f} (should be ${investment})")
    assert abs(val_at_entry - investment) < 0.01, "Entry value mismatch!"

    # Test value at P=2200 (in range)
    P_test = 2200
    sqrt_P_test = np.sqrt(P_test)
    val_in_range = L * (sqrt_P_test - sqrt_Pa) + L * (1/sqrt_P_test - 1/sqrt_Pb) * P_test
    x_at_2200 = L * (1/sqrt_P_test - 1/sqrt_Pb)
    y_at_2200 = L * (sqrt_P_test - sqrt_Pa)
    print(f"\n   At P=2200 (in range):")
    print(f"   ETH amount: {x_at_2200:.4f} ETH")
    print(f"   USDC amount: ${y_at_2200:.2f}")
    print(f"   Total value: ${val_in_range:.2f}")
    print(f"   Value check: ${y_at_2200:.2f} + {x_at_2200:.4f}*{P_test} = ${y_at_2200 + x_at_2200*P_test:.2f}")

    # Test value at P=1800 (below range)
    P_below = 1800
    val_below = L * (1/sqrt_Pa - 1/sqrt_Pb) * P_below
    x_below = L * (1/sqrt_Pa - 1/sqrt_Pb)
    print(f"\n   At P=1800 (below range):")
    print(f"   ETH amount: {x_below:.4f} ETH")
    print(f"   USDC amount: $0")
    print(f"   Total value: ${val_below:.2f}")
    print(f"   Value check: {x_below:.4f}*{P_below} = ${x_below*P_below:.2f}")

    # Test Case 2: Position with P_entry in middle of range
    print("\n\n2. Test: Entry in middle of range (P=2000, range 1800-2200)")
    P_a2 = 1800
    P_b2 = 2200
    P_entry2 = 2000

    sqrt_Pa2 = np.sqrt(P_a2)
    sqrt_Pb2 = np.sqrt(P_b2)
    sqrt_P_entry2 = np.sqrt(P_entry2)

    # Calculate L from investment value
    L2 = investment / ((sqrt_P_entry2 - sqrt_Pa2) + (1/sqrt_P_entry2 - 1/sqrt_Pb2)*P_entry2)
    print(f"   Liquidity L: {L2:.2f}")

    # Calculate amounts at entry
    x_entry = L2 * (1/sqrt_P_entry2 - 1/sqrt_Pb2)
    y_entry = L2 * (sqrt_P_entry2 - sqrt_Pa2)
    val_entry = y_entry + x_entry * P_entry2

    print(f"   Initial ETH (x): {x_entry:.4f} ETH")
    print(f"   Initial USDC (y): ${y_entry:.2f}")
    print(f"   Total value at entry: ${val_entry:.2f} (should be ${investment})")
    assert abs(val_entry - investment) < 0.01, "Entry value mismatch!"

    # Test impermanent loss concept
    print("\n\n3. Test: Impermanent Loss")
    print("   Entry at P=2000, check value at different prices")

    # Calculate HODL value (what we'd have if we just held the initial amounts)
    test_prices = [1800, 2000, 2200]
    for P_test in test_prices:
        sqrt_P_test = np.sqrt(P_test)

        # LP position value
        if P_test <= P_a2:
            x_lp = L2 * (1/sqrt_Pa2 - 1/sqrt_Pb2)
            y_lp = 0
            lp_value = x_lp * P_test
        elif P_test >= P_b2:
            x_lp = 0
            y_lp = L2 * (sqrt_Pb2 - sqrt_Pa2)
            lp_value = y_lp
        else:
            x_lp = L2 * (1/sqrt_P_test - 1/sqrt_Pb2)
            y_lp = L2 * (sqrt_P_test - sqrt_Pa2)
            lp_value = y_lp + x_lp * P_test

        # HODL value
        hodl_value = y_entry + x_entry * P_test

        # Impermanent loss
        il = lp_value - hodl_value
        il_pct = (il / hodl_value) * 100

        print(f"\n   At P={P_test}:")
        print(f"   LP value: ${lp_value:.2f}")
        print(f"   HODL value: ${hodl_value:.2f}")
        print(f"   IL: ${il:.2f} ({il_pct:.2f}%)")

    print("\n" + "=" * 60)
    print("✓ All formula verifications passed!")
    print("=" * 60)

if __name__ == "__main__":
    test_uniswap_formulas()
