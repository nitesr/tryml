# tryml
Contains the python code and notebooks for trying out ML models.

Some of the notebooks are from switchup career program @IK which have been modified to explore further on it.

# layout/structure
Based out of mono repo setup described in this blog - https://www.tweag.io/blog/2023-04-04-python-monorepo-1/

*This setup has manual work to keep toml & requirement.txt files up-to-date and also it doesn't use any lib (e.g. poetry) to lock transitive dependencies so there could be suprises*

**Root level folder structure**
- **libs**: contains the python packages which can be used across projects

- **projects**: contains code for different ML topics/assignments/projects at IK and of self explore

- **templates**: contains the template to generate a new package in libs. Look at templates/pylibrary/README.md for commands to create a libs package from template.

# devpi setup
We will use the  PyPi mirror to locally install the /libs packages and looking up them while building the docker files. It will allow to add /libs packages as regular dependencies.

https://devpi.net/docs/devpi/devpi/latest/+doc/index.html

# Kaggle setup
Some of the projects use Kaggle to download the dataset.

On your Kaggle account, under API, select "Create New API Token" and kaggle.json will be downloaded on your computer.

Go to directory — "${user.home}\.kaggle\" — and move here the downloaded JSON file.
