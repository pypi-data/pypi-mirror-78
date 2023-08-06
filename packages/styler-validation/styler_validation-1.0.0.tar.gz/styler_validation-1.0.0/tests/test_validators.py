""" Tests for validators
"""

from decimal import Decimal
from unittest.mock import Mock
import random
import string

from styler_validation import validators as va
from styler_validation import messages as msg


class MyModel:
    pass


class TestIsRequired:
    def test_is_required(self):
        val = va.is_required()
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.REQUIRED_VALUE,)

    def test_valid(self):
        val = va.is_required()
        model = MyModel()
        model.prop = 'something'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_accepts(self):
        val = va.is_required(accepts={0})
        model = MyModel()
        model.prop = 0

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsInteger:
    def test_is_integer(self):
        val = va.is_integer()
        model = MyModel()
        model.prop = '123'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_is_none(self):
        val = va.is_integer()
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_type_mismatch(self):
        val = va.is_integer()
        model = MyModel()
        model.prop = {'123'}

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_value_mismatch(self):
        val = va.is_integer()
        model = MyModel()
        model.prop = 'abc123'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)


class TestIsBetween:
    def test_is_between(self):
        val = va.is_between(min_=0, max_=10)
        model = MyModel()
        model.prop = 2

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_outside_interval(self):
        val = va.is_between(min_=0, max_=10)
        model = MyModel()
        model.prop = 20
        model.prop2 = -1

        valid, error = val(model, 'prop')
        valid2, error2 = val(model, 'prop2')

        assert not valid
        assert error == (msg.LESS_OR_EQUAL_THAN, 10)
        assert not valid2
        assert error2 == (msg.GREATER_OR_EQUAL_THAN, 0)

    def test_no_interval_set(self):
        val = va.is_between()
        model = MyModel()
        model.prop = 20
        model.prop2 = -1

        valid, error = val(model, 'prop')
        valid2, error2 = val(model, 'prop2')

        assert valid
        assert error is None
        assert valid2
        assert error2 is None

    def test_one_sided_interval(self):
        val = va.is_between(min_=0)
        val2 = va.is_between(max_=10)
        model = MyModel()
        model.prop = 20
        model.prop2 = -1

        valid, error = val(model, 'prop')
        valid2, error2 = val(model, 'prop2')

        assert valid
        assert error is None
        assert not valid2
        assert error2 == (msg.GREATER_OR_EQUAL_THAN, 0)

        valid, error = val2(model, 'prop')
        valid2, error2 = val2(model, 'prop2')

        assert not valid
        assert error == (msg.LESS_OR_EQUAL_THAN, 10)
        assert valid2
        assert error2 is None

    def test_none(self):
        val = va.is_between(min_=0, max_=10)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_type_mismatch(self):
        val = va.is_between(min_=0, max_=10)
        model = MyModel()
        model.prop = {'123'}

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)


class TestIsInside:
    def test_is_inside(self):
        accepted_values = {'a', 'b'}
        val = va.is_inside(accepted=accepted_values)
        model = MyModel()
        model.prop = 'b'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_inside(self):
        accepted_values = {'a', 'b'}
        val = va.is_inside(accepted=accepted_values)
        model = MyModel()
        model.prop = 'c'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_none(self):
        accepted_values = {'a', 'b'}
        val = va.is_inside(accepted=accepted_values)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsOfType:
    def test_is_of_type(self):
        val = va.is_of_type(Decimal)
        model = MyModel()
        model.prop = Decimal('12.33')

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_type(self):
        val = va.is_of_type(Decimal)
        model = MyModel()
        model.prop = '12.33'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_none(self):
        val = va.is_of_type(Decimal)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsMoney:
    def test_is_money(self):
        val = va.is_money()
        model = MyModel()
        model.prop = Decimal('12.33')

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_allow_zero(self):
        val = va.is_money(allow_zero=False)
        model = MyModel()
        model.prop = Decimal('0.0')

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.NOT_ZERO,)

    def test_negative(self):
        val = va.is_money()
        model = MyModel()
        model.prop = Decimal('-12.33')

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.POSITIVE_VALUE,)

    def test_none(self):
        val = va.is_money()
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_type_mismatch(self):
        val = va.is_money()
        model = MyModel()
        model.prop = {'sdfads'}

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_value_mismatch(self):
        val = va.is_money()
        model = MyModel()
        model.prop = 'sdfads'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)


class TestIsValidTime:
    def test_is_valid_time(self):
        val = va.is_valid_time()
        model = MyModel()
        model.prop = '12:33'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_valid(self):
        val = va.is_valid_time()
        model = MyModel()
        model.prop = '12:73'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_TIME,)

    def test_none(self):
        val = va.is_valid_time()
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsGreaterThanField:
    def test_is_greater_than_field(self):
        val = va.is_greater_than_field('prop2')
        model = MyModel()
        model.prop = 333
        model.prop2 = 222

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_valid(self):
        val = va.is_greater_than_field('prop2')
        model = MyModel()
        model.prop = 11
        model.prop2 = 12

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.GREATER_THAN, 'mymodel.prop2')

    def test_none(self):
        val = va.is_greater_than_field('prop2')
        model = MyModel()
        model.prop = 1
        model.prop2 = None

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_default(self):
        val = va.is_greater_than_field('prop2', default=True)
        model = MyModel()
        model.prop = 1
        model.prop2 = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_allow_equal(self):
        val = va.is_greater_than_field('prop2', allow_equal=True)
        model = MyModel()
        model.prop = 1
        model.prop2 = 1

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsLessThanField:
    def test_is_less_than_field(self):
        val = va.is_less_than_field('prop2')
        model = MyModel()
        model.prop = 111
        model.prop2 = 222

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_valid(self):
        val = va.is_less_than_field('prop2')
        model = MyModel()
        model.prop = 13
        model.prop2 = 12

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.LESS_THAN, 'mymodel.prop2')

    def test_none(self):
        val = va.is_less_than_field('prop2')
        model = MyModel()
        model.prop = 1
        model.prop2 = None

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_default(self):
        val = va.is_less_than_field('prop2', default=True)
        model = MyModel()
        model.prop = 1
        model.prop2 = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_allow_equal(self):
        val = va.is_less_than_field('prop2', allow_equal=True)
        model = MyModel()
        model.prop = 1
        model.prop2 = 1

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsGreaterThanNumber:
    def test_is_greater_than_number(self):
        val = va.is_greater_than_number(10)
        model = MyModel()
        model.prop = 111

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_valid(self):
        val = va.is_greater_than_number(10)
        model = MyModel()
        model.prop = 1

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.GREATER_THAN, 10)

    def test_none(self):
        val = va.is_greater_than_number(10)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_default(self):
        val = va.is_greater_than_number(10, default=True)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_allow_equal(self):
        val = va.is_greater_than_number(10, allow_equal=True)
        model = MyModel()
        model.prop = 10

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsLessThanNumber:
    def test_is_less_than_number(self):
        val = va.is_less_than_number(10)
        model = MyModel()
        model.prop = 1

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_not_valid(self):
        val = va.is_less_than_number(10)
        model = MyModel()
        model.prop = 11

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.LESS_THAN, 10)

    def test_none(self):
        val = va.is_less_than_number(10)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_default(self):
        val = va.is_less_than_number(10, default=True)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_allow_equal(self):
        val = va.is_less_than_number(10, allow_equal=True)
        model = MyModel()
        model.prop = 10

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestIsNotEmpty:
    def test_is_not_empty(self):
        val = va.is_not_empty()
        model = MyModel()
        model.prop = 'something'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_invalid(self):
        val = va.is_not_empty()
        model = MyModel()
        model.prop = ' '

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.NOT_EMPTY,)

    def test_none(self):
        val = va.is_not_empty()
        model = MyModel()
        model.prop = 0

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_default(self):
        val = va.is_not_empty(default=True)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None


class TestObjectValidator:
    def test_child_object(self):
        child = Mock()
        child.is_valid.return_value = (True, {})
        model = MyModel()
        model.prop = child
        val = va.object_validator()

        valid, error = val(model, 'prop')

        assert valid
        assert error == {}
        child.is_valid.assert_called_once()

    def test_multiple_child_objects(self):
        child1 = Mock()
        child1.is_valid.return_value = (False, {'error1': 'error'})
        child2 = Mock()
        child2.is_valid.return_value = (True, {})
        child3 = Mock()
        child3.is_valid.return_value = (False, {'error3': 'error'})

        model = MyModel()
        model.prop = [child1, child2, child3]
        val = va.object_validator()

        valid, error = val(model, 'prop')

        assert not valid
        assert error == {
            'error1': 'error',
            'error3': 'error'
        }
        child1.is_valid.assert_called_once()
        child2.is_valid.assert_called_once()
        child3.is_valid.assert_called_once()

    def test_none(self):
        model = MyModel()
        model.prop = None
        val = va.object_validator()

        valid, error = val(model, 'prop')

        assert valid
        assert error == {}


class TestIsUuid:
    def test_is_uuid(self):
        val = va.is_uuid()
        model = MyModel()
        model.prop = '42fb4cf1-bd85-469c-8266-9dfcd54796a4'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_invalid(self):
        val = va.is_uuid()
        model = MyModel()
        model.prop = 'anything'

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)

    def test_none(self):
        val = va.is_uuid()
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_type_mismatch(self):
        val = va.is_uuid()
        model = MyModel()
        model.prop = 1234

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)


class TestIf_:
    def test_if_true(self):
        validation = Mock(return_value=(True, None))
        val = va.if_(lambda x: True, validation)
        model = MyModel()
        model.prop = '123'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None
        validation.assert_called_once()

    def test_if_false(self):
        validation = Mock(return_value=(True, None))
        val = va.if_(lambda x: False, validation)
        model = MyModel()
        model.prop = '123'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None
        validation.assert_not_called()


class TestMaxLength:
    def test_valid_max_length(self):
        val = va.max_length(255)
        model = MyModel()
        model.prop = 'string_with_length_under_255'

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_invalid_max_length(self):
        length = 255
        val = va.max_length(length)
        model = MyModel()
        model.prop = ''.join(random.choices(string.ascii_uppercase +
                                            string.digits, k=256))

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.STRING_TOO_LONG, length)

    def test_none(self):
        val = va.max_length(255)
        model = MyModel()
        model.prop = None

        valid, error = val(model, 'prop')

        assert valid
        assert error is None

    def test_invalid_type(self):
        val = va.max_length(255)
        model = MyModel()
        model.prop = 1

        valid, error = val(model, 'prop')

        assert not valid
        assert error == (msg.INVALID_VALUE,)
