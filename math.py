import math
import cmath
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from abc import ABC, abstractmethod

class PolynomialModel(ABC):
    @abstractmethod
    def train(self, x, y):
        pass
    @abstractmethod
    def predict(self, x):
        pass
    @abstractmethod
    def get_params(self):
        pass

class LinearPolynomialModel(PolynomialModel):
    def __init__(self):
        self.m = None

    def train(self, x, y):
        x = np.array(x).flatten()
        y = np.array(y).flatten()
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        cov_xy = np.mean((x - x_mean) * (y - y_mean))
        var_x = np.mean((x - x_mean)**2)
        a = cov_xy / var_x
        b = y_mean - a * x_mean
        self.m = (a, b)

    def predict(self, x):
        a, b = self.m
        x = np.array(x)
        return a * x + b

    def get_params(self):
        return self.m

class QuadraticPolynomialModel(PolynomialModel):
    def __init__(self):
        self.m = None

    def train(self, x, y):
        x = np.array(x).flatten()
        y = np.array(y).flatten()
        matrix = np.vander(x, N=3)
        theta = np.linalg.inv(matrix.T @ matrix) @ matrix.T @ y
        self.m = tuple(theta)

    def predict(self, x=None):
        a, b, c = self.m
        
        def solve_quadratic(a, b, c):
            delta = b**2 - 4*a*c
            if delta < 0: return None
            elif delta == 0: return (-b / (2*a), )
            else:
                sqrt_delta = math.sqrt(delta)
                return ((-b + sqrt_delta) / (2*a), (-b - sqrt_delta) / (2*a))

        def quadratic_function(x, a, b, c):
            return a * x**2 + b * x + c

        if x is None:
            return solve_quadratic(a, b, c)
        else:
            if isinstance(x, (list, tuple, np.ndarray)):
                return np.array([quadratic_function(xi, a, b, c) for xi in x])
            return quadratic_function(x, a, b, c)

    def get_params(self):
        return self.m

class CubicPolynomialModel(PolynomialModel):
    def __init__(self):
        self.m = None

    def train(self, x, y):
        x = np.array(x).flatten()
        y = np.array(y).flatten()
        matrix = np.vander(x, N=4)
        theta = np.linalg.inv(matrix.T @ matrix) @ matrix.T @ y
        self.m = tuple(theta)

    def predict(self, x=None):
        a, b, c, d = self.m
        if x is not None:
            x = np.array(x)
            return a*x**3 + b*x**2 + c*x + d
        return None

    def get_params(self):
        return self.m

class PolynomialParameterFinder:
    def __init__(self, degree):
        self.degree = degree
        self.model = None
        self.x = None
        self.y = None

    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        self.x = df.iloc[:, 0].values
        self.y = df.iloc[:, 1].values

    def run(self):
        indices = np.arange(len(self.x))
        np.random.shuffle(indices)
        split = int(0.8 * len(self.x))
        train_idx, test_idx = indices[:split], indices[split:]
        
        self.x_train, self.x_test = self.x[train_idx], self.x[test_idx]
        self.y_train, self.y_test = self.y[train_idx], self.y[test_idx]

        if self.degree == 1: self.model = LinearPolynomialModel()
        elif self.degree == 2: self.model = QuadraticPolynomialModel()
        elif self.degree == 3: self.model = CubicPolynomialModel()
        
        self.model.train(self.x_train, self.y_train)

    def plot_results(self):
        y_pred = self.model.predict(self.x_test)
        plt.scatter(self.x_test, self.y_test, color='blue', label='Actual')
        plt.scatter(self.x_test, y_pred, color='red', label='Predicted')
        plt.legend()
        plt.title(f'Polynomial Degree {self.degree}')
        plt.show()
