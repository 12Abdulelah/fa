import math

from fraud_service.domain.entities import Transaction


def test_to_features_is_the_single_public_feature_contract() -> None:
    txn = Transaction(transaction_id="T-1", amount_sar=99.0, is_night=1)

    features = txn.to_features().values

    assert features == {"amount_log": math.log1p(99.0), "is_night": 1}
