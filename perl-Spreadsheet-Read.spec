# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Spreadsheet
%define		pnam	Read
%include	/usr/lib/rpm/macros.perl
Summary:	Spreadsheet::Read - Read the data from a spreadsheet
Name:		perl-Spreadsheet-Read
Version:	0.47
Release:	2
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Spreadsheet/%{pdir}-%{pnam}-%{version}.tgz
# Source0-md5:	84fe60094d79a6e85c6ed414a77e89cb
URL:		http://search.cpan.org/~hmbrand/Spreadsheet-Read/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-NoWarnings
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Spreadsheet::Read tries to transparently read *any* spreadsheet and
return its content in a universal manner independent of the parsing
module that does the actual spreadsheet scanning.

For OpenOffice this module uses Spreadsheet::ReadSXC

For Microsoft Excel this module uses Spreadsheet::ParseExcel or
Spreadsheet::XLSX

For CSV this module uses Text::CSV_XS or Text::CSV_PP.

For SquirrelCalc there is a very simplistic built-in parser

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%{__sed} -i -e '/#!\/pro\/bin\/perl/d' Read.pm
%{__sed} -i -e 's|/pro/bin/perl|%{_bindir}/perl|' examples/*

%build
AUTOMATED_TESTING=1 \
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Spreadsheet/Read*.pm
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
