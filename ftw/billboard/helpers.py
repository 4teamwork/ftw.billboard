def format_currency(value, decimal_mark='.', thousands_separator=''):
    parts = str(value).split('.')
    if len(parts) > 1:
        intpart, floatpart = ''.join(parts[:-1]), parts[-1]
    else:
        intpart = str(value)
        floatpart = ''

    if not intpart:
        intpart = '0'

    if len(floatpart) > 2:
        floatpart = str(round(float('0.%s' % floatpart), 2))[2:]

    if thousands_separator:
        intpart = ''.join(reversed(intpart))
        # enumerate over the number.
        # if the counter divided by 3 is a full number
        # it inserts the char and the defined thousands_seperator. If it isn't
        # a full number only the char is inserted.
        intpart = [i % 3 == 0 and '%s%s' % (char, thousands_separator) or char
                   for i, char in enumerate(intpart)]
        intpart = ''.join(reversed(intpart))[:-1]

    if floatpart:
        return decimal_mark.join((intpart, floatpart))
    else:
        return intpart
