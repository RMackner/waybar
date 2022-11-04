%define githash d48eebd4d3d92d7a8f39cf28574dd8543c105b8a

%define shorthash %(c=%{githash}; echo ${c:0:10})

Name:           waybar
Version:        0.9.15
Release:        1.git.%{shorthash}%{?dist}
Summary:        Highly customizable Wayland bar for Sway and Wlroots based compositors
License:        MIT
URL:            https://github.com/Alexays/Waybar
Source0:        %{url}/archive/%{githash}/%{name}-%{githash}.tar.gz
Conflicts:      waybar

Requires: gtkmm30
Requires: jsoncpp
Requires: libsigc++20
Requires: fmt
Requires: libdate-tz
Requires: spdlog
Requires: gtk-layer-shell
Requires: upower
Requires: libevdev
Requires: pulseaudio-libs
Requires: libnl3
Requires: libappindicator-gtk3
Requires: libdbusmenu-gtk3
Requires: libmpdclient
Requires: libxkbcommon

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.47.0
BuildRequires:  scdoc
BuildRequires:  cmake
BuildRequires:  systemd-rpm-macros
BuildRequires:  libsigc++
BuildRequires:  upower
BuildRequires:  libappindicator-gtk3
BuildRequires:  libdbusmenu-gtk3
BuildRequires:  libxkbcommon
BuildRequires:  catch-devel
BuildRequires:  pipewire-jack-audio-connection-kit

BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(fmt) >= 5.3.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(date)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(spdlog) >= 1.3.1
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libmpdclient)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pipewire-jack-audio-connection-kit-devel

Recommends:     fontawesome-fonts

%description
%{summary}

%prep
%autosetup -n Waybar-%{githash}
sed -i 's/zext_workspace_handle_v1_activate(workspace_handle_);/const std::string command = "hyprctl dispatch workspace " + name_;\n\tsystem(command.c_str());/g' src/modules/wlr/workspace_manager.cpp # use hyprctl to switch workspaces

%build
MESON_OPTIONS=(
    -Dsndio=disabled
    -Dexperimental=true
)
%{meson} "${MESON_OPTIONS[@]}"
%meson_build

%install
%meson_install

%files
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/config
%config(noreplace) %{_sysconfdir}/xdg/%{name}/style.css
%{_bindir}/%{name}
%{_mandir}/man5/%{name}*
# FIXME: exclude user service until a proper way to start it has been decided
# see rhbz#1798811 for more context
%exclude %{_userunitdir}/%{name}.service

%changelog
