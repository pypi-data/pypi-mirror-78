#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/29 22:14
# @File   : _sqlite.py
# -------------------------------
# Mysql 数据库连接器
# -------------------------------

import pymysql as pdbc
from ..assist.cfg import *
from ..assist import log


class MysqlDBC :
    """
    Mysql 数据库连接器
    """

    def __init__(self, host='127.0.0.1', port=3306, username='root', password='123456', dbname='test', charset=CHARSET_DB) :
        """
        构造函数
        :param host : 数据库地址
        :param port : 数据库端口
        :param username : 数据库账号
        :param password : 数据库密码
        :param dbname : 数据库名称
        :param charset : 数据库编码
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.charset = charset
        self._conn = None


    def dbtype(self) :
        '''
        获取数据库类型
        :return: 数据库类型
        '''
        return MYSQL


    def conn(self) :
        """
        连接到数据库
        :return : 数据库连接（失败返回 None）
        """
        if not self._conn :
            try :
                self._conn = pdbc.connect(
                    host = self.host,
                    port = self.port,
                    user = self.username,
                    password = self.password,
                    db = self.dbname,
                    charset = self.charset
                )
            except :
                log.error("连接数据库 [%s] 失败" % self.dbname)
        return self._conn


    def close(self) :
        """
        断开数据库连接
        :return : 是否断开成功
        """
        is_ok = False
        if self._conn :
            try :
                self._conn.close()
                self._conn = None
                is_ok = True
            except :
                log.error("断开数据库 [%s] 失败" % self.dbname)
        return is_ok


    def reconn(self) :
        """
        重连数据库
        :return : 数据库连接（失败返回 None）
        """
        self.close()
        return self.conn()


    def commit(self) :
        """
        提交事务
        :return : 是否提交成功
        """
        is_ok = False
        if self._conn :
            try :
                self._conn.commit()
                is_ok = True
            except :
                log.error("提交事务到数据库 [%s] 失败" % self.dbname)
        return is_ok


    def cursor(self) :
        """
        返回数据库连接游标
        :return: 游标（失败返回 None）
        """
        return self._conn.cursor() if self._conn else None


    def exec_script(self, filepath) :
        """
        执行 SQL 脚本
        :param filepath : 脚本文件
        :return : 是否执行成功
        """
        is_ok = False
        if self.conn() :
            try :
                with open(filepath, "r") as file :
                    data = file.read()

                    cursor = self._conn.cursor()
                    sqls = data.split(";")
                    for sql in sqls :
                        sql = sql.strip()
                        if sql :
                            cursor.execute(sql)
                    self._conn.commit()
                    cursor.close()
                    is_ok = True
            except :
                log.error("执行 SQL 脚本失败： [%s]" % filepath)
            self.close()
        return is_ok


    def exec_sql(self, sql):
        """
        执行 SQL 语句
        :param sql: SQL 语句
        :return: 是否执行成功
        """
        is_ok = False
        if self.conn() :
            try:
                cursor = self._conn.cursor()
                cursor.execute(sql)
                self._conn.commit()
                cursor.close()
                is_ok = True
            except:
                log.error("执行 SQL 失败： [%s]" % sql)
        return is_ok

