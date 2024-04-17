import subprocess
import logging
import os
import re
from datetime import datetime

def Create():

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


    return output




def Change(contract_id,text):

    command = '''octez-client -E https://mainnet.api.tez.ie transfer 0 from doner to ''' + contract_id + ''' --entrypoint update_text --arg '" ''' + text + ''' "' --burn-cap 0.1'''
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode == 0:
        logging.info("Command executed successfully!")
    else:
        logging.error("Error executing command:")
    return process.returncode