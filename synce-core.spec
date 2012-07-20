# TODO:
# - check connector-dccm requirements
# - bluetooth?
#
# Conditional build:
%bcond_without	dccm	# build without dccm file support
%bcond_without	odccm	# build without odccm support
#
Summary:	Connection framework and dccm-implementation for WinCE devices
Name:		synce-core
Version:	0.16
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	e823e5b97b57c568129c116fc289bcf3
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	gnet-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
Requires:	dhcp-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Synce-connector is a connection framework and dccm-implementation for
Windows Mobile devices that integrates with udev.

%description -l pl.UTF-8
Biblioteka libsynce to część projektu SynCE. Jest wymagana dla (co
najmniej) następujących części projektu: librapi2, dccmd.

%package lib
Summary:	Core SynCE library
Summary(pl.UTF-8):	Podstawowa biblioteka SynCE
Group:		Libraries
Obsoletes:	synce-libsynce

%description lib
libsynce is part of the SynCE project. It's required for (at least)
the following parts of the SynCE project: librapi2, dccmd.

%description lib -l pl.UTF-8
Biblioteka libsynce to część projektu SynCE. Jest wymagana dla (co
najmniej) następujących części projektu: librapi2, dccmd.

%package lib-devel
Summary:	Header files for libsynce library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsynce
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Requires:	dbus-devel
Requires:	dbus-glib-devel
Obsoletes:	synce-libsynce-devel

%description lib-devel
Header files for libsynce library.

%description lib-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsynce.

%package lib-static
Summary:	Static libsynce library
Summary(pl.UTF-8):	Statyczna biblioteka libsynce
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Obsoletes:	synce-libsynce-static

%description lib-static
Static libsynce library.

%description lib-static -l pl.UTF-8
Statyczna biblioteka libsynce.

%package odccm
Summary:	Provides Connection via odccm for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description odccm
Provides Connection via odccm for WinCE devices.

%package dccm
Summary:	Provides Connection via dccm for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
# check what is actually required
Requires:	synce-vdccm

%description dccm
Provides Connection via dccm for WinCE devices.

%prep
%setup -q

%build
DHCLIENTPATH=/sbin/dhclient \
UDEVADMPATH=/sbin/udevadm \
%configure \
	--enable-udev \

#	%{!?with_dccm: --disable-dccm-file-support} \
#	%{!?with_odccm: --disable-odccm-support}
#
#  --enable-bluetooth-support Build in bluetooth support

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_postclean %{_datadir}/%{name}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsynce.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog
%attr(755,root,root) %{_bindir}/synce-unlock
%attr(755,root,root) %{_libdir}/synce-serial-chat
%dir %{_datadir}/synce-core
%{_datadir}/synce-core/dhclient.conf
%{_datadir}/synce-core/synceconnector.py[co]

/etc/dbus-1/system.d/org.synce.dccm.conf
/lib/udev/rules.d/85-synce.rules
%attr(755,root,root) %{_bindir}/synce-serial
%attr(755,root,root) /lib/udev/synce-udev-rndis
%attr(755,root,root) /lib/udev/synce-udev-serial
%{_datadir}/dbus-1/system-services/org.synce.dccm.service
%attr(755,root,root) %{_datadir}/synce-core/udev-synce-rndis
%attr(755,root,root) %{_datadir}/synce-core/udev-synce-serial

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsynce.so.0

%files lib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so
%{_includedir}/*.h
%{_pkgconfigdir}/libsynce.pc
%{_mandir}/man3/*

%files lib-static
%defattr(644,root,root,755)
%{_libdir}/libsynce.a
%{_mandir}/man7/synce.7*

%if %{with odccm}
%files odccm
%defattr(644,root,root,755)
%endif

%if %{with dccm}
%files dccm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dccm
%endif
