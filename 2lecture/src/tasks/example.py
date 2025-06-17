from src.celery import app


@app.task
def add(x: int, y: int) -> int:
    """
    A simple example task that adds two numbers
    """
    return x + y 