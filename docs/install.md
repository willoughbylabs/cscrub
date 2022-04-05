# Build From Source
Below is my configuration for building this scraper locally.

## My Configuration
Built and running using macOS 12.3.1 and Python 3.10.3.

## Install Dependencies
Install the following using your preferred Terminal app.<br/> 
Please double check all main sites before running code hardcorded here, just in case the maintainers' instructions have changed.

### Xcode Command Line Tools
- Required for Homebrew.

    ```
    xcode-select --install
    ```
### Homebrew
- [Homebrew](https://brew.sh/)

### pyenv
- [pyenv](https://github.com/pyenv/pyenv) (using Homebrew)

    ```
    brew update
    brew install pyenv
    ```

### pyenv-virtualenv
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

    ```
    brew update
    brew install pyenv-virtualenv

    ```

### Selenium
[Selenium](https://www.selenium.dev/documentation/webdriver/getting_started/) is used to automate browser actions.
- Install the [Selenium library for Python](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/).

    ```
    pip install selenium
    ```
- Download [appropriate browser driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) for your browser of choice. 

### Webdriver Manager
[Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager) keeps the webdriver version updated with the broswer version. 

    ```
    pip install webdriver-manager
    ```

## Configure Dependencies

### pyenv
See [pyenv's COMMANDS.md](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md) for additional usage info.
- View list of available Python versions and install 3.10.3 (or later, but not fully tested).
    ```shell
    pyenv install --list
    pyenv install version

    # i.e. pyenv install 3.10.3
    ```

### pyenv-virtualenv
See [pyenv-virtualenv's GitHub](https://github.com/pyenv/pyenv-virtualenv) for additional usage info.
- Create a new virtual environment specifying the preferred Python version from your installs. 
```shell
pyenv virtualenv 3.10.3 name-of-virtualenv

# i.e. pyenv virtualenv 3.10.3 cscrub3.10.3
```
- In the cscrub directory, add a `.python-version`. Inside the file, write the name of the virtual environment to [auto-activate the virtualenv](https://github.com/pyenv/pyenv-virtualenv#activate-virtualenv)
```shell
# Inside .python-version, for example:

cscrub3.10.3
```
