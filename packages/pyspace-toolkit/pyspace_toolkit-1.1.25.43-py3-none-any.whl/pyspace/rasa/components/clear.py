
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig

from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

class ClearSparseFeatures(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(ClearSparseFeatures, self).__init__(component_config)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            
            del message.data[SPARSE_FEATURE_NAMES[TEXT]]

    def process(self, message: Message, **kwargs: Any):

        del message.data[SPARSE_FEATURE_NAMES[TEXT]]
