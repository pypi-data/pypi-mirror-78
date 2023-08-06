#!/bin/sh

MAJOR_MINOR="2.10"

pip install --user antsibull
git clone git@github.com:ansible-community/ansible-build-data
mkdir built
BUILD_DATA_DIR="ansible-build-data/${MAJOR_MINOR}"
if test -e "${BUILD_DATA_DIR}/ansible-${MAJOR_MINOR}.build" ; then
  BUILDFILE="ansible-${MAJOR_MINOR}.build"
else
  BUILDFILE="acd-${MAJOR_MINOR}.build"
fi
antsibull-build rebuild-single "2.10.0b2" --build-data-dir "${BUILD_DATA_DIR}" --build-file "$BUILDFILE" --dest-dir built

#pip install twine
#twine upload "built/ansible-2.10.0b2.tar.gz"