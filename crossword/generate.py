import sys

from crossword import Variable, Crossword
from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        # for i, j in self.domains.items():
        #     print(i, j)

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        # DeprecationWarning: textsize is deprecated and will be removed in Pillow 10 (2023-07-01). 
                        # Use textbbox or textlength instead.
                        # w, h = draw.textsize(letters[i][j], font=font)
                        bbox = draw.textbbox((0, 0), letters[i][j], font=font)
                        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())
    
    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        temp_domain = deepcopy(self.domains)

        for var, words in temp_domain.items():
            for x in words:
                if len(x) != var.length:
                    self.domains[var].remove(x)

        # print("/////////new")
        # for var, words in self.domains.items():
        #     print(var, "///", words)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False

        revision = False
        x_intersect, y_intersect = self.crossword.overlaps[x, y]

        # Set of available chars for y's location
        y_chars = set()
        for word in self.domains[y]:
            y_chars.add(word[y_intersect])

        # Check if x's domain's words have a char that can fit
        temp_xdomain = deepcopy(self.domains[x])
        for word in temp_xdomain:
            if word[x_intersect] not in y_chars:
                self.domains[x].remove(word)
                revision = True

        # print("intersect", self.crossword.overlaps[x, y])    
        # print("new x", self.domains[x])
        # print("y", self.domains[y], y_chars)
        # print()

        return revision
    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """    

        # queue = all arcs in csp
        # while queue non-empty:
            # (X, Y) = Dequeue(queue)
            # if Revise(csp, X, Y):
                # if size of X.domain == 0:
                    # return false
                # for each Z in X.neighbors - {Y}:
                    # Enqueue(queue, (Z,X))
        # return true

        # Create initial queue
        if arcs == None:
            queue = []
            for keys, overlaps in self.crossword.overlaps.items():
                if overlaps is not None:
                    queue.append([keys[0], keys[1]])
        else:
            queue = arcs

        # for i, j in self.domains.items():
        #     print("before", i, j)

        # # Enforce arc consistency
        # # Any time a domain is changed, this may change the requirements for another domain
        # #   Therefore, loop until no changes are made                
        while len(queue) > 0:
            var1, var2 = queue.pop()

            if self.revise(var1, var2) == True:
                # No solution
                if not self.domains[var1]:
                    return False
                
                # Each domain change may cause other domains to be affected
                for variable in (self.crossword.neighbors(var1) - {var2}):
                    queue.append((variable, var1))                
                
        # for i, j in self.domains.items():
        #     print("after", i, j)

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.domains) == len(assignment):
            return True
        else:
            return False
             

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        word_set = set()
        for var, word in assignment.items():

            # Check word length
            if var.length != len(word):
                return False
            
            # Check distinct
            if word in word_set:
                return False
            else:
                word_set.add(word)

            # Check conflict
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    var_overlap, neighbor_overlap = self.crossword.overlaps[var, neighbor]
                    if assignment[var][var_overlap] != assignment[neighbor][neighbor_overlap]:
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        elim_dict = {}
        for word in self.domains[var]:
            # print("word", word)
            # Count number of eliminations for each word
            for neighbor in self.crossword.neighbors(var):
                var_intersect, neighbor_intersect = self.crossword.overlaps[var, neighbor]
                # print("intersect", var_intersect, neighbor_intersect)

                elim_count = 0
                for neigh_word in self.domains[neighbor]:
                    # print("word, neigh_words", word, neigh_word)
                    if word[var_intersect] != neigh_word[neighbor_intersect]:
                        elim_count += 1
                elim_dict.update({word: elim_count})

        sorted_keys = sorted(elim_dict, key=lambda x: elim_dict[x])

        return sorted_keys
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
  
        choice = None
        for var in self.domains:
            if var in assignment:
                continue
            
            # Init choice
            if choice is None:
                choice = var

            # Choose var with the smallest domain
            elif len(self.domains[var]) < len(self.domains[choice]):
                choice = var

            # If tie, choose the variable with the highest degree (most neighbors)
            elif len(self.domains[var]) == len(self.domains[choice]):
                if len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(choice)):
                    choice = var

        return choice


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # Terminal condition
        if self.assignment_complete(assignment) == True:
            return assignment
        # for i, j in self.domains.items():
        #     print(i, "///", j)

        # Recursively choose a word for the next node
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value

            # If consistent, continue recursively with current comp
            if self.consistent(assignment) == True:
                result = self.backtrack(assignment)
                if result != None:
                    return result
                
            # Else, remove newest addition and
            # continue the 'for loop' to try new comp
            else:
                assignment.pop(var)
            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print("(╯°□°)╯︵ ┻━┻")
    # structure = "data/structure1.txt"
    # words = "data/words1.txt"
    # output = "output.png"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
