from functools import reduce

def luhn(code):
    LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    code = reduce(str.__add__, filter(str.isdigit, code))
    evens = sum(int(i) for i in code[-1::-2])
    odds = sum(LOOKUP[int(i)] for i in code[-2::-2])
    return ((evens + odds) % 10 == 0)



def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False
