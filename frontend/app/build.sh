#!/bin/bash

npm run build

dest="../../backend/flask-app/app/app"
rm -rf "$dest/dist"
mv dist "$dest"
