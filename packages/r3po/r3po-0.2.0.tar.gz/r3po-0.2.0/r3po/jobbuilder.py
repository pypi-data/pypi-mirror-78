from pathlib import Path
from glob import glob
import yaml
import sys
from typing import Callable, List


def reset_all_errors(yaml_path):
    '''
    Deletes all error.job files so that we can process the errored jobs again

    Parameters:
        yaml_path: String: filepath to the config.yaml file

    Returns:
        None
    '''
    config = read_yaml_file(yaml_path)
    match = config['working_dir']+'/tracking/**/*'
    files: List[str] = glob(str(match), recursive=True)
    tracking_files = [f for f in files if f.endswith("error.job")]
    for f in tracking_files:
        Path(f).unlink()


def reset_all_tracking(yaml_path):
    '''
    Deletes all error.job and done.job files
    inside the working directory specified in config.yaml

    This is dangerous --- If you do this, you will lose all your progress
    if you need to restart the job. Only do this if you're willing to 
    delete everything and start again!

    Parameters:
        yaml_path: String: filepath to the config.yaml file

    Returns:
        None
    '''
    config = read_yaml_file(yaml_path)
    match = config['working_dir']+'/tracking/**/*'
    files: List[str] = glob(str(match), recursive=True)
    tracking_files = [f for f in files if (
        f.endswith("error.job") or f.endswith("done.job"))]
    for f in tracking_files:
        Path(f).unlink()


def _file_already_processed_(fs, working_dir) -> bool:
    '''
    Returns True if there is an error.job or done.job in the tracking folder
    for the filepath filestring fs, otherwise False

    Parameters:
        fs: String : file string
        working_dir: filepath to working directory

    Returns:
        bool: whether there's an error.job or done.job 
    '''
    error = Path(working_dir + '/tracking' + fs.strip() + '/error.job')
    done = Path(working_dir + '/tracking' + fs.strip() + '/done.job')
    return (error.is_file() or done.is_file())


def _generate_all_pending_files_(file_paths: List[str], working_dir) -> List[str]:
    '''
    Takes a list of filepaths and returns the ones that have not already been processed.
    '''
    return [line for line in file_paths if not _file_already_processed_(line, working_dir)]


def _distribute_filepaths_(file_paths: List[str], num_lists: int) -> List[List[str]]:
    '''
    Takes a list of file paths and returns `num_lists` lists of path files.
    '''
    lists = [[] for _ in range(num_lists)]
    for index, item in enumerate(file_paths):
        lists[index % num_lists].append(item)
    return lists


def write_filepaths_to_file(file_paths: List, working_dir: str, node_number: int):
    '''
    Writes filepaths to be processed to a .txt file, one filepath per line.

    Takes a list of file paths and a node_number and 
    writes to `node_number`.nodejobfile.txt
    '''
    outfile = str(working_dir + '/' + str(node_number) + '.nodejobfile.txt')
    with open(outfile, 'w') as f:
        f.writelines(file_path + '\n' for file_path in file_paths)


def write_nodejobfiles(file_path_parts: List[List[str]], working_dir: str):
    for (i, file_path_part) in enumerate(file_path_parts):
        write_filepaths_to_file(file_path_part, working_dir, i)


def remove_nodejobfiles(working_dir):
    for f in Path(working_dir).glob('*.nodejobfile.txt'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def read_yaml_file(yaml_path: str):
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        return config


def build_jobs(yaml_path: str):
    '''
    Reads a config YAML file found at yaml_path and generates
    a series of nodejobfile.txt
    '''
    config = read_yaml_file(yaml_path)
    print("Building job called: " + config['job_name'])

    Path(config['working_dir']).mkdir(parents=True, exist_ok=True)

    print("Reading job source directory and generating master job CSV file...")
    print("Scanning for files ending with " + config['source_file_part'])
    match = config['source_path']+'/**/*'+config['source_file_part']

    files: List[str] = glob(str(match), recursive=True)
    # Select only files that do not have .done or .error
    pending_files = _generate_all_pending_files_(files, config['working_dir'])
    print("Pending files generated.")

    # Remove old node job files and generate new ones
    print("Removing old node jobfiles...")
    remove_nodejobfiles(config['working_dir'])
    distributed_files = _distribute_filepaths_(
        pending_files, config['processes'])

    print("Writing new node jobfiles...")
    write_nodejobfiles(
        distributed_files,
        config['working_dir'])

    # Write out the YAML file describing the processing job
    print(f"Number of files: {len(files)}")
    print(f"Number of pending files: {len(pending_files)}")
    config['count_all_files'] = len(files)
    config['count_job_files'] = len(pending_files)

    print(config)

    # with open(Path(str(config['working_dir']+'/config.yaml')), 'w') as f:
    with open(Path(str('./config.yaml')), 'w') as f:
        yaml.dump(config, f)


if __name__ == "__main__":
    build_jobs(sys.argv[1])
