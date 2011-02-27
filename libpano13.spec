%define bigfov 0
# --with plf build libpano with fov > 160 support wich is patent covered
# or have some legal issue, so disabled by default

%{?_with_plf: %{expand: %%global bigfov 1}}

%define name	libpano13
%define version 2.9.17
%if %bigfov
%define distsuffix plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

%define	release	%mkrel 4
%define lib_major 2
%define libname %mklibname pano13_ %{lib_major}
%define develname %mklibname -d pano13

Name:		%{name}
Version:	%{version}
Release:	%{release}%{?extrarelsuffix}
Summary:	Panorama Tools library
License:	GPL
Group:		System/Libraries
URL:		http://panotools.sourceforge.net/
Source:		http://downloads.sourceforge.net/panotools/%{name}-%{version}.tar.gz
Patch:		string_literal.patch
BuildRequires:	java-1.7.0-icedtea-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Helmut Dersch's Panorama Tools

%if %bigfov
This package is in PLF because there is a patent if FOV is > 160
%endif

%package tools
Summary:	Panorama Tools library
Group:		Graphics

%description tools
Utilies for Helmut Dersch's Panorama Tools.

%package -n %{libname}
Summary:	Panorama Tools library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Libraries for Helmut Dersch's Panorama Tools.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pano13-devel = %{version}-%{release}

%description -n %{develname}
Developent headers for Helmut Dersch's Panorama Tools.

%prep
%setup -q
%patch -p 0

%build
export LIBS="-lm"
%if %bigfov
perl -pi -e "s|\#define\s+MAX_FISHEYE_FOV.*|\#define MAX_FISHEYE_FOV 3600|" filter.h
%endif
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure2_5x --enable-shared=yes --enable-static=no --disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall
chmod 644 %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files tools
%defattr (-,root,root)
%doc gpl.txt README.linux README.windows
%{_bindir}/PT*
%{_bindir}/panoinfo
%{_mandir}/man1/*.1.*

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/libpano13.so.%{lib_major}*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/pano13
%{_libdir}/libpano13.la
%{_libdir}/libpano13.so
%{_libdir}/pkgconfig/*.pc
