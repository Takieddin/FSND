Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, 
http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format: 


{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal Server Error

Endpoints
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
  Sample:curl http://127.0.0.1:5000/categories

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/categories/<int:category_id>/questions'
- Returns a list of question objects and success value.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Request Arguments: integer page 
- Sample: curl http://127.0.0.1:5000/categories/3/questions

{
    "questions": [
        
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
}

GET '/questions'
- Returns a list of question objects, success value, a list of categories and total number of questions
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Request Arguments: integer page 
- Sample: curl http://127.0.0.1:5000/questions

{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "currentCategory": 3,
    "questions": [
        
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "totalQuestions": 19
}

DELETE '/questions/{question_id}'
-Deletes the question of the given ID if it exists.
-Request Arguments: None
-Returns the id of the deleted question, success value, total books, and total number of question.
curl -X DELETE http://127.0.0.1:5000/questions/2
{
'success': True,
'deleted': 2,
'total_questions': 13
}


POST'/questions'
-If 'searchTerm' is provided in request body , searches for questions containing that searchTerm
-Returns the success value and a paginted list of question objects matching the Results
-Request Arguments: int page
sample :curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"art"}'
{
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true
}
-If 'searchTerm' is  not provided in request body , creates a new  question
-Returns the success value , id of the created  question and number of total questions
sample :
curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d'{"question":"what is the capital of France ?","answer" == "Paris","category":3,"difficulty":3}'
{
 'success': True,
 'created': 16,
 'total_questions': 16
 }


POST '/quizzes'
-Returns the success value and a random question object that its id not included in request body previous questions 
-if a quiz_category type is provided in request body, the question will be selected from that category
-if the provided quiz_category type is 'click' the question will be selected from a random category 
-Request Arguments: None 
sample :curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Art","id":2},"previous_questions":[4,5,9,8]}'
{
    "question":
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
        }
        ,
    "success": true
}