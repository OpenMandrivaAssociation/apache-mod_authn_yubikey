#Module-Specific definitions
%define mod_name mod_authn_yubikey
%define mod_conf B47_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Authentication provider for Yubicos YubiKey
Name:		apache-%{mod_name}
Version:	0.1
Release: 	20
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
BuildRequires:	libyubikey-devel
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
%{_bindir}/apxs -c %{mod_name}.c -Wl,-lcurl -Wl,-lyubikey

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


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-10mdv2011.0
+ Revision: 674425
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-9
+ Revision: 662773
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-8mdv2011.0
+ Revision: 588279
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-7mdv2010.1
+ Revision: 515834
- rebuilt for apache-2.2.15

* Wed Oct 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.1-6mdv2010.0
+ Revision: 455759
- rebuild for new curl SSL backend

* Sun Aug 02 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-5mdv2010.0
+ Revision: 407524
- fix deps and build
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-4mdv2009.1
+ Revision: 325573
- rebuild

* Mon Sep 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-3mdv2009.0
+ Revision: 285021
- rebuilt due to common build system fjukiness
- rebuild

* Mon Sep 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2009.0
+ Revision: 284929
- import apache-mod_authn_yubikey


* Mon Sep 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2009.0
- initial Mandriva package
