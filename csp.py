
# defining CSP

class CSP:
    """
    A class used to represent a CSP problem.

    ...

    Attributes
    ----------
    variables : list
        Vertives of the graph
    neighbors : dictionary
        Represents neighbors of each vertex
    domain : list
        All possible values(colors)
    
    Methods
    -------
    def constraint(self, color1, color2)

    def add_val(self, var, val, assignment)

    def remove_val(self, var, assignment)

    def not_conflict(self, var, val, assignment)

    def conflict_num(self, var, val, assignment):

    """

    def __init__(self, variables, domain, neighbors):
       
        self.variables = variables
        self.neighbors = neighbors
        self.domain = domain
        
    def constraint(self, color1, color2):
        """Checks if constraint is satisfied for given values """ 
        
        return color1 != color2    
     

    def add_val(self, var, val, assignment):
        """adds new {var: val} pair to assignment"""

        assignment[var] = val

        #apply AC-3 after assigning value - MAC algorithm
        AC3(self)

    def remove_val(self, var, assignment):
        """removes {var: val} pair from assignment"""

        if var in assignment:
            del assignment[var]

    def not_conflict(self, var, val, assignment):
        """Checks if there is a conflict in values of assignment """ 

        is_not_conf = True
        for var2 in self.neighbors[var]:

            #get value of var2
            val2 = assignment.get(var2, None)

            #check is constraint is satisfied
            #if not and value is not None return False
            if val2 != None and not self.constraint(val, val2):
                is_not_conf = False
                break
        return is_not_conf        
    

    def conflict_num(self, var, val, assignment):
        """Returns number of the conflicting values of assignment """ 

        num_conf = 0
        for var2 in self.neighbors[var]:
            val2 = assignment.get(var2, None)
            
            #check is constraint is satisfied
            #if not and value is not None add 1 to counter
            if val2 != None and not self.constraint(val, val2):
                num_conf += 1
        return num_conf
        

# Backtracking Search
                
def backtracking_search(csp):
    """Backtracking search for graph coloring problem""" 

    global assignment
    return recursive_backtracking(assignment, csp)

def recursive_backtracking(assignment, csp):
    """Recursive depth-first search for backtracking""" 

    #check if assignment is complete
    if len(assignment) == len(csp.variables):
        return assignment

    var = select_unassigned_variable(assignment, csp)

    for val in order_domain_values(var, assignment, csp):
        if csp.not_conflict(var, val, assignment):
            
            #if no conflict assign new value to var
            csp.add_val(var, val, assignment)
            result = recursive_backtracking(assignment, csp)
            
            #if result is failure, remove value
            if result is not None:
                return result
        csp.remove_val(var, assignment)

    return None

# selecting variable - heuristics
def mrv(variables):
    """minimum remaining values (MRV) heuristic to select variable"""

    min_var = variables[0] 
    min_rem = rem_legal_values(csp, min_var, assignment)
    
    #find variable with minimum remaining values
    for var in variables:
        rem_vals = rem_legal_values(csp, var, assignment)
        if rem_vals < min_rem:
            min_var, min_rem = var, rem_vals
    return min_var

def rem_legal_values(csp, var, assignment):
    """Returns number for remaining possible "legal" values"""
    
    num = 0
    
    #calculate number of remaining variables
    for color in csp.domain[var]:
        if csp.conflict_num(var, color, assignment) == 0:
            num += 1
    return  num

def select_unassigned_variable(assignment, csp):
    """selects next unassigned variable using MRV"""

    #get list of unassigned variables
    unassigned = [var for var in csp.variables
                  if var not in assignment] 
    return mrv(unassigned)


# selecting value - heuristics

def lcv(var, domain):
    """least-constraining-value heuristic to select value"""

    #sort domain by number of conflicts
    return sorted(domain, key=lambda val: csp.conflict_num(var, val, assignment))


def order_domain_values(var, assignment, csp):
    """orders values in a specific way to select value using LCV"""

    #get domain for given variable
    domain = csp.domain[var]

    return lcv(var, domain)


#  AC-3 constraint propagation (MAC)

def AC3(csp):
    """ Maintaining Arc Consistency for constraint propagation"""
    
    #simulate queue using list
    queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    while queue:

        #get element from start
        (Xi, Xj) = queue.pop(0)
        if remove_inconsistent_values(csp, Xi, Xj):
            for Xk in csp.neighbors[Xi]:

                #add element to the end of queue
                queue.append((Xk, Xi))

     

def remove_inconsistent_values(csp, Xi, Xj):
    """Removes inconsistent values from domain"""

    removed = False

    for x in csp.domain[Xi]:

        #check if there is a non-conflicting value y for x
        is_not_conflict = False
        for y in csp.domain[Xj]:
            if csp.constraint(x, y): 
                is_not_conflict = True
                break
        
        #if no non-conflicting val left, remove x from domain
        if is_not_conflict == False :
            csp.domain[Xi].remove(x)
            removed = True
            
    return removed

    
# reading from input file

def file_reader(filepath):
    """Reads input file and generates data"""
        
    global edges
    global vertices
    global color_num
    
    with open(filepath, "r") as filestream:
        for line in filestream:

            if line.startswith("#"):
                continue

            #get number of colors
            elif line.startswith("colors"):
                line = line.rstrip('\n')
                color_num = int(line.split("=")[1])

            #get edges and vertices
            else:
                line = line.rstrip('\n')
                start, end = map(int, line.split(","))
                
                vertices.add(start)
                vertices.add(end)

                edges.append((start,end))
                edges.append((end, start))



def plot_grap():
    """
    Plots visualizations of resulting colored graph

    Note: MAX number of colors - 6
    If number of colors will be more than 6, all colors 
    greater and equal to 6 will be assigned as gray
    
    """

    import networkx as nx
    import matplotlib.pyplot as plt
    
    #create graph from edge list
    g = nx.from_edgelist(edges)

    #assign colors to vertices 
    for i in range(min(vertices),max(vertices)+1):
        g.nodes[i]['color'] = assignment[i]

    #create color map for visualization
    color_map = []
    for i in range(min(vertices),max(vertices)+1):
        if g.nodes[i]['color'] == 1:
            color_map.append('blue')
        elif g.nodes[i]['color'] ==2: 
            color_map.append('green') 
        elif g.nodes[i]['color'] ==3:
            color_map.append('red')
        elif g.nodes[i]['color'] == 4:
            color_map.append('pink')
        elif g.nodes[i]['color'] == 5:
            color_map.append('purple')
        else:
            color_map.append('gray')  

    #visualize graph
    nx.draw(g, node_color=color_map,with_labels=True)
    plt.show()

# main program - solving graph coloring
                    
if __name__ == '__main__':

    #initialize edges, vertices, etc.
    edges = []
    vertices = set()
    color_num = 0
    domain = dict()
    assignment = dict()
    inputpath = input('Enter your file path:  ')
    
    file_reader(inputpath)
    
    #generate neighbors dictionary
    neighbors = dict()
    vertices = sorted(list(vertices))
    for vertex in vertices:
        neighbors[vertex] = []
        domain[vertex] = list(range(1, color_num + 1))

    for edge in edges:
        neighbors[edge[0]].append(edge[1])

    #initialize CSP problem with given values
    csp = CSP(vertices, domain, neighbors)


    print(backtracking_search(csp))

    # to see graph visualization uncomment below:
    #plot_grap()


