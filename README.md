# langchaindocuments

Project to explore Langchain tool wich implement those features: 
- Twitter ice breaker


### Prerequisites and Dependencies

Before you begin, ensure you have the following installed:
- Python 3.11.x or later. Note that this was only tested on 3.11.8
- [Pipenv](https://pipenv.pypa.io/en/latest/) : tested on v2024.4.0


```bash
python --version
pipenv --version
```

### Cleanup pipenv environment : Make sure you're in the project directory when running these commands

```bash
python --version
pipenv --version

deactivate
pipenv --rm
```

Remove the packages from the Piplock.file
```bash
rm Pipfile Pipfile.lock
```

### Installation


Recommend using Install pipenv or other vitual environment tool. 


```bash
pipenv --version
python --version
```

```bash
pipenv install
pipenv shell
python --version
```


Clone the repository and install the required packages:

```bash
git clone https://github.com/yacine555/langchain-documents.git
cd langchain-documents
pipenv install -r requirements.txt
```



### Running the Application

Start the application by running:

```bash
pipenv run python main.py
pipenv run python ./tools/twitter.py
```

run flask server

```bash
pipenv run python app.py
```
