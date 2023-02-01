import glob
import os

from analyzer import Analyzer
from generator import Generator

class NameGenerator:
    def __init__(self):
        self.generators = []
        self.input_files = []
        abs = os.path.abspath(os.getcwd())


        for root, dirs, files in os.walk(os.path.abspath("./input")):
           for file in files:
               print(root+"/"+file)
               self.input_files.append(root+"/"+file)

    def create_generator(self, name, depth, filenames, optional_values, lmin, lmax):
        print(str(filenames[0]))
        analyzer = Analyzer(depth)
        analyzer.build_model(filenames, "")
        generator = Generator(
            name,
            depth,
            minlen = lmin,
            maxlen = lmax,
            m_init = analyzer.m_init,
            m_mid = analyzer.m_mid,
            m_tail = analyzer.m_tail)
        self.generators.append(generator)
        return generator.name


    def get_generators(self):
        return [ x for x in map(lambda x: x.name, self.generators)]

    def get_input_files(self):
        return self.input_files

    def generate_names(self, generator_name, amount, depth, lmin, lmax):
        gi = self.get_generators().index(generator_name)
        names = []
        g = self.generators[gi]
        g.depth = depth
        g.minlen = lmin
        g.maxlen = lmax
        for i in range(0, amount):
            name = g.generate_name() + ',\n'
            names += name
        return names

