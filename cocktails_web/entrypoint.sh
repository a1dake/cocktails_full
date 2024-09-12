#!/bin/sh
SOURCE_DIR="/frontend"
CACHE_DIR="/frontend_build"

if [ ! -d "$SOURCE_DIR/node_modules" ]; then
    echo "Copy node_modules folder to host machine..."
    cp -r $CACHE_DIR/node_modules $SOURCE_DIR
else
    echo "Do not copy: node_modules folder exists on host machine"
fi

chown -R node:node $SOURCE_DIR/node_modules

if [ "$LOAD_ENV" = "true" ]; then
    echo "Loading given environment variables into $ENV_FILE file"
    load_env $ENV_FILE "$ENV_VARS"
    echo "Completed"
fi

if [ -z "$DEBUG" ] || [ ! "$DEBUG" = "true" ]; then
    exec npm run build
else
    exec npm run serve
fi
