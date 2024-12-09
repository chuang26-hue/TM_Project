import os
import csv

# Class representing the configuration of a Turing Machine
class Configuration:
    def __init__(self, state, tape, head_position):
        # Initialize with the current state, tape, and head position
        self.state = state
        self.tape = tape
        self.head_position = head_position

    def __str__(self):
        # Format the Turing Machine's tape for readability
        # Displays the tape with the head position indicated by parentheses
        left = ''.join(self.tape[:self.head_position])  # Tape content to the left of the head
        right = ''.join(self.tape[self.head_position + 1:])  # Tape content to the right of the head
        return f"{left}({self.state},{self.tape[self.head_position]}){right}"  # Combine into readable string


# Function to parse a non-deterministic Turing Machine (NTM) description from a file
def parse_ntm(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)  # Read the file using CSV reader
        lines = [line for line in reader]  # Collect all lines into a list

    # Extract machine details from the header lines
    machine_name = lines[0][0]  # Name of the machine
    states = lines[1]  # List of states
    input_alphabet = lines[2]  # Input alphabet
    tape_alphabet = lines[3]  # Tape alphabet
    start_state = lines[4][0]  # Start state
    accept_state = lines[5][0]  # Accept state
    reject_state = lines[6][0]  # Reject state

    # Parse transition rules starting from the 8th line onward
    transitions = {}
    for line in lines[7:]:
        current_state, read_char, next_state, write_char, direction = line  # Transition details
        key = (current_state, read_char)  # Current state and character read
        if key not in transitions:
            transitions[key] = []  # Initialize a list if key is not present
        transitions[key].append((next_state, write_char, direction))  # Append the transition tuple

    # Return the parsed Turing Machine description as a dictionary
    return {
        "name": machine_name,  # Name of the machine
        "states": states,  # List of states
        "input_alphabet": input_alphabet,  # Input alphabet
        "tape_alphabet": tape_alphabet,  # Tape alphabet
        "start_state": start_state,  # Start state
        "accept_state": accept_state,  # Accept state
        "reject_state": reject_state,  # Reject state
        "transitions": transitions  # Transition rules
    }

    
# Simulate the behavior of a non-deterministic Turing Machine (NTM)
def simulate_ntm(ntm, input_string, max_depth=None, max_steps=None, debug=False):
    transitions = ntm["transitions"]  # Extract transitions from the NTM definition
    start_state = ntm["start_state"]  # Extract the start state
    accept_state = ntm["accept_state"]  # Extract the accept state

    initial_tape = list(input_string) + ["_"]  # Initialize the tape with input string and blank symbol
    initial_config = Configuration(start_state, initial_tape, 0)  # Set initial configuration of the NTM

    tree = [[initial_config]]  # Create a tree to store configurations at each depth
    output_lines = []  # Store output messages for simulation results
    output_lines.append(f"Machine: {ntm['name']}")  # Add machine name to output
    output_lines.append(f"Input string: {input_string}")  # Add input string to output

    for depth in range(max_depth or float('inf')):  # Simulate for a maximum depth or until halted
        current_level = tree[depth]  # Get the configurations at the current depth
        next_level = []  # Prepare to store configurations for the next depth
        for config in current_level:
            if debug:  # Debug mode to trace steps
                output_lines.append(f"Debug: Exploring configuration: {config}")

            # Check if the machine is in the accept state
            if config.state == accept_state:
                output_lines.append(f"String accepted in {depth} steps")
                output_lines.append("Path to acceptance:")

                # Reconstruct the path to the accept state
                path_to_acceptance = []
                seen_configurations = set()
                for d in range(depth + 1):
                    formatted_config = format_configuration(tree[d][0])  # Format configurations
                    if formatted_config not in seen_configurations:
                        path_to_acceptance.append(formatted_config)  # Append unique configurations
                        seen_configurations.add(formatted_config)

                # Add the final configuration if not already added
                final_formatted_config = format_configuration(config)
                if final_formatted_config not in seen_configurations:
                    path_to_acceptance.append(final_formatted_config)

                output_lines.extend(path_to_acceptance)  # Append path to output
                return output_lines  # Stop simulation upon acceptance

            # Fetch possible transitions for the current state and tape symbol
            key = (config.state, config.tape[config.head_position])
            if key not in transitions:
                if debug:  # Debug message for missing transitions
                    output_lines.append(f"Debug: No transition found for {key}, implicitly rejecting")
                continue

            for next_state, write_char, direction in transitions[key]:  # Process each valid transition
                if debug:  # Debug message for transitions
                    output_lines.append(f"Debug: Transition: {config.state} + {config.tape[config.head_position]} -> {next_state} ({write_char}, {direction})")

                # Check if the transition leads to the accept state
                if next_state == accept_state:
                    output_lines.append(f"String accepted in {depth + 1} steps")
                    output_lines.append("Path to acceptance:")
                    path_to_acceptance = []
                    seen_configurations = set()
                    for d in range(depth + 1):
                        formatted_config = format_configuration(tree[d][0])  # Format configurations
                        if formatted_config not in seen_configurations:
                            path_to_acceptance.append(formatted_config)
                            seen_configurations.add(formatted_config)
                    final_formatted_config = format_configuration(config)
                    if final_formatted_config not in seen_configurations:
                        path_to_acceptance.append(final_formatted_config)
                    final_accept_config = format_configuration(Configuration(next_state, config.tape, config.head_position))
                    if final_accept_config not in seen_configurations:
                        path_to_acceptance.append(final_accept_config)
                    output_lines.extend(path_to_acceptance)  # Append path to output
                    return output_lines

                # Update the tape and head position for the new configuration
                new_tape = config.tape[:]
                new_tape[config.head_position] = write_char  # Write the character to the tape
                new_head_position = config.head_position + (1 if direction == "R" else -1)  # Move the head

                # Check for out-of-bounds head position
                if new_head_position < 0 or new_head_position >= len(new_tape):
                    if debug:  # Debug message for out-of-bounds head
                        output_lines.append(f"Debug: Head out of bounds at position {new_head_position}")
                    continue

                next_level.append(Configuration(next_state, new_tape, new_head_position))  # Add new configuration

                # Stop simulation if the maximum step limit is reached
                if max_steps and len(next_level) >= max_steps:
                    output_lines.append(f"Execution stopped after step limit of {max_steps}")
                    return output_lines

        if not next_level:  # No more configurations to process
            output_lines.append(f"String rejected in {depth} steps")
            output_lines.append("Longest path to rejection:")

            # Reconstruct the longest path to rejection
            longest_path = []
            seen_configurations = set()
            for d in range(depth + 1):
                formatted_config = format_configuration(tree[d][0])  # Format configurations
                if formatted_config not in seen_configurations:
                    longest_path.append(formatted_config)  # Append unique configurations
                    seen_configurations.add(formatted_config)

            output_lines.extend(longest_path)  # Append path to output
            return output_lines

        tree.append(next_level)  # Add the next level to the tree

    output_lines.append(f"Execution stopped after max depth of {max_depth}")  # Simulation halted by max depth
    return output_lines




def format_configuration(config):
    """Format the configuration as 'left_of_headstatehead_characterright_of_head'."""
    # Extract the tape, head position, and state from the configuration
    tape = config.tape
    head_position = config.head_position
    state = config.state

    # Divide the tape into parts relative to the head position
    left_of_head = ''.join(tape[:head_position])  # Tape content to the left of the head
    head_character = tape[head_position]  # Character under the head
    right_of_head = ''.join(tape[head_position + 1:])  # Tape content to the right of the head

    # Combine all parts into the formatted configuration string
    return f"{left_of_head}{state}{head_character}{right_of_head}"


def parse_input_file(input_file):
    """Parse the input file to extract simulation parameters."""
    with open(input_file, 'r') as f:
        lines = f.readlines()  # Read all lines from the input file

    params = {}  # Initialize a dictionary to store parameters
    for line in lines:
        # Split each line into a key-value pair based on the '=' delimiter
        key, value = line.strip().split("=", 1)  # Use maxsplit=1 to handle values with '='
        if key == "input_strings":
            params[key] = [s.strip() for s in value.split(",")]  # Handle multiple input strings
        elif key in {"max_depth", "max_steps"}:
            params[key] = int(value)  # Convert numeric parameters to integers
        elif key == "debug":
            params[key] = value.lower() == "true"  # Convert debug flag to boolean
        else:
            params[key] = value  # Store other parameters as strings

    return params  # Return the dictionary of parameters


if __name__ == "__main__":
    input_file = os.path.join("input", "input.txt")
    output_file = os.path.join("output", "output.txt")

    # Ensure directories exist
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("input"):
        os.makedirs("input")

    # Parse input file
    params = parse_input_file(input_file)

    # Parse the NTM
    ntm_file = "input/NTM.csv"
    ntm = parse_ntm(ntm_file)

    # Simulate and write all results to the output file
    all_output = []
    for idx, input_str in enumerate(params["input_strings"]):
        result = simulate_ntm(ntm, input_str, max_depth=params["max_depth"], max_steps=params["max_steps"], debug=params["debug"])
        all_output.extend(result)
        all_output.append("\n")

    # Write all outputs to the output.txt file and print to terminal
    with open(output_file, 'w') as f:
        f.write('\n'.join(all_output))

    print('\n'.join(all_output))
