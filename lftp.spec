Summary:	Commandline ftp client
Summary(pl):	Zaawansowany klient ftp
Name:		lftp
Version:	1.2.4
Release:	3
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Copyright:	GPL
Source:		ftp://ftp.yars.free.net:/pub/software/unix/net/ftp/client/%{name}-%{version}.tar.gz
Icon:		ftp.gif
BuildPrereq:	ncurses-devel
BuildPrereq:	readline-devel
Buildroot:	/tmp/%{name}-%{version}-root

%description
LFTP is a shell-like command line ftp client. The main two advantages over
other ftp clients are reliability and ability to perform tasks in
background. It will reconnect and reget the file being transferred if the
connection broke. You can start a transfer in background and continue
browsing on the ftp site. It does this all in one process. When you have
started background jobs and feel you are done, you can just exit lftp and it
automatically moves to nohup mode and completes the transfers. It has also
such nice features as reput and mirror.

%description -l pl
Lftp jest zaawansowanym klientem ftp. Potrafi automatycznie po³±czyæ siê z 
serwerem ftp po zerwanym po³±czeniu i dokoñczyæ ¶ci±ganie archiwów. Lftp mo¿e 
pracowaæ w tle i nie zrywa przy tym po³±czenia po tym jak siê wylogujesz. 
Program ten honoruje komendy shellowe podczas sesji, np. `ls -al | less` itp. 
Doskonale siê spisuje jako aplikacja do mirrorowania serwerów FTP.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target} \
	--prefix=/usr
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc

make prefix=$RPM_BUILD_ROOT/usr install

install lftp.conf $RPM_BUILD_ROOT/etc

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man1/* \
	README NEWS 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS}.gz

%attr(755,root,root) /usr/bin/*
%{_mandir}/man1/*

%attr(755,root,root) %{_datadir}/lftp

%lang(es)    %{_datadir}/locale/es/LC_MESSAGES/lftp.mo
%lang(ru)    %{_datadir}/locale/ru/LC_MESSAGES/lftp.mo
%lang(it)    %{_datadir}/locale/it/LC_MESSAGES/lftp.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/lftp.mo
%lang(pl)    %{_datadir}/locale/pl/LC_MESSAGES/lftp.mo

%config(noreplace) %verify(not size mtime md5) /etc/lftp.conf
  [1.2.4-4]
%changelog
- more rpm macros,
- added rpm BuildPrereq rules.

* Tue Apr 20 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2.4-3]
- changed Group to Networking/Utilities,
- added resdline-devel to BuildPrereq,
- removed %%requires_pkg (dependences for ncurses is generted automatycally).

* Mon Apr 20 1999 Piotr Czerwiñski <pius@pld.org.pl>
- recompiled on rpm 3,
- added %requires_pkg macro and BuildPrereq,
- replacements in %files.

* Thu Mar 18 1999 Micha³ Kuratczyk <kura@pld.org.pl>
  [1.2.4-2]
- gzipping documentation (instead bzipping)

* Tue Feb 23 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2.4-1]
- removed man group from man pages,
- added "Requires: ncurses => 4.2-12" for prevent using lftp with proper
  version ncurses,
- removed "rm -rf $RPM_BUILD_ROOT" from %prep,
- simplification in %files,
- changed %lang to pt_BR on pt_BR lftp.mo.

* Fri Jun 12 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
- moved %changelog at the end of spec.
- build against glibc-2.1,
- translation modified for pl,
- moved %changelog at the end of spec.
