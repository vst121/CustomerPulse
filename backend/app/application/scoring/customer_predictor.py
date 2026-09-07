from abc import ABC, abstractmethod

from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.scoring.customer_prediction import CustomerPrediction


class CustomerPredictor(ABC):
    @abstractmethod
    def predict(
        self,
        features: CustomerFeatures,
    ) -> CustomerPrediction:
        ...