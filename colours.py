import argparse
import logging

class Graph:

    def __init__(self):
        self.adjacent = {}
        self.degree_sequences = {}
        self.sort_keys = {}

    def set_vertices(self):
        self.vertices = list(self.adjacent.keys())

    def sort_vertices(self):
        degree_base = 0
        for vertex in graph.vertices:
            neighbours = graph.adjacent[vertex]
            if len(neighbours) > degree_base:
                degree_base = len(neighbours)
        degree_base += 1

        for vertex in graph.vertices:
            sequence = self.degree_sequences[vertex]
            exponents = range(len(sequence))
            sort_key = 0
            for exponent, degree in enumerate(sequence):
                product = degree * (degree_base ** exponent)
                sort_key += product
            self.sort_keys[vertex] = sort_key

        self.vertices.sort(key = lambda vertex: self.sort_keys[vertex])

    def __str__(self):
        s = '----------- Graph -----------\n'
        for vertex in self.vertices:
            neighbours = graph.adjacent[vertex]
            degree_sequence = self.degree_sequences[vertex]
            sort_key = self.sort_keys[vertex]
            s += f'Vertex {vertex}: {neighbours}\n'
            s += f'  has degree sequence {degree_sequence}\n'
            s += f'  has sort key {sort_key}\n'
        return s

def parse(file):
    '''
        If file is a file, this function consumes the file, that is, it can only be called once.
        If it is called a second time, the function will continue to read the file,
        where it left off last time, namely at the end and read nothing.
    '''
    graph = None
    for line in file:
        if line[0] == 'c': continue

        if line[-1] == '\n':
            line = line[:-1]
        info = line.split(' ')
        if line[0] == 'p':
            if len(info) < 3:
                logging.error(f'The problem line has too few words!')
                return None
            num_vertices = int(info[2])
            graph = Graph()
            for vertex in range(num_vertices):
                graph.adjacent[vertex+1] = []
        else:
            if graph is None:
                logging.error(f'Encountered a non-comment line before the problem line!')
                return None
            tail, head = int(info[0]), int(info[1])
            graph.adjacent[tail].append(head)
            graph.adjacent[head].append(tail)
    return graph

def refine_step(graph):
    next_degree_sequences = {}
    for vertex in graph.vertices:
        next_degree_sequences[vertex] = []

    for vertex in graph.vertices:
        my_sequence = graph.degree_sequences[vertex]
        for neigh in graph.adjacent[vertex]:
            neigh_sequence = next_degree_sequences[neigh]
            neigh_sequence.extend(my_sequence)

    for vertex in graph.vertices:
        sorted_sequence = sorted(next_degree_sequences[vertex])
        graph.degree_sequences[vertex] = sorted_sequence

def refine_degree_sequences(graph):
    same_degree = len(graph.adjacent[1])
    for vertex in graph.vertices:
        neighbours = graph.adjacent[vertex]
        graph.degree_sequences[vertex] = [len(neighbours)]
        graph.sort_keys[vertex] = len(neighbours)
        if same_degree != len(neighbours):
            same_degree = None

    if same_degree is not None:
        logging.warning(f'Input graph is {same_degree}-regular; so will not be ordered.')

    logging.debug(f'Refining local_structure of graph\n{graph}')
    graph.sort_vertices()
    logging.debug(f'Initial sort\n{graph}')

    i = 1
    last_ordering = None
    while last_ordering != graph.vertices:
        last_ordering = list(graph.vertices)
        refine_step(graph)
        graph.sort_vertices()
        logging.info(f'{i}th refinement step completed.')
        logging.debug(f':\n{graph}')
        i += 1

    logging.info(last_ordering)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('graphpath')
    parser.add_argument('--verbose', '-v', action='count')
    args = parser.parse_args()

    log_levels = {
        None: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }
    if args.verbose is not None and args.verbose >= len(log_levels):
        args.verbose = len(log_levels)-1
    logging.basicConfig(format='%(message)s', level=log_levels[args.verbose])

    with open(args.graphpath) as f:
        graph = parse(f)
    graph.set_vertices()
    refine_degree_sequences(graph)
