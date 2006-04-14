# TODO
# - package itself defaults to GNUTLS (prefferring over openssl) should we too?
#
# Conditional build:
%bcond_without	ssl	# do not use SSL
%bcond_with	gnutls	# use gnutls, otherwise openssl is used when ssl is on

%if %{with ssl}
%define with_openssl 1
%endif

%if %{with gnutls} && %{with ssl}
%undefine with_openssl
%endif

Summary:	Sophisticated command line FTP/HTTP client
Summary(ko):	¸í·ÉÁÙ¿¡¼­ µ¹¾Æ°¡´Â FTP/HTTP Å¬¶óÀÌ¾ðÆ®
Summary(pl):	Zaawansowany klient FTP/HTTP
Summary(pt_BR):	Sofisticado programa de transferência de arquivos (cliente FTP/HTTP)
Summary(zh_CN):	lftp ¿Í»§¶Ë³ÌÐò
Name:		lftp
Version:	3.4.4
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.yars.free.net/pub/source/lftp/%{name}-%{version}.tar.bz2
# Source0-md5:	84af5617bba109b18b5d5f28f55d26e9
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	cdad8fb5342eebd9916eccefc98a855b
Source2:	%{name}.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-pl.po-update.patch
URL:		http://lftp.yar.ru/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.14.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel >= 5.2
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
BuildRequires:	readline-devel >= 4.2
BuildRequires:	sed >= 4.0
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

%description -l pl
Lftp jest zaawansowanym klientem FTP/HTTP. Potrafi automatycznie
po³±czyæ siê z serwerem FTP po zerwanym po³±czeniu i dokoñczyæ
¶ci±ganie archiwów. Lftp mo¿e pracowaæ w tle i nie zrywa przy tym
po³±czenia po tym jak siê wylogujesz. Program ten honoruje komendy
pow³oki podczas sesji, np. `ls -al | less` itp. Doskonale siê spisuje
jako aplikacja do mirrorowania serwerów FTP.

%description -l pt_BR
O lftp é um programa de transferência de arquivos por linha de
comando. Ele suporta os protocolos FTP/HTTP. Suporta: proxy FTP, proxy
HTTP, FTP sobre HTTP, opie/skey, transferências fxp, repetição de
tentativa automática em erros não-fatais e timeouts, ipv6, socks. Veja
o arquivo FEATURES para uma lista mais detalhada.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
rm -f po/stamp-po

sed -i -e 's#pkgverlibdir.*=.*#pkgverlibdir = $(pkglibdir)#g' src/Makefile*
# for gettext >= 0.14.2
sed -i -e 's/jm_AC/gl_AC/' m4/human.m4

%{!?with_gnutls:echo 'AC_DEFUN([AM_PATH_LIBGNUTLS],[/bin/true])' > m4/gnutls.m4}

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions -fno-implicit-templates"
%configure \
	--with-modules \
	--with%{!?with_ssl:out}-ssl \
	--with%{!?with_openssl:out}-openssl \
	--with%{!?with_gnutls:out}-gnutls

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}
install contrib/lftp-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/lftp.png
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS FAQ FEATURES BUGS ChangeLog TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lftp.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/lftp
%attr(755,root,root) %{_libdir}/liblftp*.so.*.*.*
%attr(755,root,root) %{_libdir}/lftp/*.so
%attr(755,root,root) %{_datadir}/lftp
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_desktopdir}/lftp.desktop
%{_pixmapsdir}/lftp.png
