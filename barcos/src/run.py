import sagunto

# Get latests Sagunto ship info
session = sagunto.setup()
sagunto.get_next_ships(session)
