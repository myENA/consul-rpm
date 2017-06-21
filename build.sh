#!/usr/bin/env bash
set -ex
sudo yum install -y rpmdevtools rpm-devel rpm-build mock
rpmdev-setuptree
ln -sf /tmp/build/SPECS/consul.spec $HOME/rpmbuild/SPECS/
find /tmp/build/SOURCES -type f -exec ln -sf {} $HOME/rpmbuild/SOURCES \;
spectool -g -R $HOME/rpmbuild/SPECS/consul.spec
rpmbuild -ba $HOME/rpmbuild/SPECS/consul.spec
mkdir -p /tmp/artifacts
sudo cp -f $HOME/rpmbuild/RPMS/x86_64/consul*.rpm /tmp/artifacts/
