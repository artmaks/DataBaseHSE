#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

def connect_sql():
    db = MySQLdb.connect(host="hseteam.mysql.pythonanywhere-services.com",    # your host, usually localhost
                     user="hseteam",         # your username
                     passwd="qwerty123456789",  # your password
                     db="hseteam$game",
                     charset='utf8')        # name of the data base
    return db


def get_leaderboard():

    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT (SELECT login FROM USERS WHERE USERS.id = HISTORY.USER_ID) AS NAME, SUM(RESULT) AS SCORE FROM HISTORY GROUP BY USER_ID ORDER BY SUM(RESULT) DESC;")

    res = []

    for row in cur.fetchall():
        res.append({"name" : row[0], "score" : row[1]})

    return res

def get_ratioboard():

    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT (SELECT login FROM USERS WHERE USERS.id = HISTORY.USER_ID) AS NAME ,SUM(RESULT)/COUNT(RESULT) as SCORE FROM HISTORY GROUP BY USER_ID ORDER BY SCORE DESC;")

    res = []

    for row in cur.fetchall():
        res.append({"name" : row[0], "score" : row[1]})

    return res

def get_looserboard():

    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT (SELECT login FROM USERS WHERE USERS.id = HISTORY.USER_ID) AS NAME ,COUNT(RESULT) - SUM(RESULT) FROM HISTORY GROUP BY USER_ID;")

    res = []

    for row in cur.fetchall():
        res.append({"name" : row[0], "score" : row[1]})

    return res

def auth(login, password):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT * FROM `USERS` WHERE login='%s' AND password='%s'" % (login,password))

    count = 0

    for row in cur.fetchall():
        count += 1

    return count

def check_user(login):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT id FROM `USERS` WHERE login='%s'" % (login,))

    if(cur.rowcount == 0):
        return None
    else:
        row = cur.fetchone()
        return row[0]

def game_count(login):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT game_count FROM `USERS` WHERE login='%s'" % (login,))

    if(cur.rowcount == 0):
        return None
    else:
        row = cur.fetchone()
        return row[0]

def game_count_increment(login):
    count = game_count(login)

    db = connect_sql()
    cur = db.cursor()

    cur.execute("UPDATE `USERS` SET game_count=%d WHERE login='%s'" % (count + 1, login))
    db.commit()

    return count


def add_user(login, password):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("INSERT INTO `USERS` (login, password) VALUES ('%s', '%s') " % (login, password))

    db.commit()

    return True

def get_song(name, artist):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT id FROM `SONG` WHERE name='%s' AND artist='%s' LIMIT 1" % (name, artist))

    if(cur.rowcount == 0):
        cur.execute("INSERT INTO `SONG` (NAME, ARTIST) VALUES ('%s', '%s')"
        % (name, artist))
        db.commit()

        return get_song(name, artist)
    else:
        row = cur.fetchone()
        return row[0]

def get_question(song_id, answer_right, op1, op2, op3, genre):

    options = [op1, op2, op3]
    options.sort()

    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT ID FROM `QUESTIONS` WHERE SONG_ID='%s' AND ANSWER_RIGHT='%s' AND OP1='%s' AND OP2='%s' AND OP3='%s' LIMIT 1"
    % (song_id, answer_right, options[0], options[1], options[2]))

    if(cur.rowcount == 0):
        cur.execute("INSERT INTO `QUESTIONS` (SONG_ID, ANSWER_RIGHT, OP1, OP2, OP3, GENRE) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
        % (song_id, answer_right, options[0], options[1], options[2], genre))
        db.commit()


        return get_question(song_id, answer_right, op1, op2, op3, genre)
    else:
        row = cur.fetchone()
        return row[0]

def add_history_row(user_id, quest_id, result, user_answer, game_id):

    db = connect_sql()
    cur = db.cursor()

    cur.execute("INSERT INTO `HISTORY` (USER_ID, QUEST_ID, RESULT, ANSWER_USER, GAME_ID) VALUES ('%d', '%d', '%d', '%s', '%d')"
        % (user_id, quest_id, result, user_answer, game_id))

    db.commit()

    return True

def add_history(user, song_name, song_artist, answer_right, op1, op2, op3, genre, user_answer, result):

    user_id = check_user(user)
    if(user_id == None):
        return False

    song = get_song(song_name, song_artist)
    if(song == None):
        return False

    question = get_question(song, answer_right, op1, op2, op3, genre)
    if(question == None):
        return False

    game_id = game_count(user)


    # print(add_history('temka', 'True song name', 'True song artist', 'True song name', 'No true', 'Nono', 'Nooooo', 'True song artist', True))

    return add_history_row(user_id, question, result, user_answer, game_id)


def get_all_rows(table = 'USERS'):
    db = connect_sql()
    cur = db.cursor()

    cur.execute("SELECT * FROM `%s`" % (table,))

    result = []

    for row in cur.fetchall():
        result.append(row)

    return result
