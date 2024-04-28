from utils.general.load_env import app_settings
from utils.general.get_driver import get_driver


# Get the driver
driverInstance = get_driver()

# To make the window appear on the second monitor
# Change the values to match your setup
driverInstance.set_window_position(app_settings["window_x"], app_settings["window_y"])
driverInstance.maximize_window()


# Open the website
driverInstance.get("https://www.linkedin.com")