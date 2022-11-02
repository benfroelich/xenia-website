export SECRET_KEY=$(<.secret_key)
export DJANGO_PG_PASS=$(<.my_pgpass)
export AWS_S3_ACCESS_KEY_ID=$(<.s3_access_key)
export AWS_S3_SECRET_ACCESS_KEY=$(<.s3_secret_access_key)
