title: Работа с данными

## Работа с данными {#work-with-data}

В разделе Working with Transactions and the DBAPI мы изучили основы взаимодействия с Python DBAPI и его транзакционное
состояние. Затем, в разделе Working with Database Metadata, мы изучили, как представлять таблицы, столбцы и ограничения
базы данных в SQLAlchemy с помощью объектов MetaData и связанных с ними объектов. В этом разделе мы объединим оба
вышеупомянутых концепта, чтобы создавать, выбирать и изменять данные в реляционной базе данных. Наше взаимодействие с
базой данных всегда осуществляется в терминах транзакции, даже если мы настроили наш драйвер базы данных на
использование автозавершения транзакций за кулисами.

Компоненты этого раздела следующие:

- **Использование операторов INSERT** - чтобы добавить данные в базу данных, мы представляем и демонстрируем конструкцию
  Core Insert. Операторы INSERT с точки зрения ORM описываются в следующем разделе Data Manipulation with the ORM.
- **Использование операторов SELECT** - в этом разделе мы подробно описываем конструкцию Select, которая является
  наиболее часто используемым объектом в SQLAlchemy. Конструкция Select генерирует операторы SELECT как для приложений,
  основанных на Core, так и для ORM-центрических приложений, и оба случая использования будут описаны здесь.
  Дополнительные ORM-варианты использования также отмечены в более позднем разделе Using Relationships in Queries, а
  также в руководстве по ORM-запросам.
- **Использование операторов UPDATE и DELETE** - завершая INSERT и SELECT данных, этот раздел описывает с Core-точки
  зрения использование конструкций Update и Delete. ORM-специфические операторы UPDATE и DELETE также описаны в разделе
  Data Manipulation with the ORM

### Использование операторов INSERT {#data-insert}

При использовании Core, а также при использовании ORM для массовых операций, SQL-запрос INSERT генерируется
непосредственно с помощью функции `insert()` - эта функция генерирует новый экземпляр Insert, который представляет собой
оператор INSERT в SQL, добавляющий новые данные в таблицу.

!!! info "Читателям ORM"

    Этот раздел подробно описывает средства Core для генерации отдельного SQL-запроса INSERT для добавления новых строк в
    таблицу. При использовании ORM мы обычно используем другой инструмент, который работает поверх этого, называемый
    единицей работы, который автоматизирует создание множества запросов INSERT одновременно. Однако понимание того, как Core
    обрабатывает создание и изменение данных, очень полезно, даже когда ORM выполняет это за нас. Кроме того, ORM
    поддерживает прямое использование оператора INSERT с помощью функции Bulk / Multi Row INSERT, upsert, UPDATE и DELETE.
    
    Чтобы перейти непосредственно к способу вставки строк с помощью ORM, используя стандартный шаблон единицы работы, см.
    Вставка строк с использованием шаблона единицы работы ORM.

#### Конструкция SQL-выражения insert() {#the-insert-sql-expression-construct}

Простой пример Insert, иллюстрирующий целевую таблицу и предложение VALUES одновременно:

``` python
>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

Переменная stmt, указанная выше, является экземпляром Insert. Большинство SQL-выражений могут быть преобразованы в
строку, чтобы увидеть общую форму того, что генерируется:

``` python
>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

Строковое представление создается путем создания скомпилированной формы объекта, которая включает в себя специфичное для
базы данных строковое представление SQL-оператора; мы можем получить этот объект напрямую, используя метод
`ClauseElement.compile()`:

``` python
>>> compiled = stmt.compile()
```

Наша конструкция Insert является примером «параметризованной» конструкции, которая была показана ранее в разделе
Отправка параметров; чтобы просмотреть имена и полные имена связанных параметров, они также доступны в скомпилированной
конструкции:

``` python
>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
```

#### Выполнение запроса {#executing-the-statement}

Для выполнения запроса на вставку новой строки в таблицу `user_table`, мы можем использовать метод `conn.execute(stmt)`
объекта соединения, передав ему наш объект `stmt` с SQL выражением. Затем мы фиксируем транзакцию, вызывая
метод `commit()` объекта соединения:

```python
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
```

В логе SQL-запросов мы можем увидеть сформированный SQL-запрос, а также значения переданных параметров:

```sql
BEGIN
    (implicit)
    INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('spongebob', 'Spongebob Squarepants')
COMMIT
```

Так как в приведенном выше запросе на вставку не возвращается никаких строк, в случае, когда вставляется только одна
строка, обычно можно получить информацию о значениях колонок сгенерированных по умолчанию, например, о значении
первичного ключа. В данном случае, первая строка в базе данных SQLite обычно вернет 1 для первичного ключа, который мы
можем получить, используя атрибут `inserted_primary_key` объекта `result`:

```python
result.inserted_primary_key
(1,)
```

!!! tip "Совет"

    CursorResult.inserted_primary_key возвращает кортеж, поскольку первичный ключ может содержать несколько столбцов. Это
    известно как составной первичный ключ. CursorResult.inserted_primary_key должен всегда содержать полный первичный ключ
    только что вставленной записи, а не только значение вроде “cursor.lastrowid”. Он также должен быть заполнен вне
    зависимости от того, использовалось ли “autoincrement” или нет, чтобы выразить полный первичный ключ, это кортеж.

!!! warning "Изменено в версии 1.4.8"

    Кортеж, возвращаемый CursorResult.inserted_primary_key, теперь является именованным кортежем,
    возвращаемым в виде объекта Row.

#### INSERT-запрос обычно автоматически генерирует часть "values". {#insert-usually-generates-the-values-clause-automatically}

В приведенном выше примере использовался метод
Insert.values(), чтобы явно создать часть VALUES SQL INSERT-запроса. Если мы не используем Insert.values() и просто
выведем "пустой" запрос, мы получим INSERT для каждого столбца в таблице:

```
>>> print(insert(user_table))

INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)
```

Если мы возьмем конструкцию Insert, которая не вызывала метод Insert.values(), а затем выполним ее, а не выведем на
экран, запрос будет скомпилирован в строку на основе параметров, которые мы передали методу Connection.execute(), и
будут включены только столбцы, связанные с переданными параметрами. Это, на самом деле, обычный способ использования
Insert для вставки строк без явного указания части VALUES. Приведенный ниже пример демонстрирует выполнение запроса
INSERT с двумя столбцами и списком параметров сразу:

``` python

>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(user_table),
...         [
...             {"name": "sandy", "fullname": "Sandy Cheeks"},
...             {"name": "patrick", "fullname": "Patrick Star"},
...         ],
...     )
...     conn.commit()


BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] [('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star')]
COMMIT

```

В приведенном выше выполнении используется форма "executemany", впервые продемонстрированная в разделе Sending Multiple
Parameters, однако в отличие от использования конструкции text(), нам не нужно указывать SQL-запрос явно. Передав
словарь или список словарей методу Connection.execute() в сочетании с конструкцией Insert, соединение гарантирует, что
имена столбцов, которые передаются, будут автоматически выражены в части VALUES конструкции Insert.

???+ info "Глубокая Алхимия"

    Deep Alchemy: Использование scalar subquery в методе Insert.values() библиотеки SQLAlchemy
    
    В этой статье мы рассмотрим более продвинутый пример использования метода `Insert.values()` библиотеки SQLAlchemy. В данном примере будет использован scalar subquery, созданный с помощью метода `select()`, а также явно указанные параметры, заданные с помощью метода `bindparam()`. 
    
    Scalar subquery используется для того, чтобы добавлять связанные строки в таблицу без получения первичных ключей из user_table. Обычно в ORM SQLAlchemy эта задача выполняется автоматически.
    
    ``` python
    from sqlalchemy import select, bindparam
    
    # Создание scalar subquery
    scalar_subq = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )
    
    # Добавление данных в таблицу address_table с использованием scalar subquery и явно заданных параметров
    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subq),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@sqlalchemy.org",
                },
                {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
            ],
        )
        conn.commit()

    # SQL
    BEGIN (implicit)
    INSERT INTO address (user_id, email_address) VALUES ((SELECT user_account.id
    FROM user_account
    WHERE user_account.name = ?), ?)
    [...] [('spongebob', 'spongebob@sqlalchemy.org'), ('sandy', 'sandy@sqlalchemy.org'),
    ('sandy', 'sandy@squirrelpower.org')]
    COMMIT
    ```
    
    Выполнение этого кода добавит данные в таблицу address_table, используя scalar subquery для задания user_id без получения первичных ключей из user_table.
    
    Мы надеемся, что этот пример поможет вам лучше понять, как использовать библиотеку SQLAlchemy для работы с базами данных.

!!! tip "Tip"

    A true “empty” INSERT that inserts only the “defaults” for a table without including any explicit values at all is generated if we indicate Insert.values() with no arguments; not every database backend supports this, but here’s what SQLite produces:
    
    ```
    >>> print(insert(user_table).values().compile(engine))
    
    # SQL
    INSERT INTO user_account DEFAULT VALUES

    ```

#### INSERT…RETURNING {#insert-returning}

Выражение `RETURNING` для поддерживаемых бэкендов используется автоматически для извлечения последнего вставленного
значения
первичного ключа, а также значений для серверных значений по умолчанию. Однако выражение `RETURNING` также может быть
явно
указана с помощью метода `Insert.returning()`; в этом случае объект `Result`, который возвращается при выполнении
операции,
имеет строки, которые могут быть извлечены:

``` python
>>> insert_stmt = insert(address_table).returning(
>>> ... address_table.c.id, address_table.c.email_address
>>> ... )
>>> print(insert_stmt)

# SQL
INSERT INTO address (id, user_id, email_address)
VALUES (:id, :user_id, :email_address)
RETURNING address.id, address.email_address
```

Она также может быть объединена с `Insert.from_select()`, как показано в примере ниже, который базируется на примере,
указанном в INSERT…FROM SELECT:

``` python
>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
>>> ...     ["user_id", "email_address"], select_stmt
>>> ... )
>>> print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))

# SQL
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account RETURNING address.id, address.email_address

```

!!! tip "Совет"

    Функция RETURNING также поддерживается в операторах UPDATE и DELETE, которые будут рассмотрены позже в этом учебнике.
    
    Для операторов INSERT функцию RETURNING можно использовать как для операторов, вставляющих одну строку, так и для
    операторов, вставляющих несколько строк одновременно. Поддержка функции вставки нескольких строк с RETURNING зависит от
    диалекта и поддерживается для всех диалектов, включенных в SQLAlchemy, которые поддерживают RETURNING. Дополнительную
    информацию об этой функции можно найти в разделе Поведение операторов INSERT для вставки множества значений.

!!! quote "Смотрите также"

    ORM также поддерживает массовую вставку с RETURNING или без нее. См. Документацию по массовой вставке ORM.

#### INSERT…FROM SELECT {#insert-from-select}

Конструкция Insert может составлять INSERT-запрос, который напрямую получает строки из запроса SELECT с помощью метода
Insert.from_select(). Этот метод принимает конструкцию select(), о которой будет рассказано в следующем разделе, а также
список имен столбцов, которые должны быть целевыми в самом INSERT. В приведенном ниже примере строки добавляются в
таблицу address, которые получены из строк таблицы user_account, предоставляя каждому пользователю бесплатный адрес
электронной почты на aol.com:

``` python
>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
>>> ...     ["user_id", "email_address"], select_stmt
>>> ... )
>>> print(insert_stmt)

# SQL
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account
```

Эта конструкция используется, когда нужно скопировать данные из другой части базы данных непосредственно в новый набор
строк, не извлекая и не отправляя данные с клиента. 

### Использование операторов SELECT
...to be continued...