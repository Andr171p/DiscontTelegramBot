def format_phone_number(phone_number):
    digits = ''.join(filter(str.isdigit, phone_number))

    if len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]

    formatted_number = '+{}({}){}-{}-{}'.format(
        digits[0], digits[1:4], digits[4:7], digits[7:9], digits[9:11]
    )

    return formatted_number


def format_order_number(order_number):
    number_list = order_number.split('-')
    number = number_list[-1]
    return number


def format_order_time(order_time):
    time_part = order_time.split('T')
    time = time_part[-1][:-3]
    return time
