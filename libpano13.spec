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

%define lib_major 2
%define libname %mklibname pano13_ %{lib_major}
%define develname %mklibname -d pano13

Name:		libpano13
Version:	2.9.18
Release:	4%{?extrarelsuffix}
Summary:	Panorama Tools library
License:	GPLv2+
Group:		System/Libraries
URL:		http://panotools.sourceforge.net/
Source:		http://downloads.sourceforge.net/panotools/%{name}-%{version}.tar.gz
BuildRequires:	java-1.7.0-icedtea-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel

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
Obsoletes:	%{mklibname pano13_ 2} < 2.9.18
Obsoletes:	%{_lib}pano13_0 < 2.9.18

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

%build
export LIBS="-lm"
%if %{bigfov}
perl -pi -e "s|\#define\s+MAX_FISHEYE_FOV.*|\#define MAX_FISHEYE_FOV 3600|" filter.h
%endif
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
%{_libdir}/libpano13.so.%{lib_major}*

%files -n %{develname}
%{_includedir}/pano13
%{_libdir}/libpano13.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Sep 06 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 2.9.18-3plf2011.0
- Rebuild for restricted with all PLF features
- Hardcore PLF build
- Spec cleanup

* Thu Jun 23 2011 Funda Wang <fwang@mandriva.org> 2.9.18-3mdv2011.0
+ Revision: 686770
- correct obsoletes old libs

* Sun Jun 19 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.9.18-2
+ Revision: 686062
- obsolete old library

* Sun May 08 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.9.18-1
+ Revision: 672526
- update to new version 2.9.18
- fix license
- spec file clean

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 2.9.17-4
+ Revision: 640457
- rebuild to obsolete old packages

  + Anssi Hannula <anssi@mandriva.org>
    - plf: append "plf" to Release on cooker to make plf build have higher EVR
      again with the rpm5-style mkrel now in use

* Sat Feb 19 2011 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.17-3
+ Revision: 638785
- bump major, and ensure this kind of error get trapped at build next time
- no need for obsoletes tag anymore

* Sat Feb 19 2011 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.17-2
+ Revision: 638776
- fix patch application

* Fri Sep 17 2010 Eugeni Dodonov <eugeni@mandriva.com> 2.9.17-1mdv2011.0
+ Revision: 579126
- Updated to 2.9.17.

* Thu Jul 22 2010 Nicholas Brown <nickbrown@mandriva.org> 2.9.17-0.beta2.1mdv2011.0
+ Revision: 556857
- New Version
- New Version
- New Version

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 2.9.14-2mdv2010.0
+ Revision: 419753
- rebuild for new libjpeg v7

* Sun Jun 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.14-1mdv2010.0
+ Revision: 387661
- 2.9.14 final

* Tue Mar 10 2009 Nicholas Brown <nickbrown@mandriva.org> 2.9.14-0.beta2.1mdv2009.1
+ Revision: 353397
- new version

* Tue Feb 24 2009 Nicholas Brown <nickbrown@mandriva.org> 2.9.14-0.beta1.1mdv2009.1
+ Revision: 344490
- new version

* Fri Oct 24 2008 Nicholas Brown <nickbrown@mandriva.org> 2.9.12-6mdv2009.1
+ Revision: 296881
- rebuild
- better packaging to fix #45206

* Mon Aug 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.12-4mdv2009.0
+ Revision: 262842
- fix linkage

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.12-3mdv2008.1
+ Revision: 158733
- update PLF description

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.12-2mdv2008.1
+ Revision: 158609
- fix devel package name

* Sat Jan 26 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.12-1mdv2008.1
+ Revision: 158477
- import libpano13


