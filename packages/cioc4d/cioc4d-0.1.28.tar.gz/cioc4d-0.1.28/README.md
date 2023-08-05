# Conductor-C4d

Conductor-C4d is Cinema 4d plugin that contains a Submitter for the Conductor Cloud rendering service.

## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Conductor-C4d. The instructions below use pip's `target` flag to install into a folder called **conductor_plugins** in your home directory. Change the first line if you prefer to install in another location.

### Mac or Linux
Create the installation directory if it doesn't already exist.

```bash
CIO_DIR=$HOME/conductor_plugins && mkdir -p $CIO_DIR
```
Install **cioc4d** and its dependencies. 

```bash
pip install --upgrade --extra-index-url  https://test.pypi.org/simple/  cioc4d --target=$CIO_DIR
```

Run the setup wizard and choose (1) for each question. 

```bash
$CIO_DIR/bin/setup
```

You can now run C4d with Conductor from a new shell. 

```bash
open '/Applications/Maxon Cinema 4D R22/Cinema 4D.app'
```

To test the conductor shell command type:
```bash
conductor --help
```


### Windows

The Wizard does not work on Windows yet. You'll have to set it up manually. Powershell example:

```powershell
$env:CIO_DIR = "$env:userprofile\conductor_plugins"
md $env:CIO_DIR

pip install --upgrade --extra-index-url  https://test.pypi.org/simple/  cioc4d --target=$env:CIO_DIR

$env:g_additionalModulePath = "$env:CIO_DIR\cioc4d"
$env:PATH = "$env:CIO_DIR\bin;$env:PATH"
$env:PYTHONPATH = "$env:CIO_DIR;$env:PYTHONPATH"
```

To set a persistent environment from Windows:

Start typing `env` in the Windows task bar search panel, then choose **Edit envoronment variables for your account**.
Add the variables listed above to your environment.


## To Update

To update **cioc4d**, use the same pip command. There's no need to set the path variables again if you are in the same shell, or if you have set it up permanently as recommended.


```bash
CIO_DIR=~/conductor_plugins
pip install --upgrade  --extra-index-url  https://test.pypi.org/simple/  cioc4d --target=$CIO_DIR
```

If you want to be sure the old version and dependencies are cleaned out, you can use the `--force-reinstall` flag: 

```bash
CIO_DIR=~/conductor_plugins
pip install --upgrade  --force-reinstall  --extra-index-url  https://test.pypi.org/simple/  cioc4d --target=$CIO_DIR
```

Next time you open C4d go to **Conductor->About** to check the version was upgraded. (NOT IMPLEMENTED YET) 

## Usage

Open the Extensions menu or the Conductor menu and choose ConductorRender to open the submission dialog.

#### To set up a render: (NOT IMPLEMENTED YET / WIP) 

* Open a scene that's ready to render.
* Open the ConductorRender dialog and sign in to your account.
* Choose an instance type and set up other parameters as required.
* Press submit.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit)