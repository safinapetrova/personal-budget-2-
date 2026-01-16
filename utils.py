def is_time_in_range(time_string, start_time, end_time):
    """
    Проверяет, попадает ли time_string в интервал [start_time, end_time].
    """
    try:
        def time_to_minutes(time):
            hours, minutes = map(int, time.split(':'))
            return hours * 60 + minutes

        time_minutes = time_to_minutes(time_string)
        start_minutes = time_to_minutes(start_time)
        end_minutes = time_to_minutes(end_time)

        return start_minutes <= time_minutes <= end_minutes
    except (ValueError, AttributeError, TypeError):
        return False


def is_leap_year(year):
    """Проверяет, является ли год високосным."""
    if not isinstance(year, int) or year < 1:
        return False
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    """Возвращает количество дней в месяце с учётом високосного года."""
    if not isinstance(year, int) or not isinstance(month, int):
        return 0
    if month < 1 or month > 12:
        return 0
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and is_leap_year(year):
        return 29
    return days[month - 1]


def validate_and_parse_date(date_str):
    """
    Валидирует и парсит дату в формате 'ГГГГ-ММ-ДД'.
    Возвращает кортеж (year, month, day) или None при ошибке.
    """
    if not isinstance(date_str, str):
        return None
    if len(date_str) != 10:
        return None
    if date_str[4] != '-' or date_str[7] != '-':
        return None

    try:
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])
    except (ValueError, TypeError):
        return None

    if year < 1000 or year > 9999:
        return None
    if month < 1 or month > 12:
        return None
    if day < 1 or day > days_in_month(year, month):
        return None

    return (year, month, day)


def tuple_to_date(year, month, day):
    """Преобразует (год, месяц, день) в строку 'ГГГГ-ММ-ДД'."""
    return f"{year:04d}-{month:02d}-{day:02d}"


def subtract_days_from_date(date_str, number):
    """
    Вычитает N дней из даты.
    Возвращает строку новой даты или None при ошибке.
    Никаких импортов.
    """
    if not isinstance(number, int) or number < 0:
        return None

    parsed = validate_and_parse_date(date_str)
    if parsed is None:
        return None

    year, month, day = parsed
    for _ in range(number):
        day -= 1
        if day < 1:
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            day = days_in_month(year, month)
    return tuple_to_date(year, month, day)


def get_valid_latest_date(transactions):
    """
    Находит самую позднюю валидную дату среди транзакций.
    Возвращает строку или None.
    """
    valid_dates = []
    for transaction in transactions:
        date_val = transaction.get('date')
        if isinstance(date_val, str) and validate_and_parse_date(date_val) is not None:
            valid_dates.append(date_val)
    if not valid_dates:
        return None
    return max(valid_dates)
