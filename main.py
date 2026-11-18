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
    
    return
if __name__ == "__main__":
    main()