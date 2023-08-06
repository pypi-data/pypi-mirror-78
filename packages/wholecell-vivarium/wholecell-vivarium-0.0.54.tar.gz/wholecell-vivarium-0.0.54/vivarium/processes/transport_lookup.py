from __future__ import absolute_import, division, print_function

import os

import numpy as np
from scipy import constants

from vivarium.core.process import Process
from vivarium.library.make_media import Media
from vivarium.library.look_up import LookUp
from vivarium.library.rate_law_utilities import load_reactions
from vivarium.library.rate_law_utilities import get_reactions_from_exchange
from vivarium.library.rate_law_utilities import get_molecules_from_reactions
from vivarium.data.spreadsheets import load_tsv
from vivarium.library.units import units
from vivarium.core.composition import simulate_process_in_experiment


EXTERNAL_MOLECULES_FILE = os.path.join('vivarium', 'data', 'flat', 'wcEcoli_environment_molecules.tsv')
TRANSPORT_IDS_FILE = os.path.join('vivarium', 'data', 'flat', 'wcEcoli_transport_reactions.tsv')

amino_acids = [
    'L-ALPHA-ALANINE',
    'ARG',
    'ASN',
    'L-ASPARTATE',
    'CYS',
    'GLT',
    'GLN',
    'GLY',
    'HIS',
    'ILE',
    'LEU',
    'LYS',
    'MET',
    'PHE',
    'PRO',
    'SER',
    'THR',
    'TRP',
    'TYR',
    'L-SELENOCYSTEINE',
    'VAL'
]
additional_exchange = ['OXYGEN-MOLECULE', 'GLC']
external_molecule_ids = additional_exchange + amino_acids

# add [p] label. TODO (Eran) -- fix this
external_molecule_ids_p = [mol_id + '[p]' for mol_id in external_molecule_ids]

COUNTS_UNITS = units.mmol
VOLUME_UNITS = units.L
TIME_UNITS = units.s
FLUX_UNITS = COUNTS_UNITS / VOLUME_UNITS / TIME_UNITS


class TransportLookup(Process):

    name = 'transport_lookup'

    def __init__(self, initial_parameters=None):
        if initial_parameters is None:
            initial_parameters = {}

        self.media_id = 'minimal' # initial_parameters.get('media_id', 'minimal')
        self.lookup_type = 'average' # initial_parameters.get('lookup', 'average')
        self.nAvogadro = constants.N_A * 1/units.mol
        self.external_molecule_ids = external_molecule_ids

        # load all reactions and maps
        self.load_data()

        # external_molecule_ids declares which molecules' exchange will be applied
        self.transport_reaction_ids = get_reactions_from_exchange(self.all_transport_reactions, external_molecule_ids_p)
        all_molecule_ids = get_molecules_from_reactions(self.transport_reaction_ids, self.all_transport_reactions)
        self.internal_molecule_ids = [mol_id for mol_id in all_molecule_ids if mol_id not in external_molecule_ids_p]

        # make look up object
        self.look_up = LookUp()

        parameters = {}
        parameters.update(initial_parameters)
        super(TransportLookup, self).__init__(parameters)

    def ports_schema(self):
        media_id = 'minimal_plus_amino_acids'
        make_media = Media()
        media = make_media.get_saved_media(media_id)
        schema = {
            'global': {
                'volume': {
                    '_default': 1 * units.fL,
                },
                'location': {
                    '_default': [0.5, 0.5],
                },
            },
            'external': {
                state_id: {
                    '_default': value,
                    '_emit': True}
                for state_id, value in media.items()},
            'internal': {
                state_id: {
                    '_default': 0.0}
                for state_id in self.internal_molecule_ids},
            'fields': {
                state_id: {
                    '_default': np.ones((1, 1)),
                    '_emit': True}
                for state_id in self.external_molecule_ids},
            'dimensions': {
                'bounds': {
                    '_default': [1, 1],
                },
                'n_bins': {
                    '_default': [1, 1],
                },
                'depth': {
                    '_default': 1,
                },
            },
        }

        return schema


    def next_update(self, timestep, states):
        external = states['external'] # TODO -- use external state? if concentrations near 0, cut off flux?

        volume = states['global']['volume']
        mmol_to_counts = self.nAvogadro.to('1/mmol') * volume.to('L')

        # get transport fluxes
        transport_fluxes = self.look_up.look_up(
            self.lookup_type,
            self.media_id,
            self.transport_reaction_ids)

        # time step dependence
        # TODO (Eran) -- load units in look_up
        transport_fluxes = {key: value * (FLUX_UNITS) * timestep * TIME_UNITS
                                 for key, value in transport_fluxes.items()}

        # convert to counts
        delta_counts = self.flux_to_counts(transport_fluxes, mmol_to_counts)

        # Get the deltas for environmental molecules
        environment_deltas = {}
        for molecule_id in delta_counts.keys():
            if molecule_id in self.molecule_to_external_map:
                external_molecule_id = self.molecule_to_external_map[molecule_id]
                environment_deltas[external_molecule_id] = delta_counts[molecule_id]

        return {
            'fields': {
                molecule: {
                    '_value': exchange,
                    '_updater': {
                        'updater': 'update_field_with_exchange',
                        'port_mapping': {
                            'global': 'global',
                            'dimensions': 'dimensions',
                        },
                    },
                }
                for molecule, exchange in environment_deltas.items()
            },
        }

    # TODO (Eran) -- make this a util
    def flux_to_counts(self, fluxes, conversion):

        rxn_counts = {reaction_id: int(conversion * flux) for reaction_id, flux in fluxes.items()}
        delta_counts = {}
        for reaction_id, rxn_count in rxn_counts.items():
            stoichiometry = self.all_transport_reactions[reaction_id]['stoichiometry']
            substrate_counts = {substrate_id: coeff * rxn_count for substrate_id, coeff in stoichiometry.items()}
            # add to delta_counts
            for substrate, delta in substrate_counts.items():
                if substrate in delta_counts:
                    delta_counts[substrate] += delta
                else:
                    delta_counts[substrate] = delta

        return delta_counts

    def load_data(self):
        '''
        - Loads all reactions, including locations for enzymes.
        - Separates out the transport reactions as an class dictionary
        - Makes mappings from molecule ids with location tags to external molecules without location tags

        '''

        # use rate_law_utilities to get all_reactions
        all_reactions = load_reactions()

        # make dict of reactions in TRANSPORT_IDS_FILE
        self.all_transport_reactions = {}
        rows = load_tsv(TRANSPORT_IDS_FILE)
        for row in rows:
            reaction_id = row['reaction id']
            stoichiometry = all_reactions[reaction_id]['stoichiometry']
            reversible = all_reactions[reaction_id]['is reversible']
            transporters_loc = all_reactions[reaction_id]['catalyzed by']

            self.all_transport_reactions[reaction_id] = {
                'stoichiometry': stoichiometry,
                'is reversible': reversible,
                'catalyzed by': transporters_loc}

        # Make map of external molecule_ids with a location tag (as used in reaction stoichiometry) to molecule_ids in the environment
        self.molecule_to_external_map = {}
        self.external_to_molecule_map = {}
        rows = load_tsv(EXTERNAL_MOLECULES_FILE)
        for row in rows:
            molecule_id = row['molecule id']
            location = row['exchange molecule location']
            self.molecule_to_external_map[molecule_id + location] = molecule_id
            self.external_to_molecule_map[molecule_id] = molecule_id + location


if __name__ == '__main__':

    process = TransportLookup({})
    settings = {
        'environment': {
            'volume': 5e-14 * units.fL,
            'states': process.external_molecule_ids,
            'environment_port': 'external',
        },
        'timestep': 1,
        'total_time': 60}
    timeseries =  simulate_process_in_experiment(process, settings)
