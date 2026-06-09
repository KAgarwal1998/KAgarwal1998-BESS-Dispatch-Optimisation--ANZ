# Methodology — ANZ Multi-Market BESS Dispatch

Plain-language explanation so you can defend every part in an interview.

## The Australian market context (why this model is ANZ-specific)

Australia is now the world's third-largest utility battery market. The federal
**Capacity Investment Scheme (CIS)** underwrites clean dispatchable capacity
(14 GW storage target by 2030), and batteries are the **largest provider of FCAS**
in the NEM. A NEM battery earns from three things at once:

1. **Energy arbitrage** — buy at low spot prices (RRP), sell at high.
2. **Contingency FCAS** — paid to stand ready to respond to sudden grid events.
3. **Regulation FCAS** — paid to continuously fine-tune frequency.

## The 10 FCAS markets

The NEM has **ten FCAS markets**, split into two functions:
- **8 contingency markets** — respond to big disturbances (a generator tripping).
  Four *raise* (R6SEC, R60SEC, R5MIN, **R1SEC**) and four *lower* (L6SEC, L60SEC,
  L5MIN, **L1SEC**). The number is the response time in seconds (or 5 minutes).
  **R1SEC / L1SEC are the "Very Fast" 1-second services**, introduced October 2023,
  which batteries are uniquely suited to because they respond near-instantly.
- **2 regulation markets** (RAISEREG, LOWERREG) — continuous, every-4-second
  adjustments via AEMO's Automatic Generation Control (AGC).

**Crucial distinction:** contingency FCAS is paid on *enabled capacity* (MW held
ready) whether or not it's ever called — so it earns revenue with almost no energy
throughput and little degradation. Regulation is *utilised* — the battery actually
moves energy to follow the AGC signal — so it carries a real throughput/degradation
cost. The model reflects this: regulation enablement adds a cycle cost, contingency
doesn't.

## Co-optimisation — the core idea

A battery has *one* power rating and *one* energy store. It can't sell the same MW
into energy and FCAS simultaneously. So all markets must be **co-optimised**: the
optimiser decides how to split the battery's power and headroom across energy,
contingency and regulation in every 5-minute interval to maximise total revenue.

This is a **linear program** (scipy HiGHS). Decision variables per interval:
charge, discharge, four raise-enablements, four lower-enablements, raise-reg,
lower-reg. The binding constraints are:

- **Power headroom up:** `discharge + Σ raise_enablement + raise_reg ≤ P`
  (you can only offer raise FCAS with discharge headroom you're not using).
- **Power headroom down:** `charge + Σ lower_enablement + lower_reg ≤ P`.
- **State of charge:** cumulative energy (including regulation utilisation) stays
  within `[SoC_min, SoC_max]`.

Linear ⇒ fast and globally optimal (no local-optimum risk).

### Why round-trip efficiency is split
RTE (88%) is energy-out ÷ energy-in over a full cycle. Modelled as `√RTE` on each
leg so the two multiply back to the round-trip loss — standard, avoids
double-counting.

### Why a cycle cost
Each charge/discharge cycle ages the battery. A marginal AUD/MWh throughput cost
stops the optimiser cycling for trivial spreads that would cost more in degradation
than they earn. Regulation also incurs this (it's utilised); contingency mostly
doesn't (it's only enabled). This is why FCAS — especially contingency — is
attractive: revenue with little wear.

## The CIS cap-and-floor contract

The defining ANZ revenue mechanism. Under a CIS agreement (10–15 year term):
- If merchant revenue falls **below the floor**, the government tops it up to the
  floor → **downside protection**, which is what makes projects bankable.
- If merchant revenue rises **above the ceiling**, the project keeps the ceiling
  plus part of the excess and pays back the rest (here 50%) → **upside sharing**.

The effect (see `cis_cap_floor.png`): a flat floor on the left, then 1:1 with
merchant in the band, then a shallower slope above the ceiling. It compresses the
revenue distribution — lower upside, but a guaranteed floor — which is exactly the
risk profile lenders want. This is why CIS unlocked billions in battery investment.

## Reading the results

- **Energy-only vs full-stack:** energy alone captures roughly half of full-stack
  revenue. Stacking FCAS roughly doubles it — the single most important takeaway.
- **Very Fast (R1/L1) uplift:** modest in the base case but grows when fast-service
  prices spike during system stress; batteries dominate these markets.
- **Duration sweep:** revenue rises with duration but with *declining marginal
  value* — a 4-hour battery doesn't earn 2× a 2-hour one, because the extra energy
  captures progressively smaller price spreads. This informs sizing.

## Benchmarking (keeping it honest)

Modo Energy reported NEM battery net revenues swinging through 2025: ~AUD 157k/MW
(July), 215k (August), 85k (September) — extreme volatility as grid conditions
changed. The model's ~AUD 200k/MW sits at the higher end, consistent with a
volatile summer month. **Annual figures should average across calm and volatile
months** — don't annualise a single hot month naïvely. Use real AEMO data across a
full year before quoting numbers to anyone.

## Limitations to own
- **Perfect foresight:** the LP sees the whole day's prices → a revenue *ceiling*,
  not what a real battery captures running on forecasts.
- **Price-taker:** the battery's dispatch doesn't move prices (fine at 100 MW,
  less so at very large scale).
- **FCAS energy security** approximated as a SoC reserve, not the full enablement-
  vs-deliverability co-optimisation AEMO's dispatch engine enforces.
- **CIS** modelled as an annual cap-and-floor, not the exact half-hourly settlement.
- Daily SoC reset; no multi-day energy shifting.
