"""
Author:   Karl Sims. 2017.
Aim:      Implement 3D version of Conway's Game of Life for LED cubes. 
          Make colors more interesting also.

Alternative rules for 'Life' in 3 dimensions used here are as follows:

    1) Any live cell with fewer than 3 live neighbors dies, 
       as if caused by underpopulation.
    2) Any live cell with more than 5 live neighbors dies, 
       as if by overcrowding.
    3) Any live cell with 3, 4, 5 live neighbors lives on 
       to the next generation.
    4) Any live cell with exactly 5 live neighbors develops a
        mutation causing it to change color. This is carried by 
        all its direct descendents.
    5) Any dead cell with exactly 5 live neighbors becomes 
       a live cell. 

Infomation on classic version of 'Life': https://goo.gl/CR7fbR
pdf Essay on 'Life' in 3 dimensions: https://goo.gl/j6BGaA

To run individually:
Local simulation:       python cube.py --pattern life
Mini cube over network: python cube.py -P cuboid:3000 --pattern life
"""
import random


class Pattern(object):
    
    def init(self):
        self.double_buffer = True # Need this for irl cube.
        self.life = CubeLife(size=self.cube.size, 
                             limit=150, 
                             new_state=random_blast,
                             next_generation=next_generation_3d)
        return 1.0/8 # time between ticks. 8 fps ?

    def tick(self):
        self.cube.clear() # Make sure cubes are cleared or problems in simulator.
        for ((x, y, z), color), just_restarted in self.life.successors():
            if just_restarted:
                raise StopIteration
            self.cube.set_pixel((x, y, z), color)



class CubeLife(object):
    """CubeLife(): class object instances will iniailise a generator function for
    infinite generations of life. Only external method 'successors' is used as a 
    iterator and will run through each game and generation sequentially."""
    def __init__(self, size, limit, new_state, next_generation):
        self.size = size
        self.limit = limit
        self.new_state = new_state
        self.next_gen = next_generation
        self.count = 0
        self.patterns = []
        self.state = set()
        self.color1, self.color2 = new_colors()
        # Initalise life generator. Round 1 will be blank for 6 iterations.
        self.generations = self.__life()

    def successors(self):
        """Iterator: Returning data structure is for each iteration is a 
        tuple of 2 tuples of 3 ints: ((x, y, z), (r, g, b)) these are constained 
        to the cube size or rgb value limits."""
        (next_gen, just_restarted) = next(self.generations)
        for (pos, mute) in next_gen:
            yield (((pos, self.color2) if mute else (pos, self.color1)), just_restarted)

    def __life(self):
        "Iterator: yield whole generations of life forever."
        while True:
            if self.__done():
                self.__restart()
                yield (self.state, True) # Just restarted? True
            else:
                self.state = self.next_gen(self.state, self.size)
                self.count += 1
                self.patterns.append(self.state)
                yield (self.state, False) # Just restarted? False

    def __restart(self):
        "Set initial values for each new game of life"
        self.count = 0
        self.patterns = []
        self.color1, self.color2 = new_colors()
        self.state = self.new_state(self.size)

    def __done(self):
        """Return whether or not the current game of life should end. 
        We don't want infinite loops, solid states, or state with 0
        population. Catching all infinite loops poses a prediction problem
        so just set an iteration limit."""
        if len(self.patterns) >= 6:
            self.patterns.pop(0)
            return (self.count >= self.limit or 
                    self.patterns[-3] == self.state)
        return False


# Generating new Generations for life:

def next_generation_3d(state, size):
    """nextGeneration(set: state, int: size): {((ints: x, y, z), bool)...};
    Following the game rules at the top of this file page. return a successive 
    state in life from any given state on a finite plane. Adapted original function
    for 3d with extra mutation attributes."""
    new_state = set()
    for cell in state:
        cell_neighbours = neighbours_3d(cell)
        if len(state & cell_neighbours) in (3, 4): # rule 3 / (1 & 2)
            new_state.add(cell)
        elif len(state & cell_neighbours) is 5: # rule 4 they get sick
            c, _ = cell
            new_state.add((c, True))
        for cn in cell_neighbours: # rule 4
            if len(state & neighbours_3d(cn)) is 5: 
                new_state.add(cn)
    return constrain(new_state, size)


def neighbours_3d(cell):
    """neighbours(tuple: cell): set: {(ints: x, y, z), ...}; returns a set of 
    co-ordinates +/- 1 from a given position."""
    (x, y, z), mute = cell
    return set(((x + dx, y + dy, z + dz), mute) for dx, dy, dz in deltas_3d)


deltas_3d = [(x, y, z) for x in range(-1, 2) 
                       for y in range(-1, 2)
                       for z in range(-1, 2) 
                       if not (x == y == z == 0)]


def constrain(S, s):
    return set(((x, y, z), mute) for (x, y, z), mute in S
               if 0 <= x < s and 0 <= y < s and 0 <= z < s)


# Generating inital states:

def random_blast(size):
    """For generating intial states in game of life. return a random state 
    with a concentrated bundle of likely points in the center of the cube 
    and a scattering around the the rest of the state space."""
    edge = int(size/2.2)
    bundle = set(((__rand(edge, size - edge-1), 
                   __rand(edge, size - edge-1),
                   __rand(edge-1, size - edge)), False)
                 for position in range(8))
    scatter = set(((__rand(0,size-1), 
                    __rand(0,size-1), 
                    __rand(0,size-1)), False) 
                  for x in range(__rand(size, size*3)))
    return (bundle | scatter)

__rand = random.randint


# Color Utilies:

def new_colors(): return random.choice(material_colors)

material_colors = [
    # colors vary across different simulations.

    ((213,0,0), (48,79,254)), # red, blue.
    ((48,79,254), (213,0,0)), # blue, red.
    ((245, 0, 87), (66, 165, 245)), # pink/puple, blue.
    
    ((170,0,255), (0,145,234)), # puple, blue.
    ((0,145,234), (170,0,255)),
    ((46,125,50), (255,143,0)),
    ((200, 83, 1), (98, 0, 234)), # comes out yellow, purple.

    ((100, 221, 23), (170,0,255)), # green, purple.

    ((38, 198, 218), (249, 168, 37)), # blue orangey yellow.

    ((96,125,139), (139,195,74)),  # lime and blue grey
    ((98,0,234), (0,121,107)),     # deep purple teal
    ((0,191,165), (98,0,234)),     # dark teal deep purple
]





