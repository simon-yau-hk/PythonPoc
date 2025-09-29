#!/usr/bin/env python3
"""
Python Examples for Expert Programmers New to Python
Demonstrates key language features and common patterns
"""

# ============================================================================
# 1. BASIC SYNTAX & DYNAMIC TYPING
# ============================================================================

def basic_syntax_demo():
    """Demonstrates Python's clean syntax and dynamic typing"""
    print("=== Basic Syntax & Dynamic Typing ===")
    
    # No variable declarations needed
    name = "Python"
    version = 3.11
    is_awesome = True
    
    # String formatting (multiple ways)
    print(f"Language: {name} {version}")  # f-strings (Python 3.6+)
    print("Language: {} {}".format(name, version))  # .format()
    print("Language: %s %.1f" % (name, version))  # % formatting
    
    # Dynamic typing in action
    variable = 42
    print(f"variable is {type(variable).__name__}: {variable}")
    variable = "Now I'm a string!"
    print(f"variable is {type(variable).__name__}: {variable}")


# ============================================================================
# 2. DATA STRUCTURES
# ============================================================================

def data_structures_demo():
    """Showcases Python's built-in data structures"""
    print("\n=== Data Structures ===")
    
    # Lists (mutable, ordered)
    fruits = ["apple", "banana", "cherry"]
    fruits.append("date")
    print(f"List: {fruits}")
    
    # List comprehensions (very Pythonic!)
    squares = [x**2 for x in range(5)]
    print(f"Squares: {squares}")
    
    # Dictionaries (key-value pairs)
    person = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }
    print(f"Dictionary: {person}")
    
    # Sets (unique elements)
    unique_numbers = {1, 2, 3, 3, 4, 4, 5}
    print(f"Set: {unique_numbers}")
    
    # Tuples (immutable)
    coordinates = (10, 20)
    print(f"Tuple: {coordinates}")


# ============================================================================
# 3. FUNCTIONS & DECORATORS
# ============================================================================

def timing_decorator(func):
    """A decorator to measure function execution time"""
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def fibonacci(n):
    """Calculate fibonacci number (with timing decorator)"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def function_features_demo():
    """Demonstrates Python function features"""
    print("\n=== Functions & Decorators ===")
    
    # Default parameters
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    print(greet("World"))
    print(greet("Python", "Hi"))
    
    # *args and **kwargs
    def flexible_function(*args, **kwargs):
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
    
    flexible_function(1, 2, 3, name="Python", version=3.11)
    
    # Lambda functions
    numbers = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Doubled: {doubled}")
    
    # Decorator in action
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")


# ============================================================================
# 4. OBJECT-ORIENTED PROGRAMMING
# ============================================================================

class Animal:
    """Base class demonstrating OOP concepts"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def __str__(self):
        return f"{self.name} the {self.species}"
    
    def __repr__(self):
        return f"Animal('{self.name}', '{self.species}')"
    
    def speak(self):
        return "Some generic animal sound"

class Dog(Animal):
    """Inheritance example"""
    
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed
    
    def speak(self):
        return "Woof!"
    
    @property
    def description(self):
        return f"{self.name} is a {self.breed}"

def oop_demo():
    """Demonstrates object-oriented programming"""
    print("\n=== Object-Oriented Programming ===")
    
    # Create objects
    generic_animal = Animal("Unknown", "Mystery")
    my_dog = Dog("Buddy", "Golden Retriever")
    
    print(f"Animal: {generic_animal}")
    print(f"Dog: {my_dog}")
    print(f"Dog says: {my_dog.speak()}")
    print(f"Description: {my_dog.description}")


# ============================================================================
# 5. FILE HANDLING & CONTEXT MANAGERS
# ============================================================================

def file_handling_demo():
    """Demonstrates file handling and context managers"""
    print("\n=== File Handling & Context Managers ===")
    
    # Writing to file with context manager (automatically closes file)
    filename = "sample.txt"
    
    with open(filename, 'w') as file:
        file.write("Hello, Python!\n")
        file.write("This is a sample file.\n")
    
    # Reading from file
    with open(filename, 'r') as file:
        content = file.read()
        print(f"File content:\n{content}")
    
    # Clean up
    import os
    os.remove(filename)
    print("File cleaned up")


# ============================================================================
# 6. ERROR HANDLING
# ============================================================================

def error_handling_demo():
    """Demonstrates Python's exception handling"""
    print("\n=== Error Handling ===")
    
    def divide_numbers(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print("Error: Cannot divide by zero!")
            return None
        except TypeError:
            print("Error: Invalid input types!")
            return None
        finally:
            print("Division operation completed")
    
    # Test different scenarios
    print(f"10 / 2 = {divide_numbers(10, 2)}")
    print(f"10 / 0 = {divide_numbers(10, 0)}")
    print(f"'10' / 2 = {divide_numbers('10', 2)}")


# ============================================================================
# 7. GENERATORS & ITERATORS
# ============================================================================

def generator_demo():
    """Demonstrates generators for memory-efficient iteration"""
    print("\n=== Generators & Iterators ===")
    
    # Generator function
    def countdown(n):
        while n > 0:
            yield n
            n -= 1
    
    print("Countdown from 5:")
    for num in countdown(5):
        print(num, end=" ")
    print()
    
    # Generator expression
    squares_gen = (x**2 for x in range(5))
    print(f"Squares generator: {list(squares_gen)}")


# ============================================================================
# 8. PRACTICAL EXAMPLE: WEB SCRAPING
# ============================================================================

def web_scraping_example():
    """Practical example: Simple web scraping simulation"""
    print("\n=== Practical Example: Data Processing ===")
    
    # Simulate web data (normally you'd use requests library)
    import json
    
    # Sample JSON data (like from an API)
    sample_data = '''
    {
        "users": [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "London"},
            {"name": "Charlie", "age": 35, "city": "Tokyo"}
        ]
    }
    '''
    
    # Parse and process data
    data = json.loads(sample_data)
    
    # Extract information using list comprehensions
    names = [user["name"] for user in data["users"]]
    ages = [user["age"] for user in data["users"]]
    cities = [user["city"] for user in data["users"]]
    
    print(f"Names: {names}")
    print(f"Average age: {sum(ages) / len(ages):.1f}")
    print(f"Cities: {set(cities)}")
    
    # Filter users over 30
    mature_users = [user for user in data["users"] if user["age"] > 30]
    print(f"Users over 30: {[user['name'] for user in mature_users]}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("Python Examples for Expert Programmers")
    print("=" * 50)
    
    # Run all demonstrations
    basic_syntax_demo()
    data_structures_demo()
    function_features_demo()
    oop_demo()
    file_handling_demo()
    error_handling_demo()
    generator_demo()
    web_scraping_example()
    
    print("\n" + "=" * 50)
    print("Examples completed! Try running: python python_examples.py")
