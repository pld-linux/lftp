Summary:	Commandline ftp client
Summary(pl):	Zaawansowany klient ftp
Name:		lftp
Version:	2.1.10
Release:	2
License:	GPL
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Source:		http://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.bz2
Patch:		lftp-passive.patch
Icon:		ftp.gif
URL:		http://ftp.yars.free.net/projects/lftp/
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel >= 4.1
BuildRequires:	gettext-devel
Buildroot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
LFTP is a shell-like command line ftp client. The main two advantages over
other ftp clients are reliability and ability to perform tasks in
background. It will reconnect and reget the file being transferred if the
connection broke. You can start a transfer in background and continue
browsing on the ftp site. It does this all in one process. When you have
started background jobs and feel you are done, you can just exit lftp and
it automatically moves to nohup mode and completes the transfers. It has
also such nice features as reput and mirror.

%description -l pl
Lftp jest zaawansowanym klientem ftp. Potrafi automatycznie po³±czyæ siê z
serwerem ftp po zerwanym po³±czeniu i dokoñczyæ ¶ci±ganie archiwów. Lftp
mo¿e pracowaæ w tle i nie zrywa przy tym po³±czenia po tym jak siê
wylogujesz. Program ten honoruje komendy pow³oki podczas sesji, np. `ls
-al | less` itp. Doskonale siê spisuje jako aplikacja do mirrorowania
serwerów FTP.

%prep
%setup -q
%patch -p1

%build
gettextize --copy --force
LDFLAGS="-s"; export LDFLAGS
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions -fno-implicit-templates"; export CXXFLAGS
%configure \
	--with-modules
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

make install DESTDIR=$RPM_BUILD_ROOT

install lftp.conf $RPM_BUILD_ROOT%{_sysconfdir}

chmod +x $RPM_BUILD_ROOT%{_libdir}/lftp/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/* \
	README NEWS

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {README,NEWS}.gz

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lftp.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%attr(755,root,root) %{_datadir}/lftp

%dir %{_libdir}/lftp
%attr(755,root,root) %{_libdir}/lftp/*.so
