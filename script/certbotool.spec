Name:           certbotool
Version:        1.0.0
Release:        1
Summary:        certbot CLI toolkit
Group:          Unspecified
License:        GPL
URL:            https://rpm.mntmdev.com/
Source0:        certbotool.tar.gz
BuildRoot:      %{_topdir}/BUILDROOT
BuildRequires:  python3
Requires:       certbot
%description
certbot CLI toolkit

%define debug_package %{nil}
%define _binpath /usr/bin

%prep
%setup -c -q

%build
pyinstaller -F src/certbotool.py

%install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}%{_binpath}

cp dist/* %{buildroot}%{_binpath}

%clean
rm -rf %{buildroot}/*

%files
%{_binpath}/*
