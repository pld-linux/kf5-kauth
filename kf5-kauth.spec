# TODO:
# - proper place for *.pri,
# - set ECM_MKSPECS_INSTALL_DIR in kde5-extra-cmake-modules
# - _IMPORT_PREFIX also must be set somewhere
# - runtime Requires if any
# - these dirs are not own by any package
#  /usr/include/KF5
#  /usr/lib/libexec
#  /usr/lib/plugins
#  /usr/share/kf5
%define         _state          stable
%define		orgname		kauth

Summary:	Execute actions as privileged user
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	eeb5e576c9d0d098cfb9def812f04089
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.2.0
BuildRequires:	Qt5DBus-devel
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	polkit-qt-1-devel
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KAuth provides a convenient, system-integrated way to offload actions
that need to be performed as a privileged user (root, for example) to
small (hopefully secure) helper utilities.

%package devel
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	-D_IMPORT_PREFIX=%{_prefix} \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
/etc/dbus-1/system.d/org.kde.kf5auth.conf
%attr(755,root,root) %ghost %{_libdir}/libKF5Auth.so.5
%attr(755,root,root) %{_libdir}/libKF5Auth.so.5.0.0
%dir %{qt5dir}/plugins/kauth
%dir %{qt5dir}/plugins/kauth/backend
%attr(755,root,root) %{qt5dir}/plugins/kauth/backend/kauth_backend_plugin.so
%dir %{qt5dir}/plugins/kauth/helper
%attr(755,root,root) %{qt5dir}/plugins/kauth/helper/kauth_helper_plugin.so
%dir %{_libdir}/kauth
%attr(755,root,root) %{_libdir}/kauth/kauth-policy-gen
%{_datadir}/kf5/kauth/dbus_policy.stub
%{_datadir}/kf5/kauth/dbus_service.stub

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KAuth
%{_includedir}/KF5/kauth_version.h
%{_libdir}/cmake/KF5Auth
%attr(755,root,root) %{_libdir}/libKF5Auth.so
%{qt5dir}/mkspecs/modules/qt_KAuth.pri
