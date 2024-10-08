# library
library

Первым делом необходимо склонировать репозиторий на локальную машину.
Для этого открываем консоль, переходим на необходимую директорию и пишем команду "git clone https://github.com/MarselMi/library.git".
Далее переходим в директорию проекта и создаем виртуальное окружения для данного приложения.

1. Запуск приложения через Docker-compose.
2. В консоле выполняете команду "docker-compose build".
3. Далее "docker-compose up -d".
4. Необходимо войти в контейнер чтоб создать суперпользователся, в консоле вводим команду "docker-compose exec web bash", будет предложено заполнить основные поля для суперпользователя.
5. Выходим из консоли контейнера написав exit.
6. После успешного создания суперпользователя можно переходить к пункту 11.

7. Если запускаете приложение используя стандартные команды: 
8. Необходимо установить зависимости для корректной работы, для этого активируем виртуальное окружени и устанавливаем зависимоти командой "pip install -r requirements.txt".
9. Последовательно выполняем команды "python manage.py makemigrations", "python manage.py migrate".
10. Создаем супераользователя командой "python manage.py createsuperuser". Далее в консоле будет предложено заполнить основные поля для суперпользователя.
11. Запуск приложения осуществляется командой "python manage.py runserver".
12. Но тк БД пустая, лучше авторизоваться через админку. Для этого в адресную строку браузера дописываем admin/.
13. Проходим авторизацию, и заполняем необходимые данные. 
Это:
1 - Жанры книг;
2 - Создаем книги;
Этого достаточно, пользователей можем создавать через форму регистрации.
13. Выходим из аккаунта суперпользователя, и по ссылке переходим на страницу регистрацию пользователя. Там у нас есть вариант создания "Читателя" либо "Библиотекаря". Выбираем нужный вариант. После регистрации происходит редирект на страницу авторизации, вводим свои необходимые данные и авторизуемся, пользуемся.
14. API становится доступно после прохождения авторизации по JWT-token. На каждом эндпоинте стоит декоратор, который закрывает доступ неавторизованным пользователям. Для этого пользователь сначала должен авторизоваться POST-запросом набрав имя пользователя и пароль на эндпоинте "api-v1/token/". В ответ придет "refresh", "access" токены. После выхода из жизни access токена необходимо сделать рефреш "api-v1/token/refresh/" указав refresh-токен, в ответ придет refresh, access токены. Для использования основых эндпоитов в заголовках необходимо указывать 'Authorization': `Bearer ${accessToken}`.
Документация на API доступна по эндпоинтам: ["redoc/", "swagger/"].

Программа предусматривает что в библиотеке хранится неограниченное количество одинаковых книг, поэтому если какой нибудь пользователь возмет одну книгу для прочтения, для других пользователей данная книга так же будет доступна.
