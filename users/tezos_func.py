import subprocess
import logging
import os
import re
from datetime import datetime

def Create():

    log_directory = "log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Setup logging configuration with time-stamped filename in the 'log' directory
    log_filename = os.path.join(log_directory, datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log"))
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Define the command as a multi-line string
    command = """
        octez-client --endpoint https://mainnet.smartpy.io originate contract contract_edf68f2affb9b99af1737129 \
        transferring 0 \
        from doner \
        running contract.tz \
        --init '""' \
        --fee 0.0015 \
        --gas-limit 10600 \
        --storage-limit 496 --force
        """

    # Execute the command using subprocess
    process = subprocess.run(command, shell=True, text=True, capture_output=True)

    # Log the results with timestamp
    if process.returncode == 0:
        logging.info("Command executed successfully!")
    else:
        logging.error("Error executing command:")

    # Log output or error regardless of success
    output = process.stdout if process.stdout else process.stderr
    logging.info("Output: %s", output)

    # Regex to find the contract ID following "Originated contracts:"
    contract_id = "No contract ID found"
    match = re.search(r"Originated contracts:\s+(KT1\w+)", output)
    if match:
        contract_id = match.group(1)

    return contract_id




def Change(contract_id,text):

    command = '''octez-client -E https://mainnet.api.tez.ie transfer 0 from doner to ''' + contract_id + ''' --entrypoint update_text --arg '" ''' + text + ''' "' --burn-cap 0.1'''
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode == 0:
        logging.info("Command executed successfully!")
    else:
        logging.error("Error executing command:")
    return process.returncode

def Read(contract_address):
    base_url = "https://api.tzkt.io/v1/contracts"
    url = f"{base_url}/{contract_address}/storage"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to retrieve data: {response.status_code}"

# Example contract address
contract_address = "KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton"
storage = Read(contract_address)
print(storage)