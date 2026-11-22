# Alan Trang
# This program implements a simple Scheme interpreter in Python. It defines basic data structures and functions to represent Scheme objects.

# Empty list in Scheme()
class Nil:
    def __repr__(self):
        return "nil"
    def __str__(self):
        return "()"
    def __len__(self):
        return 0
    def map(self, func):
        return self

nil = Nil()

# Pair class in Scheme
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    # Sets the first and second elements of the pair and returns the pair object as a string representation
    def __repr__(self):
        return f"Pair({repr(self.first)}, {repr(self.second)})"

    # Returns the string representation of the pair in Scheme format
    def __str__(self):
        s = "(" + scheme_str(self.first)
        rest = self.second

        while isinstance(rest, Pair):
            s += " " + scheme_str(rest.first)
            rest = rest.second
        if rest is not nil:
            s += " . " + scheme_str(rest)

        return s + ")"

    # Calculates obj length in scheme
    def __len__(self):
        # n keeps track of how many counted elements, rest keeps track of point in pair
        n, rest = 1, self.second

        # Checks if second element is a pair, if so, increments n and sets rest to second element of pair
        while isinstance(rest, Pair):
            n += 1
            rest = rest.second
        # Checks if rest is nil, if not, err occurs since length is only defined for proper lists
        if rest is not nil:
            raise TypeError("Length is only defined for proper lists")
        return n

    # handles a list that contains elements, applies the given function to first element, then calls map on rest of list
    def map(self, func):
        return Pair(func(self.first), self.second.map(func))
    
# Helper function to convert Scheme expressions to string representation
def scheme_str(expr):
    # if expr is nil, return empty list
    if expr is nil:
        return "()"
    # Convert python bools to Scheme bools
    elif expr is True:
        return '#t'
    elif expr is False:
        return '#f'

    # If expr is Pair, return string representation
    elif isinstance(expr, Pair):
        return str(expr)
    
    # if expr is neither, return using Python's regular str()
    else:
        return str(expr)

# Helper function to create scheme list from elements
def scheme_list(*elements):
    # start with empty list
    result = nil
    
    # Iterate through elements in reverse order and create pairs
    for elements in reversed(elements):
        result = Pair(elements, result)

    # return the resulting scheme list
    return result

# Buffer class to manage tokens in a list and keeps track of current position in the list
class Buffer:
    # Initializes buffer object with list of tokens and sets position to 0
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    # Pops first token from buffer and increments position, returning popped token
    def pop_first(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    # returns current token in buffer without modifying position
    def current(self):
        return self.tokens[self.pos]
    # Checks for more tokens in buffer by comparing current position with length of tokens list
    def has_next(self):
        return self.pos < len(self.tokens)

# Helper function to tokenize a line of scheme code by adding spaces around parans and splitting line into list of tokens    
def tokenize(line):
    return line.replace("(", " ( ").replace(")", " ) ").split()

# Helper function to convert individual tokens from strings into python vals
def atomize(token):
    # If token is boolean, return corresponding Python bool vals
    if token == "#t":
        return True
    elif token == '#f':
        return False

    # If token is number, return corresponding int or float vals, otherwise return as string
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token

# Takes tokens from Buffer and turns them into Scheme expressions, returning resulting expressions
def scheme_read(src):
    # Checks if there are more tokens if buffer, if not, raises Syntax Error for unexpected EOF
    if not src.has_next():
        raise SyntaxError("Unexpected EOF while reading")
    # Pops first token from buffer
    token = src.pop_first()

    # If token is open parans, calls read_tail to read rest of expression
    if token == "(":
        return read_tail(src)
    # if token is close parans, raises Syntax Error for unexpected close parans
    elif token == ")":
        raise SyntaxError("Unexpected )")
    # If token is neither, calls atomize to convert token into Python val and returns it
    else:
        return atomize(token)

# Reads contents of a scheme list after scheme_read encounters open parans
def read_tail(src):
    # If no more tokens in buffer, raises Syntax Error for unexpected EOF
    if not src.has_next():
        raise SyntaxError("Unexpected EOF while reading")

    # If current token is close parans, pops from buffer and returns nil to indicate end of list
    if src.current() == ")":
        src.pop_first()
        return nil
    # Calls scheme_read to read first element of list, then recursively calls read_tail to read rest of list and returns Pair
    first = scheme_read(src)
    rest = read_tail(src)
    return Pair(first, rest)

# Frame class to represent an environment frame in Scheme. Stores variable bindings and reference to parent frame for nested scopes
class Frame:
    # Initializes Frame obj
    def __init__(self, parent = None):
        # Empty dictionary to store variables in the frame
        self.bindings = {}
        # Reference to parent frame for nested scopes
        self.parent = parent
    
    # Stores variable and value into the frame's dictionary
    def define(self, symbol, val):
        self.bindings[symbol] = val

    # Retrieves the value associated with a variable name
    def lookup(self, symbol):
        # Checks if symbol is in current frame's bindings
        if symbol in self.bindings:
            return self.bindings[symbol]
        # If no symbol, checks if parent frame exists, if so, recursively calls lookup on parent frame
        elif self.parent is not None:
            return self.parent.lookup(symbol)
        # If symbol is not found in current frame or parent frames, raises NameError for unbound variable
        else:
            raise NameError(f"Unbound variable: {symbol}")
    # Returns string representation of Frame
    def __repr__(self):
        return f"Frame({self.bindings})"

    # When Scheme function is called, creates own enviroment to store params and arg values
    def make_child_frame(self, formals, vals):
        
        # Create child frame connected to current frame
        child = Frame(self)

        # Assign parameters to corresponding arguments
        while isinstance(formals, Pair) and isinstance(vals, Pair):
            child.define(formals.first, vals.first)
            formals = formals.second
            vals = vals.second
        # Handle variable number of arguments
        if isinstance(formals, str):
            child.define(formals, vals)
        
        # Check for mismatched argument counts
        elif formals is not nil or vals is not nil:
            raise TypeError("argument count mismatch")

        # Return child when completed
        return child

# Stores a primitive procedure in Scheme
class PrimProcedure:
    # Initializes PrimProcedure object with a function and optional name, and environment
    def __init__(self, func, name = None, use_env = False):
        self.func = func
        self.name = name
        self.use_env = use_env
    # Returns string representation of PrimProcedure object
    def __repr__(self):
        return f"PrimProcedure({self.name})"
    

# Represents Lambda procedure in Scheme that lets users define themselves in scheme
class LambdaProcedure:
    # Initializes Lambda Procedure object with parameters, body, and environment
    def __init__(self, params, body, env):
        # Parameter names
        self.params = params
        # Expression to execute
        self.body = body
        # Environment where function was defined
        self.env = env

    # Returns string representation of LambdaProcedure object
    def __repr__(self):
        return f"LambdaProcedure({self.params}, {self.body})"

# Stores an expression and environment so it can be evaluted later for tail-call optimization/deep recursion
class Thunk:
    # Receives expression and environment
    def __init__ (self, expr, env):
        self.expr = expr
        self.env = env
    # Returns string representation of the expression held
    def __repr__(self):
        return f"Thunk({self.expr})"

# returns values that don't need further evaluation
def is_self_eval(expr):
    return isinstance(expr, (int, float, bool)) or (isinstance(expr, str) and expr.startswith('"'))

# Takes scheme expression and environment, then determines the meaning and evaluates 
def scheme_eval(expr, env, tail = False):
    while True:
        # Numbers and bools return themselves
        if is_self_eval(expr):
            return expr
        # Symbols and strings are looked up in environment
        if isinstance(expr, str):
            return env.lookup(expr)
        # Bad input
        if not isinstance(expr, Pair):
            raise SyntaxError("Malformed Expression")
    
        # Stores operator and operands
        first, rest = expr.first, expr.second

        # return expression as written in scheme
        if first == "quote":
            return rest.first

        # if special form in scheme
        if first == "if":
            test = scheme_eval(rest.first, env)

            # if evals to true
            if test is not False:
                expr = rest.second.first
            # if evals to false
            else:
                expr = rest.second.second.first
            continue
        
        # cond special form in scheme
        if first == "cond":
            # Loops through each condition clause
            while rest is not nil:
                # get current clause
                clause = rest.first

                # Get condition from the clause
                test = clause.first

                # Check if condition is "else" or evaluates to true
                if test == "else":
                    test_val = True
                else:
                    test_val = scheme_eval(test, env)

                if test_val is not False:
                    # If clause has no body, return condition
                    if clause.second is nil:
                        return test_val

                    #Turn clause body into a begin expression
                    expr = Pair("begin", clause.second)
                    break

                # Move to next condition clause
                rest = rest.second

            # If no condition matched
            else:
                return None
            
            continue

        # And special form in scheme
        if first == "and":
            if rest is nil:
                return True
            # evals each expression except last one
            while rest.second is not nil:
                if scheme_eval(rest.first, env) is False:
                    return False
                
                rest = rest.second
            
            # If no expressions remain    
            if rest is nil:
                return True
            
            #Evaluates final expression in the main loop
            expr = rest.first
            continue

        # Or special form in scheme
        if first == "or":
            if rest is nil:
                return False
            
            # Evaluate each expression except last one
            while rest.second is not nil:
                value = scheme_eval(rest.first, env)

                # Return immediately if val is not False
                if value is not False:
                    return value
                
                # next expression
                rest = rest.second
            
            # If no expressions remain, return False
            if rest is nil:
                return False

            # Evaluate last expression in the main loop
            expr = rest.first
            continue

        # define special form in scheme
        if first == "define":
            target = rest.first

            # Defines a variable. Evaluates the assigned expression and stores result in the environment
            if isinstance(target, str):
                val = scheme_eval(rest.second.first, env)
                env.define(target, val)
                return target

            # Defines a function in scheme. Creates a LambdaProcedure containing parameters, function body, and current environment
            elif isinstance(target, Pair):
                name = target.first
                params = target.second
                body = rest.second

                procedure = LambdaProcedure(params, body, env)
                env.define(name, procedure)

                return name
            
        # Lambda special form in scheme
        if first == "lambda":
            params = rest.first
            body = rest.second

            return LambdaProcedure(params, body, env)

        # Begin special form in scheme
        if first == "begin":
            if rest is nil:
                return None
            # Evaluate every expression except last
            while rest.second is not nil:
                scheme_eval(rest.first, env)
                rest = rest.second

            # Evaluate final expression in main loop
            expr = rest.first
            continue

        # Let special form in scheme
        if first == "let":
            bindings = rest.first
            body = rest.second

            # Create a new child environment
            new_env = Frame(env)

            # Evaluate and store each variable binding
            while bindings is not nil:
                binding = bindings.first
                symb = binding.first
                val = scheme_eval(binding.second.first, env)

                new_env.define(symb, val)
                bindings = bindings.second

            expr = Pair("begin", body)
            env = new_env
            continue

        # Evaluate operator to get to procedure
        procedure = scheme_eval(first, env)

        # Evaluate all arguments
        args = rest.map(lambda arg: scheme_eval(arg, env))

        # Apply procedure to the evaluated arguments
        return scheme_apply(procedure, args, env)

# Takes procedure and its args, then executes procedure
def scheme_apply(procedure, args, env, tail = False):
    # Handle python procedures
    if isinstance(procedure, PrimProcedure):
        arguments = []

        # Convert scheme args into Python list
        while args is not nil:
            arguments.append(args.first)
            args = args.second

        # Pass environment if the procedure requires it
        if procedure.use_env:
            arguments.append(env)

        return procedure.func(*arguments)
    # Handles user defined lambda procedures
    elif isinstance(procedure, LambdaProcedure):
        # Create child frame with parameters and arguments
        new_env = procedure.env.make_child_frame(procedure.params, args)

        # Evaluates procedure body in new environment
        return scheme_eval(Pair("begin", procedure.body), new_env)

# Creates global environment for Scheme
def create_global_frame():
    env = Frame()

    # Subtraction helper function
    def subtract(first, *rest):
        if not rest:
            return -first

        for num in rest:
            first -= num
        return first

    # Multiplication helper function
    def multiply(*args):
        result = 1
        for num in args:
            result *= num
        return result

    # Division helper function
    def divide(first, *rest):
        if not rest:
            return 1 / first
        for num in rest:
            first /= num
        return first 
    
    # +, -, *, / primitive procedures
    env.define("+", PrimProcedure(lambda *args: sum(args), name = "+"))
    env.define("-", PrimProcedure(subtract, name = "-"))
    env.define("*", PrimProcedure(multiply, name = "*"))
    env.define("/", PrimProcedure(divide, name = "/"))

    return env
    
#TODO: Implement the following classes and methods for the Scheme interpreter
# Comparison Primitives ( =, <, >, <=, >= )
# List Primitives ( cons, car, cdr, list, length, null )
# Type-checking and Utility Primitives ( number?, bool?, Pair? not, abs, min, max )
# Global environment initialization
# REPL
# Thunk functionality
def main():
    # tests
    #empty = Nil()
    #first_pair = Pair(1, nil)
    #second_pair = Pair(2, first_pair)

    #print(empty)
    #print(first_pair)
    #print(len(first_pair))

    #empty = nil
    #list1 = scheme_list(1)
    #list2 = scheme_list(1, 2)
    #list3 = scheme_list(1, 2, 3)

    #print(empty)
    #print(list1)
    #print(list2)
    #print(list3)

    #print(len(list1))
    #print(len(list2))
    #print(len(list3))

    #tokens = tokenize("(+ 1 2)")
    #src = Buffer(tokens)
    #result = scheme_read(src)
    #print(result)
    #print(repr(result))

    # Frame test
    #env = Frame()
    #env.define("x", 10)
    #env.define("y", 20)

    #print(env.lookup("x"))
    #print(env.lookup("y"))

    # parent Frame test
    #child = Frame(env)
    #child.define("z", 30)
    #print(child.lookup("z"))
    #print(child.lookup("x"))

    # PrimProcedure test
    #prim = PrimProcedure(lambda x, y: x + y, "+")
    #print(prim)

    # LambdaProcedure test
    #procedure = LambdaProcedure(
    #    scheme_list("x"),
    #    scheme_list("+", "x", 10),
    #    env
    #)
    #print(procedure)

    #Thunk test
    #thunk = Thunk(scheme_list("+", 1, 2), Frame())
    #print(thunk)

    global_env = create_global_frame()

    # Basic arith test with manually created Pair objects
    print(scheme_eval(Pair("+", scheme_list(10, 5)), global_env))
    print(scheme_eval(Pair("-", scheme_list(10, 5)), global_env))
    print(scheme_eval(Pair("*", scheme_list(10, 5)), global_env))
    print(scheme_eval(Pair("/", scheme_list(10, 5)), global_env))

    # Test multiple arguments
    print(scheme_eval(Pair("+", scheme_list(1, 2, 3, 4)), global_env))
    print(scheme_eval(Pair("-", scheme_list(20, 3, 2)), global_env))
    print(scheme_eval(Pair("*", scheme_list(2, 3, 4)), global_env))

    # Test single argument
    print(scheme_eval(Pair("-", scheme_list(5)), global_env))
    print(scheme_eval(Pair("/", scheme_list(4)), global_env))

    # Test for scheme-style bool returns
    print(scheme_str(True))
    print(scheme_str(False))
    print(scheme_str(10))


    return
if __name__ == "__main__":
    main()