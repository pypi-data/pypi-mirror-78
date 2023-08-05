from python_freeipa.exceptions import DuplicateEntry, NotFound
import logging


def safe_run(func):
    _log = logging.getLogger('ipa-connector')

    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NotFound, DuplicateEntry) as e:
            _log.error(e)
            _log.warning("Minor error occured, continue...")
            return None

    return func_wrapper


class LoggingClass(object):
    _log = logging.getLogger('ipa-connector')


class TranslatedObject:
    def _translate(self, input_data: dict):
        """
        Get rid of nasty newValue keys from input json file.
        Also workaround to set None values on non-provided, mandatory fields
        """
        trans = dict()
        for key in input_data.keys():
            try:
                trans[key] = input_data[key]['newValue']
            except KeyError:
                trans[key] = input_data[key]
        return trans


class User(TranslatedObject, LoggingClass):
    def __init__(self, input_data: dict):
        self._user_info = self._translate(input_data)
        self.login = self._get_login()
        self.first_name = self._get_firstname()
        self.name = self._get_name()
        self.full_name = self._get_full_name()
        self.email = self._get_mail()
        self.homedir = f"/data01/{self.login}/"
        self.gecos = self._get_gecos()
        self.org = self._get_org()
        self.keytab = self._get_keytab()

    def _get_keytab(self):
        kt = self._user_info.get('keytab', None)
        if kt == 'true':
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.login}|{self.full_name}|{self.email}"

    def _get_login(self):
        try:
            return self._user_info['login']
        except KeyError:
            return self._user_info['primaryKey']['login']

    def _get_gecos(self):
        return f"FR/C//BYTEL/{self.full_name}"

    def _get_mail(self):
        return self._user_info.get('email')

    def _get_org(self):
        company = self._user_info.get('company')
        if not company:
            company = "Bouygues Telecom"
        return company

    def _get_full_name(self):
        return " ".join([str(i) for i in [self.first_name, self.name] if i is not None])

    def _get_firstname(self):
        return self._user_info.get('firstname', '')

    def _get_name(self):
        return self._user_info.get('name', '')

    @safe_run
    def add(self, client):
        """
        Performs actual operation towards IPA server.
        client: ipa client instance
        """
        self._log.info(f"Adding user {self.login}")
        self._log.debug(f"User info: {self.login} \n "
                        f"Full name {self.full_name} \n"
                        f"First name {self.first_name} \n"
                        f"Last name {self.name} \n"
                        f"Homedir {self.homedir} \n"
                        f"Email {self.email} \n"
                        f"GECOS {self.gecos} \n"
                        f"ORG {self.org} \n")
        client.user_add(self.login,
                        self.first_name,
                        self.name,
                        self.full_name,
                        o_homedirectory=self.homedir,
                        o_mail=self.email,
                        o_gecos=self.gecos,
                        o_ou=self.org)

        return self

    @safe_run
    def delete(self, client):
        """
        Deletes user from IPA
        """
        self._log.info(f"Deleting user {self.login}")
        client.user_del(self.login)

    @safe_run
    def add_to_group(self, client, group_name):
        self._log.info(f"Adding {self.login} to group {group_name}")
        client.group_add_member(a_cn=group_name, o_user=self.login)

    @safe_run
    def delete_from_group(self, client, group_name):
        self._log.info(f"Deleting {self.login} from group {group_name}")
        client.group_remove_member(a_cn=group_name, o_user=self.login)


class AppUser(User):
    def get_groups(self):
        groups = []
        to_delete = []
        grp_nms = ['appUserGroupsRwxHome', 'userGroupsImpersonify', 'appUserGroupsRHome',
                   'userGroupsRHome', 'gdhRolesRxHome', 'gdhRolesImpersonify']
        for grp_nm in grp_nms:
            # groups.extend(Group(self._user_info.get(grp_nm, {"add": []})["add"]))
            grp_info = self._user_info.get(grp_nm)
            if not grp_info:
                continue

            groups.extend(grp_info.get('add', []))
            to_delete.extend(grp_info.get('remove', []))
        groups_dict = {'add': groups, 'remove': to_delete}
        return groups_dict

    def get_groups_to_remove(self):
        return self.get_groups()['remove']

    def get_groups_to_add(self):
        return self.get_groups()['add']

    def _get_login(self):
        try:
            return self._user_info['login']
        except KeyError:
            return self._user_info['primaryKey']['login']

    def _get_firstname(self):
        return "Application"

    def _get_full_name(self):
        return f"{self.first_name} {self.login}"

    def _get_mail(self):
        return ""

    def _get_name(self):
        return self._get_login()

    def _get_gecos(self):
        return f"FR/C//BYTEL/{self._user_info.get('description', f'App {self.login}')}"


class Group(TranslatedObject, LoggingClass):
    def __init__(self, input_data: dict):
        group_info = self._translate_group(input_data)
        try:
            self.name = group_info['name']
        except KeyError:
            self.name = input_data['primaryKey']['name']
        self.members = group_info['members']
        self.description = group_info.get('description')

    def _translate_group(self, input_data):
        translated = self._translate(input_data)
        try:
            translated['members'] = input_data['members']
        except KeyError:
            translated['members'] = {"add": []}
        return translated

    @safe_run
    def add(self, client):
        """
        Adds group to IPA
        """
        self._log.info(f"Adding Group: {self.name}")
        self._log.debug(
            f"Adding Group: {self.name} \n Description: {self.description} \n Members: {self.members['add']}")
        client.group_add(self.name, o_description=self.description)
        for member in self.members['add']:
            self._change_membership('add', member, client)

    @safe_run
    def delete(self, client):
        """
        Deletes Group from IPA
        """
        client.group_del(self.name)

    def update_members(self, client):
        for member in self.members['add']:
            self.add_member(client, member)
        for member in self.members['remove']:
            self._change_membership('remove', member, client)

    def add_member(self, client, member):
        self._log.info(f"Adding {member} to group {self.name}")
        self._change_membership('add', member, client)

    @safe_run
    def _change_membership(self, action, member, client):
        if action == 'add':
            func = client.group_add_member
        elif action == 'remove':
            func = client.group_remove_member
        self._log.info(f"{action} {member} to/from group {self.name}")
        func(a_cn=self.name, o_user=member)
