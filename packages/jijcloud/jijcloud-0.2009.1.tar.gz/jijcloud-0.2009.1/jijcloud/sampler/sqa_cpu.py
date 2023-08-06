from jijcloud.sampler import JijCloudSampler
from jijcloud.sampler.model_post import JijModelSamplerInterface


class JijSQASampler(JijCloudSampler, JijModelSamplerInterface):
    hardware = 'cpu'
    algorithm = 'sqa'

    def sample(self, bqm, beta=1.0, gamma=1.0, trotter=4,
               num_reads=1, num_sweeps=100, timeout=None, sync=True):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta (float, optional): inverse temperature. Defaults to 1.0.
            gamma (float, optional): minimum beta (initial beta in SA).
            trotter (int, optional): number of trotter slices. should be even.
            num_reads (int, optional): number of samples. Defaults to 1.
            num_sweeps (int, optional): number of MonteCarlo steps
            timeout (float, optional): number of timeout for post request. Defaults to None.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        # number of trotter should be even
        # since c++ implementation
        if trotter % 2 == 1:
            raise ValueError('trotter number should be even.')

        return super().sample(
            bqm, num_reads, num_sweeps,
            gamma=gamma, trotter=trotter, beta=1.0, 
            timeout=timeout,
            sync=sync
        )
