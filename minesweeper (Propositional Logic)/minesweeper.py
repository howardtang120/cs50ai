import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __sub__(self, other):
        cells = self.cells - other.cells
        count = self.count - other.count
        return(Sentence(cells, count))
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If count of the set of cells == count of mines
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If there are no mines in the set of cells
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width
        self.count = 0

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # A set of safe moves
        self.safe_moves = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.count += 1
        self.moves_made.add(cell)
        self.mark_safe(cell)

        nearby = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # If mine is already confirmed
                if (i, j) in self.mines:
                    count -= 1
                    continue
                if (i, j) not in (self.safes):
                # Boundary check
                    if 0 <= i < self.height and 0 <= j < self.width:               
                        nearby.add((i,j))

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        new_sentence = Sentence(nearby, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
        self.knowledge_organize()
        self.safe_moves = self.safes - self.moves_made
        self.debuggy()

    def knowledge_organize(self):
        """
        Cleaning up the knowledge base
        1) Removes empty sentences
        2) Sort sentences with no mines
        3) Sort sentences full of mines
        4) Restructure sentences that are subsets of another
        Loops until no changes are made to the knowledgebase,
            because each change might enable a new change
        """
        change = True
        calculating = "Calculating"
        # Keeps looping until no changes are made to KB
        while change == True:
            calculating += "."
            print(calculating)
            change = False
            for sentence in self.knowledge:
                # Remove empty sentences
                if not sentence.cells:
                    self.knowledge.remove(sentence)
                    change = True
                    break
                # Mark safe cells
                safes = Sentence.known_safes(sentence)
                if safes:
                    change = True
                    for safe in list(safes):
                        self.mark_safe(safe)    
                    break
                # Mark mines
                mines = Sentence.known_mines(sentence)
                if mines:
                    change = True
                    for mine in list(mines):
                        self.mark_mine(mine)
                    break   

            # Handle simple calculations before inference calculations
            if change == True:
                continue
            change = self.inference()                

    def inference(self):
        """        
        If a set is a subset of another,
        Subtract the cells and count from the superset
        """
        for pair in itertools.combinations(self.knowledge, 2):
            if pair[0].cells.issubset(pair[1].cells):
                new = pair[1] - pair[0]
                print(f"\n~~inference~~\n{pair[0]}\n{pair[1]}\n>>>new\n{new}\n")
                self.knowledge.remove(pair[1])
                self.knowledge.append(new)
                return True
            elif pair[1].cells.issubset(pair[0].cells):
                new = pair[0] - pair[1]
                print(f"\n~~inference~~\n{pair[1]}\n{pair[0]}\n>>>new\n{new}\n")
                self.knowledge.remove(pair[0])
                self.knowledge.append(new)
                return True
            
        return False
                

    def debuggy(self):
        """
        4 debuggyn
        """
        print("\nKnowledgebase version", self.count)
        print("~~Knowledge~~~")
        for sentence in self.knowledge:
            print(sentence)
        print("\n~~~Safe cells~~~")
        for i in sorted(self.safes):
            print(i, end=" ")
        print("\n~~~Is mine~~~")
        for i in sorted(self.mines):
            print(i, end=" ")
        print("\n~~~Safe moves~~~")
        for i in sorted(self.safe_moves):
            print(i, end = " ")
        print()

    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safe_moves:
            return random.choice(list(self.safe_moves))
        return None
    
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            if (i, j) not in (self.moves_made, self.mines):
                return (i, j)
