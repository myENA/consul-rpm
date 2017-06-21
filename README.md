# RPM Spec for Consul

Originally forked from [CiscoCloud/consul-rpm](https://github.com/CiscoCloud/consul-rpm) and modified for the ENA environment.

# Building

If you have Vagrant installed:

* Check out this repo.
    ```
    git clone https://github.com/myENA/consul-rpm
    ```

* Add or update the official CentOS 7 boxfile in your vagrant environment.

Add the box:
    ```
    vagrant box add centos/7
    ```

Update the box:
    ```
    vagrant box update --box centos/7
    ```

* Vagrant up! The rpms will be copied to working directory after provisioning.
    ```
    vagrant up
    ```

Or, do it manually by building the RPM as a non-root user from your home directory:

* Check out this repo. Seriously - check it out. Nice.
    ```
    git clone https://github.com/myENA/consul-rpm
    ```

* Install `rpmdevtools` and `mock`.
    ```
    sudo yum install rpmdevtools mock
    ```

* Set up your rpmbuild directory tree.
    ```
    rpmdev-setuptree
    ```

* Link the spec file and sources.
    ```
    ln -sf $HOME/consul-rpm/SPECS/consul.spec $HOME/rpmbuild/SPECS/
    find $HOME/consul-rpm/SOURCES -type f -exec ln -sf {} $HOME/rpmbuild/SOURCES/ \;
    ```

* Download remote source files.
    ```
    spectool -g -R rpmbuild/SPECS/consul.spec
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/consul.spec
    ```

## Result

Five RPMs will be copied to `./artifacts/`:
* `consul-<version>-<release>.rpm`          - The binary and systemd service definition
* `consul-checks-<version>-<release>.rpm`   - Example check scripts
* `consul-config-<version>-<release>.rpm`   - Example agent configuration
* `consul-services-<version>-<release>.rpm` - Example service definitions
* `consul-webui-<version>-<release>.rpm`    - The web ui files for modification if desired (latest Consul bundles these in the binary)

# Running

* Install the RPM(s) - the consul binary package and configuration are recommended at a minimum
* Review and edit (if needed) `/etc/sysconfig/consul` and associated config under `/etc/consul.d/*` (config package)
* Start the service and tail the logs: `systemctl start consul.service` and `journalctl -f --no-pager -u consul`
* Optionally start on reboot with: `systemctl enable consul.service`

## Config

Config files are loaded in lexicographical order from the `config-dir` specified in `/etc/sysconfig/consul` (config package).
You may modify and/or add to the provided configuration as needed.

# More info

See the [consul.io](http://www.consul.io) website.
