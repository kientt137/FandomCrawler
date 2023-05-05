import re


class Utilities:

    @staticmethod
    def string_to_id(s):
        s = s.strip().lower()
        s = re.sub(r"[^\w\s]", '', s)
        s = re.sub(r"\s+", '_', s)
        return s
