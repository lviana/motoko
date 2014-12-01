%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:           mtktool
Version:        1.0
Release:        1%{?dist}
Summary:        Motoko command line interface

License:        ASL 2.0
URL:            https://github.com/lviana/motoko
Source0:        mtktool-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python

Requires:       python
Requires:       python-baker

%description
Command line interface for motoko service.
Responsible for smart servers management and resource control.

%prep
%setup -q -n mtktool

%build
echo -n

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%defattr(0755,root,root,-)
%{_bindir}/mtktool
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/motoko/mtktool.conf
%{python_sitelib}/*

%changelog
* Sat Mar 15 2014 Luiz Viana <luiz@include.io> - 1.0-1
- Initial release, compatible with motoko 1.0.x
