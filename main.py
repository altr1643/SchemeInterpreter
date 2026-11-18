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
    def __repr__(self):
        return f"Pair({repr(self.first)}, {repr(self.second)})"
    
    def __str__(self):
        return f"({self.first} . {self.second})"

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

def main():
    #print("Scheme Interpreter")
    # test
    #empty = Nil()
    #first_pair = Pair(1, nil)
    #second_pair = Pair(2, first_pair)

    #print(empty)
    #print(first_pair)
    #print(len(first_pair))
    return
if __name__ == "__main__":
    main()