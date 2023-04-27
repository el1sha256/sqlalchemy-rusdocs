title:  Использование операторов UPDATE и DELETE

## Использование операторов UPDATE и DELETE {#using-update-and-delete-statements}
До этого мы рассмотрели [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert"), чтобы добавить данные в нашу базу данных, и потратили много времени на [`Select`](../core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"), который обрабатывает широкий спектр использования для извлечения данных из базы данных. В этом разделе мы рассмотрим конструкции [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") и [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete"), которые используются для изменения существующих строк и удаления существующих строк. В этом разделе мы рассмотрим эти конструкции с точки зрения Core.

**ORM-читатели** - Как и в случае, упомянутом в [Использование операторов INSERT](data_insert.html#tutorial-core-insert), операции [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") и [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete"), когда они используются с ORM, обычно вызываются внутренне из объекта [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") в рамках процесса [единицы работы](../glossary.html#term-unit-of-work).

Однако, в отличие от [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert"), конструкции [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") и [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete") также могут использоваться напрямую с ORM, используя шаблон, известный как «ORM-enabled update and delete»; поэтому знакомство с этими конструкциями полезно для использования ORM. Оба стиля использования обсуждаются в разделах [Обновление объектов ORM с использованием шаблона единицы работы](orm_data_manipulation.html#tutorial-orm-updating) и [Удаление объектов ORM с использованием шаблона единицы работы](orm_data_manipulation.html#tutorial-orm-deleting).

### Конструкция выражения SQL update() {#tutorial-core-update}

Функция [`update()`](../core/dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update") генерирует новый экземпляр [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update"), который представляет оператор UPDATE в SQL, который обновит существующие данные в таблице.

Как и конструкция [`insert()`](../core/dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"), есть «традиционная» форма [`update()`](../core/dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"), которая генерирует оператор UPDATE для одной таблицы за раз и не возвращает никаких строк. Однако некоторые бэкэнды поддерживают оператор UPDATE, который может изменятьМетод [`Update.values()`](../core/dml.html#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values") управляет содержимым элементов SET оператора UPDATE. Этот метод используется также в конструкции [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert"). Обычно параметры могут быть переданы с использованием имен столбцов в качестве именованных аргументов.

UPDATE поддерживает все основные формы SQL UPDATE, включая обновления по выражениям, где мы можем использовать выражения [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"):

```
>>> stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
>>> print(stmt)
UPDATE user_account SET fullname=(:name_1 || user_account.name)
```

Для поддержки UPDATE в контексте "executemany", где множество наборов параметров будут вызываться для одного и того же оператора, можно использовать конструкцию [`bindparam()`](../core/sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam") для настройки привязанных параметров; они заменяют места, где обычно находятся литеральные значения:

```
>>> from sqlalchemy import bindparam
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == bindparam("oldname"))
...     .values(name=bindparam("newname"))
... )
>>> with engine.begin() as conn:
...     conn.execute(
...         stmt,
...         [
...             {"oldname": "jack", "newname": "ed"},
...             {"oldname": "wendy", "newname": "mary"},
...             {"oldname": "jim", "newname": "jake"},
...         ],
...     )
BEGIN (implicit)
UPDATE user_account SET name=? WHERE user_account.name = ?
[...] [('ed', 'jack'), ('mary', 'wendy'), ('jake', 'jim')]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Другие техники, которые могут быть применены к UPDATE, включают:

#### Связанные обновления {#tutorial-correlated-updates}

Оператор UPDATE может использовать строки в других таблицах, используя [связанный подзапрос](data_select.html#tutorial-scalar-subquery). Подзапрос может быть использован в любом месте, где может быть размещено выражение столбца:

```
>>> scalar_subq = (
...     select(address_table.c.email_address)
...     .where(address_table.c.user_id == user_table.c.id)
...     .order_by(address_table.c.id)
...     .limit(1)
...     .scalar_subquery()
... )
>>> update_stmt = update(user_table).values(fullname=scalar_subq)
>>> print(update_stmt)
UPDATE user_account SET fullname=(SELECT address.email_address
FROM address
WHERE address.user_id = user_account.id ORDER BY address.id
LIMIT :param_1)
```

#### UPDATE..FROM {#tutorial-update-from}

Некоторые базы данных, такие как PostgreSQL и MySQL, поддерживают синтаксис "UPDATE FROM", где дополнительные таблицы могут быть указаны непосредственно в специСуществует также специфический для MySQL синтаксис, который может обновлять несколько таблиц. Для этого необходимо ссылаться на объекты [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") в клаузе VALUES, чтобы ссылаться на дополнительные таблицы:


```
>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "patrick@aol.com")
...     .values(
...         {
...             user_table.c.fullname: "Pat",
...             address_table.c.email_address: "pat@aol.com",
...         }
...     )
... )
>>> from sqlalchemy.dialects import mysql
>>> print(update_stmt.compile(dialect=mysql.dialect()))
UPDATE user_account, address
SET address.email_address=%s, user_account.fullname=%s
WHERE user_account.id = address.user_id AND address.email_address = %s


```

#### Обновления с упорядоченными параметрами {#tutorial-parameter-ordered-updates} 


Еще одно поведение, специфичное только для MySQL, заключается в том, что порядок параметров в клаузе SET в операторе UPDATE фактически влияет на вычисление каждого выражения. Для этого случая метод [`Update.ordered_values()`](../core/dml.html#sqlalchemy.sql.expression.Update.ordered_values "sqlalchemy.sql.expression.Update.ordered_values") принимает последовательность кортежей, чтобы этот порядок можно было контролировать [[2]](#id2):


```
>>> update_stmt = update(some_table).ordered_values(
...     (some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10)
... )
>>> print(update_stmt)
UPDATE some_table SET y=:y, x=(some_table.y + :y_1)


```

[[2](#id1)]
Хотя словари Python гарантированно упорядочены по вставке, начиная с Python 3.7, метод [`Update.ordered_values()`](../core/dml.html#sqlalchemy.sql.expression.Update.ordered_values "sqlalchemy.sql.expression.Update.ordered_values") все еще обеспечивает дополнительную ясность намерений, когда необходимо, чтобы клауза SET оператора MySQL UPDATE происходила в определенном порядке.

### Конструкция выражения SQL delete() {#tutorial-deletes} 


Функция [`delete()`](../core/dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete") генерирует новый экземпляр [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete"), который представляет оператор DELETE в SQL, который удаляет строки из таблицы.


Конструкция [`delete()`](../core/dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete") с точки зрения API очень похожа на конструкцию [`update()`](../core/dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"), традиционно не возвращая строк, но позволяя использовать вариант RETURNING на некоторых базах данных.


```
>>> from sqlalchemy import delete
>>> stmt = delete(user_table).where(user_table.c.name == "patrick")
>>> print(stmt)
DELETE```
>>> delete_stmt = (
...     delete(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "patrick@aol.com")
... )
>>> from sqlalchemy.dialects import mysql
>>> print(delete_stmt.compile(dialect=mysql.dialect()))
DELETE FROM user_account USING user_account, address
WHERE user_account.id = address.user_id AND address.email_address = %s


```


### Получение количества затронутых строк при UPDATE, DELETE {#tutorial-update-delete-rowcount} 


Классы [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") и [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete") поддерживают возможность
возвращения количества строк, соответствующих условию, после выполнения операции, для операций,
которые вызываются через [`Connection`](../core/connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection") ядра, т.е.
[`Connection.execute()`](../core/connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"). С учетом оговорок, упомянутых ниже, это значение
доступно через атрибут [`CursorResult.rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.rowcount "sqlalchemy.engine.CursorResult.rowcount"):


```
>>> with engine.begin() as conn:
...     result = conn.execute(
...         update(user_table)
...         .values(fullname="Patrick McStar")
...         .where(user_table.c.name == "patrick")
...     )
...     print(result.rowcount)
BEGIN (implicit)
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Patrick McStar', 'patrick')
1
COMMIT


```


Совет


Класс [`CursorResult`](../core/connections.html#sqlalchemy.engine.CursorResult "sqlalchemy.engine.CursorResult") является подклассом
[`Result`](../core/connections.html#sqlalchemy.engine.Result "sqlalchemy.engine.Result"), который содержит дополнительные атрибуты, специфичные для объекта `cursor` DBAPI. Экземпляр этого подкласса
возвращается, когда оператор вызывается через метод
[`Connection.execute()`](../core/connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"). При использовании ORM метод
[`Session.execute()`](../orm/session_api.html#sqlalchemy.orm.Session.execute "sqlalchemy.orm.Session.execute") возвращает объект этого типа для всех операторов INSERT, UPDATE и DELETE.

Факты об [`CursorResult.rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.rowcount "sqlalchemy.engine.CursorResult.rowcount"):* Возвращаемое значение - это количество строк, **соответствующих** условию WHERE в запросе. Не имеет значения, были ли строки фактически изменены или нет.
* [`CursorResult.rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.rowcount "sqlalchemy.engine.CursorResult.rowcount") не всегда доступен для операторов UPDATE или DELETE, использующих RETURNING.
* Для выполнения [executemany](dbapi_transactions.html#tutorial-multiple-parameters) [`CursorResult.rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.rowcount "sqlalchemy.engine.CursorResult.rowcount") также может быть недоступен, что сильно зависит от используемого модуля DBAPI и настроенных параметров. Атрибут [`CursorResult.supports_sane_multi_rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.supports_sane_multi_rowcount "sqlalchemy.engine.CursorResult.supports_sane_multi_rowcount") указывает, будет ли этот параметр доступен для текущей используемой базы данных.
* Некоторые драйверы, особенно сторонние диалекты для нереляционных баз данных, могут вообще не поддерживать [`CursorResult.rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.rowcount "sqlalchemy.engine.CursorResult.rowcount"). Атрибут [`CursorResult.supports_sane_rowcount`](../core/connections.html#sqlalchemy.engine.CursorResult.supports_sane_rowcount "sqlalchemy.engine.CursorResult.supports_sane_rowcount") указывает на это.
* «rowcount» используется процессом ORM [unit of work](../glossary.html#term-unit-of-work) для проверки того, что оператор UPDATE или DELETE соответствует ожидаемому количеству строк, и также является необходимым для функции ORM версионирования, описанной в разделе [Configuring a Version Counter](../orm/versioning.html#mapper-version-counter).


### Использование RETURNING с UPDATE, DELETE 


Как и конструкция [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert"), [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") и [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete")
также поддерживают оператор RETURNING, который добавляется с помощью методов [`Update.returning()`](../core/dml.html#sqlalchemy.sql.expression.Update.returning "sqlalchemy.sql.expression.Update.returning") и [`Delete.returning()`](../core/dml.html#sqlalchemy.sql.expression.Delete.returning "sqlalchemy.sql.expression.Delete.returning").
Когда эти методы используются на бэкэнде, который поддерживает RETURNING, выбранные
столбцы из всех строк, которые соответствуют условиям WHERE в запросе,
будут возвращены в объекте [`Result`](../core/connections.html#sqlalchemy.engine.Result "sqlalchemy.engine.Result") в виде строк, которые можно
перебирать:


```
>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
...     .returning(user_table.c.id, user_table.c.name)
... )
>>> print(update_stmt)
UPDATE user_account SET fullname=:fullname
WHEREORM-возможности для UPDATE и DELETE:

* [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update") - обновление данных
* [`Delete`](../core/dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete") - удаление данных