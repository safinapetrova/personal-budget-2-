from display import (
    display_main_menu,
    wait_for_user_to_return,
    add_new_transaction,
    edit_transaction,
    delete_selected_transaction,
    display_transactions
)
from data_loader import (
    load_budget_transactions,
    create_sample_budget_data
)
from reports import (
    generate_income_report_last_n_days,
    generate_expense_report_by_category,
    generate_expense_report_in_time_interval
)


def get_valid_n_days() -> int:
    """Запрашивает у пользователя корректное N (неотрицательное целое число)."""
    while True:
        days_input = input(
            "Введите количество дней N (целое неотрицательное число, например 3): "
        ).strip()
        if days_input.isdigit():
            return int(days_input)
        else:
            print(" Некорректный ввод. Пожалуйста, введите целое число ≥ 0.")


def get_non_empty_category() -> str:
    """Запрашивает непустую категорию."""
    while True:
        category = input("Введите категорию (например, питание, транспорт): ").strip()
        if category:
            return category
        else:
            print(" Категория не может быть пустой. Попробуйте снова.")


def get_valid_time(prompt: str) -> str:
    """Запрашивает корректное время в формате ЧЧ:ММ."""
    while True:
        time_str = input(prompt).strip()
        time_parts = time_str.split(':')
        if len(time_parts) == 2:
            try:
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                if 0 <= hours <= 23 and 0 <= minutes <= 59:
                    return f"{hours:02d}:{minutes:02d}"
            except ValueError:
                pass
        print(" Неверный формат времени. Используйте ЧЧ:ММ (например, 18:30).")


def handle_income_report():
    days_input = get_valid_n_days()
    transactions = load_budget_transactions()
    if transactions is not None:
        generate_income_report_last_n_days(transactions, days_input)
        wait_for_user_to_return()


def handle_expense_report_by_category():
    category = get_non_empty_category()
    transactions = load_budget_transactions()
    if transactions is not None:
        generate_expense_report_by_category(transactions, category)
        wait_for_user_to_return()


def handle_expense_report_in_time_interval():
    start_time = get_valid_time("Начало интервала (ЧЧ:ММ, например 18:00): ")
    end_time = get_valid_time("Конец интервала (ЧЧ:ММ, например 21:00): ")

    # Сравниваем строки напрямую — безопасно для формата ЧЧ:ММ
    if start_time > end_time:
        print(" Начало интервала позже конца. Отчёт может быть пустым.")

    transactions = load_budget_transactions()
    if transactions is not None:
        generate_expense_report_in_time_interval(transactions, start_time, end_time)
        wait_for_user_to_return()


def main():
    print("Добро пожаловать в программу 'Персональный бюджет'")
    create_sample_budget_data()

    while True:
        display_main_menu()
        user_choice = input("Выберите действие (1-8): ").strip()

        if user_choice == "1":
            transactions = load_budget_transactions()
            if transactions is None:
                print(" Не удалось загрузить данные.")
            else:
                display_transactions(transactions)
            wait_for_user_to_return()

        elif user_choice == "2":
            add_new_transaction()

        elif user_choice == "3":
            edit_transaction()
            wait_for_user_to_return()

        elif user_choice == "4":
            delete_selected_transaction()

        elif user_choice == "5":
            handle_income_report()

        elif user_choice == "6":
            handle_expense_report_by_category()

        elif user_choice == "7":
            handle_expense_report_in_time_interval()

        elif user_choice == "8":
            print(" До свидания! Бюджет сохранён.")
            break

        else:
            print(" Некорректный выбор. Введите число от 1 до 8.")


if __name__ == "__main__":
    main()
