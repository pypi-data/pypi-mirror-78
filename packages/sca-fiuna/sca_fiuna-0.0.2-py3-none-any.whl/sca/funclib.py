import cmath
from control.matlab import TransferFunction

def phase(V):
    """
    function phase:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on radian

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    if not type(V) == type([]): V = [V]
    fases = [cmath.phase(Poriginal) for Poriginal in V]
    if len(fases) == 1: return fases[0]
    return fases

def phased(V):
    """
    function phased:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on deg

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    fases = phase(V)
    if not type(fases) == type([]): fases = [fases]
    fases = [fase*180/cmath.pi for fase in fases]
    if len(fases) == 1: return fases[0]
    return fases

def evals(G, Pole):
    """
    function evals:

    Receive a TransferFunction and one complex number s and evaluate in

    G: TransferFunction
    Pole: complex number

    return the complex number of result

    """
    return G.horner(Pole)[0][0]
