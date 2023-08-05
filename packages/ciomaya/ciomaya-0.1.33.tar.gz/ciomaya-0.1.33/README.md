# Conductor for Maya
Conductor for Maya is Maya plugin that contains a Submitter for the Conductor Cloud rendering service.

## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Conductor for Maya. The instructions below will install into a folder called **conductor_plugins** in your home directory. Change the first line if you prefer to install in another location.

### Mac or Linux
Create the installation directory if it doesn't already exist.

```bash
CIO_DIR=$HOME/conductor_plugins && mkdir -p $CIO_DIR
```

Install **ciomaya** and its dependencies

```bash
pip install --upgrade  --force-reinstall  --extra-index-url  https://test.pypi.org/simple/  ciomaya --target=$CIO_DIR
```

Run the setup wizard and choose (1) for each question. 

```bash
$CIO_DIR/bin/setup
```

You can now launch Maya.


To test the conductor shell command type:
```bash
conductor --help
```


### Windows

The Wizard does not work on Windows yet. You'll have to set it up manually. Powershell example:

```powershell
$env:CIO_DIR = "$env:userprofile\conductor_plugins"
md $env:CIO_DIR

pip install --upgrade --extra-index-url  https://test.pypi.org/simple/  ciomaya --target=$env:CIO_DIR

$env:MAYA_MODULE_PATH = "$env:CIO_DIR\ciomaya;$env:MAYA_MODULE_PATH"
$env:PATH = "$env:CIO_DIR\bin;$env:PATH"
$env:PYTHONPATH = "$env:CIO_DIR;$env:PYTHONPATH"
```

To set a persistent environment from Windows:

Start typing `env` in the Windows task bar search panel, then choose **Edit envoronment variables for your account**.
Add the variables listed above to your environment.



## To Update

To update **ciomaya**, use the same pip command. There's no need to set the path variables again if you are in the same shell, or if you have set it up permanently as recommended.


```bash
CIO_DIR=~/conductor_plugins
pip install --upgrade  --extra-index-url  https://test.pypi.org/simple/  ciomaya --target=$CIO_DIR
```

If you want to be sure the old version and dependencies are cleaned out, you can use the `--force-reinstall` flag:

```bash
CIO_DIR=~/conductor_plugins
pip install --upgrade    --force-reinstall --extra-index-url  https://test.pypi.org/simple/  ciomaya --target=$CIO_DIR
```

Next time you open Maya go to **Conductor->About** to check the version was upgraded.

## Usage

Open the Plugin Manager and scroll down to find Conductor.py. When you load it you should see a Conductor menu appear in the main menu bar.

The plugin provides a **conductorRender** node to submit rendering jobs based on values in Maya's **RenderSettings** node.

#### To set up a render:
* Open a scene that's ready to render.
* Use the Plugin Manager to load the Conductor plugin. A Conductor Menu will appear in the main menu bar.
* Choose **Conductor->Submitter->Create**. A submitter node will be created and it will automatically try to connect with Conductor to fetch account data. Sign in woth the browser if necessary.
* Choose an instance type and set up other parameters as required.
* Press submit.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

 

## License
[MIT](https://choosealicense.com/licenses/mit)