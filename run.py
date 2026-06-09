{
  "_meta": {
    "name": "ANZ BESS base case",
    "description": "Grid-scale BESS in the NEM. Market structure & benchmarks reflect 2025 AEMO/Modo data; figures indicative.",
    "currency": "AUD",
    "region": "QLD1",
    "benchmark_note": "NEM BESS net revenue 2025 ranged ~AU$85k-215k/MW/yr (Modo Energy); high volatility."
  },
  "battery": {
    "power_mw": 100.0,
    "duration_h": 2.0,
    "rte": 0.88,
    "soc_min_frac": 0.05,
    "soc_max_frac": 0.95,
    "cycle_cost_per_mwh": 4.5,
    "max_cycles_per_day": 1.5,
    "degradation_per_cycle": 0.000045
  },
  "fcas": {
    "_comment": "10 FCAS markets: 4 contingency-raise (R6/R60/R5/R1), 4 contingency-lower (L6/L60/L5/L1), 2 regulation (RREG/LREG). Modelled as raise/lower bundles + regulation. R1/L1 = Very Fast (1s), live since Oct 2023.",
    "enable_fcas": true,
    "enable_regulation": true,
    "enable_very_fast": true,
    "raise_services": ["R6SEC", "R60SEC", "R5MIN", "R1SEC"],
    "lower_services": ["L6SEC", "L60SEC", "L5MIN", "L1SEC"],
    "regulation_utilisation": 0.15,
    "regulation_throughput_cost": true
  },
  "contract": {
    "_comment": "CIS cap-and-floor: govt covers shortfall below floor; claws back 50% of revenue above ceiling. 10-15yr term.",
    "cis_enabled": true,
    "revenue_floor_per_mw_yr": 95000,
    "revenue_ceiling_per_mw_yr": 200000,
    "ceiling_clawback_frac": 0.50,
    "contract_term_yrs": 14
  },
  "market": {
    "_comment": "Synthetic price scale; replace with real AEMO data via fetch_aemo_data.py.",
    "region": "QLD1",
    "negative_price_frequency": 0.08,
    "volatility_regime": "medium"
  }
}
