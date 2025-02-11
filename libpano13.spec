%define _disable_ld_no_undefined 1
%define _disable_lto 1

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
Version:	2.9.22
Release:	1%{?extrarelsuffix}1
License:	GPLv2+
Group:		System/Libraries
Url:		https://panotools.sourceforge.net/
Source0:	http://downloads.sourceforge.net/panotools/%{name}-%{version}.tar.gz
BuildRequires:	cmake
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
%cmake

%make_build

%install
%make_install -C build

rm -f %{buildroot}/%{_libdir}/libpano13.a

%files tools
%doc %{_datadir}/pano13/doc/
%{_bindir}/PT*
%{_bindir}/panoinfo
%{_mandir}/man1/*.1.*

%files -n %{libname}
%{_libdir}/libpano13.so.%{major}*

%files -n %{devname}
%{_includedir}/pano13
%{_libdir}/libpano13.so
%{_libdir}/pkgconfig/*.pc

