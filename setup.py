from setuptools import find_packages,setup

setup(
    name='MCQGenrator',
    version='0.0.1',
    author='KRSNA',
    author_email='krisnabadde@gmail.com',
    install_requires=["google-generativeai","langchain-google-genai","pillow","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)