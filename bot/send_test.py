from services import build_daily_message
from repository import load_contacts, load_ports, load_materials, load_safety_talks

if __name__ == '__main__':
    contacts = load_contacts()
    ports = load_ports()
    materials = load_materials()
    talks = load_safety_talks()
    if not contacts:
        print('No hay contactos en data/contacts.csv')
    else:
        c = contacts[0]
        print(build_daily_message(c, ports, materials, talks))
