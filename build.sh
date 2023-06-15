#!/usr/bin/env bash
set -e
latest=true
name="hanifan/bokeh"
for version in 1.0.0; do
    tag="-t ${name}:$version";

    if [ ${latest} = true ] ; then
        tag="${tag} -t ${name}:latest";
    fi
    docker build --build-arg VERSION=${version} docker ${tag};

    latest=false;
done
