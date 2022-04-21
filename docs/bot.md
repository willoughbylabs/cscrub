# Build Bot From Source
Built and running using macOS 12.3.1 and Python 3.10.3.

## Steps
1. Install Mac dependencies.
2. Configure Mac dependencies.
3. Install Python dependencies.
4. Set configurations in [app.py](../app.py).

## Install Mac Dependencies

Please double check all main sites before running code hardcorded here, just in case the maintainers' instructions have changed.

### Xcode Command Line Tools
- Required for Homebrew. </br>
    `xcode-select --install`

### Homebrew
- A package manager, in this case used for installing Python-related tools.
- [Homebrew](https://brew.sh/)

### PostgreSQL
- An open-source, relational database system.
- [Postgres.app](https://postgresapp.com/) offers an easy installation.

### pyenv
- Used to install and manage different versions of Python.
- [pyenv](https://github.com/pyenv/pyenv) (install using Homebrew)</br>
    `brew update`</br>
    `brew install pyenv`

### pyenv-virtualenv
- Used to manage a virtual environment for this app's Python version and its specific dependencies.
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (install using Homebrew)</br>
    `brew update`</br>
    `brew install pyenv-virtualenv`

## Configure Mac Dependencies

### PostgreSQL
- After completing the [Postgres.app install steps](https://postgresapp.com/), start the PostgreSQL server.
- To create a new database, in your Terminal app, run:</br>
`createdb cscrub`

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
- In the cscrub directory, add a `.python-version` file. Inside this file, write the name of the virtual environment to [auto-activate the virtualenv](https://github.com/pyenv/pyenv-virtualenv#activate-virtualenv).

    ```shell
    # Inside .python-version, for example:

    cscrub3.10.3
    ```
## Install Python Dependencies

- All dependencies below can be automatically installed using the `requirements.txt` file.</br>
    `pip install -r requirements.txt`
- To see what this command installs, or to install the components separately, please see below.

### Selenium
- [Selenium](https://www.selenium.dev/documentation/webdriver/getting_started/) is used to automate browser actions.
- Install the [Selenium library for Python](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/).</br>
    `pip install selenium`

### Webdriver Manager
- [Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager) updates the webdriver version to remain compatible with the broswer version.</br> 
    `pip install webdriver-manager`
- In [`models/helpers/wd_connect.py`](../models/helpers/wd_connect.py), please note to set the imports at the top based on the browser you intend to use (more info available from [webdriver-manager's site](https://pypi.org/project/webdriver-manager/)).

### psycopg2-binary
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) is an adapater for PostgreSQL.</br>
    `pip install psycopg2-binary`

### SQLAlchemy
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/quickstart.html) is an ORM to map Python objects to PostgreSQL tables.</br>
    `pip install sqlalchemy`

### feedparser
- [feedparser](https://pypi.org/project/feedparser/) helps parse an RSS feed.</br>
    `pip install feedparser`


## Set Configurations in app.py

- A `CONFIGURATIONS` section at the top of [app.py](../app.py) allows for customizing the bot's actions. 

#### `create_tables_in_db`
- `TRUE`: creates tables in the database.
- This should be run as `TRUE` at least once.

#### `add_members_to_db`
- `TRUE`: fetches and adds City Council members to the `Alderpersons` table.

#### `add_meetings_to_db`
- `TRUE`: fetches and adds City Council meeetings to the `Meetings` table.

#### `add_legislation_to_db`
- `TRUE`: fetches and adds legislation from each meeting to the `Legislation` table.
- This option can be further customized using `set_legislation_links_list` and `links_list`.

#### `set_legislation_links_list`
- `FALSE`, by default: the bot will fetch legislation for every meeting in the database. 
- To override this behavior, and only fetch legislation from specific meetings, set this option to `TRUE`. 
- Use `links_list` to set which meetings to fetch legislation from.

#### `links_list`
- Accepts an `array` of `Meetings` links.
- Each meeting in the database has a `link` column.
- To set which meeting to fetch legislation from, obtain the meeting's link, and append to the `links_list` variable.
- When `set_legislation_links_list` is set to `TRUE`, the bot will only fetch legislation for the meetings appended to `links_list`. 
