---
title: SQL management
date: 2020-03-07 22:59:06 +08
---

**Deprecated: use tortoise orm instead, you can use aiosql for other statistic data query, like pipelinedb stream and views**

# SQL 使用 AIOSQL 进行管理

使用的组件：
- aiosql
- asyncpg

## 为什么选择使用 AIOSQL 而不是其他的 ORM ?

主要有这几点参考：

- AIOSQL 的方式实现了方法和 SQL 的分离，并不会导致代码看起来丑陋
- 学习成本低，相对于 sqlachemy 这样的框架而言，学习 aiosql 可能只需要一会儿
- 通过 sql 来编写方法更加的灵活
- 后续迁移至其他框架更加灵活
- 完美支持 asyncio
- 通过参数模板，并不会有常见的 SQL 注入问题，相对安全

## 编写流程

1. 需要到 sql_query/sql 目录下编写你需要的业务 sql 模板
2. 编写需要加载对象的 record_class，参见 sql_query/database_record_model.py
3. 在 processers/postgres_process 中添加你需要的业务方法

需要注意的是，整个里面最复杂的部分是 SQL 的模板，需要注意模板名称里面有些比较特殊的符号。

-  Execute SQL script statements with #
-  Insert/Update/Delete Many with *!
-  Insert Returning with <!
-  Insert/Update/Delete with !
-  Flat return single row data with ? [(a, c)] -> (a, c)

## 初始化 postgres 数据库

直接运行 `init_postgres_schema.py` 文件即可，初始化的 sql 在 sql_query/sql/full.sql 中。

## 后续如何管理多个 sql 版本？

使用 git 直接在 sql_query/sql/full.sql 上面迭代；或者使用新增 patch.sql 的形式，每次通过运行 patch.sql 文件实现迁移。

## ORM

如果你需要使用 ORM 的话，推荐使用 [tortoise](https://tortoise-orm.readthedocs.io/en/latest/)，类 django 风格。

