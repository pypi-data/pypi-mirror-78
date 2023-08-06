import setuptools

import rssht_controller_qt


setuptools.setup(
    name='remote-ssh-tunnel-controller-qt',
    version=rssht_controller_qt.__version__,
    author=rssht_controller_qt.__author__,
    author_email='guallo.username@gmail.com',
    description='Remote SSH Tunnel (RSSHT) controller - Qt frontend',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/guallo/remote-ssh-tunnel-controller-qt',
    packages=[rssht_controller_qt.__name__],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'remote-ssh-tunnel-controller-lib>=0.1.0,<1',
        'PySide2>=5.14.2.2,<5.15',
    ],
    entry_points={
        'gui_scripts': [
            'rssht-controller-qt = rssht_controller_qt.main:main',
        ],
    },
)
