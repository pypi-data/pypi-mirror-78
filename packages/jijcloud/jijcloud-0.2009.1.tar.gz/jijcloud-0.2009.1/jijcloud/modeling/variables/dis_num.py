from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO
import pyqubo

class DisNumVar(ToPyQUBO):
    def __init__(self, label:str, lower:float =0.0, upper:float =1.0, bits:int=1):
        """Discreate number variable

        Args:
            label (str): [description]
            lower (float, optional): [description]. Defaults to 0.0.
            upper (float, optional): [description]. Defaults to 1.0.
            bits (int, optional): [description]. Defaults to 1.
        """

        self.label = label
        self.lower = lower
        self.upper = upper
        self.bits = bits

    def to_pyqubo(self, label: str = None):
        var_lable = self.label if label is None else label
        var_lable = var_lable + '[{}]'
        coeff = (self.upper - self.lower)/(2**self.bits-1)
        return coeff * sum(2**i*pyqubo.Binary(var_lable.format(i)) for i in range(self.bits)) + self.lower