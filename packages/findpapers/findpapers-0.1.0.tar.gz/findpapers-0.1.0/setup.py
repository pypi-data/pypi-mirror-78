# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['findpapers',
 'findpapers.models',
 'findpapers.searchers',
 'findpapers.tools',
 'findpapers.utils']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'edlib>=1.3.8,<2.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'inquirer>=2.7.0,<3.0.0',
 'lxml>=4.5.2,<5.0.0',
 'requests>=2.24.0,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['findpapers = findpapers.cli:main']}

setup_kwargs = {
    'name': 'findpapers',
    'version': '0.1.0',
    'description': 'Easy way to find academic papers across scientific databases by using a single query.',
    'long_description': '# Findpapers\n\nFindpapers is a console application that helps researchers find papers by submitting a single query to multiple databases (currently ACM, arXiv, IEEE, PubMed, and Scopus)\n\n## Requirements\n\n- Python 3.7+\n\n## Installation\n\n```console\n$ pip install findpapers\n```\n\n## Usage\n\nWe basically have 4 basic commands available in the tool:\n\n- ```findpapers search```\n\n    When you have a query and needs to get papers using it, this is the command that you\'ll need to call.\n    This command will find papers from some databases based on the provided query.\n\n    All the query terms need to be enclosed by single quotes (\') and can be associated using boolean operators,\n    and grouped using parentheses. The available boolean operators are "AND", "OR". "NOT".\n    All boolean operators needs to be uppercased. The boolean operator "NOT" must be preceded by an "AND" operator.\n\n    E.g.: \'term A\' AND (\'term B\' OR \'term C\') AND NOT \'term D\'\n\n    You can use some wildcards in the query too. Use ? to replace a single character or * to replace any number of characters.\n\n    E.g.: \'son?\' -> will match song, sons, ...\n\n    E.g.: \'son*\' -> will match song, sons, sonar, songwriting, ...\n\n    Nowadays, we search for papers on ACM, arXiv, IEEE, PubMed, and Scopus database.\n    The searching on IEEE and Scopus requires an API token, that must to be provided\n    by the user using the -ts (or --scopus_api_token) and -te (or --ieee_api_token) arguments.\n    If these tokens are not provided the search on these databases will be skipped.\n\n    You can constraint the search by date using the -s (or --since) and -u (or --until) arguments\n    following the pattern YYYY-MM-DD (E.g. 2020-12-31). \n    \n    You can restrict the max number of retrived papers by using -l (or --limit).\n    And, restrict the max number of retrived papers by database using -ld (or --limit_per_database) argument.\n\n    Usage example:\n\n    ```console\n    $ findpapers search /some/path/search.json "(\'machine learning\' OR \'deep learning\') AND \'music\' AND NOT \'drum*\'" -s 2019-01-01 -u 2020-12-31 -ld 100 -v -ts VALID_SCOPUS_API_TOKEN -te VALID_IEEE_API_TOKEN\n    ```\n\n- ```findpapers refine```\n\n    When you have a search result and wanna refine it, this is the command that you\'ll need to call.\n    This command will iterate through all the papers showing their collected data,\n    then asking if you wanna select a particular paper or not\n\n    You can show or hide the paper abstract by using the -a (or --abstract) flag.\n\n    If a comma-separated list of categories is provided by the -c (or --categories) argument, \n    you can assign a category to the paper.\n\n    And to help you on the refinement, this command can also highlight some terms on the paper\'s abstract \n    by a provided comma-separated list of them provided by the -h (or --highlights) argument.\n\n    ```console\n    $ findpapers refine /some/path/search.json -c "Category A, Category B" -h "result, state of art, improve, better" -v\n    ```\n\n- ```findpapers download```\n\n    If you\'ve done your search, (probably made the search refinement too) and wanna download the papers, \n    this is the command that you need to call. This command will try to download the PDF version of the papers to\n    the output directory path.\n\n    You can download only the selected papers by using the -s (or --selected) flag\n\n    We use some heuristics to do our job, but sometime they won\'t work properly, and we cannot be able\n    to download the papers, but we logging the downloads or failures in a file download.log\n    placed on the output directory, you can check out the log to find what papers cannot be downloaded\n    and try to get them manually later. \n\n    Note: Some papers are behind a paywall and won\'t be able to be downloaded by this command. \n    However, if you have a proxy provided for the institution where you study or work that permit you \n    to "break" this paywall. You can use this proxy configuration here\n    by setting the environment variable FINDPAPERS_PROXY.\n\n    ```console\n    $ findpapers download /some/path/search.json /some/path/papers/ -s -v\n    ```\n\n- ```findpapers download```\n\n    Command used to generate a BibTeX file from a search result.\n\n    You can generate the bibtex only for the selected papers by using the -s (or --selected) flag\n\n    ```console\n    $ findpapers bibtex /some/path/search.json /some/path/mybib.bib -s -v\n    ```\n\nMore details about the commands can be found by running ```findpapers [command] --help```. \n\nYou can control the commands logging verbosity by the -v (or --verbose) argument.\n\nI know that this documentation is boring and incomplete, and it needs to be improved.\nI just don\'t have time to do this for now. But if you wanna help me with it see the [contribution guidelines](https://gitlab.com/jonatasgrosman/findpapers/-/blob/master/CONTRIBUTING.md).\n\n\n## FAQ\n\n- I don\'t have the API token for Scopus and IEEE databases, how do I get them?\n\n    Go to https://dev.elsevier.com and https://developer.ieee.org to get them\n\n- When I tried to download the papers collected in my search, most of them were not downloaded, why did this happen?\n\n    Most papers are behind a paywall, so you may not have access to download them using the network you\'re connected to. However, this problem can be worked around, if you have a proxy from the institution where you work/study that has broader access to these databases, you only need to define a environment variable called FINDPAPERS_PROXY with the URL that points to that proxy. Another possible cause of the download problem is some limitation in the heuristic that we use to download the papers, identifying this problem and coding a solution is a good opportunity for you to contribute to our project. See the [contribution guidelines](https://gitlab.com/jonatasgrosman/findpapers/-/blob/master/CONTRIBUTING.md)\n\n- My institutional proxy has login and password, how can i include this in the proxy URL definition?\n\n    Probably your institutional proxy can be defined with credentials following the pattern "https://[username]:[password]@[host]:[port]"\n\n\n## Want to help?\n\nSee the [contribution guidelines](https://gitlab.com/jonatasgrosman/findpapers/-/blob/master/CONTRIBUTING.md)\nif you\'d like to contribute to Findpapers project.\n\nYou don\'t even need to know how to code to contribute to the project. Even the improvement of our documentation is an outstanding contribution.\n\nIf this project has been useful for you, please share it with your friends, this project could be helpful for them too.\n\nAnd, if you like this project and wanna motivate the maintainers, give us a :star:. This kind of recognition will make us very happy with the work that we\'ve done :heart:\n\n---\n\n**Note**: If you\'re seen this project from GitHub, this is just a mirror, \nthe official project source code is hosted [here](https://gitlab.com/jonatasgrosman/findpapers) on GitLab.',
    'author': 'Jonatas Grosman',
    'author_email': 'jonatasgrosman@gmail.com',
    'maintainer': 'Jonatas Grosman',
    'maintainer_email': 'jonatasgrosman@gmail.com',
    'url': 'https://gitlab.com/jonatasgrosman/findpapers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
