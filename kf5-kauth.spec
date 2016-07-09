# TODO:
# - runtime Requires if any
%define		kdeframever	5.24
%define		qtver		5.3.2
%define		kfname		kauth

Summary:	Execute actions as privileged user
Name:		kf5-%{kfname}
Version:	5.24.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	41a52cd2eb1e0d6acf8c36c45999df2c
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	polkit-qt5-1-devel
BuildRequires:	polkit-qt5-1-gui-devel
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KAuth provides a convenient, system-integrated way to offload actions
that need to be performed as a privileged user (root, for example) to
small (hopefully secure) helper utilities.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
/etc/dbus-1/system.d/org.kde.kf5auth.conf
%attr(755,root,root) %ghost %{_libdir}/libKF5Auth.so.5
%attr(755,root,root) %{_libdir}/libKF5Auth.so.*.*
%dir %{qt5dir}/plugins/kauth
%dir %{qt5dir}/plugins/kauth/backend
%attr(755,root,root) %{qt5dir}/plugins/kauth/backend/kauth_backend_plugin.so
%dir %{qt5dir}/plugins/kauth/helper
%attr(755,root,root) %{qt5dir}/plugins/kauth/helper/kauth_helper_plugin.so
%dir %{_libdir}/kauth
%attr(755,root,root) %{_libdir}/kauth/kauth-policy-gen
%dir %{_datadir}/kf5/kauth
%{_datadir}/kf5/kauth/dbus_policy.stub
%{_datadir}/kf5/kauth/dbus_service.stub

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KAuth
%{_includedir}/KF5/kauth_version.h
%{_libdir}/cmake/KF5Auth
%attr(755,root,root) %{_libdir}/libKF5Auth.so
%{qt5dir}/mkspecs/modules/qt_KAuth.pri
