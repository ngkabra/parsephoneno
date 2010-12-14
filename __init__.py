import re

number_punct_re = re.compile(r'[\s,.\-\(\)\[\]\{\}_]')
digits_re = re.compile(r'^\d+$')

class Error(Exception): pass

class MobileFormatError(Error): pass
class WrongCountryCodeError(MobileFormatError): pass
class WrongCountryCodeOrNumberTooLongError(WrongCountryCodeError): pass
class NumberTooShortError(MobileFormatError): pass
class IllegalCharactersError(MobileFormatError): pass

def canonical_number(number):
    '''Take a user entered mobile number and return a canonical number
    
    remove punctuation, and spaces.
    remove leading 91 or +91
    might raise Error

    Usage:
    >>> canonical_number('9822020096')
    '919822020096'
    >>> canonical_number('09822020096')
    '919822020096'
    >>> canonical_number(' 098220 20096')
    '919822020096'
    >>> canonical_number('919822020096')
    '919822020096'
    >>> canonical_number('+919822020096')
    '919822020096'
    >>> canonical_number('+91 9822020096')
    '919822020096'
    >>> canonical_number('+91 98220 20096')
    '919822020096'
    >>> canonical_number('+91-98220-20096')
    '919822020096'
    >>> canonical_number(' 982 202 0096 ')
    '919822020096'
    >>> canonical_number(' (982)202-0096 ')
    '919822020096'
    >>> canonical_number('+91 (982)202-0096 ')
    '919822020096'
    >>> canonical_number(None)
    >>> canonical_number('')
    >>> canonical_number(' ')
    >>> canonical_number('+91 (982)202-0096 x')
    Traceback (most recent call last):
    ...
    IllegalCharactersError: 9822020096x
    >>> canonical_number('xakljkl;a;lx[x!')
    Traceback (most recent call last):
    ...
    IllegalCharactersError: xakljkl;a;lxx!
    >>> canonical_number(' (982)202-009 ')
    Traceback (most recent call last):
    ...
    NumberTooShortError: 982202009
    >>> canonical_number('982202009 ')
    Traceback (most recent call last):
    ...
    NumberTooShortError: 982202009
    >>> canonical_number('982202009x')
    Traceback (most recent call last):
    ...
    IllegalCharactersError: 982202009x
    >>> canonical_number('98220200961')
    Traceback (most recent call last):
    ...
    WrongCountryCodeOrNumberTooLongError: 98220200961
    >>> canonical_number('9198220200961')
    Traceback (most recent call last):
    ...
    WrongCountryCodeOrNumberTooLongError: 9198220200961
    '''
    if not number: return None
    number = number_punct_re.sub('', number) # remove punctuation
    if not number: return None

    if number[0:1] == '+':
        if number[0:3] == '+91':
            number = number[3:] # remove country code
        else:
            raise WrongCountryCodeError(number)

    if number [0] == '0':
        number = number[1:]

    if not digits_re.match(number):
        raise IllegalCharactersError(number)
    digits = len(number)
    if digits > 10:
        if digits == 12 and number[0:2] == '91':
            number = number[2:]
        else:
            raise WrongCountryCodeOrNumberTooLongError(number)
    elif digits < 10:
        raise NumberTooShortError(number)
    return '91'+number

def phone_no(text):
    '''Return a phone number in a canonical format, or None in case of errors

    This is same as canonical_number, except that it does not throw any Exceptions.

    >>> phone_no('9822012345')
    '919822012345'
    >>> phone_no('98220 1234')
    >>> phone_no('+91 88220 12345')
    '918822012345'
    '''
    try:
        return canonical_number(text)
    except Error:
        return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    
