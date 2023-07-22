import logging
import subprocess
import sys,os
import time
import platform

from tqdm import tqdm
import pandas as pd
import shutil
from config_py import config_global
import xml.etree.ElementTree as ET

pd.set_option('display.max_columns', None)
sys.path.append("..")
sys.path.append("")
sys.path.append('/home/18mia2/scitools/bin/linux64/Python')

from platform import python_version
import understand


def shellCommand(command_str):
    '''Execute a shell command and capture its output and error.'''
    cmd_str = " ".join(command_str)
    cmd = subprocess.Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_out, cmd_err = cmd.communicate()
    return cmd_out, cmd_err

def get_commit_list(project):
    '''Get the list of all commits from the sequence file.'''
    seq_path = f'/home/18mia2/clone_genealogies_py/raw_data/{project}_sequence_all.txt'
    commit_list = []
    with open(seq_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Remove the newline character
            commit = line.strip()
            commit_list.append(commit)
    return commit_list

def create_df_metrics():
    '''Create the df that will contain the extracted und metrics'''
    metric_columns = config_global.METRIC_COLUMNS
    cols = ['commit_id', 'clone_signiture']
    cols.extend(metric_columns)
    metrics_all_df = pd.DataFrame(columns=cols)

def load_project_genealogy(project):
    '''Load project genealogy data from a CSV file and return it as a pandas DataFrame.'''
    gen_path = f'/home/18mia2/clone_genealogies_py/output_data/nicad/{project}_genealogies_d_all.csv'
    project_gen = pd.read_csv(gen_path)
    print(f'Genealogy size {project_gen.shape}  {project_gen.columns}')
    return project_gen

def extract_unique_files_from_xml_clone_result(commit_id):
    
    '''Parse the xml of each clone snapshot and extract the unique list of file for every commit'''
    xml_file_path = f'/home/18mia2/clone_genealogies_py/clone_results/nicad/{project}/{commit_id}.xml'

    unique_files = set()

    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    for source_tag in root.findall(".//source"):
        file_value = source_tag.get("file")
        # Clean the file value by removing the "../" prefix
        cleaned_file = file_value.replace(f"../src_code/{project}/", "")
        unique_files.add(cleaned_file)

    return list(unique_files)

def get_files_by_commit(commit_id, genealogy_df):
    '''Extract the files involved in clone pairs for a specific commit ID.'''
    groups_by_commit = genealogy_df.loc[genealogy_df['start_commit'] == commit_id]['clone_pair']

    files_by_commit = set()
    for group in groups_by_commit:
        for clone in group.split("+"):
            clone_path = clone.split("^")[0]
            if len(clone):
                files_by_commit.add(clone_path)
    return files_by_commit

def build_und_project_db(commit_id, metric_columns, project, clone_files):
    '''Build an Understand project database for a specific commit using Understand CLI.'''
   
    # run understand cli to construct the project understand db
    und_commit_db = os.path.join(config_global.DATA_PATH, 'udb', "%s" %project, '%s.und' % commit_id)

    # create und db
    if not os.path.exists(und_commit_db):
        cmd_create_und_db = ['und', '-db', und_commit_db, 'create', '-languages', 'Python']
        shellCommand(cmd_create_und_db)

    # append the results of all the files of the current commit to the db
    for clone_file in clone_files:
        cmd_add_file = ['und', 'add', clone_file, und_commit_db]
        shellCommand(cmd_add_file)

        # settings and analyze udb to retrieve functions with parameters
        cmd_setting_analyze = ['und', '-db', und_commit_db, 'settings', '-metrics']
        cmd_setting_analyze.extend(metric_columns)
        cmd_setting_analyze.extend(['-MetricShowFunctionParameterTypes', 'on'])
        cmd_setting_analyze.extend(['-MetricFileNameDisplayMode', 'RelativePath'])
        cmd_setting_analyze.extend(['-MetricDeclaredInFileDisplayMode', 'RelativePath'])
        cmd_setting_analyze.extend(['-MetricShowDeclaredInFile', 'on'])
        cmd_setting_analyze.extend(['-MetricAddUniqueNameColumn', 'off'])
        cmd_setting_analyze.extend(['-ReportDisplayParameters', 'on'])
        cmd_setting_analyze.extend(['-ReportFileNameDisplayMode', 'RelativePath'])
        cmd_setting_analyze.extend(['analyze', 'metrics'])
        shellCommand(cmd_setting_analyze)


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print('Please input [project]!')
    else:
        project = sys.argv[1]
        print(f'Processing project {project}')

        project_repo = config_global.REPO_PATH + project

        # changing the current report to the project repository to do the checkout
        current_dir = os.getcwd()
        os.chdir(project_repo)
    
        und_metric_df = create_df_metrics()
        
        # traverse all the commits sequence for the project
        commit_list = get_commit_list(project)
    
        # for commit_id in tqdm(gen_project['start_commit'].unique().tolist()):
        for commit_id in tqdm(commit_list):
            # check out project repo at a specified commit to update the source repo
            cmd_checkout = ['git', 'checkout', '-f', commit_id]  # 'git checkout %s' % commit_id
            shellCommand(cmd_checkout)  # optimize: can be checked out using pydriller.Git().checkout(hash)

            # if checkout already visited, skip the checkout
            metrics_path = f'{config_global.UDB_PATH}/{project}/{commit_id}.csv'
            if os.path.exists(metrics_path):
                continue

            cmd_checkout = ['git', 'checkout', '-f', commit_id]
            shellCommand(cmd_checkout)

            # double check the usage of this code
            curr_commit_id = os.popen('git rev-parse --short HEAD').read()
            while curr_commit_id[:len(commit_id)] != commit_id:
                print(curr_commit_id[:len(commit_id)], commit_id)
                time.sleep(5)
                sys.exit(-1)
            
            clone_files = extract_unique_files_from_xml_clone_result(commit_id)
            
            # verify if the clone metrics file is created already if not create it in write mode
            files_to_analyze_path = f'{config_global.UDB_PATH}/{project}/{commit_id}_clone_files.txt'
            if not os.path.exists(files_to_analyze_path):
                with open(files_to_analyze_path, 'w') as fp:
                    fp.write("\n".join(clone_files))

            # extract the metric and build the und db for every project
            build_und_project_db(commit_id, config_global.METRIC_COLUMNS, project, clone_files)

        os.chdir(current_dir)