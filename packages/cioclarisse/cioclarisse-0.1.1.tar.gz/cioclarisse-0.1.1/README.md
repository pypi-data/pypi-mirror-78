# Conductor for Clarisse
Conductor for Clarisse is Clarisse plugin that contains a Submitter for the Conductor Cloud rendering service.

## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Conductor for Clarisse. The instructions below will install into a folder called **conductor_plugins** in your home directory. Change the first line if you prefer to install in another location.

### Mac or Linux
Use a variable to hold the install location.

```bash
CONDUCTOR_DIR=$HOME/conductor_plugins
```
Make sure the directory exists

```bash
mkdir -p $CONDUCTOR_DIR
```

Install **cioclarisse** and its dependencies

```bash
pip install --upgrade  --force-reinstall  --extra-index-url  https://test.pypi.org/simple/  cioclarisse --target=$CONDUCTOR_DIR
```
Set the MAYA_MODULE_PATH in the shell to let Clarisse know where to find the plugin. You should also set the PYTHONPATH and PATH variables to ensure the Conductor API and commandline tools are available
```bash
export MAYA_MODULE_PATH=$CONDUCTOR_DIR/cioclarisse:$MAYA_MODULE_PATH
export PATH=$CONDUCTOR_DIR/bin:$PATH
export PYTHONPATH=$CONDUCTOR_DIR:$PYTHONPATH
```
You can now run Clarisse with Conductor from this shell. 

```bash
</path/to>/maya
```

To test the conductor shell command type:
```bash
conductor --help
```


### Windows

The process is similar for Windows users. For example, if you run Clarisse from Powershell:

```powershell
$env:CONDUCTOR_DIR = "$env:userprofile\conductor_plugins"
md $env:CONDUCTOR_DIR

pip install --upgrade --extra-index-url  https://test.pypi.org/simple/  cioclarisse --target=$env:CONDUCTOR_DIR

$env:MAYA_MODULE_PATH = "$env:CONDUCTOR_DIR\cioclarisse;$env:MAYA_MODULE_PATH"
$env:PATH = "$env:CONDUCTOR_DIR\bin;$env:PATH"
$env:PYTHONPATH = "$env:CONDUCTOR_DIR;$env:PYTHONPATH"
```
 

### Permanent setup
To ensure the module is always available, you'll need to set the path variables in your .bashrc or similar. Some examples:

To set a persistent environment on Mac or Linux in .bashrc, type:
```bash
echo 'export CONDUCTOR_DIR=$HOME/conductor_plugins' >> ~/.bashrc
echo 'export MAYA_MODULE_PATH=$CONDUCTOR_DIR/cioclarisse:$MAYA_MODULE_PATH' >> ~/.bashrc
echo 'export PATH=$CONDUCTOR_DIR/bin:$PATH' >> ~/.bashrc
echo 'export PYTHONPATH=$CONDUCTOR_DIR:$PYTHONPATH' >> ~/.bashrc
```

To set a persistent environment from Windows:

Start typing `env` in the Windows task bar search panel, then choose **Edit envoronment variables for your account**.
Edit the environment as illustrated below.

![Winenv](images/winenv.png)



## To Update

To update **cioclarisse**, use the same pip command. There's no need to set the path variables again if you are in the same shell, or if you have set it up permanently as recommended.


```bash
CONDUCTOR_DIR=~/conductor_plugins
pip install --upgrade  --extra-index-url  https://test.pypi.org/simple/  cioclarisse --target=$CONDUCTOR_DIR
```

If you want to be sure the old version and dependencies are cleaned out, you can use the `--force-reinstall` flag: 

```bash
CONDUCTOR_DIR=~/conductor_plugins
pip install --upgrade    --force-reinstall --extra-index-url  https://test.pypi.org/simple/  cioclarisse --target=$CONDUCTOR_DIR
```

Next time you open Clarisse go to **Conductor->About** to check the version was upgraded.  

## Usage

Open the Plugin Manager and scroll down to find Conductor.py. When you load it you should see a Conductor menu appear in the main menu bar.

The plugin provides a **conductorRender** node to submit rendering jobs based on values in Clarisse's **RenderSettings** node.

#### To set up a render:
* Open a scene that's ready to render.
* Use the Plugin Manager to load the Conductor plugin. A Conductor Menu will appear in the main menu bar.
* Choose **Conductor->Submitter->Create**. A submitter node will be created and it will automatically try to connect with Conductor to fetch account data. Sign in woth the browser if necessary.
* Choose an instance type and set up other parameters as required.
* Press submit.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

You'll find a guide for setting up an efficient development workflow [here]().


## License
[MIT](https://choosealicense.com/licenses/mit)