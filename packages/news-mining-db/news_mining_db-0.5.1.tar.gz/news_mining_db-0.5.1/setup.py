from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='news_mining_db',
    url='https://github.com/Myroslav341/news-mining-db',
    author='Myroslav Havryliuk',
    author_email='myroslav04@gmail.com',
    # Needed to actually package something
    packages=[
        'news_mining_db',
        'news_mining_db.migrations',
        'news_mining_db.models',
        'news_mining_db.alembic',
        'news_mining_db.commands',
    ],
    package_data={
        'news_mining_db': ['alembic.ini'],
    },
    entry_points={
        'console_scripts': [
            'init-news-db=news_mining_db.commands:init_db',
            'upgrade-db=news_mining_db.commands:upgrade_db'
        ]
    },
    # Needed for dependencies
    install_requires=['sqlalchemy', 'alembic', 'psycopg2'],
    # *strongly* suggested for sharing
    version='0.5.1',
    # The license can be anything you like
    license='MIT',
    description='Sheared db models for news-mining project',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
