""" Tests for the base ValidatorMixin
"""

from unittest.mock import Mock

from styler_validation import ValidatorMixin


class TestIsValid:
    def test_is_valid(self):
        class MyModelValidator(ValidatorMixin):
            validates = [
                ('prop', Mock(name='validator', return_value=(True, None)))
            ]
        model = MyModelValidator()
        model.prop = '123'

        model.is_valid()

        MyModelValidator.validates[0][1].assert_called_with(model, 'prop')

    def test_override_rules(self):
        class MyModelValidator(ValidatorMixin):
            validates = [
                ('prop', Mock(name='validator', return_value=(True, None)))
            ]
        model = MyModelValidator()
        model.prop2 = '123'
        val = Mock(return_value=(True, None), name='other')

        model.is_valid(custom=[('prop2', val)])

        MyModelValidator.validates[0][1].assert_not_called()
        val.assert_called_with(model, 'prop2')

    def test_prefix(self):
        class MyModelValidator(ValidatorMixin):
            validates = [
                ('prop', Mock(name='validator', return_value=(False, 'error')))
            ]
        model = MyModelValidator()
        model.prop2 = '123'

        result, errors = model.is_valid(prefix='abc')

        assert not result
        assert errors == {
            'abc.prop': 'error'
        }

    def test_index(self):
        class MyModelValidator(ValidatorMixin):
            validates = [
                ('prop', Mock(name='validator', return_value=(False, 'error')))
            ]
        model = MyModelValidator()
        model.prop2 = '123'

        result, errors = model.is_valid(prefix='abc', index=22)

        assert not result
        assert errors == {
            'abc[22].prop': 'error'
        }
