# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_credential_process']
install_requires = \
['boto3>=1.11,<2.0',
 'click>=7.1,<8.0',
 'keyring>=21.3,<22.0',
 'pynentry>=0.1.3,<0.2.0',
 'yubikey-manager==3.1.1']

entry_points = \
{'console_scripts': ['aws-credential-process = aws_credential_process:main']}

setup_kwargs = {
    'name': 'aws-credential-process',
    'version': '0.6.0',
    'description': 'AWS Credential Process',
    'long_description': '# Description\nScript to use as `credential_process` for the AWS CLI (including boto3), it caches your MFA session in a keyring and can use a Yubi key to authenticate.\n\n# Installing\nYou can install aws-credential-process using pip:\n```bash\npip install aws_credential_process\n```\n\nI recommend to install aws-credential-process in a virtualenv:\n```bash\nvirtualenv ~/venv/aws_credential_process\n~/venv/aws_credential_process/bin/pip install aws_credential_process\n```\n\nAfter the above commands you should be able to run `~/venv/aws_credential_process/bin/aws-credential-process`\n\n# Usage\n\nYou can use the following arguments to start aws-credential-process:\n```\nUsage: aws-credential-process [OPTIONS]\n\n  Get output suitable for aws credential process\n\nOptions:\n  --access-key-id TEXT\n  --secret-access-key TEXT\n  --mfa-oath-slot TEXT\n  --mfa-serial-number TEXT        [required]\n  --mfa-session-duration INTEGER\n  --assume-session-duration INTEGER\n  --assume-role-arn TEXT\n  --force-renew\n  --credentials-section TEXT\n  --help                          Show this message and exit.\n```\n\naws-credential-process is meant to be used as `credential_process` in your `.aws/config` file. For example:\n```\n[profile yourprofile]\ncredential_process = /home/user/venv/aws_credential_process/bin/aws-credential-process --oath-slot "Amazon Web Services:test@example.com" --serial-number arn:aws:iam::123456789012:mfa/john.doe --role-arn arn:aws:iam::123456789012:role/YourRole\n```\n\nIf you\'ve supplied the secret-access-key once you can omit it with the next call, it will be cached in your keyring.\n\nWhen you don\'t supply the access-key-id it will be loaded from `~/.aws/credentials`. You can use another section than "default" by using the credentials-section argument.\n',
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meeuw/aws-credential-process',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
