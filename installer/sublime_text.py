import os
import urllib2
import subprocess
import shutil

from os.path import join as pjoin


from .base import (print_step, print_info,
                   load_json_config, save_json_config,
                   ensure_dirpath_created)

CONFIG_DIRPATH = pjoin(os.environ['HOME'], '.config', 'sublime-text-2')
INSTALLED_PACKAGES_DIRPATH = pjoin(CONFIG_DIRPATH, 'Installed Packages')
PACKAGES_DIRPATH = pjoin(CONFIG_DIRPATH, 'Packages')
PACKAGES_USER_DIRPATH = pjoin(PACKAGES_DIRPATH, 'User')

PACKAGE_CONTROL_USER_SETTINGS_PATH = pjoin(PACKAGES_USER_DIRPATH,
                                           'Package Control.sublime-settings')


def install_package_control():
    print_step('Installing Package Control')
    pf = 'Package Control.sublime-package'
    ipp = INSTALLED_PACKAGES_DIRPATH
    os.makedirs(ipp) if not os.path.exists(ipp) else None
    urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler()))
    package_url = 'http://sublime.wbond.net/' + pf.replace(' ', '%20')
    url_f = None
    package_path = pjoin(ipp, pf)
    if not os.path.exists(package_path):
        try:
            print_info('Fetching {}'.format(package_url))
            url_f = urllib2.urlopen(package_url)
            with open(package_path, 'wb') as f:
                f.write(url_f.read())
        finally:
            url_f.close() if url_f else None
    else:
        print_info(u'Package Control seems to be installed')

    ensure_dirpath_created(PACKAGES_USER_DIRPATH)
    pc_settings = load_json_config(PACKAGE_CONTROL_USER_SETTINGS_PATH, {})
    pc_settings.setdefault('installed_packages', ['Package Control'])
    save_json_config(PACKAGE_CONTROL_USER_SETTINGS_PATH, pc_settings)


def install_package(package_name, package_repo_url, pc_settings):
    print_info(u'Installing {} Package'.format(package_name))
    working_dir = os.getcwd()
    ensure_dirpath_created(PACKAGES_DIRPATH)
    try:
        if not os.path.exists(pjoin(PACKAGES_DIRPATH, package_name)):
            # package dir does not exists
            os.chdir(PACKAGES_DIRPATH)
            print_info(u'Cloning package repo {}'.format(package_repo_url))
            subprocess.check_output(['git', 'clone',
                                    package_repo_url, package_name])
        else:
            print_info(u'Package {package_name} seems to be installed'.format(
                package_name=package_name))
        pc_settings.setdefault('installed_packages', [])
        if package_name not in pc_settings['installed_packages']:
            pc_settings['installed_packages'].append(package_name)
    finally:
        os.chdir(working_dir)


def install_packages():
    print_step(u'Installing Sublime Text 2 packages')
    pc_settings = load_json_config(PACKAGE_CONTROL_USER_SETTINGS_PATH, {})
    for data in load_json_config('files/sublime-text/packages.json', []):
        install_package(data['name'], data['repository_url'], pc_settings)
    save_json_config(PACKAGE_CONTROL_USER_SETTINGS_PATH, pc_settings)


def copy_config_files():
    print_step(u'Copying Sublime Text 2 config files')
    ensure_dirpath_created(PACKAGES_USER_DIRPATH)
    src_dirname = 'files/sublime-text/config'
    for filename in ['Preferences.sublime-settings',
                     'SublimeLinter.sublime-settings']:
        print_info(u'Copying {}'.format(filename))
        shutil.copyfile(pjoin(src_dirname, filename),
                        pjoin(PACKAGES_USER_DIRPATH, filename))


def configure():
    install_package_control()
    install_packages()
    copy_config_files()
