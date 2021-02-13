# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API references

### Getting Started
- Base URL: '127.0.0.1:5000'
- Authentication: This application does not require authentication.

### Errors
The API will return three types of errors:
- 400 - bad request
- 404 - resource not found
- 422 - unprocessable
Example response:
'''
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
'''

### Endpoints

#### GET /categories
- Returns a dictionary of all available categories
- Sample: 'curl http://127.0.0.1:5000/categories'
Example response:
'''
  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
'''

#### GET /questions
- Returns a paginated dictionary of questions of all available categories
- Sample: 'curl http://127.0.0.1:5000/questions'
Example Response:
'''
 "categories": {
   "1": "Science", 
   "2": "Art", 
   "3": "Geography", 
   "4": "History", 
   "5": "Entertainment", 
   "6": "Sports"
 }, 
 "current_category": null, 
 "questions": [
   {
     "answer": "Maya Angelou", 
     "category": 4, 
     "difficulty": 2, 
     "id": 5, 
     "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
   },  
   {
     "answer": "Escher", 
     "category": 2, 
     "difficulty": 1, 
     "id": 16, 
     "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
   }
 ], 
 "success": true, 
 "total_questions": 2
}
'''

#### DELETE /questions/<int:question_id>
- Delete an existing questions from the repository of available questions
- Sample: 'curl -X DELETE http://127.0.0.1:5000/questions/28'
Example response:
'''
{
  "deleted": "18", 
  "success": true
}
'''


#### POST /questions
- Create a new question to the repository of available questions
- Sample: 'curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Do I like Winter more than Summer?", "answer": "Yes", "difficulty": 1, "category": "1" }''
Example response:
'''
{
  "created": 19, 
  "success": true
}
'''

#### POST /questions/search
- Returns all questions having a substring matches with the input("searchTerm")
- Sample: 'curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "summer"}''
Example response:
'''
"question_num": 2,
  "questions": [
    {
      "answer": "no",
      "category": 2,
      "difficulty": 1,
      "id": 25,
      "question": "Do you like Summer?"
    },
    {
      "answer": "no",
      "category": 2,
      "difficulty": 1,
      "id": 26,
      "question": "Do you like Summer?"
    }
  ],
  "success": true
}
'''

#### GET /categories/<int:category_id>/questions
- Returns a dictionary of questions for the specified category
- Sample: 'curl http://127.0.0.1:5000/categories/1/questions'
Example response:
'''
  "current_category": 1,
  "current_category_name": "Science",
  "question_num": 26,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true
}
'''

#### POST /quizzes
- Returns one random question within a specified category
- Previously returned questions does not show again.
- Sample: 'curl -X POST "http://127.0.0.1:5000/quizzes" -d "{\"quiz_category\":{\"type\": \"History\", \"id\": \"4\"},\"previous_questions\":[2]}" -H "Content-Type: application/json"'
Example response:
'''
"question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
'''

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```