Summary:     Commandline ftp client.
Summary(pl): Zaawansowany klient ftp
Name:        lftp
Version:     1.2.2
Release:     1
Copyright:   GPL
Group:       Applications/Networking
Group(pl):   Aplikacje/Sieæ
Source:      ftp://ftp.yars.free.net:/pub/software/unix/net/ftp/client/%{name}-%{version}.tar.gz
Icon:        ftp.gif
BuildRoot:   /tmp/%{name}-%{version}-root

%description
LFTP is a shell-like command line ftp client. The main two advantages over
other ftp clients are reliability and ability to perform tasks in
background. It will reconnect and reget the file being transferred if the
connection broke. You can start a transfer in background and continue
browsing on the ftp site.  It does this all in one process. When you have
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
CXXFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
make prefix=$RPM_BUILD_ROOT/usr install
install lftp.conf $RPM_BUILD_ROOT/etc

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc README NEWS 
%config(noreplace) %verify(not size mtime md5) /etc/lftp.conf
%attr(755, root, root) /usr/bin/*
%attr(755, root, root, 755) /usr/share/lftp
%attr(644, root,  man) /usr/man/man1/*
%lang(es) /usr/share/locale/es/LC_MESSAGES/lftp.mo
%lang(it) /usr/share/locale/it/LC_MESSAGES/lftp.mo
%lang(pl) /usr/share/locale/pl/LC_MESSAGES/lftp.mo
%lang(pt) /usr/share/locale/pt*/LC_MESSAGES/lftp.mo
%lang(ru) /usr/share/locale/ru/LC_MESSAGES/lftp.mo

%changelog
* Wed Dec  9 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2-1]
- added gzipping man pages,
- added using LDFLAGS="-s" to ./configure enviroment,
- added /usr/share/lftp to %files,
- recompiled against libstdc++.so.2.9.0,
- added /usr/share/locale/pl/LC_MESSAGES/lftp.mo to %files.

* Mon Nov  2 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.0.1-2]
- fixed passing $RPM_OPT_FLAGS,
- added Group(pl).
- removed "rm -rf $RPM_BUILD_ROOT" from %prep,
- simplification in %files,
  [1.0.1-1]
- added %lang macros for /usr/share/locale/*/LC_MESSAGES/lftp.mo files,
- added pl translation.- build against glibc-2.1,
- translation modified for pl,
- moved %changelog at the end of spec.
