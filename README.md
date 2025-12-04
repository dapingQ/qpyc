# Qpyc 

A python package for controlling Quantum Photonic Integrated Circuits (QPyc).

```
‾‾\__/‾‾\__/‾‾‾‾‾‾‾‾‾‾\__/‾‾\__/‾‾‾‾‾‾‾‾‾‾\__/‾‾\__/‾‾‾‾‾‾‾‾‾‾‾‾
__/‾‾\__/‾‾\          /‾‾\__/‾‾\          /‾‾\__/‾‾\            
            \__/‾‾\__/          \__/‾‾\__/          \__/‾‾\__/‾‾
            /‾‾\__/‾‾\          /‾‾\__/‾‾\          /‾‾\__/‾‾\__
‾‾\__/‾‾\__/          \__/‾‾\__/          \__/‾‾\__/            
__/‾‾\__/‾‾\          /‾‾\__/‾‾\          /‾‾\__/‾‾\            
            \__/‾‾\__/          \__/‾‾\__/          \__/‾‾\__/‾‾
            /‾‾\__/‾‾\          /‾‾\__/‾‾\          /‾‾\__/‾‾\__
‾‾\__/‾‾\__/          \__/‾‾\__/          \__/‾‾\__/            
__/‾‾\__/‾‾\__________/‾‾\__/‾‾\__________/‾‾\__/‾‾\____________
```

## Features

- Configurable, editable classes for integrated photonic circuits
- Calibration and controlling 
- Universal unitary matrix mesh (Reck, Clements)

## Installation

1. download or clone the repo, `git clone https://github.com/dapingQ/qpyc`
2. enter the repo, `cd qpyc`
3. install in the editable mode, `pip intall -e .`

## Development

### Devive.py

The `Device.py` file contains the core classes and methods for defining and manipulating optical components in a quantum photonic integrated circuit. Below is a brief overview of the main classes and their functionalities:

#### Component Class

The `Component` class is an abstract base class for all optical components. It includes properties and methods for:
- Address (`addr`): The position of the component in the circuit.
- Dimension (`dom`): The number of waveguides or ports.
- Matrix representation (`matrix`): The unitary matrix representing the component.
- Merging and spanning components (`merge`, `span`).

#### Waveguide Class

The `Waveguide` class inherits from `Component` and represents an optical waveguide. It has a matrix representation as an identity matrix.

#### PhaseShifter Class

The `PhaseShifter` class inherits from `Component` and represents a phase shifter. It includes:
- Phase (`phase`): The phase shift in units of π.
- Matrix representation as a complex exponential.

#### BeamSpiliter Class

The `BeamSpiliter` class inherits from `Component` and represents a beam splitter with a bias. It includes:
- Bias (`bias`): The bias angle in units of π.
- Matrix representation as a 2x2 unitary matrix.

#### MZI Class

The `MZI` class inherits from `Component` and represents a Mach-Zehnder interferometer. It includes:
- Internal and external phases (`theta`, `phi`).
- Biases for the beam splitters (`bias`).
- Matrix representation as a product of the constituent components.

#### Circuit Class

The `Circuit` class represents a collection of components arranged in a circuit. It includes methods for:
- Adding and removing components (`add`, `remove`).
- Calculating the overall matrix representation (`matrix`).
- Plotting the circuit (`plot`).

These classes provide a flexible and extensible framework for modeling and simulating quantum photonic circuits.
