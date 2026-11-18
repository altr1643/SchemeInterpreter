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
    
# Helper function to convert Scheme expressions to string representation
def scheme_str(expr):
    # if expr is nil, return empty list
    if expr is nil:
        return "()"
    # if expr is Pair, return string representation
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
    
    return
if __name__ == "__main__":
    main()