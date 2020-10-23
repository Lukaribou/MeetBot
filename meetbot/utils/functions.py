def get_int(n: str) -> int:
    n = n.replace('#', '0x')
    if any(letter in ['A', 'B', 'C', 'D', 'E', 'F'] for letter in n.upper()) and not n.startswith('0x'):
        return int(n, 16)
    return int(n, 0)