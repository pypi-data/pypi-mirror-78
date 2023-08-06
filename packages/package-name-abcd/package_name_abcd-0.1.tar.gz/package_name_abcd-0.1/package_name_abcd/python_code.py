import pandas as pd
import numpy as np

class Filter():
    
    def __init__(self, df, cols, values):
        self.cols = cols
        self.values = values
        self.df = df
   
    def process(self):
        if len(self.cols) > 0:
            for i, c in enumerate(self.cols):
                self.df = self.df[self.df[c]==self.values[i]]
        return self.df
    
    def __repr__(self):
        self.df = self.process(self.df)
        return "Number of records {}".format(len(self.df))