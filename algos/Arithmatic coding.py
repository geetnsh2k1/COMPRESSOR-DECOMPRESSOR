import sys
import random
import string

import decimal
from decimal import Decimal

decimal.getcontext().prec=100

def encode(encode_str, N):
    count = dict.fromkeys(string.ascii_lowercase, 1)                                        # probability table
    cdf_range = dict.fromkeys(string.ascii_lowercase, 0)
    pdf = dict.fromkeys(string.ascii_lowercase, 0)

    low = 0
    high = Decimal(1)/Decimal(26)

    for key, value in sorted(cdf_range.iteritems()):
        cdf_range[key] = [low, high]
        low = high
        high += Decimal(1)/Decimal(26)

    for key, value in sorted(pdf.iteritems()):
        pdf[key] = Decimal(1)/Decimal(26)

    # for key, value in sorted(cdf_range.iteritems()):
    #   print key, value

    # for key, value in sorted(pdf.iteritems()):
    #   print key, value

    i = 26

    lower_bound = 0                                                                     # upper bound
    upper_bound = 1                                                                     # lower bound

    u = 0

    # go thru every symbol in the string
    for sym in encode_str:
        i += 1
        u += 1
        count[sym] += 1

        curr_range = upper_bound - lower_bound                                          # current range
        upper_bound = lower_bound + (curr_range * cdf_range[sym][1])                    # upper_bound
        lower_bound = lower_bound + (curr_range * cdf_range[sym][0])                    # lower bound

        # update cdf_range after N symbols have been read
        if (u == N):
            u = 0

            for key, value in sorted(pdf.iteritems()):
                pdf[key] = Decimal(count[key])/Decimal(i)

            low = 0
            for key, value in sorted(cdf_range.iteritems()):
                high = pdf[key] + low
                cdf_range[key] = [low, high]
                low = high

    return [lower_bound, len(encode_str)]

def decode(encoded, strlen, every):
    decoded_str = ""

    count = dict.fromkeys(string.ascii_lowercase, 1)                                        # probability table
    cdf_range = dict.fromkeys(string.ascii_lowercase, 0)
    pdf = dict.fromkeys(string.ascii_lowercase, 0)

    low = 0
    high = Decimal(1)/Decimal(26)

    for key, value in sorted(cdf_range.iteritems()):
        cdf_range[key] = [low, high]
        low = high
        high += Decimal(1)/Decimal(26)

    for key, value in sorted(pdf.iteritems()):
        pdf[key] = Decimal(1)/Decimal(26)


    lower_bound = 0                                                                     # upper bound
    upper_bound = 1                                                                     # lower bound

    k = 0

    while (strlen != len(decoded_str)):
        for key, value in sorted(pdf.iter_items()):

            curr_range = upper_bound - lower_bound                                      # current range
            upper_cand = lower_bound + (curr_range * cdf_range[key][1])                 # upper_bound
            lower_cand = lower_bound + (curr_range * cdf_range[key][0])                 # lower bound

            if (lower_cand <= encoded < upper_cand):
                k += 1
                decoded_str += key

                if (strlen == len(decoded_str)):
                    break

                upper_bound = upper_cand
                lower_bound = lower_cand

                count[key] += 1

                if (k == every):
                    k = 0
                    for key, value in sorted(pdf.iteritems()):
                        pdf[key] = Decimal(count[key])/Decimal(26+len(decoded_str))

                    low = 0
                    for key, value in sorted(cdf_range.iteritems()):
                        high = pdf[key] + low
                        cdf_range[key] = [low, high]
                        low = high

    print (decoded_str)

def main():
    count = 10
    encode_str = "heloworldheloworld"
    strlen = len(encode_str)
    every = 3
    encoded = encode(encode_str, every)
    decoded = decode(encoded, strlen, every)

if __name__ == '__main__':
    main()
