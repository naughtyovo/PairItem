from fractions import Fraction


def fraction_to_mixed(frac: Fraction) -> str:
    """
    将分数转换为带分数的字符串形式。
    :param frac: Fraction 对象，表示要转换的分数。
    :return: 返回带分数形式的字符串。如果分子小于等于分母，或是整数（分母为 1），则直接返回其字符串形式。
    """
    # 如果分子小于等于分母，或者分母为 1，表示这是一个小于 1 的分数或整数，直接返回其字符串表示
    if frac.numerator <= frac.denominator or frac.denominator == 1:
        return str(frac)

    # 否则，将其转换为带分数形式。计算整数部分 (frac.numerator // frac.denominator)
    # 然后将剩余的分数部分 (frac - frac.numerator // frac.denominator) 组合成字符串返回
    result = f"{frac.numerator // frac.denominator}'{frac - (frac.numerator // frac.denominator)}"
    return result


def mixed_to_fraction(string: str) -> Fraction:
    """
    将带分数的字符串形式转换为 Fraction 对象。
    :param string: 带分数形式的字符串，例如 "3'1/2" 或 "1/2"。
    :return: 返回 Fraction 对象，表示字符串形式的分数。
    """
    # 如果字符串包含 "/" 和 "'"，则表示这是带分数的格式
    if '/' in string and "'" in string:
        # 使用 "'" 将整数部分与分数部分分开
        div = string.split("'")
        div1 = div[0]  # 获取整数部分
        # 使用 "/" 将分数部分的分子和分母分开
        div = div[1].split("/")
        div2 = div[0]  # 获取分子
        div3 = div[1]  # 获取分母
        # 返回整数部分与分数部分相加的 Fraction 对象
        return int(div1) + Fraction(f"{div2}/{div3}")

    # 如果字符串是简单的分数或整数，直接将其转换为 Fraction 对象
    return Fraction(string)
