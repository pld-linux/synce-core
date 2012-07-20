# TODO:
# - check connector-dccm requirements
# - bluetooth?
#
# Conditional build:
%bcond_without	dbus	# build without DBus support
%bcond_without	dccm	# build without dccm file support
%bcond_without	odccm	# build without odccm support

%if %{without dbus}
%undefine	with_odccm
%endif

Summary:	Connection framework and dccm-implementation for WinCE devices
Name:		synce-core
Version:	0.16
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	d557b3fd89b8ecdff6772bd7e1d2451e
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.60}
BuildRequires:	gnet-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	synce-libsynce-devel >= 0.11
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

%package odccm
Summary:	Provides Connection via odccm for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description -n synce-connector-odccm
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/synce-unlock
%attr(755,root,root) %{_libdir}/synce-serial-chat
%dir %{_datadir}/synce-connector
%{_datadir}/synce-connector/dhclient.conf
%{_datadir}/synce-connector/synceconnector.py[co]

/etc/dbus-1/system.d/org.synce.dccm.conf
/lib/udev/rules.d/85-synce.rules
%attr(755,root,root) %{_bindir}/synce-serial
%attr(755,root,root) /lib/udev/synce-udev-rndis
%attr(755,root,root) /lib/udev/synce-udev-serial
%{_datadir}/dbus-1/system-services/org.synce.dccm.service
%attr(755,root,root) %{_datadir}/synce-connector/udev-synce-rndis
%attr(755,root,root) %{_datadir}/synce-connector/udev-synce-serial

%if %{with odccm}
%files odccm
%defattr(644,root,root,755)
%endif

%if %{with dccm}
%files dccm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dccm
%endif
