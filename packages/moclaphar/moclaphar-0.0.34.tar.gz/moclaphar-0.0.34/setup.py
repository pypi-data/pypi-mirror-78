import setuptools

setuptools.setup(
    name="moclaphar",
    version="0.0.34",
    license='MIT',
    author="Jongkuk Lim",
    author_email="lim.jeikei@gmail.com",
    description="This packages mainly aims to make an easy process for dataset manipulation.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JeiKeiLim/moclaphar",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'scipy>=1.4.1',
        'matplotlib>=3.2.1',
        'seaborn>=0.10.1',
        'h5py>=2.10.0',
        'pandas>=1.0.3',
        'moviepy>=1.0.3',
        'tqdm>=4.46.0',
        'opencv-python>=4.2.0'
      ],
)