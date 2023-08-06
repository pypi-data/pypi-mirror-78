from dataclasses import dataclass as python_dataclass, field
from typing import Any, List

from marshmallow import ValidationError
from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@dataclass
@python_dataclass
class AbstractQuestionWithOptions(Serializable):

    def retrieve_answers(self):
        answers = []
        options_len = len(self.options)
        for answer_id in self.answers:
            if answer_id >= options_len:
                raise ValidationError({
                    'answers': f'No existing option has been picked! Answer id: {answer_id}. Options length: {options_len}.'
                })

            answer = self.options[answer_id]
            answers.append(answer)

        return answers

@dataclass
@python_dataclass
class ChoiseQuestion(AbstractQuestionWithOptions):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)
    label: str = None

    repr_type: str = None

    id: int = None


@dataclass
@python_dataclass
class SelectQuestion(AbstractQuestionWithOptions):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)
    label: str = None

    repr_type: str = None

    id: int = None


@dataclass
@python_dataclass
class MultipleSelectQuestion(AbstractQuestionWithOptions):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)
    label: str = None

    repr_type: str = None

    id: int = None


@dataclass
@python_dataclass
class CheckBoxQuestion(AbstractQuestionWithOptions):
    options: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)
    label: str = None

    repr_type: str = None

    id: int = None


@dataclass
@python_dataclass
class RangeQuestion(Serializable):
    answers: List[Any] = field(default_factory=list)
    min_value: float = None
    max_value: float = None
    label: str = None

    repr_type: str = None

    id: int = None


@dataclass
@python_dataclass
class TextFieldQuestion(Serializable):
    answers: List[Any] = field(default_factory=list)
    shadow_title: str = None
    validation_type: str = None
    label: str = None

    repr_type: str = None

    id: int = None
