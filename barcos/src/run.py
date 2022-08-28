import nagoya
import sagunto


# Update Nagoya port information
nagoya.update_forward_movements()


# Get latests Sagunto ship info
session = sagunto.setup()
sagunto.get_next_ships(session)
