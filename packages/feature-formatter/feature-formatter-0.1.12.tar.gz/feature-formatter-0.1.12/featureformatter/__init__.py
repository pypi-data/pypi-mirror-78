import re
import string

import num2words

CURRENCY_WORD_MAPPING = {
    "en": {"$": "dollar", "€": "euro", "£": "pound"},
    "de": {"$": "Dollar", "€": "Euro", "£": "Pfund"},
}

INVALID_CHARS = {"en": r"[^a-zA-Z]", "de": r"[^a-zA-ZäöüÄÖÜß]"}

PERCENT_WORD = {"en": "percent", "de": "Prozent"}
AND_WORD = {"en": "and", "de": "und"}

METRIC_WORD = {
    "en": {
        "km/h": "kilometers per hour",
        "mph": "miles per hour",
        "m/s": "meters per second",
    },
    "de": {
        "km/h": "Kilometer pro Stunde",
        "mph": "Meilen pro Stunde",
        "m/s": "Meter pro Sekunde",
    },
}

YEAR_PRECEEDING_WORDS = {
    "en": ["in", "year", "before", "after", "since"],
    "de": ["im", "jahr", "vor", "ab", "seit"],
}

# the dict key is regex
ABBR_WORDS = {
    "en": {
        r"\ba\.m\.": "am",
        r"\bp\.m\.": "pm",
        r"\bmr[\. ]": "mister",
        r"\bmrs[\. ]": "missus",
        r"\bdr[\. ]": "doctor",
        r"\bprof[\. ]": "professor",
        r"\bcapt[\. ]": "captain",
        r"\betc\b": "et cetera",
        r"\bvs[\. ]": "versus",
        r"\bdept\.": "department",
        r"\bapprox\.": "approximately",
        r"\best\.": "established",
        r"\bmisc\.": "miscellaneous",
        r"\be\.g\.": "for example",
        r"\btv\b": "T V",
    },
    "de": {
        r"\bz\.B\. ": "zum Beispiel",
        r"\bbzw\.": "beziehungsweise",
        r"\busw\.": "und so weiter",
    },
}


class BaseFormatter:
    def __init__(self, lang="en"):
        if lang not in ["en", "de"]:
            raise Exception("language not implemented")

        self.lang = lang


class TextFormatter(BaseFormatter):
    def __init__(self, lang="en", return_upper_case=True):
        super().__init__(lang)
        # the purpose is to remove ambiguity of cases
        # in German it might be unnecessary
        self.return_upper_case = return_upper_case

        self.__cache = {}

    def n2w(self, word, to="cardinal"):
        word = re.sub(r"[^0-9]", "", word)
        numword = num2words.num2words(int(word), to=to, lang=self.lang)
        numword = numword.replace(",", "").replace("-", " ")
        return numword.split()

    def is_currency(self, word):
        symbol = word[0]
        name = CURRENCY_WORD_MAPPING.get(self.lang).get(symbol)
        if name and re.match(r"^[\d,]+$", word[1:]):
            value = re.sub(r"[^0-9]", "", word[1:])  # return string
            # TODO other languages
            if int(value) > 1:
                name += "s"
            return name, value
        return None

    def roman2w(self, s):
        rom_val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        int_val = 0
        for i in range(len(s)):
            if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
                int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
            else:
                int_val += rom_val[s[i]]
        return self.n2w(str(int_val))

    def remove_invalid_chars(self, text):
        return re.sub(INVALID_CHARS.get(self.lang), "", text)

    def is_valid_non_punc_char(self, c):
        if c in string.punctuation:
            return False

        if self.lang == "en":
            return ord(c) < 128

        if self.lang == "de":
            return ord(c) < 128 or c in "äöüÄÖÜß"

    def contains_metric(self, word):
        w = word.lower()
        keys = METRIC_WORD[self.lang].keys()
        for k in keys:
            if w.endswith(k):
                return k
        return None

    def format_text(self, text):
        """
        a whitelisted fashion as opposed to tokenizing
        """
        original_text = text
        if self.__cache.get(original_text):
            return self.__cache.get(original_text)

        text = text.strip()

        # remove punctuation
        c_list = []
        for idx, c in enumerate(text):
            is_valid = False

            # replace common typing errors
            if c == "’":
                c = "'"
            elif c == "–":
                c = "-"

            if c == "%" or c == "&" or c == "/" or c == ".":
                # dot should be handled specially for abbr
                is_valid = True
            elif (
                c == "'"
                and idx > 0
                and text[idx - 1] != " "
                and (
                    (
                        idx + 1 < len(text)
                        and (text[idx + 1].isalpha() or text[idx - 1].lower() == "s")
                    )
                    or (idx + 1 == len(text) and text[idx - 1].lower() == "s")
                )
            ):
                is_valid = True
            elif (
                c == "-"
                and idx > 0
                and text[idx - 1] != " "
                and idx + 1 < len(text)
                and text[idx + 1] != " "
            ):
                is_valid = True
            elif (
                c in [",", ":"]
                and idx > 0
                and text[idx - 1].isdigit()
                and idx + 1 < len(text)
                and text[idx + 1].isdigit()
            ):
                is_valid = True  # finance number, or time
            elif c in CURRENCY_WORD_MAPPING[self.lang]:
                is_valid = True
            elif self.is_valid_non_punc_char(c):
                is_valid = True

            if is_valid:
                c_list.append(c)
            else:
                c_list.append(" ")  # adding a space, it will be trimmed later on

        text = "".join(c_list)

        word_list = []
        change_list = {}

        # handle dot and abbr words first
        # so it not confuses with period and illegal dots
        for abbr, repl in ABBR_WORDS[self.lang].items():
            for found in re.findall(abbr, text, flags=re.IGNORECASE):
                change_list[found] = repl.upper() if self.return_upper_case else repl
            text = re.sub(abbr, repl + " ", text, flags=re.IGNORECASE)

        text = text.replace(".", " ")

        text_iter = text.split()
        for idx, word in enumerate(text_iter):
            if not word:
                continue

            to_append = None

            if (
                len(word) == 4
                and word.isdigit()
                and (
                    int(word) < 2100
                    and int(word) > 1700
                    or idx > 0
                    and text_iter[idx - 1].lower() in YEAR_PRECEEDING_WORDS[self.lang]
                )
            ):
                # this needs further improvements
                # in (year) 1900
                # match year before matching numbers
                # this is a best-guess approach
                to_append = self.n2w(word, to="year")
            elif re.match(r"^[\d,]+$", word):  # number or number with comma
                to_append = self.n2w(word)
            elif re.match(
                r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", word
            ):  # complete telephone number regex, although it will only be like 123-123-123
                to_append = []
                for digit in re.sub("[^0-9]", "", word):
                    to_append += self.n2w(digit)
            elif "%" in word:
                newword = word.replace("%", "")
                if newword.isdigit():
                    to_append = self.n2w(newword) + [PERCENT_WORD.get(self.lang)]
                else:
                    newword = self.remove_invalid_chars(newword)
                    to_append = [newword, PERCENT_WORD.get(self.lang)]
            elif "&" in word:
                newword = word.replace("&", f" {AND_WORD.get(self.lang)} ")
                to_append = newword.strip().split()
            elif "-" in word:
                to_append = word.split("-")
            elif ":" in word:
                to_append = []
                for t in word.split(":"):
                    to_append += self.n2w(t)
            elif self.contains_metric(word):
                k = self.contains_metric(word)
                rep = METRIC_WORD[self.lang][k]
                to_append = word.lower().replace(k, f" {rep}").strip().split()
            elif "/" in word:
                # just ignore the slash
                to_append = word.split("/")
            elif (
                self.lang == "en"
                and len(word) > 2
                and word[:-2].isdigit()
                and word[-2:].lower() in ["th", "st", "rd", "nd"]
            ):
                # 125th
                # TODO this is English only
                to_append = self.n2w(word[:-2], to="ordinal")
            elif len(word) == 5 and word[:4].isdigit() and word[-1].lower() == "s":
                # 1900s
                to_append = self.n2w(word[:4], to="year")
            elif len(word) > 2 and word[:-2].isdigit() and word[-2:].lower() == "'s":
                # 80's
                to_append = self.n2w(word[:-2])
                to_append.append(word[-2:])
            elif self.is_currency(word):
                name, value = self.is_currency(word)
                to_append = self.n2w(value)
                to_append.append(name)
            elif len(word) > 1 and re.match(
                r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", word
            ):
                # "I" will be One, but it is wrong. We prefer "I" to roman "One"
                # same applies for German, that M is probably a letter
                # it applis to all single X, M, I, etc.
                to_append = self.roman2w(word)
            else:
                m = re.match(
                    r"^([a-zA-Z]+)(\d+)$", word
                )  # particular case like "gate E25"
                if m:
                    if not m.group(1).lower().startswith("xx"):
                        # such as XXEY1, phonics
                        to_append = [m.group(1)] + self.n2w(m.group(2))
                else:
                    m = re.match(
                        r"^(\d+)([a-zA-Z]+)$", word
                    )  # particular case like "seat 12C"
                    if m:
                        to_append = self.n2w(m.group(1)) + [m.group(2)]

            if to_append is None:
                final_append = [word]
            else:
                # finally check whether there is still number in to_append
                final_append = []
                for ta in to_append:
                    if ta.isdigit():
                        final_append += self.n2w(ta)
                    else:
                        final_append.append(self.remove_invalid_chars(ta))

                change_list[word] = " ".join(
                    [
                        x.upper() if self.return_upper_case else x
                        for x in filter(len, final_append)
                    ]
                )

            word_list += final_append

        text = " ".join(word_list)
        if self.return_upper_case:
            text = text.upper()

        self.__cache[original_text] = (text, change_list)
        return self.__cache[original_text]


class PhoneFormatter(BaseFormatter):
    def __init__(self, lang="en"):
        super().__init__(lang)

    def get_phone_root(self, phone, sep="_"):
        if not phone or phone == sep:
            return phone

        if self.lang == "en":
            phone_root = phone.split(sep)[0]
            if phone_root[-1].isdigit():
                return phone_root[:-1]

            return phone_root

        if self.lang == "de":
            # In German we have also numbers as phone code
            phone_root = (
                phone.split(sep)[0].replace("~", "").replace("'", "").replace('"', "")
            )
            return phone_root

    def get_phone_stress(self, phone, sep="_"):
        """
        0    — No stress
        1    — Primary stress
        2    — Secondary stress

        Return:
        None: no stress digit
        True: stress must be performed
        False: stress must not be performed
        """
        if not phone or phone == sep:
            return None
        if self.lang == "en":
            phone_root = phone.split(sep)[0]
            if phone_root[-1].isdigit():
                return int(phone_root[-1]) > 0

        return None

    def is_vowel(self, phone):
        if not phone:
            return False

        if self.lang == "en":
            return phone[0] in ["A", "E", "I", "O", "U"]

        if self.lang == "de":
            return phone[0] in [
                "a",
                "e",
                "E",
                "i",
                "I",
                "o",
                "O",
                "u",
                "U",
                "y",
                "2",
                "9",
                "@",
            ]

        return False
