#
# Conditional build:
# _without_ssl - do not use SSL
#
Summary:	Commandline ftp client
Summary(ko):	명령줄에서 돌아가는 FTP/HTTP 클라이언트
Summary(pl):	Zaawansowany klient ftp
Summary(pt_BR):	Sofisticado programa de transfer�ncia de arquivos (cliente ftp/http)
Summary(zh_CN):	lftp 와빵똥넋埼
Name:		lftp
Version:	2.6.4
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.bz2
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Patch0:		%{name}-amfix.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-pl.patch
Icon:		ftp.gif
URL:		http://lftp.yar.ru/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel >= 5.2
%{!?_without_ssl:BuildRequires:	openssl-devel >= 0.9.7}
BuildRequires:	readline-devel >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)
%if %{_gcc_ver} == 2
%define		__cxx		"%{__cc}"
%endif

%description
LFTP is a shell-like command line ftp client. The main two advantages
over other ftp clients are reliability and ability to perform tasks in
background. It will reconnect and reget the file being transferred if
the connection broke. You can start a transfer in background and
continue browsing on the ftp site. It does this all in one process.
When you have started background jobs and feel you are done, you can
just exit lftp and it automatically moves to nohup mode and completes
the transfers. It has also such nice features as reput and mirror.

%description -l pl
Lftp jest zaawansowanym klientem ftp. Potrafi automatycznie po낢czy�
si� z serwerem ftp po zerwanym po낢czeniu i doko�czy� 턢i켫anie
archiw�w. Lftp mo풽 pracowa� w tle i nie zrywa przy tym po낢czenia po
tym jak si� wylogujesz. Program ten honoruje komendy pow쿽ki podczas
sesji, np. `ls -al | less` itp. Doskonale si� spisuje jako aplikacja
do mirrorowania serwer�w FTP.

%description -l pt_BR
O lftp � um programa de transfer�ncia de arquivos por linha de
comando. Ele suporta os protocolos FTP e HTTP. Suporta: proxy ftp,
proxy http, ftp sobre http, opie/skey, transfer�ncias fxp, repeti豫o
de tentativa autom�tica em erros n�o-fatais e timeouts, ipv6, socks.
Veja o arquivo FEATURES para uma lista mais detalhada.

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS FAQ FEATURES BUGS ChangeLog TODO
%attr(755,root,root) %{_bindir}/*
# All modules specified here because lftp breaks things
%attr(755,root,root) %{_libdir}/lftp/%{version}/cmd-mirror.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/cmd-sleep.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/libnetwork.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/proto-file.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/proto-fish.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/proto-ftp.so
%attr(755,root,root) %{_libdir}/lftp/%{version}/proto-http.so

%attr(755,root,root) %{_datadir}/lftp
%dir %{_libdir}/lftp
%dir %{_libdir}/lftp/%{version}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lftp.conf
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
