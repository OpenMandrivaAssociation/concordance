
%define name	concordance
%define version	0.20
%define cvs	20081101
%define rel	1

%define major	0
%define libname	%mklibname concord %major
%define devname	%mklibname concord -d 

Summary:	Command-line Logitech Harmony remote programmer
Name:		%{name}
Version:	%{version}
%if %cvs
Release:	%mkrel 1.%cvs.%rel
%else
Release:	%mkrel %{rel}
%endif
License:	GPLv3+
URL:		http://www.phildev.net/harmony/
%if %cvs
Source:		concordance-%{cvs}.tar.lzma
%else
Source:		http://downloads.sourceforge.net/concordance/concordance-%{version}.tar.bz2
%endif
BuildRoot:	%{_tmppath}/%{name}-root
Group:		System/Configuration/Hardware
BuildRequires:	libusb-devel
BuildRequires:	python-devel
BuildRequires:	swig
BuildRequires:	perl-devel
BuildRequires:	chrpath

%description
This command-line software allows you to program your Logitech Harmony
remote using a configuration object retreived from the Harmony website.

%package -n %libname
Summary:	System library of libconcord
Group:		System/Libraries

%description -n %libname
Logitech Harmony remote programmer library for applications that use it.

%package -n %devname
Summary:	Development headers for libconcord
Group:		Development/C
Requires:	%libname = %version
Provides:	concord-devel = %version

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
%if %cvs
%setup -q -n concordance
autoreconf -i libconcord concordance
%else
%setup -q
%endif

%build
cd libconcord
%configure2_5x --disable-static
%make
cd bindings/perl
swig -perl5 concord.i
%{__perl} Makefile.PL INSTALLDIRS=vendor INC=-I../.. LIBS="-L../../.libs -lconcord"
%make
cd ../../..
cd concordance
%configure2_5x CPPFLAGS=-I../libconcord LDFLAGS="%{?ldflags} -L../libconcord"
%make
cd ..
cd consnoop
%make CXXFLAGS="%optflags"

%install
rm -rf %{buildroot}
%makeinstall_std -C libconcord
%makeinstall_std -C libconcord/bindings/perl
chrpath -d %{buildroot}%{perl_vendorarch}/auto/concord/concord.so
%makeinstall_std -C concordance

cd libconcord/bindings/python
python setup.py install --root=%{buildroot}
cd -

# useful or not? include for now:
install -m755 consnoop/consnoop %{buildroot}%{_bindir}

rm -f %{buildroot}%{_libdir}/libconcord.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc concordance/README
%doc Changelog
%{_bindir}/concordance
%{_mandir}/man1/concordance*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libconcord.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%doc libconcord/README
%{_bindir}/consnoop
%{_libdir}/libconcord.so
%{_includedir}/libconcord.h

%files -n perl-concord
%defattr(-,root,root)
%{perl_vendorarch}/concord.pm
%{perl_vendorarch}/auto/concord

%files -n python-libconcord
%defattr(-,root,root)
%{py_sitedir}/libconcord*

