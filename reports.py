from heap_sort import heap_sort
from utils import (
    is_time_in_range,
    validate_and_parse_date,
    subtract_days_from_date,
    get_valid_latest_date,
)


def generate_income_report_last_n_days(transactions, number_of_days):
    """
    Отчёт 1: Поступления за последние N дней (включительно).
    Сортировка: дата (по убыванию), сумма (по убыванию).
    """
    if not isinstance(number_of_days, int) or number_of_days < 0:
        print("  Ошибка: N должно быть целым неотрицательным числом.")
        return

    if not transactions:
        print("  Нет данных для анализа.")
        return

    today = get_valid_latest_date(transactions)
    if today is None:
        print("  Не удалось определить текущую дату: нет валидных записей.")
        return

    start_date = subtract_days_from_date(today, number_of_days)
    if start_date is None:
        print("  Ошибка при вычислении начальной даты.")
        return

    filtered = [
        transaction
        for transaction in transactions
        if (
            transaction.get('direction') == 'приход'
            and isinstance(transaction.get('date'), str)
            and transaction['date'] >= start_date
        )
    ]

    if not filtered:
        print(
            f" Нет поступлений за последние {number_of_days} дн. "
            f"(с {start_date} по {today})."
        )
        return

    # Создаём составной ключ: (-год, -месяц, -день, -сумма)
    # reverse=False → даёт: дата по убыванию, сумма по убыванию
    for transaction in filtered:
        parsed = validate_and_parse_date(transaction['date'])
        if parsed:
            year, month, day = parsed
            transaction['_sort_key'] = (-year, -month, -day, -transaction['amount'])
        else:
            # На случай невалидной даты — ставим в конец
            transaction['_sort_key'] = (9999, 99, 99, -transaction['amount'])

    heap_sort(filtered, '_sort_key', reverse=False)

    # Удаляем временный ключ
    for transaction in filtered:
        del transaction['_sort_key']

    print(
        f"\n Отчёт 1: Поступления за последние {number_of_days} дн. "
        f"(с {start_date} по {today})"
    )
    print(f" Всего: {len(filtered)}")
    for transaction in filtered:
        amount = transaction.get('amount', 0.0)
        counterparty = transaction.get('counterparty', '—')
        time_val = transaction.get('time', '—')
        print(
            f"{transaction['date']} {time_val} | {amount:>8.2f} | {counterparty}"
        )


def generate_expense_report_by_category(transactions, category_name):
    """
    Отчёт 2: Затраты по категории.
    Сортировка: дата (по убыванию), контрагент (по возрастанию), сумма (по убыванию).
    """
    expense_transactions = [
        transaction
        for transaction in transactions
        if (
            transaction['direction'] == 'расход'
            and transaction['category'] == category_name
        )
    ]

    if not expense_transactions:
        print(f" Нет затрат по категории '{category_name}'.")
        return

    # Составной ключ: (-год, -месяц, -день, контрагент, -сумма)
    # reverse=False → 
    #   дата: по убыванию (благодаря -год и т.д.)
    #   контрагент: по возрастанию (обычный порядок строк)
    #   сумма: по убыванию (благодаря -сумма)
    for transaction in expense_transactions:
        parsed = validate_and_parse_date(transaction['date'])
        if parsed:
            year, month, day = parsed
            transaction['_sort_key'] = (-year, -month, -day, transaction['counterparty'], -transaction['amount'])
        else:
            transaction['_sort_key'] = (9999, 99, 99, transaction['counterparty'], -transaction['amount'])

    heap_sort(expense_transactions, '_sort_key', reverse=False)

    for transaction in expense_transactions:
        del transaction['_sort_key']

    print(
        f"\n Отчёт 2: Затраты по категории '{category_name}' "
        f"(всего: {len(expense_transactions)})"
    )
    for transaction in expense_transactions:
        print(
            f"{transaction['date']} {transaction['time']} | "
            f"{transaction['amount']:>8.2f} | "
            f"{transaction['counterparty']}"
        )


def generate_expense_report_in_time_interval(transactions, start_time, end_time):
    """
    Отчёт 3: Затраты в интервале времени.
    Сортировка: сумма (по убыванию), контрагент (по возрастанию).
    """
    expense_transactions = [
        transaction
        for transaction in transactions
        if transaction['direction'] == 'расход'
    ]
    filtered_transactions = [
        transaction
        for transaction in expense_transactions
        if is_time_in_range(transaction['time'], start_time, end_time)
    ]

    if not filtered_transactions:
        print(f" Нет затрат в интервале {start_time}–{end_time}.")
        return

    # Составной ключ: (-сумма, контрагент)
    # reverse=False → 
    #   -сумма: меньшие значения (более отрицательные) идут первыми → большие суммы первыми
    #   контрагент: по возрастанию
    for transaction in filtered_transactions:
        transaction['_sort_key'] = (-transaction['amount'], transaction['counterparty'])

    heap_sort(filtered_transactions, '_sort_key', reverse=False)

    for transaction in filtered_transactions:
        del transaction['_sort_key']

    print(
        f"\n Отчёт 3: Затраты в интервале {start_time}–{end_time} "
        f"(всего: {len(filtered_transactions)})"
    )
    for transaction in filtered_transactions:
        print(
            f"{transaction['date']} {transaction['time']} | "
            f"{transaction['amount']:>8.2f} | "
            f"{transaction['counterparty']}"
        )
