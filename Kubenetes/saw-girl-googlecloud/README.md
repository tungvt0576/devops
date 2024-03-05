create configmap-be
kubectl create configmap saw-girl-be-config --from-env-file=backend.env


Nội dung backend.env
PORT=8888
MONGODB_URL=mongodb://mongo-db:27017/amonyos

FACEBOOK_APP_ID=1028685518132915
FACEBOOK_APP_SECRET=fc9d58a0f55da3f5ecafb7fdc4b2063e
CALLBACK_FACEBOOK_URL=http://saw-girl-be-svc:8888/v1/auth/facebook/callback

GOOGLE_CLIENT_ID="700651331760-q329rkrpgr8o5634pr1bg029r226fpqm.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="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"
CALLBACK_GOOGLE_URL=http://saw-girl-be-svc:8888/v1/auth/google/callback

FRONTEND_URL=http://saw-girl-fe-svc:8090/questions
SESSION_SECRET=tung