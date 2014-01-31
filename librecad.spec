Name:           librecad
Version:        2.0.2
Release:        1%{?dist}
Summary:        A generic 2D CAD program

License:        GPLv2
URL:            http://www.librecad.org
%if (0%{?rhel} > 0)
Source0:        http://github.com/LibreCAD/LibreCAD/archive/%{version}
%else
Source0:        http://github.com/LibreCAD/LibreCAD/archive/%{version}.tar.gz
%endif
Source1:        %{name}-rpmlintrc
Patch2:         %{name}-external-libs.patch

BuildRequires:  boost-devel
BuildRequires:  libdxfrw-devel >= 0.5.11
BuildRequires:  qt-devel
BuildRequires:  fdupes
BuildRequires:  muParser-devel
BuildRequires:  desktop-file-utils


%description
LibreCAD is a Qt4 application to design 2D cad drawing based
on the community edition of QCad.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package parts
Summary:        Parts collection for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description parts
Collection of parts for %{name}, a Qt4 application to design 2D cad drawing
based on the community edition of QCad.

%prep
%setup -q -n LibreCAD-%{version}
sed -i -e 's|MimeType=image/vnd.dxf|MimeType=image/vnd.dxf;|' desktop/librecad.desktop
%patch2 -p1
sed -i -e 's|tr("Compiled on: %1").arg(__DATE__) + "<br>" +|tr("Compiled on: 2013-Aug-28") + "<br>" +|' librecad/src/main/qc_applicationwindow.cpp

sed -i '/QMAKE_POST_LINK = cd $$_PRO_FILE_PWD_\/..\/.. && scripts\/postprocess-unix.sh/d' librecad/src/src.pro
sed -i -e 's|RESOURCEDIR="\${THISDIR}\/unix\/resources"|RESOURCEDIR=\$BUILDDIR|' scripts/postprocess-unix.sh

#sed -i -e 's|# Generate translations|# Generate translations\nLRELEASE="lrelease-qt4"|' scripts/postprocess-unix.sh

sed -i -e 's|QStringList ret;|if (subDirectory=="plugins") {\n\t\tdirList.append("%{_libdir}/" + appDirName + "/" + subDirectory);\n\t}\n\n\tQStringList ret;|' librecad/src/lib/engine/rs_system.cpp


%build
export CXXFLAGS="$RPM_OPT_FLAGS"
qmake-qt4 -makefile librecad.pro "CONFIG+=release"
make %{?_smp_mflags}


%install
export BUILDDIR="%{buildroot}%{_datadir}/%{name}"
sh scripts/postprocess-unix.sh

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins
mv unix/resources/plugins/* %{buildroot}%{_libdir}/%{name}/plugins/
# mv gpl-2.0.txt LICENSE
chmod 644 LICENSE
mv README.md README
chmod 644 README
find %{buildroot}%{_datadir}/%{name} -type f -exec chmod 644 {} \;

%{__install} -Dm 755 -s unix/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -Dm 755 -s unix/ttf2lff %{buildroot}%{_bindir}/ttf2lff
desktop-file-install desktop/%{name}.desktop
%{__install} -Dm 644 librecad/res/main/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__install} -Dm 644 desktop/%{name}.sharedmimeinfo $RPM_BUILD_ROOT%{_datadir}/mime/packages/%{name}.xml
%{__install} -Dm 644 desktop/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -Dm 644 tools/ttf2lff/ttf2lff.1 %{buildroot}%{_mandir}/man1/ttf2lff.1
%{__install} -Dm 644 librecad/src/plugins/document_interface.h %{buildroot}%{_includedir}/%{name}/document_interface.h
%{__install} -Dm 644 librecad/src/plugins/qc_plugininterface.h %{buildroot}%{_includedir}/%{name}/qc_plugininterface.h

#find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :


%files
%doc LICENSE README
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/ttf2lff.1*
%{_bindir}/%{name}
%{_bindir}/ttf2lff
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/library
%{_libdir}/%{name}


%files devel
%doc
%{_includedir}/%{name}

%files parts
%{_datadir}/%{name}/library


%changelog
* Thu Jan 23 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 2.0.2-1
- Initial releasefor Fedora
- Convert 32/64 bit patch to sed string
