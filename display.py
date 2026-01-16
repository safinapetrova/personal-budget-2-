from data_loader import (
    load_budget_transactions,
    add_transaction,
    delete_transaction,
    update_transaction
)
from utils import validate_and_parse_date


def display_main_menu():
    """Отображает главное меню программы."""
    print("\n" + "=" * 60)
    print(" Персональный бюджет — Главное меню")
    print("=" * 60)
    print("1. Просмотреть все транзакции")
    print("2. Добавить новую транзакцию")
    print("3. Редактировать транзакцию")
    print("4. Удалить транзакцию")
    print("5. Отчёт 1: Поступления за N дней")
    print("6. Отчёт 2: Затраты по категории")
    print("7. Отчёт 3: Затраты в интервале времени")
    print("8. Выход")
    print("-" * 60)


def wait_for_user_to_return():
    """Ожидает нажатия Enter для возврата в меню."""
    input("\nНажмите Enter, чтобы вернуться в главное меню...")


def display_transactions(transactions):
    """Отображает список транзакций с индексами."""
    if not transactions:
        print(" Нет транзакций.")
        return

    print(f"\n Всего транзакций: {len(transactions)}")
    print(
        f"\n{'№':<3} | {'Дата':<10} | {'Время':<8} | {'Направление':<12} | "
        f"{'Категория':<15} | {'Сумма':>8} | {'Контрагент':<25}"
    )
    print("-" * 85)
    for transaction_number, transaction in enumerate(transactions, start=1):
        print(
            f"{transaction_number:<3} | "
            f"{transaction['date']:<10} | "
            f"{transaction['time']:<8} | "
            f"{transaction['direction']:<12} | "
            f"{transaction['category']:<15} | "
            f"{transaction['amount']:>8.2f} | "
            f"{transaction['counterparty']:<25}"
        )


def get_transaction_input():
    """Запрашивает у пользователя данные для новой транзакции."""
    print("\nВведите данные для новой транзакции:")

    while True:
        date_str = input("Дата (ГГГГ-ММ-ДД): ").strip()
        if validate_and_parse_date(date_str) is not None:
            break
        print(
            "  Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД."
        )

    while True:
        time_str = input("Время (ЧЧ:ММ): ").strip()
        try:
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                break
            print(
                "  Неверный формат времени. Часы должны быть от 0 до 23, "
                "минуты от 0 до 59."
            )
        except ValueError:
            print("  Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ.")

    while True:
        direction = input("Направление (приход/расход): ").strip().lower()
        if direction in ['приход', 'расход']:
            break
        print("  Неверное направление. Пожалуйста, введите 'приход' или 'расход'.")

    category = input("Категория: ").strip()
    if not category:
        category = "Без категории"

    while True:
        amount_str = input("Сумма: ").strip()
        try:
            amount = float(amount_str)
            if amount >= 0:
                break
            print("  Сумма должна быть неотрицательной.")
        except ValueError:
            print("  Неверный формат суммы. Пожалуйста, введите число.")

    counterparty = input("Контрагент: ").strip()
    if not counterparty:
        counterparty = "Неизвестный"

    return {
        'date': date_str,
        'time': time_str,
        'direction': direction,
        'category': category,
        'amount': amount,
        'counterparty': counterparty
    }


def add_new_transaction():
    """Добавляет новую транзакцию."""
    transaction = get_transaction_input()
    if add_transaction(transaction):
        print(" Транзакция успешно добавлена.")
    else:
        print(" Ошибка при добавлении транзакции.")


def edit_transaction():
    """Редактирует существующую транзакцию."""
    transactions = load_budget_transactions()
    if transactions is None:
        print(" Не удалось загрузить данные.")
        return

    display_transactions(transactions)

    if not transactions:
        return

    while True:
        try:
            user_index = int(input("Введите номер транзакции для редактирования (0 для отмены): "))
            if user_index == 0:
                return
            if 1 <= user_index <= len(transactions):
                break
            print("  Неверный номер транзакции.")
        except ValueError:
            print("  Пожалуйста, введите число.")

    current_transaction = transactions[user_index - 1]
    print(f"\nТекущие данные транзакции №{user_index}:")
    print(f"Дата: {current_transaction['date']}")
    print(f"Время: {current_transaction['time']}")
    print(f"Направление: {current_transaction['direction']}")
    print(f"Категория: {current_transaction['category']}")
    print(f"Сумма: {current_transaction['amount']:.2f}")
    print(f"Контрагент: {current_transaction['counterparty']}")

    print("\nВведите новые данные (оставьте пустым для сохранения текущего значения):")

    date_str = input(f"Дата ({current_transaction['date']}): ").strip()
    if date_str and validate_and_parse_date(date_str) is None:
        print("  Неверный формат даты. Оставляем текущее значение.")
        date_str = current_transaction['date']

    time_str = input(f"Время ({current_transaction['time']}): ").strip()
    if time_str:
        try:
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                pass
            else:
                print("  Неверный формат времени. Оставляем текущее значение.")
                time_str = current_transaction['time']
        except ValueError:
            print("  Неверный формат времени. Оставляем текущее значение.")
            time_str = current_transaction['time']
    else:
        time_str = current_transaction['time']

    direction = input(f"Направление ({current_transaction['direction']}): ").strip().lower()
    if direction and direction not in ['приход', 'расход']:
        print("  Неверное направление. Оставляем текущее значение.")
        direction = current_transaction['direction']
    elif not direction:
        direction = current_transaction['direction']

    category = input(f"Категория ({current_transaction['category']}): ").strip()
    if not category:
        category = current_transaction['category']

    amount_str = input(f"Сумма ({current_transaction['amount']:.2f}): ").strip()
    if amount_str:
        try:
            amount = float(amount_str)
            if amount >= 0:
                pass
            else:
                print("  Сумма должна быть неотрицательной. Оставляем текущее значение.")
                amount = current_transaction['amount']
        except ValueError:
            print("  Неверный формат суммы. Оставляем текущее значение.")
            amount = current_transaction['amount']
    else:
        amount = current_transaction['amount']

    counterparty = input(f"Контрагент ({current_transaction['counterparty']}): ").strip()
    if not counterparty:
        counterparty = current_transaction['counterparty']

    new_transaction = {
        'date': date_str,
        'time': time_str,
        'direction': direction,
        'category': category,
        'amount': amount,
        'counterparty': counterparty
    }

    if update_transaction(user_index - 1, new_transaction):
        print(" Транзакция успешно обновлена.")
    else:
        print(" Ошибка при обновлении транзакции.")


def delete_selected_transaction():
    """Удаляет выбранную транзакцию."""
    transactions = load_budget_transactions()
    if transactions is None:
        print(" Не удалось загрузить данные.")
        return

    display_transactions(transactions)

    if not transactions:
        return

    while True:
        try:
            user_index = int(input("Введите номер транзакции для удаления (0 для отмены): "))
            if user_index == 0:
                return
            if 1 <= user_index <= len(transactions):
                break
            print("  Неверный номер транзакции.")
        except ValueError:
            print("  Пожалуйста, введите число.")

    confirm = input(f"Вы уверены, что хотите удалить транзакцию №{user_index}? (y/n): ").strip().lower()
    if confirm == 'y':
        if delete_transaction(user_index - 1):
            print(" Транзакция успешно удалена.")
        else:
            print(" Ошибка при удалении транзакции.")
    else:
        print(" Удаление отменено.")
