## package settings
%define consul_user    consul
%define consul_group   %{consul_user}
%define consul_home    %{_localstatedir}/lib/consul
%define consul_confdir %{_sysconfdir}/consul.d
%define debug_package  %{nil}

## docker check tool
%define check_docker_dist https://github.com/myENA/check_docker/releases/download/v3.0/check_docker-linux-3.0

Name:           consul
Version:        1.4.4
Release:        0%{?dist}
Summary:        Service discovery and configuration made easy.

Group:          System Environment/Daemons
License:        Mozilla Public License, version 2.0
URL:            http://www.consul.io

Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source2:        %{name}.service
Source3:        %{name}.sysconfig

BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

## Consul 0.9.0+ bundles the webui and no longer provides standalone files
Obsoletes:  %{name}-webui < 0.9.0

%description
Consul is a tool for service discovery and configuration.
Consul is distributed, highly available, and extremely scalable.

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons
Requires:   consul

%description config
Example configuration for %{name}.

%package services
Summary:    Common service definitions for %{name}
Group:      System Environment/Daemons
Requires:   consul

%description services
Example service definitions for %{name}.

%package checks
Summary:    Collection of check scripts for %{name}
Group:      System Environment/Daemons
Requires:   consul

%description checks
Check scripts suitable for execution by %{name}.

%prep
%setup -q -c

%build

%install
## directories
%{__install} -d -m 0750 %{buildroot}%{consul_home}/data
%{__install} -d -m 0750 %{buildroot}%{consul_home}/checks

## sytem files
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

## client configuration
for svc in %{_sourcedir}/consul-client-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/client/$(echo $(basename $svc)|sed s/consul-client-//)
done

## server configuration
for svc in %{_sourcedir}/consul-server-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/server/$(echo $(basename $svc)|sed s/consul-server-//)
done

## common configuration
for svc in %{_sourcedir}/consul-common-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/client/$(echo $(basename $svc)|sed s/consul-common-//)
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/server/$(echo $(basename $svc)|sed s/consul-common-//)
done

## service configuration
for svc in %{_sourcedir}/consul-service-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/service/$(echo $(basename $svc)|sed s/consul-service-//)
done

## main binary
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

## build passing test
echo 'building test passing check ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/pass
#!/bin/bash
echo "[OKAY] TEST"
exit 0
EOF

## build warning test
echo 'building test warning check ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/warn
#!/bin/bash
echo "[WARN] TEST"
exit 1
EOF

## build failing test
echo 'building test failing check ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/fail
#!/bin/bash
echo "[FAIL] TEST"
exit 2
EOF

## fetch docker check
curl -s -L -o %{buildroot}%{consul_home}/checks/docker %{check_docker_dist}

%pre
## add required user and group if needed
getent group %{consul_group} >/dev/null || \
	groupadd -r %{consul_group}
getent passwd %{consul_user} >/dev/null || \
	useradd -r -g %{consul_user} -d %{consul_home} \
	-s /sbin/nologin -c %{name} %{consul_user}
exit 0
## cleanup legacy 'bootstrap' configuration if present
if [ -d %{consul_confdir}/server/bootstrap ]; then
	rm -rf %{consul_confdir}/server/bootstrap
fi

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%attr(-,%{consul_user},%{consul_group}) %dir %{consul_home}/data

%files config
%defattr(0644,root,root,0755)
%dir %{consul_confdir}/client
%dir %{consul_confdir}/server
%config(noreplace) %{consul_confdir}/client/*
%config(noreplace) %{consul_confdir}/server/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files services
%defattr(0644,root,root,0755)
%dir %{consul_confdir}/service
%config(noreplace) %{consul_confdir}/service/*

%files checks
%defattr(0755,root,root,0755)
%dir %{consul_home}/checks
%{consul_home}/checks/*

%changelog
