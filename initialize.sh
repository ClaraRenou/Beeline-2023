#!/bin/bash

# Building docker for the different algorithms 
echo "This may take a while..."

BASEDIR=$(pwd)

# You may remove the -q flag if you want to see the docker build status
cd $BASEDIR/Algorithms/ARBORETO
docker build -q -t arboreto:base .
if [[ "$(docker images -q arboreto:base 2> /dev/null)" != "" ]]; then
    echo "Docker container for ARBORETO is built and tagged as arboreto:base"
else
    echo "Oops! Unable to build Docker container for ARBORETO"
fi


cd $BASEDIR/Algorithms/PIDC/
docker build -q -t pidc:base .
if ([[ "$(docker images -q pidc:base 2> /dev/null)" != "" ]]); then
    echo "Docker container for PIDC is built and tagged as pidc:base"
else
    echo "Oops! Unable to build Docker container for PIDC"
fi


cd $BASEDIR/Algorithms/SCODE/
docker build -q -t scode:base .
if ([[ "$(docker images -q scode:base 2> /dev/null)" != "" ]]); then
    echo "Docker container for SCODE is built and tagged as scode:base"
else
    echo "Oops! Unable to build Docker container for SCODE"
fi


cd $BASEDIR/Algorithms/GRN-VAE/
docker build -q -t grnvae:base .
if ([[ "$(docker images -q grnvae:base 2> /dev/null)" != "" ]]); then
    echo "Docker container for GRNVAE is built and tagged as grnvae:base"
else
    echo "Oops! Unable to build Docker container for GRNVAE"
fi

cd $BASEDIR
