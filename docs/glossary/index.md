title: Глоссарий


!!! warning

    Этот раздел не редактировался людьми, возможны ошибки и неточности в форматировании, вы можете помочь исправив и сделав pull request


1.x стиль2.0 стильЭти термины новы в SQLAlchemy 1.4 и относятся к плану перехода SQLAlchemy 1.4->2.0, описанному
в [SQLAlchemy 2.0 - Major Migration Guide](changelog/migration_20.html). Термин "1.x стиль" относится к API,
использованному так, как это было задокументировано на протяжении серии 1.x и ранее (например, 1.3, 1.2 и т.д.), а
термин "2.0 стиль" относится к тому, как будет выглядеть API в версии 2.0. Версия 1.4 реализует почти все API 2.0 в так
называемом "режиме перехода", в то время как версия 2.0 все еще поддерживает устаревший
объект [`Query`](orm/queryguide/query.html#sqlalchemy.orm.Query "sqlalchemy.orm.Query"), чтобы устаревший код оставался
в значительной степени совместимым с 2.0.

См. также

[SQLAlchemy 2.0 - Major Migration Guide](changelog/migration_20.html)

ACIDМодель ACIDАкроним для "Atomicity, Consistency, Isolation, Durability"; набор свойств, гарантирующих надежную
обработку транзакций базы данных.
(через Википедию)

См. также

[атомарность](#term-atomicity)

[согласованность](#term-consistency)

[изоляция](#term-isolation)

[надежность](#term-durability)

[Модель ACID (через Википедию)](https://en.wikipedia.org/wiki/ACID_Model)

Двухуровневая ассоциативная[связь](#term-relationship), которая связывает две таблицы
вместе, используя таблицу ассоциации посередине.
Ассоциативная связь отличается от [многие ко многим](#term-many-to-many)
отношение в том, что таблица многие-ко-многим отображается
полным классом, а не обрабатывается невидимо
конструкцией [`sqlalchemy.orm.relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
как в случае
с многие-ко-многим, так что дополнительные атрибуты
явно доступны.

Например, если мы хотим связать сотрудников с
проектами, также храня конкретную роль для этого сотрудника
с проектом, реляционная схема может выглядеть так:

```
CREATE TABLE employee (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30)
)

CREATE TABLE project (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30)
)

CREATE TABLE employee\_project (
 employee\_id INTEGER PRIMARY KEY,
 project\_id INTEGER PRIMARY KEY,
 role\_name VARCHAR(30),
 FOREIGN KEY employee\_id REFERENCES employee```
proj.project_employees.extend(
    [
        EmployeeProject(employee=emp1, role_name="технический лидер"),
        EmployeeProject(employee=emp2, role_name="клиентский менеджер"),
    ]
)
```

См. также

[многие ко многим](#term-many-to-many)

атомарностьАтомарность является одним из компонентов модели [ACID](#term-ACID) и требует, чтобы каждая транзакция была "
все или ничего": если одна часть транзакции не удалась, вся транзакция не удалась, и состояние базы данных остается
неизменным. Атомарная система должна гарантировать атомарность в любой ситуации, включая отключения питания, ошибки и
сбои.
(из Википедии)

См. также

[ACID](#term-ACID)

[Атомарность (через Википедию)](https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%BE%D0%BC%D0%B0%D1%80%D0%BD%D0%BE%D1%81%D1%82%D1%8C_(%D0%B1%D0%B0%D0%B7%D1%8B_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85))

прикрепленныйОбозначает ORM-объект, который в настоящее время связан с определенной [Session](#term-Session).

См. также

[Краткое введение в состояния объектов](orm/session_state_management.html#session-object-states)

обратная ссылкабидирекциональная связьРасширение системы [relationship](#term-relationship), при котором два отдельных
объекта [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") могут
быть взаимосвязаны друг с другом, так что они координируются в памяти при изменениях с любой стороны. Самый
распространенный способ создания этих двух отношений - использование
функции [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") явно для
одной стороны и указание ключевого слова `backref`, чтобы
другая [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
создавалась автоматически. Мы можем проиллюстрировать это на примере, который мы использовали
в [один ко многим](#term-one-to-many), следующим образом:

```
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    employees = relationship("Employee", backref="department")


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dep_id = Column(Integer, ForeignKey("department.id"))
```

Обратная ссылка может быть применена к любому отношению, включая один ко многим, мнОтправка параметров -
в [SQLAlchemy Unified Tutorial](tutorial/index.html#unified-tutorial)

Кандидатский ключ - термин реляционной алгебры, относящийся к атрибуту или набору атрибутов, которые образуют уникальный
идентифицирующий ключ для строки. У строки может быть более одного кандидатского ключа, каждый из которых подходит для
использования в качестве первичного ключа этой строки. Первичный ключ таблицы всегда является кандидатским ключом.

См. также

[primary key](#term-primary-key)

[Кандидатский ключ (через Википедию)](https://en.wikipedia.org/wiki/Candidate_key)

<https://www.databasestar.com/database-keys/>

Декартово произведение - для двух множеств A и B декартово произведение является множеством всех упорядоченных пар (a,
b), где a находится в A, а b находится в B.

В терминах SQL-баз данных декартово произведение происходит, когда мы выбираем из двух или более таблиц (или других
подзапросов) без установления каких-либо критериев между строками одной таблицы и другой (непосредственно или косвенно).
Если мы выбираем из таблицы A и таблицы B одновременно, мы получаем каждую строку A, сопоставленную с первой строкой B,
затем каждую строку A, сопоставленную со второй строкой B, и так далее, пока каждая строка из A не будет сопоставлена со
всеми строками из B.

Декартово произведение приводит к генерации огромных наборов результатов и может легко вызвать сбой клиентского
приложения, если не предотвратить его.

См. также

[Декартово произведение (через Википедию)](https://en.wikipedia.org/wiki/Cartesian_product)

Каскад - термин, используемый в SQLAlchemy для описания того, как действие сохранения ORM, которое происходит с
определенным объектом, распространяется на другие объекты, которые непосредственно связаны с этим объектом. В SQLAlchemy
эти связи объектов настраиваются с помощью
конструкции [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship). [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship)
содержит параметр,
называемый [`relationship.cascade`](orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade), который
предоставляет опции, какие операции сохранения могут распространяться.

Термин "каскады", а также общая архитектура этой системы в SQLAlchemy были заимствованы, лучше или хуже, из ORM
Hibernate.

См. также

[КСогласованность

Согласованность является одним из компонентов модели [ACID](#term-ACID) и гарантирует, что любая транзакция приведет
базу данных из одного допустимого состояния в другое. Любые данные, записанные в базу данных, должны быть допустимы в
соответствии со всеми определенными правилами, включая, но не ограничиваясь, [ограничениями](#term-constraints),
каскадами, триггерами и любой их комбинацией. (источник: Wikipedia)

См. также

[ACID](#term-ACID)

[Согласованность (через Wikipedia)](https://en.wikipedia.org/wiki/Consistency_(database_systems))

Ограничение

Ограничения - это правила, установленные в пределах реляционной базы данных, которые обеспечивают допустимость и
согласованность данных. Общие формы ограничений
включают [ограничение первичного ключа](#term-primary-key-constraint), [ограничение внешнего ключа](#term-foreign-key-constraint)
и [ограничение проверки](#term-check-constraint).

Коррелированный подзапрос

Коррелированный подзапрос - это [подзапрос](#term-subquery), который зависит от данных в охватывающем `SELECT`.

Ниже приведен подзапрос, который выбирает агрегированное значение `MIN(a.id)` из таблицы `email_address`, так что он
будет вызываться для каждого значения `user_account.id`, коррелируя значение этого столбца
с `email_address.user_account_id`:

```
SELECT user\_account.name, email\_address.email
 FROM user\_account
 JOIN email\_address ON user_account.id=email_address.user_account_id
 WHERE email_address.id = (
 SELECT MIN(a.id) FROM email_address AS a
 WHERE a.user_account_id=user_account.id
 )
```

Вышеуказанный подзапрос ссылается на таблицу `user_account`, которая сама не находится в `FROM`-клаузе этого вложенного
запроса. Вместо этого таблица `user_account` получается из охватывающего запроса, где каждая выбранная строка
из `user_account` приводит к отдельному выполнению подзапроса.

Коррелированный подзапрос в большинстве случаев присутствует в [WHERE-клаузе](#term-WHERE-clause)
или [клаузе столбцов](#term-columns-clause) непосредственно охватывающего оператора `SELECT`, а также в клаузе ORDER BY
или HAVING.

В менее распространенных случаях коррелированный подзапрос может присутствовать в [FROM-клаузе](#term-FROM-clause)
охватывающего `SELECT`; в этих случаях
корреля[Курсор (через Википедию)](https://ru.wikipedia.org/wiki/%D0%9A%D1%83%D1%80%D1%81%D0%BE%D1%80_(%D0%B1%D0%B0%D0%B7%D1%8B_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85))

цикломатическая сложность - это мера сложности кода, основанная на количестве возможных путей через исходный код
программы.

См. также

[Цикломатическая сложность](https://ru.wikipedia.org/wiki/%D0%A6%D0%B8%D0%BA%D0%BB%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%BB%D0%BE%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D1%8C)

DBAPIpep-249DBAPI - это сокращение от фразы «Python Database API Specification». Это широко используемая спецификация в
Python, которая определяет общие шаблоны использования для всех пакетов подключения к базе данных. DBAPI - это
«низкоуровневый» API, который обычно является самым низким уровнем системы, используемой в приложении Python для общения
с базой данных. Система диалектов SQLAlchemy построена вокруг работы с DBAPI, предоставляя отдельные классы диалектов,
которые обслуживают конкретный DBAPI поверх конкретного движка базы данных; например,
URL `postgresql+psycopg2://@localhost/test` относится к комбинации DBAPI /
диалект [`psycopg2`](dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2 "sqlalchemy.dialects.postgresql.psycopg2"),
тогда как URL `mysql+mysqldb://@localhost/test` относится к комбинации DBAPI /
диалект [`MySQL для Python`](dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb "sqlalchemy.dialects.mysql.mysqldb").

См. также

[PEP 249 - Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/)

DDL - это аббревиатура от **Data Definition Language**. DDL - это подмножество SQL, которое реляционные базы данных
используют для настройки таблиц, ограничений и других постоянных объектов в схеме базы данных. SQLAlchemy предоставляет
богатый API для создания и вывода выражений DDL.

См. также

[Описание баз данных с MetaData](core/metadata.html)

[DML](#term-DML)

[DQL](#term-DQL)

deleted - это описывает одно из основных состояний объекта, которое может иметь в [Session](#term-Session); удаленный
объект - это объект, который ранее быКласс `MyClass` будет [отображен](#term-mapped), когда его определение будет
завершено, после чего атрибуты `id` и `data`, начинающиеся как
объекты [`Column`](core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"), будут заменены
системой [инструментации](#term-instrumentation) на
экземпляры [`InstrumentedAttribute`](orm/internals.html#sqlalchemy.orm.InstrumentedAttribute "sqlalchemy.orm.InstrumentedAttribute"),
которые являются дескрипторами, предоставляющими вышеупомянутые методы `__get__()`, `__set__()`
и `__delete__()`. [`InstrumentedAttribute`](orm/internals.html#sqlalchemy.orm.InstrumentedAttribute "sqlalchemy.orm.InstrumentedAttribute")
будет генерировать выражение SQL при использовании на уровне класса:

```
>>> print(MyClass.data == 5)
data = :data_1
```

а на уровне экземпляра отслеживает изменения значений и также [лениво загружает](#term-lazy-loads) не загруженные
атрибуты из базы данных:

```
>>> m1 = MyClass()
>>> m1.id = 5
>>> m1.data = "some data"

>>> from sqlalchemy import inspect
>>> inspect(m1).attrs.data.history.added
"some data"
```

Отсоединенный. Это описывает одно из основных состояний объекта, которое может иметь в [Session](#term-Session);
отсоединенный объект - это объект, который имеет идентификатор базы данных (т.е. первичный ключ), но не связан с
какой-либо сессией. Объект, который ранее был [постоянным](#term-persistent) и был удален из своей сессии, либо потому,
что он был удален, либо потому, что владеющая сессия была закрыта, переходит в состояние отсоединения. Состояние
отсоединения обычно используется, когда объекты перемещаются между сессиями или когда они перемещаются в/из внешнего
кэша объектов.

См. также

[Quickie Intro to Object States](orm/session_state_management.html#session-object-states)

Диалект. В SQLAlchemy «диалект» - это объект Python, который представляет информацию и методы, которые позволяют
выполнять операции с базой данных на конкретном типе базы данных и конкретном типе драйвера Python (
или [DBAPI](#term-DBAPI)) для этой базы данных. Диалекты SQLAlchemy являются подклассами
класса [`Dialect`](core/internals.html#sqlalchemy.engine.Dialect "sqlalchemy.engine.Dialect").

См. также

[Engine Configuration](core/engines.html)

Дискриминатор. Столбец результата, который используется во время [полиморфной](#term-polymorphic) загрузки, чтобы
определить, какой тип отображенного класса должDQL - это аббревиатура от "Data Query Language". DQL - это подмножество
SQL, которое используют реляционные базы данных для чтения данных в таблицах. DQL почти исключительно относится к
конструкции SQL SELECT в качестве основного оператора SQL.

См. также

[DQL (через Wikipedia)](https://en.wikipedia.org/wiki/Data_query_language)

[DML](#term-DML)

[DDL](#term-DDL)

durability - это свойство модели [ACID](#term-ACID), которое означает, что после того, как транзакция была подтверждена,
она останется такой, даже в случае потери питания, сбоев или ошибок. В реляционной базе данных, например, после того,
как группа SQL-операторов выполнена, результаты должны быть сохранены навсегда (даже если база данных немедленно
аварийно завершится).

(via Wikipedia)

См. также

[ACID](#term-ACID)

[Durability (через Wikipedia)](https://en.wikipedia.org/wiki/Durability_(database_systems))

eager load - в отображении объектов-отношений "eager load" относится к атрибуту, который заполняется его значением на
стороне базы данных в то же время, когда сам объект загружается из базы данных. В SQLAlchemy термин "eager loading"
обычно относится к связанным коллекциям и экземплярам объектов, которые связаны между отображениями с использованием
конструкции [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), но
также может относиться к дополнительным атрибутам столбцов, которые загружаются, часто из других таблиц, связанных с
определенной запрашиваемой таблицей, например, при использовании отображений наследования.

Eager loading - это противоположность [lazy loading](#term-lazy-loading).

См. также

[Techniques of Relationship Loading](orm/queryguide/relationships.html)

executemany - этот термин относится к части спецификации [**PEP 249**](https://peps.python.org/pep-0249/) DBAPI,
указывающей на один SQL-оператор, который может быть вызван против соединения с базой данных с несколькими наборами
параметров. Конкретный метод известен как [cursor.executemany()](https://peps.python.org/pep-0249/#executemany), и у
него много поведенческих отличий по сравнению с методом [cursor.execute()](https://peps.python.org/pep-0249/#execute),
который используется для вызова одного оператора. Метод "executemany" выполняет данный SQL-оператор несколько раз, по
одному разу для каждого переданного набора параметров.Для преодоления этого ограничения SQLAlchemy начиная с серии 2.0
реализует альтернативную форму "executemany", которая
называется ["Insert Many Values" Behavior for INSERT statements](core/connections.html#engine-insertmanyvalues). Эта
функция использует `cursor.execute()` для вызова оператора INSERT, который будет выполнять несколько наборов параметров
за один проход, таким образом, производя тот же эффект, что и использование `cursor.executemany()`, при этом поддерживая
RETURNING.

См. также

[Отправка нескольких параметров](tutorial/dbapi_transactions.html#tutorial-multiple-parameters) - введение в учебник "
executemany"

["Insert Many Values" Behavior for INSERT statements](core/connections.html#engine-insertmanyvalues) - функция
SQLAlchemy, которая позволяет использовать RETURNING с "executemany"

expireexpiredexpiresexpiringExpiring В ORM SQLAlchemy относится к тому, когда данные в [persistent](#term-persistent)
или иногда [detached](#term-detached) объекте стираются, так что при следующем доступе к атрибутам объекта будет
отправлен SQL-запрос [lazy load](#term-lazy-load), чтобы обновить данные для этого объекта, как они хранятся в текущей
идущей транзакции.

См. также

[Обновление / истечение срока действия](orm/session_state_management.html#session-expire)

facadeОбъект, который служит в качестве интерфейса, маскирующего более сложный
подлежащий или структурный код.

См. также

[Шаблон фасада (через Википедию)](https://en.wikipedia.org/wiki/Facade_pattern)

foreign key constraintОграничение ссылочной целостности между двумя таблицами. Внешний ключ - это поле или набор полей в
реляционной таблице, которое соответствует [кандидатскому ключу](#term-candidate-key) другой таблицы.
Внешний ключ может использоваться для перекрестной ссылки таблиц.
(через Википедию)

Ограничение внешнего ключа может быть добавлено к таблице в стандартном
SQL с использованием [DDL](#term-DDL) следующим образом:

```
ALTER TABLE employee ADD CONSTRAINT dep\_id\_fk
FOREIGN KEY (employee) REFERENCES department (dep\_id)
```

См. также

[Ограничение внешнего ключа (через Википедию)](https://en.wikipedia.org/wiki/Foreign_key_constraint)

FROM clauseЧасть оператора `SELECT`, которая указывает начальный
источник строк.

Простой `SELECT` будет содержать одно или несколько имен таблиц в его
FROM clause. Несколько источников разделяются запятой:

```
SELECT user.name, address.email\_address
FROM user, address
WHERE user.id=address.user\_id
```

FROM clause также является местом, где указываidentity map
Карта идентичности - это отображение между объектами Python и их идентификаторами в базе данных. Карта идентичности -
это коллекция, связанная с объектом ORM [Session](#term-Session), и поддерживает единственный экземпляр каждого объекта
базы данных, ключевым является его идентификатор. Преимущество этого шаблона заключается в том, что все операции,
которые происходят для определенного идентификатора базы данных, прозрачно координируются на один объектный экземпляр.
При использовании карты идентичности в сочетании с [изолированной](#term-isolated) транзакцией, имея ссылку на объект,
который известен по определенному первичному ключу, можно считать с практической точки зрения прокси фактической строки
базы данных.

См. также

[Карта идентичности (через Martin Fowler)](https://martinfowler.com/eaaCatalog/identityMap.html)

[Получение по первичному ключу](orm/session_basics.html#session-get) - как искать объект в карте идентичности по
первичному ключу

императивный декларативный
В ORM SQLAlchemy эти термины относятся к двум разным стилям отображения классов Python на таблицы базы данных.

См. также

[Декларативное отображение](orm/mapping_styles.html#orm-declarative-mapping)

[Императивное отображение](orm/mapping_styles.html#orm-imperative-mapping)

insertmanyvalues
Это относится к функциональности, специфичной для SQLAlchemy, которая позволяет операторам INSERT выдавать тысячи новых
строк в рамках одного оператора, позволяя при этом возвращать значения, созданные сервером, встроенные в оператор с
помощью RETURNING или подобных методов, для оптимизации производительности. Эта функция предназначена для
автоматического использования на выбранных бэкэндах, но предлагает некоторые конфигурационные параметры. См.
раздел [Поведение "Вставить много значений" для операторов INSERT](core/connections.html#engine-insertmanyvalues) для
полного описания этой функции.

См. также

[Поведение "Вставить много значений" для операторов INSERT](core/connections.html#engine-insertmanyvalues)

инструментирование
Инструментирование относится к процессу расширения функциональности и набора атрибутов определенного класса. В идеале
поведение класса должно оставаться близким к обычному классу, за исключением того, что дополнительные функции и
возможности становятся доступными. Процесс [отЛенивая загрузка (lazy load) - это техника, используемая в
объектно-реляционном отображении, при которой атрибут не содержит значения, полученного из базы данных в течение
некоторого времени, обычно при первой загрузке объекта. Вместо этого атрибут получает мемоизацию, которая заставляет его
обратиться к базе данных и загрузить свои данные при первом использовании. Используя этот шаблон, сложность и время,
затраченное на получение объектов, иногда можно уменьшить, поскольку атрибуты для связанных таблиц не нужно обрабатывать
немедленно.

Ленивая загрузка - это противоположность [жадной загрузке](#term-eager-loading).

В SQLAlchemy ленивая загрузка является ключевой функцией ORM и применяется к атрибутам,
которые [отображены](#term-mapped) на пользовательский класс. Когда обращаются к атрибутам, которые относятся к столбцам
базы данных или связанным объектам, для которых нет загруженного значения, ORM
использует [`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), с которым связан текущий
объект в состоянии [persistent](#term-persistent), и генерирует SELECT-запрос в текущей транзакции, начиная новую
транзакцию, если она не была запущена. Если объект находится в состоянии [detached](#term-detached) и не связан с
какой-либо [`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), это считается ошибочным
состоянием, и генерируется [информативное исключение](errors.html#error-bhk3).

См. также

[Ленивая загрузка (через Martin Fowler)](https://martinfowler.com/eaaCatalog/lazyLoad.html)

[Проблема N+1](#term-N-plus-one-problem)

[Опции загрузки столбцов](orm/queryguide/columns.html#loading-columns) - содержит информацию о ленивой загрузке
отображаемых столбцов ORM

[Техники загрузки отношений](orm/queryguide/relationships.html) - содержит информацию о ленивой загрузке связанных
объектов ORM

[Предотвращение неявного ввода-вывода при использовании AsyncSession](orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads) -
советы по избежанию ленивой загрузки при использовании
расширения [Asynchronous I/O (asyncio)](orm/extensions/asyncio.html)

Многие ко многим (many-to-many) - это
стиль [`sqlalchemy.orm.relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
который связывает две таблицы через промежуточную таблицу посередине. Используя эту конфигурацию, любое количествоВыше
определены коллекции `Employee.projects` и обратная связь `Project.employees`:

```
proj = Project(name="Клиент A")

emp1 = Employee(name="emp1")
emp2 = Employee(name="emp2")

proj.employees.extend([emp1, emp2])
```

См. также

[ассоциативная связь](#term-association-relationship)

[связь](#term-relationship)

[один ко многим](#term-one-to-many)

[многие к одному](#term-many-to-one)

многие к
одномуСтиль [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
который связывает
внешний ключ в таблице родительского отображения с первичным
ключом связанной таблицы. Каждый объект-родитель может
ссылаться на ровно ноль или один связанный объект.

Связанные объекты, в свою очередь, будут иметь неявную или
явную [один ко многим](#term-one-to-many) связь с любым количеством
родительских объектов, которые на них ссылается.

Пример схемы многие к одному (которая, заметим, идентична
схеме [один ко многим](#term-one-to-many)):

```
CREATE TABLE department (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30)
)

CREATE TABLE employee (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30),
 dep\_id INTEGER REFERENCES department(id)
)
```

Связь от `employee` к `department` является
многие к одному, так как многие записи сотрудников могут быть связаны с
одним отделом. Отображение SQLAlchemy может выглядеть так:

```
class Department(Base):
    \_\_tablename\_\_ = "department"
    id = Column(Integer, primary\_key=True)
    name = Column(String(30))


class Employee(Base):
    \_\_tablename\_\_ = "employee"
    id = Column(Integer, primary\_key=True)
    name = Column(String(30))
    dep\_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department")
```

См. также

[связь](#term-relationship)

[один ко многим](#term-one-to-many)

[обратная связь](#term-backref)

отображениеОтображенный класс ORMОтображенный класс ORMМы говорим, что класс «отображен», когда он был связан с
экземпляром класса [`Mapper`](orm/mapping_api.html#sqlalchemy.orm.Mapper "sqlalchemy.orm.Mapper"). Этот процесс
связывает
класс с таблицей базы данных или другой [selectable](#term-selectable) конструкцией,
чтобы экземпляры могли быть сохранены и загружены с помощью
[`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session").

См. также

[Обзор отображенных классов ORM](orm/mapping_styles.html)

маршаллингмаршаллинг данныхПроцесс преобразования представления объекта в памяти вРасширение существующих
типов - [`TypeDecorator`](core/custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
SQLAlchemy часто используется для маршалинга данных при отправке данных в базу данных для операций INSERT и UPDATE, а
также для "размаршаливания" данных при их извлечении с помощью операций SELECT.

Метаданные - термин "метаданные" обычно относится к "данным, описывающим данные"; данные, которые сами представляют
формат и/или структуру каких-либо других данных. В SQLAlchemy термин "метаданные" обычно относится к
конструкции [`MetaData`](core/metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"), которая является
коллекцией информации о таблицах, столбцах, ограничениях и других объектах [DDL](#term-DDL), которые могут существовать
в конкретной базе данных.

См. также

[Metadata Mapping (через Martin Fowler)](https://www.martinfowler.com/eaaCatalog/metadataMapping.html)

[Работа с метаданными базы данных](tutorial/metadata.html#tutorial-working-with-metadata) -
в [SQLAlchemy Unified Tutorial](tutorial/index.html#unified-tutorial)

Цепочка методов - "Цепочка методов", называемая в документации SQLAlchemy "генеративной", является
объектно-ориентированной техникой, при которой состояние объекта создается путем вызова методов объекта. Объект содержит
любое количество методов, каждый из которых возвращает новый объект (или в некоторых случаях тот же объект) с
добавленным состоянием объекта.

Два объекта SQLAlchemy, которые наиболее часто используют цепочку методов, это
объект [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") и
объект [`Query`](orm/queryguide/query.html#sqlalchemy.orm.Query "sqlalchemy.orm.query.Query"). Например,
объект [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") может быть
назначен двум выражениям в его условии WHERE, а также выражению ORDER BY, вызвав
методы [`Select.where()`](core/selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")
и [`Select.order_by()`](core/selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by"):

```
stmt = (
    select(user.c.name)
    .where(user.c.id > 5)
    .where(user.c.name.like("e%"))
    .order\_by(user.c.name)
)
```

Каждый вызов метода выше возвращает копию исходного
объекта [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") с
добавленными дополнительными квалификаторами.

Миксин-класс - это распространенный объектно-ориентированный шаблон, где класс содержит методы или атрибуты для
использования другими классами, не являяСтратегии загрузки

Техники загрузки отношений

one to many
Стиль [`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), который
связывает первичный ключ таблицы родительского отображения с внешним ключом связанной таблицы. Каждый уникальный
объект-родитель может ссылаться на ноль или более уникальных связанных объектов.

Связанные объекты, в свою очередь, будут иметь неявное или явное [many to one](#term-many-to-one) отношение к своему
родительскому объекту.

Пример схемы one to many (которая, заметьте, идентична схеме [many to one](#term-many-to-one)):

```
CREATE TABLE department (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30)
)

CREATE TABLE employee (
 id INTEGER PRIMARY KEY,
 name VARCHAR(30),
 dep\_id INTEGER REFERENCES department(id)
)
```

Отношение от `department` к `employee` является one to many, так как множество записей employee может быть связано с
одним department. Отображение SQLAlchemy может выглядеть так:

```
class Department(Base):
    \_\_tablename\_\_ = "department"
    id = Column(Integer, primary\_key=True)
    name = Column(String(30))
    employees = relationship("Employee")


class Employee(Base):
    \_\_tablename\_\_ = "employee"
    id = Column(Integer, primary\_key=True)
    name = Column(String(30))
    dep\_id = Column(Integer, ForeignKey("department.id"))
```

Смотрите также

[relationship](#term-relationship)

[many to one](#term-many-to-one)

[backref](#term-backref)

ORM-аннотации
Фраза «ORM-аннотированный» относится к внутреннему аспекту SQLAlchemy, где объект Core, такой как
объект [`Column`](core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"), может нести дополнительную
информацию о времени выполнения, которая помечает его как принадлежащий определенному ORM-отображению. Этот термин не
следует путать с общей фразой «аннотация типа», которая относится к подсказкам типа исходного кода Python, используемым
для статической типизации, как это было представлено в [**PEP 484**](https://peps.python.org/pep-0484/).

Большинство примеров кода SQLAlchemy, документированных в документации, отформатированы с небольшим примечанием
«Annotated Example» или «Non-annotated Example». Это относится к тому, аннотирован ли пример [**PEP 484
**](https://peps.python.org/pep-0484/), и не связан с понятием SQLAlchemy «ORM-аннотированный».

Когда в документации появляется фраза «ORM-аннотированный», она относится к объектам выражений SQL Core, таким
как [`Table`](core/metadata.html#sqlalchemy.schema.Table "sqlalchemyВнутреннее
состояние [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") относится
к [`Table`](core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), к которому отображается `User`. Сам
класс `User` не непосредственно ссылается. Таким образом,
конструкция [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
остается совместимой с процессами уровня Core (обратите внимание, что член `._raw_columns`
объекта [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") является
закрытым и не должен быть доступен для кода конечного пользователя):

```
>>> stmt.\_raw\_columns
[Table('user\_account', MetaData(), Column('id', Integer(), ...)]
```

Однако, когда наш [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
передается в ORM [`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), сущности ORM,
косвенно связанные с объектом, используются для интерпретации
этого [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select") в контексте
ORM. Фактические «ORM-аннотации» можно увидеть в другой закрытой переменной `._annotations`:

```
>>> stmt.\_raw\_columns[0].\_annotations
immutabledict({
 'entity\_namespace': <Mapper at 0x7f4dd8098c10; User>,
 'parententity': <Mapper at 0x7f4dd8098c10; User>,
 'parentmapper': <Mapper at 0x7f4dd8098c10; User>
})
```

Поэтому мы называем `stmt` **ORM-аннотированным объектом select()**. Это
выражение [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"), которое
содержит дополнительную информацию, которая приведет к его интерпретации в специфическом для ORM контексте при передаче
методам, таким
как [`Session.execute()`](orm/session_api.html#sqlalchemy.orm.Session.execute "sqlalchemy.orm.Session.execute").

pendingЭто описывает одно из основных состояний объекта, которое
может иметь внутри [Session](#term-Session); ожидающий объект

- это новый объект, у которого нет идентификатора в базе данных,
  но недавно связанный с сеансом. Когда
  сеанс запускает флаш и строка вставляется, объект переходит в состояние
  [постоянный](#term-persistent).

См. также

[Краткое введение в состояния объектов](orm/session_state_management.html#session-object-states)

persistentЭто описывает одно из основных состояний объекта, которое
может иметь внутри [Session](#term-Session); постоянный объект

- это объект, у которого есть идентификатор в базе данных (т.е. первичный ключ)
  и в настВ частности, основным «плагином» является плагин «orm», который
  является основой системы, которую ORM SQLAlchemy использует
  для составления и выполнения SQL-запросов, возвращающих результаты ORM.

См. также

[ORM Query Unified with Core Select](changelog/migration_20.html#migration-20-unify-select)

polymorphicpolymorphicallyОтносится к функции, которая обрабатывает несколько типов одновременно. В SQLAlchemy
термин обычно применяется к концепции ORM отображаемого класса,
при которой операция запроса будет возвращать различные подклассы
на основе информации в наборе результатов, обычно проверяя
значение определенного столбца в результате, известного как [дискриминатор](#term-discriminator).

Полиморфная загрузка в SQLAlchemy подразумевает использование одной или
комбинации трех различных схем для отображения иерархии классов:
«joined», «single» и «concrete». Раздел
[Отображение иерархий классов наследования](orm/inheritance.html) полностью описывает отображение наследования.

primary keyprimary key constraintОграничение, которое уникально определяет характеристики
каждой строки в таблице. Первичный ключ должен состоять из
характеристик, которые не могут быть дублированы другой строкой.
Первичный ключ может состоять из одного атрибута или
нескольких атрибутов в комбинации.
(через Википедию)

Первичный ключ таблицы обычно, хотя и не всегда,
определяется в `CREATE TABLE` [DDL](#term-DDL):

```
CREATE TABLE employee (
 emp\_id INTEGER,
 emp\_name VARCHAR(30),
 dep\_id INTEGER,
 PRIMARY KEY (emp\_id)
)
```

См. также

[composite primary key](#term-composite-primary-key)

[Primary key (через Википедию)](https://en.wikipedia.org/wiki/Primary_Key)

read committedОдин из четырех уровней [изоляции](#term-isolation) базы данных, read committed
обеспечивает, что транзакция не будет иметь доступа к данным из
других параллельных транзакций, которые еще не были подтверждены,
предотвращая так называемые «грязные чтения». Однако при read committed
могут быть неповторяющиеся чтения, что означает, что данные в строке могут измениться
при повторном чтении, если другая транзакция подтвердила изменения.

read uncommittedОдин из четырех уровней [изоляции](#term-isolation) базы данных, read uncommitted
обеспечивает, что изменения, внесенные в данные базы данных в рамках транзакции, неrelationshiprelationshipsСвязующий
элемент между двумя отображаемыми классами, соответствующий
некоторому отношению между двумя таблицами в базе данных.

Отношение определяется с помощью функции SQLAlchemy
[`relationship()`](orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"). После создания
SQLAlchemy
анализирует аргументы и базовые отображения, участвующие
чтобы классифицировать отношение как один из трех типов:
[один ко многим](#term-one-to-many), [многие к одному](#term-many-to-one) или [многие ко многим](#term-many-to-many).
С этой классификацией конструкция отношения
обрабатывает задачу сохранения соответствующих связей
в базе данных в ответ на ассоциации объектов в памяти,
а также задачу загрузки ссылок на объекты и коллекции
в память на основе текущих связей в
базе данных.

См. также

[Конфигурация отношений](orm/relationships.html)

releasereleasesreleasedВ контексте SQLAlchemy термин «выпущенный»
относится к процессу завершения использования конкретного
соединения с базой данных. SQLAlchemy поддерживает использование
пулов соединений, что позволяет настраивать время жизни соединений с базой данных. При использовании пула
соединений процесс «закрытия» соединения, т. е. вызов
оператора типа `connection.close()`, может привести
к тому, что соединение будет возвращено в существующий пул,
или может привести к тому, что будет фактически закрыто
подключение TCP/IP, на которое ссылается это соединение -
какой из них произойдет, зависит от конфигурации, а также
от текущего состояния пула. Поэтому мы используем термин
*выпущенный* вместо того, чтобы означать «сделайте все,
что вам нужно сделать с соединениями, когда мы закончим их использование».

Термин иногда используется в фразе «освобождение
транзакционных ресурсов», чтобы более явно указать, что
мы фактически «освобождаем» любое транзакционное
состояние, которое накопилось на соединении. В большинстве
ситуаций процесс выборки из таблиц, отправки
обновлений и т. д. приобретает [изолированное](#term-isolated) состояние на
этом соединении, а также потенциальные блокировки строк или таблиц.
Это состояние локально для конкретнойВышеуказанное выражение INSERT при выполнении предоставит набор результатов,
который включает значения столбцов `user_account.id` и `user_account.timestamp`, которые должны были быть сгенерированы
как значения по умолчанию, так как они не включены в противном случае (но обратите внимание, что любая серия столбцов
или SQL-выражений может быть помещена в RETURNING, а не только столбцы со значениями по умолчанию).

Серверы, которые в настоящее время поддерживают RETURNING или аналогичную конструкцию, - это PostgreSQL, SQL Server,
Oracle и Firebird. Реализации PostgreSQL и Firebird обычно полнофункциональны, тогда как реализации SQL Server и Oracle
имеют ограничения. В SQL Server этот оператор известен как «OUTPUT INSERTED» для операторов INSERT и UPDATE и «OUTPUT
DELETED» для операторов DELETE; главное ограничение заключается в том, что триггеры не поддерживаются в сочетании с этим
ключевым словом. В Oracle он известен как «RETURNING…INTO» и требует, чтобы значение было помещено в OUT-параметр, что
означает, что синтаксис неуклюжий, и его можно использовать только для одной строки за раз.

Система [`UpdateBase.returning()`](core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
SQLAlchemy предоставляет слой абстракции поверх систем RETURNING этих серверов, чтобы обеспечить согласованный интерфейс
для возврата столбцов. ORM также включает множество оптимизаций, которые используют RETURNING при наличии.

selectable - термин, используемый в SQLAlchemy для описания конструкции SQL, которая представляет собой набор строк. Он
в значительной степени похож на концепцию «отношения» в [реляционной алгебре](#term-relational-algebra). В SQLAlchemy
объекты, которые наследуют
класс [`Selectable`](core/selectable.html#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable"),
считаются пригодными для использования в качестве «selectable» при использовании SQLAlchemy Core. Два наиболее
распространенных конструкта - это [`Table`](core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
и [`Select`](core/selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select").

sentinelinsert sentinel - это специфический для SQLAlchemy термин, который относится
к [`Column`](core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"), который может использоваться для
операции массовой вставки [insertmanyvalues](#term-insertmanyvalues) для отслеживания вставленных записей данных против
строк, переданных обратно с помощью RETURNING или аналогичных. Такая конфигурация столбца необходима для тSerializable
Один из четырех уровней [изоляции](#term-isolation) базы данных, serializable
обладает всей изоляцией [repeatable read](#term-repeatable-read) и, кроме того, в рамках подхода на основе блокировки
гарантирует, что так называемые
"призрачные чтения" не могут произойти; это означает, что строки, которые были вставлены
или удалены в рамках других транзакций, не будут
обнаруживаться в этой транзакции. Строка, которая была прочитана в этой
транзакции, гарантированно продолжает существовать, а строка, которой нет
гарантируется, что она не может появиться из другой
транзакции.

Изоляция Serializable обычно основывается на блокировке строк или диапазонов строк, чтобы достичь этого эффекта, и может
повысить вероятность
взаимоблокировок и ухудшить производительность. Также существуют схемы, не основанные на блокировке, однако они
обязательно отклоняют транзакции, если
обнаруживаются коллизии записи.

Session Контейнер или область для операций ORM с базой данных. Сессии
загружают экземпляры из базы данных, отслеживают изменения в отображенных
экземплярах и сохраняют изменения в единице работы при
flushed.

См. также

[Использование сессии](orm/session.html)

subqueryscalar subquery Относится к оператору `SELECT`, встроенному во внешний
`SELECT`.

Подзапросы бывают двух типов: "скалярный подзапрос", который должен вернуть ровно одну строку и один столбец, и "
производная таблица", которая служит источником строк для оператора FROM другого оператора SELECT. Скалярный подзапрос
может быть размещен в [WHERE clause](#term-WHERE-clause), [columns clause](#term-columns-clause),
ORDER BY clause или HAVING clause внешнего оператора SELECT, тогда как
производная таблица может быть размещена в операторе FROM внешнего `SELECT`.

Примеры:

1. скалярный подзапрос, размещенный в [columns clause](#term-columns-clause) внешнего
   `SELECT`. В этом примере подзапрос является [коррелированным подзапросом](#term-correlated-subquery), потому что
   часть
   строк, которые он выбирает, задаются через внешний оператор.

```
SELECT id, (SELECT name FROM address WHERE address.user\_id=user.id)
FROM user
```

2. скалярный подзапрос, размещограничение уникальности, уникальный ключ, индекс
   Уникальный ключ или индекс может уникально идентифицировать каждую строку данных в таблице базы данных. Уникальный
   ключ или индекс может состоять из одного столбца или набора столбцов в одной таблице базы данных. Если не
   используются значения NULL, то никакие две разные строки или записи данных в таблице базы данных не могут иметь
   одинаковое значение данных (или комбинацию значений данных) в этих столбцах уникального ключа или индекса. В
   зависимости от ее конструкции, таблица базы данных может иметь много уникальных ключей или индексов, но не более
   одного первичного ключа или индекса.

См. также

[Уникальный ключ (через Википедию)](https://ru.wikipedia.org/wiki/%D0%A3%D0%BD%D0%B8%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%BA%D0%BB%D1%8E%D1%87#%D0%9E%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D1%83%D0%BD%D0%B8%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9)

единица работы
Архитектура программного обеспечения, в которой система сохранения, такая как объектно-реляционный отображатель,
поддерживает список изменений, внесенных в ряд объектов, и периодически сбрасывает все эти ожидающие изменения в базу
данных.

`Session` SQLAlchemy [`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") реализует шаблон
единицы работы, где объекты, добавленные
в [`Session`](orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") с использованием методов, таких
как [`Session.add()`](orm/session_api.html#sqlalchemy.orm.Session.add "sqlalchemy.orm.Session.add"), будут участвовать в
сохранении в стиле единицы работы.

Для примера того, как выглядит сохранение единицы работы в SQLAlchemy, начните с
раздела [Манипулирование данными с ORM](tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation)
в [SQLAlchemy Unified Tutorial](tutorial/index.html#unified-tutorial). Затем для получения более подробной информации
см. [Основы использования сеанса](orm/session_basics.html#id1) в общей справочной документации.

См. также

[Единица работы (через Martin Fowler)](https://martinfowler.com/eaaCatalog/unitOfWork.html)

[Манипулирование данными с ORM](tutorial/