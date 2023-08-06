.. _cmd_options:

======================================
Using XT command options
======================================

Every command you issue in XT has a set of directives you use to shape how the command works and what it works on. These are called *command options*.

You can customize behavior of XT commands using two methods:
    - Override the default XT config file properties with a *local* XT config file;
    - Override default and local config file properties using command options. These take precedence over config file properties.

This topic describes how to use XT command options. 

You will also get an introduction to the **xt run** command. It uses a large dedicated set of its own command options.

.. note:: The **xt run** command is a special case with some syntax differences.

------------------------------------------
Standard XT command options
------------------------------------------

The syntax for XT commands (excluding **xt run**) is as follows:

   - **xt** [ <root options/flags> ] <**command keyword**> <command arguments> <command options>

There are two main types of XT command options. Rules for their placement in an XT command are as follows:

    - *Root* options appear before the command keyword and define settings for the command to do its work. They apply to each XT command and always use two hyphens, such as::

        --plot-type

    - *Normal* command options are command-specific and appear after the command keyword(s)). Use them to specify Python scripts, scripts of other types, and operating system commands & executables.

-------------------------------------
Specifying XT root options
-------------------------------------

For command options, always use the general syntax::

    <name>=<value>

Where the <name> of the option (such as **cluster=**) equates to a <value> (such as **ML_Cluster_102**)::

    --cluster=ML_Cluster_102

Root options (**console**, **stack-trace**, etc.) appear immediately after the **xt** name.  These options apply to all XT commands and control things like how much output is displayed during command execution.

--------------
Using XT flags
--------------

XT root flags are global to all XT commmands. They are not associated with a particular command. They also must appear before any command names.

**Flags** are a subset of command options that don't require a `<value>`.  When you specify a flag by their name only, they are automatically set to **true**. You can also explicitly set flags to **On** (using **on**, **true**, or **1**) or **Off** (using **off**, **false**, or **0**).

Option value types include the following:
    - flag            (as described above)
    - string          (quoted string; can be unquoted if value is a simple token)
    - int             (integer value)
    - float           (floating point number)
    - bool            (**true** or **false** value)
    - string list     (a comma separated list of unquoted strings)
    - number list     (a comma separated list of numbers - can be mixture of ints and floats)
    - prop_op_value   (a triple of a property name, a relational operator, and a string or number value, with no spaces between the parts)

The current XT flags include the following::

    --console         (option)  Sets the level of console output (none, normal, diagnostics, detail)
    --help            (flag)    Shows an overview of XT command syntax
    --stack-trace     (flag)    Show the stack trace when an exception is raised
    --quick-start     (flag)    XT startup time is reduced (experimental)

Example::

    xt --console=diagnostics list runs

The command executes the XT 'list runs' command, enabling timing and diagnostic messages.

------------------------------------
Specifying string values in commands
------------------------------------

XT is a command line program, so it gets the majority of its input from the OS command line shell. To use strings as arguments in command options, you need to format the strings depending on the operating system on which you are running XT. Text string formatting is as follows:

    - On Linux, single and double quotes are removed 
    - On Windows, double quotes are removed 

For these reasons, we recommend the following when specifying string values to XT:

    - For strings that consist of a single token, no quotes are needed::

        title=Accuracy

    - On Windows, you can use brackets '{}' or single quotes::
        
        --title={this is my title}
        --title='this is my title'

    - On Linux, you can use {}, nested quotes, or escaped quotes::

        --title={this is my title}
        --title="'this is my title'"
        --title=\'this is my title\'

----------------------
XT Run command options
----------------------

The **xt run** command enables you to execute scripts, executable programs, or operating system commands to run jobs for machine learning. It uses a substantial set of dedicated root options to 

The syntax for the **xt run** command is::

   xt [ <root options> ] run [ <run options> ] <script file> [ <script arguments> ]

XT run command options also use the double-hyphen convention, such as::

--attach=
--cluster=

Run command options apply only to the **run** command and must appear before the **run** keyword in the XT run command. See the section :ref:`XT run command <run>` for more information about **run** command options.

At any time, you can enter::

    xt help run 

You will see a complete listing and descriptions of the **xt run** command's root options, arguments, and examples.

.. seealso:: 

    - :ref:`XT Config file <xt_config_file>`
    - :ref:`XT run command <run>`
    - :ref:`XT Filters <filters>`
