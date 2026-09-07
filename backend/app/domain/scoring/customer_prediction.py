from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CustomerPrediction:
    churn_probability: Decimal

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.churn_probability <= Decimal("1"):
            raise ValueError(
                "churn_probability must be between 0 and 1."
            )