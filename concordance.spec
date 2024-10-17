%define major	3
%define libname	%mklibname concord %major
%define devname	%mklibname concord -d 

Summary:	Command-line Logitech Harmony remote programmer
Name:		concordance
Version:	1.0
Release:	2
License:	GPLv3+
URL:		https://www.phildev.net/harmony/
Source:		http://downloads.sourceforge.net/concordance/concordance-%{version}.tar.bz2
Patch0:		concordance-mime.patch
Patch1:		consnoop-includes.patch
Patch2:		concordance-1.0-automake.patch
Group:          System/Configuration/Hardware
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(python)
BuildRequires:	swig
BuildRequires:	perl-devel
BuildRequires:	zziplib-devel

%description
This command-line software allows you to program your Logitech Harmony
remote using a configuration object retrieved from the Harmony website.

%package -n libconcord-common
Summary:	Common files of libconcord

Group:		System/Libraries

%description -n libconcord-common
Common files required by Logitech Harmony remote programmer library.

%package -n %libname
Summary:	System library of libconcord

Group:		System/Libraries
Requires:	libconcord-common >= %{version}-%{release}

%description -n %libname
Logitech Harmony remote programmer library for applications that use it.

%package -n %devname
Summary:	Development headers for libconcord

Group:		Development/C
Requires:	%libname = %{version}
Provides:	concord-devel = %{version}-%{release}

%description -n %devname
Development headers for developing applications that use libconcord, a
Logitech Harmony remote programmer library.

%package -n perl-concord
Summary:	Perl bindings for libconcord

Group:		Development/Perl

%description -n perl-concord
Perl bindings for libconcord, a Logitech Harmony remote programmer
library.

%package -n python-libconcord
Summary:	Python bindings for libconcord

Group:		Development/Python
Requires:	%libname

%description -n python-libconcord
Python bindings for libconcord, a Logitech Harmony remote programmer
library.

%prep
%setup -q
%autopatch -p1

%build
cd libconcord
# patch0
autoreconf -fi
%configure2_5x --disable-static --disable-mime-update
%make
%make udev
cd bindings/perl
swig -perl5 concord.i
%{__perl} Makefile.PL INSTALLDIRS=vendor INC=-I../..
%make OTHERLDFLAGS="-L../../.libs" LDLOADLIBS="-lconcord"
cd ../../..
cd concordance
%configure2_5x CPPFLAGS=-I../libconcord LDFLAGS="%{?ldflags} -L../libconcord/.libs"
%make
cd ..
cd consnoop
%make CXXFLAGS="%{optflags} %{?ldflags}"

%install
%makeinstall_std -C libconcord \
	install_udev UDEVROOT=/
#
%makeinstall_std -C libconcord/bindings/perl
%makeinstall_std -C concordance

pushd libconcord/bindings/python
python setup.py install --root=%{buildroot}
popd

# useful or not? include for now:
install -m755 consnoop/consnoop %{buildroot}%{_bindir}

%post -n libconcord-common
# apply new/updated rules
/sbin/udevadm trigger --subsystem-match=usb --attr-match=idVendor=046d --attr-match=idProduct="c1*"
/sbin/udevadm trigger --subsystem-match=usb --attr-match=idVendor=0400 --attr-match=idProduct="c359"

%files
%doc concordance/README
%doc Changelog
%{_bindir}/concordance
%{_mandir}/man1/concordance*

%files -n libconcord-common
%{_udevrulesdir}/80-libconcord-usbnet.rules
%{_udevrulesdir}/60-libconcord.rules
/lib/udev/start_concordance_dhcpd.sh
/lib/udev/start_concordance_dhcpd_wrapper.sh
%{_datadir}/mime/packages/libconcord.xml

%files -n %{libname}
%{_libdir}/libconcord.so.%{major}*

%files -n %{devname}
%doc libconcord/README
%{_bindir}/consnoop
%{_libdir}/libconcord.so
%{_includedir}/libconcord.h

%files -n perl-concord
%{perl_vendorarch}/concord.pm
%{perl_vendorarch}/auto/concord

%files -n python-libconcord
%{py_puresitedir}/libconcord*

