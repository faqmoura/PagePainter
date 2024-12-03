from setuptools import setup, find_packages

setup(
    name="pagepainter",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai",
        "Pillow",
        "python-dotenv",
        "requests",
        "reportlab",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered children's book generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PagePainter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
