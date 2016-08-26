#AddressBookPerson

first and last names are mandatory params:

```
person = AddressBookPerson(first_name="First Name",
                            last_name="Last Name")
```
list of street_addresses, email_adresses and phone_numbers is not mandatory:
```
person = AddressBookPerson(first_name="First Name",
                            last_name="Last Name",
                            street_addresses=[
                                "Street Address 1",
                                "Street Address 2"
                            ],
                            email_addresses=[
                                "email 1",
                                "email 2"
                            ],
                            phone_numbers=[
                                "phone number 1",
                                "phone number 2"
                            ])
```

email, phone numbers or street adresses can be added or removed from person's entry in Address Book:
```
add_street_adress()
add_email_adress()
add_phone_number()
remove_street_adress()
remove_email_adress()
remove_phone_number()
```
phone number and email will be validated before adding, or throw **AddressBookInvalidDataException** exception

validation rules is saved in properties **email_validation_rule** and **phone_validation_rule** and can be overrided with child classes

#AddressBookGroup
name is mandatory param for group:
```
group = AddressBookGroup('Group Name')
```

# AddressBook
Address book can use storage for persistence.
Storage class instance with save() method should be provided.
Pickle storage class provided as an example
```
storage = AddressBookPickleStorage('my_storage.pkl')
address_book = AddressBook(storage)
```
Address book can add or remove persons:
```
address_book.add_person(person)
address_book.remove_person(person)
```
Address book can add or remove groups:
```
address_book.add_group(group)
address_book.remove_group(group)
```
Address book can add or remove persons to groups:
```
address_book.add_person_to_group(person, group)
remove_person_from_group(person, group)
```

Person can be found by First name, Last name or both:
```
address_book.get_persons_by_name(first_name="First name",
last_name="Last name")
```
Person can be found by email or it's prefix:
```
address_book.get_persons_by_email('email')
```
Address book can find group's members:
```
get_group_members(group)
```
Address book can find the groups the person belongs to:
```
get_person_groups(person)
```
