#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Functions useful in mobile related, GLib based projects
Summary(pl.UTF-8):	Funkcje przydatne w opartych na GLib projektach dla urządzeń przenośnych
Name:		gmobile
Version:	0.1.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://sources.phosh.mobi/releases/gmobile/%{name}-%{version}.tar.xz
# Source0-md5:	22749819a84cc34c24c2e520b767e071
URL:		https://gitlab.gnome.org/World/Phosh/gmobile
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	json-glib-devel >= 1.6.2
BuildRequires:	meson >= 0.56.1
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.66
Requires:	json-glib >= 1.6.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gmobile carries some helpers for GNOME on mobile devices. Some of
those parts might move to glib or libgnome-desktop eventually. There
aren't any API stability guarantees at this point in time.

%description -l pl.UTF-8
gmobile gromadzi funkcje pomocnicze dla środowiska GNOME na
urządzeniach przenośnych. Niektóre elementy mogą być w przyszłości
przeniesione do bibliotek glib lub libgnome-desktop. Obecnie nie ma
żadnych gwarancji co do stabilności API.

%package devel
Summary:	Header files for gmobile library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gmobile
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.66
Requires:	json-glib-devel >= 1.6.2

%description devel
Header files for gmobile library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gmobile.

%package static
Summary:	Static gmobile library
Summary(pl.UTF-8):	Statyczna biblioteka gmobile
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gmobile library.

%description static -l pl.UTF-8
Statyczna biblioteka gmobile.

%package apidocs
Summary:	API documentation for gmobile library
Summary(pl.UTF-8):	Dokumentacja API biblioteki gmobile
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for gmobile library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gmobile.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gmobile-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gm-display-panel-preview
%attr(755,root,root) %{_bindir}/gm-display-panel-run-phosh
%attr(755,root,root) %{_bindir}/gm-timeout
%attr(755,root,root) %{_libdir}/libgmobile.so.0
%{_libdir}/girepository-1.0/Gm-0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgmobile.so
%{_includedir}/gmobile
%{_datadir}/gir-1.0/Gm-0.gir
%{_pkgconfigdir}/gmobile.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgmobile.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/gmobile-0
%endif
