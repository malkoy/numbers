class NumberToString:
    """
        Transform numbers to english spelling words.
        Allowed numbers:
            from -999999999999999999999 to 999999999999999999999
        Usage:
            NumberToString().transform(number)
    """
    ONES_MAPPINGS = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine'
    }

    TENS_MAPPINGS = {
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety'
    }

    ONE = 'one'
    TEN = 'ten'
    HUNDRED = 'hundred'
    THOUSAND = 'thousand'
    MILLION = 'million'
    BILLION = 'billion'
    TRILLION = 'trillion'
    QUADRILLION = 'quadrillion'
    QUINTILLION = 'quintillion'
    SEXTILLION = 'sextillion'

    NUMBERS_MAPPINGS = {
        ONE: 10 ** 0,
        TEN: 10 ** 1,
        HUNDRED: 10 ** 2,
        THOUSAND: 10 ** 3,
        MILLION: 10 ** 6,
        BILLION: 10 ** 9,
        TRILLION: 10 ** 12,
        QUADRILLION: 10 ** 15,
        QUINTILLION: 10 ** 18,
        SEXTILLION: 10 ** 21
    }

    NUMBER_NAMES_LIST = [
        ONE,
        TEN,
        HUNDRED,
        THOUSAND,
        MILLION,
        BILLION,
        TRILLION,
        QUADRILLION,
        QUINTILLION,
        SEXTILLION
    ]

    def _get_ones(self, number):
        return self.ONES_MAPPINGS[number]

    def _get_tens(self, number):
        if number > 19:
            tens, ones = divmod(number, 10)
            if not ones:
                number_str = self.TENS_MAPPINGS[number]
            else:
                number_str = '{tens}-{ones}'.format(
                    tens=self.TENS_MAPPINGS[tens * 10],
                    ones=self.ONES_MAPPINGS[ones]
                )
        else:
            number_str = self.TENS_MAPPINGS[number]

        return number_str

    def _get_hundreds(self, number, segment_name, sep=','):
        quotient, remainder = divmod(number, self.NUMBERS_MAPPINGS[segment_name])
        if remainder:
            res = '{quotient} {segment_name}{separator} {remainder}'.format(
                quotient=self._int_to_str(quotient),
                segment_name=segment_name,
                remainder=self._int_to_str(remainder),
                separator=sep if segment_name != self.HUNDRED else ''
            )
        else:
            res = '{quotient} {segment_name}'.format(
                quotient=self._int_to_str(quotient),
                segment_name=segment_name
            )
        return res

    def _get_dec_position(self, dec_str):
        for i in range(1, len(dec_str) + 1):
            if dec_str[-i] == '0':
                continue
            else:
                return len(dec_str[:-i])

    def _int_to_str(self, number):
        if number == 0:
            return self.ONES_MAPPINGS[number]
        elif self.NUMBERS_MAPPINGS[self.ONE] <= number < self.NUMBERS_MAPPINGS[self.TEN]:
            return self._get_ones(number)
        elif self.NUMBERS_MAPPINGS[self.TEN] <= number < self.NUMBERS_MAPPINGS[self.HUNDRED]:
            return self._get_tens(number)

        for i in range(2, len(self.NUMBER_NAMES_LIST) - 1):  # starting from hundreds
            floor_val = self.NUMBERS_MAPPINGS[self.NUMBER_NAMES_LIST[i]]
            ceil_val = self.NUMBERS_MAPPINGS[self.NUMBER_NAMES_LIST[i + 1]]

            if floor_val <= number < ceil_val:
                return self._get_hundreds(number, self.NUMBER_NAMES_LIST[i])

    def _float_to_str(self, number):
        int_str, dec_str = str(number).split('.')
        dec_int = int(dec_str)
        int_part = self._int_to_str(int(int_str))

        if dec_int:
            dec_part = self._int_to_str(int(dec_str))
            dec_name = self._int_to_str(10 ** (self._get_dec_position(dec_str) + 1))
            dec_name = dec_name.replace(self.ONE, '').strip()
            return "{int_part} and {dec_part} {dec_name}ths".format(
                int_part=int_part,
                dec_part=dec_part,
                dec_name=dec_name
            )
        else:
            return "{int_part}".format(int_part=int_part)

    def transform(self, number):
        if isinstance(number, int):
            func_ = self._int_to_str
        elif isinstance(number, float):
            func_ = self._float_to_str
        else:
            raise Exception("Invalid number type.")

        negative = False
        if number < 0:
            negative, number = True, abs(number)

        if number >= self.NUMBERS_MAPPINGS[self.SEXTILLION]:
            raise Exception("Max number %d is allowed." % (self.NUMBERS_MAPPINGS[self.SEXTILLION] - 1))

        num_str = func_(number)
        return "negative %s" % num_str if negative else num_str


if __name__ == '__main__':
    #FIXME: rounding
    max_str = "nine hundred ninety-nine quintillion, nine hundred ninety-nine quadrillion, nine hundred ninety-nine trillion, nine hundred ninety-nine billion, nine hundred ninety-nine million, nine hundred ninety-nine thousand, nine hundred ninety-nine"
    assert NumberToString().transform(999999999999999999999) == max_str
    assert NumberToString().transform(12345) == "twelve thousand, three hundred forty-five"
    assert NumberToString().transform(123) == "one hundred twenty-three"
    assert NumberToString().transform(7) == "seven"
    assert NumberToString().transform(0) == "zero"
    assert NumberToString().transform(-0) == "zero"
    assert NumberToString().transform(-256) == "negative two hundred fifty-six"
    assert NumberToString().transform(1.1245) == "one and one thousand, two hundred forty-five ten thousandths"
    assert NumberToString().transform(63.45) == "sixty-three and forty-five hundredths"
    assert NumberToString().transform(123.0004500) == "one hundred twenty-three and forty-five hundred thousandths"
    print(NumberToString().transform(999999999999999999999.999999999999999999999))
