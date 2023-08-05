from functools import reduce

import numpy as np

from mygrad.operation_base import BroadcastableOp, Operation

__all__ = [
    "Add",
    "Subtract",
    "Multiply",
    "Divide",
    "Reciprocal",
    "Power",
    "Square",
    "Positive",
    "Negative",
    "AddSequence",
    "MultiplySequence",
]


class Add(BroadcastableOp):
    def __call__(self, a, b):
        """ Performs 'add' forward-pass: f(a,b) -> a + b

            Parameters
            ----------
            a : mygrad.Tensor
            b : mygrad.Tensor

            Returns
            -------
            out : numpy.ndarray """

        self.variables = (a, b)
        out = a.data + b.data
        return out

    def backward_var(self, grad, index, **kwargs):
        return grad


class Subtract(BroadcastableOp):
    def __call__(self, a, b):
        """ f(a,b) -> a - b

            Parameters
            ----------
            a : mygrad.Tensor
            b : mygrad.Tensor

            Returns
            -------
            out : numpy.ndarray """
        self.variables = (a, b)
        out = a.data - b.data
        return out

    def backward_var(self, grad, index, **kwargs):
        if index == 0:
            return grad
        else:
            return -grad


class Multiply(BroadcastableOp):
    def __call__(self, a, b):
        """ Parameters
            ----------
            a : mygrad.Tensor
            b : mygrad.Tensor"""
        self.variables = (a, b)
        out = a.data * b.data
        return out

    def backward_var(self, grad, index, **kwargs):
        a, b = self.variables
        if index == 0:  # backprop through a
            return grad * b.data
        elif index == 1:  # backprop through b
            return grad * a.data


class Divide(BroadcastableOp):
    def __call__(self, a, b):
        """ f(a, b) -> a / b"""
        self.variables = (a, b)
        out = a.data / b.data
        return out

    def backward_var(self, grad, index, **kwargs):
        a, b = self.variables
        if index == 0:  # backprop through a
            return grad / b.data
        else:  # broadcast through b
            return -grad * a.data / (b.data ** 2)


class Reciprocal(BroadcastableOp):
    def __call__(self, a):
        """ f(a) -> 1 / a"""
        self.variables = (a,)
        return np.reciprocal(a.data)

    def backward_var(self, grad, index, **kwargs):
        a = self.variables[index]
        return -grad * np.reciprocal(a.data ** 2)


class Power(BroadcastableOp):
    def __call__(self, a, b):
        """ f(a, b) -> a ** b

            Parameters
            ----------
            a: mygrad.Tensor
            b: mygrad.Tensor"""
        self.variables = (a, b)
        out = a.data ** b.data
        return out

    def backward_var(self, grad, index, **kwargs):
        a, b = self.variables
        x, y = a.data, b.data
        if index == 0:
            return grad * y * (x ** np.where(y, (y - 1), 1))
        else:
            return grad * (x ** y) * np.log(np.where(x, x, 1))


class Square(Operation):
    def __call__(self, a):
        """ f(a) -> a ** 2

            Parameters
            ----------
            a : mygrad.Tensor"""
        self.variables = (a,)
        return np.square(a.data)

    def backward_var(self, grad, index, **kwargs):
        return grad * 2 * self.variables[index].data


class Positive(Operation):
    """ f(a) = +a """

    def __call__(self, a, where=True):
        """
        Parameters
        ----------
        a: mygrad.Tensor

        where : array_like, optional
            Values of True indicate to calculate the ufunc at that position,
            values of False indicate to leave the value in the output alone."""
        self.variables = (a,)
        self.conf = dict(where=where)
        return np.positive(a.data, where=where)

    def backward_var(self, grad, index, **kwargs):
        return np.positive(grad, **self.conf)


class Negative(Operation):
    """ f(a) = -a """

    def __call__(self, a, where=True):
        """
        Parameters
        ----------
        a : mygrad.Tensor

        where : array_like, optional
            Values of True indicate to calculate the ufunc at that position,
            values of False indicate to leave the value in the output alone."""
        self.variables = (a,)
        self.conf = dict(where=where)
        return np.negative(a.data, where=where)

    def backward_var(self, grad, index, **kwargs):
        return np.negative(grad, **self.conf)


class AddSequence(BroadcastableOp):
    """Performs f(a, b, ..., z) = a + b + ... + z"""

    def __call__(self, *input_vars):
        assert len(input_vars) > 1, "`add_sequence` requires at least two operands"
        self.variables = input_vars
        out = sum(var.data for var in input_vars)
        return out

    def backward_var(self, grad, index, **kwargs):
        return grad


class MultiplySequence(BroadcastableOp):
    """ Performs f(a, b, ..., z) = a * b * ... * z"""

    def __call__(self, *input_vars):
        self.variables = input_vars
        assert 2 <= len(self.variables)

        out = reduce(lambda x, y: x * y, (var.data for var in input_vars))
        self._iszero = np.any(out == 0)
        return out

    def backward(self, grad, *, graph, **kwargs):
        """ Back-propagates the gradient through all of the operation's inputs. This needs to be updated
            by an operation if that operation takes more than 2 Tensor arguments."""
        if not self._iszero:
            self._product = grad * reduce(
                lambda x, y: x * y, (var.data for n, var in enumerate(self.variables))
            )
        else:
            self._product = None
        super().backward(grad, graph=graph, **kwargs)

    def backward_var(self, grad, index, **kwargs):
        var = self.variables[index]
        if not self._iszero:
            return self._product / var.data
        else:
            return grad * reduce(
                lambda x, y: x * y,
                (var.data for n, var in enumerate(self.variables) if n != index),
            )
