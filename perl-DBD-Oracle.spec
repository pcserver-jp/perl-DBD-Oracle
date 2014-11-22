%define name perl-DBD-Oracle
%define pkgname %(echo %{name}| sed 's/perl-//')
%{!?version:%define version 1.74}
%{!?oi_ver:%define oi_ver instantclient11.2}
%{!?oi_release:%define oi_release 11.2.0.4.0}
%define release %{oi_release}%{dist}
%define perl_vendorarch %(eval "$(%{__perl} -V:installvendorarch)"; echo $installvendorarch)
%define _use_internal_dependency_generator 0
%define custom_find_req %{_tmppath}/%{pkgname}-%{version}-find-requires
%define __find_requires %{custom_find_req}
%define __perl_requires %{custom_find_req}

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   DBD-Oracle - Oracle database driver for the DBI module
Group:     Development/Libraries
Vendor:    Tim Bunce <timb@cpan.org>, John Scoles <byterock@cpan.org>, Yanick Champoux <yanick@cpan.org>, Martin J. Evans <mjevans@cpan.org>
Packager:  dba@ha <hamada@pc-office.net>
License:   GPL+ or Artistic
URL:       https://github.com/pythian/DBD-Oracle
Source0:   %{pkgname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/perl-DBD-Oracle-buildroot/
Requires:  libaio
Requires:  perl(:MODULE_COMPAT_%(eval "$(%{__perl} -V:version)"; echo $version))
Requires:  perl(ExtUtils::MakeMaker) >= 6.30
Requires:  perl(DBI) >= 1.51
Requires:  oracle-%{oi_ver}-basic = %{oi_release}
BuildRequires: oracle-%{oi_ver}-devel = %{oi_release}
BuildRequires: oracle-%{oi_ver}-sqlplus = %{oi_release}
Provides:  perl(DBD-Oracle) = %{version}

%description
DBD::Oracle is a Perl module which works with the DBI module to provide
access to Oracle databases.
This documentation describes driver specific behaviour and restrictions.
It is not supposed to be used as the only reference for the user.
In any case consult the DBI documentation first!

%prep
%setup -q -n %{pkgname}-%{version}
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
export ORACLE_HOME=$(dirname $(dirname $(rpm -ql oracle-%{oi_ver}-sqlplus | grep '/usr/lib/oracle/.*/sqlplus')))
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
MKFILE=$(rpm -ql oracle-%{oi_ver}-devel | grep demo.mk)
%{__perl} Makefile.PL -m $MKFILE INSTALLDIRS="vendor" PREFIX=%{_prefix} -V %{oi_release}
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cat << 'EOF' > %{custom_find_req}
#!/bin/sh
/usr/lib/rpm/redhat/find-requires | grep -v -e 'libclntsh.so.10.1' -e 'libocci.so.10.1' -e 'libclntsh.so.11.1' -e 'libocci.so.11.1' -e 'libclntsh.so.12.1' -e 'libocci.so.12.1'
EOF
chmod 755 %{custom_find_req}
%{__make} PREFIX=$RPM_BUILD_ROOT%{_prefix} pure_install
rm -f $(find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
rm -f %{custom_find_req}

%files
%defattr(-,root,root)
%defattr(-,root,root)
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Fri Nov 21 2014 dba@ha <hamada@pc-office.net>
- Initial build.
