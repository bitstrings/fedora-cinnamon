Name:          muffin
Version:       5.2.1
Release:       123%{?dist}
Summary:       Window and compositing manager based on Clutter

License:       GPLv2+
URL:           https://github.com/linuxmint/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source0:       %{name}-%{version}.tar.gz
Source1:       muffin-adwaita.txt

Patch0: tiled_shadow.patch
Patch1: upstream.patch

BuildRequires: make
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(cinnamon-desktop) >= 5.0.0
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
%setup -q
%patch0 -p0
#%patch1 -p1

NOCONFIGURE=1 ./autogen.sh

%build
# gobject introspection does not work with LTO.  There is an effort to fix this
# in the appropriate project upstreams, so hopefully LTO can be enabled someday
# Disable LTO.
%define _lto_cflags %{nil}

%configure --disable-static \
           --enable-startup-notification=yes \
           --disable-silent-rules \
           --enable-gtk-doc \
           --disable-clutter-doc \
           --disable-wayland-egl-platform \
           --disable-wayland-egl-server \
           --disable-kms-egl-platform \
           --disable-wayland \
           --disable-native-backend

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
* Sat Jun 12 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-1
- Update to 5.0.1 release

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.1-1
- Update to 4.8.1 release

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Tue Aug 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.3-1
- Update to 4.6.3 release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4.6.2-2
- Disable LTO

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.2-1
- Update to 4.6.2 release

* Wed May 27 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.1-1
- Update to 4.6.1 release

* Wed May 13 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Mon May 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.3-1
- New upstream release 4.4.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-1
- Update to 4.4.2 release

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-4
- Add upstream fixes for reverted commits

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-3
- Revert another bad commit

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-2
- Revert bad commit

* Wed Nov 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Tue Oct 01 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-2
- Remove --warn-error from gir scannerflags

* Wed Jul 31 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-1
- Update to 4.2.2 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.1-1
- Update to 4.2.1 release

* Sat Jul 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-3
- Revert last commit

* Sat Jul 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-2
- Add upstream pull request

* Fri Jun 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Wed Jun 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.6.20190611git6b11adb
- Update snapshot

* Wed Jun 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.5.20190604git5774eb2
- Add upstream pull request #514

* Wed Jun 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.4.20190604git5774eb2
- Update snapshot

* Wed Apr 17 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.3.20190417gitc72054b
- Update snapshot

* Tue Apr 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.2.20190416gitb625cfb
- Update snapshot

* Fri Apr 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.1.20190405git462a534
- Update to git master snapshot

* Wed Apr 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.7-1
- Update to 4.0.7 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.6-1
- Update to 4.0.6 release

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.5-1
- Update to 4.0.5 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.4-1
- Update to 4.0.4 release

* Wed Nov 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Sat Nov 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release
- Readd muffin binary, useful for debug only
