from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-wiki",
    version="0.1.0",
    author="LLM Wiki Contributors",
    author_email="",
    description="LLM-powered knowledge management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/llm-wiki",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.18.0",
        "ollama>=0.1.0",
        "click>=8.1.0",
        "pyyaml>=6.0",
        "pypdf>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "llm-wiki=llm_wiki.cli:cli",
        ],
    },
)
