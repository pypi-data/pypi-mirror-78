from __future__ import print_function
from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import os


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # note: pip install suppresses all user stdout/stderr output unless -v/--verbose option is specified. 
        print("We are running in the postInstallCommand")
        cwd = os.path.dirname(os.path.realpath(__file__))
        check_call("bash %s/ha_tools.sh" % cwd, shell=True)
        install.run(self)
        print("NOTE: 'source ~/.bashrc' is necessary for HA commands to be accessible.")


project_name = 'csr_ha'
project_ver = '2.0.1'

setup(
    name=project_name,
    packages=['csr_ha'],  # this must be the same as the name above
    version=project_ver,
    description='High availability of CSR 1000v routers in cloud',
    author='Cisco Systems Inc.',
    author_email='csr-cloud-dev@cisco.com',
    scripts=['csr_ha/client_api/node_event.py',
             'csr_ha/client_api/clear_params.py',
             'csr_ha/client_api/create_node.py',
             'csr_ha/client_api/set_params.py',
             'csr_ha/client_api/delete_node.py',
             'csr_ha/client_api/ha_api.py',
             'csr_ha/client_api/show_node.py',
             'csr_ha/client_api/revert_nodes.sh',
             'ha_tools.sh'
            ],
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-cloud/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-cloud/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'ha', 'high availability', 'csr1000v', 'csr', 'guestshell'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    license="MIT",
    include_package_data=True,
    install_requires=[
        'ipaddress==1.0.23',
        'future==0.18.2',
        'cryptography==2.9.2'
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)
