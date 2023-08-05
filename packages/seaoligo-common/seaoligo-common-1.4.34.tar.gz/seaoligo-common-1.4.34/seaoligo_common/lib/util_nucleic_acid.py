import math


def calc_tm(seq: str) -> float:
    # Define the concentration and buffer condition
    con = 0.25  # in μM
    na = 150  # in mM

    # Enthalpy terms for dinucleotides
    enthalpy_dna_rna = {
        'AA': -11.5, 'AC': -7.8, 'AG': -7.0, 'AT': -8.3,
        'CA': -10.4, 'CC': -12.8, 'CG': -16.3, 'CT': -9.1,
        'GA': -8.6, 'GC': -8.0, 'GG': -9.3, 'GT': -5.9,
        'TA': -7.8, 'TC': -5.5, 'TG': -9.0, 'TT': -7.8
    }

    # Initialization and calculation of enthalpy
    ent_0 = 1.9 * 1000
    for pos in range(0, len(seq) - 1):
        ent_0 += enthalpy_dna_rna[seq[pos:pos + 2]] * 1000

    # Entropy terms for dinucleotides
    entropy_dna_rna = {
        'AA': -36.4, 'AC': -21.6, 'AG': -19.7, 'AT': -23.9,
        'CA': -28.4, 'CC': -31.9, 'CG': -47.1, 'CT': -23.5,
        'GA': -22.9, 'GC': -17.1, 'GG': -23.2, 'GT': -12.3,
        'TA': -23.2, 'TC': -13.5, 'TG': -26.1, 'TT': -21.9
    }

    # Initialization and calculation of entropy
    etr_0 = -3.9
    for pos in range(0, len(seq) - 1):
        etr_0 += entropy_dna_rna[seq[pos:pos + 2]]

    # Tm calculation
    tm = ent_0 / (etr_0 + 1.987 * math.log(con * 10 ** -6)) - 273.15

    # Correction for monovalent ion
    gc_content = (seq.count('G') + seq.count('C')) / len(seq)
    tm = (1 / (tm + 273.15) + ((4.29 * gc_content - 3.95) * math.log(na / 1000)
                               + 0.94 * (math.log(na / 1000)) ** 2) * 10 ** -5) ** -1 - 273.15

    return tm
