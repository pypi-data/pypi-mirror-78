"""Console script for testtool."""
import sys
import json
from collections import defaultdict
import os
import re
import time
import base64
import hmac
import hashlib
import random
from os import environ
import subprocess
import logging

import requests
import arrow
import regobj
import parse
import pandas as pd
import click
from requests.auth import AuthBase
from agtest import errors_enum


def rec_dd():
    return defaultdict(rec_dd)


def get_installed_plugins(plugin_dir=r'C:\ProgramData\AGCO Corporation\EDT\Plug-Ins'):
    installed_plugins = defaultdict(list)
    for dir_name, sub_dir_list, file_list in os.walk(plugin_dir):
        if 'plugin.xml' in file_list:
            dir_split = dir_name.split('\\')
            plugin = dir_split[-2].upper()
            version = dir_split[-1]
            installed_plugins[plugin].append(version)
    return dict(installed_plugins)


def get_required_plugins(models_dir):
    required_plugins = rec_dd()
    version_pattern = r"[0-9]{3}\.[0-9]{3}_[0-9]{4}\.[0-9]{2}\.[0-9]{2}_[0-9]{6}\.xml"

    for dir_name, sub_dir_list, file_list in os.walk(models_dir):
        for f in file_list:
            if re.match(version_pattern, f):
                dir_split = dir_name.split('\\')
                basename = f.replace('.xml', '')
                plugin = dir_split[-1]
                master = dir_split[-3]
                required_plugins[master].update({plugin.upper(): basename})
    return dict(required_plugins)


def compare_plugins(installed_plug, required_plug):
    found_plugins = rec_dd()
    missing_plugins = rec_dd()
    with open('plugin_results.txt', mode='wt') as f:
        for master, plugins in required_plug.items():
            f.write('Master: {}\n'.format(master))
            for plugin, version in plugins.items():
                if version in installed_plug[plugin]:
                    f.write('\t {0:<25} {1:<35} installed\n'.format(plugin, version))
                    found_plugins[master].update({plugin: version})
                else:
                    f.write('\t {0:<25} {1:<35} Not Found!!!!\n'.format(plugin, version))
                    missing_plugins[master].update({plugin: version})
    return missing_plugins, found_plugins


def get_date_x_weeks_from_now(number_of_weeks=4):
    utc = arrow.utcnow()
    x_weeks_from_now = utc.shift(weeks=+number_of_weeks)
    return x_weeks_from_now.isoformat()


def get_reg_client_id():
    try:
        client_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
            'ClientID'].data
    except AttributeError as e:
        click.secho(f'Client ID was not present in registry. Please confirm that you have AGCO update client installed. {e}',
                    fg='red')
    return client_id


def get_reg_voucher():
    try:
        voucher_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data
    except AttributeError as e:
        click.secho(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}', fg='red')
    return voucher_id


def copy2clip(txt):
    cmd = f'echo {txt.strip()}|clip'
    return subprocess.check_call(cmd, shell=True)


def store_to_environmental_variable():
    key = input('Input the variable name that you want to save as an Environmental Variable: ')
    value = input(f'Input the value for {key}: ')
    environ[key] = value
    print(key in environ)


def save_auc_client():
    url = 'https://dl.agco-ats.com/AUC_EDT.exe'
    save_path = os.path.expanduser('~\\Desktop\\AUC_DL.exe')
    try:
        r = requests.get(url, allow_redirects=True)
        try:
            open(save_path, 'wb').write(r.content)
        except:
            print('Unable to download the AUC client')
    except:
        print('The link to download the latest AUC is down')


def execute_command(path_and_command):
    """
    Runs an inputted command. If the command returns a non-zero return code it will fail. This method is not for
    capturing the output
    """
    logging.debug(f'Attempting to execute: {path_and_command}')
    p1 = subprocess.run(path_and_command,
                        shell=True,
                        # check=True,
                        capture_output=True,
                        text=True,
                        )
    standard_out = p1.stdout
    standard_error = p1.stderr
    return_code = str(p1.returncode)
    logging.debug(f'Command: {path_and_command}')
    logging.debug(f'Standard Out: {standard_out}')
    logging.debug(f'Returncode: {return_code}')
    logging.debug(f'Standard Error: {standard_error}')
    if return_code != '0':
        print(f'Command: {path_and_command}')
        print(f'Standard Out: {standard_out}')
        print(f'Returncode: {return_code}')


def run_auc_client():
    execute_command(os.path.expanduser('~\\Desktop\\AUC_DL.exe /S'))


def print_object(obj):
    click.echo_via_pager(json.dumps(obj, sort_keys=True, indent=4))


def get_voucher_type(base_url, mac_id, mac_token, host, voucher):
    pass


# def get_api_plugins(base_url, mac_id, mac_token, host, release_id):

def get_users_dict(base_url, mac_id, mac_token, host):
    """
    /GET /api/v2/Users
    :return: python dict of Users with Name and Email data for each
    """
    uri = f'{base_url}/api/v2/Users'
    payload = {
        "limit": 1000,
    }
    r = requests.get(f'{uri}', auth=MACAuth(mac_id, mac_token, host), params=payload)
    return_dict = json.loads(r.text)
    user_dict = defaultdict(dict)
    for item in return_dict['Entities']:
        user_id = item['UserID']
        name = item['Name']
        username = item['Username']
        email = item['Email']
        user_dict[user_id].update({'name': name, 'username': username, 'email': email})
    user_dict[0].update({'name': 'None', 'username': 'None', 'email': 'None'})
    return user_dict


def get_content_definitions(base_url, mac_id, mac_token, host):
    """
    /GET /api/v2/ContentDefinitions/{contentDefinitionID}
    :return: content definitions which contains the master name and Description
    """
    uri = f'{base_url}/api/v2/ContentDefinitions'
    payload = {
        "limit": 1000,
    }
    r = requests.get(f'{uri}', auth=MACAuth(mac_id, mac_token, host), params=payload)
    returned_definitions = json.loads(r.text)
    content_dict = defaultdict(dict)
    for item in returned_definitions['Entities']:
        content_definition_id = item['ContentDefinitionID']
        name = item['Name']
        typeid = item['TypeID']
        description = item['Description']
        content_dict[content_definition_id].update({'name': name, 'typeid': typeid, 'description': description})
    return content_dict


def get_release_content(base_url, mac_id, mac_token, host, release):
    """
    /GET /api/v2/ContentReleases
    :return: text of all masters in a given release
    """
    uri = f'{base_url}/api/v2/ContentReleases'
    payload = {
        "limit": 1000,
        "releaseID": release,
    }
    r = requests.get(f'{uri}', auth=MACAuth(mac_id, mac_token, host), params=payload)
    returned_content = json.loads(r.text)
    released_content_dict = defaultdict(dict)
    user_dict = get_users_dict(base_url, mac_id, mac_token, host)
    content_dict = get_content_definitions(base_url, mac_id, mac_token, host)
    for item in returned_content['Entities']:
        content_def_id = item["ContentDefinitionID"]
        version = item["Version"]
        # release_id = item["ReleaseID"]
        publisher_id = item["PublisherUserID"]
        updated_date = item["UpdatedDate"]
        # deleted = item["Deleted"]
        test_report_url = item["TestReportUrl"]
        released_content_dict[content_dict[content_def_id]['name']].update({'version': version,
                                                                            'type': content_dict[content_def_id][
                                                                                'typeid'],
                                                                            'publisher_id': publisher_id,
                                                                            'submitter_name': user_dict[publisher_id][
                                                                                'name'],
                                                                            'submitter_email': user_dict[publisher_id][
                                                                                'email'],
                                                                            'updated_date': updated_date,
                                                                            'test_report_url': test_report_url,
                                                                            })
    return released_content_dict


def create_content_table(path, name, content_dict, masters_only):
    """
    Creates a table of content submission
    :return:
    """
    path = f'{path}\\'
    my_df = pd.DataFrame.from_dict(content_dict, orient='index')
    my_df.drop(['publisher_id', ], axis=1, inplace=True)
    updated_df = my_df.rename(columns={'submitter_name': 'Submitter',
                                       'submitter_email': 'Email',
                                       'test_report_url': 'Report_Download',
                                       'updated_date': 'Submitted_Date',
                                       'type': 'Submission_Type',
                                       'version': 'Version',
                                       })
    updated_df.index.name = 'Submission'
    sorted_df = updated_df.sort_values(by='Submitter')
    if masters_only:
        sorted_df = sorted_df.loc[sorted_df['Submission_Type'] == 1]
    try:
        sorted_df.to_excel(f'{path}{name}.xlsx', header=True)
    except PermissionError:
        print('Unable to create an excel file with that name. It is possible that you have another spread sheet'
              ' open with that same name')


@click.group()
def main(args=None):
    """Command-line tool for common testing tasks"""


@main.command()
@click.option('--location', '-l', default='prod', type=click.Choice(["my_docs", 'prod', 'test']), help="Choose where it"
                                                                                                       " looks for "
                                                                                                       "masters")
@click.option('--report', '-r', required=True, type=click.Choice(['installed', 'required', 'missing', 'full']))
def plugins(location, report):
    """Console script for plugins."""
    if location == 'my_docs':
        directory = os.path.expanduser(r'~\Documents\AGCO Corporation\EDT\Models')
    elif location == 'prod' or location != 'test':
        directory = r'C:\ProgramData\AGCO Corporation\EDT\Models'
    else:
        directory = r'C:\ProgramData\AGCO Corporation\EDT Test\Models'
    installed_plugins = get_installed_plugins()
    required_plugins = get_required_plugins(directory)
    missing_plugins, found_plugins = compare_plugins(installed_plugins, required_plugins)
    if report in ['installed', 'full']:
        click.secho("Installed Plugins:\n", bold=True)
        print_object(installed_plugins)
    if report in ['required', 'full']:
        click.secho("Required Plugins:\n", bold=True)
        print_object(required_plugins)
    if report in ['missing', 'full']:
        click.secho("Missing Plugins:\n", bold=True, fg='red')
        print_object(missing_plugins)
    if report == 'full':
        click.secho("Found Plugins:\n", bold=True)
        print_object(found_plugins)
    if missing_plugins:
        return -1
    else:
        return 0


@main.command()
@click.option('--item', '-i', default='client', type=click.Choice(['client', 'voucher', 'masters', 'errors', 'all']))
def registry(item):
    """Returns the following reg values: AUC client, EDT voucher, installed masters, Errors, and all EDT values"""
    if item == 'client':
        try:
            return_value = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
                'ClientID'].data
            copy2clip(return_value)
            click.secho(f'Client_id {return_value} was copied to the clipboard', fg="green")
        except AttributeError as e:
            click.secho("Client Id was not present in registry. Please confirm that you have AUC installed", fg='red')

    if item == 'voucher':
        try:
            return_value = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data
            copy2clip(return_value)
            click.secho(f'Client_id {return_value} was copied to the clipboard', fg="green")
        except AttributeError as e:
            click.secho("Voucher was not present in registry. Please confirm that EDT has been vouchered", fg='red')

    if item == 'masters':
        masters_versions = {}
        try:
            edt_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT.values()
            for i in edt_values:
                if "_Version" in i.name and 'UPDATE_' in i.name:
                    p = parse.parse("Update_{}_Version", i.name)
                    master = p[0]
                    masters_versions.update({master: i.data})
            print_object(masters_versions)
        except AttributeError as e:
            click.secho('EDT does not appear to be installed. Please confirm that EDT is installed', fg='red')
        return masters_versions

    if item == 'errors':
        edt_errors = {}
        edt_reg_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT.values()
        for i in edt_reg_values:
            entry = i.name
            data = i.data
            if ('_err' in entry.lower()) or ('Error' in entry):
                edt_errors.update({i.name: i.data})
        for key, value in edt_errors.items():
            num_val = int(value)
            if num_val:
                try:
                    click.secho(f'{key:.<40}{value:<15}{errors_enum.ErrorCode(num_val).name}', fg='red')
                except ValueError:
                    click.secho(f'{key:.<40}{value:<15}{num_val} not defined', fg='red')
            else:
                click.secho(f'{key:.<40}{value:<15}', fg='green')
        return edt_errors

    if item == 'all':
        edt_values = {}
        agco_update = {}
        try:
            edt_reg_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT.values()
            for i in edt_reg_values:
                edt_values.update({i.name: i.data})
            for key, value in edt_values.items():
                if ('_err' in key.lower()) or ('Error' in key):
                    if int(value):
                        click.secho(f'{key:.<40}{value:<15}', fg='red', bg='black')
                    else:
                        click.secho(f'{key:.<40}{value:<15}', fg='green', bg='black')
                else:
                    click.secho(f'{key:.<40}{value:<15}', fg='blue', bg='black')
        except AttributeError as e:
            click.secho('EDT does not appear to be installed. Please confirm that EDT is installed', fg='red')
        try:
            update_reg_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(
                r'AGCO Update').values()
            for i in update_reg_values:
                agco_update.update({i.name: i.data})
            for key, value in agco_update.items():
                click.secho(f'{key:.<40}{value:<15}', fg='yellow', bg='black')
        except AttributeError as e:
            click.secho('AGCO update client does not appear to be installed. Please install AUC.', fg='red')
        return edt_values


@main.command()
@click.option('--installer', '-i', default='auc', type=click.Choice(['auc', 'choco']))
def install(installer):
    """Allows for install of common testing tools"""
    if installer == 'auc':
        save_auc_client()
        # run_auc_client()


@main.group()
@click.option('--env', '-e', default='prod', type=click.Choice(['prod', 'test', 'dev']), help='Choose the environment '
                                                                                              'that the API calls will'
                                                                                              ' be directed')
@click.pass_context
def api(ctx, env):
    """API commands to assist with testing"""
    if env == 'dev':
        HOST = 'edtsystems-webtest-dev.azurewebsites.net'
    elif env == 'prod':
        HOST = "secure.agco-ats.com"
    elif env == 'test':
        HOST = 'edtsystems-webtest.azurewebsites.net'
    BASE_URL = f'https://{HOST}'
    ctx.ensure_object(dict)
    ctx.obj['HOST'] = HOST
    ctx.obj['BASE_URL'] = BASE_URL
    ctx.obj['MAC_ID'] = os.environ.get('MAC_ID')
    ctx.obj['MAC_TOKEN'] = os.environ.get('MAC_TOKEN')


@api.group()
@click.pass_context
def voucher(ctx):
    """
    Performs api calls for common voucher actions such as extend and create
    """
    pass


@voucher.command()
@click.option('--weeks_to_extend', '-wte', default=4, help='Allows the user to extend a temporary voucher a custom'
                                                           'number of weeks')
@click.pass_context
def extend(ctx, weeks_to_extend):
    """Extends temporary vouchers"""
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    voucher = get_reg_voucher()
    expir_date = get_date_x_weeks_from_now(weeks_to_extend)
    uri = f'{base_url}/api/v2/Vouchers'
    payload = {"VoucherCode": voucher,
               "Type": "Temporary",
               "DealerCode": "NA0001",
               "LicenseTo": "fraserda",
               "Purpose": "Testing",
               "Email": "darrin.fraser@agcocorp.com",
               "Punched": False,
               "ExpirationDate": expir_date,
               }
    r = requests.put(f'{uri}', auth=MACAuth(mac_id, mac_token, host), data=payload)
    return r.text


@voucher.command()
@click.pass_context
@click.option('--duration', '-d', default=8, help='Specify the number of weeks the temporary voucher lasts')
def create(ctx, duration):
    """Creates temporary voucher"""
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    expir_date = get_date_x_weeks_from_now(duration)
    uri = f'{base_url}/api/v2/Vouchers'
    payload = {
        "Type": "Temporary",
        "DealerCode": "NA0001",
        "LicenseTo": "Darrin Fraser",
        "Purpose": "Testing",
        "Email": "darrin.fraser@agcocorp.com",
        "ExpirationDate": expir_date,
    }
    r = requests.post(f'{uri}', auth=MACAuth(mac_id, mac_token, host), data=payload)
    voucher_text = (r.text).strip('"')
    copy2clip(voucher_text)
    click.secho(f'Voucher: {voucher_text} copied to clipboard')
    return voucher_text


@api.group()
@click.pass_context
def release(ctx):
    """
    Performs api calls for common release actions
    """
    pass


@release.command(name='plugins')
@click.argument('release_id', type=click.INT, required=True)
@click.pass_context
def api_plugins(ctx, release_id):
    """Parses the plugins for a given release"""
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    api_plugins_dict = defaultdict(list)
    uri = f'{base_url}/api/v2/ContentSubmissions'
    payload = {
        "contentDefinitionID": 1234,
        "includeAttributes": 'IncludedPlugIn',
        "releaseID": release_id,
    }
    r = requests.get(f'{uri}', auth=MACAuth(mac_id, mac_token, host), params=payload)
    plugins_response = r.json()
    for item in plugins_response['Entities'][0]['Attributes']:
        unedited_item = item['Value']
        plugin, _sep, plug_value = unedited_item.partition('::')
        api_plugins_dict[plugin.upper()].append(plug_value)
    print_object(api_plugins_dict)
    return api_plugins_dict


@release.command(name='list')
@click.pass_context
def get_list(ctx):
    """Retrieves release ids identified by release name"""
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    uri = f'{base_url}/api/v2/Releases'
    payload = {
        "limit": 1000,
        "offset": 30,
    }
    r = requests.get(f'{uri}', auth=MACAuth(mac_id, mac_token, host), params=payload)
    releases = json.loads(r.text)
    release_dict = defaultdict(dict)
    for item in releases['Entities']:
        release_id = item["ReleaseID"]
        release_number = item["ReleaseNumber"]
        build_date = item['BuildDate']
        release_date = item["ReleaseDate"]
        visible = item["Visible"]
        release_dict[release_id].update({'release_name': release_number,
                                         'build_date': build_date,
                                         'release_date': release_date,
                                         'visible': visible,
                                         })
    for key, value in release_dict.items():
        rel_name = value['release_name']
        click.secho(f'{key:2} : {rel_name}')
    return release_dict


@release.command()
@click.argument('release_id', type=click.INT, required=True)
@click.option('--create_table', '-ct', is_flag=True, help='Creates .xlsx spreadsheet of output of release info')
@click.option('--path', '-p', default=os.path.expanduser('~\\Documents\\reports\\'), help='Allows user to save to '
                                                                                          'alternate location')
@click.option('--name', '-n', default='Released_Content', help='Allows user to save file with alternate name')
@click.option('--masters_only', '-mo', is_flag=True, help='Used in conjunction with create table.')
@click.pass_context
def content(ctx, release_id, create_table, path, name, masters_only):
    """
    Text of all released content in a given release with
    """
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    released_content_dict = get_release_content(base_url, mac_id, mac_token, host, release_id)
    updated_name = f'{release_id}_{name}'
    if create_table:
        create_content_table(path, updated_name, released_content_dict, masters_only)
    else:
        print_object(released_content_dict)

    return released_content_dict


@release.command()
@click.argument('current_id', type=click.INT, required=True)
@click.argument('previous_id', type=click.INT, required=True)
@click.option('--create_table', '-ct', is_flag=True, help='Creates .xlsx spreadsheet of output of release info')
@click.option('--path', '-p', default=os.path.expanduser('~\\Documents\\reports\\'), help='Allows user to save to '
                                                                                          'alternate location')
@click.option('--name', '-n', default='Released_Content', help='Allows user to save file with alternate name')
@click.option('--masters_only', '-mo', is_flag=True, help='Used in conjunction with create table.')
@click.pass_context
def compare(ctx, current_id, previous_id, create_table, path, name, masters_only):
    """
    Text of added or changed items in a release. Requires the current release ID of the current as well as the previous
    release ID
    """
    host = ctx.obj.get('HOST')
    base_url = ctx.obj.get('BASE_URL')
    mac_id = ctx.obj.get('MAC_ID')
    mac_token = ctx.obj.get('MAC_TOKEN')
    updated_content_dict = defaultdict(dict)
    current_content_dict = get_release_content(base_url, mac_id, mac_token, host, current_id)
    current_name = f'{current_id}_vs_{previous_id}_{name}'
    previous_content_dict = get_release_content(base_url, mac_id, mac_token, host, previous_id)
    for key, value in current_content_dict.items():
        if key in previous_content_dict:
            if value['updated_date'] == previous_content_dict[key]['updated_date']:
                continue
            else:
                updated_content_dict[key].update(value)
        else:
            updated_content_dict[key].update(value)

    if create_table:
        create_content_table(path, current_name, updated_content_dict, masters_only)
    else:
        print_object(updated_content_dict)

    return updated_content_dict


class MACAuth(AuthBase):
    """
    Attaches HTTP Authentication to the given Request object, and formats the header for every API call used
    """

    def __init__(self, mac_id, mac_token, host):
        # setup any auth-related data here
        self.mac_id = mac_id
        self.mac_token = mac_token
        self.host = host

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.generate_header(r.method, r.path_url)
        return r

    def get_hmac(self, method, uri, milliseconds, nonce):
        http_version = 'HTTP/1.1'
        # host = HOST
        request_string = f'{method} {uri} {http_version}\n{self.host}\n{milliseconds}\n{nonce}\n'
        return base64.b64encode(
            hmac.new(self.mac_token.lower().encode(), request_string.encode(), hashlib.sha256).digest()).decode()

    def generate_header(self, method, uri):
        milliseconds = str(int(time.time() * 1000))
        nonce = ''.join([str(random.randint(0, 9)) for i in range(8)])
        formatted_hmac = self.get_hmac(method, uri, milliseconds, nonce)
        return f'MAC kid={self.mac_id},ts={milliseconds},nonce={nonce},mac=\"{formatted_hmac}\"'


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
