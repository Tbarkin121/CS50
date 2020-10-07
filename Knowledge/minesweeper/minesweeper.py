import itertools
import random
from copy import deepcopy


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

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (len(self.cells) == self.count):
            return self.cells
        else:
            return set()
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0):
            return self.cells
        else:
            return set()
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

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
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #Construct a new sentence to add
        print("Cell Click : " + str(cell))
        print("Cell Count : " + str(count))
        print("")
        new_cells = set()
        for i in range(-1 + cell[0], 2 + cell[0]) :             # (-1, 0, 1) + cell[0]
            if (i >= 0 and i < self.height):                         #Checks if indice is on the board
                for j in range(-1 + cell[1], 2 + cell[1]):      # (-1, 0, 1) + cell[1]
                    if (j >= 0 and j < self.width):                  #Checks if indice is on the board
                        new_cells.add((i, j))
                        # if ( (new_cell not in self.mines) and (new_cell not in self.safes) ):
        mine_intersection = new_cells.intersection(self.mines)
        safe_intersection = new_cells.intersection(self.safes)
        
        # print(new_cells)
        if(len(new_cells) > 0):
            new_sentence = Sentence(new_cells.difference(mine_intersection).difference(safe_intersection), count - len(mine_intersection))
            self.knowledge.append(new_sentence)
        print("Knowledge Base with New Sentence")
        for idx in range(len(self.knowledge)):
            print(self.knowledge[idx])

        max_iter = 5
        iter = 0
        while(True):
            iter += 1
            if(iter > max_iter):
                input()
            #(Find and Mark) (Safe Spots and Mines)
            Modified_Knowledgebase = False
            for i in range(len(self.knowledge)):
                safe_cells = deepcopy(self.knowledge[i].known_safes())
                if(len(safe_cells) > 0):
                    print("Safe Cells : ")
                    print(safe_cells)
                for ele in safe_cells:
                    self.mark_safe(ele)
                    Modified_Knowledgebase = True

                mine_cells = deepcopy(self.knowledge[i].known_mines())
                if(len(mine_cells) != 0):
                    print("Mine Cells : ")
                    print(mine_cells)
                for ele in mine_cells:
                    self.mark_mine(ele)
                    Modified_Knowledgebase = True
                

            #removing empty sets from the knowledge base that resulted from mine and safe cells being removed
            while Sentence(set(), 0) in self.knowledge:
                self.knowledge.remove(Sentence(set(), 0))
            print("Updated Knowledge Base (Removed Safe, Mines, and Empty Sets)")
            for idx in range(len(self.knowledge)):
                print(self.knowledge[idx])

            print("Check the knowledge for new inferences")
            inferred_sentences = []
            for i in range(len(self.knowledge)):
                for j in range(len(self.knowledge)):
                    if (i != j):
                        # print("Sentence Comp {i : " + str(i) + ", j : " + str(j) + "}")
                        # print(self.knowledge[i])
                        # print(self.knowledge[j])
                        #Mark duplicate entries for removal 
                        if(self.knowledge[i] == self.knowledge[j]):
                            print("Found a duplicate entry!")
                            self.knowledge[j].cells = set()
                            self.knowledge[j].count = 0
                        
                        elif (self.knowledge[j].cells.issubset(self.knowledge[i].cells) and len(self.knowledge[j].cells)>0 ):
                            inferred_sentence = Sentence(self.knowledge[i].cells.difference(self.knowledge[j].cells), self.knowledge[i].count - self.knowledge[j].count)
                            if (inferred_sentence not in self.knowledge):
                                inferred_sentences.append(inferred_sentence)
                                print("Found an inference :")
                                print(inferred_sentence)

            while Sentence(set(), 0) in self.knowledge:
                self.knowledge.remove(Sentence(set(), 0))

            
            
            for ele in inferred_sentences:
                self.knowledge.append(ele)
                Modified_Knowledgebase = True
                    
            # input()
            if(not Modified_Knowledgebase):

                print("Nothing New To Add")
                print("Save Cells : ")
                print(self.safes.difference(self.moves_made))
                print("Mine Cells : ")
                print(self.mines)
                print("~~~~~~~~~~~~~~~~~~~")
                break




        
        # for i in range(len(self.knowledge)):
        #     print("Knowledge Sentence : ")
        #     print(self.knowledge[i])
        #     print("New Sentence : ")
        #     print(new_sentence)

        #     inferred_sentence = Sentence(set(), 0)
        #     if (new_sentence.cells.issubset(self.knowledge[i].cells)):
        #         inferred_sentence.cells = self.knowledge[i].cells
        #         for ele in new_sentence.cells:
        #             inferred_sentence.cells.remove(ele)
        #         inferred_sentence.count = self.knowledge[i].count - new_sentence.count
        #     if (self.knowledge[i].cells.issubset(new_sentence.cells)):
        #         inferred_sentence.cells = new_sentence.cells
        #         for ele in self.knowledge[i].cells:
        #             inferred_sentence.cells.remove(ele)
        #         inferred_sentence.count = new_sentence.count - self.knowledge[i].count
        #     print("Inferred Sentence : ")
        #     print(inferred_sentence)
        #     print("~~~~~~~~~~~~~~~~~~~")
            

        

        
        

        #Process New Sentence? 

        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes.difference(self.moves_made)
        print("Safe New Moves :")
        print(safe_moves)
        if (len(safe_moves) > 0):
            safe_move = random.sample(safe_moves, 1)
            return safe_move[0]
        else:
            return None

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("Mines?")
        print(self.mines)
        # input()
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i,j))
        random_moves = all_moves.difference(self.mines).difference(self.safes)
        print("Random Moves?")
        print(random_moves)
        if (len(random_moves) > 0):
            random_move = random.sample(random_moves, 1)
            return random_move[0]
        else:
            return None

        # raise NotImplementedError
