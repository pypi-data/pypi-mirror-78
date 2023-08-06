import mdtraj
import numpy as np

import os

from simtk.openmm import app
from simtk.openmm.app import PDBFile
from simtk import openmm as mm
from simtk.openmm import unit
from sys import stdout

from tempfile import mkdtemp

from .utils import *

import pickle

import shutil

from .custom_reporters import FESReporter

from platform import uname


class MDSimulation():
    def __init__(self, parmed_structure, coordinates=None,
                 velocities=None, box_vectors=None,
                 cwd=None, centering=True,
                 temperature=300 * unit.kelvin, pressure=1 * unit.atmosphere, membrane=False,
                 integrator_type='Langevin', platform_name=None, nonbonded_method='PME', nonbonded_cutoff=1 * unit.nanometer,
                 precision=None,
                 atoms_to_freeze=None, atoms_to_restrain=None,
                 restraint_weight=None, constraints='HBonds',
                 state_out='sim.log',
                 implicit_solvent_model=None, hmr=False,
                 state_interval=None, progress_interval=None, traj_interval=None,
                 progress_out='progress.log',
                 traj_out='trajectory.h5',
                 run_time = 2 * unit.nanosecond
                 ):

        """Base Simulation Class for MDSimulations.

        Examples
        --------

        Load packages
        >>> import parmed
        >>> from simtk.openmm import unit
        >>> from rs_simtools import MDSimulation, select_atoms

        instantiate sim from parmed alone, minimize (save h5 file) and run
        >>> mdsim = MDSimulation(parmed_structure=parmed)
        >>> mdsim.minimize()
        >>> minimized_parmed = mdsim.run(2 * unit.nanosecond)

        build sim using a previous trajectory or h5 file
        >>> mdsim = MDSimulation(parmed_structure=parmed_structure, coordinates=trajectory.h5)

        build sim with positional restraints, run some equilibration and remove them for longer run
        >>> protein_atoms = select_atoms(parmed_structure=parmed_structure, keyword_selection='protein')
        >>> mdsim = MDSimulation(parmed_structure=parmed_structure, atoms_to_restrain=protein_atoms, restraint_weight=4)
        >>> mdsim.run(1*unit.nanosecond)
        >>> mdsim.update_restraint_weight(2)
        >>> mdsim.run(1*unit.nanosecond)
        >>> mdsim.remove_positional_restratins()
        >>> end_parmed = mdsim.run(4 * unit.nanosecond)

        Parameters
        ----------
        parmed_structure : Parmed.Structure
            The Parmed Topology Object containing topology nand force field parameters

        coordinates: unit.Quantity or mdtraj.Trajectory, optional
            Alternate coordiantes to be used if parmed_structure coordinates aren't going to be used

        velocities: numpy array, optional
            Velociites to be used for restarting sim from previous simulation

        box_vectors: unit.Quantity, optional
            Box vectors to be used for simulation. If not specified box vectors are taken from parmed_structure

        cwd : string, optional
            directory for storing simulation files. If None a folder will be created in /tmp/ with a unique 6 digit randomized name

        temperature: unit.Quantity, optional
            temperature for running simulation and Langevin bath if used. Default 300 Kelvin

        pressue : unit.Quantity, optional
            pressure at which to hold the simulation via barostat. If None no temperature control will be used

        membrane : bool, optional
            flag for whether or not the simulation contains a membrane, which will ensure the correct barostat is used for membranes

        integrator_type : {'Langevin, Verlet'}, optional
            string indicating integrator type to use. Default: Langevin

        platform_name : {'Reference, CPU, CUDA, OpenCL'}, optional
            string indicating which platform to use for running simulation. If None the fastest platform available will be used

        nonbonded_method : string, optional
            string indicating nonbonded method to use, default is PME

        nonbonded_cutoff : unit.Quantity, optional
            nonbonded cutoff distance, default 1 *unit.nanometer

        atoms_to_freeze : list of integers, optional
            list of atom indeces indicating which atoms to freeze during the simulation

        atoms_to_restrain : list of integers, optional
            list of atoms indeces to restrain to initial positions during the simulation

        restraint_weight : unit.Quantity or float, optional
            force constant to be used for positional restraints. If not units given, they will be assumed as kcal/mol/A.

        constraints :  {'HBonds', 'HAngles' ,'AllBonds'}, optional
            type of constraints to use during simulation. Default is HBonds

        implicit_solvent_model : {'HCT', 'OBC1', 'OBC2', 'GBn', 'GBn2'}, optional
            string indicating the type of implicit model to use if any

        hmr : boolean, optional
            boolean indicating whether or not to use Hydrogen Mass Repartitioning and a 4 fs time step.

        run_time : unit.Quantity, optional
            default run time for the simulation if non is given as input to run method.

        state_interval : unit.Quantity, optional
            interval with which to write state information (temperature, potential energy etc) to file

        state_out :  string, optional
            name of file for writing state information. Defaults to 'sim.log'

        progress_interval : unit.Quantity, optional
            Frequency with which to report progress data

        progress_out : string or sys.stdout, optional
            name of file for writing progress information. Defaults to 'progress.log' If sys.stdout is specified,
            pickling of the simulation will not be supported

        traj_interval : unit.Quantity, optional
            frequency to write trajectory information to file

        traj_out : string, optional
            name of file for writing trajectory information. Defaults to 'trajectory.h5'

        """
        self.parmed_structure = parmed_structure

        # check that the coordinates have units
        if coordinates is not None:
            if isinstance(coordinates, unit.Quantity):
                print('using coordinates supplied at input')
                converted_coordinates = coordinates.value_in_unit(unit.nanometer)
                self.positions = converted_coordinates
            elif isinstance(coordinates, mdtraj.Trajectory):
                print('setting positions and box vectors from final frame in hdf5 trajectory file')
                self.positions = coordinates.openmm_positions(frame=-1)
                self.box_vectors = coordinates.openmm_boxes(frame=-1)
            else:
                raise ValueError('coordinates must have units, got {}'.format(type(coordinates)))
        else:
            self.positions = parmed_structure.positions

        self.coordinates = parmed_structure.coordinates

        if velocities is not None:
            self.velocities = velocities
        elif parmed_structure.velocities is not None:
            self.velocities = parmed_structure.velocities
        else:
            self.velocities = None

        if box_vectors is not None:
            print('using box vectors specified at input')
            self.box_vectors = box_vectors
        else:
            print('getting box vectors from parmed')
            self.box_vectors = parmed_structure.box_vectors

        self.centering=centering
        self.cwd = cwd

        self.atoms_to_freeze = atoms_to_freeze
        self.platform_name = platform_name
        self.precision = precision
        self.temperature = temperature
        self.integrator_type = integrator_type
        self.state_out = state_out
        self.atoms_to_restrain = atoms_to_restrain
        self.restraint_weight = restraint_weight
        self.implicit_solvent_model = implicit_solvent_model
        self.hmr = hmr
        self.run_time = run_time

        # set step length
        if self.hmr:
            self.step_length = 0.004 * unit.picoseconds
        else:
            self.step_length = 0.002 * unit.picoseconds

        self.constraints = constraints
        self.nonbonded_cutoff = nonbonded_cutoff
        self.nonbonded_method = nonbonded_method
        self.membrane = membrane
        self.pressure = pressure

        self.state_interval = state_interval
        self.traj_interval = traj_interval
        self.progress_interval = progress_interval
        self.state_out = state_out
        self.traj_out = traj_out
        self.progress_out = progress_out
        self.custom_forces = {}

        # if they're still none this should be an implicit or vacuum sim
        if self.box_vectors == None and self.implicit_solvent_model == None:
            print('Warning! No box vectors found and no implicit model, proceeding with vacuum simulation')

        # run sanity checks

        # make sure the parmed has all the params
        if len([i.type for i in parmed_structure.bonds if i.type == None]) > 0:
            raise ValueError('Parmed object does not have all parameters')

        # match num atoms to num coordinates
        if len(parmed_structure.atoms) != len(self.positions):
            raise ValueError('Number of coordinates does not match number of atoms')

        # match num velocities to num coords
        if self.velocities is not None:
            if len(self.velocities) != len(self.positions):
                raise ValueError('Number of velocities does not match number of coordinates')

        if membrane and pressure == None:
            print('WARNING - membrane simulations without pressure controls are not recommended')

        # build sim
        self._build_sim()

    def set_positional_restraints(self, atoms_to_restrain, restraint_weight=2, reference_coordinates=None):
        """ add positional restraints to current MD Sim object

        Parameters
        ----------

        atoms_to_restrain : list of integers
            list of atom indices

        restraint_weight : unit.Quantity or float, optional
            strength of the positional restraint in kcal/mol/A^2

        reference_coordinates : unit.Quantity, optional
            reference coordinates to be used with restraint defaults to current positions

        """
        print('setting restraints for {} atoms'.format(len(atoms_to_restrain)))

        if not reference_coordinates:
            reference_coordinates = self.positions.in_units_of(unit.nanometer)
        else:
            reference_coordinates = reference_coordinates.in_units_of(unit.nanometer)

        if not (isinstance(atoms_to_restrain, list)) and (isinstance(atoms_to_restrain[0], int)):
            raise ValueError('Restraint selection must be a list of integers corresponding to atom indeces')
        if restraint_weight == None:
            restraint_weight = 2 * unit.kilocalories_per_mole / unit.angstrom ** 2
            print('restraint weight for positional restraints not specified, using 2 kcals/mol*A^2')
        elif isinstance(restraint_weight, unit.Quantity):
            restraint_weight = restraint_weight
        else:
            restraint_weight = restraint_weight * unit.kilocalories_per_mole / unit.nanometer ** 2

        restraint_force = mm.CustomExternalForce('K*periodicdistance(x, y, z, x0, y0, z0)^2')
        # Add the restraint weight as a global parameter in kcal/mol/nm^2
        restraint_force.addGlobalParameter("K", restraint_weight)
        # Define the target xyz coords for the restraint as per-atom (per-particle) parameters
        restraint_force.addPerParticleParameter("x0")
        restraint_force.addPerParticleParameter("y0")
        restraint_force.addPerParticleParameter("z0")

        for index in range(0, len(self.positions)):
            if index in atoms_to_restrain:
                xyz = reference_coordinates[index].in_units_of(unit.nanometers) / unit.nanometers
                restraint_force.addParticle(index, xyz)
        self.custom_forces['positional_restraints'] = self.system.addForce(restraint_force)
        self.simulation.context.reinitialize()
        self.simulation.context.setPositions(self.positions)

    def update_restraint_weight(self, restraint_weight):
        """ update the restraint weight of current positional restraints

        """
        print('updating restraint weight to {}'.format(restraint_weight))
        self.restraint_weight = restraint_weight
        self.simulation.context.setParameter("K", restraint_weight)

    def remove_positional_restraints(self):
        """ Remove all positional restraints added using the API or on init

        """
        print('removing positional restraints')
        self.system.removeForce(self.custom_forces['positional_restraints'])
        self.simulation.context.reinitialize()
        self.simulation.context.setPositions(self.positions)

    def set_implicit_solvent_model(self, implicit_solvent_model, nonbonded_method, nonbonded_cutoff):
        """ Add an implicit solvent force to the system

        Parameters
        ----------

        implicit_solvent_model : {'HCT', 'OBC1', 'OBC2', 'GBn', 'GBn2'}

        nonbonded_method : {'PME'}

        nonbonded_cutoff : unit.Quantity

        """
        if "implict_solvent" in self.custom_forces:
            raise ValueError('Implicit solvent model has already been set for this system')

        if not implicit_solvent_model in ['HCT', 'OBC1', 'OBC2', 'GBn', 'GBn2']:
            raise ValueError('Unknown implicit solvent model {}'.format(implicit_solvent_model))

        implicit_model_object = eval("app.%s" % implicit_solvent_model)
        nonbonded_method_object = eval("app.%s" % nonbonded_method)
        implicit_force = self.parmed_structure.omm_gbsa_force(implicit_model_object,
                                                              temperature=self.temperature,
                                                              nonbondedMethod=nonbonded_method_object,
                                                              nonbondedCutoff=nonbonded_cutoff)

        self.custom_forces['implicit_solvent'] = self.system.addForce(implicit_force)

    def freeze_atom_selection(self, atoms_to_freeze):
        """freeze selected atoms

        """

        if not (isinstance(atoms_to_freeze, list)) and (isinstance(atoms_to_freeze[0], int)):
            raise ValueError('Freeze selection must be a list of integers corresponding to atom indeces')

        # Set frozen atom masses to zero and then they won't be integrated
        self.frozen_atoms = {}
        for atom_index in range(0, len(self.positions)):
            if atom_index in atoms_to_freeze:
                self.frozen_atoms[str(atom_index)] = self.system.getParticleMass(atom_index)
                self.system.setParticleMass(atom_index, 0.0)
        print('froze {} atoms'.format(len(atoms_to_freeze)))

    def unfreeze_atoms(self):
        """unfreeze all atoms frozen with the freze_atom_selection command

        """

        for atom_index in self.frozen_atoms:
            self.system.setParticleMass(int(atom_index), self.frozen_atoms[atom_index])
        print('unfroze {} atoms'.format(len(self.frozen_atoms)))
        self.frozen_atoms = {}

    def restrain_COM(self, atom_selection, COM_restraint_weight):
        """ Adds a positional restraint to the COM of the atom_selection

        """

        # get the masses of the selection
        masses = []
        for atom_index in range(len(self.positions)):
            if atom_index in atom_selection:
                masses.append(self.system.getParticleMass(atom_index) / unit.dalton)

        # get the coordinates of the selection
        selected_positions = np.array(self.positions / unit.nanometer)[atom_selection]
        # get the center of mass of the selection
        com = find_center_of_mass(masses=masses, coord=selected_positions)

        print('coordinates being used for COM restraint: {}'.format(com))

        restraint = mm.CustomCentroidBondForce(1, 'K*sqrt((x1-x0)^2 + (y1-y0)^2 + (z1-z0)^2)')
        restraint.addGlobalParameter('K', COM_restraint_weight)
        restraint.addGlobalParameter('x0', com[0])
        restraint.addGlobalParameter('y0', com[1])
        restraint.addGlobalParameter('z0', com[2])
        restraint.addGroup(atom_selection)
        restraint.addBond([0])
        self.custom_forces['COM_restraint'] = self.system.addForce(restraint)

    def remove_COM_restraint(self):
        """ Removes COM restraint
        """
        print('removing COM positional restraints -does not include other positional restraints')
        self.system.removeForce(self.custom_forces['COM_restraint'])

    def center_coordinates(self):
        print('centering coordinates')
        cog = np.mean(self.coordinates, axis=0)
        # System box vectors
        box_v = self.box_vectors.in_units_of(unit.angstrom) / unit.angstrom
        box_v = np.array([box_v[0][0], box_v[1][1], box_v[2][2]])
        # Translation vector
        delta = box_v / 2 - cog
        # New Coordinates
        new_coords = self.coordinates + delta
        self.positions = new_coords * unit.angstrom


    def _build_sim(self):
        """Use params specified on init to build the simulation context, specify the platform and bind an integrator

        """

        if self.cwd is None:
            self.cwd = mkdtemp()
            print('created directory {} for storing sim files'.format(self.cwd))
        #make sure the cwd exists in case we're unpickling
        elif not os.path.exists(self.cwd):
            self.cwd = os.mkdir(self.cwd)
            print('storing sim files in directory {}'.format(self.cwd))
        else:
            print('storing sim files in directory {}'.format(self.cwd))

        if self.centering:
            self.center_coordinates()

        if self.constraints in ['HBonds', 'HAngles', 'Allbonds']:
            print('setting {} constraints'.format(self.constraints))
            constraints_object = eval("app.%s" % self.constraints)
        else:
            print('did not set any constraints')
            constraints_object = None

        nonbonded_method_object = eval("app.%s" % self.nonbonded_method)


        self.system = self.parmed_structure.createSystem(nonbondedMethod=nonbonded_method_object,
                                                         nonbondedCutoff=self.nonbonded_cutoff,
                                                         constraints=constraints_object,
                                                         removeCMMotion=False,
                                                         hydrogenMass=4.0 * unit.amu if self.hmr else None)

        if self.implicit_solvent_model:
            self.set_implicit_solvent_model(self.implicit_solvent_model, self.nonbonded_method, self.nonbonded_cutoff)

        if self.pressure:
            if self.membrane:
                print('setting membrane barostat')
                barostat_force = mm.MonteCarloMembraneBarostat(1 * unit.bar, 200 * unit.bar * unit.nanometer,
                                                               self.temperature,
                                                               mm.MonteCarloMembraneBarostat.XYIsotropic,
                                                               mm.MonteCarloMembraneBarostat.ZFree)
            else:
                print('setting barostat with pressure {}'.format(self.pressure))
                barostat_force = mm.MonteCarloBarostat(self.pressure, self.temperature, 25)
            self.system.addForce(barostat_force)


        if self.atoms_to_freeze is not None:
            self.freeze_atom_selection(self.atoms_to_freeze)

        # get integrator
        if self.integrator_type not in ['Langevin', 'Verlet']:
            raise ValueError('{} integrator type not supported'.format(self.integrator))

        if self.integrator_type == 'Langevin':
            self.integrator = mm.LangevinIntegrator(self.temperature, 1 / unit.picoseconds, self.step_length)

        if self.integrator_type == 'Verlet':
            self.integrator = mm.VerletIntegrator(self.step_length)

        if self.precision:
            if self.precision not in ['mixed', 'single', 'double']:
                raise ValueError('precision must be either mixed, single or double')

            precision = {'Precision':self.precision}
        else:
            precision = None

        if self.platform_name:

            if self.platform_name not in ['CPU', 'CUDA', 'OpenCL', 'Reference']:
                raise ValueError('Platform must be one of the following: CPU, CUDA, OpenCL, Reference')

            self.platform = mm.Platform.getPlatformByName(self.platform_name)
            self.simulation = app.Simulation(self.parmed_structure.topology, self.system, self.integrator,
                                             platform=self.platform, platformProperties=precision)
        else:
            self.simulation = app.Simulation(self.parmed_structure.topology, self.system, self.integrator,
                                             platformProperties=precision)
            self.platform = self.simulation.context.getPlatform()

        print('using platform {}'.format(self.simulation.context.getPlatform().getName()))

        self.simulation.context.setPositions(self.positions)

        if self.box_vectors is not None:
            self.simulation.context.setPeriodicBoxVectors(self.box_vectors[0], self.box_vectors[1], self.box_vectors[2])

        if self.velocities is not None:
            print('found velocities, restarting from previous simulation')
            self.simulation.context.setVelocities(self.velocities)
        else:
            print('assigning random velocity distribution with temperature {}'.format(self.temperature))
            self.simulation.context.setVelocitiesToTemperature(self.temperature)

        if self.atoms_to_restrain is not None:
            self.set_positional_restraints(self.atoms_to_restrain, self.restraint_weight)



    def _write_coordinates_to_h5(self, fname='current_frame.h5'):
        """Writes minimized coordinates to an H5 file

        """

        if not fname.endswith('h5'):
            print('WARNING: saving an h5 file without the suffix .h5')

        # write hdf5 single frame
        current_state = self.simulation.context.getState(getPositions=True,enforcePeriodicBox=True)
        current_positions = current_state.getPositions()

        # mdtraj is set up to read from files more easily than memory so write a pdb to disk and
        # load it as a frame
        mm.app.PDBFile.writeFile(self.parmed_structure.topology,
                                 current_positions, open('temp_pdb.pdb', 'w'))

        mdtraj_top = mdtraj.Topology.from_openmm(self.parmed_structure.topology)

        frame = mdtraj.load_frame('temp_pdb.pdb', top=mdtraj_top, index=-1)

        # cleanup the pdb file
        os.remove('temp_pdb.pdb')

        # write the h5 file
        print('saving minimized coordinates to {}'.format(os.path.join(self.cwd, fname)))
        frame.save_hdf5(os.path.join(self.cwd, fname))

    def pickle_sim(self, pickle_name='mdsim.pickle'):
        """ Remove the Swigpy objects that don't pickle and write the current simulation pickle to cwd
        In order to use the pickle you will need to run _build_sim

        Examples
        -------
        >>> mdsim.pickle_sim()
        >>> with open(os.path.join(mdsim.cwd,'mdsim.pickle'), 'rb') as handle:
        >>>     new_sim = pickle.load(handle)
        >>>
        >>> new_sim._build_sim()
        >>> new_sim.run()


        """

        if (self.progress_out == stdout) or (self.state_out == stdout):
            raise ValueError('cant pickle system if any logs point to stdout!')

        print('removing sim and system objects in order to pickle')
        del self.simulation
        del self.system
        del self.platform

        fname = os.path.join(self.cwd, pickle_name)
        with open(fname, 'wb') as handle:
            pickle.dump(obj=self, file=handle)
        print('pickled sim saved as {}'.format(fname))
        print('to use it once unpickled you will need to run self._build_sim()')

    def purge_sim_files(self):
        """Removes all files in mdsim.cwd

        """
        print('removing directory {} and everything in it'.format(self.cwd))
        shutil.rmtree(self.cwd)
        del self.cwd

    def update_platform(self, platform_name=None):
        """ Update the platform used for simulation - Warning this will reinitialize the context

        """

        if platform_name not in ['CPU','CUDA','OpenCL','Reference']:
            raise ValueError('Platform must be one of the following: CPU, CUDA, OpenCL, Reference')

        print('updating platform to {}'.format(platform_name))
        self.platform_name = platform_name
        del self.simulation
        self._build_sim()

    def _add_reporters(self, total_steps):
        """ Add reporters to the sim object

        """
        if self.progress_interval:
            if isinstance(self.progress_interval, unit.Quantity):
                prog_int = self.progress_interval / self.step_length
            else:
                raise ValueError('progress report interval must have units, got {}'.format(self.progress_interval))

            progress_report_steps = int(round(prog_int))

            if progress_report_steps == 0:
                raise ValueError('progress report interval cannot be less than step size')

            # Print host information
            for k, v in uname()._asdict().items():
                print("{} : {}".format(k, v))

            # Platform properties
            print("Platform in use", self.platform.getName())
            for prop in self.platform.getPropertyNames():
                val = self.platform.getPropertyValue(self.simulation.context, prop)
                print("{} : {}".format(prop, val))

            # MM Version
            print("OpenMM Version : {}".format(mm.version.version))


            progress_reporter = app.StateDataReporter(self.progress_out, separator="\t",
                                                      reportInterval=progress_report_steps,
                                                      step=False,
                                                      totalSteps=total_steps,
                                                      time=True,
                                                      speed=True,
                                                      progress=True,
                                                      elapsedTime=False,
                                                      remainingTime=True)
            self.simulation.reporters.append((progress_reporter))

        if self.state_interval:
            if isinstance(self.state_interval, unit.Quantity):
                state_int = self.state_interval / self.step_length
            else:
                raise ValueError('state report interval must have units, got {}'.format(self.state_interval))

            file_name = os.path.join(self.cwd, self.state_out)
            state_report_steps = int(round(state_int))

            if state_report_steps == 0:
                raise ValueError('state report interval cannot be less than step size')

            state_reporter = app.StateDataReporter(file_name,
                                                   separator="\t",
                                                   reportInterval=state_report_steps,
                                                   step=True,
                                                   potentialEnergy=True,
                                                   kineticEnergy=True,
                                                   totalEnergy=True,
                                                   volume=True,
                                                   density=True,
                                                   temperature=True)

            self.simulation.reporters.append(state_reporter)

        if self.traj_interval:
            if isinstance(self.traj_interval, unit.Quantity):
                traj_int = self.traj_interval / self.step_length
            else:
                raise ValueError('traj report interval must have units, got {}'.format(self.traj_interval))

            traj_file = os.path.join(self.cwd, self.traj_out)
            traj_steps = int(round(traj_int))

            if traj_steps == 0:
                raise ValueError('traj report interval cannot be less than step size')

            traj_reporter = mdtraj.reporters.HDF5Reporter(traj_file, traj_steps)
            self.simulation.reporters.append(traj_reporter)

    def update_parmed(self):
        """ updates the parmed object with velocities, coordinates, posiitons, and box vectors


        """
        state = self.simulation.context.getState(getPositions=True,
                                                 getVelocities=True,
                                                 getEnergy=True,
                                                 enforcePeriodicBox=True)

        current_positions = state.getPositions()
        current_velocities = state.getVelocities()
        current_box = state.getPeriodicBoxVectors()

        self.coordinates = np.array(current_positions.value_in_unit(unit.nanometer))
        self.parmed_structure.positions = current_positions
        self.parmed_structure.velocities = current_velocities
        self.parmed_structure.box_vectors = current_box
        self.positions = current_positions

    def minimize(self, max_steps=None, save_h5=False):
        """Minimize the energy of the current simulation

        :param max_steps: int, optional
        :param save_h5: bool, optional
        :return: updated parmed_structure
        """
        state = self.simulation.context.getState(getEnergy=True, enforcePeriodicBox=True)
        starting_energy = state.getPotentialEnergy()

        print('minimizing system with beginning energy: {}'.format(starting_energy))

        if max_steps is None:
            self.simulation.minimizeEnergy()
        else:
            max_steps = int(max_steps)
            self.simulation.minimizeEnergy(maxIterations=max_steps)

        #using enforce periodic box to make sure coordinates will reinitialize
        state = self.simulation.context.getState(getPositions=True,
                                                 getEnergy=True,
                                                 enforcePeriodicBox=True)
        final_energy = state.getPotentialEnergy()

        # reset self.positions with current context positions
        self.positions = state.getPositions()

        print('successfully minimized the system to final energy {}'.format(final_energy))

        if save_h5:
            self._write_coordinates_to_h5(fname='minimized.h5')

        current_box = state.getPeriodicBoxVectors()

        self.coordinates = np.array(self.positions.in_units_of(unit.angstrom) / unit.angstrom)
        self.parmed_structure.positions = self.positions
        self.parmed_structure.box_vectors = current_box

        return self.parmed_structure

    def run(self, time=None, total_steps=None):
        """"
        :time: unit.Quantity, optional
        Returns
        -------
        parmed_structure
            parmed_strcutre with updated coordinates, positions, box_vectors, and velocities if generated

         """


        if not time:
            time=self.run_time

        if not isinstance(time, unit.Quantity):
            raise ValueError('sim time must have units')

        nsteps = int(round(time / self.step_length))

        if total_steps is None:
            total_steps = nsteps

        # reporters sometimes require total_steps, so we build it in the run method
        if len(self.simulation.reporters) == 0:
            self._add_reporters(total_steps)

        self.simulation.step(nsteps)

        self.update_parmed()

        self.simulation.reporters.clear()
        return self.parmed_structure

class GentleHeatSimulation(MDSimulation):
    """Simulation protocol that gradually increases the temperature over a number of stages before releasing
    restraints gradually over another set of stages

    :start_temp: unit.Quantity
    :target_temp: unit.Quantity
    :start_restraint_weight unit.Quantity or float
    :num_heat_stages int
    :num_release_stages


    """
    def __init__(self, start_temp=100,
                 start_restraint_weight=2, num_heat_stages=2,
                 num_release_stages=2, equil_time=2,
                 stage_run_time=.5, **kwargs):
        super().__init__(**kwargs)
        self.start_temp = start_temp
        self.start_restraint_weight = start_restraint_weight
        self.num_heat_stages = num_heat_stages
        self.num_release_stages = num_release_stages
        self.equil_time = equil_time
        self.stage_run_time = stage_run_time

    def run(self):
        """

        :param time: unit.Quantity
        :return: parmed_structure
        """

        current_weight = self.start_restraint_weight
        current_temp = self.start_temp
        temp_interval = (self.temperature.value_in_unit(unit.kelvin)-self.start_temp)/self.num_heat_stages
        if self.equil_time is not None:
            total_steps = ((self.num_heat_stages + self.num_release_stages) \
                           * self.stage_run_time + self.equil_time) * unit.nanosecond / self.step_length
            equil_steps = int(round(self.equil_time * unit.nanosecond /self.step_length))
        else:
            total_steps = ((self.num_heat_stages + self.num_release_stages) \
                           * self.stage_run_time) * unit.nanosecond / self.step_length

        self._add_reporters(total_steps)

        print('starting temp', self.start_temp)
        print('starting restraint weight ',current_weight)

        stage_steps = int(round(self.stage_run_time * unit.nanosecond /self.step_length))

        for i in range(self.num_heat_stages):
            self.simulation.step(stage_steps)
            current_temp+=temp_interval
            print(' setting temp to ',current_temp)
            self.integrator.setTemperature(current_temp * unit.kelvin)

        for i in range(self.num_release_stages):
            self.simulation.step(stage_steps)
            print('setting restraint weight to ',current_weight)
            current_weight -= self.start_restraint_weight/self.num_release_stages
            self.update_restraint_weight(current_weight)

        if self.equil_time is not None:
            print('equilibrating for {} ns'.format(self.equil_time))
            self.simulation.step(equil_steps)

        self.update_parmed()

        self.simulation.reporters.clear()
        return self.parmed_structure


class MetadynamicSimulation(MDSimulation):
    """
    Metadynamics Simulation Class

    A maximum of 3 CVs can be specified, and each CV must be one of the following:
    'Distance, RMSD, Z-Proj, Angle'

    Examples
    --------

    CVs are specified in a list with strict formatting
    >>> CV_list = [
    >>> ['Distance', 'ligand', 'resid A 1', 0, 4, .1],
    >>> ['RMSD', 'protein', 'None', 0, 2, .02 ]
    >>> ]

    >>> metaD = MetadynamicSimulation(parmed_structure = parmed_structure,
    >>>                        dome=True,
    >>>                        CV_list= CV_list, run_time=25 * unit.nanosecond)
    >>>
    >>>metaD.run()


    Parameters
    ----------
    CV_list : list of CVs and CV specs (see above)

    funnel : bool, optional

    dome : bool, optional

    radius_scale_factor : float, optional
        factor for determining the radius of funnel or dome relative to ligand size

    funnel_angle : float, optional
        angle of the funnel wrt to line intersecting cone apex from center of funnel

    bias_factor : int, optional

    initial_bias_height : unit.Quantity, optional

    bias_frequency : unit.Quantity, optional
        frequency with which to deposit bias, default 1 ps

    bias_save_frequency :  unit.Quantity, optional
        frequency with which to write bias to disk, must be a multiple of bias_freq

    bias_directory : string, optional
        string specifying where to write the bias file. If blank it will write to self.cwd

    fes_interval : unit.Quantity, optional
        frequency with which to write FES and CV values to disk


    """
    def __init__(self, CV_list=[],
                 funnel=False, radius_scale_factor=2,
                 dome=False, funnel_angle=.5,
                 bias_factor=20,
                 initial_bias_height=2 * unit.kilojoule_per_mole,
                 bias_frequency=1 * unit.picoseconds,
                 bias_save_frequency=1 * unit.picoseconds,
                 bias_directory=None,
                 fes_interval=.5 * unit.nanoseconds,
                 **kwargs):

        super().__init__(**kwargs)

        #set up init vars
        self.CV_list = CV_list
        self.bias_factor = bias_factor
        self.initial_bias_height = initial_bias_height
        self.bias_frequency = int(bias_frequency / self.step_length)
        self.bias_save_frequency = int(bias_save_frequency / self.step_length)
        self.fes_interval = int(fes_interval / self.step_length)

        if bias_directory is not None:
            self.bias_directory = bias_directory
        else:
            self.bias_directory = self.cwd


        # build funnel or dome restraints in init
        if dome:
            if self.membrane:
                raise ValueError(
                    'Spherical restraints should not be used for channel protein systems with deep binding pockets.')

            # Now get the setup stage for placing sphere (otherwise coords may be wrapped)
            lig_atom_index = select_atoms(self.parmed_structure, keyword_selection='ligand')
            prot_atom_index = select_atoms(self.parmed_structure, keyword_selection='protein')

            lig_positions = np.array(self.positions.value_in_unit(unit.nanometer))[lig_atom_index]

            if len(lig_atom_index) == 0 or len(prot_atom_index) == 0:
                raise ValueError('could not select ligand or protein for dome placement')

            radius, center = find_radius_and_center(lig_positions, radius_scale_factor)

            print('Adding a spherical potential to keep ligand near binding site ',
                  'using the following params',
                  ' radius: {} rcenter: {}'.format(radius, center))
            print('Note, this should only be used for shallow binding pockets')

            spherical_boundary_force = mm.CustomExternalForce(
                'K*max(0, (r-radius))^2; r=sqrt(periodicdistance(x,y,z,x0,y0,z0)^2)')

            spherical_boundary_force.addGlobalParameter('K', 30)
            spherical_boundary_force.addGlobalParameter('radius', radius)
            spherical_boundary_force.addGlobalParameter('x0', center[0])
            spherical_boundary_force.addGlobalParameter('y0', center[1])
            spherical_boundary_force.addGlobalParameter('z0', center[2])

            self.custom_forces['dome'] = self.system.addForce(spherical_boundary_force)

            # use the inherited restrain COM to keep the protein from floating away
            self.restrain_COM(atom_selection=prot_atom_index, COM_restraint_weight=10)

        if funnel:
            if not self.membrane:
                raise ValueError('funnel for non-membrane systems not yet supported.')

            # Now get the setup stage for placing funnel (otherwise coords may be wrapped)
            lig_atom_index = select_atoms(self.parmed_structure, keyword_selection='ligand')
            prot_atom_index = select_atoms(self.parmed_structure, keyword_selection='protein')
            lig_positions = np.array(self.positions.value_in_unit(unit.nanometer))[lig_atom_index]
            prot_positions = np.array(self.positions.value_in_unit(unit.nanometer))[prot_atom_index]

            if len(lig_atom_index) == 0 or len(prot_atom_index) == 0:
                raise ValueError('could not select ligand or protein for funnel placement')

            print('lig ave zcoord used for funnel placement: {}'.format(np.mean(lig_positions, axis=0)[2]))
            print('prot ave zcoord used for funnel placement: {}'.format(np.mean(prot_positions, axis=0)[2]))

            # if the ligand is on the positive z-side use the z coordinate dimension
            if np.mean(lig_positions, axis=0)[2] > np.mean(prot_positions, axis=0)[2]:
                z_cone_apex = self.box_vectors[2][2].value_in_unit(unit.nanometer)
                orient_factor = -1
            # else use the negative dimension
            else:
                z_cone_apex = 0
                orient_factor = 1

            r_cyl, center = find_radius_and_center(lig_positions, radius_scale_factor)

            print('Adding a funnel potential to keep ligand near channel',
                  'mouth using the following params',
                  'r_cyl: {} zcc: {} alpha: {}, ligand COG {} '.format(r_cyl, z_cone_apex, funnel_angle, center))
            print('Note! This funnel assumes that the channel protein extracellular domain is aligned ',
                  'with the z-axis')

            # the funnel shape depends on the radius and the x,y as function of z, needs to use periodicdistance()
            funnel_force = mm.CustomExternalForce(
                'K*max(0, (r-radius))^2; r=sqrt(periodicdistance(x,y,z*0,x0,y0,zcc*0)^2); '
                'radius=min(r_cyl,(tan(alpha)*orient_factor*periodicdistance(x*0,y*0,z,x0*0,y0*0,zcc)))')

            funnel_force.addGlobalParameter('K', 10)
            funnel_force.addGlobalParameter('r_cyl', r_cyl)
            funnel_force.addGlobalParameter('zcc', z_cone_apex)
            funnel_force.addGlobalParameter('orient_factor', orient_factor)
            funnel_force.addGlobalParameter('alpha', funnel_angle)
            funnel_force.addGlobalParameter('x0', center[0])
            funnel_force.addGlobalParameter('y0', center[1])
            self.custom_forces['funnel'] = self.system.addForce(funnel_force)
            for i in lig_atom_index:
                funnel_force.addParticle(i, [])

        CVs = []
        self.bin_lengths = []
        # cv list format will be:
        #       cv[0] = cv name
        #       cv[1] = atom_selection1
        #       cv[2] = atom_selection2
        #       cv[3] = cv min value
        #       cv[4] = cv max value
        #       cv[5] = cv bin width

        print('Building collective variables with the following specifications: {}'.format(CV_list))

        for cv in CV_list:
            if cv[0] == 'RMSD':

                if cv[1].startswith('resid'):
                    resid_list = cv[1][6:]
                    atom_set = select_atoms(self.parmed_structure, resid_selection=resid_list)
                else:
                    atom_set = select_atoms(self.parmed_structure, keyword_selection=cv[1])

                if len(atom_set) == 0:
                    raise ValueError('RMSD atom selection found no atoms')
                print('Number of atoms to be used for RMSD Bias: {}'.format(len(atom_set)))
                rmsd_force = mm.RMSDForce(self.positions, atom_set)
                rmsd_bias = mm.app.BiasVariable(rmsd_force,
                                                minValue=cv[3],
                                                maxValue=cv[4],
                                                biasWidth=cv[5])
                self.bin_lengths.append((cv[4] - cv[3]) / cv[5])
                CVs.append(rmsd_bias)

            if cv[0] == 'Distance':
                com_force = mm.CustomCentroidBondForce(2, 'distance(g1,g2)')

                # find first group
                if cv[1].startswith('resid'):
                    resid_list = cv[1][6:]
                    atom_group1 = select_atoms(self.parmed_structure, resid_selection=resid_list)
                else:
                    atom_group1 = select_atoms(self.parmed_structure, keyword_selection=cv[1])

                # find second group
                if cv[2].startswith('resid'):
                    resid_list = cv[2][6:]
                    atom_group2 = select_atoms(self.parmed_structure, resid_selection=resid_list)
                else:
                    atom_group2 = select_atoms(self.parmed_structure, keyword_selection=cv[2])

                if len(atom_group1) == 0 or len(atom_group2) == 0:
                    raise ValueError('One of the atom selection sets has no atoms')

                print('num atoms being used in 1st moeity: {}'.format(len(atom_group1)))
                print('num atoms being used in 2nd moeity: {}'.format(len(atom_group2)))
                com_force.addGroup(atom_group1)
                com_force.addGroup(atom_group2)
                com_force.addBond([0, 1])
                com_bias = mm.app.BiasVariable(com_force,
                                               minValue=cv[3],
                                               maxValue=cv[4],
                                               biasWidth=cv[5])
                CVs.append(com_bias)

                self.bin_lengths.append((cv[4] - cv[3]) / cv[5])

            if cv[0] == 'Z-Proj':
                # z-proj is just a distance force using only the z components
                zproj_force = mm.CustomCentroidBondForce(2, 'abs(z1-z2)')

                # find first group
                if cv[1].startswith('resid'):
                    resid_list = cv[1][6:]
                    atom_group1 = select_atoms(self.parmed_structure, resid_selection=resid_list)
                else:
                    atom_group1 = select_atoms(self.parmed_structure, keyword_selection=cv[1])

                # find second group
                if cv[2].startswith('resid'):
                    resid_list = cv[2][6:]
                    atom_group2 = select_atoms(self.parmed_structure, resid_selection=resid_list)
                else:
                    atom_group2 = select_atoms(self.parmed_structure, keyword_selection=cv[2])

                if len(atom_group1) == 0 or len(atom_group2) == 0:
                    raise ValueError('One of the atom selection sets has no atoms')

                zproj_force.addGroup(atom_group1)
                zproj_force.addGroup(atom_group2)
                zproj_force.addBond([0, 1])
                z_bias = mm.app.BiasVariable(zproj_force,
                                             minValue=cv[3],
                                             maxValue=cv[4],
                                             biasWidth=cv[5])
                self.bin_lengths.append((cv[4] - cv[3]) / cv[5])
                CVs.append(z_bias)

            if cv[0] == 'Angle':
                # angle force can only be applied to three atoms, but they don't need to be bound
                # if we want to support angles between groups we can use CustomCentroidBondForce
                angle_force = mm.CustomAngleForce('theta')

                lig_atom_index = select_atoms(self.parmed_structure, keyword_selection='ligand')
                prot_atom_index = select_atoms(self.parmed_structure, keyword_selection='protein')
                lig_positions = np.array(self.positions.value_in_unit(unit.nanometer))[lig_atom_index]
                prot_positions = np.array(self.positions.value_in_unit(unit.nanometer))[prot_atom_index]
                three_coords, indeces = get_angle_particle_coords(lig_positions, prot_positions)
                print('Using atoms {}, {}, {} for angle bias'.format(indeces[0], indeces[1], indeces[2]))
                angle_force.addAngle(indeces[0], indeces[1], indeces[2])
                angle_bias = mm.app.BiasVariable(angle_force,
                                                 minValue=cv[3],
                                                 maxValue=cv[4],
                                                 biasWidth=cv[5],
                                                 periodic=True)
                self.bin_lengths.append((cv[4] - cv[3]) / cv[5])
                CVs.append(angle_bias)


        #all bins must be the same shape
        if not self.bin_lengths[1:] == self.bin_lengths[:-1]:
            raise ValueError(
                'Bias dimensions must be equal for all CVs specified. Please adjust the max, min, and binwidths',
                'such that max-min/width are equal for all CVs')


        # build sim
        self.metaD = mm.app.Metadynamics(system=self.system,
                                         variables=CVs,
                                         temperature=self.temperature,
                                         biasFactor=self.bias_factor,
                                         height=self.initial_bias_height,
                                         frequency=self.bias_frequency,
                                         saveFrequency=self.bias_save_frequency,
                                         biasDir=self.bias_directory)

        self.simulation.context.reinitialize()
        self.simulation.context.setPositions(self.positions)


    def _add_FESReporter(self):
        """
        adds the FES reporter to the sim
        :return:
        """

        fes_steps = int(round(self.fes_interval))

        if fes_steps == 0:
            raise ValueError('FES interval cannot be zero')

        FES_reporter = FESReporter(self.cwd, reportInterval=fes_steps, metaD_wrapper=self.metaD, CV_list=self.CV_list)
        self.simulation.reporters.append(FES_reporter)

    def run(self, time):
        """

        :param time: unit.Quantity, optional
        :return:  updated parmed
        """

        if not isinstance(time, unit.Quantity):
            raise ValueError('sim time must have units')

        nsteps = int(time / self.step_length)

        self._add_reporters(nsteps)

        if FESReporter:
            self._add_FESReporter()

        self.metaD.step(self.simulation, nsteps)

        self.update_parmed()
        self.simulation.reporters.clear()
        return self.parmed_structure

class SimulatedTemperingSimulation(MDSimulation):
    """
    Simulated Tempering simulation which samples multiple temperatures via a Weng-Landau weights and
    metropolis monte carlo temperature updates.

    Parameters
    ----------

    minTemperature:

    numTemperatures:

    maxTemperature:

    reportInterval:

    reportFile:

    """
    def __init__(self, numTemperatures=7, minTemperature=300 * unit.kelvin, maxTemperature=450 * unit.kelvin,
                 reportInterval=1000, reportFile='weights.dat', **kwargs):
        super().__init__(**kwargs)
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature
        self.numTemperatures = numTemperatures
        self.reportInterval = reportInterval
        self.reportFile = os.path.join(self.cwd, reportFile)

        self.ser_temp = mm.app.SimulatedTempering(self.simulation,
                                                  numTemperatures=self.numTemperatures,
                                                  minTemperature=self.minTemperature,
                                                  maxTemperature=self.maxTemperature,
                                                  reportInterval=self.reportInterval,
                                                  reportFile=self.reportFile)

    def run(self, time):
        """

        :param time: unit.Quantity, optional
        :return: updated parmed
        """
        if not isinstance(time, unit.Quantity):
            raise ValueError('time must have units')

        total_nsteps = int(round(time / self.step_length))

        self._add_reporters(total_nsteps)

        self.ser_temp.step(total_nsteps)

        self.update_parmed()

        self.simulation.reporters.clear()
        return self.parmed_structure


if __name__ == '__main__':
    import _pickle as pickle

    import sys

    if len(sys.argv[1:]) != 2:
        print("Usage: python rs_simtools.py pickled_sim end_parmed")
        exit(1)
    else:
        pickled_sim, new_parmed_file = sys.argv[1:]

        try:
            with open(pickled_sim, 'rb') as handle:
                mdsim = pickle.load(handle)
        except:
            raise
        
        mdsim.cwd = os.getcwd()
        mdsim.progress_out = sys.stdout
        mdsim._build_sim()

        new_parmed = mdsim.run()

        with open(new_parmed_file,'wb') as handle:
            pickle.dump(new_parmed.__getstate__(), handle)