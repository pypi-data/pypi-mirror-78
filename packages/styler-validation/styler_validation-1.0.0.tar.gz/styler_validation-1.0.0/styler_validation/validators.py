""" Common validators
"""

import re
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from uuid import UUID

from styler_validation import messages as msg


def is_required(accepts=None):
    """ Generates a validator to validate if the property
        is set with a not falsy value.

        Args:
            accepts: a collection of values that it accepts as truthy
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if accepts and value in accepts:
            return (True, None)
        if not value:
            return (False, (msg.REQUIRED_VALUE,))
        return (True, None)

    return wrapper


def is_integer():
    """ Generates a validator to validate if the value
        of a property is an integer.
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        try:
            int(value)
        except ValueError:
            return (False, (msg.INVALID_VALUE,))
        except TypeError:
            return (False, (msg.INVALID_VALUE,))
        return (True, None)

    return wrapper


def is_between(min_=None, max_=None):
    """ Generates a validator to validate if a property
        is within a min_ and max_ value.

        Args:
            min_: the lower threshold
            max_: the upper threshold
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if (not value and value != 0):
            return (True, None)
        try:
            if (min_ or min_ == 0) and value < min_:
                return (False, (msg.GREATER_OR_EQUAL_THAN, min_))
            if (max_ or max_ == 0) and value > max_:
                return (False, (msg.LESS_OR_EQUAL_THAN, max_))
            return (True, None)
        except TypeError:
            return (False, (msg.INVALID_VALUE,))

    return wrapper


def is_inside(accepted):
    """ Generates a validator to validate if the value
        of a property belongs to a collection of accepted
        values.

        Args:
            accepted: the collection of accepted values
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        if value not in accepted:
            return (False, (msg.INVALID_VALUE,))
        return (True, None)

    return wrapper


def is_of_type(type_):
    """ Generates a validator to validate if the value
        of a property is of a specific type.

        Args:
            type_: the type
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        if not isinstance(value, type_):
            return (False, (msg.INVALID_VALUE,))
        return (True, None)

    return wrapper


def is_money(allow_zero=True):
    """ Generates a validator to validate if the value
        of a property is of a specific type.

        Args:
            allow_zero: should allow zero or not
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        try:
            value = Decimal(value)
            if value < Decimal('0.0'):
                return (False, (msg.POSITIVE_VALUE,))
            if not allow_zero and value == Decimal('0.0'):
                return (False, (msg.NOT_ZERO,))
        except TypeError:
            return (False, (msg.INVALID_VALUE,))
        except InvalidOperation:
            return (False, (msg.INVALID_VALUE,))
        return (True, None)

    return wrapper


def is_valid_time():
    """ Generates a validator to validate if the property
        is a valid time format (HH:MM)
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        if not re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', value):
            return (False, (msg.INVALID_TIME,))
        return (True, None)

    return wrapper


def is_greater_than_field(target_prop, allow_equal=False, default=False):
    """ Generates a validator to validate if the value
        is greater than target prop's value.

        Args:
            target_prop: property name to be compared with
            allow_equal: should allow equal or not
            default: value returned if target_prop is empty
    """
    def wrapper(obj, prop):
        value_1 = getattr(obj, prop)
        value_2 = getattr(obj, target_prop)
        if (not value_1 and value_1 != 0) or (not value_2 and value_2 != 0):
            return (True, None) if default else (False, (msg.INVALID_VALUE,))
        class_prefix = obj.__class__.__name__.lower()
        if allow_equal:
            return (True, None) if value_1 >= value_2 else (
                False,
                (msg.GREATER_OR_EQUAL_THAN, f'{class_prefix}.{target_prop}'))
        else:
            return (True, None) if value_1 > value_2 else (
                False, (msg.GREATER_THAN, f'{class_prefix}.{target_prop}'))

    return wrapper


def is_less_than_field(target_prop, allow_equal=False, default=False):
    """ Generates a validator to validate if the value
        is less than target prop's value.

        Args:
            target_prop: property name to be compared with
            allow_equal: should allow equal or not
            default: value returned if target_prop is empty
    """
    def wrapper(obj, prop):
        value_1 = getattr(obj, prop)
        value_2 = getattr(obj, target_prop)
        if (not value_1 and value_1 != 0) or (not value_2 and value_2 != 0):
            return (True, None) if default else (False, (msg.INVALID_VALUE,))
        class_prefix = obj.__class__.__name__.lower()
        if allow_equal:
            return (True, None) if value_1 <= value_2 else (
                False, (
                    msg.LESS_OR_EQUAL_THAN, f'{class_prefix}.{target_prop}'))
        else:
            return (True, None) if value_1 < value_2 else (
                False, (msg.LESS_THAN, f'{class_prefix}.{target_prop}'))

    return wrapper


def is_greater_than_number(target, allow_equal=False, default=False):
    """ Generates a validator to validate if the value
        is greater than target number.

        Args:
            target: target number to be compared with
            allow_equal: should allow equal or not
            default: value returned if target_prop is empty
    """
    def wrapper(obj, prop):
        value_1 = getattr(obj, prop)
        value_2 = target
        if (not value_1 and value_1 != 0):
            return (True, None) if default else (False, (msg.INVALID_VALUE,))
        if allow_equal:
            return (True, None) if value_1 >= value_2 else (
                False, (msg.GREATER_OR_EQUAL_THAN, target))
        else:
            return (True, None) if value_1 > value_2 else (
                False, (msg.GREATER_THAN, target))

    return wrapper


def is_less_than_number(target, allow_equal=False, default=False):
    """ Generates a validator to validate if the value
        is less than target number.

        Args:
            target: number to be compared with
            allow_equal: should allow equal or not
            default: value returned if target_prop is empty
    """
    def wrapper(obj, prop):
        value_1 = getattr(obj, prop)
        value_2 = target
        if (not value_1 and value_1 != 0):
            return (True, None) if default else (False, (msg.INVALID_VALUE,))
        if allow_equal:
            return (True, None) if value_1 <= value_2 else (
                False, (msg.LESS_OR_EQUAL_THAN, target))
        else:
            return (True, None) if value_1 < value_2 else (
                False, (msg.LESS_THAN, target))

    return wrapper


def is_not_empty(default=False):
    """ Generates a validator to validate if the value
        is empty.
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if not value:
            return (True, None) if default else (False, (msg.INVALID_VALUE,))
        if not value.strip():
            return (False, (msg.NOT_EMPTY,))
        return (True, None)
    return wrapper


def object_validator():
    """ Generates a validator to validate a child object.
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if not value:
            return (True, {})
        if isinstance(value, Iterable):
            errors = {}
            for i, obj in enumerate(value):
                status, error = obj.is_valid(index=i)
                if not status:
                    errors.update(error)
            return (True, None) if not errors else (False, errors)
        else:
            return value.is_valid()

    return wrapper


def is_uuid(version=4):
    """ Generates a validator to validate if the value
        of a property is an integer.
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        try:
            _ = UUID(value, version=version)
        except ValueError:
            return (False, (msg.INVALID_VALUE,))
        except (AttributeError, TypeError):
            return (False, (msg.INVALID_VALUE,))
        return (True, None)

    return wrapper


def if_(condition_func, validation_func):
    """ Generates a validator to conditionally run a validation function

        Args:
            condition_func: a function that evaluates to a boolean
            validation_func: a validation function to apply
    """
    def wrapper(obj, prop):
        if not condition_func(obj):
            return (True, None)
        return validation_func(obj, prop)

    return wrapper


def max_length(length):
    """ Generates a validator to validate if a string
        is no longer than target prop's value.
        Args:
            length: max length of string
    """
    def wrapper(obj, prop):
        value = getattr(obj, prop)
        if value is None:
            return (True, None)
        if not isinstance(value, str):
            return (False, (msg.INVALID_VALUE,))
        if len(value) > length:
            return (False, (msg.STRING_TOO_LONG, length))
        return (True, None)

    return wrapper
