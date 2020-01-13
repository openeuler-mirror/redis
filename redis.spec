Name:           redis
Version:        4.0.11
Release:        2
Summary:        A persistent key-value database
License:        BSD and MIT
URL:            https://redis.io
Source0:        http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:        %{name}.logrotate
Source2:        %{name}-sentinel.service
Source3:        %{name}.service

%description
Redis is an advanced key-value store. It is often referred to as a dattructure server since keys can contain strings, hashes
,lists, sets anorted sets.

%prep
%autosetup -p1

%build
make

%install
%make_install PREFIX=%{buildroot}%{_prefix}
install -pDm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
mkdir -p %{buildroot}%{_unitdir}
install -pm644 %{SOURCE2} %{buildroot}%{_unitdir}
install -pm644 %{SOURCE3} %{buildroot}%{_unitdir}
install -pDm640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -pDm640 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}-sentinel.conf

%check
make test

%files
%license COPYING
%doc BUGS README.md 00-RELEASENOTES MANIFESTO CONTRIBUTING
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0640, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0640, redis, root) %config(noreplace) %{_sysconfdir}/%{name}-sentinel.conf
%{_bindir}/%{name}-*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service

%changelog
* Wed Jan 08 2020 lijin Yang <yanglijin@openeuler.org> - 4.0.11-2
- Package init

