Name: my-nagios-plugins
Version: {{{ git_version }}}
Release: 1%{?dist}
Summary: Custom Nagios plugins

License: GPL
URL: https://lab.d3s.mff.cuni.cz/nagios-plugins/
VCS: {{{ git_vcs }}}

Requires: python3
Requires: python3-setuptools

%description
Blab blah


%global debug_package %{nil}

%prep
{{{ git_setup_macro }}}

%build
python3 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
