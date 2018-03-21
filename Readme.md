# Houdini - The Research

An exploration into datascience, a research into figuring out how to determine purchase intent using from a social feed using maching learning. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Clone this repository unto your system

```
git clone git@bitbucket.org:ampersandlabs-gh/houdini-research.git
```

### Run using docker

```
docker-compose up
```

You would see something similar to this when the app starts successfully. 

```
notebook_1  | [I 13:55:25.246 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
notebook_1  | [I 13:55:25.801 NotebookApp] Serving notebooks from local directory: /app/notebook
notebook_1  | [I 13:55:25.802 NotebookApp] 0 active kernels
notebook_1  | [I 13:55:25.802 NotebookApp] The Jupyter Notebook is running at:
notebook_1  | [I 13:55:25.803 NotebookApp] http://0.0.0.0:8888/?token=514848f23f594b8adc7e1be166a16917a868073f74423f4e
notebook_1  | [I 13:55:25.803 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
notebook_1  | [W 13:55:25.804 NotebookApp] No web browser found: could not locate runnable browser.
notebook_1  | [C 13:55:25.805 NotebookApp]
notebook_1  |
notebook_1  |     Copy/paste this URL into your browser when you connect for the first time,
notebook_1  |     to login with a token:
notebook_1  |         http://0.0.0.0:8888/?token=514848f23f594b8adc7e1be166a16917a868073f74423f4e
notebook_1  | [W 13:55:35.134 NotebookApp] Forbidden
notebook_1  | [W 13:55:35.138 NotebookApp] 403 GET /api/sessions?_=1521639957907 (172.19.0.1) 12.56ms referer=http://0.0.0.0:8888/tree/notebook
notebook_1  | [W 13:55:35.144 NotebookApp] Forbidden
notebook_1  | [W 13:55:35.146 NotebookApp] 403 GET /api/terminals?_=1521639957908 (172.19.0.1) 4.40ms referer=http://0.0.0.0:8888/tree/notebook
notebook_1  | [I 13:55:37.610 NotebookApp] 302 GET /?token=514848f23f594b8adc7e1be166a16917a868073f74423f4e (172.19.0.1) 1.30ms
```

## Built With

* [Python](https://python.org/) - The web framework used
* [PIP](https://npmjs.com/) - Dependency Management
* [Sklearn](https://npmjs.com/) - Scikit Learn
* [Jupyter](https://npmjs.com/) - Jupyter
* [Matplotlib](https://npmjs.com/) - Matplotlib 




## License

This project is licensed under the ISC License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

