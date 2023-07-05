# gcp-experiments

## Run locally

```
% cd functions

% python3 -m venv env

% source env/bin/activate

% export GOOGLE_CLOUD_PROJECT=getting-started-337714

% python main.py "{'gameId': '100', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'}"

% python main.py "{'gameId': '101', 'fen': 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'}"
```

## Run tests

```
% pytest
```

## Create topic

```
% gcloud pubsub topics create random-topic
```

## Deploy function

```
% gcloud functions deploy random-function --gen2 --runtime=python311 --region=us-central1 --source=. --entry-point=subscribe --trigger-topic=random-topic

% gcloud pubsub topics publish random-topic --message="{'gameId': '100', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'}"

% gcloud pubsub topics publish random-topic --message="{'gameId': '101', 'fen': 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'}"
```

## Links

* https://cloud.google.com/python/docs/setup
* https://cloud.google.com/python/docs/getting-started
* https://cloud.google.com/python/docs/getting-started/background-processing
* https://docs.pytest.org/