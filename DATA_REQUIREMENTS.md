# Research notebook inputs

Set `MVO_DATA_DIR` before starting Jupyter, and launch Jupyter from the repository
root. Required filenames in that directory depend on the notebook branch:

- `All_SwanBeta100_MVO2.xlsx` or `All_SwanBeta500.xlsx`: per-stock Swan-beta features.
- `MarketDD.xlsx` and `trainingMarketdrop.csv`: drawdown/training-event inputs.
- `optdata_MVO4.xlsx`: optimization inputs.
- `allocation weight.xlsx`: post-allocation rules, indexed by `stock selected`.

The notebook also generates intermediate CSV tables and retrieves market data
with yfinance. Do not substitute arbitrary workbooks: inspect the indexing and
column accesses in the notebook when constructing compatible inputs.

These workbooks are not redistributed. The full historical workflow has not been
rerun in the public package. `examples/synthetic_portfolio.py` is an independent,
self-contained mean-variance illustration with no private inputs and no network.
