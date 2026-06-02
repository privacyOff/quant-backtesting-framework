import pytest

from cli.registry import (
    STRATEGIES,
)

from cli.commands import (
    list_strategies,
    show_version,
)

from strategies import (
    SMACrossoverStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
)


def test_registry_contains_sma():

    assert "sma" in STRATEGIES


def test_registry_contains_momentum():

    assert (
        "momentum"
        in STRATEGIES
    )


def test_registry_contains_mean_reversion():

    assert (
        "mean_reversion"
        in STRATEGIES
    )


def test_sma_lookup():

    assert (
        STRATEGIES["sma"]
        is SMACrossoverStrategy
    )


def test_momentum_lookup():

    assert (
        STRATEGIES["momentum"]
        is MomentumStrategy
    )


def test_mean_reversion_lookup():

    assert (
        STRATEGIES[
            "mean_reversion"
        ]
        is MeanReversionStrategy
    )


def test_invalid_strategy():

    with pytest.raises(
        KeyError
    ):
        STRATEGIES["invalid"]


def test_show_version():

    assert (
        show_version()
        == "Quant Backtester v1.0.0"
    )


def test_list_strategies():

    strategies = (
        list_strategies()
    )

    assert "sma" in strategies
    assert "momentum" in strategies

    assert (
        "mean_reversion"
        in strategies
    )