=================
Styler Validation
=================


.. image:: https://img.shields.io/pypi/v/styler_validation.svg
        :target: https://pypi.python.org/pypi/styler_validation

.. image:: https://github.com/STYLER-Inc/styler-validation/workflows/Python%20package/badge.svg


Validators to be used as mixins in models


* Free software: MIT license


Usage
-----

Install from pypi::

        pip install styler-validation

Set validation rules for a class

.. code-block:: python

        from styler_validation import ValidatorMixin
        from styler_validation import validators as va


        class User(ValidatorMixin):
            validates = [
                ('name', va.is_required()),
                ('age', va.is_required(), va.is_integer())
            ]
        
        my_user = User()
        result, errors = my_user.is_valid()

        print(result)   # False
        print(errors)   # {'user.name': ('required_value',), 'user.age': ('required_value',)}

        my_user.name = 'John Doe'
        my_user.age = 'nine'
        result, errors = my_user.is_valid()

        print(result)   # False
        print(errors)   # {'user.age': ('invalid_value',)}

