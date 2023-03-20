#!/bin/sh

echo "starting frontend server"

npm run dev

exec "$@"