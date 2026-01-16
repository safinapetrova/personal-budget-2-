"""Модуль для загрузки, сохранения и управления транзакциями бюджета."""

from utils import validate_and_parse_date
from heap_sort import heap_sort

BUDGET_DATA_FILE = "budget_data.txt"


def create_sample_budget_data():
    """Создаёт файл с примерными транзакциями, если его ещё нет или он пуст."""
    try:
        with open(BUDGET_DATA_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip() == '':
                print("Файл пуст. Создаю примерные записи...")
            else:
                return
    except FileNotFoundError:
        print("Файл данных не найден. Создаю примерные записи...")

    sample_records = [
        ("2026-01-01", "09:30", "приход", "зарплата", "50000.00", "Работодатель АО"),
        ("2026-01-01", "10:45", "приход", "стипендия", "3124.00", "ПГНИУ"),
        ("2026-01-02", "13:00", "приход", "аванс", "20000.00", "Работодатель АО"),
        ("2026-01-03", "12:00", "расход", "питание", "450.00", "Ресторан"),
        ("2026-01-04", "14:00", "приход", "подарок", "3000.00", "Дедушка"),
        ("2026-01-05", "12:00", "расход", "питание", "280.00", "Столовая"),
        ("2026-01-05", "12:00", "расход", "питание", "280.00", "Кафе"),
        ("2026-01-05", "14:00", "расход", "питание", "350.00", "Ресторан"),
        ("2026-01-06", "12:00", "расход", "транспорт", "100.00", "Метро"),
        ("2026-01-06", "14:00", "расход", "транспорт", "100.00", "Автобус"),
        ("2026-01-06", "16:00", "расход", "транспорт", "150.00", "Такси"),
        ("2026-01-06", "16:00", "приход", "подарок", "5000.00", "Мама"),
        ("2026-01-07", "10:00", "расход", "развлечения", "500.00", "Игровой клуб"),
        ("2026-01-07", "12:00", "расход", "развлечения", "500.00", "Кино"),
        ("2026-01-07", "13:00", "приход", "аванс", "15000.00", "Работодатель АО"),
        ("2026-01-07", "14:00", "расход", "развлечения", "900.00", "Бильярд"),
        ("2026-01-08", "10:00", "расход", "подарок", "750.00", "Подруга"),
        ("2026-01-08", "12:00", "расход", "подарок", "750.00", "Коллега"),
        ("2026-01-08", "14:00", "расход", "подарок", "1000.00", "Мама"),
        ("2026-01-09", "09:00", "приход", "зарплата", "50000.00", "Работодатель АО"),
        ("2026-01-10", "11:00", "приход", "фриланс", "12000.00", "Клиент ИП"),
        ("2026-01-10", "18:30", "расход", "развлечения", "1200.00", "Концерт"),
        ("2026-01-10", "19:00", "расход", "развлечения", "1200.00", "Театр"),
        ("2026-01-12", "15:30", "приход", "дивиденды", "8500.00", "Брокер ООО"),
        ("2026-01-15", "10:00", "приход", "возврат", "1200.00", "Магазин Техно"),
        ("2026-01-15", "20:15", "расход", "одежда", "4500.00", "Бутик"),
        ("2026-01-18", "14:20", "приход", "премия", "25000.00", "Работодатель АО"),
        ("2026-01-20", "09:15", "приход", "сдача квартиры", "35000.00", "Арендатор"),
        ("2026-01-20", "13:40", "расход", "аптека", "890.00", "Аптека Здоровье"),
        ("2026-01-25", "16:45", "приход", "подработка", "7500.00", "Коллега"),
    ]

    with open(BUDGET_DATA_FILE, 'w', encoding='utf-8') as file:
        for record in sample_records:
            file.write("\t".join(record) + "\n")
    print(f" Файл '{BUDGET_DATA_FILE}' создан с {len(sample_records)} записями.\n")


def load_budget_transactions():
    """Загружает транзакции из файла. Возвращает список словарей или None при ошибке."""
    try:
        with open(BUDGET_DATA_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f" Файл '{BUDGET_DATA_FILE}' не найден.")
        create_sample_budget_data()
        return load_budget_transactions()
    except Exception as error:
        print(f" Ошибка при чтении файла: {error}")
        return None

    transactions_list = []
    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split('\t')
        if len(parts) != 6:
            print(f"  Неверный формат строки {line_number} — пропущена.")
            continue

        date_str, time_str, transaction_direction, category_name, amount_str, counterparty_name = parts
        try:
            amount_value = float(amount_str)
        except ValueError:
            print(f"  Некорректная сумма в строке {line_number} — пропущена.")
            continue

        transaction_record = {
            'date': date_str,
            'time': time_str,
            'direction': transaction_direction,
            'category': category_name,
            'amount': amount_value,
            'counterparty': counterparty_name,
        }
        transactions_list.append(transaction_record)

    return transactions_list


def _sort_transactions_chronologically(transactions):
    """
    Сортирует список транзакций по дате и времени по возрастанию.
    Использует временный ключ '_sort_key' и heap_sort.
    """
    if not transactions:
        return

    for transaction in transactions:
        # Парсим дату
        parsed = validate_and_parse_date(transaction['date'])
        if parsed:
            year, month, day = parsed
        else:
            year, month, day = 9999, 99, 99

        # Парсим время
        try:
            time_parts = transaction['time'].split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except (ValueError, IndexError, AttributeError):
            hour, minute = 99, 99

        transaction['_sort_key'] = (year, month, day, hour, minute)

    heap_sort(transactions, '_sort_key', reverse=False)

    for transaction in transactions:
        del transaction['_sort_key']


def save_budget_transactions(transactions):
    """Сохраняет транзакции в файл в хронологическом порядке."""
    _sort_transactions_chronologically(transactions)
    try:
        with open(BUDGET_DATA_FILE, 'w', encoding='utf-8') as file:
            for transaction in transactions:
                record = (
                    transaction['date'],
                    transaction['time'],
                    transaction['direction'],
                    transaction['category'],
                    str(transaction['amount']),
                    transaction['counterparty']
                )
                file.write("\t".join(record) + "\n")
        print(f" Данные успешно сохранены в файл '{BUDGET_DATA_FILE}'.")
    except Exception as error:
        print(f" Ошибка при сохранении файла: {error}")


def add_transaction(transaction):
    """
    Добавляет новую транзакцию в базу данных.
    Принимает словарь с ключами: date, time, direction, category, amount, counterparty.
    Возвращает True при успехе, False при ошибке.
    """
    transactions = load_budget_transactions()
    if transactions is None:
        return False

    transactions.append(transaction)
    save_budget_transactions(transactions)
    return True


def delete_transaction(index):
    """
    Удаляет транзакцию по индексу (начиная с 0).
    Возвращает True при успехе, False при ошибке.
    """
    transactions = load_budget_transactions()
    if transactions is None:
        return False

    if 0 <= index < len(transactions):
        transactions.pop(index)
        save_budget_transactions(transactions)
        return True
    return False


def update_transaction(index, new_transaction):
    """
    Обновляет транзакцию по индексу (начиная с 0).
    Принимает новый словарь транзакции.
    Возвращает True при успехе, False при ошибке.
    """
    transactions = load_budget_transactions()
    if transactions is None:
        return False

    if 0 <= index < len(transactions):
        transactions[index] = new_transaction
        save_budget_transactions(transactions)
        return True
    return False
