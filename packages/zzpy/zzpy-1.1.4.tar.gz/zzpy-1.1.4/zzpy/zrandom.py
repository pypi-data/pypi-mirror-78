def randint(min=0, max=9):
    import random
    if min > max:
        min, max = max, min
    return random.randint(min, max)


def randhex(digits=1, prefix=False, lower=False):
    import random
    alpha = '0123456789ABCDEF'
    prefix_str = '0x' if prefix else ''
    num_str = ''.join(random.choice(alpha)
                      for _ in range(digits))
    if lower:
        num_str = num_str.lower()
    return prefix_str+num_str
