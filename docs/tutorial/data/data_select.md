title: Использование операторов SELECT

## Использование оператора SELECT

Для Core и ORM
функция [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
генерирует
конструкцию [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
которая используется для всех запросов SELECT. Передается методам, таким
как [`Connection.execute()`](../core/connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")
в Core и [`Session.execute()`](../orm/session_api.html#sqlalchemy.orm.Session.execute "sqlalchemy.orm.Session.execute")
в ORM, и выдается SELECT-запрос в текущей транзакции, а строки результата доступны через возвращаемый
объект [`Result`](../core/connections.html#sqlalchemy.engine.Result "sqlalchemy.engine.Result").

**ORM Читатели** - содержание здесь одинаково хорошо применимо как к Core, так и к ORM использованию, и здесь
упоминаются базовые варианты использования ORM. Однако также доступно много других специфических для ORM функций; они
документированы в [ORM Querying Guide](../orm/queryguide/index.html).

### Конструкция select() SQL Expression

Конструкция [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
строит оператор таким же образом,
как [`insert()`](../core/dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"),
используя [генеративный](../glossary.html#term-generative) подход, где каждый метод добавляет больше состояния в объект.
Как и другие SQL-конструкции, его можно преобразовать в строку на месте:

```
>>> from sqlalchemy import select
>>> stmt = select(user_table).where(user_table.c.name == "spongebob")
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1
```

Также так же, как и все другие SQL-конструкции на уровне оператора, чтобы фактически выполнить оператор, мы передаем его
методу выполнения. Поскольку оператор SELECT возвращает строки, мы всегда можем перебирать объект результата, чтобы
получить обратно объекты [`Row`](../core/connections.html#sqlalchemy.engine.Row "sqlalchemy.engine.Row"):

```
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(1, 'spongebob', 'Spongebob Squarepants')
ROLLBACK
```

При использовании ORM, особенно с
конструкцией [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
которая составляется против сущностей ORM, мы захотим выполнить ее, используя
метод [`Session.execute()`](../orm/session_api.html#sqlalchemy.orm.Session.execute "sqlalchemy.orm.Session.execute")
на [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"); используя этот подход, мы
продолжаем получать объекты [`Row`](../core/connections.html#sqlalchemy.engine.Row "sqlalchemy.engine.Row")

### Установка COLUMNS и FROM clause {#tutorial-selecting-columns}

Функция [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
принимает позиционные элементы, представляющие любое количество
выражений [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
и/или [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), а также широкий спектр
совместимых объектов, которые преобразуются в список SQL-выражений, которые будут выбраны и возвращены в качестве
столбцов в результате. Эти элементы также используются в более простых случаях для создания FROM clause, которая
выводится из переданных столбцов и выражений, похожих на таблицы:

```
>>> print(select(user_table))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account


```

Для выбора отдельных столбцов с помощью подхода Core
объекты [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") получаются из доступа
к [`Table.c`](../core/metadata.html#sqlalchemy.schema.Table.c "sqlalchemy.schema.Table.c") и могут быть отправлены
непосредственно; FROM clause будет выведен как набор
всех [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") и
других [`FromClause`](../core/selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
объектов, которые представлены этими столбцами:

```
>>> print(select(user_table.c.name, user_table.c.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account


```

В качестве альтернативы, при использовании
коллекции [`FromClause.c`](../core/selectable.html#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
любого [`FromClause`](../core/selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
такого как [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
для [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select") могут быть
указаны несколько столбцов с помощью кортежа строковых имен:

```
>>> print(select(user_table.c["name", "fullname"]))
SELECT user_account.name, user_account.fullname
FROM user_account


```

Новое в версии 2.0: Добавлена возможность доступа к кортежам в коллекции :attr`.FromClause.c`

#### Выбор ORM-сущностей и столбцов {#tutorial-selecting-orm-entities}

ORM-сущности, такие как наш класс `User`, а также отображаемые на них столбцы, такие как `User.name`, также участвуют в
системе языка выражений SQL Expression, представляя таблицы и столбцы. Ниже приведен пример выбора из сущности `User`,
который в конечном итоге отображается так же, как если бы мы использовали `user_table` напрямую:

Вышеуказанный [`Row`](../core/connections.html#sqlalchemy.engine.Row "sqlalchemy.engine.Row") имеет только один элемент,
представляющий сущность `User`:

```

> > > row[0]
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants')

```

Высоко рекомендуемым методом для достижения того же результата, что и выше, является использование
метода [`Session.scalars()`](../orm/session_api.html#sqlalchemy.orm.Session.scalars "sqlalchemy.orm.Session.scalars")
для выполнения оператора
непосредственно; этот метод вернет
объект [`ScalarResult`](../core/connections.html#sqlalchemy.engine.ScalarResult "sqlalchemy.engine.ScalarResult"),
который
одновременно доставляет первый «столбец» каждой строки, в данном случае,
экземпляры класса `User`:

```

> > > user = session.scalars(select(User)).first()
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
[...] ()
> > > user
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants')

```

В качестве альтернативы мы можем выбирать отдельные столбцы сущности ORM в качестве отдельных
элементов в строках результата, используя привязанные к классу атрибуты; когда они
передаются в такую конструкцию,
как [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"), они
разрешаются в
[`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") или другое SQL-выражение,
представленное каждым
атрибут:

```

> > > print(select(User.name, User.fullname))
> > > SELECT user_account.name, user_account.fullname
> > > FROM user_account

```

Когда мы вызываем *этот* оператор с
помощью [`Session.execute()`](../orm/session_api.html#sqlalchemy.orm.Session.execute "sqlalchemy.orm.Session.execute"),
мы теперь
получаем строки, которые имеют отдельные элементы для каждого значения, каждый соответствующий
отдельному столбцу или другому SQL-выражению:

```

> > > row = session.execute(select(User.name, User.fullname)).first()
> > > SELECT user_account.name, user_account.fullname
> > > FROM user_account
[...] ()
> > > row
('spongebob', 'Spongebob Squarepants')

```

Подходы также могут быть смешаны, как в примере ниже, где мы выбираем атрибут `name`
сущности `User` в качестве первого элемента строки и объединяем
его с полными сущностями `Address` во втором элементе:

```
>>> session.execute(
...     select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
... ).all()
SELECT user_account.name, address.id, address.email_address, address.user_id
FROM user_account, address
WHERE user_account.id = address.user_id ORDER BY address.id
[...] ()
[('spongebob', Address(id=1, email_address='spongebob@sqlalchemy.org')),
('sandy', Address(id=2, email_address='sandy@sqlalchemy.org')),
('sandy', Address(id=3, email_address='sandy@squirrelpower.org'))]

```

[`ColumnElement.label()`](../core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label"),
а также метод с тем же именем, доступный в ORM-атрибутах, предоставляет SQL-метку столбца или выражения, позволяя ему
иметь определенное имя в наборе результатов. Это может быть полезно при обращении к произвольным SQL-выражениям в строке
результата по имени:

```
>>> from sqlalchemy import func, cast
>>> stmt = select(
...     ("Username: " + user_table.c.name).label("username"),
... ).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.username}")
BEGIN (implicit)
SELECT ? || user_account.name AS username
FROM user_account ORDER BY user_account.name
[...] ('Username: ',)
Username: patrick
Username: sandy
Username: spongebob
ROLLBACK
```

!!! info "См. также"

    [Упорядочивание или группировка по метке](#tutorial-order-by-label) - имена меток, которые мы создаем, также могут быть
    использованы в клаузе ORDER BY или GROUP
    BY [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select").

#### Выбор с текстовыми столбцовыми выражениями {#tutorial-select-arbitrary-text}

Когда мы создаем
объект [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
используя
функцию [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"), мы
обычно передаем ему серию объектов [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
и [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"), которые были определены с
использованием [метаданных таблицы](metadata.html#tutorial-working-with-metadata), или при использовании ORM мы можем
отправлять атрибуты ORM, которые представляют столбцы таблицы. Однако иногда также требуется создавать произвольные
SQL-блоки внутри операторов, такие как константные строковые выражения или просто какой-то произвольный SQL, который
быстрее написать буквально.

Конструкция [`text()`](../core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text"),
введенная в [Работа с транзакциями и DBAPI](dbapi_transactions.html#tutorial-working-with-transactions), может
фактически быть встроена в
конструкцию [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
непосредственно, например, ниже, где мы создаем жестко закодированную строковую литеру `'some phrase'` и встраиваем ее в
оператор SELECT:

```
>>> from sqlalchemy import text
>>> stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     print(conn.execute(stmt).all())
BEGIN (implicit)
SELECT 'some phrase', user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
[('some phrase', 'patrick'), ('some phrase', 'sandy'), ('some phrase', 'spongebob')]
ROLLBACK
```

Хотя конструкция [`text()`](../core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
может использоваться в большинстве случаев для вставки литеральных фраз SQL, чаще всего мы имеем дело с текстовыми
единицами, каждая из которых представляет отдельное выражение столбца. В этом общем случае мы можем получить больше
функциональности из нашего текстового фрагмента, используя
конструкцию [`literal_column()`](../core/sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")
вместо этого. Этот объект похож
на [`text()`](../core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text"), за исключением
того, что вместо представления произвольного SQL любой формы он явно представляет отдельный "столбец" и может быть
помечен и обращаться к нему в подзапросах и других выражениях:

```
>>> from sqlalchemy import literal_column
>>> stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
...     user_table.c.name
... )
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.p}, {row.name}")
BEGIN (implicit)
SELECT 'some phrase' AS p, user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
some phrase, patrick
some phrase, sandy
some phrase, spongebob
ROLLBACK

```

Обратите внимание, что в обоих случаях, при
использовании [`text()`](../core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
или [`literal_column()`](../core/sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column"),
мы пишем синтаксическое выражение SQL, а не литеральное значение. Поэтому мы должны включать все кавычки или
синтаксические элементы, необходимые для SQL, который мы хотим увидеть в рендеринге.

### Оператор WHERE {#tutorial-select-where-clause}

SQLAlchemy позволяет нам составлять выражения SQL, такие как `name = 'squidward'` или `user_id > 10`, используя
стандартные операторы Python в сочетании
с [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") и подобными объектами. Для
логических выражений большинство операторов Python, таких как `==`, `!=`, `<`, `>=` и т. д., генерируют новые объекты
SQL Expression, а не простые булевы значения `True`/`False`:

```

> > > print(user_table.c.name == "squidward")
> > > user_account.name = :name_1

> > > print(address_table.c.user_id > 10)
> > > address.user_id > :user_id_1

```

Мы можем использовать такие выражения для генерации оператора WHERE, передавая полученные объекты
методу [`Select.where()`](../core/selectable.html#Один
вызов [`Select.where()`](../core/selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")
также принимает несколько выражений с тем же эффектом:

```

> > > print(
> > > ... select(address_table.c.email_address).where(
> > > ... user_table.c.name == "squidward",
> > > ... address_table.c.user_id == user_table.c.id,
> > > ...     )
> > > ... )
> > > SELECT address.email_address
> > > FROM address, user_account
> > > WHERE user_account.name = :name_1 AND address.user_id = user_account.id

```

"AND" и "OR" соединения также доступны непосредственно с использованием
функций [`and_()`](../core/sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
и [`or_()`](../core/sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_"), проиллюстрированных
ниже в терминах сущностей ORM:

```

> > > from sqlalchemy import and_, or_
> > > print(
> > > ... select(Address.email_address).where(
> > > ... and_(
> > > ... or_(User.name == "squidward", User.name == "sandy"),
> > > ... Address.user_id == User.id,
> > > ...         )
> > > ...     )
> > > ... )
> > > SELECT address.email_address
> > > FROM address, user_account
> > > WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
> > > AND address.user_id = user_account.id

```

Для простых сравнений "равенства" с одной сущностью также существует популярный метод, известный
как [`Select.filter_by()`](../core/selectable.html#sqlalchemy.sql.expression.Select.filter_by "sqlalchemy.sql.expression.Select.filter_by"),
который принимает именованные аргументы, соответствующие ключам столбцов или именам атрибутов ORM. Он будет фильтровать
по самому левому FROM-выражению или последней присоединенной сущности:

```

> > > print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > WHERE user_account.name = :name_1 AND user_account.fullname = :fullname_1

```

Смотрите также

[Справочник операторов](../core/operators.html) - описания большинства функций операторов SQL в SQLAlchemy

### Явные выражения FROM и JOIN {#tutorial-select-join}

Как уже упоминалось ранее, выражение FROM обычно **выводится** на основе выражений, которые мы устанавливаем в столбцах,
а также других
элементов [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select").

Если мы устанавливаем один столбец из
определенной [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") в COLUMNS, то это
помещает эту [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") в выражение FROM:

```

> > > print(select(user_table.c.name))
> > > SELECT user_account.name
> > > FROM user_account

```

Если мы установим столбцы из двух таблиц, то получим выражение FROM, разделенное запятыми:

```

> > > print(
> > > ... select(user_table.c.name, address_table.c.email_address).join_from(
> > > ... user_table, address_table
> > > ...     )
> > > ... )
> > > SELECT user_account.name, address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id

```

Другой
метод - [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join"),
который указывает только правую сторону JOIN, левая сторона подразумевается:

```

> > > print(select(user_table.c.name, address_table.c.email_address).join(address_table))
> > > SELECT user_account.name, address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id

```

ON Clause подразумевается

При
использовании [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from")
или [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join")
мы можем
заметить, что ON clause соединения также подразумевается для нас в простых случаях внешнего ключа. Больше об этом в
следующем разделе.

У нас также есть возможность явно добавлять элементы в FROM clause, если он не
выводится так, как мы хотим из списка столбцов. Мы используем
метод [`Select.select_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")
для этого, как показано ниже,
где мы устанавливаем `user_table` в качестве первого элемента в FROM
clause
и [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join")
для установки `address_table` в качестве второго:

```

> > > print(select(address_table.c.email_address).select_from(user_table).join(address_table))
> > > SELECT address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id

```

Еще один пример, когда мы можем захотеть
использовать [`Select.select_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")-
это если наш список столбцов не содержит достаточно информации для FROM clause. Например, для SELECT из общего
SQL-выражения
`count(*)`, мы используем элемент SQLAlchemy, известный
как [`sqlalchemy.sql.expression.func`](../core/sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func"),
чтобы
произвести функцию SQL `count()`:

```

> > > from sqlalchemy import func
> > > print(select(func.count("*")).select_from(user_table))
> > > SELECT count(:count_2) AS count_1
> > > FROM user_account

```

Смотрите также

[Установка самого левого элемента FROM clause в join](../orm/queryguide/select.html#orm-queryguide-select-from) -
в [ORM Querying Guide](../orm/queryguide/index.html) -
содержит дополнительные примеры и заметки
относительно
взаимодействия [`Select.select_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")
и
[`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join")
.Если у левой и правой цели соединения нет такого ограничения, или есть несколько ограничений, мы должны указать
ON-клаузу напрямую.
Как [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join"),
так
и [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from")
принимают дополнительный аргумент для ON-клаузы, который указывается с использованием тех же механизмов SQL-выражений,
что и в разделе [WHERE-клауза](#tutorial-select-where-clause):

```

> > > print(
> > > ... select(address_table.c.email_address)
> > > ... .select_from(user_table)
> > > ... .join(address_table, user_table.c.id == address_table.c.user_id)
> > > ... )
> > > SELECT address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id

```

**Совет ORM** - есть еще один способ генерировать ON-клаузу при использовании сущностей ORM, которые используют
конструкцию [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
как это было настроено в предыдущем разделе
в [Объявление отображаемых классов](metadata.html#tutorial-declaring-mapped-classes). Это целая тема, которая подробно
рассматривается в
разделе [Использование отношений для соединения](orm_related_objects.html#tutorial-joining-relationships).

#### OUTER и FULL join

Методы [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join")
и [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from")
принимают ключевые
аргументы [`Select.join.isouter`](../core/selectable.html#sqlalchemy.sql.expression.Select.join.params.isouter "sqlalchemy.sql.expression.Select.join")
и [`Select.join.full`](../core/selectable.html#sqlalchemy.sql.expression.Select.join.params.full "sqlalchemy.sql.expression.Select.join"),
которые будут отображать LEFT OUTER JOIN и FULL OUTER JOIN соответственно:

```

> > > print(select(user_table).join(address_table, isouter=True))
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account LEFT OUTER JOIN address ON user_account.id = address.user_id
> > > print(select(user_table).join(address_table, full=True))
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id

```

Также есть
метод [`Select.outerjoin()`](../core/selectable.html#sqlalchemy.sql.expression.Select.outerjoin "sqlalchemy.sql.expression.Select.outerjoin"),
который эквивалентен использованию `.join(..., isouter=True)`.

Совет

SQL также имеет "RIGHT OUTER JOIN". SQLAlchemy не отображает это напрямую; вместо этого поменяйте порядок таблиц и
используйте "LEFT OUTER JOIN".

### ORDER BY, GROUP BY, HAVING {#tutorial-order-by-group-by-having}

SQL-оператор SELECT включает клаузу, называемую ORDER BY, которая используется для возврата выбранных строк в заданном
порядкеКлаузу ORDER BY составляют на основе конструкций SQL Expression, обычно основанных
на [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") или аналогичных объектах.
Метод [`Select.order_by()`](../core/selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")
принимает одно или несколько таких выражений в качестве позиционных аргументов:

```

> > > print(select(user_table).order_by(user_table.c.name))
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account ORDER BY user_account.name

```

Возможность сортировки по возрастанию / убыванию предоставляют
модификаторы [`ColumnElement.asc()`](../core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.asc "sqlalchemy.sql.expression.ColumnElement.asc")
и [`ColumnElement.desc()`](../core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.desc "sqlalchemy.sql.expression.ColumnElement.desc"),
которые присутствуют также и в связанных с ORM атрибутах:

```

> > > print(select(User).order_by(User.fullname.desc()))
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account ORDER BY user_account.fullname DESC

```

Этот оператор вернет строки, отсортированные по столбцу `user_account.fullname` в порядке убывания.

#### Агрегатные функции с GROUP BY / HAVING {#tutorial-group-by-w-aggregates}

В SQL агрегатные функции позволяют объединять выражения столбцов из нескольких строк в один результат. Примеры включают
подсчет, вычисление среднего значения, а также поиск максимального или минимального значения в наборе значений.

SQLAlchemy предоставляет SQL-функции в открытом виде, используя пространство
имен [`func`](../core/sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func"). Это специальный
объект-конструктор, который создает новые
экземпляры [`Function`](../core/functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function"),
когда ему передается имя конкретной SQL-функции, которое может иметь любое имя, а также ноль или более аргументов,
которые, как и во всех других случаях, являются конструкциями SQL Expression. Например, чтобы вывести функцию SQL
COUNT() для столбца `user_account.id`, мы вызываем имя `count()`:

```

> > > from sqlalchemy import func
> > > count_fn = func.count(user_table.c.id)
> > > print(count_fn)
> > > count(user_account.id)

```

SQL-функции описываются более подробно позже в этом учебнике в разделе [Работа с SQL-функциями](#tutorial-functions).

При использовании агрегатных функций в SQL клауза GROUP BY является необходимой, поскольку она позволяет разбивать
строки на группы, в которых агрегатные функции будут применяться к каждой группе индив```

```
>>> with engine.connect() как conn:
...     result = conn.execute(
...         select(User.name, func.count(Address.id).label("count"))
...         .join(Address)
...         .group_by(User.name)
...         .having(func.count(Address.id) > 1)
...     )
...     print(результат.all())
BEGIN (implicit)
SELECT user_account.name, count(address.id) AS count
FROM user_account JOIN address ON user_account.id = address.user_id GROUP BY user_account.name
HAVING count(address.id) > ?
[...] (1,)
[('sandy', 2)]
ROLLBACK
```

#### Сортировка или группировка по метке {#tutorial-order-by-label}

Важная техника, в частности на некоторых базах данных, - это возможность
УПОРЯДОЧИТЬ ПО или ГРУППИРОВАТЬ ПО выражению, которое уже указано в столбцах
клаузы, без повторного указания выражения в клаузе ORDER BY или GROUP BY
и вместо этого использовать имя столбца или помеченное имя из клаузы COLUMNS.
Эта форма доступна, передавая строковый текст имени в
[`Select.order_by()`](../core/selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")
или [`Select.group_by()`](../core/selectable.html#sqlalchemy.sql.expression.Select.group_by "sqlalchemy.sql.expression.Select.group_by")
метод. Текст
передается **не напрямую**; вместо этого имя, данное выражению
в клаузе столбцов и отображаемое как имя этого выражения в контексте, поднимается
ошибка, если соответствие не найдено. Унарные модификаторы
[`asc()`](../core/sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
и [`desc()`](../core/sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc") также могут
использоваться в этой форме:

```
>>> from sqlalchemy import func, desc
>>> stmt = (
...     выбрать(Address.user_id, func.count(Address.id).label("num_addresses"))
...     .group_by("user_id")
...     .order_by("user_id", desc("num_addresses"))
... )
>>> print(stmt)
SELECT address.user_id, count(address.id) AS num_addresses
FROM address GROUP BY address.user_id ORDER BY address.user_id, num_addresses DESC

```

### Использование псевдонимов {#tutorial-using-aliases}

Теперь, когда мы выбираем из нескольких таблиц и используем соединения, мы быстро
сталкиваемся с тем, что нам нужно ссылаться на одну и ту же таблицу несколько раз
в клаузе FROM выражения. Мы делаем это с помощью SQL **псевдонимов**,
которые являются синтаксисом, который предоставляет альтернативное имя таблице или подзапросу
от которого можно ссылаться на него в выражении.

В SQLAlchemy Expression Language эти "имена" представлены
объектами [`FromClause`](../core/selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
известными как
конструкция [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias").
Конструкция [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
создается в Core с использованием
метода [`FromClause.alias()`](../core/selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias").
Конструкция [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias") так же,
как и конструкция `Table`, имеет пространство
имен [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") объектов внутри
коллекции `Alias.c`. Например, приведенный ниже оператор SELECT возвращает все уникальные пары имен пользователей:

```
> > > user_alias_1 = user_table.alias()
> > > user_alias_2 = user_table.alias()
> > > print(
> > > ... select(user_alias_1.c.name, user_alias_2.c.name).join_from(
> > > ... user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
> > > ...     )
> > > ... )
> > > SELECT user_account_1.name, user_account_2.name AS name_1
> > > FROM user_account AS user_account_1
> > > JOIN user_account AS user_account_2 ON user_account_1.id > user_account_2.id

```

#### Псевдонимы ORM-сущностей {#tutorial-orm-entity-aliases}

ORM-эквивалент
метода [`FromClause.alias()`](../core/selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias") -
функция
ORM [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased"), которая может быть
применена к сущности
такой как `User` и `Address`. Это создает
объект [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
внутри, который используется с оригинальным
отображенным [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") объектом,
с сохранением функциональности ORM. SELECT ниже выбирает из
сущности `User` все объекты, которые включают два конкретных адреса электронной почты:

```

> > > from sqlalchemy.orm import aliased
> > > address_alias_1 = aliased(Address)
> > > address_alias_2 = aliased(Address)
> > > print(
> > > ... select(User)
> > > ... .join_from(User, address_alias_1)
> > > ... .where(address_alias_1.email_address == "patrick@aol.com")
> > > ... .join_from(User, address_alias_2)
> > > ... .where(address_alias_2.email_address == "patrick@gmail.com")
> > > ... )
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > JOIN address AS address_1 ON user_account.id = address_1.user_id
> > > JOIN address AS address_2 ON user_account.id = address_2.user_id
> > > WHERE address_1.email_address = :email_address_1
> > > AND address_2.email_address = :email_address_2

```

Совет

Как упоминалось в разделе [Установка ON Clause](#tutorial-select-join-onclause), ORM предоставляет
еще один способ объединения с использованием
конструкции [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship").
Приведенный выше пример с псевдонимами демонстрируется с
использованием [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
в
разделе [Использование Relationship для объединения между псевдонимами целей](../orm/queryguide/select.html#tutorial-joining-relationships-aliased).

### Подзапросы и CTE {#tutorial-subqueries-ctes}

Подзапрос в SQL - это оператор SELECT, который отображается внутри скобок и
размещается в контексте включающего оператора, обычно оператора SELECT,
но не обязательно.

В этом разделе будет рассмотрен так называемый "нескалярный" SQLAlchemy использует
объект [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery") для
представления подзапроса и
объект [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE") для представления
CTE, обычно получаемых из
методов [`Select.subquery()`](../core/selectable.html#sqlalchemy.sql.expression.Select.subquery "sqlalchemy.sql.expression.Select.subquery")
и [`Select.cte()`](../core/selectable.html#sqlalchemy.sql.expression.Select.cte "sqlalchemy.sql.expression.Select.cte")
соответственно. Любой из этих объектов может использоваться в качестве элемента FROM внутри более крупной
конструкции [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").

Мы можем
создать [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery"),
который будет выбирать агрегатное количество строк из таблицы `address` (функции агрегирования и GROUP BY были
рассмотрены ранее в разделе [Функции агрегирования с GROUP BY / HAVING](#tutorial-group-by-w-aggregates)):

```

>>> subq = (
select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
.group_by(address_table.c.user_id)
.subquery()


```

Преобразование подзапроса в строку без вложения его в
другой [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") или
другой оператор дает простой оператор SELECT без каких-либо вложенных скобок:

```

> > > print(subq)
> > > SELECT count(address.id) AS count, address.user_id
> > > FROM address GROUP BY address.user_id

```

Объект [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery")
ведет себя как любой другой объект FROM, такой
как [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), в частности, он включает
пространство имен `Subquery.c` столбцов, которые он выбирает. Мы можем использовать это пространство имен для ссылки как
на столбец `user_id`, так и на нашу настраиваемую метку выражения `count`:

```

> > > print(select(subq.c.user_id, subq.c.count))
> > > SELECT anon_1.user_id, anon_1.count
> > > FROM (SELECT count(address.id) AS count, address.user_id AS user_id
> > > FROM address GROUP BY address.user_id) AS anon_1

```

С выборкой строк, содержащихся в объекте `subq`, мы можем применить объект к более
крупному [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
который объединит данные с таблицей `user_account`:

```

> > > stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
> > > ... user_table, subq
> > > ... )

> > > print(stmt)
> > > SELECT user_account.name, user_account.fullname, anon_1.count
> > > FROM user_account JOIN (SELECT count(address.id) AS count, address.user_id AS user_id
> > > FROM address GROUP BY address.user
```

Для соединения таблиц `user_account` и `address` мы использовали
метод [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from").
Как было показано ранее, условие ON для этого соединения было снова **выведено** на основе ограничений внешнего ключа.
Несмотря на то, что у SQL-подзапроса самого по себе нет ограничений, SQLAlchemy может использовать ограничения,
представленные на столбцах, определив, что столбец `subq.c.user_id` **производный** от
столбца `address_table.c.user_id`, который выражает обратную связь с столбцом `user_table.c.id`, который затем
используется для создания ON-условия.

#### Общие таблицы выражений (CTE)

Использование конструкции [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")
в SQLAlchemy практически идентично использованию
конструкции [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery").
Изменив вызов
метода [`Select.subquery()`](../core/selectable.html#sqlalchemy.sql.expression.Select.subquery "sqlalchemy.sql.expression.Select.subquery")
на
использование [`Select.cte()`](../core/selectable.html#sqlalchemy.sql.expression.Select.cte "sqlalchemy.sql.expression.Select.cte"),
мы можем использовать полученный объект как элемент FROM таким же образом, но SQL, сгенерированный в этом случае, имеет
совершенно другой синтаксис общих таблиц выражений:

```

> > > subq = (
> > > ... select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
> > > ... .group_by(address_table.c.user_id)
> > > ... .cte()
> > > ... )

> > > stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
> > > ... user_table, subq
> > > ... )

> > > print(stmt)
> > > WITH anon_1 AS
(SELECT count(address.id) AS count, address.user_id AS user_id
> > > FROM address GROUP BY address.user_id)
> > > SELECT user_account.name, user_account.fullname, anon_1.count
> > > FROM user_account JOIN anon_1 ON user_account.id = anon_1.user_id

```

Конструкция [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE") также имеет
возможность использоваться в «рекурсивном» стиле и может в более сложных случаях составляться из RETURNING-запроса
операторов INSERT, UPDATE или DELETE. В документации
к [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE") содержатся подробности
об этих дополнительных шаблонах.

В обоих случаях подзапрос и CTE были названы на уровне SQL с использованием «анонимного» имени. В коде Python нам не
нужно вообще указывать эти имена. Идентичность объекта [`Subquery`](
../core/selectable.html#sqlalchemy.sql.expression.Subquery "
sqlalchemy.sql.expression.Subquery[`Select.cte()`](../core/selectable.html#sqlalchemy.sql.expression.Select.cte "sqlalchemy.sql.expression.Select.cte") -
примеры использования CTE, включая то, как использовать RECURSIVE, а также CTE, ориентированные на DML.

#### ORM Entity Subqueries/CTEs {#tutorial-subqueries-orm-aliased}

В ORM конструкция [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased") может
использоваться для связи ORM-сущности, такой как наш класс `User` или `Address`, с любым
концептом [`FromClause`](../core/selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
который представляет источник строк. Предыдущий раздел [ORM Entity Aliases](#tutorial-orm-entity-aliases) иллюстрирует
использование [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased") для связи
отображенного класса
с [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias") его
отображенной [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"). Здесь мы
иллюстрируем [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased"), делающий то же
самое
против [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery"), а
также [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE"), сгенерированный
против
конструкции [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
который в конечном итоге происходит от той же
отображенной [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

Ниже приведен пример
применения [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased") к
конструкции [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery"),
чтобы извлечь ORM-сущности из его строк. Результат показывает серию объектов `User` и `Address`, где данные для каждого
объекта `Address` в конечном итоге происходят из подзапроса против таблицы `address`, а не непосредственно из этой
таблицы:
```
> > > subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
> > > address_subq = aliased(Address, subq)
> > > stmt = (
> > > ... select(User, address_subq)
> > > ... .join_from(User, address_subq)
> > > ... .order_by(User.id, address_subq.id)
> > > ... )
> > > with Session(engine) as session:
> > > ... for user, address in session.execute(stmt):
> > > ... print(f"{user} {address}")
> > > BEGIN (implicit)
> > > SELECT user_account.id, user_account.name, user_account.fullname,
> > > anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
> > > FROM user_account JOIN
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
> > > FROM address
> > > WHERE address.email_address NOT LIKE ?) AS anon_1 ON user_account.id = anon_1.user_id
> > > ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='spongebob@sqlalchemy.org')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='sandy@sqlalchemy.org')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='sandy@squirrelpower.org')
> > > ROLLBACK

```

Далее приводится еще один пример, который полностью аналогичен предыдущему, за исключением того, что он использует
конструкцию [`CTE`](../core/selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE"):

```

> > > cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
> > > address_cte = aliased(Address, cte_obj)
> > > stmt = (
> > > ... select(User, address_cte)
> > > ... .join_from(User, address_cte)
> > > ... .order_by(User.id, address_cte.id)
> > > ... )
> > > with Session(engine) as session:
> > > ... for user, address in session.execute(stmt):
> > > ... print(f"{user} {address}")
> > > BEGIN (implicit)
> > > WITH anon_1 AS
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
> > > FROM address
> > > WHERE address.email_address NOT LIKE ?)
> > > SELECT user_account.id, user_account.name, user_account.fullname,
> > > anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
> > > FROM user_account
> > > JOIN anon_1 ON user_account.id = anon_1.user_id
> > > ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='spongebob@sqlalchemy.org')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='sandy@sqlalchemy.org')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='sandy@squirrelpower.org')
> > > ROLLBACK

```

См. также

[Выбор сущностей из подзапросов](../orm/queryguide/select.html#orm-queryguide-subqueries) -
в [Руководстве по запросам ORM](../orm/queryguide/index.html)

### Скалярные и коррелированные подзапросы {#tutorial-scalar-subquery}

Скалярный подзапрос - это подзапрос, который возвращает ровно ноль или одну строку и ровно один столбец. Затем подзапрос
используется в COLUMNS или WHERE-клаузе включающего SELECT-запроса и отличается от обычного подзапроса тем, что не
используется в FROM-клаузе. Коррелированный подзапрос - это скалярный подзапрос, который ссылается на таблицу во
включающем SELECT-запросе.

SQLAlchemy представляет скалярный подзапрос с помощью конструкции ScalarSelect, которая является частью иерархии
выражений ColumnElement, в отличие от обычного подзапроса, который представлен конструкцией Subquery, которая находится
в иерархии FromClause.

Скалярные подзапросы часто, но не обязательно, используются с агрегатными функциями, ранее представленными в разделе "
Агрегатные функции с GROUP BY / HAVING". Скалярный подзапрос указывается явно с помощью метода Select.scalar_subquery(),
как показано ниже. Его строковая форма по умолчанию при преобразовании в строку представляет собой обычный
SELECT-запрос, который выбирает из двух таблиц:

```

> > > subq = (
> > > ... select(func.count(address_table.c.id))
> > > ... .where(user_table.c.id == address_table.c.user_id)
> > > ... .scalar_subquery()
> > > ... )
> > > print(subq)
(SELECT count(address.id) AS count_1
> > > FROM address, user_account
> > > WHERE user_account.id = address.user_id)

```

Теперь объект subq относится к иерархии SQL-выражений ColumnElement, и его можно использовать как любое другое выражение
столбца:

```

> > > print(subq == 5)
(SELECT count(address.id) AS count_1
> > > FROM address, user_account
> > > WHERE user_account.id = address.user_id) = :param_1

```

Хотя скалярный подзапрос по умолчанию включает в свой FROM-клауз таблицы user_account и address, когда он встраивается
во включающую конструкцию select(), которая работает с таблицей user_account, таблица user_account автоматически
становится скоррелированной, что означает, что она не отображается в FROM-клаузе подзапроса:

```

> > > stmt = select(user_table.c.name, subq.label("address_count"))
> > > print(stmt)
> > > SELECT user_account.name, (SELECT count(address.id) AS count_1
> > > FROM address
> > > WHERE user_account.id = address.user_id) AS address_count
> > > FROM user_account

```

Простые коррелированные подзапросы обычно делают то, что требуется. Однако, если корреляция неоднозначна, SQLAlchemy
сообщит нам, что требуется больше ясности:
```
> > > stmt = (
> > > ... select(
> > > ... user_table.c.name,
> > > ... address_table.c.email_address,
> > > ... subq.label("address_count"),
> > > ...     )
> > > ... .join_from(user_table, address_table)
> > > ... .order_by(user_table.c.id, address_table.c.id)
> > > ... )
> > > print(stmt)
> > > Traceback (most recent call last):
> > > ...
> > > InvalidRequestError: Выборка '<... Select object at ...>' не вернула
> > > ни одного из FROM выражений из-за автокорреляции; укажите correlate(<tables>),
> > > чтобы управлять корреляцией вручную.

```

Чтобы указать, что `user_table` - это та таблица, которую мы ищем для корреляции, мы указываем это, используя
методы [`ScalarSelect.correlate()`](../core/selectable.html#sqlalchemy.sql.expression.ScalarSelect.correlate "sqlalchemy.sql.expression.ScalarSelect.correlate")
или [`ScalarSelect.correlate_except()`](../core/selectable.html#sqlalchemy.sql.expression.ScalarSelect.correlate_except "sqlalchemy.sql.expression.ScalarSelect.correlate_except"):

```

> > > subq = (
> > > ... select(func.count(address_table.c.id))
> > > ... .where(user_table.c.id == address_table.c.user_id)
> > > ... .scalar_subquery()
> > > ... .correlate(user_table)
> > > ... )

```

Затем оператор может возвращать данные для этого столбца, как и для любого другого:

```

> > > with engine.connect() as conn:
> > > ... result = conn.execute(
> > > ... select(
> > > ... user_table.c.name,
> > > ... address_table.c.email_address,
> > > ... subq.label("address_count"),
> > > ...         )
> > > ... .join_from(user_table, address_table)
> > > ... .order_by(user_table.c.id, address_table.c.id)
> > > ...     )
> > > ... print(result.all())
> > > BEGIN (implicit)
> > > SELECT user_account.name, address.email_address, (SELECT count(address.id) AS count_1
> > > FROM address
> > > WHERE user_account.id = address.user_id) AS address_count
> > > FROM user_account JOIN address ON user_account.id = address.user_id ORDER BY user_account.id, address.id
[...] ()
[('spongebob', 'spongebob@sqlalchemy.org', 1), ('sandy', 'sandy@sqlalchemy.org', 2),
('sandy', 'sandy@squirrelpower.org', 2)]
> > > ROLLBACK

```

#### Корреляция LATERAL {#tutorial-lateral-correlation}

Корреляция LATERAL - это особый подтип корреляции SQL, который
позволяет выбираемому элементу ссылаться на другой выбираемый элемент в
одном FROM выражении. Это крайне специальный случай использования, который,
хотя и является частью стандарта SQL, известен только в последних
версиях PostgreSQL.

Обычно, если оператор SELECT ссылается на
`table1 JOIN (SELECT ...) AS subquery` в своем выражении FROM, подзапрос
справа не может ссылаться на выражение "table1" слева;
корреляция может ссылаться только на таблицу, которая является частью другого SELECT, который
полностью включает этот SELECT. Ключевое слово LATERAL позволяет нам изменить эту
логику и позволяет корреляцию с правой стороны JOIN.SQLAlchemy поддерживает эту функцию с помощью
метода [`Select.lateral()`](../core/selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral"),
который создает объект, известный
как [`Lateral`](../core/selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral"). [`Lateral`](../core/selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")
находится в той же семье, что
и [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery")
и [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias"), но также
включает корреляционное поведение, когда конструкция добавляется в FROM-клаузу охватывающего SELECT. В следующем примере
показан SQL-запрос, который использует LATERAL, выбирая данные "учетной записи пользователя / количество адресов
электронной почты", как было обсуждено в предыдущем разделе:

```

> > > subq = (
> > > ... select(
> > > ... func.count(address_table.c.id).label("address_count"),
> > > ... address_table.c.email_address,
> > > ... address_table.c.user_id,
> > > ...     )
> > > ... .where(user_table.c.id == address_table.c.user_id)
> > > ... .lateral()
> > > ... )
> > > stmt = (
> > > ... select(user_table.c.name, subq.c.address_count, subq.c.email_address)
> > > ... .join_from(user_table, subq)
> > > ... .order_by(user_table.c.id, subq.c.email_address)
> > > ... )
> > > print(stmt)
> > > SELECT user_account.name, anon_1.address_count, anon_1.email_address
> > > FROM user_account
> > > JOIN LATERAL (SELECT count(address.id) AS address_count,
> > > address.email_address AS email_address, address.user_id AS user_id
> > > FROM address
> > > WHERE user_account.id = address.user_id) AS anon_1
> > > ON user_account.id = anon_1.user_id
> > > ORDER BY user_account.id, anon_1.email_address

```

Выше, правая сторона JOIN является подзапросом, который коррелирует с таблицей `user_account`, которая находится на
левой стороне соединения.

При
использовании [`Select.lateral()`](../core/selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")
поведение
методов [`Select.correlate()`](../core/selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
и [`Select.correlate_except()`](../core/selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")
также применяется к
конструкции [`Lateral`](../core/selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral").

См. также

[`Lateral`](../core/selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")

[`Select.lateral()`](../core/selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")

### UNION, UNION ALL и другие операции наборов {#tutorial-union}

В SQL операторы SELECT могут быть объединены с помощью операции UNION или UNION ALL, которая производит набор всех
строк, производимых одним или несколькими операторами
вместе.Конструкция [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
в SQLAlchemy поддерживает композиции такого рода с помощью функций, таких
как [`union()`](../core/selectable.html#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union"), [`intersect()`](../core/selectable.html#sqlalchemy.sql.expression.intersect "sqlalchemy.sql.expression.intersect")
и [`except_()`](../core/selectable.html#sqlalchemy.sql.expression.except_ "sqlalchemy.sql.expression.except_"), а также
их аналогов с "
all" - [`union_all()`](../core/selectable.html#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all"), [`intersect_all()`](../core/selectable.html#sqlalchemy.sql.expression.intersect_all "sqlalchemy.sql.expression.intersect_all")
и [`except_all()`](../core/selectable.html#sqlalchemy.sql.expression.except_all "sqlalchemy.sql.expression.except_all").
Эти функции все принимают произвольное количество под-выборок, которые обычно являются
конструкциями [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
но могут также быть существующей композицией.

Конструкция, созданная этими функциями,
является [`CompoundSelect`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect"),
которая используется так же, как и
конструкция [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"), за
исключением того, что у нее меньше
методов. [`CompoundSelect`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect"),
созданный, например, с
помощью [`union_all()`](../core/selectable.html#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all"),
может быть вызван непосредственно с
помощью [`Connection.execute()`](../core/connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"):

```

> > > from sqlalchemy import union_all
> > > stmt1 = select(user_table).where(user_table.c.name == "sandy")
> > > stmt2 = select(user_table).where(user_table.c.name == "spongebob")
> > > u = union_all(stmt1, stmt2)
> > > with engine.connect() as conn:
> > > ... result = conn.execute(u)
> > > ... print(result.all())
> > > BEGIN (implicit)
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > WHERE user_account.name = ?
> > > UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
[(2, 'sandy', 'Sandy Cheeks'), (1, 'spongebob', 'Spongebob Squarepants')]
> > > ROLLBACK

```

Чтобы
использовать [`CompoundSelect`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")
в качестве подзапроса, как
и [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"), он
предоставляет
метод [`SelectBase.subquery()`](../core/selectable.html#sqlalchemy.sql.expression.SelectBase.subquery "sqlalchemy.sql.expression.SelectBase.subquery"),
который создаст
объект [`Subquery`](../core/selectable.html#sqlalchemy.sql.expression.Subquery "sqlalchemy.sql.expression.Subquery") с
коллекцией [`FromClause#### Выбор ORM-сущностей из объединений {#tutorial-orm-union}

Предыдущие примеры показали, как создать объединение двух
объектов [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), чтобы затем вернуть строки
из базы данных. Если мы хотим использовать объединение или другую операцию над множествами для выбора строк, которые мы
затем получаем в виде ORM-объектов, можно использовать два подхода. В обоих случаях мы сначала создаем
объект [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
или [`CompoundSelect`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect"),
который представляет выражение SELECT / UNION / и т.д., которое мы хотим выполнить; это выражение должно быть составлено
против целевых ORM-сущностей или их базовых
отображенных [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") объектов:

```

> > > stmt1 = select(User).where(User.name == "sandy")
> > > stmt2 = select(User).where(User.name == "spongebob")
> > > u = union_all(stmt1, stmt2)

```

Для простого SELECT с UNION, который еще не вложен в подзапрос, это можно часто использовать в контексте получения
объектов ORM, используя
метод [`Select.from_statement()`](../core/selectable.html#sqlalchemy.sql.expression.Select.from_statement "sqlalchemy.sql.expression.Select.from_statement").
При этом подходе оператор UNION представляет всю выборку; после
использования [`Select.from_statement()`](../core/selectable.html#sqlalchemy.sql.expression.Select.from_statement "sqlalchemy.sql.expression.Select.from_statement")
нельзя добавлять дополнительные критерии:

```

> > > orm_stmt = select(User).from_statement(u)
> > > with Session(engine) as session:
> > > ... for obj in session.execute(orm_stmt).scalars():
> > > ... print(obj)
> > > BEGIN (implicit)
> > > SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > WHERE user_account.name = ? UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
> > > FROM user_account
> > > WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks')
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants')
> > > ROLLBACK

```
Чтобы использовать UNION или другую связанную сущность в более гибком
способе, конструкцию [`CompoundSelect`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect") можно
организовать в подзапрос, используя метод [`CompoundSelect.subquery()`](../core/selectable.html#sqlalchemy.sql.expression.CompoundSelect.subquery "sqlalchemy.sql.expression.CompoundSelect.subquery"), который
затем связывается с ORM-объектами с помощью функции [`aliased()`](../orm/queryguide/api.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased"). Это работает
так же, как и в [ORM Entity Subqueries/CTEs](#tutorial-subqueries-orm-aliased), чтобы сначала
создать вспомогательное «отображение» нашей желаемой сущности для подзапроса, затем
выбирая из этой новой сущности, как если бы это был любой другой отображенный класс.
В приведенном ниже примере мы можем добавить дополнительные критерии, такие как ORDER BY
вне самого UNION, так как мы можем фильтровать или сортировать по экспортированным столбцам
подзапроса:


```

> > > user_alias = aliased(User, u.subquery())
> > > orm_stmt = select(user_alias).order_by(user_alias.id)
> > > with Session(engine) as session:
> > > ... for obj in session.execute(orm_stmt).scalars():
> > > ... print(obj)
> > > BEGIN (implicit)
> > > SELECT anon_1.id, anon_1.name, anon_1.fullname
> > > FROM (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
> > > FROM user_account
> > > WHERE user_account.name = ? UNION ALL SELECT user_account.id AS id, user_account.name AS name,
> > > user_account.fullname AS
> > > fullname
> > > FROM user_account
> > > WHERE user_account.name = ?) AS anon_1 ORDER BY anon_1.id
[generated in ...] ('sandy', 'spongebob')
> > > User(id=1, name='spongebob', fullname='Spongebob Squarepants')
> > > User(id=2, name='sandy', fullname='Sandy Cheeks')
> > > ROLLBACK

```


Смотрите также


[Выбор сущностей из UNION и других операций над множествами](../orm/queryguide/select.html#orm-queryguide-unions) - в [Руководстве по запросам ORM](../orm/queryguide/index.html)


### EXISTS подзапросы {#tutorial-exists} 


Ключевое слово SQL EXISTS - это оператор, который используется с [скалярными подзапросами](#tutorial-scalar-subquery) для возврата логического значения true или false в зависимости от того,
вернет ли оператор SELECT строку. SQLAlchemy включает вариант объекта [`ScalarSelect`](../core/selectable.html#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect") под названием [`Exists`](../core/selectable.html#sqlalchemy.sql.expression.Exists "sqlalchemy.sql.expression.Exists"), который
сгенерирует подзапрос EXISTS и наиболее удобно сгенерируется с помощью метода [`SelectBase.exists()`](../core/selectable.html#sqlalchemy.sql.expression.SelectBase.exists "sqlalchemy.sql.expression.SelectBase.exists
```
>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .having(func.count(address_table.c.id) > 1)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE EXISTS (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id GROUP BY address.user_id
HAVING count(address.id) > ?)
[...] (1,)
[('sandy',)]
ROLLBACK


```

Конструкция EXISTS чаще всего используется в отрицательной форме, например NOT EXISTS, так как она обеспечивает
SQL-эффективную форму поиска строк, для которых связанная таблица не имеет строк. Ниже мы выбираем имена пользователей,
у которых нет адресов электронной почты; обратите внимание на оператор отрицания (~), используемый внутри второго WHERE:

```
>>> subq = (
...     select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(~subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE NOT (EXISTS (SELECT address.id
FROM address
WHERE user_account.id = address.user_id))
[...] ()
[('patrick',)]
ROLLBACK


```

### Работа с SQL-функциями {#tutorial-functions}

Как было введено ранее в этом разделе в
[Функции агрегирования с GROUP BY / HAVING](#tutorial-group-by-w-aggregates),
объект [`func`](../core/sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func") служит как
фабрика для создания новых
объектов [`Function`](../core/functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function"),
которые при использовании
в конструкции [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
производят отображение SQL-функции,
которое обычно состоит из имени, некоторых скобок (хотя не всегда) и
возможно некоторых аргументов. Примеры типичных SQL-функций включают:

* функция `count()`, агрегатная функция, которая подсчитывает, сколько
  строк возвращается:

```
>>> print(select(func.count()).select_from(user_table))
SELECT count(*) AS count_1
FROM user_account


```

* функция `lower()`, строковая функция, которая преобразует строку в нижний
  регистр:

```
>>> print(select(func.lower("A String With Much UPPERCASE")))
SELECT lower(:lower_2) AS lower_1


```

* функция `now()`, которая обеспечивает текущую дату и время; так как это
  общая функция, SQLAlchemy знает, как отображать это по-разному для каждой
  базы данных, в случае SQLite используется функция CURRENT\_TIM```

```
>>> print(select(func.some_crazy_function(user_table.c.name, 17)))
SELECT some_crazy_function(user_account.name, :some_crazy_function_2) AS some_crazy_function_1
FROM user_account
```

В то же время, относительно небольшой набор чрезвычайно распространенных SQL-функций, таких
как [`count`](../core/functions.html#sqlalchemy.sql.functions.count "sqlalchemy.sql.functions.count"), [`now`](../core/functions.html#sqlalchemy.sql.functions.now "sqlalchemy.sql.functions.now"), [`max`](../core/functions.html#sqlalchemy.sql.functions.max "sqlalchemy.sql.functions.max"),
[`concat`](../core/functions.html#sqlalchemy.sql.functions.concat "sqlalchemy.sql.functions.concat") включают в себя
предварительно упакованные версии, которые обеспечивают правильную информацию о типах, а также генерацию SQL,
специфичную для бэкэнда в некоторых случаях. Приведенный ниже пример контрастирует генерацию SQL, которая происходит для
диалекта PostgreSQL по сравнению с диалектом Oracle для
функции [`now`](../core/functions.html#sqlalchemy.sql.functions.now "sqlalchemy.sql.functions.now"):

```
>>> from sqlalchemy.dialects import postgresql
>>> print(select(func.now()).compile(dialect=postgresql.dialect()))
SELECT now() AS now_1
>>> from sqlalchemy.dialects import oracle
>>> print(select(func.now()).compile(dialect=oracle.dialect()))
SELECT CURRENT_TIMESTAMP AS now_1 FROM DUAL
```

#### Функции имеют типы возврата

Поскольку функции являются выражениями столбцов, они также имеют
SQL [типы данных](../core/types.html), которые описывают тип данных
сгенерированного SQL-выражения. Мы называем эти типы здесь "SQL-типами возврата",
в отношении типа SQL-значения, возвращаемого функцией
в контексте SQL-выражения на стороне базы данных,
в отличие от "типа возврата" функции Python.

SQL-тип возврата любой SQL-функции может быть получен, обычно для
отладки, обращаясь к атрибуту `Function.type`:

```
>>> func.now().type
DateTime()

```

Эти SQL-типы возврата значимы при использовании выражения функции в контексте более крупного выражения; то есть,
математические операторы будут работать лучше, когда тип выражения будет
что-то вроде [`Integer`](../core/type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")
или [`Numeric`](../core/type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric"), JSON
доступоразрешающие устройства, чтобы работать, должны использовать тип, такой как
[`JSON`](../core/type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON"). Некоторые классы функций возвращают
целые строки
вместо значений столбцов, где есть
```
> > > from sqlalchemy import JSON
> > > function_expr = func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)

```

Создавая нашу функцию JSON с типом данных [`JSON`](../core/type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON"), объект выражения SQL принимает свойства, связанные с JSON, такие как доступ к элементам:


```

> > > stmt = select(function_expr["def"])
> > > print(stmt)
> > > SELECT json_object(:json_object_1)[:json_object_2] AS anon_1

```

#### Встроенные функции имеют заранее настроенные типы возврата 


Для общих агрегатных функций, таких как [`count`](../core/functions.html#sqlalchemy.sql.functions.count "sqlalchemy.sql.functions.count"),
[`max`](../core/functions.html#sqlalchemy.sql.functions.max "sqlalchemy.sql.functions.max"), [`min`](../core/functions.html#sqlalchemy.sql.functions.min "sqlalchemy.sql.functions.min"), а также очень небольшого количества
функций даты, таких как [`now`](../core/functions.html#sqlalchemy.sql.functions.now "sqlalchemy.sql.functions.now") и функций строк, таких как
[`concat`](../core/functions.html#sqlalchemy.sql.functions.concat "sqlalchemy.sql.functions.concat"), SQL-тип возврата настраивается соответствующим образом,
иногда на основе использования. Функция [`max`](../core/functions.html#sqlalchemy.sql.functions.max "sqlalchemy.sql.functions.max") и аналогичные
функции фильтрации агрегатов настраивают SQL-тип возврата на основе
заданного аргумента:


```

> > > m1 = func.max(Column("some_int", Integer))
> > > m1.type
> > > Integer()

> > > m2 = func.max(Column("some_str", String))
> > > m2.type
> > > String()

```

Функции даты и времени обычно соответствуют SQL-выражениям, описанным в
[`DateTime`](../core/type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime"), [`Date`](../core/type_basics.html#sqlalchemy.types.Date "sqlalchemy.types.Date") или [`Time`](../core/type_basics.html#sqlalchemy.types.Time "sqlalchemy.types.Time"):


```

> > > func.now().type
> > > DateTime()
> > > func.current_date().type
> > > Date()

```

Известно, что функция строк, такая как [`concat`](../core/functions.html#sqlalchemy.sql.functions.concat "sqlalchemy.sql.functions.concat"),
знает, что SQL-выражение будет иметь тип [`String`](../core/type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String"):


```

> > > func.concat("x", "y").type
> > > String()

```

Однако для подавляющего большинства SQL-функций SQLAlchemy не имеет их
явно присутствующих в своем очень небольшом списке известных функций. Например,
хотя обычно нет проблем с использованием SQL-функций `func.lower()`
и `func.upper()` для преобразования регистра строк, SQLAlchemy не
фактически знает об этих функциях, поэтому у них нет SQL-типа возврата:


```

> > > >>> func.upper("lowercase").type
NullType()
```
1. Функция еще не является встроенной функцией SQLAlchemy; это можно увидеть, создав функцию и
наблюдая за атрибутом `Function.type`, который выглядит следующим образом:

    ```
    >>> func.count().type
    Integer()
    
    ```
    
    в отличие от:
    
    ```
    >>> func.json_object('{"a", "b"}').type
    NullType()
    
    ```

2. Необходима поддержка выражений, осознающих функции; это обычно относится к специальным операторам, связанным с типами
   данных, такими как [`JSON`](../core/type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")
   или [`ARRAY`](../core/type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")
3. Необходима обработка результирующего значения, которая может включать типы, такие
   как `DateTime`, [`Boolean`](../core/type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean"), [`Enum`](../core/type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum"),
   или опять же специальные типы данных, такие
   как [`JSON`](../core/type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON"), [`ARRAY`](../core/type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY").

#### Расширенные техники работы с SQL-функциями

В следующих подразделах иллюстрируются более продвинутые вещи, которые можно сделать с SQL-функциями. Хотя эти техники
менее распространены и более продвинуты, чем базовое использование SQL-функций, они тем не менее чрезвычайно популярны,
в основном благодаря упору PostgreSQL на более сложные формы функций, включая формы со значениями таблиц и столбцов,
которые популярны с данными JSON.

##### Использование оконных функций {#tutorial-window-functions}

Оконная функция - это специальное использование агрегатной SQL-функции, которая вычисляет агрегатное значение по
строкам, возвращаемым в группе, по мере обработки отдельных результатов строк. В то время как функция, такая
как `MAX()`, даст вам наивысшее значение столбца в наборе строк, использование той же функции в качестве "оконной
функции" даст вам наивысшее значение для каждой строки, *на момент этой строки*.

В SQL оконные функции позволяют указать строки, над которыми должна быть применена функция, значение "раздела", которое
учитывает окно в разных подмножествах строк, и выражение "order by", которое важно указывает порядок, в котором строки
должны быть применены к агрегатной функции.

В SQLAlchemy все SQL-функции, созданные пространством имен [`func`](
../core/sqlelement.html#sqlalchemy.sql.expression.func "
```
> > > stmt = (
> > > ... select(
> > > ... func.row_number().over(partition_by=user_table.c.name),
> > > ... user_table.c.name,
> > > ... address_table.c.email_address,
> > > ...     )
> > > ... .select_from(user_table)
> > > ... .join(address_table)
> > > ... )
> > > with engine.connect() as conn:  
> > > ... result = conn.execute(stmt)
> > > ... print(result.all())
> > > BEGIN (implicit)
> > > SELECT row_number() OVER (PARTITION BY user_account.name) AS anon_1,
> > > user_account.name, address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id
[...] ()
[(1, 'sandy', 'sandy@sqlalchemy.org'), (2, 'sandy', 'sandy@squirrelpower.org'), (1, 'spongebob', 'spongebob@sqlalchemy.org')]
> > > ROLLBACK

```

Выше используется параметр [`FunctionElement.over.partition_by`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.over.params.partition_by "sqlalchemy.sql.functions.FunctionElement.over"), чтобы `PARTITION BY` был отображен внутри OVER-оператора. Мы также можем использовать оператор `ORDER BY`, используя [`FunctionElement.over.order_by`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.over.params.order_by "sqlalchemy.sql.functions.FunctionElement.over"):


```

> > > stmt = (
> > > ... select(
> > > ... func.count().over(order_by=user_table.c.name),
> > > ... user_table.c.name,
> > > ... address_table.c.email_address,
> > > ...     )
> > > ... .select_from(user_table)
> > > ... .join(address_table)
> > > ... )
> > > with engine.connect() as conn:  
> > > ... result = conn.execute(stmt)
> > > ... print(result.all())
> > > BEGIN (implicit)
> > > SELECT count(*) OVER (ORDER BY user_account.name) AS anon_1,
> > > user_account.name, address.email_address
> > > FROM user_account JOIN address ON user_account.id = address.user_id
[...] ()
[(2, 'sandy', 'sandy@sqlalchemy.org'), (2, 'sandy', 'sandy@squirrelpower.org'), (3, 'spongebob', 'spongebob@sqlalchemy.org')]
> > > ROLLBACK

```

Дополнительные опции для оконных функций включают использование диапазонов; см. [`over()`](../core/sqlelement.html#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over") для получения дополнительных примеров.

Совет

Важно отметить, что метод [`FunctionElement.over()`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over") применяется только к тем SQL-функциям, которые являются агрегатными функциями; хотя конструкция [`Over`](../core/sqlelement.html#sqlalchemy.sql.expression.Over "sqlalchemy.sql.expression.Over") будет успешно отображаться для любой заданной SQL-функции, база данных отклонит выражение, если сама функция не является SQL-агрегатной функцией.

##### Специальные модификаторы WITHIN GROUP, FILTER {#tutorial-functions-within-group}

Синтаксис SQL "WITHIN GROUP" используется в сочетании с функцией агрегирования "упорядоченного набора" или "гипотетического набора". Общие функции "упорядоченного набора" включают `percentile_cont()` и `rank()`. SQLAlchemy включает встроенные реализации [`rank`](../core/functions.html#sqlalchemy.sql.functions.rank "sqlalchemy.sql.functions.rank"), [`dense_rank`](../core/functions.html#sqlalchemy.sql.functions.dense_rank "sqlalchemy.sql.functions.dense_rank"), [`mode`](../core/functions.html#sqlalchemy.sql.functions.mode "sqlalchemy.sql.functions.mode"), [`percentile_cont`](../core/functions.html#sqlalchemy.sql.functions.percentile_cont "sqlalchemy.sql.functions.percentile_cont") и [`percentile_disc`](../core/functions.html#sqlalchemy.sql.functions.percentile_disc "sqlalchemy.sql.functions.percentile_disc"), которые включают метод [`FunctionElement.within_group()`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group"):

```

> > > print(
> > > ... func.unnest(
> > > ... func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
> > > ...     )
> > > ... )
> > > unnest(percentile_disc(:percentile_disc_1) WITHIN GROUP (ORDER BY user_account.name))

```

"FILTER" поддерживается некоторыми бэкэндами для ограничения диапазона функции агрегирования до определенного подмножества строк по сравнению с общим диапазоном возвращаемых строк, доступных с помощью метода [`FunctionElement.filter()`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter"):

```

> > > stmt = (
> > > ... select(
> > > ... func.count(address_table.c.email_address).filter(user_table.c.name == "sandy"),
> > > ... func.count(address_table.c.email_address).filter(
> > > ... user_table.c.name == "spongebob"
> > > ...         ),
> > > ...     )
> > > ... .select_from(user_table)
> > > ... .join(address_table)
> > > ... )
> > > with engine.connect() as conn:  
> > > ... result = conn.execute(stmt)
> > > ... print(result.all())
> > > BEGIN (implicit)
> > > SELECT count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_1,
> > > count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_2
> > > FROM user_account JOIN address ON user_account.id = address.user_id
[...] ('sandy', 'spongebob')
[(2, 1)]
> > > ROLLBACK

```

##### Функции со значением таблицы {#tutorial-functions-table-valued}

Функции SQL со значением таблицы поддерживают скалярное представление, которое содержит именованные подэлементы. Часто используется для функций, ориентированных на JSON и ARRAY, а также для функций, таких как `generate_series()`. Функция со значением таблицы указывается в FROM-клаузе, а затем ссылается на нее как на таблицу или иногда даже как на столбец. Функции этой формы являются распространенными в базе данных PostgreSQL, однако некоторые формы функций со значением таблицы также поддерживаются SQLite, Oracle и SQL Server.

СмSQLAlchemy предоставляет метод [`FunctionElement.table_valued()`](../core/functions.html#sqlalchemy.sql.functions.FunctionElement.table_valued "sqlalchemy.sql.functions.FunctionElement.table_valued") в качестве основной конструкции "функции со значением таблицы", который преобразует объект [`func`](../core/sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func") в выражение FROM, содержащее ряд именованных столбцов на основе строковых имен, переданных позиционно. Это возвращает объект [`TableValuedAlias`](../core/selectable.html#sqlalchemy.sql.expression.TableValuedAlias "sqlalchemy.sql.expression.TableValuedAlias"), который является конструкцией с функцией, включенной в [`Alias`](../core/selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias"), который может использоваться как любое другое выражение FROM, как это было представлено в разделе [Использование псевдонимов](#tutorial-using-aliases). Ниже мы иллюстрируем функцию `json_each()`, которая, хотя и распространена в PostgreSQL, также поддерживается современными версиями SQLite:


```

> > > onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
> > > stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
> > > with engine.connect() as conn:
> > > ... result = conn.execute(stmt)
> > > ... result.all()
> > > BEGIN (implicit)
> > > SELECT anon_1.value
> > > FROM json_each(?) AS anon_1
> > > WHERE anon_1.value IN (?, ?)
[...] ('["one", "two", "three"]', 'two', 'three')
[('two',), ('three',)]
> > > ROLLBACK

```

Выше мы использовали функцию `json_each()` JSON, поддерживаемую SQLite и PostgreSQL, чтобы сгенерировать выражение со значением таблицы с одним столбцом, на который ссылается как `value`, а затем выбрали две из его трех строк.

Смотрите также


[Функции со значением таблицы](../dialects/postgresql.html#postgresql-table-valued) - в документации [PostgreSQL](../dialects/postgresql.html) -
этот раздел подробно описывает дополнительные синтаксисы, такие как специальные производные столбцы и "WITH ORDINALITY", которые известны работать с PostgreSQL.

##### Функции со значением столбца - функция со значением таблицы как скалярный столбец {#tutorial-functions-column-valued} 


Особый синтаксис, поддерживаемый PostgreSQL и Oracle, заключается в ссылке
на функцию в выражении FROM, которая затем представляет собой
один столбец в выражении столбцов оператора SELECT или другом контексте
выражения столбца. PostgreSQL широко использует этот синтаксис для таких
функций, как `json_array_elements()`, `json_object_keys()`,
`json_each_text()`, `json_each()`, и т.д.


SQLAlchemy называет это "функцией со[Функции со значением столбца](../dialects/postgresql.html#postgresql-column-valued) - в документации [PostgreSQL](../dialects/postgresql.html).

### Приведение типов данных и приведение типов {#tutorial-casts}


В SQL нам часто нужно явно указывать тип данных выражения, либо чтобы сообщить базе данных, какой тип ожидается в противном случае неоднозначного выражения, либо в некоторых случаях, когда мы хотим преобразовать подразумеваемый тип данных SQL-выражения в что-то другое. Для этой задачи используется ключевое слово SQL CAST, которое в SQLAlchemy предоставляется функцией [`cast()`](../core/sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast"). Эта функция принимает выражение столбца и объект типа данных в качестве аргументов, как показано ниже, где мы создаем SQL-выражение `CAST(user_account.id AS VARCHAR)` из объекта столбца `user_table.c.id`:


```

> > > from sqlalchemy import cast
> > > stmt = select(cast(user_table.c.id, String))
> > > with engine.connect() as conn:
> > > ... result = conn.execute(stmt)
> > > ... result.all()
> > > BEGIN (implicit)
> > > SELECT CAST(user_account.id AS VARCHAR) AS id
> > > FROM user_account
[...] ()
[('1',), ('2',), ('3',)]
> > > ROLLBACK

```

Функция [`cast()`](../core/sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast") не только отображает синтаксис SQL CAST, но также
производит выражение столбца SQLAlchemy, которое также будет действовать как данный тип на стороне Python. Выражение строки, которое [`cast()`](../core/sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast") в
[`JSON`](../core/type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON"), получит подсказки и операторы сравнения JSON, например:


```

> > > from sqlalchemy import JSON
> > > print(cast("{'a': 'b'}", JSON)["a"])
> > > CAST(:param_1 AS JSON)[:param_2]

```


#### type_coerce() - Python-only "cast"


Иногда необходимо, чтобы SQLAlchemy знал тип данных выражения по всем причинам, упомянутым выше, но не отображал само выражение CAST на стороне SQL, где оно может мешать SQL-операции, которая уже работает без него. Для этого довольно распространенного случая использования существует другая функция [`type_coerce()`](../core/sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce"), которая тесно связана с [`cast()`](../core/sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast"), поскольку она устанавливает выражение Python как имеющее определенный тип базы данных SQL, но не отображает ключевое слово CAST или тип данных на стороне базы данных. [`type_coerce()`](../core/sq)
```
>>> import json
>>> from sqlalchemy import JSON
>>> from sqlalchemy import type_coerce
>>> from sqlalchemy.dialects import mysql
>>> s = select(type_coerce({"some_key": {"foo": "bar"}}, JSON)["some_key"])
>>> print(s.compile(dialect=mysql.dialect()))
SELECT JSON_EXTRACT(%s, %s) AS anon_1
```
