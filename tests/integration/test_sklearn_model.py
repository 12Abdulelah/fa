from pathlib import Path

from fraud_service.adapters.sklearn_model import SklearnModel
from fraud_service.domain.entities import Transaction


def test_saved_model_through_public_adapter() -> None:
    model_path = Path(__file__).resolve().parents[2] / "models" / "fraud_model.joblib"
    model = SklearnModel.load(model_path)
    features = Transaction("T-1", amount_sar=100.0, is_night=0).to_features().values

    probability = model.predict_proba(features)

    assert 0.0 <= probability <= 1.0
    assert model.model_version == "v3.2.0"
