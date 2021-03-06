%global srcname pyspotify

Name:           python-%{srcname}
Version:        2.1.2
Release:        7%{?dist}
Summary:        Python bindings for libspotify

License:        ASL 2.0
URL:            https://pyspotify.mopidy.com/
Source0:        %{pypi_source pyspotify}

ExclusiveArch:  i686 x86_64 armv7hl

%global _description %{expand:
pyspotify provides a Python interface to Spotify's online music streaming
service.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  libspotify-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-invoke
BuildRequires:  python3-setuptools
Requires:       python3-cffi
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%package doc
BuildRequires:  python3-mock
BuildRequires:  python3-sphinx
Summary:        Documentation for pyspotify
BuildArch:      noarch

%description doc
Documentation for pyspotify, the Python bindings for libspotify.


%prep
%autosetup -n %{srcname}-%{version}
rm spotify/api.processed.h
# overwriting upstream's manifest as it includes a lot of files we do not want,
# and we need some additional excludes as well
cat > MANIFEST.in <<-'EOF'
  exclude spotify/api.h
  exclude spotify/api.processed.h
  exclude spotify/_spotify_build.py
EOF

%build
# regenerate api.processed.h before attempting to build the module (note: this
# prints errors, even though everything worked fine)
invoke3 preprocess-header
%py3_build

cd docs
make SPHINXBUILD=sphinx-build-3 html
rm _build/html/.buildinfo

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{srcname}-*.egg-info/
%{python3_sitearch}/spotify/

%files doc
%doc docs/_build/html


%changelog
* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 2.1.2-7
- Rebuild for python-3.10

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 2.1.2-4
- Rebuild for python-3.9

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 2.1.2-3
- Rebuild for python-3.9

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild


* Sun Dec 22 2019 Tobias Girstmair <t-rpmfusion@girst.at> - 2.1.2-1
- Initial release
