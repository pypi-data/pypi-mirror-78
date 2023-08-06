import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webhook-debugger",
    version="0.0.3",
    author="LinaLinn",
    author_email="lina.cloud@outlook.de",
    description="A simple http server for debugging Webhooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/linalinn/webhook-debugger",
    packages=setuptools.find_packages(),
    scripts=['WebhookDebugger.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires='>=3.6',
)