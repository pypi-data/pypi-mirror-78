from . import jobbuilder  # relative import
import ray
from pathlib import Path
import yaml
import sys
import csv
import os


def touch_job(working_dir, line, status, error=None):
    '''
    Writes done.job or error.job into the appropriate tracking directory
    for the file
    '''
    abs_path = working_dir+'/tracking'+line.strip()
    Path(abs_path).mkdir(parents=True, exist_ok=True)
    if status == True:
        statusstr = 'done.job'
        Path(abs_path + '/' + statusstr).touch()
    else:
        statusstr = 'error.job'
        Path(abs_path + '/' + statusstr).touch()
        # Write error to the file
        Path(abs_path + '/' + statusstr).write_text(error)
    return


@ray.remote
def process_file(config_yaml, node_number, fn):
    '''
    Main function called by each process
    that goes down the nodejobfile.txt and calls a user-provided function
    `fn` on each filepath.

    Parameters:
        config_yaml: str : file path to the config YAML file
        node_number : int: the index of the child process 
        fn: (filestring: str) -> Dict : the function called for each file

    Returns:
        None, but:
        Guaranteed to print exactly one line of text for each file
        Generates a error.job or done.job for each file
    '''

    config = jobbuilder.read_yaml_file(config_yaml)

    # From the YAML file, get the nodejobtxt
    nodejobfilepath = str(config['working_dir'] + '/' +
                          str(node_number) + '.nodejobfile.txt')

    # Get the output file
    outputfilepath = str(config['output_path'] + '/' +
                         str(node_number) + '.results.csv')

    with open(nodejobfilepath, 'r') as f:
        with open(outputfilepath, 'a') as outfile:
            for line in f:
                filepath = line.rstrip()
                try:
                    results_dict = fn(filepath)

                    header_row = [key for key in results_dict]
                    writer = csv.DictWriter(outfile, fieldnames=header_row)
                    outfile.seek(0, 2)
                    if outfile.tell() == 0:  # If file is empty, write CSV header
                        writer.writeheader()
                    writer.writerow(results_dict)
                    print(
                        f"Processed trip {outputfilepath} in node {node_number}.")
                    touch_job(config['working_dir'], line, True)
                except Exception as e:  # think about catching more specific exceptions
                    print(f"Exception! {str(e)}")
                    touch_job(config['working_dir'],
                              line, False, error=str(e))


def run_jobs(config_yaml, fn):
    '''
    Main driver function

    Parameters:
        config_yaml: str : file path to the config YAML file
        fn: (filestring: str) -> Dict : the function called for each file
    '''
    config = jobbuilder.read_yaml_file(config_yaml)
    total_nodes = config['processes']

    # Start Ray
    ray.init()

    # fire up the Ray processes...
    futures = [None] * total_nodes
    print("Spinning up Ray processes...")
    for this_node in range(total_nodes):
        futures[this_node] = process_file.remote(config_yaml, this_node, fn)
        print(f"Process {this_node} spawned!")

    # get results from each process... (only returns when all the jobs are done!)
    for p in ray.get(futures):
        print(p)


if __name__ == "__main__":
    # read the yaml config and get the number of processes (total_nodes) to spin up
    config_yaml = sys.argv[1]
    fn = sys.argv[2]
    run_jobs(config_yaml, fn)
