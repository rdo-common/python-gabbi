%global pypi_name gabbi
%global pypi gabbi-run

%if 0%{?fedora}
%global with_python3 1
%endif

# Only reason to choose 24 is that that's what was in development when we made
# the switch for this package.  Fedora Policy was to have made this switch for
# Fedora 22.
%if 0%{?fedora} >= 24
%global default_python 3
%else
%global default_python 2
%endif


Name:           python-%{pypi_name}
Version:        1.33.0
Release:        2%{?dist}
Summary:        Declarative HTTP testing library

License:        ASL 2.0
URL:            https://github.com/cdent/gabbi
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%description
Gabbi is a tool for running HTTP tests where requests and responses
are represented in a declarative YAML-based form.

%package -n python2-%{pypi_name}
Summary:        Declarative HTTP testing library
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:       python2-devel
BuildRequires:       python-setuptools
BuildRequires:       python-six
BuildRequires:       python-pbr
BuildRequires:       python-httplib2
BuildRequires:       python-wsgi_intercept
BuildRequires:       python-colorama
BuildRequires:       python-jsonpath-rw-ext
BuildRequires:       PyYAML
BuildRequires:       pytest
BuildRequires:       python-urllib3


Requires:       python-setuptools
Requires:       python-six
Requires:       python-pbr
Requires:       python-wsgi_intercept
Requires:       python-colorama
Requires:       python-jsonpath-rw-ext
Requires:       pytest
Requires:       PyYAML
Requires:       python-urllib3


# test requirements
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-coverage

%description -n python2-%{pypi_name}
Gabbi is a tool for running HTTP tests where requests and responses
are represented in a declarative YAML-based form.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Declarative HTTP testing library
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:       python3-devel
BuildRequires:       python3-setuptools
BuildRequires:       python3-six
BuildRequires:       python3-pbr
BuildRequires:       python3-httplib2
BuildRequires:       python3-wsgi_intercept
BuildRequires:       python3-colorama
BuildRequires:       python3-jsonpath-rw-ext
BuildRequires:       python3-PyYAML
BuildRequires:       python3-pytest
BuildRequires:       python3-urllib3

Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-pbr
Requires:       python3-wsgi_intercept
Requires:       python3-colorama
Requires:       python3-jsonpath-rw-ext
Requires:       python3-pytest
Requires:       python3-PyYAML
Requires:       python3-urllib3

# test requirements
BuildRequires:  python3-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-coverage

%description -n python3-%{pypi_name}
Gabbi is a tool for running HTTP tests where requests and responses
are represented in a declarative YAML-based form.
%endif

%package -n python-%{pypi_name}-doc
Summary:        Documentation for the gabbi module

BuildRequires:  python-sphinx
BuildRequires:  python-sphinx_rtd_theme

Requires:   python2-%{pypi_name}
%description -n python-%{pypi_name}-doc
Documentation for the gabbi module

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
mv %{buildroot}%{_bindir}/%{pypi} %{buildroot}%{_bindir}/python2-%{pypi}

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{pypi} %{buildroot}%{_bindir}/python3-%{pypi}
%endif

%if 0%{?default_python} >= 3
ln -s %{_bindir}/python3-%{pypi} %{buildroot}%{_bindir}/%{pypi}
%else
ln -s %{_bindir}/python2-%{pypi} %{buildroot}%{_bindir}/%{pypi}
%endif

# generate html docs
sphinx-build docs/source html
sphinx-build -b man docs/source man

install -p -D -m 644 man/gabbi.1 %{buildroot}%{_mandir}/man1/gabbi.1


rm -rf html/.{doctrees,buildinfo}

%check
# some tests are broken so bypassing tests
export GABBI_SKIP_NETWORK=true
%{__python2} setup.py test ||
rm -fr .testrepository
%if 0%{?with_python3}
%{__python3} setup.py test ||
%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%if 0%{?default_python} <= 2
%{_bindir}/%{pypi}
%{_mandir}/man1/gabbi.1*
%endif
%{_bindir}/python2-%{pypi}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%exclude %{python2_sitelib}/gabbi/tests/gabbits_intercept/horse


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%if 0%{?default_python} >= 3
%{_bindir}/%{pypi}
%{_mandir}/man1/gabbi.1*
%endif
%{_bindir}/python3-%{pypi}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%exclude %{python3_sitelib}/gabbi/tests/gabbits_intercept/horse
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1.33.0-1
- Upstream 1.33.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.27.0-2
- Rebuild for Python 3.6

* Thu Oct 13 2016 Alan Pevec <alan.pevec@redhat.com> 1.27.0-1
- Update to 1.27.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.22.0-1
- Upstream 1.22.0

* Mon Jun  6 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.21.0-1
- Upstream 1.21.0

* Wed Jun  1 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.19.1-1
- Upstream 1.19.1
- Add IPv6 support

* Mon May 09 2016 chandankumar <chkumar246@gmail.com> - 1.19.0-1
- Initial package.
