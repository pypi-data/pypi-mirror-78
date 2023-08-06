
import setuptools

setuptools.setup(
    name="warpseq",
    version="0.3.17",
    author="Michael DeHaan",
    author_email="michael@michaeldehaan.net",
    description="MIDI sequencer",
    long_description="text-based MIDI sequencer",
    long_description_content_type="text/plain",
    url="https://warpseq.com",
    packages=setuptools.find_packages(),
    package_data={'package': [ 'templates/*', 'static/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "python-rtmidi",
        "falcon",
        "requests",
        "jinja2"
    ]
)
