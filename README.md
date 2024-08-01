# Task Manager using Flask REST API

This project is a task manager application built with Flask REST API in Python. It includes features for user registration, login with JWT authentication, and middleware.

## Features

1. **User Registration (Password Hash)**
2. **Login (JWT Authentication)**
3. **Middleware**

### Tasks
- Create a task for logged-in user
- Fetch all tasks based on logged-in user
- Mark a task as completed
- Delete the task after completing

## Installation

### Prerequisites

- Python 3.8+
- Virtualenv (optional, but recommended)

### Steps

1. **Clone the repository**

    ```sh
    git clone https://github.com/itzakash/Python-Task-Manager-Flask.git
    cd your-repo
    ```

2. **Create a virtual environment (optional)**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**

    Create a `.env` file in the project root directory and add the following variables:

    ```env
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```

5. **Run the application**

    ```sh
    flask run
    ```

6. **API Endpoints**

    - **User Registration**: `POST /users/register`
    - **Login**: `POST /user/login`
    - **Create Task**: `POST /`
    - **Fetch Tasks**: `GET /`
    - **Mark Task as Completed**: `PATCH /tasks/<task_id>`
    - **Delete Task**: `DELETE /<task_id>`

## Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
