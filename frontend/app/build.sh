#!/bin/bash

npm run build

dest="../../backend/flask-app/app"
rm -rf "$dest/dist"
mv dist "$dest"
