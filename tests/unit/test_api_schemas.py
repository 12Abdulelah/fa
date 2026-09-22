from fraud_service.api.schemas import TransactionRequest
from fraud_service.domain.entities import Transaction


def test_api_schema_maps_to_domain_without_schema_leakage() -> None:
    request = TransactionRequest(
        transaction_id="T-1",
        amount_sar=50.0,
        is_night=1,
        channel="online",
    )

    domain = request.to_domain()

    assert isinstance(domain, Transaction)
    assert domain.transaction_id == "T-1"
