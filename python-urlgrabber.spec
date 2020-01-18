%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: A high-level cross-protocol url-grabber
Name: python-urlgrabber
Version: 3.10
Release: 7%{?dist}
Source0: http://urlgrabber.baseurl.org/download/urlgrabber-%{version}.tar.gz
Patch1: BZ-853432-single-conn-reset.patch
Patch2: BZ-1017491-respond-to-ctrl-c.patch

# rhel-7.1.0
Patch10: BZ-1099101-revert-curl-ctrl-c.patch
Patch11: BZ-1082648-curl-77-error-message.patch

# rhel-7.2
Patch20: BZ-1233329-timedhosts-parsing-error-handling.patch

License: LGPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel, python-pycurl
Url: http://urlgrabber.baseurl.org/
Provides: urlgrabber = %{version}-%{release}
Requires: python-pycurl

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}
%patch1 -p1
%patch2 -p1

# rhel-7.1.0
%patch10 -p1
%patch11 -p1

# rhel-7.2
%patch20 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{python_sitelib}/urlgrabber*
%{_bindir}/urlgrabber
%attr(0755,root,root) %{_libexecdir}/urlgrabber-ext-down

%changelog
* Tue Jun 30 2015 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10-7
- Don't crash on timedhosts parsing error.
- Resolves: bug#1233329

* Wed Sep 24 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10-6
- Add a comprehensive error message to curl error 77.
- Resolves: bug#1082648

* Wed Sep 10 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10-5
- Revert treating curl errcodes 55 and 56 as Ctrl-C.
- Resolves: bug#1099101

* Tue Feb 4 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10-4
- Treat curl errcodes 55 and 56 as Ctrl-C.
- Resolves: bug#1017491

* Thu Jan 16 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10-3
- Tell curl to return immediately on ctrl-c.
- Resolves: bug#1017491

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.10-2
- Mass rebuild 2013-12-27

* Mon Oct 21 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.10-1
- single-conn mode: Kill the cached idle connection. BZ 853432

* Thu Oct 17 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.10-0
- clamp timestamps from the future.  BZ 894630, 1013733
- Fix the condition to enter single-connection mode. BZ 853432
- Fix unit tests

* Tue Oct  8 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-33
- Fix the condition to enter single-connection mode (again)

* Thu Oct  3 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-32
- Update to latest HEAD.
- Fix traceback when entering single-connection mode with DEBUG off
- Fix traceback when limit==None and DEBUG is on
- Fix the condition to enter single-connection mode

* Thu Oct  3 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-31
- Update to latest HEAD.
- Switch to max_connections=1 after refused connect. BZ 853432
- Never display negative downloading speed. BZ 1001767
- clamp timestamps from the future.  BZ 894630, 1013733

* Thu Aug 29 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-30
- Update to latest HEAD.
- add ftp_disable_epsv option. BZ 849177
- Spelling fixes.
- docs: throttling is per-connection, suggest max_connections=1. BZ 998263
- More robust "Content-Length" parsing. BZ 1000841

* Tue Jun 18 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-29
- Update to latest HEAD.
- Fix parsing of FTP 213 responses
- Switch to max_connections=1 after timing out.  BZ 853432
- max_connections=0 should imply the default limit.

* Fri May 17 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-28
- Update to latest HEAD.
- Add the "minrate" option. BZ 964298
- Workaround progress "!!!" end for file:// repos.
- add URLGrabError.code to the external downloader API
- Disable GSSNEGOTIATE to work around a curl bug.  BZ 960163

* Wed Mar 27 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-26
- Update to latest HEAD.
- Handle HTTP 200 response to range requests correctly.  BZ 919076
- Reset curl_obj to clear CURLOPT_RANGE from previous requests.  BZ 923951

* Thu Mar  7 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-25
- Update to latest HEAD.
- fix some test cases that were failing.  BZ 918658
- exit(1) or /bin/urlgrabber failures.  BZ 918613
- clamp timestamps from the future.  BZ 894630
- enable GSSNEGOTIATE if implemented correctly.
- make error messages more verbose.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-23
- Update to latest HEAD.
- Handle checkfunc unicode exceptions. BZ 672117

* Thu Dec  6 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-22
- Update to latest HEAD.
- Improve URLGRABBER_DEBUG, add max_connections.  BZ 853432

* Thu Nov  1 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-21
- Update to latest HEAD.
- Get rid of "HTTP 200 OK" errors.  BZ 871835.

* Tue Sep  4 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-20
- Update to latest HEAD.
- Fixed BZ 851178, 854075.

* Mon Aug 27 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-19
- timedhosts: defer 1st update until a 1MB+ download.  BZ 851178

* Wed Aug 22 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-18
- Update to latest HEAD, lots of enhancements.

* Wed Aug 10 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-17
- Fix a bug in progress display code. BZ 847105.

* Wed Aug  8 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-16
- Update to latest head.
- Improved multi-file progress, small bugfixes.

* Fri Jul 20 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-15
- Update to latest head, misc bugfixes: BZ 832028, 831904, 831291.
- Disable Kerberos auth.  BZ 769254
- copy_local bugfix. BZ 837018
- send 'tries' counter to mirror failure callback

* Mon May 21 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-14
- timedhosts: sanity check on dl_time

* Fri May 18 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-13
- fix file:// profiling.  BZ 822632.

* Mon May 14 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-12
- Update to latest HEAD
- Merge multi-downloader patches

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep  3 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-9
- new update to latest head with a number of patches collected from 
  older bug reports.

* Mon Aug 30 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-8
- update to latest head patches

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 James Antill <james@fedoraproject.org> 3.9.1-6
- Update to upstream HEAD.
- LOWSPEEDLIMIT and hdrs

* Fri Feb 19 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-5
- add patch to allow reset_curl_obj() to close and reload the cached curl obj

* Thu Nov 12 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-4
- reset header values when we redirect and make sure debug output will work

* Wed Nov 11 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-3
- fixing a bunch of redirect and max size bugs

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-2
- stupid patch

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-1
- 3.9.1

* Tue Aug 18 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-8
- ssl options, http POST string type fixes

* Mon Aug 10 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-6
- reget fixes, tmpfiles no longer made for urlopen() calls.

* Wed Aug  5 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-5
- apply complete patch to head fixes: timeouts, regets, improves exception raising

* Tue Aug  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-4
- timeout patch for https://bugzilla.redhat.com/show_bug.cgi?id=515497


* Thu Jul 30 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-1
- new version - curl-based

* Wed Apr  8 2009 James Antill <james@fedoraproject.org> 3.0.0-15
- Fix progress bars for serial consoles.
- Make C-c behaviour a little nicer.

* Fri Mar 13 2009 Seth Vidal <skvidal at fedoraproject.org>
- kill deprecation warning from importing md5 if anyone uses keepalive

* Mon Mar  9 2009 Seth Vidal <skvidal at fedoraproject.org>
- apply patch for urlgrabber to properly check file:// urls with the checkfunc

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 3.0.0-11
- Rebuild for Python 2.6

* Wed Oct 14 2008 James Antill <james@fedoraproject.org> 3.0.0-10
- Have the progress bar have a small bar, for a virtual size doubling.

* Thu Jul 10 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Make urlgrabber usable if openssl is broken
- Relates: bug#454179

* Sun Jun 15 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Don't count partial downloads toward the total

* Sat May 18 2008 James Antill <james@fedoraproject.org> 3.0.0-8
- Tweak progress output so it's hopefully less confusing
- Add dynamic resizing ability to progress bar
- Resolves: bug#437197

* Fri May  2 2008 James Antill <james@fedoraproject.org> 3.0.0-7
- Fix reget's against servers that don't allow Range requests, also tweaks
- reget == check_timestamp, if anyone/thing uses that.
- Resolves: bug#435156
- Fix minor typo in progress for single instance.

* Mon Apr  7 2008 James Antill <james@fedoraproject.org> 3.0.0-6
- Fix the ftp byterange port problem:
- Resolves: bug#419241
- Fixup the progress UI:
-   add function for total progress
-   add total progress percentagee current download line
-   add rate to current download line
-   use dead space when finished downloading
-   don't confuse download rate on regets.

* Sat Mar 15 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-5
- Make sure, that *.egg-info is catched up during build

* Mon Dec  3 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-4
- Ensure fds are closed on exceptions (markmc, #404211)

* Wed Oct 10 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-3
- fix type checking of strings to also include unicode strings; fixes 
  regets from yum (#235618)

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-2
- fixes for package review (#226347)

* Thu May 31 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-1
- update to 3.0.0

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-5
- rebuild for python 2.5

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-4
- fix keepalive (#218268) 

* Sat Nov 11 2006 Florian La Roche <laroche@redhat.com>
- add version/release to "Provides: urlgrabber"

* Mon Jul 17 2006 James Bowes <jbowes@redhat.com> - 2.9.9-2
- Add support for byte ranges and keepalive over HTTPS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9.9-1.1
- rebuild

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-1
- update to 2.9.9

* Tue Mar 14 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-2
- catch read errors so they trigger the failure callback.  helps catch bad cds

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-1
- update to new version fixing progress bars in yum on regets

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-4
- don't use --record and list files by hand so that we don't miss 
  directories (#158480)

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-3
- add directory to file list (#168261)

* Fri Jun 03 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.6-2
- Fixed the reget method to actually work correctly (skip completely transfered
  files, etc)

* Tue Mar  8 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-1
- update to 2.9.6

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 2.9.5-1
- import into dist
- make the description less of a book

* Mon Mar  7 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.5-0
- 2.9.5

* Thu Feb 24 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.3-0
- first package for fc3
- named python-urlgrabber for naming guideline compliance

