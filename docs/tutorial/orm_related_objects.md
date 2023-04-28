title: Работа с объектами, связанными с ORM

!!! warning

    Этот раздел не редактировался людьми, возможны ошибки и неточности в форматировании, вы можете помочь исправив и сделав pull request


## Работа с объектами, связанными с ORM {#working-with-orm-related-objects}

В этом разделе мы рассмотрим еще один важный концепт ORM, а именно, как ORM взаимодействует с отображаемыми классами, которые ссылается на другие объекты. В разделе [Объявление отображаемых классов](metadata.html#tutorial-declaring-mapped-classes) примеры отображаемых классов использовали конструкцию, называемую [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"). Эта конструкция определяет связь между двумя разными отображаемыми классами или отображаемым классом самого себя, последнее из которых называется **самореференциальной** связью.

Чтобы описать основную идею [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), сначала мы рассмотрим отображение в краткой форме, опуская отображения [`mapped_column()`](../orm/mapping_api.html#sqlalchemy.orm.mapped_column "sqlalchemy.orm.mapped_column") и другие директивы:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


class User(Base):
    \_\_tablename\_\_ = "user\_account"

    # ... отображения mapped\_column()

    addresses: Mapped[List["Address"]] = relationship(back\_populates="user")


class Address(Base):
    \_\_tablename\_\_ = "address"

    # ... отображения mapped\_column()

    user: Mapped["User"] = relationship(back\_populates="addresses")
```

Выше класс `User` теперь имеет атрибут `User.addresses`, а класс `Address` имеет атрибут `Address.user`. Конструкция [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), в сочетании с конструкцией [`Mapped`](../orm/internals.html#sqlalchemy.orm.Mapped "sqlalchemy.orm.Mapped") для указания поведения типизации, будет использоваться для анализа отношений таблиц между объектами [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), которые отображаются на классы `User` и `Address`. Поскольку объект [`Table`](../core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"), представляющий таблицу `address`, имеет [`ForeignKeyConstraint`](../core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint"), который ссылается на таблицу `user_account`, [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") может однозначно определить, что существует [один ко многим](../glossary.html#term-one-to-many) отношение от `User.addresses` к `User`; одна конкретная строка в таблице `user_account` может быть ссылкой на многие строки в таблице `address`.

Все одно-ко-многим отношения естественным образом соответствуют [многим к одному](../glossary.html#term-many-to-one) отношению в другом направлении, в данном случае отношению, указанному в `Address.user`. Параметр```
>>> u1 = User(name="pkrabs", fullname="Pearl Krabs")
>>> u1.addresses
[]

```

Этот объект является специфичной для SQLAlchemy версией списка Python, который имеет возможность отслеживать и реагировать на изменения, внесенные в него. Коллекция также появилась автоматически, когда мы получили доступ к атрибуту, даже если мы никогда не присваивали ее объекту. Это аналогично поведению, отмеченному в [Вставка строк с использованием шаблона Unit of Work ORM](orm_data_manipulation.html#tutorial-inserting-orm), где было отмечено, что атрибуты, основанные на столбцах, которым мы явно не присваиваем значение, также автоматически отображаются как `None`, а не вызывают `AttributeError`, как это обычно происходит в Python.


Поскольку объект `u1` все еще [временный](../glossary.html#term-transient), а `list`, который мы получили из `u1.addresses`, не был изменен (т.е. не был добавлен или расширен), он на самом деле еще не связан с объектом, но по мере изменения его состояния он станет частью состояния объекта `User`.


Коллекция специфична для класса `Address`, который является единственным типом объекта Python, который может быть сохранен в ней. Используя метод `list.append()`, мы можем добавить объект `Address`:


```
>>> a1 = Address(email_address="pearl.krabs@gmail.com")
>>> u1.addresses.append(a1)

```

На этом этапе коллекция `u1.addresses`, как и ожидалось, содержит новый объект `Address`:


```
>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com')]

```

Поскольку мы связали объект `Address` с коллекцией `User.addresses` экземпляра `u1`, произошло также другое поведение, а именно, что отношение `User.addresses` синхронизировалось с отношением `Address.user`, так что мы можем перемещаться не только от объекта `User` к объекту `Address`, но также можем перемещаться от объекта `Address` обратно к «родительскому» объекту `User`:


```
>>> a1.user
User(id=None, name='pkrabs', fullname='Pearl Krabs')

```

Эта синхронизация произошла в результате использования параметра [`relationship.back_populates`](../orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship") между двумя объектами [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"). Этот параметр называет другой [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), для которого должно происходить взУ нас теперь есть объекты `User` и два объекта `Address`, которые связаны в двунаправленной структуре в памяти, но, как отмечено ранее в [Вставка строк с использованием шаблона ORM Unit of Work](orm_data_manipulation.html#tutorial-inserting-orm), эти объекты находятся в [переходном](../glossary.html#term-transient) состоянии, пока они не будут связаны с объектом [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session").

Мы используем [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), который все еще активен, и отмечаем, что когда мы применяем метод [`Session.add()`](../orm/session_api.html#sqlalchemy.orm.Session.add "sqlalchemy.orm.Session.add") к объекту `User`, связанный объект `Address` также добавляется в эту же [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"):

```
>>> session.add(u1)
>>> u1 in session
True
>>> a1 in session
True
>>> a2 in session
True

```

Вышеуказанное поведение, при котором [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") получил объект `User` и следовал по отношению `User.addresses`, чтобы найти связанный объект `Address`, известно как **каскад сохранения-обновления** и подробно обсуждается в документации по ORM в разделе [Каскады](../orm/cascades.html#unitofwork-cascades).

Три объекта теперь находятся в [ожидающем](../glossary.html#term-pending) состоянии; это означает, что они готовы к вставке, но это еще не произошло; у всех трех объектов еще нет первичного ключа, и, кроме того, у объектов `a1` и `a2` есть атрибут `user_id`, который ссылается на [`Column`](../core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"), который имеет [`ForeignKeyConstraint`](../core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint"), относящийся к столбцу `user_account.id`; они также равны `None`, так как объекты еще не связаны с реальной строкой базы данных:

```
>>> print(u1.id)
None
>>> print(a1.user_id)
None

```

Именно на этом этапе мы можем увидеть очень большую полезность процесса единицы работы; напомним, что в разделе [INSERT usually generates the “values” clause automatically](data_insert.html#tutorial-core-insert-values-clause) строки вставлялись в таблицы `user_account` и `address` с использованием некоторых сложных синтаксисов, чтобы автоматически связать столбцы `address.user_id` с теми из строк `user_account`. Кроме того, было необходимо, чтобы мы сначала вставляли строки `user_account`, а зат```
>>> session.commit()
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('pkrabs', 'Pearl Krabs')
INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
[... (insertmanyvalues) 1/2 (ordered; batch not supported)] ('pearl.krabs@gmail.com', 6)
INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
[insertmanyvalues 2/2 (ordered; batch not supported)] ('pearl@aol.com', 6)
COMMIT


```


### Загрузка отношений {#tutorial-loading-relationships} 


В последнем шаге мы вызвали [`Session.commit()`](../orm/session_api.html#sqlalchemy.orm.Session.commit "sqlalchemy.orm.Session.commit"), который выполнил COMMIT
для транзакции, а затем, в соответствии с параметром
[`Session.commit.expire_on_commit`](../orm/session_api.html#sqlalchemy.orm.Session.commit.params.expire_on_commit "sqlalchemy.orm.Session.commit"), истекли все объекты, чтобы
они обновились для следующей транзакции.


Когда мы следующий раз обратимся к атрибуту этих объектов, мы увидим SELECT,
выполненный для первичных атрибутов строки, например, когда мы просматриваем
новый сгенерированный первичный ключ для объекта `u1`:


```
>>> u1.id
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (6,)
6

```

У объекта `u1` теперь есть постоянная коллекция `User.addresses`,
к которой мы также можем обратиться. Поскольку эта коллекция состоит из
дополнительного набора строк из таблицы `address`, когда мы обращаемся к этой коллекции,
мы снова видим [ленивую загрузку](../glossary.html#term-lazy-load), чтобы получить объекты:


```
>>> u1.addresses
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (6,)
[Address(id=4, email_address='pearl.krabs@gmail.com'), Address(id=5, email_address='pearl@aol.com')]

```

Коллекции и связанные атрибуты в SQLAlchemy ORM являются постоянными в
памяти; после того, как коллекция или атрибут заполнены, SQL больше не
выполняется, пока эта коллекция или атрибут не будут [истекши](../glossary.html#term-expired). Мы можем обратиться
к `u1.addresses` снова, а также добавлять или удалять элементы, и это не
приведет к новым вызовам SQL:


```
>>> u1.addresses
[Address(id=4, email_address='pearl.krabs@gmail.com'), Address(id=5, email_address='pearl@aol.com')]

```

Хотя загрузка, вызываемая ленивой### Использование отношений в запросах {#tutorial-select-relationships}

Предыдущий раздел представил поведение конструкции [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") при работе с **экземплярами отображаемого класса**, такими как `u1`, `a1` и `a2` экземпляры классов `User` и `Address`. В этом разделе мы представляем поведение [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") в отношении **поведения на уровне класса отображаемого класса**, где он служит нескольким способам для автоматизации создания SQL-запросов.

#### Использование отношений для объединения {#tutorial-joining-relationships}

Разделы [Явные FROM-клаузы и JOIN-ы](data_select.html#tutorial-select-join) и [Установка ON-клаузы](data_select.html#tutorial-select-join-onclause) представили использование методов [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join") и [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from") для составления SQL JOIN-клауз. Чтобы описать, как объединять таблицы, эти методы либо **выводят** ON-клаузу на основе наличия единственного неоднозначного объекта [`ForeignKeyConstraint`](../core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint") в структуре метаданных таблицы, связывающей две таблицы, либо мы можем предоставить явный конструкт SQL Expression, который указывает на конкретную ON-клаузу.

При использовании сущностей ORM доступен дополнительный механизм, который помогает нам настроить ON-клаузу объединения, а именно использование объектов [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), которые мы настроили в нашем отображении пользователя, как было продемонстрировано в разделе [Объявление отображаемых классов](metadata.html#tutorial-declaring-mapped-classes). Атрибут, связанный с классом, соответствующий [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"), может быть передан как **единственный аргумент** в [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join"), где он служит для указания как правой стороны объединения, так и ON-клаузы сразу же:

```
>>> print(select(Address.email_address).select_from(User).join(User.addresses))
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id


```

Наличие объекта ORM [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") в отображении не используется [`Select.join()`](../core/selectableСмотрите раздел [Joins](../orm/queryguide/select.html#orm-queryguide-joins) в [ORM Querying Guide](../orm/queryguide/index.html) для получения множества примеров использования [`Select.join()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join "sqlalchemy.sql.expression.Select.join") и [`Select.join_from()`](../core/selectable.html#sqlalchemy.sql.expression.Select.join_from "sqlalchemy.sql.expression.Select.join_from") с конструкциями [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship").

Смотрите также

[Joins](../orm/queryguide/select.html#orm-queryguide-joins) в [ORM Querying Guide](../orm/queryguide/index.html)

#### Операторы WHERE для отношений {#tutorial-relationship-operators}


Существуют дополнительные варианты генерации SQL-запросов, которые поставляются с [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") и обычно полезны при создании
WHERE-выражения. Смотрите раздел [Операторы WHERE для отношений](../orm/queryguide/select.html#orm-queryguide-relationship-operators) в [ORM Querying Guide](../orm/queryguide/index.html).

Смотрите также

[Операторы WHERE для отношений](../orm/queryguide/select.html#orm-queryguide-relationship-operators) в [ORM Querying Guide](../orm/queryguide/index.html)


### Стратегии загрузки {#tutorial-orm-loader-strategies}


В разделе [Loading Relationships](#tutorial-loading-relationships) мы представили концепцию
того, что при работе с экземплярами отображаемых объектов доступ к атрибутам,
которые отображаются с помощью [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") в стандартном случае, вызовет
[ленивую загрузку](../glossary.html#term-lazy-load), когда коллекция не заполнена, чтобы загрузить
объекты, которые должны быть присутствовать в этой коллекции.


Ленивая загрузка - один из самых известных шаблонов ORM и, вероятно, самый
контроверсиальный. Когда в памяти находится несколько десятков ORM-объектов, каждый из которых ссылается на
несколько незагруженных атрибутов, рутинная манипуляция этими объектами может
вызвать множество дополнительных запросов, которые могут накапливаться (иначе
известно как [проблема N+1](../glossary.html#term-N-plus-one-problem)), и, что еще хуже, они генерируются
неявно. Эти неявные запросы могут не быть замечены, могут вызывать ошибки,
когда они попытаются выполниться после того, как транзакция базы данных больше не доступна,
или при использовании альтернативных подходов к параллелизму```
Для объекта пользователя в session.execute(
    select(User).options(selectinload(User.addresses))
).scalars():
    user_obj.addresses  # доступ к уже загруженной коллекции адресов
```


Они также могут быть настроены как значения по умолчанию для [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") с использованием
опции [`relationship.lazy`](../orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship"), например:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


class User(Base):
    \_\_tablename\_\_ = "user\_account"

    addresses: Mapped[List["Address"]] = relationship(
        back\_populates="user", lazy="selectin"
    )
```


Каждый объект стратегии загрузки добавляет какой-то вид информации в выражение, которое
будет использоваться позже [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") при принятии решения о том, как различные
атрибуты должны быть загружены и/или как они должны вести себя при доступе к ним.


Ниже приведены несколько наиболее часто используемых
стратегий загрузки.

Смотрите также


Два раздела в [Техниках загрузки отношений](../orm/queryguide/relationships.html):


* [Настройка стратегий загрузки во время отображения](../orm/queryguide/relationships.html#relationship-lazy-option) - подробности о настройке стратегии
на [`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
* [Загрузка отношений с параметрами загрузчика](../orm/queryguide/relationships.html#relationship-loader-options) - подробности об использовании стратегий загрузки на этапе запроса


#### Selectin Load 


Самый полезный загрузчик в современном SQLAlchemy это
опция загрузчика [`selectinload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.selectinload "sqlalchemy.orm.selectinload"). Эта опция решает наиболее распространенную
форму проблемы "N plus one", которая заключается в том, что набор объектов ссылается
на связанные коллекции. [`selectinload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.selectinload "sqlalchemy.orm.selectinload") гарантирует, что определенная
коллекция для полного набора объектов будет загружена заранее с помощью одного
запроса. Он делает это с помощью формы SELECT, которая в большинстве случаев может быть
выпущена только против связанной таблицы, без введения JOIN или
подзапросов, и запрашивает только те родительские объекты, для которых
коллекция еще не загружена. Ниже мы иллюстрируем [`selectinload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.selectinload "sqlalchemy.orm.selectinload")
загрузкой всех объектов `User` и всех связанных```
>>> from sqlalchemy.orm import selectinload
>>> stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
>>> for row in session.execute(stmt):
...     print(
...         f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})"
...     )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
SELECT address.user_id AS address_user_id, address.id AS address_id,
address.email_address AS address_email_address
FROM address
WHERE address.user_id IN (?, ?, ?, ?, ?, ?)
[...] (1, 2, 3, 4, 5, 6)
spongebob  (spongebob@sqlalchemy.org)
sandy  (sandy@sqlalchemy.org, sandy@squirrelpower.org)
patrick  ()
squidward  ()
ehkrabs  ()
pkrabs  (pearl.krabs@gmail.com, pearl@aol.com)

```


Смотрите также


[Выборка с IN-загрузкой](../orm/queryguide/relationships.html#selectin-eager-loading) - в [Техники загрузки связей](../orm/queryguide/relationships.html)

#### Joined Load 


Стратегия жадной загрузки [`joinedload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload") является самой старой стратегией загрузки в SQLAlchemy, которая дополняет передаваемый в базу данных оператор SELECT соединением (которое может быть внешним или внутренним соединением в зависимости от параметров), которое может загружать связанные объекты.


Стратегия [`joinedload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload") наилучшим образом подходит для загрузки связанных объектов многие-к-одному, поскольку для этого требуется только добавить дополнительные столбцы к строке первичной сущности, которая была бы выбрана в любом случае. Для большей эффективности она также принимает параметр [`joinedload.innerjoin`](../orm/queryguide/relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload"), чтобы использовать внутреннее соединение вместо внешнего соединения, как в случае ниже, где мы знаем, что все объекты `Address` имеют связанный `User`:


```
>>> from sqlalchemy.orm import joinedload
>>> stmt = (
...     select(Address)
...     .options(joinedload(Address.user, innerjoin=True))
...     .order_by(Address.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.Address.email_address} {row.Address.user.name}")
SELECT address.id, address.email_address, address.user_id, user_account_1.id AS id_1,
user_account_1.name, user_account_1.fullname
FROM address
JOIN user_account AS user_account_1 ON user_account_1.id = address.user_id
ORDER BY address.id
[...] ()
spongebob@sqlalchemy.org spongebob
sandy@sqlalchemy.org sandy
sandy@squirrelpower.org sandy
pearl.krabs@gmail.com pkrabs
pearl@aol.com pkrabs

```

[`joinedload()`](../orm/queryguide/relationships.html#Важно отметить, что критерии WHERE и ORDER BY внешнего выражения Select не направлены на таблицу, отображаемую joinedload(). В SQL выше можно увидеть, что к таблице user_account применяется анонимный псевдоним, который не может быть напрямую адресован в запросе. Эта концепция подробно рассматривается в разделе The Zen of Joined Eager Loading.

Совет

Важно отметить, что многие к eager-загрузкам связей многие-к-одному часто не нужны, так как проблема "N plus one" гораздо менее распространена в общем случае. Когда многие объекты ссылаются на один и тот же связанный объект, например, многие объекты Address, каждый из которых ссылается на один и тот же объект User, SQL будет генерироваться только один раз для этого объекта User с использованием обычной ленивой загрузки. Процедура ленивой загрузки будет искать связанный объект по первичному ключу в текущей сессии Session без генерации SQL, когда это возможно.

См. также

Joined Eager Loading - в Relationship Loading Techniques

#### Явное объединение + Eager load {#tutorial-orm-loader-strategies-contains-eager}

Если мы загружаем строки Address, объединяя их с таблицей user_account, используя метод, такой как Select.join(), чтобы отобразить JOIN, мы также можем использовать этот JOIN, чтобы предварительно загрузить содержимое атрибута Address.user на каждом возвращенном объекте. Это по существу то, что мы используем "joined eager loading", но рендерим JOIN сами. Этот распространенный случай использования достигается с помощью опции contains_eager(). Эта опция очень похожа на joinedload(), за исключением того, что она предполагает, что мы настроили JOIN сами, и вместо этого указывает, что в каждый возвращенный объект должны быть загружены дополнительные столбцы в COLUMNS, например:

```
>>> from sqlalchemy.orm import contains_eager
>>> stmt = (
...     select(Address)
...     .join(Address.user)
...     .where(User.name == "pkrabs")
...     .options(contains_eager(Address.user))
...     .order_by(Address.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.Address.email_address} {row.Address.user.name}")
SELECT user_account.id, user_account.name, user_account.fullname,
address.id AS id_1, address.email_address, address.user_id
FROM address JOIN user_account ON user_account.id = address.user_id
WHERE user_account.name = ? ORDER BY address.id
[...] ('pkrabs',)
pearl.krabs@gmail.com pkrabs
pearl@aol.com pkrabs

```

Выше мы фильтровали строки по user_account.name и загружали строки из user_account в атрибут Address.user возвращаемых строк. Если бы мы применили joined```
>>> stmt = (
...     select(Address)
...     .join(Address.user)
...     .where(User.name == "pkrabs")
...     .options(joinedload(Address.user))
...     .order_by(Address.id)
... )
>>> print(stmt)  # SELECT имеет JOIN и LEFT OUTER JOIN, которые не нужны
SELECT address.id, address.email_address, address.user_id,
user_account_1.id AS id_1, user_account_1.name, user_account_1.fullname
FROM address JOIN user_account ON user_account.id = address.user_id
LEFT OUTER JOIN user_account AS user_account_1 ON user_account_1.id = address.user_id
WHERE user_account.name = :name_1 ORDER BY address.id


```


Смотрите также


Два раздела в [Техники загрузки отношений](../orm/queryguide/relationships.html):


* [Zen of Joined Eager Loading](../orm/queryguide/relationships.html#zen-of-eager-loading) - подробно описывает вышеупомянутую проблему
* [Routing Explicit Joins/Statements into Eagerly Loaded Collections](../orm/queryguide/relationships.html#contains-eager) - использование [`contains_eager()`](../orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")

#### Raiseload 


Одна дополнительная стратегия загрузки, которую стоит упомянуть, - [`raiseload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload").
Этот параметр используется для полного блокирования приложения от проблемы
[N plus one](../glossary.html#term-N-plus-one), вызывая ошибку вместо того, чтобы выполнять ленивую
загрузку. У него есть две вариации, которые управляются через
опцию [`raiseload.sql_only`](../orm/queryguide/relationships.html#sqlalchemy.orm.raiseload.params.sql_only "sqlalchemy.orm.raiseload"), чтобы блокировать либо ленивую загрузку,
которая требует SQL, либо все операции «загрузки», включая те, которые
только нужно проверить в текущей [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session").


Один из способов использования [`raiseload()`](../orm/queryguide/relationships.html#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload") - настроить его на
[`relationship()`](../orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") самостоятельно, установив [`relationship.lazy`](../orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")
на значение `"raise_on_sql"`, так что для определенного
отображения определенное отношение никогда не будет пытаться генерировать SQL:


```
>>> from sqlalchemy.orm import Mapped
>>> from sqlalchemy.orm import relationship


>>> class User(Base):
...     __tablename__ = "user_account"
...     id: Mapped[int] = mapped_column(primary_key=True)
...     addresses: Mapped[List["Address"]] = relationship(
...         back_populates="user", lazy="raise_on_sql"
...     )


>>> class Address(Base):
...     __tablename__ = "address"
...     id: Mapped[int] = mapped_column(primary_key=True)
...     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
...    ```
>>> u1 = (
...     session.execute(select(User).options(selectinload(User.addresses)))
...     .scalars()
...     .first()
... )
SELECT user_account.id
FROM user_account
[...] ()
SELECT address.user_id AS address_user_id, address.id AS address_id
FROM address
WHERE address.user_id IN (?, ?, ?, ?, ?, ?)
[...] (1, 2, 3, 4, 5, 6)


```

Опция `lazy="raise_on_sql"` пытается быть умной и в отношениях многие-к-одному; выше, если атрибут `Address.user` объекта `Address` не был загружен, но объект `User` был локально присутствующим в той же [`Session`](../orm/session_api.html#sqlalchemy.orm.Session), стратегия "raiseload" не вызовет ошибку.

Смотрите также


[Предотвращение нежелательной ленивой загрузки с помощью raiseload](../orm/queryguide/relationships.html#prevent-lazy-with-raiseload) - в [Техниках загрузки отношений](../orm/queryguide/relationships.html)