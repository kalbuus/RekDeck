from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.app import App
import interaction_managers.network_manager as network_manager

class NetworksRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(NetworksRecycleView, self).__init__(**kwargs)
        networks = []
        for network in network_manager.scan_wifi(App.get_running_app().is_debug_mode):
            if network["ssid"]:
                networks.append({"text": network["ssid"], "has_password": network["requires_password"]})
        self.data = networks

    def build(self):
        return self

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    pass
    
class SelectableNetworkLabel(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    has_password = BooleanProperty()
    index = 0

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableNetworkLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_up(self, touch):
        if super(SelectableNetworkLabel, self).on_touch_up(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            sm = App.get_running_app().root.ids.wifi_screen_manager
            sm.current = "wifi_password" if self.has_password else "wifi_select"
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected