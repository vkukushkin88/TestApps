
import re

MAX_ARAB = 3999
ROME_NUM_LIST = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M']
ARAB_NUM_LIST = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
ROME_ARAB_DICT = dict(zip(ROME_NUM_LIST, ARAB_NUM_LIST))
ROME_NUMBER_PATTERN = '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'


def arab_to_rome(num):
    if num < 0 or num > MAX_ARAB:
        raise ValueError('Arabian number should be in range between 1 and %s' % (MAX_ARAB))

    res = []
    for i in xrange(len(ARAB_NUM_LIST) - 1, -1, -1):
        local_num = num / ARAB_NUM_LIST[i]
        num %= ARAB_NUM_LIST[i]
        if local_num % 5 > 3:
            res.append(ROME_NUM_LIST[i] + ROME_NUM_LIST[i + 1])
        else:
            res.append(ROME_NUM_LIST[i] * (local_num % 5))

    return ''.join(res)


def rome_to_arab(rome_num_str):
    rome_num_str.upper()
    i = 0
    res = 0
    if not re.match(ROME_NUMBER_PATTERN, rome_num_str):
        print 'WARNING: "%s" number is not valid, translation could be wrong' % rome_num_str

    while i <= len(rome_num_str) - 1:
        if i < (len(rome_num_str) - 1) and (rome_num_str[i] + rome_num_str[i + 1]) in ROME_ARAB_DICT:
            key = rome_num_str[i] + rome_num_str[i + 1]
            i += 2
        elif rome_num_str[i] in ROME_ARAB_DICT:
            key = rome_num_str[i]
            i += 1
        else:
            raise ValueError('Not allowed character "%s"' % key)

        res += ROME_ARAB_DICT[key]

    return res


def _print(method, number):
    print '"%s" -> "%s"' % (number, method(number))


if __name__ == '__main__':
    _print(arab_to_rome, 0)
    _print(arab_to_rome, 1)
    _print(arab_to_rome, 4)
    _print(arab_to_rome, 10)
    _print(arab_to_rome, 22)
    _print(arab_to_rome, 2222)
    _print(arab_to_rome, 3999)
    try:
        _print(arab_to_rome, 4000)
    except Exception:
        pass

    _print(rome_to_arab, '')
    _print(rome_to_arab, 'I')
    _print(rome_to_arab, 'III')
    _print(rome_to_arab, 'IIII')
    _print(rome_to_arab, 'CD')
    _print(rome_to_arab, 'CDCD')
