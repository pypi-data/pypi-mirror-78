import logging
import typing
from typing import Any, Dict, Optional, Text, List

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.training_data import Message, TrainingData

logger = logging.getLogger(__name__)


if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class OneCharTokenizer(Tokenizer):
    """自定义中文分词组件"""

    # provides = ["tokens"]
    language_list = ["zh"]

    defaults = {
        "custom_dict": None,
        # Flag to check whether to split intents
        "intent_tokenization_flag": False,
        # Symbol on which intent should be split
        "intent_split_symbol": "_",
    }  # default don't load custom dictionary

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        tokenized = [i for i in text]
        tokens = []
        offset = 0
        for word in tokenized:
            tokens.append(Token(word, offset))
            offset += len(word)

        return tokens
