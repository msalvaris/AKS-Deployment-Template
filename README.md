# AKS Deployment cookiecutter
This repo contains the templates for generating the deployment notebooks for the following repositories:
* [Image Classification](https://github.com/msalvaris/AKS-Deployment-for-Image-Classification)
* [Sentiment Analysis]()


## Prerequisites
Uubntu Linux VM/PC  
[Anaconda](https://docs.anaconda.com/anaconda/install/)  
[Hub](https://github.com/github/hub)
 

## Setup & Run
To generate the files from the template and update the final repos clone the project: 
```
git clone https://github.com/msalvaris/AKS-Deployment-Template
```

Configure git and hub with your GitHub credentials and then finally run:
```
chmod +x scripts/bash/generate
scripts/bash/generate
```

This script will do the following:
1) Create a conda env based on the dev_environment.yml file
2) It will use invoke to call update
3) This will call cookiecutter to generate the appropriate projects
4) The staging branches of the repos will be cloned 
5) The files will updated based on the cookiecutter template and the changes pushed to a branch
6) A PR will be made on the specified branches
7) All files and conda environments are cleaned up



# Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
