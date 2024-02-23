import os
import shutil
import time
import argparse
import logging

# Function that handles all the logging configurations (file and console)
def setup_log(log_file):
    
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    console.setFormatter(formatter)
    
    logging.getLogger('').addHandler(console)

# Function that synchronizes folders
def synchronize(source, replica):
    
    try:
        
        # Creates replica folder if not exists
        if not os.path.exists(replica):
            os.makedirs(replica)
        
        # Iterates files in source folder
        for root, dirs, files in os.walk(source):
            for file in files:
                source_path = os.path.join(root, file)
                replica_path = os.path.join(replica, os.path.relpath(source_path, source))

                # Create/update file in replica folder
                shutil.copy2(source_path, replica_path)

                # Write log message
                logging.info(f'Created/Updated: {source_path} -> {replica_path}')

        # Iterats files in replica folder
        for root, dirs, files in os.walk(replica):
            for file in files:
                replica_path = os.path.join(root, file)
                source_path = os.path.join(source, os.path.relpath(replica_path, replica))

                if not os.path.exists(source_path):
                    
                    # Remove file from replica folder
                    os.remove(replica_path)
                    
                    # Write log message
                    logging.info(f'Removed: {replica_path}')

    except Exception as e:
        logging.error(f'Error Exception: {e}')
        
# Uses the argparse module to parse the arguments from command line interface and return them
def get_args():
    
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, help='Path to the log file')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    
    return parser.parse_args()

def main():

    args = get_args()

    setup_log(args.log_file)

    try:
        while True:
            
            logging.info('Start of synchronization')
            synchronize(args.source, args.replica)
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        logging.info('End of synchronization')

if __name__ == '__main__':
    main()
