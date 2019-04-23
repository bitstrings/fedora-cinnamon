Name:          muffin
Version:       4.0.8
Release:       105.%{gitdate}git%{shortcommit}%{?dist}
Summary:       Window and compositing manager based on Clutter

License:       GPLv2+
URL:           https://github.com/linuxmint/%{name}
#Source0:       %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source0:       %{url}/archive/master.mint19.tar.gz
Source1:       muffin-adwaita.txt

#Patch0:        tiled_shadow.patch
#Patch0:        upstream.patch

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(cinnamon-desktop) >= 4.0.0
BuildRequires: pkgconfig(gnome-doc-utils)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(xkeyboard-config)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(xtst)
BuildRequires: zenity
# Bootstrap requirements
BuildRequires: pkgconfig(gtk-doc)
BuildRequires: gnome-common
BuildRequires: intltool

Requires: dbus-x11
Requires: zenity

%description
Muffin is a window and compositing manager that displays and manages
your desktop via OpenGL. Muffin combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

Muffin is very extensible via plugins, which
are used both to add fancy visual effects and to rework the window
management behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
Header files and libraries for developing Muffin plugins. Also includes
utilities for testing Metacity/Muffin themes.

%prep
%autosetup -p1 -n muffin-master.mint19

NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-static \
           --enable-compile-warnings=minimum \
           --disable-wayland-egl-platform \
           --disable-wayland-egl-server \
           --disable-kms-egl-platform \
           --disable-wayland \
           --disable-native-backend \
           --disable-clutter-doc

sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build V=1

%install
%make_install

# Create a dummy themes directory so that cinnamon settings will see
# the Adwaita fallback theme which has been removed from gnome-themes-standard
mkdir -p %{buildroot}/%{_datadir}/themes/Adwaita/metacity-1/
cp %{SOURCE1} %{buildroot}/%{_datadir}/themes/Adwaita/metacity-1/

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  --add-only-show-in X-Cinnamon \
  %{buildroot}%{_datadir}/applications/muffin.desktop

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc README AUTHORS NEWS HACKING doc/theme-format.txt
%license COPYING
%{_bindir}/muffin
%{_libdir}/libmuffin.so.*
%{_libdir}/libmuffin-clutter-0.so
%{_libdir}/libmuffin-cogl-0.so
%{_libdir}/libmuffin-cogl-pango-0.so
%{_libdir}/libmuffin-cogl-path-0.so
%{_libdir}/muffin/
%{_libexecdir}/muffin-restart-helper
%exclude %{_libdir}/muffin/*.gir
%{_datadir}/applications/muffin.desktop
%dir %{_datadir}/muffin/
%{_datadir}/muffin/theme/
%{_datadir}/glib-2.0/schemas/org.cinnamon.muffin.gschema.xml
%{_datadir}/themes/Adwaita/metacity-1/
%{_mandir}/man1/muffin.1.*

%files devel
%{_bindir}/muffin-message
%{_bindir}/muffin-theme-viewer
%{_bindir}/muffin-window-demo
%{_datadir}/muffin/icons/
%{_datadir}/gtk-doc/html/muffin/
%{_includedir}/muffin/
%{_libdir}/libmuffin.so
%{_libdir}/muffin/*.gir
%{_libdir}/pkgconfig/*
%{_mandir}/man1/muffin-*

%changelog
