# TODO: build kernel module (src/currera_acq_module)
#
Summary:	XIMEA API Software Package for Linux
Summary(pl.UTF-8):	Pakiet XIMEA API dla Linuksa
Name:		XIMEA
# see version_LINUX_SP.txt
Version:	4.07.13
Release:	1
# some mix of binaries and sources with no licensing information (except for GPL kernel module)
License:	unknown
Group:		Libraries
Source0:	https://www.ximea.com/support/attachments/271/XIMEA_Linux_SP.tgz
# NoSource0-md5:	b60f28842bf3e5fb94c5f43c84bb7027
NoSource:	0
URL:		http://www.ximea.com/support/wiki/apis/XIMEA_Linux_Software_Package
BuildRequires:	gstreamer0.10-devel
BuildRequires:	gstreamer0.10-plugins-base-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
Requires:	libraw1394 >= 2.1.0
Requires:	libusb >= 1.0.9
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch	%{ix86}
%define	abi	X32
%endif
%ifarch %{x8664}
%define	abi	X64
%endif
%ifarch %{arm}
%define	abi	Xarm
%endif

%description
XIMEA Linux Software Package contains of
 * Kernel Driver of CURRERA-R cameras for Ubuntu 10.04
 * xiAPI
 * Examples:
   * xiSample - sample showing basic image acquisition in xiAPI
   * streamViewer - camera live image viewer for picture check

%description -l pl.UTF-8
Pakiet XIMEA Linux Software Package składa się z:
 - modułu jądra dla kamer CURRERA-R dla Ubuntu 10.04
 - biblioteki xiAPI
 - przykładów:
   - xiSample - przykładu pokazującego proste ściąganie obrazu przy
     użyciu xiAPI
   - streamViewer - podgląd kamery na żywo

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
Summary:	XIMEA streamViewer utility
Summary(pl.UTF-8):	Narzędzie streamViewer dla urządzeń XIMEA
Group:		X11/Applications/Graphics
Requires:	%{name}-devel = %{version}-%{release}

%description viewer
XIMEA streamViewer utility.

%description viewer -l pl.UTF-8
Narzędzie streamViewer dla urządzeń XIMEA.

%prep
%setup -q -c

ln -s ../../include package/examples/streamViewer/m3api
ln -s libm3api.so.2 package/api/%{abi}/libm3api.so

%build
cd package
%{__make} -C examples/streamViewer streamViewer.o \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcxxflags} %{rpmcppflags} -I."
%{__cxx} %{rpmldflags} %{rpmcxxflags} -o examples/streamViewer/streamViewer \
	examples/streamViewer/*.o \
	$(pkg-config --libs gtk+-2.0 gstreamer-0.10 gstreamer-app-0.10 gstreamer-interfaces-0.10) \
	-Lapi/%{abi} -lm3api

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_includedir}/ximea}

cd package
cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}/ximea
install api/%{abi}/libm3api.so.0 $RPM_BUILD_ROOT%{_libdir}/libm3api.so.0.0.0
install api/%{abi}/libm3api.so.2 $RPM_BUILD_ROOT%{_libdir}/libm3api.so.2.0.0
ln -sf libm3api.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libm3api.so.0
ln -sf libm3api.so.2.0.0 $RPM_BUILD_ROOT%{_libdir}/libm3api.so.2
ln -sf libm3api.so.2.0.0 $RPM_BUILD_ROOT%{_libdir}/libm3api.so
install libs/gentl/%{abi}/libXIMEA_GenTL.cti.* $RPM_BUILD_ROOT%{_libdir}
ln -sf libXIMEA_GenTL.cti.2 $RPM_BUILD_ROOT%{_libdir}/libXIMEA_GenTL.cti
install examples/streamViewer/streamViewer $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc package/README
%attr(755,root,root) %{_libdir}/libXIMEA_GenTL.cti.0
%attr(755,root,root) %{_libdir}/libXIMEA_GenTL.cti.2
%attr(755,root,root) %{_libdir}/libXIMEA_GenTL.cti
%attr(755,root,root) %{_libdir}/libm3api.so.0.*.*
%attr(755,root,root) %ghost %{_libdir}/libm3api.so.0
%attr(755,root,root) %{_libdir}/libm3api.so.2.*.*
%attr(755,root,root) %ghost %{_libdir}/libm3api.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libm3api.so
%{_includedir}/ximea

%files viewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/streamViewer
