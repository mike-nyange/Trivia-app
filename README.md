# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Reference

### Getting Started

Base Url: This application is currently hosted on a local machine. It is hosted at [http://127.0.0.1:5000/]
Authentication: It doesn't supprt authentication hence requires no authentication or  API keys.

## Error Handling

Errors that will be returned include the following;

- 400: Bad Request.
- 404: Resource not found.
- 422: Unprocessable Entity.
- 500: Internal Server Error.

## Endpoints

###  GET "/categories"

- Fetches all categories available in the database.
- Request Parameters: None
- Returns categories as a dictionary and success value
- Sample: curl `http://127.0.0.1:5000/categories` 

```json
{
  "categories": {
    "1" : "Countries",
    "2" : "Continents",
    "3" : "General History",
    "4" : "Pop Culture",
    "5" : "Presidents",
    "6" : "Sports"
    },
  "success": true
}
```

### POST/categories

- This creates a new category using the submitted type.
- Returns the created category, success value and total categories
- Sample `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"new Category"}'`

```json
{
  "created": 7,
  "success": true,
  "total_categories": 7
}
```

### DELETE "categories/{category_id}

- This deletes a category provided that its id exists.
- Returns the id of the deleted category, success value and total categories.
- Sample `curl -X DELETE http://127.0.0.1:5000/categories/8`

```json
{
  "deleted": 7,
  "success": true,
  "total_categories": 6
}
```

### Get "questions"

- Returns a list of questions for the given phone number as they have been paginated in groups of 10.
- Sample `curl http://127.0.0.1:5000/questions?page=1`

```json
  "categories": {
    "1" : "Capital cities",
    "2" : "Continents",
    "3" : "General History",
    "4" : "Pop Culture",
    "5" : "Presidents",
    "6" : "Sports"
    },
  "questions": [
    {
      "answer": "Dodoma",
      "category": 1,
      "difficulty": 1,
      "id": 1,
      "question": "The capital city of Tanzania"
    },
    {
      "answer": "South America",
      "category": 2,
      "difficulty": 2,
      "id": 2,
      "question": "In which continent are the Andes Mountains located"
    },
    {
      "answer": "Asia",
      "category": 2,
      "difficulty": 3,
      "id": 3,
      "question": "Which continent has the largest population"
    },
    {
      "answer": "Uhuru Kenyatta",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "Who is the president of Kenya"
    },
    
  ],
  "success": true,
  "total_questions": 4
```

### POST "/questions"

- Creates a new question.
- Returns the id of the created question, success value total questions and question list based on current page.
- Sample: `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"question":"When did Hitler die", "answer":"1945", "category":"3" , "difficulty":"3"}'`

```json
  "created": 5,
  "questions": [
    {
      "answer": "Dodoma",
      "category": 1,
      "difficulty": 1,
      "id": 1,
      "question": "The capital city of Tanzania"
    },
    {
      "answer": "South America",
      "category": 2,
      "difficulty": 2,
      "id": 2,
      "question": "In which continent are the Andes Mountains located"
    },
    {
      "answer": "Asia",
      "category": 2,
      "difficulty": 3,
      "id": 3,
      "question": "Which continent has the largest population"
    },
    {
      "answer": "Uhuru Kenyatta",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "Who is the president of Kenya"
    },
    {
      "answer": "1945",
      "category": 3,
      "difficulty": 3,
      "id": 5,
      "question": "When did Hitler die"
    },
  ],
  "success": true,
  "total_questions": 5
```

### POST "/questions"

- Search for questions using a search term.
- Return questions paginated with the matching search term.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "continents"}'`

```json
{
  "questions": [
    {
      "answer": "South America",
      "category": 2,
      "difficulty": 2,
      "id": 2,
      "question": "In which continent are the Andes Mountains located"
    },
    {
      "answer": "Asia",
      "category": 2,
      "difficulty": 3,
      "id": 3,
      "question": "Which continent has the largest population"
    },
  ],
  "success": true,
  "total_questions": 2
}
```

### DELETE "questions/{category_id}

- This deletes a question provided that its id exists.
- Returns the id of the deleted question, success value and total questions.
- Sample `curl -X DELETE http://127.0.0.1:5000/question/5`

```json
{
  "deleted": 5,
  "success": true,
  "total_categories": 4
}
```

### GET "/categories/<{category_id}/questions"

- get all questions associated to a particular category.
- Returns the currently category, a list of paginated questions, success
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`

```json
{
  "current_category": 2,
  "questions": [
    {
      "answer": "South America",
      "category": 2,
      "difficulty": 2,
      "id": 2,
      "question": "In which continent are the Andes Mountains located"
    },
    {
      "answer": "Asia",
      "category": 2,
      "difficulty": 3,
      "id": 3,
      "question": "Which continent has the largest population"
    },
  ],
  "success": true,
  "total_questions": 2
}
```

### POST/quizzes

- Takes a list of previous questions and category of choice and allows a user to play the trivia game.
- Returns a random questions belonging to the provided category and which is not in the previous questions list and a success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2], "quiz_category": {"type": "continents", "id": "3"}}'`

```json

{
  "question":
   {
      "answer": "Asia",
      "category": 2,
      "difficulty": 3,
      "id": 3,
      "question": "Which continent has the largest population"
    },
  "success": true
}

```

## Author

- Mike Mwanyika Nyange
- Esther Wanjiru Kariuki

## Testing

### To run tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
