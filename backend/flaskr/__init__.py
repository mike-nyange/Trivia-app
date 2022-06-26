import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
import sys

from models import setup_db, Question, Category

db = SQLAlchemy()


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    
    CORS(app, resources={'/':{'origins':'*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    
    @app.route("/categories", methods=["GET"])
    def get_all_categories():
        if request.method == "GET":
            categories = Category.query.order_by(Category.id).all()
            category_dict = {}

            #Create a dictionary of all categories
            
            for category in categories:
                category_dict[category.id] = category.type

            if (len(category_dict) == 0):
                abort(404)

            return jsonify({
                'categories': category_dict,
                'success': True
            })
            
   
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions')
    def get_questions():
        if request.method == "GET":
            # get all the questions and paginate
            questions = Question.query.all()
            all_questions = len(questions)
            paginated_questions = paginate_questions(request, questions)

            # If no questions are found abort
            if (len(paginated_questions) == 0):
                abort(404)

            try:
                # Get all categories and put them in a dict
                categories = Category.query.all()
                categories_dict = {}
                for category in categories:
                    categories_dict[category.id] = category.type

                # return to view in json
                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': all_questions,
                    'categories': categories_dict
                })
            except:
                db.session.rollback()
                print(sys.exc_info())
                abort(422)
            finally:
                db.session.close()
    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        if request.method == "DELETE":
            try:
                #get one question by id
                question = Question.query.filter_by(id=id).one_or_none()
                all_questions = len(Question.query.all())
                
                if question is None:
                    abort(404)

                question.delete()
                
                return jsonify({
                    'deleted': id,
                    'success': True,
                    'total_questions': all_questions
                })
            except:
                abort(422)            
            
    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    @app.route('/questions', methods=['POST'])
    def create_question():
        if request.method == "POST":
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category',  None)
            searchTerm = body.get('searchTerm', None)
            try:
                if searchTerm:
                    questions = Question.query.filter(Question.question.ilike(f"%{searchTerm}%")).all()
                    paginated_questions = paginate_questions(request, questions)
                    
                    return jsonify({
                        'success': True,
                        'questions': paginated_questions,
                        'total_questions': len(paginated_questions)
                    })
                else:                  
                    q = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                    q.insert()

                    questions = Question.query.order_by(Question.id).all()
                    paginated_questions = paginate_questions(request, questions)
                    all_questions = len(Question.query.all())

                    return jsonify({
                        'success': True,
                        'question_created': q.question,
                        'created': q.id,
                        'questions': paginated_questions,
                        'total_questions': all_questions
                    })
                
            except:
                abort(422)
    
    

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/search', methods=['POST'])
    def search():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        questions = Question.query.filter(Question.question.ilike(f"%{searchTerm}%")).all()
        paginated_questions = paginate_questions(request, questions)
        
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(paginated_questions)
        })
        
        # questions = [question.format() for question in Question.query.all() if
        #              re.search(search_term, question.question, re.IGNORECASE)]
        # return jsonify({
        #     'questions': questions,
        #     'total_questions': len(questions)
        # })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        if request.method == "GET":
            category = Category.query.filter_by(id=category_id).one_or_none()
            if category is None:
                abort(404)
            try:
                questions = Question.query.filter_by(category=category.id).all()
                paginated_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'total_questions': len(Question.query.all()),
                    'current_category': category.type,
                    'questions': paginated_questions
                })

            except:
                abort(400)
    

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    @app.route('/quizzes', methods=['POST'])
    def play_quiz_game():
        if request.method == "POST":
            try:
                body = request.get_json()
                previous_questions = body.get('previous_questions', None)
                category = body.get('quiz_category', None)

                category_id = category['id']
                next_question = None
                
                if category_id != 0:
                    questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_((previous_questions))).all()    
                else:
                    questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
                
                if len(questions) > 0:
                    next_question = random.choice(questions).format()
                
                return jsonify({
                    'question': next_question,
                    'success': True,
                })
            except:
                abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 422

    return app
