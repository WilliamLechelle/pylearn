from theano import tensor

class MeanSquaredReconstructionError(object):
    def __call__(self, model, X):
        return ((model.reconstruct(X) - X) ** 2).sum(axis=1).mean()


class MeanBinaryCrossEntropy(object):
    def __call__(self, model, X):
        return (
            - X * tensor.log(model.reconstruct(X)) -
            (1 - X) * tensor.log(1 - model.reconstruct(X))
        ).sum(axis=1).mean()


#class MeanBinaryCrossEntropyTanh(object):
#     def __call__(self, model, X):
#        X = (X + 1) / 2.
#        return (
#            tensor.xlogx.xlogx(model.reconstruct(X)) +
#            tensor.xlogx.xlogx(1 - model.reconstruct(X))
#        ).sum(axis=1).mean()


class ModelMethodPenalty(object):
    def __init__(self, method_name):
        self._method_name = method_name

    def __call__(self, model, X):
        if hasattr(model, self._method_name):
            return getattr(model, self._method_name)(X)
        else:
            raise ValueError("no such method '%s' for model %s" %
                             (str(self._method_name), str(model)))

class ScaleBy(object):
    def __init__(self, cost, coefficient):
        self._cost = cost
        self._coefficient = coefficient

    def __call__(self, model, X):
        return self._coefficient * self._cost(model, X)
