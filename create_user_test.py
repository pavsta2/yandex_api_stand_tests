import data, sender_stand_request


def get_user_body(first_name)-> dict:
    """
    Функция для создания user_body с разными именами
    :param first_name: значение имени пользователя, с которым надо создать user_body
    :return: словать user_body
    """
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body


def positive_assert(first_name) -> None:
    """
    Функция для проверки позитивных сценариев создания пользователя
    :param first_name: Имя пользователя
    :return: None
    """
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name) -> None:
    """
    Функция для негативных тестов создания пользователя
    :param first_name: имя пользователя
    :return: None
    """
    # получаем тело запроса с нужным именем и сохраняем в user_body
    user_body = get_user_body(first_name)

    # получаем и сохраняем в user_response ответ сервера
    user_response = sender_stand_request.post_new_user(user_body)

    # проверяем, что код ответа равен 400
    assert user_response.status_code == 400

    # проверяем, что в теле ответа параметр code равен 400
    assert user_response.json()['code'] == 400

    # проверяем, что в ответе параметр message равен тексту с сообщением об ошибке
    assert user_response.json()['message'] == ("Имя пользователя введено некорректно. Имя может содержать только русские или "
                                               "латинские буквы, длина должна быть не менее 2 и не более 15 символов")


def negative_assert_no_firstname(user_body: dict) -> None:
    """
    Функция для негативных тестов создания пользователя, когда не передано Имя
    :param user_body: словарь с телом запроса (данне пользователя)
    :return: None
    """
    # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_user(user_body)

    # Проверь, что код ответа — 400
    assert response.status_code == 400

    # Проверь, что в теле ответа атрибут "code" — 400
    assert response.json()["code"] == 400

    # Проверь текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Тест 2. Неуспешное создание пользователя
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Тест 3. Неуспешное создание пользователя
# Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Тест 4. Успешное создание пользователя
# Параметр fisrtName состоит из англ.букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 5. Успешное создание пользователя
# Параметр fisrtName состоит из русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 6. Неуспешное создание пользователя
# Параметр fisrtName содержит пробел
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

# Тест 7. Неуспешное создание пользователя
# Параметр fisrtName содержит спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Тест 8. Неуспешное создание пользователя
# Параметр fisrtName содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 9. Неуспешное создание пользователя
# Параметр fisrtName не передан
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

# Тест 10. Неуспешное создание пользователя
# Параметр fisrtName содержит пустое значение
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

# Тест 11. Неуспешное создание пользователя
# Параметр fisrtName содержит НЕ строковое значение
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    negative_assert_no_firstname(user_body)
