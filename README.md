<h1 align="center">
    TODO API with Python
</h1>

<p align="center">
 <img src="https://img.shields.io/static/v1?label=LinkedIn&message=https://www.linkedin.com/in/cassianodess/&color=8257E5&labelColor=000000" alt="@cassianodess" />
</p>

## Techs
 
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Patterns

- SOLID, DRY
- Integration Tests
- API REST

## How to run

- Clone this repository
- Create a Postgres database `todo_db`
- Copy .env.example and rename to .env
- Change `DB_URL` variables like `username`, `password`, `host` and `port`
- Run command:
```
make init && make run
```

## How to run integration tests
```
make test
```

## Endpoints

To make the HTTP requests below, was used [httpie](https://httpie.io):

- Create Todo
```
http POST :8080/api/todos title="Todo 1" description="Desc Todo 1"
```
- Response body
```
{
    "message": "todo has been created successfully",
    "data": {
        "id": "8ef08864-cc9e-472c-932d-0b01075d754f"
        "title": "Todo 1"
        "completed": false,
    }
}
```

- List Todo
```
http GET :8080/api/todos
```
- Response body
```

{
    "message": "todos has been listed successfully",
    "data": [
        {
            "id": "8ef08864-cc9e-472c-932d-0b01075d754f",
            "title": "Todo 1"
            "completed": false,
        }
    ]
}
```

- Update Todo
```
http PUT :8080/api/todos/<id> title="Todo 1 Up" description="Desc Todo 1 Up"
```
- Response body
```

{
    "message": "todo has been updated successfully",
    "data": {
        "title": "Todo 1 Up"
        "completed": false,
    }
}

```

- Delete Todo
```
http DELETE :8080/api/todos/<id>
```
```
{
    "message": "todo has been deleted successfully",
    "data": {
        "title": "Todo 1 Up"
        "completed": false,
    }
}
```