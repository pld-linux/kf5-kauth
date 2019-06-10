# TODO:
# - runtime Requires if any
%define		kdeframever	5.59
%define		qtver		5.9.0
%define		kfname		kauth

Summary:	Execute actions as privileged user
Name:		kf5-%{kfname}
Version:	5.59.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	80da78562d813e834039c8c166d8f940
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	ninja
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
Requires:	cmake >= 2.6.0
Requires:	kf5-kcoreaddons-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %ghost %{_libdir}/libKF5Auth.so.5
%attr(755,root,root) %{_libdir}/libKF5Auth.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5AuthCore.so.5
%attr(755,root,root) %{_libdir}/libKF5AuthCore.so.5.*.*
%dir %{qt5dir}/plugins/kauth
%dir %{qt5dir}/plugins/kauth/backend
%attr(755,root,root) %{qt5dir}/plugins/kauth/backend/kauth_backend_plugin.so
%dir %{qt5dir}/plugins/kauth/helper
%attr(755,root,root) %{qt5dir}/plugins/kauth/helper/kauth_helper_plugin.so
%dir %{_libexecdir}/kauth
%attr(755,root,root) %{_libexecdir}/kauth/kauth-policy-gen
%dir %{_datadir}/kf5/kauth
%{_datadir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_datadir}/kf5/kauth/dbus_policy.stub
%{_datadir}/kf5/kauth/dbus_service.stub
/etc/xdg/kauth.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KAuth
%{_includedir}/KF5/kauth_version.h
%{_libdir}/cmake/KF5Auth
%attr(755,root,root) %{_libdir}/libKF5Auth.so
%attr(755,root,root) %{_libdir}/libKF5AuthCore.so
%{qt5dir}/mkspecs/modules/qt_KAuth.pri
