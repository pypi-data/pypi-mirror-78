"""
user preferences widgets for your kivy app
==========================================

This namespace portion is providing a set of widgets
for to allow the user of your app to change the
her/his personal app settings/preferences, like
the theme, the font size, the language and the used
colors.

For to use it in your app you have to import this module.
This can be done either in one of the modules
of your app via::

    import ae.kivy_user_prefs

Alternatively you can also import it within your main KV
file, like this::

    #: import _any_dummy_name ae.kivy_user_prefs

The user preferences are implemented as a
:class:`~ae.kivy_app.FlowDropDown` via the widget
`UserPreferencesOpenPopup`.

For to integrate it in your app you simply
add the `UserPreferencesButton` widget to
the main KV file of your app.


user preferences debug mode
---------------------------

The user preferences are activating a debug mode
when you click/touch the `UserPreferencesButton`
button more than 3 times within 6 seconds.

This debug mode activation is implemented in the
event handler method
:meth:`~ae.kivy_app.KivyMainApp.on_user_preferences_open`
declared in the :mod:`ae.kivy_app` module. It can be
disabled for your app by simply overriding
this method with an empty method in your
main app class.
"""
from kivy.lang import Builder                                                       # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import ObjectProperty                                          # type: ignore

from ae.kivy_app import FlowDropDown                                                # type: ignore


__version__ = '0.1.3'


Builder.load_string("""\
#: import DEBUG_LEVELS ae.core.DEBUG_LEVELS

#: import DEF_LANGUAGE ae.i18n.DEF_LANGUAGE
#: import INSTALLED_LANGUAGES ae.i18n.INSTALLED_LANGUAGES

#: import MIN_FONT_SIZE ae.gui_app.MIN_FONT_SIZE
#: import MAX_FONT_SIZE ae.gui_app.MAX_FONT_SIZE
#: import THEME_LIGHT_BACKGROUND_COLOR ae.gui_app.THEME_LIGHT_BACKGROUND_COLOR
#: import THEME_LIGHT_FONT_COLOR ae.gui_app.THEME_LIGHT_FONT_COLOR
#: import THEME_DARK_BACKGROUND_COLOR ae.gui_app.THEME_DARK_BACKGROUND_COLOR
#: import THEME_DARK_FONT_COLOR ae.gui_app.THEME_DARK_FONT_COLOR


<UserPreferencesButton@FlowButton>:
    ae_flow_id: id_of_flow('open', 'user_preferences')
    circle_fill_color: app.mixed_back_ink


<UserPreferencesOpenPopup@FlowDropDown>:
    canvas.before:
        Color:
            rgba: app.mixed_back_ink
        RoundedRectangle:
            pos: self.pos
            size: self.size
    ChangeColorButton:
        color_name: 'flow_id_ink'
    ChangeColorButton:
        color_name: 'flow_path_ink'
    ChangeColorButton:
        color_name: 'selected_item_ink'
    ChangeColorButton:
        color_name: 'unselected_item_ink'
    FontSizeButton:
        # pass
    UserPrefSlider:
        ae_state_name: 'sound_volume'
        cursor_image: 'atlas://data/images/defaulttheme/audio-volume-high'
    # UserPrefSlider:    current kivy module vibrator.py does not support amplitudes arg of android api
    #    ae_state_name: 'vibrate_amplitude'
    #    cursor_image: app.main_app.img_file('vibrate', app.ae_states['font_size'], app.ae_states['light_theme'])
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if INSTALLED_LANGUAGES else 0
        opacity: 1 if INSTALLED_LANGUAGES else 0
        OptionalButton:
            lang_code: DEF_LANGUAGE
            ae_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
            ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
            square_fill_color:
                app.ae_states['selected_item_ink'] if app.main_app.lang_code in ('', self.lang_code) else \
                Window.clearcolor
            text: _(self.lang_code)
            visible: DEF_LANGUAGE not in INSTALLED_LANGUAGES
        LangCodeButton:
            lang_idx: 0
        LangCodeButton:
            lang_idx: 1
        LangCodeButton:
            lang_idx: 2
        LangCodeButton:
            lang_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5
        FlowButton:
            ae_flow_id: id_of_flow('change', 'light_theme')
            ae_clicked_kwargs: dict(light_theme=False)
            text: _("dark")
            color: THEME_DARK_FONT_COLOR or self.color
            square_fill_color: THEME_DARK_BACKGROUND_COLOR or self.square_fill_color
        FlowButton:
            ae_flow_id: id_of_flow('change', 'light_theme')
            ae_clicked_kwargs: dict(light_theme=True)
            text: _("light")
            color: THEME_LIGHT_FONT_COLOR or self.color
            square_fill_color: THEME_LIGHT_BACKGROUND_COLOR or self.square_fill_color
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        DebugLevelButton:
            level_idx: 0
        DebugLevelButton:
            level_idx: 1
        DebugLevelButton:
            level_idx: 2
        DebugLevelButton:
            level_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        KbdInputModeButton:
            text: 'below_target'
        KbdInputModeButton:
            text: 'pan'
        KbdInputModeButton:
            text: 'scale'
        KbdInputModeButton:
            text: 'resize'
        KbdInputModeButton:
            text: ''
    OptionalButton:
        square_fill_color: Window.clearcolor
        size_hint_x: 1
        text: 'kivy settings'
        visible: app.main_app.debug
        on_release: app.open_settings()


<FontSizeButton@FlowButton>:
    ae_flow_id: id_of_flow('edit', 'font_size')
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent_popup_to_close=self.parent.parent, parent=self))
    square_fill_color: Window.clearcolor


<FontSizeEditPopup>:
    on_select:
        app.main_app.change_flow(id_of_flow('change', 'font_size'), \
        font_size=args[1], popups_to_close=(self.parent_popup_to_close, ))
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 1 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 2 / 6
    FontSizeSelectButton:
        font_size: (MIN_FONT_SIZE + MAX_FONT_SIZE) / 2
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 4 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 5 / 6
    FontSizeSelectButton:
        font_size: MAX_FONT_SIZE


<FontSizeSelectButton@Button>:
    # text: f'Aa Bb Zz {round(self.font_size)}'  F-STRING displaying always 15 as font size
    text: 'Aa Bb Zz {}'.format(round(self.font_size))
    on_release: self.parent.parent.select(self.font_size)
    size_hint_y: None
    size: self.texture_size
    color: app.font_color
    background_normal: ''
    background_color:
        app.ae_states['selected_item_ink'] if app.main_app.font_size == self.font_size else Window.clearcolor


<ChangeColorButton@FlowButton>:
    color_name: 'flow_id_ink'
    ae_flow_id: id_of_flow('open', 'color_picker', self.color_name)
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent=self))
    square_fill_color: Window.clearcolor
    circle_fill_color: app.ae_states[self.color_name]
    text: _(self.color_name)


<ColorPickerOpenPopup@FlowDropDown>:
    ColorPicker:
        color: app.ae_states[root.attach_to.color_name] if root.attach_to else (0, 0, 0, 0)
        on_color: root.attach_to and app.main_app.change_app_state(root.attach_to.color_name, tuple(args[1]))
        size_hint_y: None
        height: self.width
        canvas.before:
            Color:
                rgba: Window.clearcolor
            RoundedRectangle:
                pos: self.pos
                size: self.size


<LangCodeButton@OptionalButton>:
    lang_idx: 0
    lang_code: INSTALLED_LANGUAGES[min(self.lang_idx, len(INSTALLED_LANGUAGES) - 1)]
    ae_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color:
        app.ae_states['selected_item_ink'] if app.main_app.lang_code == self.lang_code else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: _(self.lang_code)
    visible: len(INSTALLED_LANGUAGES) > self.lang_idx


<DebugLevelButton@OptionalButton>:
    level_idx: 0
    ae_flow_id: id_of_flow('change', 'debug_level', self.text)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color:
        app.ae_states['selected_item_ink'] if app.main_app.debug_level == self.level_idx else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: DEBUG_LEVELS[min(self.level_idx, len(DEBUG_LEVELS) - 1)]
    visible: app.main_app.debug and self.level_idx < len(DEBUG_LEVELS)


<KbdInputModeButton@OptionalButton>:
    ae_flow_id: id_of_flow('change', 'kbd_input_mode', self.text)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color:
        app.ae_states['selected_item_ink'] if app.main_app.kbd_input_mode == self.text else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    visible: app.main_app.debug


<UserPrefSlider@AppStateSlider>:

""")


class FontSizeEditPopup(FlowDropDown):
    """ drop down to select font size """
    parent_popup_to_close = ObjectProperty()    #: tuple of popup widget instances to be closed if this drop down closes
