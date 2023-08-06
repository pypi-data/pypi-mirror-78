import pyqubo
from jijcloud.modeling.express import Express
from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO

class Constraint(Express, ToPyQUBO):
    def __init__(self, term, label, condition='== 0'):
        # TODO: change constructor to (self, term, condition, constant, label)
        super().__init__([term])
        self.label = label
        self.condition = condition.split(' ')[0]
        self.constant = condition.split(' ')[1]

    def to_pyqubo(self, **indices) -> pyqubo.Express:
        term = self.children[0].to_pyqubo(**indices)
        return pyqubo.Constraint(term, self.label)