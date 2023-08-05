from abc import ABCMeta
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    Choices,
    Field,
    IntegerChoices,
    IntegerField,
    TextChoices,
    TextField,
)

T = TypeVar("T", bound=Choices)
DBType = TypeVar("DBType")


class _ChoicesField(Field, Generic[T, DBType], metaclass=ABCMeta):
    def __init__(self, *, choice_type: Type[T], **kwargs):
        assert "choices" not in kwargs
        super().__init__(choices=choice_type.choices, **kwargs)
        self.choice_type = choice_type

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choice_type"] = self.choice_type
        del kwargs["choices"]
        return name, path, args, kwargs

    def to_python(self, value: Union[None, DBType, T]) -> Optional[T]:
        if isinstance(value, self.choice_type):
            return value
        if value is None:
            return None

        try:
            return self.choice_type(value)
        except ValueError:
            raise ValidationError(self.error_messages["invalid"], code="invalid")

    def from_db_value(
        self, value: Optional[DBType], expression, connection
    ) -> Optional[T]:
        if value is None:
            return None
        return self.choice_type(value)

    def get_prep_value(self, value: Optional[T]):
        if not isinstance(value, self.choice_type):
            value = self.choice_type(value)
        return super().get_prep_value(value.value)


IntegerChoicesT = TypeVar("IntegerChoicesT", bound=IntegerChoices)


class IntegerChoicesField(
    _ChoicesField[IntegerChoicesT, int], IntegerField, Generic[IntegerChoicesT]
):
    """
    TODO
    """

    pass


TextChoicesT = TypeVar("TextChoicesT", bound=TextChoices)


class CharChoicesField(
    _ChoicesField[TextChoicesT, str], CharField, Generic[TextChoicesT]
):
    """TODO"""

    pass


class TextChoicesField(
    _ChoicesField[TextChoicesT, str], TextField, Generic[TextChoicesT]
):
    """TODO"""

    pass
