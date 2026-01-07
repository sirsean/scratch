# 15-Minute Presentation Guide: Uniswap v3

## Time Allocation (Strict)

**Total: 15 minutes**
- Opening + What is Uniswap: **2 min**
- Why it matters (LP = derivatives): **5 min**
- Business opportunity: **5 min**
- The ask: **2 min**
- Q&A: **1 min** (rest in follow-up)

**Critical**: Stay on time. This is punchy, executive-style. Details come later.

---

## The 60-Second Opening (Memorize This)

> "I'm going to share a strategic opportunity we discovered analyzing Uniswap v3. Bottom line up front: Liquidity provider positions are mathematically identical to selling options strategies. We can use this to generate 15-30% yields in range-bound volatile markets, especially where traditional options don't exist. We're proposing a $100k, 6-month pilot to validate the strategy. Let me show you why this makes sense..."

**Then immediately go to Slide 2**

---

## Slide-by-Slide Timing

### Slide 1: The Opportunity (30 sec)
- Read the four bullets, don't elaborate
- Set expectations: "15 minutes, then questions"
- Move fast

### Slide 2: What is Uniswap v3? (60 sec)
- **Don't** get bogged down in technical details
- Key points only: "$4B TVL, you deposit in a range, earn fees"
- Example in 30 seconds: "Range $2000-2500, in range = earn fees"
- **Skip if running short on time**

### Slide 3: LP = Covered Call (90 sec)
- **SLOW DOWN HERE** - this is your hook
- "Look at this payoff curve - it's identical to a covered call"
- Point out the smooth curve vs sharp kink
- "We can quantify this with Greeks we already use"

### Slide 4: LP vs Collar (60 sec)
- Quick reinforcement of the concept
- "Another match - protective collar strategy"
- Don't overexplain, the graph does the work

### Slide 5: The Greeks (90 sec)
- **CRITICAL SLIDE** - establishes risk framework
- Delta = exposure (hedge-able)
- Gamma = IL (this is the risk)
- Theta = fees (this is the reward)
- "It's just selling options, but in DeFi"

### Slide 6: Core Economics (60 sec)
- The equation: Fees - IL = Profit
- Real example: $450 fees, $200 IL = $250 net
- "Same risk/return as straddles we already trade"
- Move to next quickly

### Slide 7: When to Use (90 sec)
- **Read the green checkmarks for Uniswap**
- Emphasize: "Complementary, not replacement"
- Key phrase: "Range-bound volatile markets"

### Slide 8: Delta-Hedged LP (90 sec)
- **THE KILLER APP**
- Walk through 3 steps: "Deposit, short perps, earn net yield"
- "10-20% delta-neutral return"
- This resonates with traders

### Slide 9: Expected Returns (60 sec)
- **Don't dwell** - they can read numbers
- "Base case 7.5% is realistic, bull case 28% in ideal conditions"
- "Bear case negative 11% - yes, it can lose money"
- Quickly state: "Comparable to vol selling we already do"

### Slide 10: Risk Framework (60 sec)
- "We already understand negative gamma - it's just IL"
- Quickly mention: "Smart contract risk mitigated by Uniswap's track record"
- Don't spend time here unless asked

### Slide 11: The Pilot (90 sec)
- **SLOW DOWN** - this is the ask
- Three phases, 6 months, clear decision criteria
- "$100k, 0.25 FTE, 2 engineer-weeks"
- "If profitable, scale. If not, we learned."

### Slide 12: Why Now (60 sec)
- Institutional DeFi coming
- Build expertise early
- Quick, punchy points

### Slide 13: Comparison Matrix (30 sec)
- **Optional - skip if running over**
- Just say: "Different tools for different markets"

### Slide 14: The Ask (60 sec)
- **Reiterate the ask clearly**
- "We need approval for $100k pilot"
- Timeline: "Deploy in 3-4 weeks"
- Success metrics: "Daily monitoring, 6-month review"

### Slide 15: Takeaways (30 sec)
- Rapid fire the 5 points
- Don't elaborate
- End strong: "Low risk, high learning value"

### Slide 16: Questions (remaining time)
- Take 1-2 quick questions
- Offer deep-dive sessions for detailed discussion

---

## The 3 Must-Hit Points

**If you forget everything else, nail these:**

1. **"LP positions are mathematically identical to selling options"**
   - Show the covered call graph
   - Mention Greeks framework

2. **"We can generate 10-20% yields in the right market conditions"**
   - Delta-hedged LP strategy
   - Range-bound volatile markets

3. **"We're asking for $100k for 6 months to validate this"**
   - Clear pilot structure
   - Low risk, high learning

---

## Anticipated Questions (Quick Answers Only)

### Q: "Why not just use Deribit options?"

**A (30 sec):** "We should for BTC/ETH. But for other pairs, options are illiquid or don't exist. This gives us exposure where traditional options fail. Plus we can delta-hedge LP with Deribit futures for pure yield."

### Q: "What if it gets hacked?"

**A (30 sec):** "Uniswap has $4B TVL and 3+ years live. It's battle-tested. That said, smart contract risk is why we start with $100k - small enough to learn, not catastrophic if something goes wrong."

### Q: "These returns seem high. What's the catch?"

**A (30 sec):** "The catch is impermanent loss. In trending markets, you lose even with fees. That's why this works in range-bound volatile markets - lots of trading volume but no persistent trend. The 25% APR can drop to 10% or go negative if conditions change."

### Q: "How much work is this?"

**A (30 sec):** "0.25 FTE daily monitoring once infrastructure is built. Mostly passive unless we actively manage ranges. Less intensive than active trading strategies."

---

## What to CUT if Running Over Time

**Priority order to skip:**

1. **Slide 13** (Comparison Matrix) - nice to have, not critical
2. **Slide 2** (What is Uniswap) - assume they'll understand from context
3. **Slide 4** (Collar comparison) - covered call graph is enough
4. **Slide 12** (Why Now) - competitive advantage is implicit

**Never cut:**
- The ask (Slide 11, 14)
- Greeks/economics (Slide 5, 6)
- Delta-hedged LP strategy (Slide 8)
- At least ONE payoff graph (Slide 3)

---

## Delivery Tips for 15-Minute Format

### Do:
- **Talk fast but clear** (practice at 1.2x speed)
- **Use the graphs** - let visuals do the work
- **Be confident** - you've done the analysis
- **Stick to time** - respect their schedule

### Don't:
- **Don't** go into formulas (available in appendix)
- **Don't** tell long stories or anecdotes
- **Don't** answer questions during (defer to end)
- **Don't** apologize for rushing (this is normal executive pace)

### Pacing Tricks:
- Set a timer, glance at it
- If at 7 min and not at Slide 7: Speed up
- If someone asks question mid-presentation: "Great question, let's cover that at the end"
- Practice at least 3 times at full speed

---

## The 30-Second Close

After slide 15, before questions:

> "To summarize: We found LP positions are selling options in DeFi form. The returns are compelling - 10-20% in the right conditions. The risks are manageable - same Greeks framework we already use. We're asking for $100k over 6 months to validate this strategy and build DeFi expertise before the institutional wave hits. The upside is new alpha opportunities. The downside is we spent $100k to learn DeFi won't work for us - still valuable. Questions?"

---

## Backup Material Ready

**If they want details:**
- "We have 300+ pages of analysis available"
- "All formulas verified, code is executable"
- "Can schedule deep-dive sessions on Greeks, risk, infrastructure"
- "Happy to share all materials after this meeting"

---

## Success Criteria for This Presentation

**You've succeeded if:**
- ✅ They understand: LP = selling options
- ✅ They see: Different use case than CEX options
- ✅ They agree: $100k pilot makes sense OR want more info
- ✅ Clear next step identified (approval, deep-dive, etc.)

**Red flags:**
- ❌ Confusion about what Uniswap is
- ❌ Think this is speculative vs strategic
- ❌ No next steps / vague "we'll think about it"

---

## Post-Presentation Actions

### If approved:
- Get written approval for $100k
- Schedule infrastructure planning
- Legal/compliance kickoff
- Timeline commitment

### If "need more info":
- Schedule deep-dive sessions (Greeks, risk, ops)
- Share all analysis materials
- Set deadline for decision

### If skeptical:
- Offer smaller pilot ($25-50k)
- Suggest paper trading first
- Provide additional research
- Keep door open for reconsideration

---

## Pre-Presentation Checklist (15-Min Version)

- [ ] Rehearsed 3+ times at full speed (time yourself!)
- [ ] Can explain core thesis in 60 seconds
- [ ] Memorized the opening (slide 1)
- [ ] Know which slides to skip if over time
- [ ] Have 30-second answers to top 3 questions ready
- [ ] Graphs are clear and readable
- [ ] Know the numbers (7.5%, 28%, -11% returns)
- [ ] Clear on the ask ($100k, 6 months)
- [ ] Water ready, phone silent
- [ ] Confident in analysis

---

## Time Check Points

**At 5 minutes**: Should be finishing Slide 5 (Greeks)
**At 10 minutes**: Should be at Slide 11 (Pilot Proposal)
**At 13 minutes**: Should be wrapping up Slide 15 (Takeaways)
**At 15 minutes**: Questions

If you're behind at any checkpoint, **skip optional slides and speed up**

---

## The Absolute Minimum (If You Only Have 10 Minutes)

**Must-show slides:**
1. The Opportunity (30 sec)
2. LP = Covered Call graph (90 sec)
3. The Greeks (90 sec)
4. Delta-Hedged LP strategy (90 sec)
5. Expected Returns (60 sec)
6. The Pilot (90 sec)
7. The Ask (60 sec)
8. Questions (remaining)

**Total: 9 minutes content + questions**

This hits: What it is, why it works, how to make money, what we're asking for.

---

## Final Tips

1. **Start strong**: First 60 seconds sets the tone
2. **Visual focus**: Let graphs do the talking
3. **Be direct**: This is business, not academia
4. **Own the risk**: Don't dodge, address head-on
5. **Clear ask**: They should know exactly what you want
6. **Time discipline**: Respect the 15-minute limit
7. **Confidence**: You've done the work, trust it

**You've got this.** The analysis is solid, the opportunity is real, the ask is reasonable.

Go get approval for that pilot. 🚀
