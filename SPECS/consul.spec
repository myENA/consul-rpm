## package settings
%define consul_user    consul
%define consul_group   %{consul_user}
%define consul_home    %{_localstatedir}/lib/consul
%define consul_confdir %{_sysconfdir}/consul.d
%define debug_package  %{nil}

## docker check tool
%define check_docker_dist https://github.com/newrelic/check_docker/releases/download/v2.3/check_docker-linux-2.3

Name:           consul
Version:        0.8.4
Release:        1%{?dist}
Summary:        Service discovery and configuration made easy.

Group:          System Environment/Daemons
License:        Mozilla Public License, version 2.0
URL:            http://www.consul.io

Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_web_ui.zip
Source2:        %{name}.service
Source3:        %{name}.sysconfig

BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

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

%package webui
Summary:    Web UI files for %{name}
Group:      System Environment/Daemons
Requires:   consul

%description webui
Web UI distribution files for %{name}.

%prep
%setup -q -c

%build

%install
## directories
%{__install} -d -m 0750 %{buildroot}%{consul_home}/data
%{__install} -d -m 0750 %{buildroot}%{consul_home}/ssl
%{__install} -d -m 0750 %{buildroot}%{consul_home}/dist
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

## bootstrap configuration
for svc in %{_sourcedir}/consul-bootstrap-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/bootstrap/$(echo $(basename $svc)|sed s/consul-bootstrap-//)
done

## common configuration
for svc in %{_sourcedir}/consul-common-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/client/$(echo $(basename $svc)|sed s/consul-common-//)
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/server/$(echo $(basename $svc)|sed s/consul-common-//)
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/bootstrap/$(echo $(basename $svc)|sed s/consul-common-//)
done

## service configuration
for svc in %{_sourcedir}/consul-service-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{consul_confdir}/service/$(echo $(basename $svc)|sed s/consul-service-//)
done

## main binary
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

## extract web ui files
unzip %{SOURCE1} -d %{buildroot}%{consul_home}/dist -x '*.git*'

## build passing test
echo 'building test_pass ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/test_pass
#!/bin/bash
echo "[OKAY] TEST"
exit 0
EOF

## build warning test
echo 'building test_warn ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/test_warn
#!/bin/bash
echo "[WARN] TEST"
exit 1
EOF

## build failing test
echo 'building test_fail ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/test_fail
#!/bin/bash
echo "[FAIL] TEST"
exit 2
EOF

## generic tcp port check
echo 'building check_tcp ...' > /dev/stderr
cat << EOF > %{buildroot}%{consul_home}/checks/check_tcp
#!/bin/bash
echo "[DEPRECATED] Please use the 'tcp' check"
exit 1
EOF

## fetch docker check
curl -s -L -o %{buildroot}%{consul_home}/checks/check_docker %{check_docker_dist}

%pre
getent group %{consul_group} >/dev/null || \
    groupadd -r %{consul_group}
getent passwd %{consul_user} >/dev/null || \
    useradd -r -g %{consul_user} -d %{consul_home} \
    -s /sbin/nologin -c %{name} %{consul_user}
exit 0

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
%defattr(-,root,root,-)
%dir %{consul_confdir}/bootstrap
%dir %{consul_confdir}/client
%dir %{consul_confdir}/server
%config(noreplace) %{consul_confdir}/bootstrap/*
%config(noreplace) %{consul_confdir}/client/*
%config(noreplace) %{consul_confdir}/server/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files services
%defattr(-,root,root,-)
%dir %{consul_confdir}/service
%config(noreplace) %{consul_confdir}/service/*

%files checks
%defattr(-,root,root,-)
%dir %{consul_home}/checks
%attr(0755,root,root) %{consul_home}/checks/*

%files webui
%defattr(-,root,root,-)
%dir %{consul_home}/dist
%{consul_home}/dist/*

%changelog
