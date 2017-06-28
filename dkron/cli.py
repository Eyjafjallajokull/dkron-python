import click
import json
import os
from .api import Dkron, DkronException
from pprint import pprint


_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
_DKRON_ENV_NAME_HOSTS = 'DKRON_HOSTS'
api = None


@click.group(context_settings=_CONTEXT_SETTINGS)
@click.option('--hosts', help='Dkron instance URLs, separated with commans', envvar=_DKRON_ENV_NAME_HOSTS)
def cli(hosts):
    '''
    Command line interface client for Dkron
    '''
    global api
    if not hosts:
        print('You must provide %s environment variable OR --hosts option' % _DKRON_ENV_NAME_HOSTS)
        print('Check docs: https://github.com/Eyjafjallajokull/dkron-python#cli-usage')
        exit(1)
    api = Dkron(hosts.split(','))


@cli.group()
def get():
    '''
    Fetch information about resources
    '''
    pass


@get.command(name='status')
def get_status():
    '''
    Get system status
    '''
    try:
        results = api.get_status()
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@get.command(name='leader')
def get_leader():
    '''
    Get system leader
    '''
    try:
        results = api.get_leader()
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@get.command(name='members')
def get_members():
    '''
    Get system members
    '''
    try:
        results = api.get_members()
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@get.command(name='jobs')
def get_jobs():
    '''
    Fetch all jobs
    '''
    try:
        results = api.get_jobs()
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@get.command(name='job')
@click.argument('job_name')
def get_job(job_name):
    '''
    Fetch specific job
    '''
    try:
        results = api.get_job(job_name)
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@get.command(name='executions')
@click.argument('job_name')
def get_executions(job_name):
    '''
    Get system executions
    '''
    try:
        results = api.get_executions(job_name)
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)
    print(json.dumps(results))


@cli.group()
def apply():
    '''
    Create or update resources
    '''
    pass


@apply.command(name='job')
@click.argument('json_file_path', nargs=-1)
def apply_job(json_file_path):
    '''
    Create or update job(s)
    '''
    for file_path in json_file_path:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            try:
                api.apply_job(data)
            except DkronException as ex:
                print('Error while applying %s: %s' % (file_path, str(ex)))
                exit(1)
            print('Processed: %s' % file_path)


@cli.command(name='run')
@click.argument('job_name')
def run_job(job_name):
    '''
    Execute job on demand
    '''
    try:
        api.run_job(job_name)
    except DkronException as ex:
        print('Error while executing: %s' % str(ex))
        exit(1)


@cli.command(name='export')
@click.argument('backup_dir')
def export(backup_dir):
    '''
    Exports all jobs to json files
    '''
    try:
        jobs = api.get_jobs()
        for job in jobs:
            filename = os.path.join(backup_dir, job['name'] + '.json')
            json.dump(job, open(filename, mode='w'), indent=2)
    except DkronException as ex:
        print('Error while fetching: %s' % str(ex))
        exit(1)


@cli.group()
def delete():
    '''
    Delete resources
    '''
    pass


@delete.command(name='job')
@click.argument('job_name')
def delete_job(job_name):
    '''
    Delete job
    '''
    try:
        api.delete_job(job_name)
    except DkronException as ex:
        print('Error while deleteing: %s' % str(ex))
        exit(1)
