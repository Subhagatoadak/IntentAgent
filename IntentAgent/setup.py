from setuptools import setup, find_packages

setup(
    name="IntentAgent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pymongo",
        "openai",
        "anthropic",
        "google-generativeai",
        "transformers"
    ],
    entry_points={
        "console_scripts": [
            "run-tests=pytest:main",
        ]
    },
    author="Subhagato Adak",
    author_email="subhagatoadak.india@gmail.com",
    description="A package for intent classification using LLMs and MongoDB",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
