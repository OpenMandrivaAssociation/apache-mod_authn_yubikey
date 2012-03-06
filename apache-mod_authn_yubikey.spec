#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_authn_yubikey
%define load_order 147

Summary:	Authentication provider for Yubicos YubiKey
Name:		apache-%{mod_name}
Version:	0.1
Release: 	12
Group:		System/Servers
License:	Apache License
URL:		http://mod_authn_yubikey.coffeecrew.org/
Source0:	http://mod_authn_yubikey.coffeecrew.org/authn_yubikey.tar.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRequires:	curl-devel
BuildRequires:	libyubikey-devel

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

%build
apxs -c %{mod_name}.c -Wl,-lcurl -Wl,-lyubikey

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule authn_yubikey_module %{_libdir}/%{mod_name}.so
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
