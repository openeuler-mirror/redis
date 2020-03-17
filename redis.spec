Name:           redis
Version:        4.0.11
Release:        4
Summary:        A persistent key-value database
License:        BSD and MIT
URL:            https://redis.io
Source0:        http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:        %{name}.logrotate
Source2:        %{name}-sentinel.service
Source3:        %{name}.service

#CVE fix
Patch0001:      CVE-2019-10192.patch
#Optimization of the above problem
Patch0002:      cve-2019-10192.patch

%description
Redis is an advanced key-value store. It is often referred to as a dattructure server since keys can contain strings, hashes
,lists, sets anorted sets.

%prep
%autosetup -p1
sed -i -e 's|^logfile .*$|logfile /var/log/redis/redis.log|g' redis.conf
sed -i -e '$ alogfile /var/log/redis/sentinel.log' sentinel.conf
sed -i -e 's|^dir .*$|dir /var/lib/redis|g' redis.conf

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

%post
%systemd_post %{name}.service
%systemd_post %{name}-sentinel.service

%preun
%systemd_preun %{name}.service
%systemd_preun %{name}-sentinel.service

%postun
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-sentinel.service


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
* Tue Mar 17 2020 wangye <wangye54@huawei.com> - 4.0.11-4
- CVE fix

* Wed Jan 15 2020 zhujunhao <zhujunhao5@huawei.com> - 4.0.11-3
- Modify redis service

* Wed Jan 08 2020 lijin Yang <yanglijin@openeuler.org> - 4.0.11-2
- Package init

