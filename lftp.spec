# TODO
# - package itself defaults to GNUTLS (prefferring over openssl) should we too?
#
# Conditional build:
%bcond_with	tests
%bcond_without	ssl	# do not use SSL
%bcond_with	gnutls	# use gnutls, otherwise openssl is used when ssl is on
# better just preload it instead forcing linking
%bcond_with	dante	# Dante-based SOCKS support
# broken currently https://www.dnssec-tools.org/trac/ticket/173
%bcond_with	dnssec	# DNSSEC local validation
#
%if %{with ssl}
%define with_openssl 1
%endif

%if %{with gnutls} && %{with ssl}
%undefine with_openssl
%endif

Summary:	Sophisticated command line FTP/HTTP client
Summary(ko.UTF-8):	명령줄에서 돌아가는 FTP/HTTP 클라이언트
Summary(pl.UTF-8):	Zaawansowany klient FTP/HTTP
Summary(pt_BR.UTF-8):	Sofisticado programa de transferência de arquivos (cliente FTP/HTTP)
Summary(zh_CN.UTF-8):	lftp 客户端程序
Name:		lftp
Version:	4.9.3
Release:	1
License:	GPL v3+
Group:		Applications/Networking
Source0:	https://lftp.yar.ru/ftp/%{name}-%{version}.tar.xz
# Source0-md5:	f2e4ffa81b68106a14d354d50635bbf4
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	cdad8fb5342eebd9916eccefc98a855b
Patch100:	%{name}-git.patch
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-m4.patch
Patch2:		aliases.patch
# when updated attach at https://github.com/lavv17/lftp/issues
Patch3:		%{name}-pl.po-update.patch
Patch4:		%{name}-desktop.patch
Patch5:		gnulib-duplicate-symbols.patch
URL:		http://lftp.tech/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
%{?with_dante:BuildRequires:	dante-devel}
%{?with_dnssec:BuildRequires:	dnssec-tools-devel}
BuildRequires:	expat-devel
BuildRequires:	gettext-tools >= 0.14.2
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
BuildRequires:	libidn2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	ncurses-devel >= 5.2
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 5.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LFTP is a shell-like command line FTP/HTTP client. The main two
advantages over other FTP clients are reliability and ability to
perform tasks in background. It will reconnect and reget the file
being transferred if the connection broke. You can start a transfer in
background and continue browsing on the FTP site. It does this all in
one process. When you have started background jobs and feel you are
done, you can just exit lftp and it automatically moves to nohup mode
and completes the transfers. It has also such nice features as reput
and mirror.

%description -l pl.UTF-8
Lftp jest zaawansowanym klientem FTP/HTTP. Potrafi automatycznie
połączyć się z serwerem FTP po zerwanym połączeniu i dokończyć
ściąganie archiwów. Lftp może pracować w tle i nie zrywa przy tym
połączenia po tym jak się wylogujesz. Program ten honoruje komendy
powłoki podczas sesji, np. `ls -al | less` itp. Doskonale się spisuje
jako aplikacja do mirrorowania serwerów FTP.

%description -l pt_BR.UTF-8
O lftp é um programa de transferência de arquivos por linha de
comando. Ele suporta os protocolos FTP/HTTP. Suporta: proxy FTP, proxy
HTTP, FTP sobre HTTP, opie/skey, transferências fxp, repetição de
tentativa automática em erros não-fatais e timeouts, ipv6, socks. Veja
o arquivo FEATURES para uma lista mais detalhada.

%prep
%setup -q
#%patch100 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__rm} po/stamp-po

%{!?with_gnutls:echo 'AC_DEFUN([AM_PATH_LIBGNUTLS],[/bin/true])' > m4/gnutls.m4}

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure \
	--without-included-regex \
	--with-dnssec-local-validation%{!?with_dnssec:=no} \
	--with-gnutls%{!?with_gnutls:=no} \
	--with-modules \
	--with-openssl%{!?with_openssl:=no} \
	--with-socksdante%{!?with_dante:=no}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{README.lftp-man-pages,lftpget.diff}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.{la,so}

# don't drag in perl deps
%{__rm} $RPM_BUILD_ROOT%{_datadir}/lftp/{convert-mozilla-cookies,verify-file}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog FAQ FEATURES NEWS README README.debug-levels README.dnssec THANKS TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lftp.conf
%attr(755,root,root) %{_bindir}/lftp
%attr(755,root,root) %{_bindir}/lftpget
%attr(755,root,root) %{_libdir}/liblftp*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblftp*.so.0
%dir %{_libdir}/lftp
%attr(755,root,root) %{_libdir}/lftp/*.so
%attr(755,root,root) %{_datadir}/lftp
%{_mandir}/man1/lftp.1*
%{_mandir}/man1/lftpget.1*
%lang(pl) %{_mandir}/pl/man1/lftpget.1*
%{_mandir}/man5/lftp.conf.5*
%{_desktopdir}/lftp.desktop
%{_iconsdir}/hicolor/48x48/apps/lftp-icon.png
%{zsh_compdir}/_lftp
