~/google-cloud-sdk/bin/gcloud config set project getting-started-337714

export GOOGLE_CLOUD_PROJECT=getting-started-337714

pip3 install -r requirements.txt --user   

~/Library/Python/3.10/bin/gunicorn -b :8080 main:app

~/google-cloud-sdk/bin/gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/bookshelf .

~/google-cloud-sdk/bin/gcloud run deploy bookshelf --image gcr.io/$GOOGLE_CLOUD_PROJECT/bookshelf --platform managed --region us-central1 --allow-unauthenticated --set-env-vars=GOOGLE_CLOUD_PROJECT=getting-started-337714 

~/google-cloud-sdk/bin/gcloud app deploy