import json
import math


def valuation_two(number):
    assert number > 0
    return (number & -number).bit_length() - 1


def fermat(index):
    return (1 << (1 << index)) + 1


def expected_gcd(index, exponent):
    period = 1 << index
    return 1 if exponent % period == 0 else fermat(valuation_two(exponent))


def smallest_divisor(number):
    assert number >= 2
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            return divisor
    return number


def run():
    counts = {
        'original_conjecture_pairs': 0,
        'plus_gcd_pairs': 0,
        'minus_gcd_pairs': 0,
        'plus_proper_divisors': 0,
        'minus_proper_divisors': 0,
        'positive_difference_pairs': 0,
        'all_prime_family_composite_terms': 0,
        'wu_conjecture_pairs': 0,
        'mersenne_prime_count_zero_inputs': 0,
    }
    for index in range(1, 13):
        period = 1 << index
        modulus = (1 << period) - 1
        positive_base = (1 << (period + 1)) - 1
        negative_base = (1 << (period - 1)) - 1
        for exponent in range(4 * period):
            plus_value = positive_base + (1 << exponent)
            assert math.gcd(plus_value, modulus) == expected_gcd(index, exponent)
            counts['plus_gcd_pairs'] += 1
            if exponent == 0:
                assert plus_value == 1 << (period + 1)
                assert 1 < 2 < plus_value
            elif exponent % period:
                divisor = expected_gcd(index, exponent)
                assert plus_value % divisor == 0 and 1 < divisor < plus_value
                counts['plus_proper_divisors'] += 1
            if exponent < period:
                counts['original_conjecture_pairs'] += 1
            difference = abs(negative_base - (1 << exponent))
            assert math.gcd(difference, modulus) == expected_gcd(index, exponent + 1)
            counts['minus_gcd_pairs'] += 1
            if index >= 3 and exponent > 0 and (exponent + 1) % period:
                divisor = expected_gcd(index, exponent + 1)
                assert difference % divisor == 0 and 1 < divisor < difference
                counts['minus_proper_divisors'] += 1
            if index >= 3 and 1 <= exponent <= period - 2:
                assert negative_base > 1 << exponent
                counts['positive_difference_pairs'] += 1
            if index >= 3 and exponent < period - 2:
                if exponent == 0:
                    assert (negative_base - 1) % 2 == 0 and negative_base - 1 > 2
                else:
                    divisor = expected_gcd(index, exponent + 1)
                    assert (negative_base - (1 << exponent)) % divisor == 0
                    assert 1 < divisor < negative_base - (1 << exponent)
                counts['wu_conjecture_pairs'] += 1
        if index >= 3:
            counts['mersenne_prime_count_zero_inputs'] += 1
    expected_offsets = {0: 1, 1: 2, 2: 4, 3: 16}
    offsets = {}
    certificates = {}
    for index, bound in expected_offsets.items():
        base = (1 << ((1 << index) + 1)) - 1
        rows = []
        for exponent in range(bound + 1):
            number = base + (1 << exponent)
            divisor = smallest_divisor(number)
            rows.append({'exponent': exponent, 'value': number, 'smallest_divisor': divisor})
            if divisor == number:
                offsets[index] = exponent
                break
        assert offsets[index] == bound
        certificates[index] = rows
    assert ((1 << 9) - 1) + (1 << 8) == 13 * 59
    for base in range(1, 100):
        first_prime = smallest_divisor(2 * base + 1)
        second_prime = smallest_divisor(base + 2) if base % 2 else 2
        for multiplier in range(1, 6):
            first_value = base * (1 << (1 + multiplier * (first_prime - 1))) + 1
            second_value = base + (1 << (1 + multiplier * (second_prime - 1)))
            assert first_value % first_prime == 0 and first_value > first_prime
            assert second_value % second_prime == 0 and second_value > second_prime
            counts['all_prime_family_composite_terms'] += 2
    return {
        'status': 'PASS',
        'arithmetic': 'Exact Python integers, Euclidean gcd, exhaustive trial division for the listed least offsets.',
        'ranges': {
            'gcd_identities': '1 <= n <= 12; 0 <= k,m < 4*2^n',
            'original_conjecture': '1 <= n <= 12; 0 <= k < 2^n',
            'absolute_difference': '3 <= n <= 12; 0 < m < 4*2^n; 2^n does not divide m+1',
            'all_prime_families': 'All positive C from 1 through 99; progression parameters t from 1 through 5',
            'wu_conjecture': '3 <= j <= 12; 0 <= k < 2^j-2',
            'mersenne_prime_count_zero': 'Inputs 2^j-1 for 3 <= j <= 12',
        },
        'counts': counts,
        'least_offsets': offsets,
        'trial_division_certificates': certificates,
        'coverage': 'Finite calculations for the stated ranges; universal claims are proved in note.tex.',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
