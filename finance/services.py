from decimal import ROUND_CEILING


def per_child_amount(total_cost, from_piggy_bank, participants, rounding_step):
    if participants <= 0:
        raise ValueError("Нужен хотя бы один участник")
    if from_piggy_bank > total_cost:
        raise ValueError("Из копилки нельзя взять больше стоимости")

    to_collect = total_cost - from_piggy_bank
    raw = to_collect / participants
    steps = (raw / rounding_step).to_integral_value(rounding=ROUND_CEILING)
    return steps * rounding_step
