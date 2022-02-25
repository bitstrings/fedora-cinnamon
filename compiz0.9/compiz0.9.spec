# Sometimes multi-threading build could fails.  Use this as workaround for such
# case.
%ifarch ppc64le
%global _smp_mflags %{nil}
%endif

# E: invalid-soname /usr/lib64/libcompiz_core.so.0.9.14.1 libcompiz_core.so.ABI-20180221
# https://bugs.launchpad.net/compiz/+bug/1924943

%global appname compiz
%global compatsuffix 0.9

Name:           %{appname}%{compatsuffix}
Version:        0.9.14.1
%global shortversion %(cut -d. -f-3 <<<"%{version}")
Release:        1.17%{?dist}
Epoch:          1
Summary:        OpenGL compositing window manager

## Python:      tests/experimental-memcheck/compiz.supp
License:        GPLv2 and GPLv2+ and LGPLv2+ and MIT and Python
URL:            https://launchpad.net/compiz
Source0:        %{appname}-%{version}.tar.xz

#Patch0:         gcc10_common_fix.patch
#Patch1:         remove-unused-or-broken-buttons.patch
Patch2:         cmake-soname.patch
#Patch3:         aa9ebef8-a5f3-11eb-9412-002481e91f22.diff

BuildRequires:  cmake >= 3.17
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glibmm-2.4)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libmetacity) >= 3.22.0
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)

# For plugins
BuildRequires:  pkgconfig(cairo-xlib)
BuildRequires:  pkgconfig(cairo) >= 1.0
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libnotify) >= 0.7.0
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.36.2
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pango)

# Searched without pkgconfig
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  lcov
BuildRequires:  libGLU-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-devel

BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libjpeg)

Requires:       gnome-control-center-filesystem

Recommends:     ccsm = %{epoch}:%{version}-%{release}

# Rename binaries and libs for compatibility with Compiz v0.8
#   * https://bugs.launchpad.net/compiz/+bug/1924940
#   * https://gitlab.com/compiz/compiz-core/-/issues/65
Conflicts:      %{appname} < 1:0.9

%description
Compiz is one of the first OpenGL-accelerated compositing window managers for
the X Window System.  The integration allows it to perform compositing effects
in window management, such as a minimization effect and a cube work space.
Compiz is an OpenGL compositing manager that use Compiz use
EXT_texture_from_pixmap OpenGL extension for binding redirected top-level
windows to texture objects.


%package        devel
Summary:        Development package for %{name}

Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
The compiz-devel package includes the header files, and developer docs for the
compiz package.  Install 'compiz-devel' if you want to develop plugins for the
compiz windows and compositing manager.


%package     -n ccsm
Summary:        CCSM package for %{name}
BuildArch:      noarch

Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       hicolor-icon-theme

%description -n ccsm
This package contains Graphical manager for CompizConfig settings.


%prep
%autosetup -n %{appname}-%{version} -p1


%build
%cmake \
    -DCOMPIZ_BUILD_TESTING=Off \
    -DCOMPIZ_BUILD_WITH_RPATH=Off \
    -DCOMPIZ_PACKAGING_ENABLED=On \
    -DCOMPIZ_WERROR=Off \
    -DCYTHON_BIN=%{_bindir}/cython \
    -DBUILD_GLES=OFF \
    %{nil}
%cmake_build


%install
%cmake_install

# Python extension module should be installed into arch-dependent directory
# https://bugs.launchpad.net/compiz/+bug/1926046
%dnl %ifnarch i686 armv7hl
%dnl mkdir -p %{buildroot}%{python3_sitearch}
%dnl mv -v %{buildroot}%{python3_sitelib}/compizconfig* %{buildroot}%{python3_sitearch}
%dnl %endif

rm -rfv %{buildroot}%{_datadir}/cmake-*

%find_lang %{appname}
%find_lang ccsm


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{appname}.lang

# Incorrect FSF address 
# https://bugs.launchpad.net/compiz/+bug/1923481
%license COPYING COPYING.GPL COPYING.LGPL COPYING.MIT

%doc README AUTHORS NEWS
%{_bindir}/%{appname}
%{_bindir}/%{appname}-decorator
%{_bindir}/gtk-window-decorator
%{_datadir}/%{appname}/*{.png,.xml}
%{_datadir}/%{appname}/colorfilter/
%{_datadir}/%{appname}/cube/
%{_datadir}/%{appname}/cubeaddon/
%{_datadir}/%{appname}/mag/
%{_datadir}/%{appname}/notification/
%{_datadir}/%{appname}/scale/
%{_datadir}/%{appname}/showmouse/
%{_datadir}/%{appname}/splash/
%{_datadir}/%{appname}/xslt/
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/glib-2.0/schemas/org.%{appname}*.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*-%{appname}-*.xml
%{_libdir}/%{appname}/
%{_libdir}/%{appname}config/
%{_libdir}/lib%{appname}_core.so.*
%{_libdir}/lib%{appname}config_*.so
%{_libdir}/lib%{appname}config_gsettings_backend.so.*
%{_libdir}/lib%{appname}config.so.*
%{_libdir}/libdecoration.so.*

%dnl %ifnarch i686 armv7hl
%{python3_sitearch}/%{appname}config_python-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{appname}config.cpython-*-%{_arch}-linux-gnu.so
%dnl %else
%dnl %{python3_sitelib}/%{appname}config_python-%{version}-py%{python3_version}.egg-info
%dnl %{python3_sitelib}/%{appname}config.so
%dnl %endif

%files devel
%{_datadir}/%{appname}/cmake/
%{_includedir}/%{appname}/
%{_includedir}/%{appname}config/
%{_libdir}/lib%{appname}_core.so
%{_libdir}/lib%{appname}config_gsettings_backend.so
%{_libdir}/lib%{appname}config.so
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/*.pc

%files -n ccsm -f ccsm.lang
%{_bindir}/ccsm
%{_datadir}/applications/ccsm.desktop
%{_datadir}/ccsm/
%{_datadir}/icons/hicolor/*/apps/ccsm.{svg,png}
%{python3_sitelib}/ccm
%{python3_sitelib}/ccsm-%{version}-py%{python3_version}.egg-info
%config %{_sysconfdir}/%{appname}config/config.conf
%dir %{_sysconfdir}/%{appname}config


%changelog
* Fri Apr 09 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1:0.9.14.1-0.13
- build: Packaging tweaks

* Tue Apr 06 2021 gasinvein <gasinvein@gmail.com>
- Initial package
