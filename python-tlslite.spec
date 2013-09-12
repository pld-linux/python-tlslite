# Conditional build:
%bcond_without  python2         # build python 2 module
%bcond_without  python3         # build python 3 module
#
%define 	module	tlslite
Summary:	Open source python library that implements SSL and TLS
Name:		python-%{module}
Version:	0.4.6
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/t/tlslite/%{module}-%{version}.tar.gz
# Source0-md5:	2f92ebea557802969653f29c7faafbc2
URL:		https://pypi.python.org/pypi/tlslite
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	python-modules >= 1:2.6
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules >= 3.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLS Lite is an open source python library that implements SSL and TLS.
TLS Lite supports RSA and SRP ciphersuites. TLS Lite is pure python,
however it can use other libraries for faster crypto operations. TLS
Lite integrates with several stdlib neworking libraries.

%package -n python3-tlslite
Summary:	Open source python library that implements SSL and TLS
Group:		Development/Languages/Python

%description -n python3-tlslite
TLS Lite is an open source python library that implements SSL and TLS.
TLS Lite supports RSA and SRP ciphersuites. TLS Lite is pure python,
however it can use other libraries for faster crypto operations. TLS
Lite integrates with several stdlib neworking libraries.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%{__python} setup.py build -b py2
%endif

%if %{with python3}
%{__python3} setup.py build -b py3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build -b py2 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py  \
	build -b py3 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%{__rm} -rf $RPM_BUILD_ROOT{%{py_sitescriptdir},%{py3_sitescriptdir}}/%{module}/{cacert.pem,packages}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README docs
%attr(755,root,root) %{_bindir}/tls.py
%attr(755,root,root) %{_bindir}/tlsdb.py
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-tlslite
%defattr(644,root,root,755)
%doc README docs
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
