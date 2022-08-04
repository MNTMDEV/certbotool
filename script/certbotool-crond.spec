Name:           certbotool-crond
Version:        1.0.0
Release:        1
Summary:        certbot automatic certificate renew helper service
Group:          System Environment/Daemons
License:        GPL
URL:            https://rpm.mntmdev.com/
Source0:        certbotool.tar.gz
BuildRoot:      %{_topdir}/BUILDROOT
BuildRequires:  python3
Requires:       certbot
%description
certbot automatic certificate renew helper service

%define debug_package %{nil}
%define _binpath /usr/bin
%define _servicepath /usr/lib/systemd/system
%define _cfgpath /etc/certbotool

%prep
%setup -c -q

%build
pyinstaller -F src/certbotool-crond.py

%install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}%{_binpath}
mkdir -p %{buildroot}%{_servicepath}
mkdir -p %{buildroot}%{_cfgpath}

cp dist/* %{buildroot}%{_binpath}
cp deploy/%{name}.service %{buildroot}%{_servicepath}
cp deploy/daemon.json %{buildroot}%{_cfgpath}

%clean
rm -rf %{buildroot}/*

%files
%{_binpath}/*
%{_servicepath}/*
%{_cfgpath}/*