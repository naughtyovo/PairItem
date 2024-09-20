from fractions import Fraction


def fraction_to_mixed(frac: Fraction) -> str:
    """
    将 Fraction 对象转换为带分数的字符串表示形式。

    :param frac: 需要转换的 Fraction 对象，表示分数。
    :return: 分数的字符串表示形式，如果是假分数，返回带分数格式，否则返回分数的原始字符串。

    - 如果分数的分子（numerator）小于或等于分母（denominator），或分母为 1，则直接返回该分数的字符串表示。
    - 如果是假分数（分子大于分母），则返回带分数的格式：
      例如，对于 7/3，返回 "2'1/3"，即带分数形式：整数部分'分数部分。
    """
    # 如果分子小于等于分母，或分母为1，返回分数原始形式
    if frac.numerator <= frac.denominator or frac.denominator == 1:
        return str(frac)  # 直接返回 Fraction 的字符串表示

    # 对于假分数，返回带分数形式
    # 整数部分: frac.numerator // frac.denominator，余数部分为 frac - (整数部分)
    else:
        return f"{frac.numerator // frac.denominator}'{frac - frac.numerator // frac.denominator}"


def mixed_to_fraction(string: str) -> Fraction:
    """
    将带分数的字符串表示转换为 Fraction 对象。

    :param string: 带分数的字符串，例如 "2'1/3" 或简单的 "3/4"。
    :return: 对应的 Fraction 对象。

    - 如果字符串包含带分数形式（即包含 "'" 和 "/"），将其分为整数部分和分数部分，并组合成一个 Fraction 对象。
    - 如果是普通分数，直接将其转换为 Fraction 对象。
    """
    # 如果字符串包含带分数的表示形式（即同时包含 "'" 和 "/"）
    if "'" in string and '/' in string:
        whole, frac_part = string.split("'")  # 将字符串分为整数部分和分数部分
        numerator, denominator = map(int, frac_part.split("/"))  # 将分数部分解析为分子和分母
        # 返回整数部分 + 分数部分组成的 Fraction 对象
        return int(whole) + Fraction(numerator, denominator)

    # 如果字符串表示的是简单的分数形式，则直接转换为 Fraction 对象
    return Fraction(string)
