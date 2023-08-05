from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "image_processing_ofc",
    version = "0.0.1",
    author = "Renoir Sampaio",
    author_email = "renoir@alu.ufc.br",
    description = "Test version - Image processing",
    long_description = page_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RenoirSampaio/Pacotes_Processamento_Imagens_Python",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.8',
)