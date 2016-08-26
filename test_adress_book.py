import os
import pickle
import unittest

from phonebook import AddressBook, AddressBookPickleStorage, \
    AddressBookPerson, AddressBookGroup, \
    AddressBookInvalidDataException, AddressBookValueError


class SelfDestructiveStorageTest():
    test_filename = 'test_file.pkl'
    test_data = {'persons': 'test'}

    def tearDown(self):
        if os.path.isfile(self.test_filename):
            os.remove(self.test_filename)

class PickleStorageTest(SelfDestructiveStorageTest, unittest.TestCase):

    def test_storage_empty(self):
        storage = AddressBookPickleStorage(None)
        self.assertEqual(storage.data, AddressBookPickleStorage.data)

    def test_storage_custom_file(self):
        # create/rewrite file with custom data
        with open(self.test_filename, 'w') as storage_file:
            pickle.dump(self.test_data, storage_file)

        storage = AddressBookPickleStorage(self.test_filename)
        self.assertEqual(storage.data, self.test_data)

        # delete file with custom data
        os.remove(self.test_filename)

    def test_storage_save(self):
        # save data in storage
        storage = AddressBookPickleStorage(self.test_filename)
        storage.data = self.test_data
        storage.save()

        # load data one more time
        storage2 = AddressBookPickleStorage(self.test_filename)
        self.assertEqual(storage2.data, self.test_data)


class AdressBookTest(SelfDestructiveStorageTest, unittest.TestCase):

    def test_adressbook_save(self):
        # create adress book and save it
        self.address_book.persons = self.test_data['persons']
        self.address_book.save_in_storage()

        # load same adress book from storage
        storage2 = AddressBookPickleStorage(self.test_filename)
        address_book2 = AddressBook(storage2)
        self.assertEqual(address_book2.persons,
                         self.test_data['persons'])

    def test_add_remove_person(self):
        person_1 = AddressBookPerson(first_name="Freddie",
                                     last_name="Mercury")

        person_2 = AddressBookPerson(first_name="Bryan",
                                     last_name="May")

        person_3 = AddressBookPerson(first_name="Mike",
                                     last_name="Gross")
        self.address_book.add_person(person_1)
        self.address_book.add_person(person_2)
        self.address_book.add_person(person_3)

        self.address_book.remove_person(person_2)

        self.assertEqual(len(self.address_book.persons), 2)
        self.assertIn(person_1, self.address_book.persons.values())
        self.assertIn(person_3, self.address_book.persons.values())

    def test_person_removal_fails(self):
        person = AddressBookPerson(first_name='Paul',
                                   last_name="Rodgers")
        with self.assertRaises(AddressBookValueError):
            self.address_book.remove_person(person)

    def test_add_remove_group(self):
        group_1 = AddressBookGroup('friends')
        group_2 = AddressBookGroup('enemies')
        group_3 = AddressBookGroup('pizzas')

        self.address_book.add_group(group_1)
        self.address_book.add_group(group_2)
        self.address_book.add_group(group_3)

        self.address_book.remove_group(group_2)

        self.assertEqual(len(self.address_book.groups), 2)
        self.assertIn(group_1, self.address_book.groups.values())
        self.assertIn(group_3, self.address_book.groups.values())

    def test_group_removal_fails(self):
        group = AddressBookGroup('dealers')
        with self.assertRaises(AddressBookValueError):
            self.address_book.remove_group(group)

    def test_relations(self):
        group = AddressBookGroup('Beatles')

        person_1 = AddressBookPerson(first_name="John",
                                   last_name="Lennon")
        person_2 = AddressBookPerson(first_name="Paul",
                                   last_name="McCartney")
        person_3 = AddressBookPerson(first_name="George",
                                   last_name="Harrison")
        person_4 = AddressBookPerson(first_name="Pete",
                                     last_name="Best")
        person_5 = AddressBookPerson(first_name="Ringo",
                                   last_name="Starr")

        self.address_book.add_group(group)
        self.address_book.add_person(person_1)
        self.address_book.add_person(person_2)
        self.address_book.add_person(person_3)
        self.address_book.add_person(person_4)
        self.address_book.add_person(person_5)

        self.address_book.add_person_to_group(person_1, group)
        self.address_book.add_person_to_group(person_2, group)
        self.address_book.add_person_to_group(person_3, group)
        self.address_book.add_person_to_group(person_4, group)

        self.address_book.remove_person_from_group(person_4, group)

        self.address_book.add_person_to_group(person_5, group)

        members = self.address_book.get_group_members(group)

        self.assertEqual(len(members), 4)
        self.assertIn(person_5, members)
        self.assertNotIn(person_4, members)


    def test_find_persons_groups(self):
        group_1 = AddressBookGroup("Nirvana")
        group_2 = AddressBookGroup("Foo Fighters")
        group_3 = AddressBookGroup("Rolling Stones")

        person = AddressBookPerson(first_name="David",
                                   last_name="Grohl")

        self.address_book.add_person(person)

        self.address_book.add_group(group_1)
        self.address_book.add_group(group_2)
        self.address_book.add_group(group_3)

        self.address_book.add_person_to_group(person, group_1)
        self.address_book.add_person_to_group(person, group_2)

        groups = self.address_book.get_person_groups(person)

        self.assertIn(group_1, groups)
        self.assertIn(group_2, groups)
        self.assertNotIn(group_3, groups)

    def find_person_by_email_part(self):
        person_1 = AddressBookPerson(first_name="Thome",
                                     last_name="Yorke",
                                     email_addresses=[
                                         "thome@radiohead.com",
                                         "thome@atomsforpease.com"
                                     ])
        person_2 = AddressBookPerson(first_name="Johny",
                                     last_name="Greenwood",
                                     email_addresses=[
                                         "johny@radiohead.com"
                                     ])
        person_3 = AddressBookPerson(first_name="Tom",
                                     last_name="Jones",
                                     email_addresses=[
                                         "thom@jones.com"
                                     ])

        self.address_book.add_person(person_1)
        self.address_book.add_person(person_2)
        self.address_book.add_person(person_3)

        persons = self.address_book.get_persons_by_email('thom')

        self.assertIn(person_1, persons)
        self.assertIn(person_3, persons)
        self.assertNotIn(person_2, persons)



    def find_person_by_name(self):
        person_1 = AddressBookPerson(first_name="Mike",
                                     last_name="Tyson")
        person_2 = AddressBookPerson(first_name="Mike",
                                     last_name="Shinoda")
        person_3 = AddressBookPerson(first_name="Tyson",
                                     last_name="Fury")
        person_4 = AddressBookPerson(first_name="Mike",
                                     last_name="Oldfield")

        self.address_book.add_person(person_1)
        self.address_book.add_person(person_2)
        self.address_book.add_person(person_3)

        by_first_name = self.address_book.get_persons_by_name(
            first_name="Mike")
        by_last_name = self.address_book.get_persons_by_name(
            last_name="Tyson")
        by_both = self.address_book.get_persons_by_name(
            first_name="Mike", last_name="Shinoda")

        self.assertIn(person_1, by_first_name)
        self.assertIn(person_3, by_first_name)
        self.assertIn(person_4, by_first_name)
        self.assertNotIn(person_2, by_first_name)

        self.assertIn(person_1, by_last_name)
        self.assertNotIn(person_2, by_last_name)

        self.assertIn(person_2, by_both)

    def setUp(self):
        storage = AddressBookPickleStorage(self.test_filename)
        self.address_book = AddressBook(storage)


class PersonTest(unittest.TestCase):

    def setUp(self):
        self.person = AddressBookPerson(first_name='Mark',
                                        last_name='Rutte')

    def test_street_address(self):
        address_list = [
            'Greek street, 3, Lisbon',
            'Palm street, 4, Porto'
        ]
        self.person.add_street_adress(address_list[0])
        self.person.add_street_adress(address_list[1])
        self.assertEqual(self.person.street_addresses, address_list)

        self.person.remove_street_adress(address_list[0])
        self.assertEqual(self.person.street_addresses, address_list[1:])

    def test_street_address_removal_fails(self):
        with self.assertRaises(AddressBookValueError):
            self.person.remove_street_adress("Bermuda Triangle, 777")

    def test_email_address(self):
        email_list = [
            'erik@gmail.com',
            'sergey@gmail.com'
        ]
        self.person.add_email_adress(email_list[0])
        self.person.add_email_adress(email_list[1])
        self.assertEqual(self.person.email_addresses, email_list)

        self.person.remove_email_adress(email_list[1])
        self.assertEqual(self.person.email_addresses, email_list[:-1])

    def test_email_address_removal_fails(self):
        with self.assertRaises(AddressBookInvalidDataException):
            self.person.add_email_adress("exam!!!ple@example.com")

    def test_email_address_validation_fails(self):
        with self.assertRaises(AddressBookValueError):
            self.person.remove_email_adress("example@example.com")

    def test_phone_number(self):
        phone_list = [
            '911',
            '112'
        ]
        self.person.add_phone_number(phone_list[0])
        self.person.add_phone_number(phone_list[1])
        self.assertEqual(self.person.phone_numbers, phone_list)

        self.person.remove_phone_number(phone_list[0])
        self.assertEqual(self.person.phone_numbers, phone_list[1:])

    def test_phone_removal_fails(self):
        with self.assertRaises(AddressBookValueError):
            self.person.remove_phone_number("012345678")

    def test_phone_validation_fails(self):
        with self.assertRaises(AddressBookInvalidDataException):
            self.person.add_phone_number("001!!!")



if __name__ == "__main__":
    unittest.main()