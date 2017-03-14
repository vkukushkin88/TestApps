def median3(v1,v2,v3):
    if v1 > v2:
        if v3 > v1:
            return v1
        return v2 if v2 > v3 else v3
    if v3 > v2:
        return v2
    return v1 if v1 > v3 else v3


assert(3 == median3(2, 5, 3))


def odd(arr):
    s = sum(arr)
    l = len(arr)
    return (l + 1) * (l + 2) / 2 - s


assert(6 == odd([1,2,3,4,5,7]))