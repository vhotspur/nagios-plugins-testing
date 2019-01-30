Name: my-nagios-plugins
Version: 0.1
Release: 1%{?dist}
Summary: Custom Nagios plugins

License: GPL
URL: https://lab.d3s.mff.cuni.cz/nagios-plugins/
VCS: {{{ git_vcs }}}
Source: {{{ git_pack }}}

BuildRequires: python3
BuildRequires: python3-setuptools
Requires: python3

%description
Blab blah


%global debug_package %{nil}

%prep
{{{ git_setup_macro }}}

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT
%py3_install --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
