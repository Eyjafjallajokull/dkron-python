import click
import json
from .api import DkronApi, DkronApiException
from pprint import pprint


_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


api = DkronApi()


@click.group(context_settings=_CONTEXT_SETTINGS)
def cli():
    '''
    Command line interface client for dkron resources
    '''
    pass


@cli.group()
def get():
    '''
    Fetch information about resources
    '''
    pass


@get.command(name='jobs')
def get_jobs():
    '''
    Fetch all jobs
    '''
    try:
        results = api.get_jobs()
    except DkronApiException as ex:
        print('Error while fetching %s: %s' % (job_name, str(ex)))
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
    except DkronApiException as ex:
        print('Error while fetching %s: %s' % (job_name, str(ex)))
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
            except DkronApiException as ex:
                print('Error while applying %s: %s' % (file_path, str(ex)))
                exit(1)
            print('Processed: %s' % file_path)


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
    except DkronApiException as ex:
        print('Error while deleteing %s: %s' % (job_name, str(ex)))
        exit(1)
