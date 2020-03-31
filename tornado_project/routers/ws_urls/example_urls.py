from tornado_project.handlers.ws_handlers import ExampleHandler
from tornado_project.handlers.ws_quiz import QuizHandler

url_patterns = [
    (r'/v1/ws/example', ExampleHandler),
    (r'/v1/ws/quiz', QuizHandler),
]
