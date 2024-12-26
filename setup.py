from setuptools import setup, find_packages

setup(
    name="video-organizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 如果有依赖包，在这里列出
    ],
    entry_points={
        'console_scripts': [
            'video-organizer=src.cli.main:main',
            'video-organizer-gui=src.gui.main:main',
        ],
    },
    python_requires='>=3.11',
) 