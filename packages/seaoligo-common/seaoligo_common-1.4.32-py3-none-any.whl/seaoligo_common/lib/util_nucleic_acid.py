from typing import Tuple
import math
from Bio.Seq import Seq


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


def calc_delta_g(seq: str) -> float:
    # ΔG terms for dinucleotides
    delta_g_dna_dna = {
        'AA': -1.00, 'AC': -1.44, 'AG': -1.28, 'AT': -0.88,
        'CA': -1.45, 'CC': -1.84, 'CG': -2.17, 'CT': -1.28,
        'GA': -1.30, 'GC': -2.24, 'GG': -1.84, 'GT': -1.44,
        'TA': -0.58, 'TC': -1.30, 'TG': -1.45, 'TT': -1.00
    }

    # Initialization and calculation of enthalpy
    delta_g = 0

    if seq[0] == 'A' or seq[0] == 'T':
        delta_g += 1.03
    elif seq[0] == 'G' or seq[0] == 'C':
        delta_g += 0.98

    if seq[-1] == 'A' or seq[-1] == 'T':
        delta_g += 1.03
    elif seq[-1] == 'G' or seq[-1] == 'C':
        delta_g += 0.98

    for pos in range(0, len(seq) - 1):
        delta_g += delta_g_dna_dna[seq[pos:pos + 2]]

    return delta_g


def calc_hairpin(seq: str) -> Tuple[str, float]:
    code = ['-'] * len(seq)  # Initialize code display
    delta_g = 0  # Threshold ΔG
    max_bp_count = int(math.floor((len(seq) - 3) / 2))  # Maximum number of base pairs possible

    for length in range(3, max_bp_count):  # For all possible bp lengths in the hairpin
        for i in range(0, len(seq) - 3 - length * 2 + 1):  # For all possible starting positions of strand #1
            for j in range(i + length + 3, len(seq) - length + 1):  # For all possible starting positions of strand #2
                # Filter if first and second strands are complementary
                if seq[i:i + length] == str(Seq(seq[j:j + length]).reverse_complement()):
                    motif = seq[i:i + length]
                    # Filter if the ΔG is less than that of the previous iteration
                    if calc_delta_g(motif) < delta_g:
                        delta_g = calc_delta_g(motif)
                        code = ['-'] * len(seq)
                        code[i:i + length] = ['('] * length
                        code[j:j + length] = [')'] * length

    code = ''.join(code)

    return code, delta_g
