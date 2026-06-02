from strategies import (
    SMACrossoverStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
)

STRATEGIES = {
    "sma": SMACrossoverStrategy,
    "momentum": MomentumStrategy,
    "mean_reversion": MeanReversionStrategy,
}