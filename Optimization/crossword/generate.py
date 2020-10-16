import sys

from crossword import *


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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        print("Entered enforce_node_consistency Function")
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # print("self.domains")
        # print(self.domains)
        for mystery in self.domains:
            # print("!!!!!!!!!!!!")
            # print(mystery)
            # print(self.domains[mystery])
            keep_list = set()
            while self.domains[mystery]:
                word = self.domains[mystery].pop()
                if(len(word) == mystery.length):
                    keep_list.add(word)
            for word in keep_list:
                self.domains[mystery].add(word)
            # print(self.domains[mystery])

        # raise NotImplementedError

    def revise(self, x, y):
        print("Entered revise Function")
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """ 
        keep_list_x = set()
        keep_list_y = set()
        domain_x = self.domains[x].copy()
        domain_y = self.domains[y].copy()
        overlaps = self.crossword.overlaps
        overlap = overlaps[(x, y)]
        # print(self.domains[x].copy)
        revision = False
        if overlap is not None:
            while domain_x:
                word_x = domain_x.pop()
                # print(word_x)
                while domain_y:
                    word_y = domain_y.pop()
                    # print(word_y)
                    keep_list_y.add(word_y)
                    if word_x[overlap[0]] != word_y[overlap[1]]:
                        keep_list_x.add(word_x)
                for word in keep_list_y:
                    domain_y.add(word)
            
            remove_list = self.domains[x].difference(keep_list_x)
            # print("DOMAIN")
            # print(self.domains[x])
            # print("KEEP")
            # print(keep_list_x)
            # print("REMOVE")
            # print(remove_list)
            for word in remove_list:
                self.domains[x].remove(word)
                revision = True

        return revision
        # raise NotImplementedError

    def ac3(self, arcs=None):
        print("Entered ac3 Function")
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        revise = False
        if arcs is None:
            arcs = set()
            for arc in self.crossword.overlaps:
                arcs.add(arc)

        while arcs:
            arc = arcs.pop()
            # print("arc")
            # print(arc)
            revise = self.revise(arc[0], arc[1])
            if revise:
                arcs.update(self.crossword.neighbors(arc[0]))
            if (self.domains[arc[0]] is None):
                return False
        #     print("revise")
        #     print(revise)
        #     print("arc")
        #     print(arc)
        #     input()

        # print("")
        # print("")
        # print("arcs")
        # print(arcs)
        # print("")
        # print("")

        return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        print("Entered assignment_complete Function")
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        print("Assignment")
        print(assignment)
        for var in assignment:
            if assignment[var] is None:
                return False
        return self.consistent(assignment)

        # raise NotImplementedError

    def consistent(self, assignment):
        print("Entered consistent Function")
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        print("assignment")
        print(assignment)
        overlaps = self.crossword.overlaps
        value_set = set()
        for variable in assignment:     
            #checking overlaps with neighbors
            neighbors = self.crossword.neighbors(variable)
            for neighbor in neighbors:
                overlap = overlaps[(variable, neighbor)]
                if (neighbor in assignment):
                    print("var 1 overlap letter")
                    print(assignment[variable][overlap[0]])
                    print("var 2 overlap letter")
                    print(assignment[neighbor][overlap[1]])
                    if (assignment[variable][overlap[0]] is not assignment[neighbor][overlap[1]]):
                        return False
                
            print("neighbors")
            print(neighbors)

            #checking that the assignment is the correct length for the variable
            if (variable.length != len(assignment[variable])):
                return False

            #the set to check for distinct variables later
            value_set.add(assignment[variable])

        #Checking that all variables are distinct
        #these should be the same length unless two or more variables share an value
        if( len(value_set) is not len(assignment)): 
            return False
        
        return True

        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        print("Entered order_domain_values Function")
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        print("Entered select_unassigned_variable Function")
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # print("Assignment")
        # print(assignment)
        variables = set()
        variables.update(self.domains.keys())
        unassigned_variables = set()
        unassigned_variables.update(variables.difference(assignment.keys()))
        # print("All Variables")
        # print(variables)
        # print("Unassigned Variables")
        # print(unassigned_variables)

        var_with_smallest_domain = set()
        for variable in unassigned_variables:
            if ( len(var_with_smallest_domain) > 0):
                test_var = var_with_smallest_domain.pop()
                if ( len(self.domains[variable]) < len(self.domains[test_var]) ):
                    var_with_smallest_domain.clear()
                    var_with_smallest_domain.add(variable)
                elif (len(self.domains[variable]) == len(self.domains[test_var])):
                    var_with_smallest_domain.add(test_var)
                    var_with_smallest_domain.add(variable)
                else:
                    var_with_smallest_domain.add(test_var)
            else:
                var_with_smallest_domain.add(variable)

        # finalist_with_most_neighbors = set()
        # for variable in finalist_with_most_neighbors:
        #     if ( len(finalist_with_most_neighbors) > 0):
        #         test_var = finalist_with_most_neighbors.pop()
        #         if ( len(self.domains[variable]) < (self.domains[test_var]) ):
        #             finalist_with_most_neighbors.clear()
        #             finalist_with_most_neighbors.add(variable)
        #         elif (len(self.domains[variable] == len(self.domains[test_var]))):
        #             finalist_with_most_neighbors.add(test_var)
        #             finalist_with_most_neighbors.add(variable)
        #         else:
        #             finalist_with_most_neighbors.add(finalist_with_most_neighbors)
        #     else:
        #         finalist_with_most_neighbors.add(variable)
        
        if( len(var_with_smallest_domain) > 0):
            return var_with_smallest_domain.pop()

        return None

        # raise NotImplementedError

    def backtrack(self, assignment):
        print("Entered backtrack Function")
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if len(assignment) == len(self.domains):
            return assignment

        # Try a new variable
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        return None

        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

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
