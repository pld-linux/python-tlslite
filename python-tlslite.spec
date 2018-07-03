#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module		tlslite
%define	egg_name	tlslite
Summary:	Open source Python library that implements SSL and TLS
Name:		python-%{module}
Version:	0.4.9
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/t/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	9f3b3797f595dd66cd36a65c83a87869
URL:		http://trevp.net/tlslite
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 3.2
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLS Lite is an open source Python library that implements SSL and TLS.
TLS Lite supports RSA and SRP cipher suites. TLS Lite is pure Python,
however it can use other libraries for faster crypto operations. TLS
Lite integrates with several stdlib networking libraries.

%package -n python3-%{module}
Summary:	Open source Python library that implements SSL and TLS
Group:		Libraries/Python

%description -n python3-%{module}
TLS Lite is an open source Python library that implements SSL and TLS.
TLS Lite supports RSA and SRP cipher suites. TLS Lite is pure Python,
however it can use other libraries for faster crypto operations. TLS
Lite integrates with several stdlib networking libraries.

%prep
%setup -q -n %{module}-%{version}

chmod a-x README

# and remove their executable permission so that they don't drag in more
# dependencies, and lint doesn't throw a warning
chmod -x scripts/tls*.py

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif
%if %{with python2}
%py3_install
%endif

# scripts are of limited usefulness, put them only in docs
rm $RPM_BUILD_ROOT%{_bindir}/tls*.py

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README LICENSE scripts/tls*.py
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README LICENSE scripts/tls*.py
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
