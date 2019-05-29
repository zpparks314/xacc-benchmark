from pelix.ipopo.decorators import ComponentFactory, Property, Requires, Provides, \
    Validate, Invalidate, Instantiate
from hamiltonian_generator import HamiltonianGenerator
import ast, xacc
import xaccvqe as vqe
from xaccvqe import PauliOperator
from openfermion.transforms import get_fermion_operator, reverse_jordan_wigner

@ComponentFactory("deuteronH2_hamiltonian_generator_factory")
@Provides("hamiltonian_generator_service")
@Property("_hamiltonian_generator", "hamiltonian_generator", "deuteronH2")
@Property("_name", "name", "deuteronH2")
@Instantiate("deuteronH2_hamiltonian_generator_instance")
class DeuteronH2(HamiltonianGenerator):

    def generate(self, inputParams):
        ham = PauliOperator(5.906709445) + \
                PauliOperator({0: 'X', 1: 'X'}, -2.1433) + \
                PauliOperator({0: 'Y', 1: 'Y'}, -2.1433) + \
                PauliOperator({0: 'Z'}, .21829) + \
                PauliOperator({1: 'Z'}, -6.125)

        qubitOp = vqe.XACC2QubitOperator(ham)
        fermiOp = reverse_jordan_wigner(qubitOp)
        src = vqe.get_fermion_compiler_source(fermiOp)

        inputParams['rdm-source'] = src
        return ham
