from setuptools import setup

setup(
    name="artretention",
    version="1.0.0",
    install_requires=[
        "requests",
        "retry"
    ],
    author = "Dan Clayton",
    author_email = "dclayton@godaddy.com",
    description = "Manage artifactory retention.",
    license = "MIT",
    keywords = "artifactory registries registry retention",
    url = "https://github.com/azweb76/artifactory-retention",
    packages=['artretention', 'artretention.common', '.'],
    entry_points={
        'console_scripts': [
            'artret=artretention.artret:main',
        ],
    },
)
