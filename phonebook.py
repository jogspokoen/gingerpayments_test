import os
import re
import pickle


class AddressBookException(Exception):
    pass


class AddressBookValueError(ValueError):
    def __init__(self, data):
        message = 'Following data is not found: {0}'.format(data)
        super(AddressBookValueError, self).__init__(message)


class AddressBookInvalidDataException(AddressBookException):
    def __init__(self, data):
        message = 'Following data is not valid: {0}'.format(data)
        super(AddressBookInvalidDataException, self).__init__(message)


class AddressBookDuplicateException(AddressBookException):
    def __init__(self, data):
        message = 'Following key is duplicate: {0}'.format(data)
        super(AddressBookDuplicateException, self).__init__(message)


class AddressBook:
    storage = None

    def __init__(self, storage=None):
        self.persons = {}
        self.groups = {}
        self.relations = {}

        if storage:
            self.storage = storage
        else:
            self.storage = AddressBookPickleStorage()
        self.load_from_storage(self.storage)

    def load_from_storage(self, storage):
        if storage.data:
            self.persons = storage.data.get('persons', {})
            self.groups = storage.data.get('groups', {})
            self.relations = storage.data.get('relations', {})

    def save_in_storage(self):
        self.storage.data = {
            'persons': self.persons,
            'groups': self.groups,
            'relations': self.relations
        }
        self.storage.save()

    def add_person(self, person):
        if person.key in self.persons:
            raise AddressBookDuplicateException(person.key)
        else:
            self.persons[person.key] = person

    def remove_person(self, person):
        if person.key in self.persons:
            del (self.persons[person.key])
            for group_name in self.groups:
                if person.key in self.relations.get(group_name):
                    self.relations[group_name].remove(person.key)
        else:
            raise AddressBookValueError(person)

    def add_group(self, group):
        if group.name in self.groups:
            raise AddressBookDuplicateException(group.name)
        else:
            self.groups[group.name] = group
            self.relations[group.name] = []

    def remove_group(self, group):
        if group.name in self.groups:
            del (self.groups[group.name])
            del (self.relations[group.name])
        else:
            raise AddressBookValueError(group.name)

    def add_person_to_group(self, person, group):
        if group.name in self.groups:
            self.relations[group.name].append(person.key)
        else:
            raise AddressBookValueError(group.name)

    def remove_person_from_group(self, person, group):
        if group.name in self.relations:
            if person.key in self.relations.get(group.name):
                self.relations[group.name].remove(person.key)
            else:
                raise AddressBookValueError(person.key)
        else:
            raise AddressBookValueError(group.name)

    def get_group_members(self, group):
        group_keys = self.relations.get(group.name, [])
        return [self.persons.get(person_key) for person_key in
                group_keys]

    def get_person_groups(self, person):
        return [self.groups[group_key] for group_key in self.relations
                if person.key in self.relations[group_key]]

    def get_persons_by_email(self, keyword):
        return [person for person in self.persons.values() if
                person.has_email(keyword)]

    def get_persons_by_name(self, first_name=None, last_name=None):
        if first_name is None:
            return [person for person in self.persons.values()
                    if person.last_name == last_name]
        elif last_name is None:
            return [person for person in self.persons.values()
                    if person.first_name == first_name]
        else:
            return [person for person in self.persons.values()
                    if person.first_name == first_name
                    and person.last_name == last_name]


class AddressBookPickleStorage:
    storage_filename = 'storage.pkl'
    data = None

    def __init__(self, storage_filename=None):
        if storage_filename:
            self.storage_filename = storage_filename

        if os.path.isfile(self.storage_filename):
            with open(self.storage_filename, 'r') as storage_file:
                self.data = pickle.load(storage_file)

    def save(self):
        with open(self.storage_filename, 'w') as storage_file:
            pickle.dump(self.data, storage_file)


class AddressBookPerson:
    first_name = ''
    last_name = ''

    email_validation_rule = \
        r'^([a-z0-9_\.-]+)@([a-z0-9_\.-]+)\.([a-z\.]{2,6})$'
    phone_validation_rule = r'^[\d\s\(\)\+\-\.]+$'

    def __init__(self, first_name='',
                 last_name='',
                 street_addresses=None,
                 email_addresses=None,
                 phone_numbers=None):

        self.first_name = first_name
        self.last_name = last_name
        self.street_addresses = []
        self.email_addresses = []
        self.phone_numbers = []

        if street_addresses:
            self.street_addresses = street_addresses

        if email_addresses:
            for email in email_addresses:
                self.add_email_adress(email)

        if phone_numbers:
            for phone in phone_numbers:
                self.add_phone_number(phone)

    @property
    def key(self):
        '''
        I decided to use first+last name as a key in phonebook
        I know it's not the best solution,
        but duplicate first+last name (even as separate entries)
        makes address book confusive anyway
        '''
        return '{0}_{1}'.format(self.first_name, self.last_name)

    def validate_email(self, email_address):
        valid = re.search(self.email_validation_rule, email_address)
        if valid is None:
            raise AddressBookInvalidDataException(email_address)
        return True

    def validate_phone(self, phone_number):
        valid = re.search(self.phone_validation_rule, phone_number)
        if valid is None:
            raise AddressBookInvalidDataException(phone_number)
        return True

    def add_street_adress(self, street_address):
        self.street_addresses.append(street_address)

    def add_email_adress(self, email_address):
        if self.validate_email(email_address):
            self.email_addresses.append(email_address)

    def add_phone_number(self, phone_number):
        if self.validate_phone(phone_number):
            self.phone_numbers.append(phone_number)

    def remove_street_adress(self, street_address):
        if street_address in self.street_addresses:
            self.street_addresses.remove(street_address)
        else:
            raise AddressBookValueError(street_address)

    def remove_email_adress(self, email_address):
        if email_address in self.email_addresses:
            self.email_addresses.remove(email_address)
        else:
            raise AddressBookValueError(email_address)

    def remove_phone_number(self, phone_number):
        if phone_number in self.phone_numbers:
            self.phone_numbers.remove(phone_number)
        else:
            raise AddressBookValueError(phone_number)

    def has_email(self, keyword):
        return any([email for email in self.email_addresses if
                    email.find(keyword) == 0])


class AddressBookGroup:
    name = None

    def __init__(self, name):
        self.name = name
