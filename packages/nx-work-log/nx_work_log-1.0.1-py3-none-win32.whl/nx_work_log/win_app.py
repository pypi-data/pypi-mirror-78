import json
import os
from nx_work_log.change_time_dialog import ChangeTimeDialog
from nx_work_log.sys_tray_icon import SysTrayIcon
from nx_work_log.minute_timer import MinuteTimer

paused = True
icons = {'running': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'SysTrayRunning.ico'),
         'paused': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'SysTrayPaused.ico')}
minute_timer = None
my_sys_tray_icon = None
config_file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'configuration.json')
configuration = {}


def show_change_time_dialog(sys_tray_icon):
    """
    This function is called when the SysTrayIcon change time menu item is selected
    :param sys_tray_icon: The SysTrayIcon object
    """
    ChangeTimeDialog().show_window()


def reset_time(sys_tray_icon):
    """
    This function is called when the SysTrayIcon change reset time menu item is selected
    :param sys_tray_icon: The SysTrayIcon object
    """
    ChangeTimeDialog().set_time(0)


def pause_clicked(sys_tray_icon):
    """
    This function is called when the SysTrayIcon change pause menu item is selected or the icon is clicked
    :param sys_tray_icon: The SysTrayIcon object
    """
    global paused
    paused = not paused
    sys_tray_icon.icon = icons['paused'] if paused else icons['running']
    sys_tray_icon.refresh_icon()


def is_paused():
    """
    This function returns if the timer is paused
    :return: Paused
    """
    return paused


def minute_timer_callback():
    """
    This is the callback function for the minute timer. It gets called every minute.
    """
    if not paused:
        dialog_time = ChangeTimeDialog().get_time()
        dialog_time += 1
        ChangeTimeDialog().set_time(dialog_time)


def change_time_dialog_time_changed_callback(minutes):
    """
    This is the callback function for the change time dialog, which keeps the time and whenever it changes due to the
    timer or user input then this function is called.
    """
    global configuration

    if my_sys_tray_icon is not None:
        my_sys_tray_icon.set_hover_text('{:02d}:{:02d}'.format(int(minutes / 60), minutes % 60))

    configuration['logged_minutes'] = minutes
    with open(config_file_name, 'w') as json_file:
        json.dump(configuration, json_file)


def on_startup(sys_tray_icon):
    """
    This function is called when the SysTrayIcon starts up
    :param sys_tray_icon: The SysTrayIcon object
    """
    global my_sys_tray_icon
    my_sys_tray_icon = sys_tray_icon


def on_exit(sys_tray_icon):
    """
    The exit function is called when the SystrayIcon exits
    :param sys_tray_icon: The SysTrayIcon object
    """
    minute_timer.cancel()


def exit():
    """
    This function ends the SysTray thread
    """
    SysTrayIcon().exit()


def main():
    """
    Main function creating the ChangeTimeDialog and SysTrayIcon with its menu
    """
    global minute_timer, configuration

    menu_options = [
        ('Change Time', None, show_change_time_dialog),
        ('Reset Time', None, reset_time),
        ('Pause', is_paused, pause_clicked),
    ]

    ChangeTimeDialog().set_time_changed_callback(change_time_dialog_time_changed_callback)

    # Load the logged time from the json file if it exists
    if os.path.exists(config_file_name):
        with open(config_file_name) as json_file:
            configuration = json.load(json_file)

        ChangeTimeDialog().set_time(configuration['logged_minutes'])
    else:
        configuration['logged_minutes'] = 0

    # Create a minute timer for logging the worked minutes
    minute_timer = MinuteTimer(minute_timer_callback)

    # Create the system tray icon and menus. This function is blocking.
    SysTrayIcon(icons['paused'], '{:02d}:{:02d}'.format(int(configuration['logged_minutes'] / 60), configuration['logged_minutes'] % 60),
                menu_options, call_on_startup=on_startup, on_exit=on_exit, default_menu_index=2)


if __name__ == '__main__':
    main()
