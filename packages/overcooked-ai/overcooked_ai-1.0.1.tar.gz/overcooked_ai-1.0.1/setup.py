#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='overcooked_ai',
      version='1.0.1',
      description='Cooperative multi-agent environment based on Overcooked',
      author='Nathan Miller',
      author_email='nathan_miller23@berkeley.edu',
      url='https://github.com/HumanCompatibleAI/overcooked_ai',
      download_url='https://github.com/HumanCompatibleAI/human_aware_rl/archive/v1.0.0.tar.gz',
      packages=find_packages('src'),
      keywords=['Overcooked', 'AI', 'Reinforcement Learning'],
      package_dir={"": "src"},
      package_data={
        'overcooked_ai_py' : ['data/layouts/*.layout', 'data/planners/*.py', 'data/human_data/*.pickle']
      },
      install_requires=[
        'numpy',
        'tqdm',
        'gym',
        'ipython'
      ]
    )