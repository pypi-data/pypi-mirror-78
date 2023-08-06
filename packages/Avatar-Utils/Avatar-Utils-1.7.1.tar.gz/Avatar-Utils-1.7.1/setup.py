import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Avatar-Utils',
    version='1.7.1',
    author='Algorithmics of Complex System',
    author_email='artem.sementsov@gmail.com',
    description='Common utils for services in ecosystem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=[
        'avatar_utils.async_requests',
        'avatar_utils.core',
        'avatar_utils.crawler',
        'avatar_utils.db',
        'avatar_utils.db.mixins',
        'avatar_utils.sso_helper',
        'avatar_utils.logs',
        'avatar_utils.objects',
        'avatar_utils.objects.abstracts',
        'avatar_utils.planner_adapter',
        'avatar_utils.registration',
        'avatar_utils.tests',
        'avatar_utils.validation',
        'avatar_utils.service_accessor',
        'avatar_utils.healthz'
    ],
    install_requires=[
        'aiohttp>=3.6.2',
        'flask>=1.1.1',
        'flask-sqlalchemy>=2.3.2',
        'psycopg2-binary>=2.7.5',
        'requests>=2.23.0',    # registration
        'apispec>=3.3.0',      # registration
        'marshmallow>=3.6.0',  # registration
        'flasgger>=0.9.4',     # registration
        'APScheduler~=3.6.3',
        'python-keycloak~=0.21.0',  # sso_helper
        'cryptography~=3.0',        # sso_helper
        'PyJWT~=1.7.1',             # sso_helper
        'marshmallow_dataclass~=7.6.0',  # objects
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
