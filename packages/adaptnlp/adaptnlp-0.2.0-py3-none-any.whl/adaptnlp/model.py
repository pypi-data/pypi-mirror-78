from typing import Union, List
from pathlib import Path
from abc import ABC, abstractmethod

from flair.data import Sentence


class AdaptiveModel(ABC):
    @abstractmethod
    def load(
        self,
        model_name_or_path: Union[str, Path],
    ):
        """ Load model into the `AdaptiveModel` object as alternative constructor """
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def predict(
        self,
        text: Union[List[Sentence], Sentence, List[str], str],
        mini_batch_size: int = 32,
        **kwargs,
    ) -> List[Sentence]:
        """ Run inference on the model """
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def train(
        self,
    ) -> None:
        """ Evaluate on the model """
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def evaluate(
        self,
    ) -> None:
        """ Evaluate on the model """
        raise NotImplementedError("Please Implement this method")
