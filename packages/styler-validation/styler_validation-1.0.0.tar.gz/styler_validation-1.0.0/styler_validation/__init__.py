"""Top-level package for Styler Validation."""


class ValidatorMixin:
    """ Adds validation behavior to models
    """

    validates = []

    def is_valid(self, prefix=None, index=None, custom=None):
        """ Validates all fields with validation rules

            Args:
                prefix: prefix string before each field (default = class name)
                index: index used in messages with collections
                custom: overrides the default validates
        """
        if not prefix:
            prefix = self.__class__.__name__.lower()
        if not index:
            index = ''
        else:
            index = f'[{index}]'

        errors = {}
        validators = custom if custom else self.validates
        for validation in validators:
            field, *rules = validation
            for rule in rules:
                result, error = rule(self, field)
                if not result:
                    errors[f'{prefix}{index}.{field}'] = error
                    break
        if errors:
            return (False, errors)
        return (True, errors)
