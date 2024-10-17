Summary: GNOME keyring manager
Name: gnome-keyring-manager
Version: 2.20.0
Release: %mkrel 3
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch:  gnome-keyring-manager-2.20.0-format-strings.patch
License: GPLv2+
Group: Graphical desktop/GNOME
Url: https://gnomesupport.org/wiki/index.php/GNOME%20Keyring%20Manager%20Wiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: intltool
BuildRequires: libgnomeui2-devel
BuildRequires: libglade2.0-devel
BuildRequires: gnome-keyring-devel >= 0.3.2
BuildRequires: gnome-doc-utils
BuildRequires: docbook-dtd42-xml
BuildRequires: libxslt-proc
BuildRequires: scrollkeeper
BuildRequires: desktop-file-utils

%description
This a keyring management program for the GNOME Desktop. The development of
this application will be like a tutorial for people on gnome-love and the main
idea is that these people in gnome-love do the code themself, helped by the
hacker-trainers.

%prep
%setup -q
%patch -p1

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std _ENABLE_SK=no
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*-{??,??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_scrollkeeper
%post_install_gconf_schemas %name
%update_menus
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%clean_menus
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc HACKING NEWS README TODO AUTHORS ChangeLog
%_bindir/%name
%_datadir/applications/%name.desktop
%_datadir/%name
%_mandir/man1/*
%_datadir/omf/%name/%name-C.omf
%_sysconfdir/gconf/schemas/%name.schemas


