Name:           redis
Version:        4.0.11
Release:        16
Summary:        A persistent key-value database
License:        BSD and MIT
URL:            https://redis.io
Source0:        http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:        %{name}.logrotate
Source2:        %{name}-sentinel.service
Source3:        %{name}.service

#CVE fix
Patch0001:      CVE-2019-10192-1.patch
#Optimization of the above problem
Patch0002:      CVE-2019-10192-2.patch
Patch0003:      CVE-2020-14147.patch 
Patch0004:      improved-HyperLogLog-cardinality-estimation.patch
Patch0005:      Aesthetic-changes-to-PR.patch
Patch0006:      CVE-2019-10193.patch
Patch0007:      modify-aarch64-architecture-jemalloc-page-size-from-4k-to-64k.patch
Patch0008:      huawei-deps-jemalloc-support-riscv.patch
Patch0009:      CVE-2021-21309.patch
Patch0010:      CVE-2021-3470.patch
BuildRequires:     systemd gcc
Requires:          /bin/awk
Requires:          logrotate
Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
Redis is an advanced key-value store. It is often referred to as a dattructure server since keys can contain strings, hashes
,lists, sets anorted sets.

%prep
%setup
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%ifarch aarch64
%patch0007 -p1
%endif
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1

sed -i -e 's|^logfile .*$|logfile /var/log/redis/redis.log|g' redis.conf
sed -i -e '$ alogfile /var/log/redis/sentinel.log' sentinel.conf
sed -i -e 's|^dir .*$|dir /var/lib/redis|g' redis.conf

%build
make

%install
%make_install PREFIX=%{buildroot}%{_prefix}
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/run/%{name}
install -d %{buildroot}%{_libdir}/%{name}/modules
install -pDm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
mkdir -p %{buildroot}%{_unitdir}
install -pm644 %{SOURCE2} %{buildroot}%{_unitdir}
install -pm644 %{SOURCE3} %{buildroot}%{_unitdir}
install -pDm640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -pDm640 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}-sentinel.conf

%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null
exit 0

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
%dir %attr(0750, redis, redis) %{_libdir}/%{name}
%dir %attr(0750, redis, redis) %{_libdir}/%{name}/modules
%dir %attr(0750, redis, redis) %{_sharedstatedir}/%{name}
%dir %attr(0750, redis, redis) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}-*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service

%changelog
* Mon May 31 2021 huanghaitao <huanghaitao8@huawei.com> - 4.0.11-16
- Completing build dependencies to fix gcc compiler missing error

* Wed Apr 07 2021 wangyue <wangyue92@huawei.com> - 4.0.11-15
- Fix CVE-2021-3470

* Wed Mar 24 2021 sunguoshuai <sunguoshuai@huawei.com> - 4.0.11-14
- change patch file in order src.rpm is same in aarch64 and x86_64
 
* Thu Mar 11 2021 wangxiao <wangxiao65@huawei.com> - 4.0.11-13
- Fix CVE-2021-21309

* Wed Nov 11 2020 yangyanchao <yangyanchao6@huawei.com> - 4.0.11-12
- enable dependency package jemalloc of redis to support riscv 

* Wed Sep 30 2020 Jiapeng Zhang <zhangjiapeng9@huawei.com> - 4.0.11-11
- Modify aarch64 architecture jemalloc page size from 4k to 64k

* Mon Sep 21 2020 wangyue <wangyue92@huawei.com> - 4.0.11-10
- fix CVE-2019-10193

* Mon Jul 20 2020 wangxiao <wangxiao654@huawei.com> - 4.0.11-9
- fix CVE-2020-14147

* Fri Jun 19 2020 Captain Wei <captain.a.wei@gmail.com> - 4.0.11-8
- Add some dependency package in building and running phase

* Fri Jun 12 2020 panchenbo <panchenbo@uniontech.com> - 4.0.11-7
- Type:bugfix
- ID: NA
- SUG: restart
- DESC: Resolve service startup failure whthout no %pre

* Mon Jun 01 2020 huanghaitao <huanghaitao8@huawei.com> - 4.0.11-6
- Resolve service startup failure
 
* Tue Mar 17 2020 wangye <wangye54@huawei.com> - 4.0.11-5
- CVE name fix

* Tue Mar 17 2020 wangye <wangye54@huawei.com> - 4.0.11-4
- CVE fix

* Wed Jan 15 2020 zhujunhao <zhujunhao5@huawei.com> - 4.0.11-3
- Modify redis service

* Wed Jan 08 2020 lijin Yang <yanglijin@openeuler.org> - 4.0.11-2
- Package init

