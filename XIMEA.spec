Summary:	XIMEA API Software Package for Linux
Summary(pl.UTF-8):	Pakiet XIMEA API dla Linuksa
Name:		XIMEA
# see version_LINUX_SP.txt
Version:	1.04
Release:	1
# probably non-distributable: contains some mix of binaries and sources with no licensing information;
# there is also binary .ko module (probably for some particular Ubuntu kernel) with license=GPL
# and no sources included
License:	unknown
Group:		Libraries
Source0:	http://www.ximea.com/support/attachments/271/XIMEA_Linux_SP.tgz
# NoSource0-md5:	2dabc84fe3a9bd5d31f5882c9d0aff21
NoSource:	0
Patch0:		%{name}-gcc.patch
Patch1:		%{name}-glib.patch
URL:		http://www.ximea.com/support/wiki/currera/XIMEA_Linux_Software_Package
BuildRequires:	gtk+2-devel
BuildRequires:	libva-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XIMEA Linux Software Package contains of
 * Kernel Driver of CURRERA-R cameras for Ubuntu 10.04
 * xiAPI
 * Examples:
   * xiSample - sample showing basic image acquisition in xiAPI
   * vaViewer - camera live image viewer for picture check

%description -l pl.UTF-8
Pakiet XIMEA Linux Software Package składa się z:
 - modułu jądra dla kamer CURRERA-R dla Ubuntu 10.04
 - biblioteki xiAPI
 - przykładów:
   - xiSample - przykładu pokazującego proste ściąganie obrazu przy
     użyciu xiAPI
   - vaViewer - podgląd kamery na żywo

%package devel
Summary:	Header files for xiAPI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki xiAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for xiAPI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki xiAPI.

%package viewer
Summary:	XIMEA vaViewer utility
Summary(pl.UTF-8):	Narzędzie vaViewer dla urządzeń XIMEA
Group:		X11/Applications/Graphics
Requires:	%{name}-devel = %{version}-%{release}

%description viewer
XIMEA vaViewer utility.

%description viewer -l pl.UTF-8
Narzędzie vaViewer dla urządzeń XIMEA.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

%build
cd examples/vaViewer

CXXFLAGS="%{rpmcxxflags} %{rpmcppflags} $(pkg-config --cflags libva libva-x11 gtk+-2.0) -I ../../include"
%{__cxx} $CXXFLAGS -c acquisition.cpp
%{__cxx} $CXXFLAGS -c main.cpp
%{__cxx} %{rpmldflags} %{rpmcxxflags} -o vaViewer acquisition.o main.o $(pkg-config --libs libva libva-x11 gtk+-2.0) -L../../api -lm3api

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_includedir}/ximea}

cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}/ximea
install api/libm3api.so $RPM_BUILD_ROOT%{_libdir}
install examples/vaViewer/vaViewer $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libm3api.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/ximea

%files viewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vaViewer
