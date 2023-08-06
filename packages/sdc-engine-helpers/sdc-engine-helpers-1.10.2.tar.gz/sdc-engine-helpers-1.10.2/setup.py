"""
    Set up the sdc_engine_helpers package
"""
from setuptools import setup

setup(
    name='sdc-engine-helpers',
    packages=[
        'sdc_engine_helpers',
        'sdc_engine_helpers.models',
        'sdc_engine_helpers.personalize',
        'sdc_engine_helpers.personalize.maintenance',
        'sdc_engine_helpers.personalize.event',
        'sdc_engine_helpers.personalize.recommendations',
        'sdc_engine_helpers.sagemaker',
        'sdc_engine_helpers.sagemaker.recommendations',
        'sdc_engine_helpers.sagemaker.maintenance',
    ],
    install_requires=[
        'sdc-helpers==1.6.1'
    ],
    description='AWS Recommendation Engine Helpers',
    url='http://github.com/RingierIMU/sdc-recommend-engine-helpers',
    version='1.10.2',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=[
        'pip',
        'helpers',
        'aws',
        'recommendation',
        'personalize',
        'sagemaker'
    ],
    download_url='https://github.com/RingierIMU/sdc-recommend-engine-helpers/archive/v1.9.2.zip'
)
