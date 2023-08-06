# coding=utf-8
# Copyright (c) 2020, VinAI Research and the HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" TF 2.0 PhoBERT model """

import logging

from .configuration_phobert import PhobertConfig
from .file_utils import add_start_docstrings
from .modeling_tf_roberta import (
    TFRobertaForMaskedLM,
    TFRobertaForMultipleChoice,
    TFRobertaForQuestionAnswering,
    TFRobertaForSequenceClassification,
    TFRobertaForTokenClassification,
    TFRobertaModel,
)


logger = logging.getLogger(__name__)

_TOKENIZER_FOR_DOC = "PhobertTokenizer"

TF_PHOBERT_PRETRAINED_MODEL_ARCHIVE_LIST = [
    "vinai/phobert-base",
    "vinai/phobert-large",
    # See all BERTweet models at https://huggingface.co/models?filter=phobert
]

PHOBERT_START_DOCSTRING = r"""

    This model is a `tf.keras.Model <https://www.tensorflow.org/api_docs/python/tf/keras/Model>`__ sub-class.
    Use it as a regular TF 2.0 Keras Model and
    refer to the TF 2.0 documentation for all matter related to general usage and behavior.

    Parameters:
        config (:class:`~transformers.PhobertConfig`): Model configuration class with all the parameters of the
            model. Initializing with a config file does not load the weights associated with the model, only the configuration.
            Check out the :meth:`~transformers.PreTrainedModel.from_pretrained` method to load the model weights.
"""


@add_start_docstrings(
    "The bare PhoBERT Model transformer outputting raw hidden-states without any specific head on top.",
    PHOBERT_START_DOCSTRING,
)
class TFPhobertModel(TFRobertaModel):
    """
    This class overrides :class:`~transformers.TFRobertaModel`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig


@add_start_docstrings(
    """PhoBERT Model with a `language modeling` head on top. """,
    PHOBERT_START_DOCSTRING,
)
class TFPhobertForMaskedLM(TFRobertaForMaskedLM):
    """
    This class overrides :class:`~transformers.TFRobertaForMaskedLM`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig


@add_start_docstrings(
    """PhoBERT Model transformer with a sequence classification/regression head on top (a linear layer
    on top of the pooled output) e.g. for GLUE tasks. """,
    PHOBERT_START_DOCSTRING,
)
class TFPhobertForSequenceClassification(TFRobertaForSequenceClassification):
    """
    This class overrides :class:`~transformers.TFRobertaForSequenceClassification`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig


@add_start_docstrings(
    """PhoBERT Model with a multiple choice classification head on top (a linear layer on top of
    the pooled output and a softmax) e.g. for RocStories/SWAG tasks. """,
    PHOBERT_START_DOCSTRING,
)
class TFPhobertForMultipleChoice(TFRobertaForMultipleChoice):
    """
    This class overrides :class:`~transformers.TFRobertaForMultipleChoice`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig


@add_start_docstrings(
    """PhoBERT Model with a token classification head on top (a linear layer on top of
    the hidden-states output) e.g. for Named-Entity-Recognition (NER) tasks. """,
    PHOBERT_START_DOCSTRING,
)
class TFPhobertForTokenClassification(TFRobertaForTokenClassification):
    """
    This class overrides :class:`~transformers.TFRobertaForTokenClassification`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig


@add_start_docstrings(
    """PhoBERT Model with a span classification head on top for extractive question-answering tasks like SQuAD
    (a linear layers on top of the hidden-states output to compute `span start logits` and `span end logits` """,
    PHOBERT_START_DOCSTRING,
)
class TFPhobertForQuestionAnswering(TFRobertaForQuestionAnswering):
    """
    This class overrides :class:`~transformers.TFRobertaForQuestionAnswering`. Please check the
    superclass for the appropriate documentation alongside usage examples.
    """

    config_class = PhobertConfig
