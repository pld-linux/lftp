#
# Conditional build:
# _without_ssl - do not use SSL
#
Summary:	Sophisticated command line ftp/http client
Summary(ko):	����ٿ��� ���ư��� ftp/http Ŭ���̾�Ʈ
Summary(pl):	Zaawansowany klient ftp/http
Summary(pt_BR):	Sofisticado programa de transfer�ncia de arquivos (cliente ftp/http)
Summary(zh_CN):	lftp �ͻ��˳���
Name:		lftp
Version:	2.6.7
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.bz2
# Source0-md5:	31092e7f94b80f8f79c5e71fc7ba636f
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	cdad8fb5342eebd9916eccefc98a855b
Source2:	%{name}.desktop
Patch0:		%{name}-amfix.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-no_pkgverlibdir.patch
Icon:		ftp.gif
URL:		http://lftp.yar.ru/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel >= 5.2
%{!?_without_ssl:BuildRequires:	openssl-devel >= 0.9.7c}
BuildRequires:	readline-devel >= 4.2
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
po��czy� si� z serwerem ftp po zerwanym po��czeniu i doko�czy�
�ci�ganie archiw�w. Lftp mo�e pracowa� w tle i nie zrywa przy tym
po��czenia po tym jak si� wylogujesz. Program ten honoruje komendy
pow�oki podczas sesji, np. `ls -al | less` itp. Doskonale si� spisuje
jako aplikacja do mirrorowania serwer�w FTP.

%description -l pt_BR
O lftp � um programa de transfer�ncia de arquivos por linha de
comando. Ele suporta os protocolos ftp/http. Suporta: proxy ftp, proxy
http, ftp sobre http, opie/skey, transfer�ncias fxp, repeti��o de
tentativa autom�tica em erros n�o-fatais e timeouts, ipv6, socks. Veja
o arquivo FEATURES para uma lista mais detalhada.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions -fno-implicit-templates"
%configure \
	--with-modules \
	--with%{?_without_ssl:out}-ssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir},%{_applnkdir}/Network/FTP}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}
install contrib/lftp-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/lftp.png
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/FTP

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
%attr(755,root,root) %{_libdir}/lftp/cmd-mirror.so
%attr(755,root,root) %{_libdir}/lftp/cmd-sleep.so
%attr(755,root,root) %{_libdir}/lftp/libnetwork.so
%attr(755,root,root) %{_libdir}/lftp/proto-file.so
%attr(755,root,root) %{_libdir}/lftp/proto-fish.so
%attr(755,root,root) %{_libdir}/lftp/proto-ftp.so
%attr(755,root,root) %{_libdir}/lftp/proto-http.so
%attr(755,root,root) %{_datadir}/lftp
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_applnkdir}/Network/FTP/lftp.desktop
%{_pixmapsdir}/lftp.png
