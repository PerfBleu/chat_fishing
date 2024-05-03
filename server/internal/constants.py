from sqlalchemy import text
SQL_INTERNAL_ADDONS_USERS_GET_USER_BY_USERNAME = text("SELECT * FROM 用户数据 WHERE 用户名=:uid;")