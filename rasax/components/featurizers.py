import os
import typing
from typing import Any, Optional, Text, Dict, List, Type

import fasttext

import numpy as np
from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.constants import TEXT, FEATURE_TYPE_SENTENCE, FEATURE_TYPE_SEQUENCE
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.features import Features
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.utils.hugging_face.hf_transformers import HFTransformersNLP
from rasa.nlu.constants import (
    DENSE_FEATURIZABLE_ATTRIBUTES,
    FEATURIZER_CLASS_ALIAS,
    TOKENS_NAMES,
)

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class FastTextFeaturizer(DenseFeaturizer):
    """This component adds fasttext features."""

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        return [Tokenizer]

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["fasttext"]

    defaults = {"file": None, "cache_dir": None}
    language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        if "cache_dir" not in component_config.keys():
            raise ValueError("You need to set `cache_dir` for the FasttextFeaturizer.")
        if "file" not in component_config.keys():
            raise ValueError("You need to set `file` for the FasttextFeaturizer.")
        path = os.path.join(component_config["cache_dir"], component_config["file"])

        if not os.path.exists(component_config["cache_dir"]):
            raise FileNotFoundError(
                f"It seems that the cache dir {component_config['cache_dir']} does not exists. Please check config."
            )
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"It seems that file {path} does not exists. Please check config."
            )

        self.model = fasttext.load_model(path)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_features(example, attribute)

    def set_fasttext_features(self, message: Message, attribute: Text = TEXT) -> None:
        tokens = message.get(TOKENS_NAMES[attribute])

        if not tokens:
            return None

        # We need to reshape here such that the shape is equivalent to that of sparsely
        # generated features. Without it, it'd be a 1D tensor. We need 2D (n_utterance, n_dim).
        text_vector = self.model.get_word_vector(message.get(TEXT)).reshape(1, -1)
        word_vectors = np.array([self.model.get_word_vector(t.text) for t in tokens])

        final_sequence_features = Features(
            word_vectors,
            FEATURE_TYPE_SEQUENCE,
            attribute,
            self.component_config[FEATURIZER_CLASS_ALIAS],
        )
        message.add_features(final_sequence_features)
        final_sentence_features = Features(
            text_vector,
            FEATURE_TYPE_SENTENCE,
            attribute,
            self.component_config[FEATURIZER_CLASS_ALIAS],
        )
        message.add_features(final_sentence_features)

    def process(self, message: Message, **kwargs: Any) -> None:
        self.set_fasttext_features(message)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component

        return cls(meta)


class HFTransformersPhobert(HFTransformersNLP):

    def _load_model_instance(self, skip_model_load: bool) -> None:
        """Try loading the model instance.

        Args:
            skip_model_load: Skip loading the model instances to save time.
            This should be True only for pytests
        """
        if skip_model_load:
            # This should be True only during pytests
            return

        print(f"Loading Tokenizer and Model for {self.model_name}")

        from rasa.nlu.utils.hugging_face.registry import (
                model_class_dict,
                model_tokenizer_dict,
            )

        if self.model_weights.startswith("vinai/phobert"):
            from transformers import PhobertTokenizer
            self.tokenizer = PhobertTokenizer.from_pretrained(
                self.model_weights, cache_dir=self.cache_dir
            )

        else:
            self.tokenizer = model_tokenizer_dict[self.model_name].from_pretrained(
                self.model_weights, cache_dir=self.cache_dir
            )

        self.model = model_class_dict[self.model_name].from_pretrained(
            self.model_weights, cache_dir=self.cache_dir
        )

        # Use a universal pad token since all transformer architectures do not have a
        # consistent token. Instead of pad_token_id we use unk_token_id because
        # pad_token_id is not set for all architectures. We can't add a new token as
        # well since vocabulary resizing is not yet supported for TF classes.
        # Also, this does not hurt the model predictions since we use an attention mask
        # while feeding input.
        self.pad_token_id = self.tokenizer.unk_token_id