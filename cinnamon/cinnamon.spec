%global commit c843f3664064742e2672e0fea528571a882d84ad
%global gitdate 20190627
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global __requires_exclude ^lib%{name}.so|^lib%{name}-js.so

%global cjs_version 4.0.0
%global cinnamon_desktop_version 4.0.0
%global gobject_introspection_version 1.38.0
%global muffin_version 4.0.3
%global json_glib_version 0.13.2

# For wallpaper.
%global rawhide_version 31
%global release_version %(echo $((%{rawhide_version} - 1)))

%global __python %{__python3}

Name:           cinnamon
Version:        4.0.12
Release:        202.%{gitdate}git%{shortcommit}%{?dist}
Summary:        Window management and application launching for GNOME
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/linuxmint/%{name}
#Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source0:        %{url}/archive/master.mint19.tar.gz
Source1:        polkit-%{name}-authentication-agent-1.desktop
Source2:        10_cinnamon-common.gschema.override
Source3:        10_cinnamon-apps.gschema.override.in

Patch0:         autostart.patch
Patch1:         set_wheel.patch
#Patch2:         revert_25aef37.patch
Patch3:         default_panal_launcher.patch
Patch4:         remove_crap_from_menu.patch
Patch5:         replace-metacity-with-openbox.patch


BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(cjs-1.0) >= %{cjs_version}
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gnome-bluetooth-1.0)
BuildRequires:  pkgconfig(libgnome-menu-3.0)
BuildRequires:  pkgconfig(lib%{name}-menu-3.0)
BuildRequires:  pkgconfig(%{name}-desktop) >= %{cinnamon_desktop_version}
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(gudev-1.0)

# for screencast recorder functionality
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  intltool
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libcroco-0.6)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libsoup-2.4)

# used in unused BigThemeImage
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libmuffin) >= %{muffin_version}
BuildRequires:  pkgconfig(libpulse)

# Bootstrap requirements
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  gnome-common

# media keys
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(colord)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libwacom)
BuildRequires:  pkgconfig(xorg-wacom)
%endif
BuildRequires:  pkgconfig(xtst)

Requires:       %{name}-desktop >= %{cinnamon_desktop_version}
Requires:       muffin%{?_isa} >= %{muffin_version}
Requires:       cjs%{?_isa} >= %{cjs_version}
Requires:       gnome-menus%{?_isa} >= 3.0.0-2

# wrapper script used to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}

# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}

# needed as it is now split from Clutter
Requires:       json-glib%{?_isa} >= %{json_glib_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= 0.100

# needed for session files
Requires:       %{name}-session%{?_isa}

# needed for schemas
Requires:       at-spi2-atk%{?_isa}

# needed for on-screen keyboard
Requires:       caribou%{?_isa}

# needed for the user menu
Requires:       accountsservice-libs%{?_isa}

# needed for settings
Requires:       python3-pexpect
Requires:       python3-gobject%{?_isa}
Requires:       python3-dbus%{?_isa}
Requires:       python3-lxml%{?_isa}
Requires:       python3-pillow%{?_isa}
Requires:       python3-pam
Requires:       mintlocale
Requires:       %{name}-control-center%{?_isa}
Requires:       %{name}-translations

# needed for theme overrides
%if 0%{?fedora}
Requires:       desktop-backgrounds-basic
Requires:       desktop-backgrounds-gnome
%endif
Requires:       gnome-backgrounds
Requires:       system-logos

# Theming
Requires:       google-noto-sans-fonts
Requires:       %{name}-themes >= 1:1.7.4-0.2.20181112gitb94b890

# RequiredComponents in the session files
Requires:       nemo%{?_isa}
Requires:       %{name}-screensaver%{?_isa}

# openbox and tint2 are needed for fallback
Requires:       openbox%{?_isa}
Requires:       tint2%{?_isa}

# required for keyboard applet
Requires:       gucharmap%{?_isa}
Requires:       xapps%{?_isa}
Requires:       python3-xapps-overrides%{?_isa}

# required for network applet
Requires:       nm-connection-editor%{?_isa}
Requires:       network-manager-applet%{?_isa}

Requires:       python3-inotify


# required for cinnamon-killer-daemon
Requires:       keybinder3%{?_isa}

# required for sound applet
Requires:       wget%{?_isa}

Provides:       desktop-notification-daemon

%description
Cinnamon is a Linux desktop which provides advanced
innovative features and a traditional user experience.

The desktop layout is similar to Gnome 2.
The underlying technology is forked from Gnome Shell.
The emphasis is put on making users feel at home and providing
them with an easy to use and comfortable desktop experience.


%package devel-doc
Summary: Development Documentation files for Cinnamon
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description devel-doc
This package contains the code documentation for various Cinnamon components.


%prep
%autosetup -p1 -n cinnamon-master.mint19

%{__sed} -i -e 's@gksu@pkexec@g' files%{_bindir}/%{name}-settings-users
%{__sed} -i -e 's@gnome-orca@orca@g' files%{_datadir}/%{name}/%{name}-settings/modules/cs_accessibility.py
# remove mintlocale im from settings
%{__sed} -i -e 's@mintlocale im@mintlocale_im_removed@g' files%{_datadir}/%{name}/%{name}-settings/%{name}-settings.py
# fix hard coded paths
%ifarch ppc64
%{__sed} -i -e 's@%{_prefix}/lib/%{name}-control-center@%{_prefix}/lib64/%{name}-control-center@g' \
 files%{_datadir}/%{name}/%{name}-settings/bin/capi.py
%endif

# Fix rpmlint errors
for file in files%{_datadir}/%{name}/%{name}-settings/bin/*.py files%{_datadir}/%{name}/%{name}-looking-glass/*.py \
   files%{_datadir}/%{name}/%{name}-settings/modules/cs_{applets,desklets}.py; do
   chmod a+x $file
done
chmod a-x files%{_datadir}/%{name}/%{name}-settings/bin/__init__.py


NOCONFIGURE=1 ./autogen.sh


%build
%configure \
    --disable-static \
    --disable-schemas-compile \
    --disable-silent-rules \
    --enable-introspection=yes \
    --enable-compile-warnings=no

%make_build


%install
%make_install

# Remove static libs and libtool crap
%{_bindir}/find %{buildroot}%{_libdir} -name '*.a' -print -delete
%{_bindir}/find %{buildroot}%{_libdir} -name '*.la' -print -delete

# install polkit autostart desktop file
%{__install} --target-directory=%{buildroot}%{_datadir}/applications \
    -Dpm 0644 %{SOURCE1}

# install common gschema override
%{__install} --target-directory=%{buildroot}%{_datadir}/glib-2.0/schemas \
    -Dpm 0644 %{SOURCE2}

# install gschema-override for apps
%{__sed} -e 's!@pkg_manager@!org.mageia.dnfdragora.desktop!g' \
    < %{SOURCE3} > %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-apps.gschema.override

# install gschema-override for wallpaper
%{__cat} >> %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-wallpaper.gschema.override << EOF
[org.cinnamon.desktop.background]
%if 0%{?fedora}
%if 0%{?fedora} < %{rawhide_version}
picture-uri='file:///usr/share/backgrounds/f%{?fedora}/default/f%{?fedora}.xml'
%else
picture-uri='file:///usr/share/backgrounds/f%{release_version}/default/f%{release_version}.xml'
%endif
%else
picture-uri='file:///usr/share/backgrounds/default.xml'
%endif
EOF

# Provide symlink for the background-propeties.
%{__ln_s} %{_datadir}/gnome-background-properties %{buildroot}%{_datadir}/%{name}-background-properties


%check
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%doc README.rst AUTHORS
%license COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/menus/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.Cinnamon.*.service
%{_datadir}/desktop-directories/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/%{name}-session/sessions/*
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/polkit-1/actions/org.%{name}.settings-users.policy
%{_datadir}/xsessions/*
%{_datadir}/%{name}/
%{_datadir}/%{name}-background-properties
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/
%{_mandir}/man1/*


%files devel-doc
%doc %{_datadir}/gtk-doc/html/*/


%changelog
* Fri Apr 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.11-0.1.20190405gitc843f36
- Update to git master snapshot

* Wed Apr 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.10-1
- Update to 4.0.10 release

* Mon Mar 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.9-1
- Update to 4.0.9 release

* Mon Mar 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-5
- Bump for f30 backgrounds

* Thu Feb 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-4
- Add monospace font override

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-2
- Tweak panel layout

* Sat Dec 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-1
- Update to 4.0.8 release

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.7-1
- Update to 4.0.7 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.5-1
- Update to 4.0.5 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.4-1
- Update to 4.0.4 release

* Wed Nov 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Wed Nov 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-2
- Switch theme and add version to cinnamon-themes requires

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Sat Nov 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release

