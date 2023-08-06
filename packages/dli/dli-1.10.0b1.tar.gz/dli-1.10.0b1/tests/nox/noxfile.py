import nox
import os


def test_existing_requirements(session):
    session.install('-r', '../../requirements.txt')
    session.install('-r', '../../requirements-test.txt')
    os.chdir('../../')
    session.run('pytest')


def test_requirements_sc0(session):
    """
        Smoke test - single unittest, no integration tests.
        Integration tests are run in test_requirements_offset_scenarios.
    """
    TEST_FILES = ['../models/test_dataset.py', ]
    session.install('-r', '../../requirements.txt')
    session.install('-r', '../../requirements-test.txt')
    os.chdir('../../')
    session.run('pytest', '-m', "'not integration'", *TEST_FILES)


def test_requirements_offset_scenarios(session):
    """
        Run all unit tests and integration tests
        using modified requirements.txt, where for each
        package>=version_number, version_number is found given its
        proximity to MIN_DATE environment variable.
    """
    scenario = os.environ.get('NOX_SCENARIO')
    min_date = os.environ.get('MIN_DATE')
    if scenario == '1':
        min_date = None
    from_file = '../../requirements.txt'
    to_file = f'requirements-{scenario}.txt'


    rm = RequirementsModifier(from_file)
    rm.modify_requirements(from_file, to_file, min_date)
    session.install('-r', f'requirements-{scenario}.txt')
    session.install('-r', '../../requirements-test.txt')
    os.chdir('../../')
    session.run('pytest')


PYTHON_VERSIONS_LIST = ['3.6', '3.7']
PIP_VERSIONS_LIST = ['9.0.0', '20.1.1']


@nox.session(python=PYTHON_VERSIONS_LIST)
@nox.parametrize('pip_version', PIP_VERSIONS_LIST)
def test(session, pip_version):
    if pip_version=='9.0.0' and session=='3.8':
        return

    session.run('pip', 'install', '-U', 'pip=={}'.format(pip_version))

    scenarios_dict = {
        '0': test_requirements_sc0,
        '1': test_requirements_offset_scenarios,
        '2': test_requirements_offset_scenarios,
        '3': test_requirements_offset_scenarios,
        '4': test_requirements_offset_scenarios,
        '5': test_requirements_offset_scenarios,
        '6': test_requirements_offset_scenarios,
    }
    scenario = os.environ.get('NOX_SCENARIO')
    print('NOX_SCENARIO=', scenario)
    if scenario in scenarios_dict:
        scenarios_dict[scenario](session)
    else:
        test_existing_requirements(session)


class RequirementsModifier:

    def __init__(self, from_file):
        self.requirements = from_file
        self.alt_requirements = None
        # Following set for each individual package.
        self.date_to_version = None
        self.version_to_date = None
        self.dates_lst = None
        self.version_lst = None
        self.min_date = None
        self.version_limits = None

    def set_known_issues(self):
        # set specific package version cutoffs
        self.version_limits = {
            'pyarrow': '0.11.1',
            'python-dateutil': '2.7.0',
            'pandas': '0.25.3',
            'keyring': '17.1.1',
        }

    def set_requirement_details(self, pckg, vrsn):
        import requests
        dc = requests.get(f'https://pypi.org/pypi/{pckg}/{vrsn}/json').json()
        releases = dc['releases']
        date_to_version, dates_lst = self.get_requirement_date_to_version(
            releases)
        version_to_date, version_lst = self.get_requirement_version_to_date(
            releases)
        self.date_to_version = date_to_version
        self.version_to_date = version_to_date
        self.dates_lst = dates_lst
        self.version_lst = version_lst

    def get_requirements_list(self, file):
        with open(file) as f:
            ls = f.readlines()
            ln = []
            for l in ls:
                sl = l.split(' ')
                if len(sl) == 1:
                    sl = l.split('\n')
                ln.append(sl[0])
        return ln

    def get_requirement_date_to_version(self, releases):
        dates_lst = []
        dates_dct = {}
        for k, v in releases.items():
            try:
                dates_dct[v[0]['upload_time']] = k
                dates_lst.append(v[0]['upload_time'])
            except Exception:
                try:
                    dates_dct[k] = v['upload_time']
                    dates_lst.append(v[0]['upload_time'])
                except Exception:
                    pass
                    # print(f'No release information for {k}, date to version')
        dates_lst.sort(reverse=True)
        return dates_dct, dates_lst

    def get_requirement_version_to_date(self, releases):
        versions_lst = []
        versions_dict = {}
        for k, v in releases.items():
            try:
                versions_dict[k] = v[0]['upload_time']
                versions_lst.append(k)
            except Exception:
                try:
                    versions_dict[v['upload_time']] = k
                    versions_lst.append(k)
                except Exception:
                    pass
                    # print(f'No release information for {k}, version to date')
        versions_lst.sort(reverse=True)
        return versions_dict, versions_lst

    def write_requirements(self, reqs, file):
        with open(file, 'w') as f:
            f.writelines(reqs)

    def print_requirements_diff(self):
        rlen = len(self.alt_requirements)
        r = 0
        while r < rlen:
            print(f'{self.requirements[r]} -> {self.alt_requirements[r]}')
            r += 1

    def get_closest_earlier_date(self, min_date):
        for date in self.dates_lst:
            if date < min_date:
                upd_vrsn = self.date_to_version[date]
                return upd_vrsn, date

        last_date = self.dates_lst[-1:][0]
        return self.date_to_version[last_date], last_date

    def get_earlier_version_by_date(self, min_date):
        return self.get_closest_earlier_date(min_date)

    def get_earlier_version_with_offset(self, vrsn, offset):
        # 1. get date for existing version
        try:
            date = self.version_to_date[vrsn]
        except Exception:
            for v in self.version_lst:
                if v.startswith(vrsn):
                    # print(f'Using {v} instead of {vrsn} for package: {pckg}')
                    vrsn = v
                    date = self.version_to_date[vrsn]

        year = int(date[:4]) - int(offset[:4])
        month = int(date[5:7]) - int(offset[5:7])
        if month < 10:
            month = f'0{month}'
        day = int(date[8:10]) - int(offset[8:10])
        if day < 10:
            day = f'0{day}'

        udate = f'{year}-{month}-{day}'

        self.min_date = os.environ.get('MIN_DATE')
        if self.min_date is not None and udate < self.min_date:
            udate = self.min_date

        return self.get_closest_earlier_date(udate)

    def modify_requirements(self, from_file, to_file, min_date):

        self.set_known_issues()

        reqs = self.get_requirements_list(from_file)
        self.requirements = reqs
        alt_reqs = []

        for req in reqs:
            if req[0] == '#':
                continue
            if '>=' in req:
                pckg, vrsn = req.split('>=')
            elif '==' in req:
                pckg, vrsn = req.split('==')
            else:  # '~=' in req:
                pckg, vrsn = req.split('~=')

            # HACK for the case of keyring>=17.1.1,<=19.2.0 where we do not
            # yet have the logic to nicely do ranges, so dump everything after
            # the comma.
            vrsn = vrsn.split(",")[0]

            self.set_requirement_details(pckg, vrsn)

            if min_date is None:
                # this will run the existing requirements with >=
                try:
                    # some versions with ~= might be missing a subversion number
                    alt_date = self.version_to_date[vrsn]
                    alt_vrsn = vrsn
                except:
                    for v in self.version_lst:
                        if vrsn in v:  # 1.2 in 1.2.9
                            alt_date = self.version_to_date[v]
                            alt_vrsn = v
                            break
            else:
                alt_vrsn, alt_date = self.get_earlier_version_by_date(min_date)

            from packaging import version  # installed to base image
            # check if req has a know issue / limit in version number
            if (
                    pckg in self.version_limits and
                    version.parse(alt_vrsn) <
                    version.parse(self.version_limits[pckg])
            ):
                alt_vrsn = self.version_limits[pckg]
                alt_date = self.version_to_date[alt_vrsn]

            alt_reqs.append(f'{pckg}=={alt_vrsn}    # {alt_date[:10]}\n')

        self.alt_requirements = alt_reqs
        self.write_requirements(alt_reqs, to_file)
        self.print_requirements_diff()
