
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

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
from pyspace.nlp.toolkit.zemberek import normalize, lemmatize

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

class ZemberekNormalizer(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            norm = normalize(message.text)

            message.text = norm
            message.set(TEXT, norm)
            

    def process(self, message: Message, **kwargs: Any):

        norm = normalize(message.text)

        message.text = norm
        message.set(TEXT, norm)


class ZemberekLemmatizer(Component):
    
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            tokens = message.data["tokens"]
            tokens = [lemmatize(t.text) for t in tokens]

            norm = " ".join(tokens)
            message.text = norm
            message.set(TEXT, norm)
            
            tokens = Tokenizer._convert_words_to_tokens(tokens, norm)
            tokens = Tokenizer.add_cls_token(tokens, TEXT)
            message.set(TOKENS_NAMES[TEXT], tokens)

            

    def process(self, message: Message, **kwargs: Any):

        tokens = message.data["tokens"]
        tokens = [lemmatize(t.text) for t in tokens]

        norm = " ".join(tokens)
        message.text = norm
        message.set(TEXT, norm)
        
        tokens = Tokenizer._convert_words_to_tokens(tokens, norm)
        tokens = Tokenizer.add_cls_token(tokens, TEXT)
        message.set(TOKENS_NAMES[TEXT], tokens)
