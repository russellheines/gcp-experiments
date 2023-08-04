# gcp-experiments

## Commands

```
$ python3 -m venv env
$ source env/bin/activate
$ pytest
$ gcloud pubsub topics create alphabeta-topic
$ gcloud functions deploy alphabeta-function --gen2 --runtime=python311 --region=us-central1 --source=. --entry-point=subscribe --trigger-topic=alphabeta-topic
$ export GOOGLE_CLOUD_PROJECT=getting-started-337714  
$ python main.py "{'gameId': '26f9debf-ba31-40a2-b698-c45607030444', 'color': '0'}"
```

## Links

* https://cloud.google.com/python/docs/setup
* https://cloud.google.com/python/docs/getting-started
* https://cloud.google.com/python/docs/getting-started/background-processing
* https://cloud.google.com/functions/docs/console-quickstart
* https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library