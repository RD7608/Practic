import os
import csv


class Price:

    def __init__(self):
        self.data = []  # Список найденных данных
        self.result = ''
        self.previous_queries = []  # Список для сохранения предыдущих запросов

    def load_prices(self, directory=''):
        for filename in os.listdir(directory):  # Получение списка файлов
            print(f'Найден файл: {filename}', end='')
            # Фильтрация файлов, содержащих "price" в имени
            if 'price' in filename.lower():
                with open(os.path.join(directory, filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)  # Создание объекта для чтения
                    headers = next(reader)  # Получаем заголовки
                    product_col, price_col, weight_col = self._search_product_price_weight(headers)

                    # Обработка строк файла
                    for row in reader:
                        if row[product_col] and row[price_col] and row[weight_col]:
                            try:
                                name = row[product_col].strip()  # Получаем название
                                price = float(row[price_col].strip())  # Получаем цену
                                weight = float(row[weight_col].strip())  # Получаем вес
                                price_per_kg = price / weight if weight != 0 else float(
                                    'inf')  # Предотвращаем деление на ноль
                                # Добавляем данные в список
                                self.data.append((name, price, weight, filename, price_per_kg))
                            except ValueError:
                                continue  # Игнорируем строки с неправильными данными
                print(' > обработан')
            else:
                print(' > пропущен')
            # Сортировка списка товаров по наименованию и цене за кг
            self.data.sort(key=lambda x: (x[0], x[4]))  # x[0] — название, x[4] — цена за кг

    @staticmethod
    def _search_product_price_weight(headers):  # Функция поиска колонок
        # Ищем колонку с названием товара
        product_col = next(i for i, h in enumerate(headers) if h in ['продукт', 'название', 'товар', 'наименование'])

        # Ищем колонку с ценой
        price_col = next(i for i, h in enumerate(headers) if h in ['цена', 'розница'])

        # Ищем колонку с весом
        weight_col = next(i for i, h in enumerate(headers) if h in ['вес', 'масса', 'фасовка'])

        return product_col, price_col, weight_col

    # Поиск по тексту в названии товара
    def find_text(self, text):
        results = [item for item in self.data if text.lower() in item[0].lower()]  # Фильтрация по тексту
        #        results.sort(key=lambda x: x[4])  # Сортировка по цене за кг
        return results

    # Функция экспорта в HTML
    def export_to_html(self, fname='output.html'):
        result = '''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table style="width: 800px; border-collapse: collapse;">
                <tr>
                    <th style="width: 5%; text-align: left;">#</th>
                    <th style="width: 30%; text-align: left;">Название</th>
                    <th style="width: 10%; text-align: right;">Цена</th>
                    <th style="width: 10%; text-align: right;">Вес</th>
                    <th style="width: 20%; text-align: right;">Файл</th>
                    <th style="width: 15%; text-align: right;">Цена за кг</th>
                </tr>

        '''
        for idx, (name, price, weight, filename, price_per_kg) in enumerate(self.data):
            result += '<tr>'
            result += f'<td style="text-align: left;">{idx + 1}</td>'
            result += f'<td style="text-align: left; width: 30%;">{name}</td>'
            result += f'<td style="text-align: right; width: 10%;">{price:.2f}</td>'
            result += f'<td style="text-align: right; width: 10%;">{weight:.2f}</td>'
            result += f'<td style="text-align: right; width: 20%;">{filename}</td>'
            result += f'<td style="text-align: right; width: 15%;">{price_per_kg:.2f}</td>'
            result += '</tr>'

        result += '</table></body></html>'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def add_query(self, query):
        # Проверка на дублирование (существуют ли старые запросы в новом)
        if any(previous_query in query.lower() for previous_query in self.previous_queries):
            # Вывод предупреждения
            print("\033[93mПредупреждение: Этот запрос уже содержит старые запросы.\033[0m")
            # Спрашиваем пользователя, хочет ли он продолжить поиск
            user_input = input("Все равно искать? (да/нет): ").strip().lower()
            if user_input != "да":
                return False  # Если пользователь ответил не "да", возвращаем False

        # Добавление нового запроса в список
        self.previous_queries.append(query.lower())
        return True


# Основное взаимодействие с пользователем
if __name__ == "__main__":
    pm = Price()
    pm.load_prices('files/')
    pm.export_to_html('output.html')
    print("\033[32mДанные из прайс-листов сохранены в output.html.\033[0m")
    print('')
    all_results = []  # Список для хранения всех найденных результатов
    print(f"\033[1;32mДля поиска товаров введите фрагмент названия товара \n\033[33mВведите\033[31m 'exit'\033[33m для вывода результатов поиска и выхода из программы.\033[0m")
    print('')
    while True:
        query = input(f"\033[1mВведите текст для поиска или 'exit': \033[0m")
        if query.lower() == 'exit' or query.lower() == 'учше':
            break
        if pm.add_query(query):
            results = pm.find_text(query)
            all_results.extend(results)  # Добавляем найденные результаты в список результатов
            print(f"\033[3mНайдено {len(results)} позиций.\033[0m")

    if all_results:
        print(f"\nВсего найдено {len(all_results)} позиций.")
        # Вывод заголовка таблицы с выравниванием
        print(f"{'№':<4} {'Название':<25} {'Цена':>10} {'Вес':>10} {'Файл':>15} {'Цена за кг':>15}")

        # Вывод позиций в таблице с выравниванием
        for idx, (name, price, weight, filename, price_per_kg) in enumerate(all_results):
            print(f"{idx + 1:<4} {name:<25} {price:>10.2f} {weight:>10.2f} {filename:>15} {price_per_kg:>15.2f}")

#        export = input('Вы хотите сохранить результаты в файл? (да(Y)/нет(N)): ')
#        if export.lower() == 'да' or export.lower() == 'y':
#           pm.data = all_results  # Устанавливаем найденные данные как список для экспорта в HTML
#            pm.export_to_html('output.html')
#            print("Результаты сохранены в output.html.")
#        else:
#            print("Результаты не сохранены.")
    else:
        print("Ничего не найдено.")

    print('\n\033[92mРабота завершена!\033[0m')
