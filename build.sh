#!/usr/bin/env bash
set -ex  ## we like things verbose

## ensure we have a full dev stack
sudo yum groupinstall -y "Development Tools"

## install other helpers
sudo yum install -y epel-release mock rpmdevtools rpm-devel

## setup our build path
rpmdev-setuptree

## link the specs
ln -sf /tmp/build/SPECS/*.spec $HOME/rpmbuild/SPECS/

## link the sources
find /tmp/build/SOURCES -type f -exec ln -sf {} $HOME/rpmbuild/SOURCES/ \;

## download sources
for spec in $HOME/rpmbuild/SPECS/*.spec; do
    spectool -g -R $spec
done

## build packages
rpmbuild -ba $HOME/rpmbuild/SPECS/*.spec

## copy built files out of the vagrant/docker environment
## skip if you are doing this manually
if [ -f /.dockerenv ] || [ -f /.doing_the_vagrant ]; then
    sudo cp -f $HOME/rpmbuild/RPMS/*/*.rpm /tmp/artifacts/ || true
    sudo cp -f $HOME/rpmbuild/SRPMS/*.rpm /tmp/artifacts/ || true
fi
