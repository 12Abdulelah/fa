from collections.abc import Mapping

from fraud_service.domain.entities import Transaction
from fraud_service.service.scorer import FraudScorer


class FakeModel:
    model_version = "fake-v1"

    def __init__(self, probability: float) -> None:
        self.probability = probability
        self.last_features: Mapping[str, float | int] | None = None

    def predict_proba(self, features: Mapping[str, float | int]) -> float:
        self.last_features = features
        return self.probability


def test_scorer_uses_public_model_seam() -> None:
    model = FakeModel(0.9)
    scorer = FraudScorer(model=model, block_threshold=0.85)
    txn = Transaction(transaction_id="T-1", amount_sar=100.0, is_night=0)

    result = scorer.score(txn)

    assert result.decision == "block"
    assert result.model_version == "fake-v1"
    assert model.last_features is not None
    assert set(model.last_features) == {"amount_log", "is_night"}


def test_model_error_is_not_silently_swallowed() -> None:
    class BrokenModel:
        model_version = "broken"

        def predict_proba(self, features: Mapping[str, float | int]) -> float:
            raise RuntimeError("model unavailable")

    scorer = FraudScorer(model=BrokenModel(), block_threshold=0.85)
    txn = Transaction(transaction_id="T-2", amount_sar=100.0, is_night=0)

    try:
        scorer.score(txn)
    except RuntimeError as exc:
        assert str(exc) == "model unavailable"
    else:
        raise AssertionError("RuntimeError should propagate to the caller")
