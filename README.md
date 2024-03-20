## Summary

1. models.py:
    - Определяет модели для Product, Order, Payment.
    - Каждая модель содержит поля, указанные в первоначальном запросе.
2. views.py:
    - Содержит функции просмотра для обработки HTTP-запросов, связанных с продуктами, заказами и платежами.
    - `get_product_list`: обрабатывает запрос GET для получения списка продуктов.
    - `create_order`: обрабатывает запрос POST для создания нового заказа на основе списка IDs продуктов.
    - `create_payment`: обрабатывает запрос POST для создания нового платежа, связанного с заказом.
3. admin.py
    - Регистрирует модели с помощью интерфейса администратора Django.
    - Определяет действие администратора `confirm_order` для модели заказа.
    - Действие `confirm_order` проверяет, является ли соответствующий статус платежа "Paid", обновляет статус заказа до "Confirmed", записывает время подтверждения, имитирует подготовку заказа с задержкой и отправляет запрос POST на сайт webhook с подробной информацией о заказе.
4. urls.py
    - Сопоставляет URL-адреса с соответствующими функциями представления, определенными в `views.py`.
    - Включает endpoints для получения списка продуктов, создания нового заказа и создания нового платежа.

Эти файлы в совокупности обеспечивают базовую структуру для управления продуктами, заказами и платежами в проекте Django, а также действия администратора для подтверждения заказов и взаимодействия с внешними службами через HTTP-запросы.


## What in this files?

****models.py****

В `models.py`, Django models определены для представления структуры данных приложения. Вот подробное описание того что делает каждая модель:

1. **Product model**:
    - Представляет продукт со следующими полями:
        - `name`: CharField для названия продукта.
        - `picture`: ImageField для хранения изображения продукта.
        - `content`: TextField для получения дополнительной информации о продукте.
        - `cost`: DecimalField для хранения стоимости продукта.
2. **Order model**:
    - Представляет заказ со следующими полями:
        - `total_amount`: DecimalField для хранения общей суммы заказа.
        - `status`: CharField для обозначения статуса ордера (например, Pending, Confirmed).
        - `creation_time`: DateTimeField для хранения “метки” времени создания заказа.
        - `confirmation_time`: DateTimeField для хранения “метки” времени подтверждения заказа.
3. **Payment model**:
    - Представляет платеж, связанный с заказом, со следующими полями:
        - `amount`: DecimalField для хранения суммы платежа.
        - `status`: CharField для указания статуса платежа (например, Pending, Paid).
        - `payment_type`: CharField для указания типа платежа (например, Online, Cash).

Эти модели определяют структуру таблиц базы данных и отношения между различными сущностями в приложении. Они обеспечивают способ взаимодействия с данными, хранящимися в базе данных, и манипулирования ими с помощью системы ORM (Object-Relational Mapping) Django. Модели инкапсулируют бизнес-логику и атрибуты данных продуктов, заказов и платежей в приложении Django.

****views.py****

1. **get_product_list function**:
    - Эта функция обрабатывает запрос GET для получения списка продуктов.
    - Она запрашивает базу данных для извлечения всех продуктов с помощью `Product.objects.all()`.
    - Она создает ответ JSON, содержащий подробную информацию о каждом продукте (name, picture URL, content, cost) в формате списка.
    - Наконец, она возвращает ответ JSON с помощью `JsonResponse`.
2. **create_order function**:
    - Эта функция обрабатывает запрос POST для создания нового заказа на основе списка ID продуктов.
    - Она извлекает список ID продуктов из данных запроса POST.
    - Она вычисляет общую сумму заказа путем суммирования стоимости выбранных продуктов.
    - Она создает новый экземпляр `Order` с рассчитанной общей суммой и текущего timestamp для времени создания.
    - Наконец, она возвращает JSON-response, содержащий ID вновь созданного заказа.
3. **create_payment function**:
    - Эта функция обрабатывает запрос POST для создания нового платежа, связанного с заказом.
    - Она извлекает идентификатор заказа из данных запроса POST.
    - Она извлекает соответствующий объект заказа из базы данных.
    - Она создает новый экземпляр `Payment` с суммой, взятой из общей суммы заказа, устанавливает тип платежа на "Online"и статус на "Pending".
    - Наконец, она возвращает JSON-ответ, содержащий идентификатор вновь созданного платежа.

Таким образом, функции в `views.py` обрабатывают различные HTTP requests, связанные с products, orders, payments.  `get_product_list` извлекает список продуктов, `create_order`. создает новый заказ на основе выбранных продуктов, а `create_payment` создает новый платеж, связанный с заказом. Каждая функция взаимодействует с базой данных для выполнения необходимых операций и возвращает JSON-responses с соответствующей информацией.

****admin.py****
1. **OrderAdmin class**:
    - **confirm_order method**:
        - Этот метод является действием администратора, определенным в `OrderAdmin` class.
        - Он срабатывает, когда пользователь-администратор выбирает один или несколько заказов и выбирает действие "Confirm selected orders"  в интерфейсе администратора.
        - Для каждого выбранного заказа он проверяет, является ли соответствующий статус платежа "Paid".
        - Если статус платежа "Paid", он обновляет статус заказа до "Confirmed" и записывает текущую дату и время в поле `confirmation_time` .
        - Затем он имитирует подготовку заказа, приостанавливая исполнение на 5 секунд с помощью `time. sleep(5`'.
        - После моделирования он создает полезную нагрузку JSON, содержащую идентификатор заказа, сумму и время подтверждения.
        - Наконец, он отправляет POST-запрос на указанный URL-адрес (`https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4`) с JSON payload в качестве тела запроса.
2. **admin.site.register**:
    - Регистрирует модели `Product`, `Order`,  `Payment` с помощью интерфейса администратора Django.
    - Это позволяет управлять этими моделями через админ-панель, где администраторы могут просматривать, добавлять, редактировать и удалять экземпляры этих моделей.
    - Регистрируя модели, Django автоматически генерирует соответствующие административные интерфейсы для этих моделей на основе определений моделей.

Таким образом, `OrderAdmin` класс в `admin.py` предоставляет действие администратора `confirm_order`, которое облегчает подтверждение заказов в админ-панели Django. Когда заказы подтверждены, действие обновляет статус заказа, записывает время подтверждения, имитирует подготовку заказа и отправляет запрос POST на сайт webhook с подробными сведениями о заказе.


****urls.py****

В `urls.py` URL-pattern(ы) определяются для сопоставления конкретных endpoint(ов) с соответствующими функциями представления в Django. Вот подробное описание того что делает каждый URL pattern:

1. **path('products/', get_product_list, name='product-list')**:
    - Этот URL pattern сопоставляет endpoint `/products/` с функцией представления `get_product_list`.
    - При запросе GET на `/products/` вызывается функция `get_product_list` для получения списка продуктов.
    - Параметр `name='product-list'` присваивает этому URL pattern имя, которое можно использовать для ссылки на него в шаблонах или коде Django.
2. **path('order/', create_order, name='create-order')**:
    - Этот URL pattern сопоставляет endpoint  `/order/` с функцией представления `create_order`.
    - При отправке запроса POST в `/order/` вызывается функция `create_order` для создания нового заказа на основе предоставленного списка ID товаров.
    - Параметр `name='create-order'` присваивает имя этому URL pattern для удобства использования.
3. **path('payment/', create_payment, name='create-payment')**:
    - Этот URL pattern сопоставляет endpoint `/payment/` с функцией представления `create_payment`.
    - При отправке запроса POST в `/payment/` вызывается функция `create_payment` для создания нового платежа, связанного с заказом.
    - Параметр `name='create-payment'` присваивает имя этому URL pattern для идентификации.

Таким образом, `urls.py` файл определяет URL pattern(ы), которые определяют, как различные HTTP-запросы направляются к определенным функциям представления в приложении Django. Каждый URL pattern определяет endpoint и связывает его с соответствующей функцией представления для обработки запроса и генерации ответа.




## How do you run this?

To run a Django project that includes the provided code snippets, you can follow these general steps:

1. **Setup Django Environment**:
    - Make sure you have Python and Django installed on your system.
    - You can install Django using pip:
        
        ```
        pip install Django
        
        ```
        
2. **Create a Django Project**:
    - Create a new Django project using the Django CLI:
        
        ```
        django-admin startproject myproject
        
        ```
        
3. **Create Django App**:
    - Create a new Django app within your project:
        
        ```
        python manage.py startapp myapp
        
        ```
        
4. **Update Files**:
    - Replace the content of the `models.py`, `views.py`, `admin.py`, and `urls.py` files in your Django app with the provided code snippets.
5. **Migrate Database**:
    - Apply migrations to create the database schema based on the models:
        
        ```
        python manage.py makemigrations
        python manage.py migrate
        
        ```
        
6. **Create Superuser**:
    - Create a superuser to access the Django admin panel:
        
        ```
        python manage.py createsuperuser
        
        ```
        
7. **Run Development Server**:
    - Start the Django development server:
        
        ```
        python manage.py runserver
        
        ```
        
8. **Access Admin Panel**:
    - Open a web browser and go to `http://127.0.0.1:8000/admin/` to access the Django admin panel.
    - Log in using the superuser credentials created earlier.
9. **Test Endpoints**:
    - Test the defined endpoints by making HTTP requests to `/products/`, `/order/`, and `/payment/` using tools like cURL, Postman, or a web browser.
10. **Interact with Admin Panel**:
    - Use the Django admin panel to manage products, orders, and payments.
    - Try confirming orders in the admin panel to trigger the actions defined in `admin.py`.

By following these steps, you should be able to run the Django project and interact with the defined models, views, and admin actions.