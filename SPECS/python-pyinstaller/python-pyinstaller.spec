%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        PyInstaller bundles a Python application and all its dependencies into a single package.
Name:           python-pyinstaller
Version:        3.2.1
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/PyInstaller/3.2.1
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/P/PyInstaller/PyInstaller-%{version}.tar.bz2
%define sha1    PyInstaller=6e8bc52d325a5527402ad574f774ed64c70bf03f
Patch0:         python2-unit-tests.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-six
BuildRequires:  python-pytest
BuildRequires:  python-psutil
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-xml

%description
PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
PyInstaller reads a Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute. Then it collects copies of all those files – including the active Python interpreter! – and puts them with your script in a single folder, or optionally in a single executable file.

PyInstaller is tested against Windows, Mac OS X, and Linux. However, it is not a cross-compiler: to make a Windows app you run PyInstaller in Windows; to make a Linux app you run it in Linux, etc. PyInstaller has been used successfully with AIX, Solaris, and FreeBSD, but is not tested against them.
%package -n     python3-pyinstaller
Summary:        Python 3 version
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  zlib-devel
%if %{with_check}
BuildRequires:  python3-pytest
%endif
Requires:       python3
Requires:       python3-libs
Requires:       zlib
Requires:       python3-setuptools
Requires:       python3-xml

%description -n python3-pyinstaller
Python 3 version.

%prep
%setup -q -n PyInstaller-%{version}

rm -rf ../p3dir
cp -a . ../p3dir
%patch0 -p1

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pyi-archive_viewer %{buildroot}/%{_bindir}/pyi-archive_viewer3
mv %{buildroot}/%{_bindir}/pyi-bindepend      %{buildroot}/%{_bindir}/pyi-bindepend3
mv %{buildroot}/%{_bindir}/pyi-grab_version   %{buildroot}/%{_bindir}/pyi-grab_version3
mv %{buildroot}/%{_bindir}/pyi-makespec       %{buildroot}/%{_bindir}/pyi-makespec3
mv %{buildroot}/%{_bindir}/pyi-set_version    %{buildroot}/%{_bindir}/pyi-set_version3
mv %{buildroot}/%{_bindir}/pyinstaller        %{buildroot}/%{_bindir}/pyinstaller3

popd
python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}


%check
py.test2 tests/unit tests/functional
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{_bindir}/pyi-archive_viewer
%{_bindir}/pyi-bindepend
%{_bindir}/pyi-grab_version
%{_bindir}/pyi-makespec
%{_bindir}/pyi-set_version
%{_bindir}/pyinstaller

%{python2_sitelib}/*
%{_bindir}/pyi-archive_viewer3
%{_bindir}/pyi-bindepend3
%{_bindir}/pyi-grab_version3
%{_bindir}/pyi-makespec3
%{_bindir}/pyi-set_version3
%{_bindir}/pyinstaller3
%exclude %{python2_sitelib}/PyInstaller/bootloader/Darwin-64bit
%exclude %{python2_sitelib}/PyInstaller/bootloader/Linux-32bit
%exclude %{python2_sitelib}/PyInstaller/bootloader/Windows-32bit
%exclude %{python2_sitelib}/PyInstaller/bootloader/Windows-64bit

%files -n python3-pyinstaller
%defattr(-,root,root,-)
%{_bindir}/*
%{python3_sitelib}/*
%exclude %{python3_sitelib}/PyInstaller/bootloader/Darwin-64bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Linux-32bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-32bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-64bit

%changelog
*   Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
-   Initial packaging for Photon
