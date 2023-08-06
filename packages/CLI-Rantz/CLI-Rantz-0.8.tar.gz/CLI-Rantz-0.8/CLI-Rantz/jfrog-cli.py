
# CLI-Rantz POC for JFrog Tech review - created by Ran Tzur.
# !/usr/bin/env python3
import requests as req
from requests.auth import HTTPBasicAuth
import sys
from pprint import pprint
import click
import json


def report_failure(res):
    try:
        error_message = res['errors'][0]['message']
        print(f"Request returned the following error: {error_message}")
    except Exception as e:
        print("Request failed, error message is " + e)
        raise SystemError()


def get_instance_id(username, password, server_name):
    url = build_url(server_name, 'api/system/service_id')
    res = req.get(url=url, auth=HTTPBasicAuth(username, password))
    if res.status_code == 200:
        return res.text


def connect_user(username, password,server_name):
    #  Taking the default values of the access token to keep it simple.
    #  Setting the token as admin token for full access of requested endpoints.
    #  Token is created by default for 1 hour.
    create_access_token = build_url(server_name, 'api/security/token')
    service_id = get_instance_id(username, password, server_name)
    data = {"username": username,
            'scope': f"{service_id}:admin api:*"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = req.post(url=create_access_token, data=data, headers=headers, auth=HTTPBasicAuth(username,password))
    if res.status_code == 200:
        access_token = res.json()['access_token']
        return access_token
    else:
        report_failure(res.json())
        exit_cli()


def exit_cli():
    sys.exit()


def build_url(server_name, api_path):
    try:
        url = f"https://{server_name}.jfrog.io/artifactory/{api_path}"
        #  This check for a valid server_name, will throw an invalid exception if server_name is not SaaS
        req.get(url=f"https://{server_name}.jfrog.io/artifactory/system/ping")
        return url
    except Exception as e:
        print("Failed to parse URL, please make sure you are using your SaaS username.\n"
              "For examples, see GitHub Readme.")
        raise SystemExit()


# CLI-Rantz #
@click.group()
def cli():
    pass


@cli.command(name= "version", help="Returns the system version. (Requires artifactory credentials)")
@click.option('-username', required=True, prompt=True)
@click.option('-password', required=True, prompt=True, hide_input=True)
@click.option('-server-name', required=True, prompt=True, help="Artifactory server name")
def get_system_version(username,password,server_name):
    auth_token = connect_user(username, password, server_name)
    system_version_url = build_url(server_name, 'api/system/version')
    res = req.get(url=system_version_url, auth=HTTPBasicAuth(username, auth_token))
    if res.status_code == 200:
        output = res.json()['version']
        print(f"\nSystem version: {output}\n")
    else:
        report_failure(res.json())


@cli.command(name="ping", help="Returns the system health.")
@click.option('-server-name', required=True, prompt=True, help="Artifactory server name")
def system_ping(server_name):
    system_ping_url = build_url(server_name, 'api/system/ping')
    res = req.get(url=system_ping_url)
    print(f"System ping returned: {res.text}")


@cli.command(name="storage-info", help="Returns the storage information as a JSON value. (Requires artifactory credentials)")
@click.option('-username', required=True, prompt=True, help="Artifactory user name")
@click.option('-password', required=True, prompt=True, hide_input=True, help="Artifactory password")
@click.option('-server-name', required=True, prompt=True, help="Artifactory server name")
def get_storage_information(username, password, server_name):
    auth_token = connect_user(username, password, server_name)
    url = build_url(server_name, 'api/storageinf')
    res = req.get(url=url, auth=HTTPBasicAuth(username, auth_token))
    if res.status_code == 200:
        print("\nSystem Storage Information: \n-------------------------------\n")
        pprint(res.json())
    else:
        report_failure(res.json())


@cli.command(name="create-user", help="Creates a new user. (requires artifactory credentials)")
@click.option('-username', required=True, prompt=True, help="Artifactory user name")
@click.option('-password', required=True, prompt=True, hide_input=True, help="Artifactory password")
@click.option('-name', required=False, help="New user username (Optional)")
@click.option('-email', required=True, help="New user email")
@click.option('-new-pass', required=True, help="New user password")
@click.option('-is-admin', required=False, help="Is user admin? (Default: false)")
@click.option('-profile-updatable', required=False, help="Is profile updatable? (Default: true)")
@click.option('-disable-ui', required=False, help="Disable UI access (Default: true)")
@click.option('-password-protected', required=False, help="Internal password protected (Default: false)")
@click.option('-groups', required=False, help="Groups to match the user with (Optional)")
@click.option('-watch-manager', required=False, help="Set as watch manager (Default: false)")
@click.option('-policy-manager', required=False, help="Set as policy manager (Default: false)")
@click.option('-server-name', required=True, prompt=True, help="Artifactory server name")
def create_user(username, password,name,email,
                new_pass, is_admin, profile_updatable,
                disable_ui, password_protected, groups,
                watch_manager, policy_manager, server_name):
    auth_token = connect_user(username, password, server_name)
    header = {'Content-Type': 'application/json'}
    url = build_url(server_name, f"api/security/users/{name}")
    data = {'name': name,
            'email': email,
            'password': new_pass,
            'admin': is_admin,
            'profileUpdatable': profile_updatable,
            'disableUIAccess': disable_ui,
            'internalPasswordDisabled': password_protected,
            'groups': groups,
            'watchManager': watch_manager,
            'policyManager': policy_manager}
    res = req.put(url=url, data=json.dumps(data),headers=header, auth=HTTPBasicAuth(username, auth_token))
    if res.status_code == 201:
        print(f"User {name} was created successfully")
    else:
        report_failure(res.json())


@cli.command(name="delete-user", help="Deletes a user. (requires artifactory credentials)")
@click.option('-username', required=True, prompt=True, help="Artifactory user name")
@click.option('-password', required=True, prompt=True, hide_input=True, help="Artifactory password")
@click.option('-user-to-delete', required=True, help="Username of the user to delete")
@click.option('-server-name', required=True, prompt=True, help="Artifactory server name")
def delete_user(username, password, user_to_delete,server_name):
    url = f"https://{server_name}.jfrog.io/artifactory/api/security/users/{user_to_delete}"
    auth_token = connect_user(username, password)
    res = req.delete(url=url, auth=HTTPBasicAuth(username, auth_token))
    if res.status_code == 200:
        print(f"User {user_to_delete} was deleted successfully")
    else:
        report_failure(res.json())


if __name__ == '__main__':
    cli()
