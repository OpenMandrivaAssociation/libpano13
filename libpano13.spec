%define bigfov 0
# --with plf build libpano with fov > 160 support which is patent covered
# or have some legal issue, so disabled by default
%{?_with_plf: %{expand: %%global bigfov 1}}

####################
# Hardcore plf build
%define bigfov 0
####################

%if %{bigfov}
%define distsuffix plf
%if %{mdvver} >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

%define major	3
%define libname	%mklibname pano13_ %{major}
%define devname	%mklibname -d pano13

Summary:	Panorama Tools library
Name:		libpano13
Version:	2.9.19
Release:	1%{?extrarelsuffix}
License:	GPLv2+
Group:		System/Libraries
Url:		http://panotools.sourceforge.net/
Source0:	http://downloads.sourceforge.net/panotools/%{name}-%{version}_beta1.tar.gz
BuildRequires:	java-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)

%description
Helmut Dersch's Panorama Tools.

%if %{bigfov}
This package is in restricted because there is a patent if FOV is > 160
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

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pano13-devel = %{version}-%{release}

%description -n %{devname}
Developent headers for Helmut Dersch's Panorama Tools.

%prep
%setup -q
%if %{bigfov}
sed -i -e "s|\#define\s+MAX_FISHEYE_FOV.*|\#define MAX_FISHEYE_FOV 3600|" filter.h
%endif

%build
export LIBS="-lm"
export CFLAGS="%{optflags} -fPIC"
%configure2_5x \
	--enable-shared=yes \
	--enable-static=no

%make

%install
%makeinstall

%files tools
%doc README.linux AUTHORS
%{_bindir}/PT*
%{_bindir}/panoinfo
%{_mandir}/man1/*.1.*

%files -n %{libname}
%{_libdir}/libpano13.so.%{major}*

%files -n %{devname}
%{_includedir}/pano13
%{_libdir}/libpano13.so
%{_libdir}/pkgconfig/*.pc

