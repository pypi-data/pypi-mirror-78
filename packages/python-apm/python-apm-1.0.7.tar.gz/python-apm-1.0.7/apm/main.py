#!/usr/bin/python
# coding=utf-8

import click
import os
import yaml
import uuid

# TODO: add config
#import src.config

# Config
temp_dir = '/tmp'
roles_folder = './remote_roles'
location = os.getcwd()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name', default='')
def install(name):
    '''
    install dependency from meta/main.yml in local folder
    '''
    # check ansible-galaxy exist
    if os.system("ansible-galaxy --version > /dev/null ") != 0:
        click.echo(click.style('✘ Ansible-galaxy not found!\nPlease install ansible on youre host or, \nyou can manualy set path to ansible-galaxy bin,\nuse GALAXY_PATH env, or galaxy_path config options',
          fg='red'), err=True)
    click.echo(click.style(
        '✓ Ansible-galaxy bin found', fg='green'))

    # check meta/main.yml exist
    if not os.path.exists('%s/meta/main.yml' % location):
        click.echo(click.style(
            '✘ file meta/main.yml not found', fg='red'), err=True)
        exit(1)
    # read data from meta/main.yml
    with open("%s/meta/main.yml" % location, 'r') as stream:
        try:
            skip_deps = False
            skip_opt_deps = False
            data = yaml.safe_load(stream)
            if data is None:
                click.echo(click.style(
                    '? File meta/main.yml is empty\nSkipping install deps.', fg='yellow'))
                exit(0)

            if not 'dependencies' in data or len(data['dependencies']) == 0:
                click.echo(click.style(
                    '? Dependencies list is empty. Skipping ...', fg='yellow'))
                skip_deps = True

            if not 'optional_dependencies' in data['galaxy_info'] or len(data['galaxy_info']['optional_dependencies']) == 0:
                click.echo(click.style(
                    '? Optional dependencies list is empty. Skipping ...', fg='yellow'))
                skip_opt_deps = True

            if skip_deps and skip_opt_deps:
                click.echo(click.style(
                    '? No deps for install...', fg='yellow'))
                exit(0)

            if skip_deps:
                reqs_data = {
                    'roles': data['galaxy_info']['optional_dependencies']
                }

            if skip_opt_deps:
                reqs_data = {
                    'roles': data['dependencies']
                }

            if not skip_opt_deps and not skip_deps:
                roles = data['galaxy_info']['optional_dependencies'] + \
                    data['dependencies']
                reqs_data = {
                    'roles': roles
                }

            click.echo(click.style(
                '✓ File meta/main.yml is valid', fg='green'))

            # Generate file reqs.yml
            uuid_var = str(uuid.uuid4())
            path = "%s/ansible-%s.yml" % (temp_dir, uuid_var)


            # write data in install yaml file
            with open(path, 'w') as yamlfile:
                yaml.dump(reqs_data, yamlfile, default_flow_style=False)
            click.echo(click.style(
                '✓ The file with dependencies is ready\nInstalling to %s folder ...' % roles_folder, fg='green'))

            # Install from file reqs.txt
            if os.path.exists(path):
                install_res = os.system('ansible-galaxy install -r %s -p %s --force' %
                          (path, roles_folder))
                if install_res == 0:
                    click.echo(click.style(
                        '✓ All dependencies were successfully installed\n\nHappy ansibling :)', fg='green'))
                    os.remove(path)
                    exit(0)
                if install_res != 0:
                    click.echo(click.style(
                        '✘ An error occurred while installing dependencies', fg='red'), err=True)
                    os.remove(path)
                    exit(1)

        except yaml.YAMLError as exc:
            click.echo(click.style(exc, fg='red'), err=True)


if __name__ == '__main__':
    cli()
