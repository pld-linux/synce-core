# TODO:
# - check connector-(o)dccm requirements
# - bluetooth?
# - upgrade paths from 0.15 packages (missing obsoletes/provides, package renames?)
#   finish package: http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2012-July/022878.html
#   and http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2012-July/022880.html
#
# Conditional build:
%bcond_without	dccm	# dccm file support
%bcond_without	odccm	# odccm support

Summary:	Connection framework and DCCM implementation for WinCE devices
Summary(pl.UTF-8):	Szkielet połączeń oraz implementacja DCCM dla urządzeń WinCE
Name:		synce-core
Version:	0.17
Release:	0.1
License:	MIT
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	ee0b9369b6fea5e2d1b970503dd7cb0e
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-Pyrex >= 0.9.6
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
Requires:	%{name}-lib = %{version}-%{release}
Requires:	dhcp-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Synce-connector is a connection framework and DCCM implementation for
Windows Mobile devices that integrates with udev.

%description -l pl.UTF-8
Synce-connector to szkielet połączeń oraz implementacja DCCM dla
urządzeń Windows Mobile; integruje się z udev.

%package lib
Summary:	Core SynCE library
Summary(pl.UTF-8):	Podstawowa biblioteka SynCE
Group:		Libraries
Requires:	glib2 >= 1:2.26
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
Requires:	glib2-devel >= 1:2.26
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

%package -n python-pyrapi2
Summary:	Python binding for synce library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki synce
Group:		Libraries/Python
Requires:	%{name}-lib = %{version}-%{release}

%description -n python-pyrapi2
Python binding for synce library.

%description -n python-pyrapi2 -l pl.UTF-8
Wiązanie Pythona do biblioteki synce.

%package odccm
Summary:	Connection via odccm for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez odccm z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description odccm
This package provides connection via odccm for WinCE devices.

%description odccm -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez odccm z urządzeniami WinCE.

%package dccm
Summary:	Connection via dccm for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez dccm z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
# check what is actually required
Requires:	synce-vdccm

%description dccm
This package provides connection via dccm for WinCE devices.

%description dccm -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez dccm z urządzeniami WinCE.

%prep
%setup -q

%build
%configure \
	DHCLIENTPATH=/sbin/dhclient \
	UDEVADMPATH=/sbin/udevadm \
	IFCONFIGPATH=/sbin/ifconfig \
	PPPDPATH=/usr/sbin/pppd \
	--enable-bluetooth-support \
	%{__enable_disable dccm dccm-file-support} \
	%{__enable_disable odccm odccm-support}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_postclean %{_datadir}/%{name}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsynce.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/pyrapi2.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog LICENSE README TODO
%attr(755,root,root) %{_libdir}/synce-serial-chat
%attr(755,root,root) %{_bindir}/pcp
%attr(755,root,root) %{_bindir}/pkillall
%attr(755,root,root) %{_bindir}/pls
%attr(755,root,root) %{_bindir}/pmkdir
%attr(755,root,root) %{_bindir}/pmv
%attr(755,root,root) %{_bindir}/prm
%attr(755,root,root) %{_bindir}/prmdir
%attr(755,root,root) %{_bindir}/prun
%attr(755,root,root) %{_bindir}/psettime
%attr(755,root,root) %{_bindir}/pshortcut
%attr(755,root,root) %{_bindir}/pstatus
%attr(755,root,root) %{_bindir}/rapiconfig
%attr(755,root,root) %{_bindir}/synce-database
%attr(755,root,root) %{_bindir}/synce-install-cab
%attr(755,root,root) %{_bindir}/synce-list-programs
%attr(755,root,root) %{_bindir}/synce-registry
%attr(755,root,root) %{_bindir}/synce-remove-program
%attr(755,root,root) %{_bindir}/synce-serial
%attr(755,root,root) %{_bindir}/synce-unlock
/etc/dbus-1/system.d/org.synce.dccm.conf
/lib/udev/rules.d/85-synce.rules
%attr(755,root,root) /lib/udev/synce-udev-rndis
%attr(755,root,root) /lib/udev/synce-udev-serial
%{_datadir}/dbus-1/system-services/org.synce.dccm.service
# no such dir?
#/etc/ppp/ip-up.d/synce-udev-bt-ipup
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/ppp/peers/synce-bt-peer
%dir %{_datadir}/synce-core
%{_datadir}/synce-core/dhclient.conf
%{_datadir}/synce-core/synceconnector.py[co]
%attr(755,root,root) %{_datadir}/synce-core/udev-synce-rndis
%attr(755,root,root) %{_datadir}/synce-core/udev-synce-serial
%{_mandir}/man1/pcp.1*
%{_mandir}/man1/pkillall.1*
%{_mandir}/man1/pls.1*
%{_mandir}/man1/pmkdir.1*
%{_mandir}/man1/pmv.1*
%{_mandir}/man1/prm.1*
%{_mandir}/man1/prmdir.1*
%{_mandir}/man1/prun.1*
%{_mandir}/man1/psettime.1*
%{_mandir}/man1/pshortcut.1*
%{_mandir}/man1/pstatus.1*
%{_mandir}/man1/rapiconfig.1*
%{_mandir}/man1/synce-install-cab.1*
%{_mandir}/man1/synce-list-programs.1*
%{_mandir}/man1/synce-registry.1*
%{_mandir}/man1/synce-remove-program.1*

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsynce.so.0

%files lib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so
%{_includedir}/irapistream.h
%{_includedir}/rapi.h
%{_includedir}/rapi2.h
%{_includedir}/rapitypes.h
%{_includedir}/rapitypes2.h
%{_includedir}/synce*.h
%{_pkgconfigdir}/libsynce.pc
%{_mandir}/man3/date_from_tm.3*
%{_mandir}/man3/date_to_tm.3*
%{_mandir}/man3/rapi_connection_from_name.3*
%{_mandir}/man3/synce*.3*
%{_mandir}/man3/time_fields_from_filetime.3*
%{_mandir}/man3/time_fields_to_filetime.3*
%{_mandir}/man3/wstr*.3*
%{_mandir}/man7/synce.7*

%files lib-static
%defattr(644,root,root,755)
%{_libdir}/libsynce.a

%files -n python-pyrapi2
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pyrapi2.so

%if %{with odccm}
%files odccm
%defattr(644,root,root,755)
%endif

%if %{with dccm}
%files dccm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dccm
%endif
