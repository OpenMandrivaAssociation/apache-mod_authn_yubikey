#Module-Specific definitions
%define mod_name mod_authn_yubikey
%define mod_conf B47_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Authentication provider for Yubicos YubiKey
Name:		apache-%{mod_name}
Version:	0.1
Release: 	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://mod_authn_yubikey.coffeecrew.org/
Source0:	http://mod_authn_yubikey.coffeecrew.org/authn_yubikey.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	curl-devel
BuildRequires:	libyubikey-client-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The mod_authn_yubikey module is an authentication provider for the apache 2.2
platform. It leverages the YubiKey which is a small token that acts as an
authentication device. By enabling your apache installation with this module
you can use your YubiKey for authentication with your website. The
mod_authn_yubikey module provides one and two factor authentication for your
website and is completely independend from the technlogy that implements your
website (like CGI, JSP or PHP). In your backend application you can read the
HTTP_X_YUBI_AUTH_TYPE header, which is either OneFactor or TwoFactor stating
that the user authenticated using either just the Yubikey itself or in
conjunction with an additional password, where TwoFactor would be sent instead.

%prep

%setup -q -n authn_yubikey

cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c %{mod_name}.c -lyubikey-client

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
