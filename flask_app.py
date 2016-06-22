#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from flask import request
import mysql.mysql as sql
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return "Welcome to HSE API"

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# ======= LEADER BOARD ===========

@app.route('/leader_board_only_table', methods=['GET'])
def leader_board_only_table():
    result = sql.get_leaderboard()
    return render_template('leaderboard-table.html', users=result, title="Right answers")

@app.route('/looser_board_only_table', methods=['GET'])
def looser_board_only_table():
    result = sql.get_looserboard()
    return render_template('leaderboard-table.html', users=result, title="Wrong answers")

@app.route('/ratio_board_only_table', methods=['GET'])
def ratio_board_only_table():
    result = sql.get_ratioboard()
    return render_template('leaderboard-table.html', users=result, title="Ratio right answers")

@app.route('/leader_board', methods=['GET'])
def leader_board():
    result = sql.get_leaderboard()
    return render_template('leaderboard.html', users=result, title="Right answers", url="leader_board_only_table")

@app.route('/looser_board', methods=['GET'])
def looser_board():
    result = sql.get_looserboard()
    return render_template('leaderboard.html', users=result, title="Wrong answers", url="looser_board_only_table")

@app.route('/ratio_board', methods=['GET'])
def ratio_board():
    result = sql.get_ratioboard()
    return render_template('leaderboard.html', users=result, title="Ratio right answers", url="ratio_board_only_table")

@app.route('/stat', methods=['GET'])
def stat():
    return render_template('stat.html')

# ======= SHOW DATABASE ===========

@app.route('/all_users', methods=['GET'])
def all_users():
    result = sql.get_all_rows('USERS')
    return render_template('all_rows.html', users=result)

@app.route('/all_history', methods=['GET'])
def all_history():
    result = sql.get_all_rows('HISTORY')
    return render_template('all_rows.html', users=result)

@app.route('/all_questions', methods=['GET'])
def all_questions():
    result = sql.get_all_rows('QUESTIONS')
    return render_template('all_rows.html', users=result)

@app.route('/all_songs', methods=['GET'])
def all_songs():
    result = sql.get_all_rows('SONG')
    return render_template('all_rows.html', users=result)

# ===================================


# ============= ADD DATA ============

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if(sql.check_user(login)):
            return json.dumps({'status' : '0', 'error' : 'User already exists'})

        if(sql.add_user(login, password)):
            return json.dumps({'status' : '1'})

    return 'Get requests isn\'t allowed'

@app.route('/add_history', methods=['POST', 'GET'])
def add_history_handler():
    if request.method == 'POST':

        params = ['user', 'song_name', 'song_artist', 'answer_right',
                    'op1', 'op2', 'op3', 'genre', 'user_answer', 'result']

        for i in params:
            if (request.form.get(i, None) == None):
                return json.dumps({'status' : '0', 'error' : 'Need parameter: ' + i})

        user = request.form['user']
        song_name = request.form['song_name']
        song_artist = request.form['song_artist']
        answer_right = request.form['answer_right']
        op1 = request.form['op1']
        op2 = request.form['op2']
        op3 = request.form['op3']
        genre = request.form['genre']
        user_answer = request.form['user_answer']
        result = str2bool(request.form['result'])

        res = sql.add_history(user, song_name, song_artist, answer_right, op1, op2, op3, genre, user_answer, result)

        return json.dumps({'status' : '1', 'result' : str(res)})

    return 'Get requests isn\'t allowed'

@app.route('/count_game', methods=['POST', 'GET'])
def count_game():
    if request.method == 'POST':
        login = request.form['login']
        return str(sql.game_count(login))

    return 'Get requests isn\'t allowed'

@app.route('/count_game_increment', methods=['POST', 'GET'])
def count_game_increment():
    if request.method == 'POST':
        login = request.form['login']
        return str(sql.game_count_increment(login))

    return 'Get requests isn\'t allowed'

# ===================================

@app.route('/auth', methods=['POST', 'GET'])
def auth():

    if request.method == 'POST':
        result = sql.auth(request.form['login'], request.form['password'])
        if result:
            return json.dumps({'status' : '1', 'result' : result})
        else:
            return json.dumps({'status' : '0', 'error' : 'Invalid username/password'})

    return 'Get requests isn\'t allowed'

