#!/bin/sh
. ./n.sh


VERSION=$(cat version)
increment_version $VERSION > version
VERSION=$(cat version)

gitpush