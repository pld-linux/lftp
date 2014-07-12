# TODO
# - package itself defaults to GNUTLS (prefferring over openssl) should we too?
#
# Conditional build:
%bcond_without	ssl	# do not use SSL
%bcond_with	gnutls	# use gnutls, otherwise openssl is used when ssl is on
%bcond_without	dante	# Dante-based SOCKS support
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
Version:	4.5.3
Release:	1
License:	GPL v3+
Group:		Applications/Networking
Source0:	http://lftp.yar.ru/ftp/%{name}-%{version}.tar.xz
# Source0-md5:	dcc20675777a4931116491534463bf46
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	cdad8fb5342eebd9916eccefc98a855b
Source2:	%{name}.desktop
Source3:	%{name}-icon.png
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-m4.patch
Patch2:		aliases.patch
# when updated attach at https://github.com/lavv17/lftp/issues
Patch3:		%{name}-pl.po-update.patch
Patch4:		lftp-4.3.8-gets.patch
Patch5:		%{name}-am.patch
URL:		http://lftp.yar.ru/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%{?with_dante:BuildRequires:	dante-devel}
%{?with_dnssec:BuildRequires:	dnssec-tools-devel}
BuildRequires:	expat-devel
BuildRequires:	gettext-devel >= 0.14.2
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel >= 5.2
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)
%if %{_gcc_ver} == 2
%define		__cxx		"%{__cc}"
%endif

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1
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
	--with-modules \
	--with-socksdante%{!?with_dante:=no} \
	--with%{!?with_openssl:out}-openssl \
	--with%{!?with_gnutls:out}-gnutls

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir},%{_desktopdir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}/lftp.png

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{README.lftp-man-pages,lftpget.diff}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.{la,so}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS FAQ FEATURES BUGS ChangeLog TODO
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
%{_pixmapsdir}/lftp.png
