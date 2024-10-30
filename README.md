Описание проекта
Данный проект предназначен для обработки и анализа данных о продуктах из CSV файлов, содержащих информацию о ценах и весах товаров. Целью приложения является поиск продуктов по их названиям и вывод информации в полезном формате. Утилита также поддерживает экспорт данных в формат HTML для удобного просмотра.

Основные функции
Загрузка цен: Чтение всех CSV файлов из указанной директории, содержащих "price" в названии. Информация о товарах (название, цена, вес) загружается в память.
Экспорт результатов в HTML: Сохранение всех загруженных данных в удобный HTML файл для просмотра.
Поиск товара: Возможность поиска товара по фрагменту названия.
Проверка предыдущих запросов: Отслеживание ранее введённых запросов с возможностью предупреждения о дублировании.

Установка
Для работы приложения требуется Python 3.x и несколько стандартных библиотек. Убедитесь, что они установлены, и скачайте проект в локальную директорию.

Убедитесь, что у вас есть директория files/ с необходимыми CSV файлами.

Использование
Запустите скрипт: python project.py

Введите фрагмент названия товара для поиска, или введите 'exit', чтобы завершить работу программы.
Все найденные результаты будут отображены в консоли.


Примеры работы:

Загрузка данных
![start.png](screenshots%2Fstart.png)

Поиск товара
![search.png](screenshots%2Fsearch.png)

Результаты
![result.png](screenshots%2Fresult.png)