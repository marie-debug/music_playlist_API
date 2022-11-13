from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


def validate(min,max,field):
        return fields.String(required=True, validate=And(Length(min=min, error= f'{field}  must be at least 3 characters long'),
        Length(
            max=max, error=f'{field} must be at less than  100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$',
                error= f'{field} Only letters, numbers and spaces are allowed')
    ))