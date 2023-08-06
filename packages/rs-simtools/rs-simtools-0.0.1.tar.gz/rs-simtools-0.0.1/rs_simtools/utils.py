
import numpy as np
from scipy import signal
from simtk.openmm import unit


aa_residues = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]

water_residues = ['HOH', 'TIP3', 'TIP3P', 'SPCE', 'SPC', 'TIP4PEW', 'WAT', 'OH2', 'TIP']

lipid_residues = ['AR', 'CHL', 'DHA', 'LA', 'MY', 'OL', 'PA', 'PC', 'PE', 'PGR', 'PH-', 'PS', 'SA', 'SM', 'ST']


def select_atoms(parmed_structure, keyword_selection=None, ligand_resname=None, resid_selection=None):

    lig_residues = ['LIG', 'UNL']

    if ligand_resname:
        lig_residues.append(ligand_resname)

    if keyword_selection == None and resid_selection == None:
        raise ValueError('Must specify either keyword selection or resid_selection')

    final_list = []

    if resid_selection:
        # split up the selection syntax
        resid_list = resid_selection.split()
        chain_selection = resid_list[0]
        resid_list = resid_list[1:]
        # convert the resids to integers
        resid_list = [int(i) for i in resid_list]
        # TODO check the order of chains in multichain proteins
        # TODO Currently assuming alphabet designation matches parmed order
        protein_chains = [i for i in parmed_structure.topology.chains() if next(i.residues()).name in aa_residues]
        for k, chain in enumerate(protein_chains):
            # convert letter rep of chain to ordinal number rep
            if ord(chain_selection.lower()) - 96 == k + 1:
                residues = [i for i in chain.residues()]
                selected_residues = [i for i in residues if i.index in resid_list]

                if len(selected_residues) == 0:
                    raise ValueError('Could not find one of the residues {} on protein chain.'.format(resid_list))

                for i in selected_residues:
                    for k in i.atoms():
                        final_list.append(k.index)
    if keyword_selection:
        selection_keywords = keyword_selection.split()

        # if selection keywords contain noh or not make sure they're at the end of the list
        if 'noh' in selection_keywords:
            selection_keywords.remove('noh')
            selection_keywords.append('noh')
        if 'not' in selection_keywords:
            selection_keywords.remove('not')
            selection_keywords.append('not')

        for keyword in selection_keywords:

            if keyword not in ['ligand', 'protein', 'lipids', 'water', 'noh', 'not']:
                raise ValueError(
                    'Keyword selection could syntax could not be parsed. Options are noh; not; protein; ligand; lipids; water.')

            if keyword == 'protein':
                protein_list = [i.idx for i in parmed_structure.atoms if i.residue.name in aa_residues]
                for i in protein_list:
                    final_list.append(i)

            if keyword == 'water':
                water_list = [i.idx for i in parmed_structure.atoms if i.residue.name in water_residues]
                for i in water_list:
                    final_list.append(i)

            if keyword == 'ligand':
                ligand_list = [i.idx for i in parmed_structure.atoms if i.residue.name in lig_residues]
                for i in ligand_list:
                    final_list.append(i)


            if keyword == 'lipid':
                lipid_list=[i.idx for i in parmed_structure.atoms if i.residue.name in lipid_residues]
                for i in lipid_list:
                    final_list.append(i)

            if keyword == 'noh':
                remove_list = []
                for i in final_list:
                    if 'H' in parmed_structure[i].name:
                        remove_list.append(i)
                final_list = list(set(final_list) - set(remove_list))

            if keyword == 'not':
                all_atoms = [i for i in parmed_structure.topology.atoms()]
                all_atoms_indeces_set = set([i.index for i in all_atoms])
                inverted_set = all_atoms_indeces_set - set(final_list)
                final_list = list(inverted_set)

    if len(final_list) == 0:
        print('warning, failed to select any atoms')
    return final_list


def annotate_fes(fes, bin_length, min_peak_loc, max_peak_loc):
    Z = fes[-1]
    try:
        maximax = signal.argrelextrema(Z, np.greater)
        maximay = signal.argrelextrema(Z, np.greater, axis=1)
        x_direction = set()
        y_direction = set()
        for i in range(len(maximax[0])):
            x_direction.add((maximax[0][i], maximax[1][i]))
        for i in range(len(maximay[0])):
            y_direction.add((maximay[0][i], maximay[1][i]))
        # consider filtering by Z value and taking y-direction only, will lead to getting saddle points
        # that aren't global maxima as well
        max_set = x_direction.intersection(y_direction)

        max_set = list(max_set)

        x_max_set = [max_set[i][0] for i in range(len(max_set))]
        y_max_set = [max_set[i][1] for i in range(len(max_set))]

        # note y's and x's are reversed because imshow follows the image conventions
        y_max_set.sort()
        y_max_set = [i for i in y_max_set if min_peak_loc < i < max_peak_loc]

        # now get deltaG estimate by trying all the locations and take mode
        deltaGs_list = []
        for i in y_max_set:
            bound = Z[:, :i]
            unbound = Z[:, i:]
            diff = np.min(bound) - np.min(unbound)
            deltaGs_list.append(diff)
        delta_Gs = [i / unit.kilocalorie_per_mole for i in deltaGs_list]
        hist_g = np.histogram(delta_Gs)
        largest_bin_g = np.argmax(hist_g[0])

        deltaG_by_mode = hist_g[1][largest_bin_g]

        hist = np.histogram(y_max_set, bins=30)
        largest_bin = np.argmax(hist[0])
        peak_loc = int(hist[1][largest_bin])

    except:
        deltaG_by_mode = 0
        peak_loc = 0

    peak_loc /= bin_length

    return deltaG_by_mode, peak_loc

def find_center_of_mass(coord, masses):
    masses = np.array(masses)
    weights = masses/masses.sum()
    com = np.average(np.array(coord/unit.nanometer), weights = weights, axis=0)
    return com

def find_z_cone_apex(surf_positions, prot_positions, lig_positions):

    #this helper function is meant to find the apex of the funnel for use in funnel metaD

    #first find z-coordinate of ligand and z_coordinate of protein
    lig_z_pos = np.mean([i.z for i in lig_positions])
    prot_z_pos = np.mean([i.z for i in prot_positions])

    #next find the position of the leaflet and add ~20 nm (roughly the thickness of half the water box)
    #we don't know which lipid leaflet we need, so take the side the ligand is on
    if lig_z_pos>prot_z_pos:
        surf_z_pos = np.mean([i.z for i in surf_positions if i.z > prot_z_pos])
        z_coord = np.mean(surf_z_pos)
        z_coord+=20
    else:
        surf_z_pos = np.mean([i.z for i in surf_positions if i.z < prot_z_pos])
        z_coord = np.mean(surf_z_pos)
        z_coord-=20

    if np.isnan(z_coord):
        raise ValueError('Could not find membrane/solvent interface for funnel placement')

    return z_coord

def find_radius_and_center(ligand_pos, radius_scale_factor):

    cog = np.mean(ligand_pos, axis=0)

    distances = []
    #choose the two ligand atoms that are the furthest apart and use as estimate for cone mouth
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                distances.append(dist(i,j))

    rcyl = radius_scale_factor * np.max(distances)

    return rcyl,cog

def find_center_atom(center, array_pos):

    distances = []
    for i in array_pos:
        distances.append(dist(i,center))

    chosen = np.argmin(distances)

    return chosen, array_pos[chosen]

def get_angle_particle_coords(ligand_pos, prot_pos):

    distances = []
    indeces= []
    #choose the two ligand atoms that are the furthest apart
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                indeces.append([k,l])
                distances.append(dist(i,j))
    chosen_k = indeces[np.argmax(distances)][0]
    chosen_l = indeces[np.argmax(distances)][1]

    #choose the protein atom that is the closest to the chosen_k'th ligand atom
    distances = []
    for z in prot_pos:
        distances.append(dist(ligand_pos[chosen_k],z))
    chosen_z = np.argmin(distances)

    #load the coords and indeces in separate arrays
    three_coords = [ligand_pos[chosen_k],ligand_pos[chosen_l],prot_pos[chosen_z]]
    indeces = [int(chosen_k),int(chosen_l),int(chosen_z)]

    return three_coords, indeces

def dist(a,b):
    return np.linalg.norm(a-b)

def find_contacts(positions1, positions2, cutoff):

    contacts_i = []
    contacts_j = []
    for i in positions1:
        for j in positions2:
            if dist(i,j)<=cutoff:
                contacts_i.append(i)
                contacts_j.append(j)

    return contacts_i,contacts_j