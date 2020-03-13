from setuptools import setup

setup(
    name="pytils",
    version="0.0",
    packages=[
        "pytils",
        "pytils.override",
    ],
    install_requires=[],
    scripts=[
        "scripts/profile-stats.py",
        "scripts/pretty-simple.py",
    ]
)
