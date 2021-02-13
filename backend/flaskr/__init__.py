import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, total_questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in total_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
	# create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        print("Question queried")
        categories_data = {}

        for category in categories:
            categories_data[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_data
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        total_questions = Question.query.order_by(Question.id).all()
        question_num = len(total_questions)
        current_questions = paginate_questions(request, total_questions)

        categories = Category.query.order_by(Category.type).all()
        categories_data = {}

        for category in categories:
            categories_data[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'question_num': question_num,
            'categories': categories_data,
            'current_category': None
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
            question = Question.query.get(question_id)

            if not question:
                abort(404)

            try:
                question.delete()

                return jsonify({
                    'success': True,
                    'deleted': question_id
                })

            except:
                abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        new_question = data.get('question')
        new_answer = data.get('answer')
        new_category = data.get('category')
        new_difficulty = data.get('difficulty')

        if ((new_question is None) or (new_answer is None) or (new_difficulty is None) or (new_category is None)):
            abort(422)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm')

        if search_term:
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in results],
                'question_num': len(results)
            })

        abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()

            # Need to use .format() to let the computer reading as json attribute.
            current_category_name = Category.query.filter(Category.id == category_id).first().format()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'question_num': len(questions),
                'current_category_name': current_category_name['type'],
                'current_category': category_id
            })

        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        data = request.get_json()
        category = data.get('quiz_category')
        previous = data.get('previous_questions')

        if ((not category) or (not previous)):
            abort(400)

        # refer to /frontend/src/componets/QuizView.js > selectCategory()
        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        next_question = questions[random.randrange(0, len(questions), 1)].format()

        used = False
        if next_question['id'] in [previous]:
            used = True

        while used:
            next_question = next_question
            if (len(previous) == len(questions)):
                return jsonify({
                    'success': True,
                    'done': "There is no more new question."
                })

        return jsonify({
            'success': True,
            'question': next_question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    return app
