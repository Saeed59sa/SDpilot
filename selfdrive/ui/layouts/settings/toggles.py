from openpilot.system.ui.lib.list_view import multiple_button_item, toggle_item
from openpilot.system.ui.lib.scroller import Scroller
from openpilot.system.ui.lib.widget import Widget
from openpilot.common.params import Params

# Description constants
DESCRIPTIONS = {
  "OpenpilotEnabledToggle": (
    "Use the openpilot system for adaptive cruise control and lane keep driver assistance. " +
    "Your attention is required at all times to use this feature."
  ),
  "DisengageOnAccelerator": "When enabled, pressing the accelerator pedal will disengage openpilot.",
  "LongitudinalPersonality": (
    "Standard is recommended. In aggressive mode, openpilot will follow lead cars closer and be more aggressive with the gas and brake. " +
    "In relaxed mode openpilot will stay further away from lead cars. On supported cars, you can cycle through these personalities with " +
    "your steering wheel distance button."
  ),
  "IsLdwEnabled": (
    "Receive alerts to steer back into the lane when your vehicle drifts over a detected lane line " +
    "without a turn signal activated while driving over 31 mph (50 km/h)."
  ),
  "AlwaysOnDM": "Enable driver monitoring even when openpilot is not engaged.",
  'RecordFront': "Upload data from the driver facing camera and help improve the driver monitoring algorithm.",
  "IsMetric": "Display speed in km/h instead of mph.",
  "RecordAudio": "Record and store microphone audio while driving. The audio will be included in the dashcam video in comma connect.",
}


class TogglesLayout(Widget):
  def __init__(self):
    super().__init__()
    self._params = Params()
    self._aalc_toggle = toggle_item(
      "Allow Auto Lane Change",
      "Automatically start lane changes after a short delay when the turn signal is on.",
      self._params.get_bool("AALCEnabled"),
      icon="road.png",
    )
    self._aalc_mode = multiple_button_item(
      "Auto Lane Change Delay",
      "Delay before automatic lane changes begin.",
      buttons=["Nudgeless", "0.5s", "1s", "2s", "3s"],
      button_width=255,
      selected_index=max(0, int(self._params.get("AALCMode") or b"1") - 1),
      callback=self._set_aalc_mode,
      icon="road.png",
    )
    self._aalc_toggle_prev = self._aalc_toggle.action_item.toggle.get_state()
    self._aalc_mode_prev = self._aalc_mode.action_item.selected_button

    items = [
      toggle_item(
        "Enable openpilot",
        DESCRIPTIONS["OpenpilotEnabledToggle"],
        self._params.get_bool("OpenpilotEnabledToggle"),
        icon="chffr_wheel.png",
      ),
      toggle_item(
        "Experimental Mode",
        initial_state=self._params.get_bool("ExperimentalMode"),
        icon="experimental_white.png",
      ),
      toggle_item(
        "Disengage on Accelerator Pedal",
        DESCRIPTIONS["DisengageOnAccelerator"],
        self._params.get_bool("DisengageOnAccelerator"),
        icon="disengage_on_accelerator.png",
      ),
      multiple_button_item(
        "Driving Personality",
        DESCRIPTIONS["LongitudinalPersonality"],
        buttons=["Aggressive", "Standard", "Relaxed"],
        button_width=255,
        callback=self._set_longitudinal_personality,
        selected_index=int(self._params.get("LongitudinalPersonality") or 0),
        icon="speed_limit.png"
      ),
      toggle_item(
        "Enable Lane Departure Warnings",
        DESCRIPTIONS["IsLdwEnabled"],
        self._params.get_bool("IsLdwEnabled"),
        icon="warning.png",
      ),
      toggle_item(
        "Always-On Driver Monitoring",
        DESCRIPTIONS["AlwaysOnDM"],
        self._params.get_bool("AlwaysOnDM"),
        icon="monitoring.png",
      ),
      toggle_item(
        "Record and Upload Driver Camera",
        DESCRIPTIONS["RecordFront"],
        self._params.get_bool("RecordFront"),
        icon="monitoring.png",
      ),
      toggle_item(
        "Record Microphone Audio",
        DESCRIPTIONS["RecordAudio"],
        self._params.get_bool("RecordAudio"),
        icon="microphone.png",
      ),
      self._aalc_toggle,
      self._aalc_mode,
      toggle_item(
        "Use Metric System", DESCRIPTIONS["IsMetric"], self._params.get_bool("IsMetric"), icon="monitoring.png"
      ),
    ]

    self._scroller = Scroller(items, line_separator=True, spacing=0)

  def _render(self, rect):
    self._scroller.render(rect)

    enabled = self._aalc_toggle.action_item.toggle.get_state()
    if enabled != self._aalc_toggle_prev:
      self._aalc_toggle_prev = enabled
      self._params.put_bool("AALCEnabled", enabled)

    mode_index = self._aalc_mode.action_item.selected_button
    if mode_index != self._aalc_mode_prev:
      self._aalc_mode_prev = mode_index
      self._params.put("AALCMode", str(mode_index + 1))

  def _set_longitudinal_personality(self, button_index: int):
    self._params.put("LongitudinalPersonality", str(button_index))

  def _set_aalc_mode(self, button_index: int):
    self._params.put("AALCMode", str(button_index + 1))
