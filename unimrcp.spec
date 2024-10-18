%define major            0
%define libasrclient     asrclient
%define libunimrcpclient unimrcpclient 
%define libunimrcpserver unimrcpserver
%define devel            %{name} 

# filter out lib requires provided by bundled libs from unimrcp-deps
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}lib(apr(|util)-1|sofia-sip-ua)\.so\.[0-9]\+

Name:           unimrcp
Version:        1.8.0
Release:        1
Summary:        Media Resource Control Protocol Stack
License:        Apache
Group:          System/Servers
Url:            http://unimrcp.org
Source0:        http://unimrcp.org/project/component-view/%{name}-1-7-0-tar-gz/download#/%{name}-%{version}.tar.gz
Source1:        %{name}server.service

#BuildRequires:  libunimrcp-deps-devel
BuildRequires:  pkgconfig(expat)
#BuildRequires:  pkgconfig(pocketsphinx)
BuildRequires:  pkgconfig(sndfile)
#BuildRequires:  pkgconfig(sphinxbase)

#Requires:       libunimrcp-deps

%description
Media Resource Control Protocol (MRCP) allows to control media processing
resources over the network using distributed client/server architecture.

Media processing resources include:
- Speech Synthesizer (TTS)
- Speech Recognizer (ASR)
- Speaker Verifier (SV)
- Speech Recorder (SR)

MRCP is not a stand alone protocol and it relies on various VoIP protocols
such as:
- SIP (MRCPv2), RTSP (MRCPv1) session management
- SDP offer/answer model
- RTP media streaming

UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.

#----------------------------------------------------------------------------

%package      %{libasrclient}
Summary:        Media Resource Control Protocol Stack shared library
Group:          System/Libraries

%description  %{libasrclient}
Media Resource Control Protocol Stack shared library.

#----------------------------------------------------------------------------

%package      %{libunimrcpclient}
Summary:        Media Resource Control Protocol Stack shared library
Group:          System/Libraries

%description  %{libunimrcpclient}
Media Resource Control Protocol Stack shared library.

#----------------------------------------------------------------------------

%package      %{libunimrcpserver}
Summary:        Media Resource Control Protocol Stack shared library
Group:          System/Libraries

%description  %{libunimrcpserver}
Media Resource Control Protocol Stack shared library.

#----------------------------------------------------------------------------

%package      %{devel}
Summary:        Media Resource Control Protocol Stack development
Group:          Development/C
#Requires:       %{libasrclient} = %{version}-%{release}
#Requires:       %{libunimrcpclient} = %{version}-%{release}
#Requires:       %{libunimrcpserver} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}

%description  %{devel}
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.
This package contains development part of UniMRCP.

%prep
%setup -q

%build
# fix build on aarch64
autoreconf -vfi -Ibuild/acmacros

#export PKG_CONFIG_PATH="%{_libdir}/unimrcp-deps/lib/pkgconfig${PKG_CONFIG_PATH}"
#export PATH=%{_libdir}/unimrcp-deps/bin/${PATH:+:${PATH}}
#export LDFLAGS="%{build_ldflags} -Wl,-rpath -Wl,%{_libdir}/unimrcp-deps/lib"
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --with-apr=/opt/unimrcp \
    --with-apr-util=/opt/unimrcp \
    --with-sofia-sip=/opt/unimrcp/lib64/pkgconfig/sofia-sip-ua.pc \
    --disable-silent-rules \
    --disable-static

%make_build

%install
%make_install

mv -f %{buildroot}%{_prefix}/share %{buildroot}%{_sysconfdir}/%{name}/
mv -f %{buildroot}%{_prefix}/log %{buildroot}%{_sysconfdir}/%{name}/
mv -f %{buildroot}%{_prefix}/plugin %{buildroot}%{_sysconfdir}/%{name}/

#install -D -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}server.service

# we don't want these
find %{buildroot} -name '*.la' -delete

%files
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/client-profiles
%dir %{_sysconfdir}/%{name}/umc-scenarios
%config(noreplace) %{_sysconfdir}/%{name}/*.xml
%config(noreplace) %{_sysconfdir}/%{name}/*.xsd
%config(noreplace) %{_sysconfdir}/%{name}/client-profiles/*.xml
%config(noreplace) %{_sysconfdir}/%{name}/umc-scenarios/*.xml
%{_bindir}/*
%{_sysconfdir}/%{name}/plugin
%{_sysconfdir}/%{name}/share
%{_sysconfdir}/%{name}/log
#%attr(0644,root,root) %{_unitdir}/%{name}server.service

%files %{libasrclient}
%{_libdir}/libasrclient.so.%{major}{,.*}

%files %{libunimrcpclient}
%{_libdir}/libunimrcpclient.so.%{major}{,.*}

%files %{libunimrcpserver}
%{_libdir}/libunimrcpserver.so.%{major}{,.*}

%files %{devel}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Sep 22 2022 wally <wally> 1.7.0-2.mga9
+ Revision: 1891678
- filter out lib requires provided by bundled libs from unimrcp-deps
- add RPATH to use libs from unimrcp-deps instead of system ones
- fix build after unimrcp-deps libs location change
- drop old conflicts and obsoletes

* Thu Sep 22 2022 papoteur <papoteur> 1.7.0-1.mga9
+ Revision: 1891438
- new 1.7.0
+ umeabot <umeabot>
- Mageia 9 Mass Rebuild

* Fri Feb 14 2020 umeabot <umeabot> 1.5.0-4.mga8
+ Revision: 1517711
- Mageia 8 Mass Rebuild
+ wally <wally>
- replace deprecated %%configure2_5x

* Sun Sep 23 2018 umeabot <umeabot> 1.5.0-3.mga7
+ Revision: 1301523
- Mageia 7 Mass Rebuild

* Tue Jul 10 2018 wally <wally> 1.5.0-2.mga7
+ Revision: 1242924
- fix build on aarch64

* Wed May 30 2018 daviddavid <daviddavid> 1.5.0-1.mga7
+ Revision: 1233135
- new version: 1.5.0
- disable static libraries and drop '.la' files
- split out all libraries into their own sub-pkgs
- switch to systemd service
+ wally <wally>
- rebuild for new sphinxbase/pocketsphinx 0.9 5prealpha

* Mon Feb 08 2016 umeabot <umeabot> 1.0.0-8.mga6
+ Revision: 943240
- Mageia 6 Mass Rebuild

* Wed Oct 15 2014 umeabot <umeabot> 1.0.0-7.mga5
+ Revision: 744563
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 1.0.0-6.mga5
+ Revision: 690045
- Mageia 5 Mass Rebuild

* Wed Aug 13 2014 wally <wally> 1.0.0-5.mga5
+ Revision: 662376
- move devel files to devel pkg

* Fri Oct 18 2013 umeabot <umeabot> 1.0.0-4.mga4
+ Revision: 519893
- Mageia 4 Mass Rebuild
+ luigiwalser <luigiwalser>
- BR sndfile-devel

* Mon Jan 14 2013 umeabot <umeabot> 1.0.0-2.mga3
+ Revision: 385065
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Sun Jan 06 2013 dlucio <dlucio> 1.0.0-1.mga3
+ Revision: 340029
- 1.0.0

* Sun Apr 29 2012 colin <colin> 0.1815-3.mga2
+ Revision: 234216
- Add LSB headers to initscripts (mga#5262)

* Mon Apr 02 2012 pterjan <pterjan> 0.1815-2.mga2
+ Revision: 227812
- Rebuild after libexpat.la removal

* Sun Mar 25 2012 dlucio <dlucio> 0.1815-1.mga2
+ Revision: 226319
- BR fixes
- We remove useless conflicting dep
- imported package unimrcp


* Wed Feb 15 2012 zamir <zamir@mandriva.org> 0.1815-1mdv2012.0
+ Revision: 774466
- need rebuild
- need rebuild

* Sun Aug 21 2011 zamir <zamir@mandriva.org> 0.1815-0
+ Revision: 696000
- add dependency
- build new pkg version

* Wed Apr 20 2011 zamir <zamir@mandriva.org> 0.1798-4
+ Revision: 656315
- rebuild with new pocketsphinx realese

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.1798-3
+ Revision: 640489
- rebuild to obsolete old packages

* Sun Feb 13 2011 zamir <zamir@mandriva.org> 0.1798-2
+ Revision: 637562
- change provides

* Sun Feb 13 2011 zamir <zamir@mandriva.org> 0.1798-1
+ Revision: 637553
- patch makefile
- fix spec files
- fixed install requires
- fixed Build Requires
- fixed Build Requires
- first build
- create unimrcp

