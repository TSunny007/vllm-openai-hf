import os
import subprocess
import re

# Function to convert environment variable names to command-line arguments
def convert_to_flag(env_var):
    # Convert to lowercase and replace underscores with hyphens
    flag = re.sub(r'^VLLM_FLAG_', '--', env_var).lower().replace('_', '-')
    return flag

# Collect all relevant VLLM_FLAG_* environment variables
vllm_flags = {}
for key, value in os.environ.items():
    if key.startswith('VLLM_FLAG_'):
        flag = convert_to_flag(key)
        vllm_flags[flag] = value

# Build the command to run vllm serve
command = ['vllm', 'serve', os.getenv('MODEL_DIR', '/repository')]

# Add the flags and their values
for flag, value in vllm_flags.items():
    # Handle flags without values (e.g., --allow-credentials)
    if value.lower() == 'true':
        command.append(flag)
    elif value.lower() != 'false':  # Ignore 'false' values
        command.extend([flag, value])


# Execute the vllm serve command
print(f"Running command: {' '.join(command)}")
subprocess.run(command)
