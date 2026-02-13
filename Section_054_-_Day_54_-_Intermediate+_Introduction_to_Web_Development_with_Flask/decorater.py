import time
def decorater_function(original_function):
    def wrapper_function():
        time.sleep(4)
        return original_function()
    return wrapper_function

@decorater_function
def say_hello():
    print("Hello")

@decorater_function
def say_goodbye():
    print("Goodbye")

def say_greeting():
    print("Hello, greetings")

say_greeting_delayed=decorater_function(say_greeting)

say_hello()
say_goodbye()
say_greeting_delayed()