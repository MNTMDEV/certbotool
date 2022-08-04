Name:           certbotool-plugins
Version:        1.0.0
Release:        1
Summary:        certbot renew hook plugin support
Group:          Unspecified
License:        GPL
URL:            https://rpm.mntmdev.com/
Source0:        certbotool.tar.gz
BuildRoot:      %{_topdir}/BUILDROOT
BuildRequires:  python3
Requires:       certbot
%description
certbot renew hook plugin support

%define debug_package %{nil}
%define _binpath /usr/bin
%define _defaultcfgpath /etc/certbotool/conf.d

%prep
%setup -c -q

%build
pyinstaller -F src/certbotool-dnspod.py
pyinstaller -F src/certbotool-aliyun.py

%install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}%{_binpath}
mkdir -p %{buildroot}%{_defaultcfgpath}

cp dist/* %{buildroot}%{_binpath}

cp deploy/dnspod.json.template %{buildroot}%{_defaultcfgpath}
cp deploy/aliyun.json.template %{buildroot}%{_defaultcfgpath}

%clean
rm -rf %{buildroot}/*

%files
%{_binpath}/*
%{_defaultcfgpath}/*