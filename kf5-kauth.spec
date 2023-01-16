#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	5.102
%define		qtver		5.15.2
%define		kfname		kauth

Summary:	Execute actions as privileged user
Name:		kf5-%{kfname}
Version:	5.102.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	f3d76da3f2d9f75058a134b6177a34cd
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	polkit-qt5-1-devel >= 0.99.0
BuildRequires:	polkit-qt5-1-gui-devel >= 0.99.0
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	kf5-dirs
Requires:	kf5-kcoreaddons >= %{version}
Requires:	polkit-qt5-1 >= 0.99.0
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
Requires:	cmake >= 3.16
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
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%if %{with tests}
ctest
%endif


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
%ghost %{_libdir}/libKF5Auth.so.5
%attr(755,root,root) %{_libdir}/libKF5Auth.so.*.*
%ghost %{_libdir}/libKF5AuthCore.so.5
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
%{_datadir}/qlogging-categories5/kauth.categories
%{_datadir}/qlogging-categories5/kauth.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KAuth
%{_includedir}/KF5/KAuthCore
%{_includedir}/KF5/KAuthWidgets
%{_libdir}/cmake/KF5Auth
%{_libdir}/libKF5Auth.so
%{_libdir}/libKF5AuthCore.so
%{qt5dir}/mkspecs/modules/qt_KAuth.pri
%{qt5dir}/mkspecs/modules/qt_KAuthCore.pri
