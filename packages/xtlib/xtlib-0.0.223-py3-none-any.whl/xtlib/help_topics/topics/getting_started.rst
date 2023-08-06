.. _getting_started:

========================================
Getting Started with XT
========================================

XT is a command line tool to manage and scale machine learning experiments, with a uniform model of workspaces and runs, across a variety of cloud compute services.  It supports powerful ML services such as :ref:`live and post Tensorboard viewing <tensorboard>`, :ref:`hyperparameter searching <hyperparameter_search>`, and :ref:`ad-hoc plotting <plot>`.

You can run XT on both Windows and Linux platforms. 

This topic introduces you to XT and its various components, and describes how to install and run the XT package and its demonstration Python package (called **xt demo**). We also provide a list of additional resources for reference and inspiration at the end of this topic.

---------------------------
Introduction to XT
---------------------------

Your XT installation leverages the following Azure cloud services to help you develop, test and deploy new Machine Learning experiments:

    - Azure Batch
    - Azure Container Registry
    - Azure Cosmos DB - MongoDB
    - Azure Storage
    - Azure Key Vault
    - Azure Virtual Machine / Virtual Machine Scale Set
    - Generic Remote Server
    - Azure Machine Learning Services

.. only:: internal

    - Philly

You conduct your own experiments using a :ref:`powerful **xt run** command <run>` to submit jobs that XT can run and complete for you.
While you test, design and run your first experiments, be aware that you can incur additional costs through usage of services such as Cosmos and virtual machines. 

-----------------------
XT Requirements
-----------------------

Requirements for installing and running XT are:
    - Windows or Linux OS
    - Python 3.5 or later   (recommended: Python 3.6)
    - Anaconda or other virtual Python environment (recommended: Anaconda)
    - User must have an Azure account (required for authenticated access to Azure computing storage and resources)
    - For Linux users who will be using the Microsoft internal Philly services, you should install **curl**::

        https://www.cyberciti.biz/faq/how-to-install-curl-command-on-a-ubuntu-linux/

----------------------------------
XT's Core Services
----------------------------------

XT has many machine learning features and commands, which revolve around three core operations:

+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| Core Operations         | Description                       | Azure Services Used      |
+============+============+===========+===========+===========+===========+===========+==+
| **Job submissions**     | Submit and run jobs with XT.      | Azure ML, Azure Batch    |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| **Experiment            | Jobs store their data artifacts in| Azure Storage,           |
| Storage**               | your Azure Storage Service.       | Container Registry       |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| **Experiment            | Stats include Job properties, Run | Azure Storage, MongoDB   |
| Statistics**            | properties, metrics, and          |                          |
|                         | hyperparameter settings.          |                          |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+

In this documentation, you will learn how to install and use all of these cloud services with XT.

.. Note:: XT supports all Machine Learning frameworks. The following procedure installs PyTorch because it supports the XT demo. XT also supports important ML tools such as TensorFlow. You can also use :ref:`hyperparameter searching <hyperparameter_search>` to tune and improve your machine learning models.

------------------
Installing XT
------------------

XT package installation is straightforward. Follow these steps to set up XT on your computer. You may need to `install Anaconda <https://www.anaconda.com/distribution/>`_ on your system in order to follow these steps:

    **1. PREPARE a conda virtual environment with PyTorch:**
        
        .. code-block::

            > conda create -n MyEnvName python=3.6
            > conda activate MyEnvName
            > conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

    **2. INSTALL XT:**

        .. code-block::

            > pip install -U xtlib

After you install XT, you can run the XT demo to get a closer look at how it works.

------------------------------------
Running the XT Demo
------------------------------------

XT offers a self-contained demo that walks you through several usage scenarios, using multiple Machine Learning backends. Each step of the demo, which you run from the Conda command line interface, provides descriptions explaining what that step does during the course of a sample experiment.

    **1. Start XT on your system:**
        
        .. code-block::

            > cd c:\ExperimentTools
            > activate xt

    **2. CREATE a set of demo files:**

        .. code-block::

            > xt create demo xt_demo

            This creates 2 files and 1 subdirectory in the *xt_demo* directory:
                - xt_config_overrides.yaml     (xt config settings, active when xt is run from this directory)
                - xt_demo.py - the python file that drives the demo
                - code  (a subdirectory containing some files used by the demo app)

    **3. Start the XT demo:**

        .. code-block::

            > cd xt_demo
            > python xt_demo.py

        Once started, you can navigate thru the demo with the following keys:
            - ENTER (to execute the current command)
            - 's'   (to skip to the next command)
            - 'b'   (to move to the previous command)
            - 'q'   (to quit the demo)

While you run the demo, you may encounter a point where it stops running. This typically happens when a numbered demo step relies on a cloud service that you may have not yet configured. To continue with the demo, note the step where the demo stopped, and enter *python xt_demo.py* once again. Then, press the 's' key to step through the demo past the numbered step where you previously stopped. 

------------
Next Steps
------------

After installation and running the XT demo, you can set up your Azure cloud services to work with XT. You do so by editing the properties inside an important document called your local *xt_config* file. See :ref:`Setting up your XT Installation <xt_config_file>` for more information.

For those just beginning to explore ML on the Microsoft Azure cloud platform, see the `What is Azure Machine Learning? <https://docs.microsoft.com/en-us/azure/machine-learning/>`_ page, and `What is Azure Batch? <https://docs.microsoft.com/en-us/azure/batch/batch-technical-overview/>`_, which gives a full description of the Azure Batch service.

To learn more about running jobs using the **xt run** command, see :ref:`XT run command <run>`.