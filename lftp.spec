#
# Conditional build:
%bcond_without ssl	# do not use SSL
#
Summary:	Sophisticated command line ftp/http client
Summary(ko):	¸í·ÉÁÙ¿¡¼­ µ¹¾Æ°¡´Â ftp/http Å¬¶óÀÌ¾ðÆ®
Summary(pl):	Zaawansowany klient ftp/http
Summary(pt_BR):	Sofisticado programa de transferência de arquivos (cliente ftp/http)
Summary(zh_CN):	lftp ¿Í»§¶Ë³ÌÐò
Name:		lftp
Version:	3.0.4
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.bz2
# Source0-md5:	382a08fed9f7396971996ad1ba12aefb
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	cdad8fb5342eebd9916eccefc98a855b
Source2:	%{name}.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-pl.po-update.patch
Icon:		ftp.gif
URL:		http://lftp.yar.ru/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel >= 5.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	readline-devel >= 4.2
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)
%if %{_gcc_ver} == 2
%define		__cxx		"%{__cc}"
%endif

%description
LFTP is a shell-like command line ftp/http client. The main two
advantages over other ftp clients are reliability and ability to
perform tasks in background. It will reconnect and reget the file
being transferred if the connection broke. You can start a transfer in
background and continue browsing on the ftp site. It does this all in
one process. When you have started background jobs and feel you are
done, you can just exit lftp and it automatically moves to nohup mode
and completes the transfers. It has also such nice features as reput
and mirror.

%description -l pl
Lftp jest zaawansowanym klientem ftp/http. Potrafi automatycznie
po³±czyæ siê z serwerem ftp po zerwanym po³±czeniu i dokoñczyæ
¶ci±ganie archiwów. Lftp mo¿e pracowaæ w tle i nie zrywa przy tym
po³±czenia po tym jak siê wylogujesz. Program ten honoruje komendy
pow³oki podczas sesji, np. `ls -al | less` itp. Doskonale siê spisuje
jako aplikacja do mirrorowania serwerów FTP.

%description -l pt_BR
O lftp é um programa de transferência de arquivos por linha de
comando. Ele suporta os protocolos ftp/http. Suporta: proxy ftp, proxy
http, ftp sobre http, opie/skey, transferências fxp, repetição de
tentativa automática em erros não-fatais e timeouts, ipv6, socks. Veja
o arquivo FEATURES para uma lista mais detalhada.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
sed -i -e 's#pkgverlibdir.*=.*#pkgverlibdir = $(pkglibdir)#g' src/Makefile*

# allow pl.gmo regeneration
rm -f po/stamp-po

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions -fno-implicit-templates"
%configure \
	--with-modules \
	--with%{!?with_ssl:out}-ssl
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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS FAQ FEATURES BUGS ChangeLog TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lftp.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/lftp
%attr(755,root,root) %{_libdir}/lftp/*.so
%attr(755,root,root) %{_datadir}/lftp
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_desktopdir}/lftp.desktop
%{_pixmapsdir}/lftp.png
