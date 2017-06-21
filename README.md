# RPM Spec for Consul

Originally forked from [CiscoCloud/consul-rpm](https://github.com/CiscoCloud/consul-rpm) and modified for the ENA environment.

# Building

The RPMs may be built with [Docker](#with-docker), [Vagrant](#with-vagrant), or [manual](#manual).

Whatever way you choose you will need to do a few basic things first.

```bash
git clone https://github.com/myENA/consul-rpm  ## check out this code
cd consul-rpm                                  ## uhh... you should know
mkdir -p artifacts                             ## prep the artifacts location
```

## With Docker

```bash
docker build -t ena/consul-rpm .                                ## build the image
docker run -v $PWD/artifacts:/tmp/artifacts -it ena/consul-rpm  ## run the image and build the RPMs
```

## With Vagrant

```bash
vagrant box add centos/7           ## add the official CentOS 7 box
vagrant box update --box centos/7  ## or update if you already have it
vagrant up                         ## provision and build the RPMs
```

## Manual

```bash
cat build.sh     ## read the script
```

## Result

Five RPMs will be copied to the `artifacts` folder:
1. `consul-<version>-<release>.rpm`          - The binary and systemd service definition (required)
2. `consul-checks-<version>-<release>.rpm`   - Example check scripts (optional)
3. `consul-config-<version>-<release>.rpm`   - Example agent configuration (recommended)
4. `consul-services-<version>-<release>.rpm` - Example service definitions (optional)
5. `consul-webui-<version>-<release>.rpm`    - Web UI files (optional - latest consul includes these in binary)

# Running

1. Install the RPM(s) that you need
2. Review and edit (if needed) `/etc/sysconfig/consul` and associated config under `/etc/consul.d/*` (config package)
3. Start the service and tail the logs: `systemctl start consul.service` and `journalctl -f --no-pager -u consul`
4. Optionally start on reboot with: `systemctl enable consul.service`

## Configuring

Config files are loaded in lexicographical order from the `config-dir` specified in `/etc/sysconfig/consul` (config package).
You may modify and/or add to the provided configuration as needed.

# Further reading

See the [consul.io](http://www.consul.io) website.
