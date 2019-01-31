Name: Name: {{{ git_name name="my-nagios-plugins" }}}
Version: 0.1
Release: 1%{?dist}
Summary: Custom Nagios plugins

License: GPL
URL: https://lab.d3s.mff.cuni.cz/nagios-plugins/
VCS: {{{ git_vcs }}}
Source: {{{ git_pack }}}

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3

%description
Blab blah


%global debug_package %{nil}

%prep
%setup

%build
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
