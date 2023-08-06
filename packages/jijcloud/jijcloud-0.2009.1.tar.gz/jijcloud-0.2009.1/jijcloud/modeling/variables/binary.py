from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO
from jijcloud.modeling.variables.variable import Variable
import pyqubo


class Binary(Variable, ToPyQUBO):

    def to_pyqubo(self):
        """Convert to pyqubo.Binary class

        Returns:
            pyqubo.Binary: pyqubo object
        """
        return pyqubo.Binary(self.label)