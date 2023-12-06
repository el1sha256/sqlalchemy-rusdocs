title: Манипуляции с данными с помощью ORM

!!! warning

    Этот раздел не редактировался людьми, возможны ошибки и неточности в форматировании, вы можете помочь исправив и сделав pull request

## Манипуляции с данными с помощью ORM {#data-manipulation-with-the-orm}

Предыдущий раздел [Работа с данными](data.html#tutorial-working-with-data) был сосредоточен на языке выражений SQL с точки зрения Core, чтобы обеспечить непрерывность между основными конструкциями операторов SQL. В этом разделе будет рассмотрен жизненный цикл [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") и то, как он взаимодействует с этими конструкциями.

**Предварительные разделы** - раздел, посвященный ORM, основан на двух предыдущих разделах ORM-центрической части этого документа:

* [Выполнение с помощью сеанса ORM](dbapi_transactions.html#tutorial-executing-orm-session) - вводит способ создания объекта ORM [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session")
* [Использование ORM-декларативных форм для определения метаданных таблицы](metadata.html#tutorial-orm-table-metadata) - где мы настраиваем наши отображения ORM для сущностей `User` и `Address`
* [Выбор ORM-сущностей и столбцов](data_select.html#tutorial-selecting-orm-entities) - несколько примеров того, как запускать операторы SELECT для сущностей, таких как `User`

### Вставка строк с использованием шаблона ORM Unit of Work {#tutorial-inserting-orm}

При использовании ORM объект [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") отвечает за создание конструкций [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert") и их эмиссию в виде операторов INSERT в рамках текущей транзакции. Способ, которым мы указываем [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") это сделать, заключается в **добавлении** записей объектов в него; [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") затем гарантирует, что эти новые записи будут выведены в базу данных, когда они будут нужны, с помощью процесса, известного как **flush**. Общий процесс, используемый [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") для сохранения объектов, известен как шаблон [unit of work](../glossary.html#term-unit-of-work).

#### Экземпляры классов представляют строки

В то время как в предыдущем примере мы выводили оператор INSERT, используя словари Python, чтобы указать данные, которые мы хотели добавить, с ORM мы непосредственно используем определенные нами пользовательские классы Python, возвращаясь к разделу [Использование ORM-декларативных форм для определения метаданных таблицы](metadata.html#tutorial-orm-table-metadata). На уровнеАналогично нашим примерам ядра [`Insert`](../core/dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert"), мы не включили первичный ключ (т. е. запись для столбца `id`), поскольку мы хотим воспользоваться функцией автоматического инкремента первичного ключа базы данных, в данном случае SQLite, которую также интегрирует ORM. Значение атрибута `id` на приведенных выше объектах, если бы мы его просмотрели, отображается как `None`:

```
>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')
```


Значение `None` предоставляется SQLAlchemy для указания того, что атрибут еще не имеет значения. Отображаемые в Python атрибуты, отображаемые SQLAlchemy, всегда возвращают значение и не вызывают `AttributeError`, если они отсутствуют, при работе с новым объектом, которому еще не было присвоено значение.


В настоящее время наши два объекта выше находятся в состоянии, называемом [transient](../glossary.html#term-transient) - они не связаны с каким-либо состоянием базы данных и еще не связаны с объектом [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), который может генерировать для них операторы INSERT.


#### Добавление объектов в сеанс 


Чтобы проиллюстрировать процесс добавления пошагово, мы создадим
[`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") без использования менеджера контекста (и, следовательно, мы должны
убедиться, что закроем его позже!):

```
>>> session = Session(engine)
```


Затем объекты добавляются в [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") с использованием
метода [`Session.add()`](../orm/session_api.html#sqlalchemy.orm.Session.add "sqlalchemy.orm.Session.add"). Когда это вызывается, объекты находятся в состоянии
известном как [pending](../glossary.html#term-pending) и еще не были вставлены:

```
>>> session.add(squidward)
>>> session.add(krabs)
```

Когда у нас есть ожидающие объекты, мы можем увидеть это состояние, посмотрев на коллекцию на [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), называемую [`Session.new`](../orm/session_api.html#sqlalchemy.orm.Session.new "sqlalchemy.orm.Session.new"):

```
>>> session.new
```
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])


Вышеуказанный вид использует коллекцию `IdentitySet`, которая
существенно является множеством Python, хеширующим по ид
```
>>> session.flush()
```
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[... (insertmanyvalues) 1/2 (ordered; batch not supported)] ('squidward', 'Squidward Tentacles')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 2/2 (ordered; batch not supported)] ('ehkrabs', 'Eugene H. Krabs')


Здесь мы видим, что [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") был вызван для генерации SQL-запроса,
таким образом, он создал новую транзакцию и выполнил соответствующие операторы INSERT
для двух объектов. Транзакция теперь **остается открытой** до тех пор, пока мы не вызовем любой
из методов [`Session.commit()`](../orm/session_api.html#sqlalchemy.orm.Session.commit "sqlalchemy.orm.Session.commit"), [`Session.rollback()`](../orm/session_api.html#sqlalchemy.orm.Session.rollback "sqlalchemy.orm.Session.rollback"), или
[`Session.close()`](../orm/session_api.html#sqlalchemy.orm.Session.close "sqlalchemy.orm.Session.close") объекта [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session").


Хотя [`Session.flush()`](../orm/session_api.html#sqlalchemy.orm.Session.flush "sqlalchemy.orm.Session.flush") может использоваться для ручной отправки ожидающих
изменений в текущую транзакцию, это обычно не требуется, так как
[`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") имеет поведение, известное как **автоочистка**, которое
будет проиллюстрировано позже. Он также очищает изменения, когда
вызывается [`Session.commit()`](../orm/session_api.html#sqlalchemy.orm.Session.commit "sqlalchemy.orm.Session.commit").


#### Автоматически сгенерированные атрибуты первичного ключа 


После вставки строк созданные нами два объекта Python находятся в состоянии, известном как [persistent](../glossary.html#term-persistent), где они связаны с
объектом [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), в котором они были добавлены или загружены, и имеют много
других функций, которые будут рассмотрены позже.


Еще одним эффектом INSERT, который произошел, является то, что ORM извлекла
новые идентификаторы первичных ключей для каждого нового объекта; внутренне она обычно использует
тот же доступор [`CursorResult.inserted_primary_key`](../core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key "sqlalchemy.engine.CursorResult.inserted_primary_key"), который мы
введены ранее. Теперь у объектов `squidward` и `krabs` есть эти новые
идентификаторы первичных ключей, связанные с ними, и мы можем просмотреть их, обратившисьПочему ORM генерирует два отдельных оператора INSERT, когда она могла бы использовать [executemany](dbapi_transactions.html#tutorial-multiple-parameters)? Как мы увидим в следующем разделе, при сохранении объектов в [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") всегда необходимо знать первичный ключ только что вставленных объектов. Если используется функция, такая как автоинкремент SQLite (другие примеры включают PostgreSQL IDENTITY или SERIAL, использование последовательностей и т. д.), то функция [`CursorResult.inserted_primary_key`](../core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key "sqlalchemy.engine.CursorResult.inserted_primary_key") обычно требует, чтобы каждый INSERT был отправлен по одной строке. Если мы предоставили значения для первичных ключей заранее, ORM смогла бы оптимизировать операцию лучше. Некоторые базы данных, такие как [psycopg2](../dialects/postgresql.html#postgresql-psycopg2), также могут вставлять множество строк за один раз, сохраняя возможность извлечения значений первичных ключей.

#### Получение объектов по первичному ключу из карты идентичности

Первичный ключ объектов важен для [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), поскольку объекты теперь связаны с этим идентификатором в памяти с использованием функции, известной как [карта идентичности](../glossary.html#term-identity-map). Карта идентичности - это хранилище в памяти, которое связывает все объекты, загруженные в память, с их первичным ключом. Мы можем наблюдать это, извлекая один из вышеуказанных объектов с помощью метода [`Session.get()`](../orm/session_api.html#sqlalchemy.orm.Session.get "sqlalchemy.orm.Session.get"), который вернет запись из карты идентичности, если она находится локально, в противном случае будет отправлен запрос SELECT:

```
>>> some\_squidward = session.get(User, 4)
>>> some\_squidward
User(id=4, name='squidward', fullname='Squidward Tentacles')
```

Важно отметить, что карта идентичности поддерживает **уникальный экземпляр** конкретного объекта Python для конкретного идентификатора базы данных в рамках конкретного объекта [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"). Мы можем заметить, что `some_squidward` ссылается на **тот же объект**, что и `squidward` ранее:

```
>>> some\_squidward is squidward
True
```

Карта идентичности - это критическая функция, которая позволяет манипулировать сложными наборами объектов в рамках тВажно отметить, что атрибуты объектов, с которыми мы только что работали, были [истекшие](../glossary.html#term-expired), что означает, что при следующем доступе к любым атрибутам на них [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") начнет новую транзакцию и перезагрузит их состояние. Этот вариант иногда проблематичен как по причине производительности, так и если вы хотите использовать объекты после закрытия [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") (что известно как [отсоединенное](../glossary.html#term-detached) состояние), так как они не будут иметь никакого состояния и не будут иметь [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), с помощью которой можно загрузить это состояние, что приведет к ошибкам "отсоединенного экземпляра". Поведение можно контролировать с помощью параметра [`Session.expire_on_commit`](../orm/session_api.html#sqlalchemy.orm.Session.params.expire_on_commit "sqlalchemy.orm.Session"). Больше об этом можно узнать в разделе [Закрытие сессии](#tutorial-orm-closing).


### Обновление ORM-объектов с использованием шаблона Unit of Work {#tutorial-orm-updating}


В предыдущем разделе [Использование операторов UPDATE и DELETE](data_update.html#tutorial-core-update-delete) мы представили конструкцию [`Update`](../core/dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update"), которая представляет оператор SQL UPDATE. При использовании ORM есть два способа использования этой конструкции. Основной способ заключается в том, что он автоматически генерируется в рамках [единицы работы](../glossary.html#term-unit-of-work), используемой [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), где оператор UPDATE генерируется на основе первичного ключа, соответствующего отдельным объектам, которые имеют изменения на них.


Предположим, что мы загрузили объект `User` для имени пользователя `sandy` в транзакцию (также демонстрируя метод [`Select.filter_by()`](../core/selectable.html#sqlalchemy.sql.expression.Select.filter_by "sqlalchemy.sql.expression.Select.filter_by") и метод [`Result.scalar_one()`](../core/connections.html#sqlalchemy.engine.Result.scalar_one "sqlalchemy.engine.Result.scalar_one")):


```
>>> sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('sandy',)


```

Python-объект `sandy`, как упоминалось ранее, действует как **прокси** для строки в базе данных, более конкретно, строкКогда [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") следующий раз вызывает `flush`, будет выполнено обновление этого значения в базе данных. Как упоминалось ранее, `flush` происходит автоматически перед тем, как мы выполняем любой `SELECT`, используя поведение, известное как **autoflush**. Мы можем запросить напрямую столбец `User.fullname` из этой строки, и мы получим обновленное значение обратно:


```
>>> sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
UPDATE user_account SET fullname=? WHERE user_account.id = ?
[...] ('Sandy Squirrel', 2)
SELECT user_account.fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
>>> print(sandy_fullname)
Sandy Squirrel

```

Мы видим выше, что мы запросили, чтобы [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") выполнить один оператор [`select()`](../core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"). Однако, SQL, который был выполнен, показывает, что было выполнено обновление, которое было процессом `flush`, выталкивающим ожидающие изменения. Объект Python `sandy` теперь больше не считается грязным:

```
>>> sandy in session.dirty
False
```


Однако, обратите внимание, что мы **все еще в транзакции**, и наши изменения не были отправлены в постоянное хранилище базы данных. Поскольку фамилия Сэнди на самом деле "Cheeks", а не "Squirrel", мы исправим эту ошибку позже, когда откатим транзакцию. Но сначала мы внесем еще несколько изменений в данные.

Смотрите также


[Flushing](../orm/session_basics.html#session-flushing) - детали процесса `flush`, а также информация о настройке [`Session.autoflush`](../orm/session_api.html#sqlalchemy.orm.Session.params.autoflush "sqlalchemy.orm.Session").

### Удаление ORM-объектов с использованием шаблона Unit of Work {#tutorial-orm-deleting} 


Для завершения основных операций сохранения, отдельный ORM-объект может быть помечен для удаления в процессе [Unit of Work](../glossary.html#term-unit-of-work) с помощью метода [`Session.delete()`](../orm/session_api.html#sqlalchemy.orm.Session.delete "sqlalchemy.orm.Session.delete"). Давайте загрузим `patrick` из базы данных:


```
>>> patrick = session.get(User, 3)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (3,)


```

Если мы пометим `patrick` для удаления, как и в случае с другими операциями, ничего не произойдет, пока не будет выполнен `flush`:

```
>>> session.delete(patrick)
```


ТВышеуказанный SELECT, который мы запросили на вывод, предшествовал DELETE, который указывал на ожидающее удаление для `patrick`. Также был выполнен SELECT из таблицы `address`, который был вызван ORM для поиска строк в этой таблице, которые могут быть связаны с целевой строкой; это поведение является частью поведения, известного как [cascade](../glossary.html#term-cascade), и может быть настроено для более эффективной работы, позволяя базе данных автоматически обрабатывать связанные строки в `address`; в разделе [delete](../orm/cascades.html#cascade-delete) содержится вся информация об этом.

См. также

[delete](../orm/cascades.html#cascade-delete) - описывает, как настроить поведение [`Session.delete()`](../orm/session_api.html#sqlalchemy.orm.Session.delete "sqlalchemy.orm.Session.delete") в отношении того, как обрабатывать связанные строки в других таблицах.

Кроме того, экземпляр объекта `patrick`, который сейчас удаляется, больше не считается постоянным в [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), как показывает проверка на содержание:

```
>>> patrick in session
False
```

Однако, как и UPDATE, которые мы сделали для объекта `sandy`, каждое изменение, которое мы сделали здесь, локально для текущей транзакции, которая не станет постоянной, если мы ее не зафиксируем. Поскольку откат транзакции на самом деле более интересен в данный момент, мы сделаем это в следующем разделе.

### Массовая вставка / многорядное вставление, upsert, UPDATE и DELETE {#tutorial-orm-bulk}

Техники [unit of work](../glossary.html#term-unit-of-work), обсуждаемые в этом разделе, предназначены для интеграции [dml](../glossary.html#term-DML), или операторов INSERT/UPDATE/DELETE, с механикой объектов Python, часто включающих сложные графы взаимосвязанных объектов. Как только объекты добавлены в [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") с помощью [`Session.add()`](../orm/session_api.html#sqlalchemy.orm.Session.add "sqlalchemy.orm.Session.add"), процесс unit of work автоматически генерирует операторы INSERT/UPDATE/DELETE от нашего имени, поскольку создаются и изменяются атрибуты наших объектов.

Однако ORM [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") также имеет возможность обрабатывать команды, которые позволяют ему генерировать операторы INSERT, UPDATE и DELETE напрямую, не передавая никаких объектов, сохраненных в ORMФункции Bulk / Multi row ORM [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") используют конструкции [`insert()`](../core/dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"), [`update()`](../core/dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update") и [`delete()`](../core/dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete") напрямую, и их использование напоминает то, как они используются с SQLAlchemy Core (впервые представлены в этом учебнике в разделах [Использование операторов INSERT](data_insert.html#tutorial-core-insert) и [Использование операторов UPDATE и DELETE](data_update.html#tutorial-core-update-delete)). При использовании этих конструкций с ORM [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") вместо обычного [`Connection`](../core/connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"), их конструирование, выполнение и обработка результатов полностью интегрированы с ORM.

Для получения дополнительной информации и примеров использования этих функций см. раздел [ORM-Enabled INSERT, UPDATE, and DELETE statements](../orm/queryguide/dml.html#orm-expression-update-delete) в [ORM Querying Guide](../orm/queryguide/index.html).

См. также

[ORM-Enabled INSERT, UPDATE, and DELETE statements](../orm/queryguide/dml.html#orm-expression-update-delete) - в [ORM Querying Guide](../orm/queryguide/index.html)

### Откат

[`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") имеет метод [`Session.rollback()`](../orm/session_api.html#sqlalchemy.orm.Session.rollback "sqlalchemy.orm.Session.rollback"), который, как и ожидалось, выполняет ROLLBACK на текущем соединении SQL. Однако он также влияет на объекты, которые в настоящее время связаны с [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), в нашем предыдущем примере это объект Python `sandy`. Хотя мы изменили `.fullname` объекта `sandy` на `"Sandy Squirrel"`, мы хотим откатить эту изменение. Вызов [`Session.rollback()`](../orm/session_api.html#sqlalchemy.orm.Session.rollback "sqlalchemy.orm.Session.rollback") не только откатит транзакцию, но также **сбросит** все объекты, которые в настоящее время связаны с этой [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), что приведет к тому, что они обновятся при следующем доступе с помощью процесса, известного как [ленивая загрузка](../glossary.html#term-lazy-loading):

```
>>> session.rollback()
ROLLBACK
```

Чтобы более тщательно просмотреть процесс «истечения срока действия», мы можем заметить, что у объекта Python `sandy` не осталось состояния в его `__dict__`, за исключением специального внутреннего объекта состояния SQLAlchemy:

`````
>>> sandy.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>,
 'id': 2, 'name': 'sandy', 'fullname': 'Sandy Cheeks'}
```


Для удаленных объектов, когда мы ранее отметили, что `patrick` больше не
находится в сессии, идентичность этого объекта также восстанавливается:

```
>>> patrick in session
True
```


и, конечно, данные базы данных также присутствуют:


```
>>> session.execute(select(User).where(User.name == "patrick")).scalar_one() is patrick
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)
True

```

### Закрытие сессии {#tutorial-orm-closing} 


В предыдущих разделах мы использовали объект [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") вне
контекстного менеджера Python, то есть мы не использовали оператор `with`.
Это нормально, однако, если мы делаем это таким образом, лучше явно
закрыть [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), когда мы закончили с ним:


```
>>> session.close()
ROLLBACK


```

Закрытие [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"), что происходит, когда мы используем его в
контекстном менеджере, также выполняет следующие действия:


* Он [освобождает](../glossary.html#term-releases) все ресурсы соединения в пуле соединений, отменяя
(например, откатывая) любые транзакции, которые были в процессе выполнения.


Это означает, что когда мы используем сессию для выполнения некоторых задач только для чтения
и затем закрываем ее, нам не нужно явно вызывать
[`Session.rollback()`](../orm/session_api.html#sqlalchemy.orm.Session.rollback "sqlalchemy.orm.Session.rollback"), чтобы убедиться, что транзакция откатывается;
это обрабатывается пулом соединений.
* Он **удаляет** все объекты из [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session").


Это означает, что все объекты Python, которые мы загрузили для этой [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session"),
такие как `sandy`, `patrick` и `squidward`, теперь находятся в состоянии, известном
как [отсоединенный](../glossary.html#term-detached). В частности, мы отметим, что объекты, которые были все еще
в состоянии [истекшего срока](../glossary.html#term-expired), например, из-за вызова [`Session.commit()`](../orm/session_api.html#sqlalchemy.orm.Session.commit "sqlalchemy.orm.Session.commit"),
теперь```
>>> session.add(squidward)
>>> squidward.name
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (4,)
'squidward'

```

Совет

Постарайтесь избегать использования объектов в их отсоединенном состоянии, если это возможно. При закрытии [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") также очищайте ссылки на все ранее присоединенные объекты. В случаях, когда отсоединенные объекты необходимы, обычно это связано с немедленным отображением только что сохраненных объектов для веб-приложения, где [`Session`](../orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.Session") закрывается перед отображением представления, установите флаг [`Session.expire_on_commit`](../orm/session_api.html#sqlalchemy.orm.Session.params.expire_on_commit "sqlalchemy.orm.Session") в значение `False`.
