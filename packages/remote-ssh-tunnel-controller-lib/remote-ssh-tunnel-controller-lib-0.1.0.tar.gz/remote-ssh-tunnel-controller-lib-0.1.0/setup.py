import setuptools

import rssht_controller_lib


setuptools.setup(
    name='remote-ssh-tunnel-controller-lib',
    version=rssht_controller_lib.__version__,
    author=rssht_controller_lib.__author__,
    author_email='guallo.username@gmail.com',
    description='Remote SSH Tunnel (RSSHT) controller library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/guallo/remote-ssh-tunnel-controller-lib',
    packages=[rssht_controller_lib.__name__],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'paramiko>=2.7.1,<3',
    ],
)
