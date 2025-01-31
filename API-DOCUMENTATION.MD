## **API Documentation for User Authentication**

### **Base URL**

`http://127.0.0.1:8000/api/accounts`

### **Endpoints**

#### **Register User**

- **Method**: POST  
- **Endpoint**: `/register/`  
- **Full URL**: `http://127.0.0.1:8000/api/accounts/register/`  
- **Headers**:  
  ```
  Content-Type: application/json
  ```

**Request Body (JSON):**

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "password123"
}
```

**Response (Success 201):**

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com"
}
```

**Response (Error 400):**

```json
{
  "password": ["This password is too weak."],
  "email": ["A user with this email already exists."]
}
```

---

#### **Email Verification**

- **Method**: GET  
- **Endpoint**: `/email-verification/{token}/`  
- **Response (Success 200):**

```json
{
  "message": "Email verified successfully"
}
```

- **Response (Error 400):**

```json
{
  "error": "Invalid or expired token"
}
```

---

#### **Login User**

- **Method**: POST  
- **Endpoint**: `/login/`  
- **Request Body (JSON):**

```json
{
  "username": "johndoe",
  "password": "password123"
}
```

- **Response (Success 200):**

```json
{
  "token": "knox-token-string"
}
```

- **Response (Error 400):**

```json
{
  "error": "Invalid credentials"
}
```

---

#### **Logout User**

- **Method**: POST  
- **Endpoint**: `/logout/`  
- **Headers**:  
  ```
  Authorization: Token knox-token
  ```

- **Response (Success 204)**: No content.  

- **Response (Error 401):**

```json
{
  "detail": "Authentication credentials were not provided."
}







Test 1: User Registration (POST /api/accounts/register/)
Request:
URL: http://localhost:8000/api/accounts/register/
Method: POST
Body (raw JSON):
json

{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123",
    "role": "Student"
}
Steps:
Open Postman.
Set the HTTP method to POST.
Enter the URL above.
Under the Body tab, select raw and choose JSON as the format.
Paste the request body provided above.
Click Send.
Expected Response:
You should get a response indicating that the user has been created successfully. You may also receive a message prompting to verify the email:

json

{
    "message": "User registered successfully. Check your email for verification."
}



Test 2: User Login (POST /api/accounts/login/)
Request:
URL: http://localhost:8000/api/accounts/login/
Method: POST
Body (raw JSON):
json

{
    "username": "testuser",
    "password": "password123"
}
Steps:
Set the HTTP method to POST.
Enter the URL http://localhost:8000/api/accounts/login/.
Under the Body tab, select raw and choose JSON as the format.
Paste the request body provided above.
Click Send.
Expected Response:
If the login is successful, you should receive a JWT token (or Auth token) as part of the response:

json

{
    "token": "your_generated_token_here"
}
You will use this token for authorization in subsequent requests.



Test 3: Mock Exam Initialization (POST /api/accounts/mock-exams/init/)
Request:
URL: http://localhost:8000/api/accounts/mock-exams/init/
Method: POST
Authorization: Bearer Token (Use the token from the login step)
Body (raw JSON):
json

{
    "subjects": [1, 2],
    "duration": 30
}
Steps:
Set the HTTP method to POST.
Enter the URL http://localhost:8000/api/accounts/mock-exams/init/.
Under the Authorization tab, select Bearer Token and paste the JWT token you received from the login.
Under the Body tab, select raw and choose JSON as the format.
Paste the request body provided above.
Click Send.
Expected Response:
If the mock exam is initialized successfully, you should receive a response with the details of the mock exam:

json

{
    "id": 1,
    "user": 1,
    "subjects": [1, 2],
    "start_time": "2024-12-04T12:00:00Z",
    "duration": 30,
    "status": "ongoing"
}




Test 4: Retrieve Mock Exam Questions (GET /api/accounts/mock-exams/{mock_exam_id}/questions/)
Request:
URL: http://localhost:8000/api/accounts/mock-exams/1/questions/ (Replace 1 with your mock exam ID)
Method: GET
Authorization: Bearer Token (Use the token from the login step)
Steps:
Set the HTTP method to GET.
Enter the URL http://localhost:8000/api/accounts/mock-exams/1/questions/ (Replace 1 with the mock exam ID).
Under the Authorization tab, select Bearer Token and paste the JWT token you received from the login.
Click Send.
Expected Response:
You should get a list of random questions related to the mock exam:

json

[
    {
        "id": 1,
        "subject": 1,
        "question_text": "What is 2 + 2?",
        "options": ["2", "3", "4", "5"]
    },
    {
        "id": 2,
        "subject": 2,
        "question_text": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"]
    }
]




Test 5: Submit Mock Exam Answers and Get Score (POST /api/accounts/mock-exams/{mock_exam_id}/submit/)
Request:
URL: http://localhost:8000/api/accounts/mock-exams/1/submit/ (Replace 1 with the mock exam ID)
Method: POST
Authorization: Bearer Token (Use the token from the login step)
Body (raw JSON):
json

{
    "answers": [
        {
            "question_id": 1,
            "user_answer": 4
        },
        {
            "question_id": 2,
            "user_answer": 3
        }
    ]
}
Steps:
Set the HTTP method to POST.
Enter the URL http://localhost:8000/api/accounts/mock-exams/1/submit/ (Replace 1 with the mock exam ID).
Under the Authorization tab, select Bearer Token and paste the JWT token you received from the login.
Under the Body tab, select raw and choose JSON as the format.
Paste the request body provided above.
Click Send.
Expected Response:
If the answers are submitted successfully, you should receive a score and detailed results for each question:

json

{
    "score": 2,
    "total_questions": 2,
    "results": [
        {
            "question_id": 1,
            "question_text": "What is 2 + 2?",
            "correct_option": 4,
            "user_answer": 4,
            "is_correct": true,
            "explanation": "2 + 2 equals 4."
        },
        {
            "question_id": 2,
            "question_text": "What is the capital of France?",
            "correct_option": 3,
            "user_answer": 3,
            "is_correct": true,
            "explanation": "The capital of France is Paris."
        }
    ]
}
