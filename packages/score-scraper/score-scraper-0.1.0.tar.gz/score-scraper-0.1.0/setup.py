import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="score-scraper", # Replace with your own username
    version="0.1.0",
    author="Christopher Höllriegl",
    author_email="christopher@hoellriegl.me",
    description="Package to scrape pre-game informations and scores from various websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buddiman/score-scraper",
    license='MIT',
    install_requires=open("requirements.txt").readlines(),
    python_requires='>=3.6',
)