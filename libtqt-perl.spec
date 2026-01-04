%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 3

%define tde_pkg libtqt-perl
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.008
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Perl bindings for the TQt library
Group:		Development/Libraries/Perl
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool 

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig

BuildRequires:	trinity-libsmoketqt-devel >= %{tde_version}

BuildRequires:	perl(ExtUtils::MakeMaker)

BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xft)
BuildRequires:  perl-devel

Requires:		perl-TQt = %{?epoch:%{epoch}:}%{version}-%{release}


%description
This module lets you use the TQt library from Perl.
It provides an object-oriented interface and is easy to use.

%files
%defattr(-,root,root,-)
%{tde_prefix}/bin/puic
%{tde_prefix}/share/man/man1/puic.1*
%{_bindir}/pqtapi
%{_bindir}/pqtsh
%if 0%{?rhel} == 5
%{_datadir}/doc/libqt-perl/
%endif

##########

%package -n perl-TQt
Summary:	Perl bindings for the TQt library
Group:		Development/Libraries/Perl

Provides:		perl(TQtShell)
Provides:		perl(TQtShellControl)

%description -n perl-TQt
This module lets you use the TQt library from Perl.
It provides an object-oriented interface and is easy to use.

%files -n perl-TQt
%defattr(-,root,root,-)
%{perl_vendorarch}/TQt.pm
%{perl_vendorarch}/TQt.pod
%dir %{perl_vendorarch}/TQt
%{perl_vendorarch}/TQt/GlobalSpace.pm
%{perl_vendorarch}/TQt/attributes.pm
%{perl_vendorarch}/TQt/constants.pm
%{perl_vendorarch}/TQt/debug.pm
%{perl_vendorarch}/TQt/enumerations.pm
%{perl_vendorarch}/TQt/isa.pm
%{perl_vendorarch}/TQt/properties.pm
%{perl_vendorarch}/TQt/signals.pm
%{perl_vendorarch}/TQt/slots.pm
%{perl_vendorarch}/auto/TQt/
%{_mandir}/man3/TQt.3pm.*

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/"*"/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export TDEDIR=%{tde_prefix}
export PATH="%{tde_prefix}/bin:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_prefix}/bin \
  --datadir=%{tde_prefix}/share \
  --libdir=%{tde_prefix}/%{_lib} \
  --mandir=%{tde_prefix}/share/man \
  --includedir=%{tde_prefix}/include/tde \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --disable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --disable-smoke

%__make %{?_smp_mflags}


%install
export PATH="%{tde_prefix}/bin:${PATH}"
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{buildroot}%{perl_archlib}/perllocal.pod
%__rm -f %{buildroot}%{perl_vendorarch}/auto/TQt/.packlist

