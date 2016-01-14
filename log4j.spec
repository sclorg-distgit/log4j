%global pkg_name log4j
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}


%global bootstrap %{?_with_bootstrap:1}%{!?_with_bootstrap:%{?_without_bootstrap:0}%{!?_without_bootstrap:%{?_bootstrap:%{_bootstrap}}%{!?_bootstrap:0}}}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.2.17
Release:        15.14%{?dist}
Epoch:          0
Summary:        Java logging package
BuildArch:      noarch
License:        ASL 2.0
URL:            http://logging.apache.org/%{pkg_name}
Source0:        http://www.apache.org/dist/logging/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
# Converted from src/java/org/apache/log4j/lf5/viewer/images/lf5_small_icon.gif
Source102:      %{pkg_name}-logfactor5.sh
Source104:      %{pkg_name}-logfactor5.1
# Converted from docs/images/logo.jpg
Source112:      %{pkg_name}-chainsaw.sh
Source114:      %{pkg_name}-chainsaw.1
Source200:      %{pkg_name}.catalog
Patch0:         0001-logfactor5-changed-userdir.patch
Patch1:         0006-Remove-mvn-clirr-plugin.patch
Patch2:         0009-Fix-tests.patch
Patch3:         0010-Fix-javadoc-link.patch
Patch4:         0011-Remove-openejb.patch
Patch5:         0012-Add-proper-bundle-symbolicname.patch

BuildRequires:  perl
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}javamail
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix_maven}geronimo-jms
BuildRequires:  %{?scl_prefix}jakarta-oro
BuildRequires:  %{?scl_prefix_maven}ant-contrib
BuildRequires:  %{?scl_prefix}ant-junit

%description
Log4j is a tool to help the programmer output log statements to a
variety of output targets.

%package        manual
Summary:        Developer manual for %{pkg_name}
Requires:       %{name}-javadoc = %{version}-%{release}

%description    manual
%{summary}.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-%{pkg_name}-%{version}
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# see patch files themselves for reasons for applying
%patch0 -p1 -b .logfactor-home
%patch1 -p1 -b .remove-mvn-clirr
%patch2 -p1 -b .fix-tests
%patch3 -p1 -b .xlink-javadoc
%patch4 -p1 -b .openejb
%patch5 -p1 -b .bundlename
%pom_remove_plugin :maven-site-plugin

sed -i "s|groupId>ant<|groupId>org.apache.ant<|g" pom.xml

sed -i 's/\r//g' LICENSE NOTICE site/css/*.css site/xref/*.css \
    site/xref-test/*.css

# fix encoding of mailbox files
for i in contribs/JimMoore/mail*;do
    iconv --from=ISO-8859-1 --to=UTF-8 "$i" > new
    mv new "$i"
done

# remove all the stuff we'll build ourselves
find -name "*.jar" -o -name "*.class" -delete
rm -rf docs/api

# Needed by tests
mkdir -p tests/lib/
(cd tests/lib/
  ln -s `build-classpath jakarta-oro`
  ln -s `build-classpath javamail/mail`
  ln -s `build-classpath junit`
)

%pom_xpath_inject "pom:dependency[pom:groupId='javax.mail']" '<scope>provided</scope>'
%pom_xpath_inject "pom:dependency[pom:groupId='org.apache.geronimo.specs']" '<scope>provided</scope>'

# tests need network
rm -rf tests/src/java/org/apache/log4j/net
sed -i '/s\.addTestSuite(org\.apache\.log4j\.net/d' tests/src/java/org/apache/log4j/CoreTestSuite.java
sed -i '/<test name="org\.apache\.log4j\.net/d' tests/build.xml

%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_file : %{pkg_name}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install

# scripts
install -pD -T -m 755 %{SOURCE102} %{buildroot}%{_bindir}/logfactor5
install -pD -T -m 755 %{SOURCE112} %{buildroot}%{_bindir}/chainsaw

# Manual pages
install -d -m 755 ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 644 %{SOURCE104} ${RPM_BUILD_ROOT}%{_mandir}/man1/logfactor5.1
install -p -m 644 %{SOURCE114} ${RPM_BUILD_ROOT}%{_mandir}/man1/chainsaw.1

# fix perl location
%__perl -p -i -e 's|/opt/perl5/bin/perl|%{__perl}|' \
contribs/KitchingSimon/udpserver.pl
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE NOTICE
%{_bindir}/*
%{_mandir}/*/*

%files manual
%doc LICENSE NOTICE
%doc site/*.html site/css site/images/ site/xref site/xref-test contribs

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.2.17-15.14
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 0:1.2.17-15.13
- Mass rebuild 2015-01-09

* Thu Jan 08 2015 Michal Srb <msrb@redhat.com> - 1.2.17-15.12
- Use .mfiles wherever possible

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.11
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.10
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.9
- Rebuild for rh-java-common collection

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.8
- Mass rebuild 2014-05-26

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 0:1.2.17-15.7
- Set javamail and geronimo scope to provided

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.6
- Mass rebuild 2014-02-19

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.5
- Skip installation of SGML catalogs

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-15.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.2.17-15
- Mass rebuild 2013-12-27

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-14
- Remove desktop files

* Thu Jul 11 2013 Michal Srb <msrb@redhat.com> - 0:1.2.17-13
- Enable tests
- Fix BR

* Tue May 14 2013 Ville Skyttä <ville.skytta@iki.fi> - 0:1.2.17-12
- Add DTD public id to XML and SGML catalogs.

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-11
- Remove unneeded BR: maven-idea-plugin

* Thu Apr 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-10
- Fix manpage names, thanks to Michal Srb for reporting

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-9
- Reindex sources in more sensible way
- Add manual pages; resolves: rhbz#949413

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.2.17-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-6
- Build aggregated javadocs with xmvn

* Fri Jan 18 2013 Michal Srb <msrb@redhat.com> - 0:1.2.17-5
- Build with xmvn

* Mon Sep 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-4
- Generate javadocs without maven skin

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.17-2
- Remove "uses" OSGI directives from MANIFEST (related #826776)

* Mon Jun 04 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.17-1
- Update to latest version
- Change OSGI bundle symbolic name to org.apache.log4j
- Resolves #826776

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.16-10
- Remove duplicate import-package declaration.
- Adapt to current guidelines.
- Remove no longer needed patches.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Ville Skyttä <ville.skytta@iki.fi> - 0:1.2.16-8
- Drop executable file mode bits from icons.

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-7
- Use package instead of install mvn target to fix build

* Thu Dec 16 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.16-6
- Do not require jaxp_parser_impl. Maven build is not using it all and it's provided by every Java5 JVM.

* Thu Dec  9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-5
- Add patch to fix ant groupId
- Versionless jars & javadocs

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-4
- Fix BRs to include ant-junit
- Fix changed path for javadocs after build run

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-3
- Add license to javadoc and manual subpackages

* Fri May 28 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-2
- Install pom file
- Trim changelog
- Add jpackage-utils to javadoc Requires

* Mon May 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-1
- Complete re-working of whole ebuild to work with maven
- Rebase to new version
- Drop gcj support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.14-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.14-5.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.14-4.3
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.14-4jpp.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.14-4jpp.1
- Autorebuild for GCC 4.3

* Sat May 26 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.2.14-3jpp.1
- Upgrade to 1.2.14
- Modify the categories for the .desktop files so they are only
  displayed under the development/programming menus
- Resolves: bug 241447

* Fri May 11 2007 Jason Corley <jason.corley@gmail.com> 0:1.2.14-3jpp
- rebuild through mock and centos 4
- replace vendor and distribution with macros

* Fri Apr 20 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.14-2jpp
- Patch to allow build of org.apache.log4j.jmx.* with mx4j
- Restore Vendor: and Distribution:

* Sat Feb 17 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.2.14-1jpp
- Upgrade

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.13-4jpp
- Add bootstrap option to build core

* Wed Aug 09 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-3jpp.2
- Remove patch for BZ #157585 because it doesnt seem to be needed anymore.

* Tue Aug 08 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-3jpp.1
- Re-sync with latest from JPP.
- Update patch for BZ #157585 to apply cleanly.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.2.13-2jpp_2fc
- Rebuilt

* Fri Jul 21 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-2jpp_1fc
- Merge spec and patches with latest from JPP.
- Clean source tar ball off prebuilt jars and classes.
- Use classpathx-jaf and jms for buildrequires for the time being.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.2.8-7jpp_9fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.2.8-7jpp_8fc
- fix scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.2.8-7jpp7fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov  3 2005 Archit Shah <ashah@redhat.com> 0:1.2.8-7jpp_6fc
- Reenable building of example that uses rmic

* Wed Jun 22 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_5fc
- Reenable building of classes that require jms.
- Remove classes and jarfiles from the tarball.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_4fc
- Work around chainsaw failure (#157585).

* Tue Jan 11 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_3fc
- Reenable building of classes that require javax.swing (#130006).

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_2fc
- Build into Fedora.
