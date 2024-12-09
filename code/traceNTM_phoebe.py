import os
import csv

class Configuration:
    def __init__(self, state, tape, head_position):
        self.state = state
        self.tape = tape
        self.head_position = head_position

    def __str__(self):
        left = ''.join(self.tape[:self.head_position])
        right = ''.join(self.tape[self.head_position + 1:])
        return f"{left}({self.state},{self.tape[self.head_position]}){right}"


def parse_ntm(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader]

    # Extract header
    machine_name = lines[0][0]
    states = lines[1]
    input_alphabet = lines[2]
    tape_alphabet = lines[3]
    start_state = lines[4][0]
    accept_state = lines[5][0]
    reject_state = lines[6][0]

    # Parse transitions
    transitions = {}
    for line in lines[7:]:
        current_state, read_char, next_state, write_char, direction = line
        key = (current_state, read_char)
        if key not in transitions:
            transitions[key] = []
        transitions[key].append((next_state, write_char, direction))

    return {
        "name": machine_name,
        "states": states,
        "input_alphabet": input_alphabet,
        "tape_alphabet": tape_alphabet,
        "start_state": start_state,
        "accept_state": accept_state,
        "reject_state": reject_state,
        "transitions": transitions
    }
    
def simulate_ntm(ntm, input_string, max_depth=None, max_steps=None, debug=False):
    transitions = ntm["transitions"]
    start_state = ntm["start_state"]
    accept_state = ntm["accept_state"]

    initial_tape = list(input_string) + ["_"]
    initial_config = Configuration(start_state, initial_tape, 0)

    tree = [[initial_config]]
    output_lines = []
    output_lines.append(f"Machine: {ntm['name']}")
    output_lines.append(f"Input string: {input_string}")

    for depth in range(max_depth or float('inf')):
        current_level = tree[depth]
        next_level = []
        for config in current_level:
            if debug:
                output_lines.append(f"Debug: Exploring configuration: {config}")

            # Halt immediately if the machine reaches the accept state
            if config.state == accept_state:
                output_lines.append(f"String accepted in {depth} steps")
                output_lines.append("Path to acceptance:")

                # Reconstruct the path to the accept state
                path_to_acceptance = []
                seen_configurations = set()
                for d in range(depth + 1):
                    formatted_config = format_configuration(tree[d][0])
                    if formatted_config not in seen_configurations:
                        path_to_acceptance.append(formatted_config)
                        seen_configurations.add(formatted_config)

                # Add the final configuration for qacc if not already added
                final_formatted_config = format_configuration(config)
                if final_formatted_config not in seen_configurations:
                    path_to_acceptance.append(final_formatted_config)

                output_lines.extend(path_to_acceptance)
                return output_lines  # Stop all further processing

            # Fetch transitions for the current configuration
            key = (config.state, config.tape[config.head_position])
            if key not in transitions:
                if debug:
                    output_lines.append(f"Debug: No transition found for {key}, implicitly rejecting")
                continue

            for next_state, write_char, direction in transitions[key]:
                if debug:
                    output_lines.append(f"Debug: Transition: {config.state} + {config.tape[config.head_position]} -> {next_state} ({write_char}, {direction})")

                # Stop processing transitions if the accept state is reached
                if next_state == accept_state:
                    output_lines.append(f"String accepted in {depth + 1} steps")
                    output_lines.append("Path to acceptance:")
                    path_to_acceptance = []
                    seen_configurations = set()
                    for d in range(depth + 1):
                        formatted_config = format_configuration(tree[d][0])
                        if formatted_config not in seen_configurations:
                            path_to_acceptance.append(formatted_config)
                            seen_configurations.add(formatted_config)
                    final_formatted_config = format_configuration(config)
                    if final_formatted_config not in seen_configurations:
                        path_to_acceptance.append(final_formatted_config)
                    final_accept_config = format_configuration(Configuration(next_state, config.tape, config.head_position))
                    if final_accept_config not in seen_configurations:
                        path_to_acceptance.append(final_accept_config)
                    output_lines.extend(path_to_acceptance)
                    return output_lines

                # Process valid transitions
                new_tape = config.tape[:]
                new_tape[config.head_position] = write_char
                new_head_position = config.head_position + (1 if direction == "R" else -1)

                if new_head_position < 0 or new_head_position >= len(new_tape):
                    if debug:
                        output_lines.append(f"Debug: Head out of bounds at position {new_head_position}")
                    continue

                next_level.append(Configuration(next_state, new_tape, new_head_position))

                if max_steps and len(next_level) >= max_steps:
                    output_lines.append(f"Execution stopped after step limit of {max_steps}")
                    return output_lines

        if not next_level:
            # Longest path to the last rejection
            output_lines.append(f"String rejected in {depth} steps")
            output_lines.append("Longest path to rejection:")
            
            # Reconstruct the longest path
            longest_path = []
            seen_configurations = set()
            for d in range(depth + 1):
                formatted_config = format_configuration(tree[d][0])
                if formatted_config not in seen_configurations:
                    longest_path.append(formatted_config)
                    seen_configurations.add(formatted_config)
            
            output_lines.extend(longest_path)
            return output_lines


        tree.append(next_level)

    output_lines.append(f"Execution stopped after max depth of {max_depth}")
    return output_lines



def format_configuration(config):
    """Format the configuration as 'left_of_headstatehead_characterright_of_head'."""
    tape = config.tape
    head_position = config.head_position
    state = config.state

    left_of_head = ''.join(tape[:head_position])
    head_character = tape[head_position]
    right_of_head = ''.join(tape[head_position + 1:])

    return f"{left_of_head}{state}{head_character}{right_of_head}"




def parse_input_file(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    params = {}
    for line in lines:
        key, value = line.strip().split("=", 1)  # Use maxsplit to avoid errors with values containing "="
        if key == "input_strings":
            params[key] = [s.strip() for s in value.split(",")]  # Strip spaces from each string
        elif key in {"max_depth", "max_steps"}:
            params[key] = int(value)
        elif key == "debug":
            params[key] = value.lower() == "true"
        else:
            params[key] = value

    return params




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
