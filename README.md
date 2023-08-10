# Build data feed for embedding from your Gmail

## Reuqirements

You need to set up your Gmail API credentials. Follow septs from [here](https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment) for details.

You should have a `credentials.json` file in the `src` directory.

## Usage 

```sh
pipenv shell
pipenv install
python src/main.py
```

Output `1_messages.txt` files will be saved in `generated_output` directory.