"""
context help system for your kivy apps
======================================

This namespace portion is a requirement
of the :mod:`ae.kivy_app` module and is
tight coupled to it.

For to keep the module size small it got
extracted into its own namespace portion.

:mod:`ae.kivy_app` is automatically
importing/integrating this module for you.
For android apps built with buildozer you
only need to add it to the requirements
list in your `buildozer.spec` file.


help behaviour mixin
--------------------

The mixin class :class:`HelpBehaviour`
of this namespace portion is extending
and preparing any Kivy widget for to
show an individual help text for it.

.. note::
    For to automatically lock and mark the
    widget you want to add help texts for,
    this mixin class has to be specified as
    the first class in the list of classes
    your widget get inherited from.

The correct identification of each
help-aware widget presuppose that the
attribute :attr:`~HelpBehaviour.ae_help_id`
has a unique value for each widget
instance. This is done automatically for
the widgets provided by the
module :mod:`~ae.kivy_app` for to change
the app flow or app states (like e.g.
:class:`~ae.kivy_app.FlowButton`).

The :attr:`~HelpBehaviour.ae_help_vars`
is a dict which can be used to provide extra
context data for the generation and the
display of help texts.


help activation and de-activation
---------------------------------

Use the widget :class:`HelpToggler`
provided by this namespace portion
in your app for to toggle the
active state of the help mode.

.. hint::
    The :class:`HelpToggler` is using
    the low-level touch events to
    prevent the dispatch of the Kivy
    events `on_press`, `on_release`
    and `on_dismiss` for to allow
    to show help texts for opened
    dropdowns and popups.


layout widget for to display help text
--------------------------------------

The layout widget :class:`HelpLayout`
of this module is displaying the help
texts prepared by the method
:meth:`~ae.gui_help.HelpAppBase.help_display`
of the namespace portion :mod:`ae.gui_help`.


"""
from typing import cast, Tuple

from kivy.animation import Animation                                                        # type: ignore
from kivy.input import MotionEvent                                                          # type: ignore
from kivy.lang import Builder                                                               # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import BooleanProperty, DictProperty, ObjectProperty, StringProperty   # type: ignore
from kivy.uix.image import Image                                                            # type: ignore
from kivy.uix.scrollview import ScrollView                                                  # type: ignore
from kivy.uix.widget import Widget                                                          # type: ignore
from kivy.app import App                                                                    # type: ignore

from ae.core import main_app_instance                                                       # type: ignore
from ae.gui_help import HelpAppBase                                                         # type: ignore


__version__ = '0.1.5'


Builder.load_string("""\
#: import anchor_points ae.gui_help.anchor_points
#: import layout_x ae.gui_help.layout_x
#: import layout_y ae.gui_help.layout_y
#: import layout_ps_hints ae.gui_help.layout_ps_hints


<HelpBehaviour>:
    ae_help_id: ''
    # 'help_layout is not None' is needed because None is not allowed for bool ae_help_lock attribute/property
    ae_help_lock: app.help_layout is not None and app.displayed_help_id != self.ae_help_id
    ae_help_vars: dict()
    canvas.after:
        Color:
            rgba: app.font_color[:3] + (0.24 if self.ae_help_lock else 0, )
        Ellipse:
            pos: self.x + dp(9), self.y + dp(9)
            size: self.width - dp(18), self.height - dp(18)
        Color:
            rgba: app.font_color[:3] + (0.51 if self.ae_help_lock else 0, )
        Line:
            width: sp(3)
            rounded_rectangle: self.x + dp(3), self.y + dp(3), self.width - dp(6), self.height - dp(6), sp(15)


<HelpLayout>:
    size_hint: None, None
    ps_hints: layout_ps_hints(*root.target.to_window(*root.target.pos), *root.target.size, Window.width, Window.height)
    width: min(help_label.width, Window.width)
    height: min(help_label.height, Window.height)
    x: layout_x(root.ps_hints['anchor_x'], root.ps_hints['anchor_dir'], root.width, Window.width)
    y: layout_y(root.ps_hints['anchor_y'], root.ps_hints['anchor_dir'], root.height, Window.height)
    ani_value: 0.99
    canvas.before:
        Color:
            rgba: Window.clearcolor[:3] + (root.ani_value, )
        RoundedRectangle:
            pos: root.pos
            size: root.size
    canvas.after:
        Color:
            rgba: app.font_color[:3] + (root.ani_value, )
        Line:
            width: dp(3)
            rounded_rectangle: root.x + dp(1), root.y + dp(1), root.width - dp(2), root.height - dp(2), dp(12)
        Triangle:
            points:
                anchor_points(app.main_app.font_size * 0.69, root.ps_hints['anchor_x'], root.ps_hints['anchor_y'], \
                root.ps_hints['anchor_dir'])
        Color:
            rgba: Window.clearcolor[:3] + (root.ani_value, )
        Line:
            width: dp(1)
            rounded_rectangle: root.x + dp(1), root.y + dp(1), root.width - dp(2), root.height - dp(2), dp(12)
    Label:
        id: help_label
        text: root.help_text
        color: app.font_color[:3] + (root.ani_value, )
        background_color: Window.clearcolor[:3] + (root.ani_value, )
        font_size: app.main_app.font_size * 0.81
        markup: True
        padding: dp(12), dp(9)
        size_hint: None, None
        size: self.texture_size


<HelpToggler>:
    ae_icon_name: 'help_icon' if app.help_layout else 'app_icon'
    ani_value: 0.99
    size_hint_x: None
    width: self.height
    source: app.main_app.img_file(self.ae_icon_name, app.ae_states['font_size'], app.ae_states['light_theme'])
    canvas.after:
        Color:
            rgba: min(self.ani_value * 1.5, 1), min(self.ani_value * 1.5, 1), 1 - self.ani_value, 1 - self.ani_value / 2
        Ellipse:
            pos: self.pos
            size: self.size


""")


class HelpBehaviour(Widget):
    """ behaviour mixin class for widgets having help texts. """
    ae_help_id = StringProperty()       #: unique help id of the widget
    ae_help_lock = BooleanProperty()    #: True if the help mode is active and this widget is not the help target
    ae_help_vars = DictProperty()       #: dict of exta data for to displayed/render the help text of this widget

    def on_touch_down(self, touch: MotionEvent) -> bool:                                    # pragma: no cover
        """ prevent any processing if touch is done on the help activator widget or in active help mode.

        :param touch:   motion/touch event data.
        :return:        True if event got processed/used.
        """
        main_app = cast(HelpAppBase, main_app_instance())      # app = App.get_running_app()

        if main_app.help_activator.collide_point(*touch.pos):
            return False        # allow help activator button to process this touch down event

        if self.ae_help_lock and self.collide_point(*touch.pos):  # main_app.help_layout is not None
            if main_app.help_display(self.ae_help_id, self.ae_help_vars):
                return True

        return super().on_touch_down(touch)


class HelpLayout(ScrollView):                                                           # pragma: no cover
    """ semi-transparent and click-through container for to display help texts. """
    target = ObjectProperty()           #: target widget to display help text for
    ps_hints = ObjectProperty()         #: pos- and size-hints for the layout window widget
    help_text = StringProperty()        #: help text string to display

    ani_slide_back = None               # used for slide back animation if target position to the help activator

    def _update_effect_bounds(self, *args):
        """ override to prevent ScrollView recursion error/crash.

        kivy bug workaround (fixed in kivy master via https://github.com/kivy/kivy/pull/6985 on 15-Jul-2020).
        solution from https://www.gitmemory.com/issue/kivy/kivy/5638/529400808
        Unfortunately not included in Kivy 2.0.0rc3 (from 15-Jun-2020)
        """

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ check for additional events added by this class.

        :param touch:   motion/touch event data.
        :return:        True if event got processed/used.
        """
        return False        # let user click through this transparent help text widget

    def begin_ani_slide_back(self, end_pos: Tuple[float, float]):
        """ create and start animation for the help target widget (just displayed new help text for).

        :param end_pos:         position (x, y) to move help target widget to (mostly the help_activator position).
        """
        tar = self.target
        beg_pos = tuple(tar.pos)        # tuple() to de-ref pos property because it is changing too on animation
        print(f"begin_ani_slide_back(win_end_pos={end_pos})")
        end_pos = tar.to_widget(*end_pos)
        print(f"begin_ani_slide_back(tar_end_pos={end_pos})")
        delta = tar.height / 2
        ani = Animation(x=min(max(beg_pos[0] - delta, end_pos[0]), beg_pos[0] + delta),
                        y=min(max(beg_pos[1] - delta, end_pos[1]), beg_pos[1] + delta),
                        t='in_out_sine', d=69)
        ani += Animation(x=end_pos[0], y=end_pos[1], t='in_elastic', d=3)
        self.ani_slide_back = dict(tar=tar, ani=ani, beg_pos=beg_pos)

        ani.bind(on_complete=self.on_ani_slide_back_complete)
        ani.start(tar)

    def cancel_ani_slide_back(self):
        """ cancel animation of help target widget.
        """
        if not self.ani_slide_back:
            return

        tar = self.ani_slide_back['tar']
        ani = self.ani_slide_back['ani']
        ani.cancel(tar)
        ani.unbind(on_complete=self.on_ani_slide_back_complete)
        tar.pos = self.ani_slide_back['beg_pos']
        self.ani_slide_back = None

    def on_ani_slide_back_complete(self, _ani: Animation, _target: Widget):
        """ on-complete handler for help target pos animation.

        :param _ani:            :class:`~kivy.animation.Animation` instance.
        :param _target:         animated help target widget instance.
        """
        self.cancel_ani_slide_back()

        main_app = cast(HelpAppBase, main_app_instance())
        if main_app.help_layout:
            main_app.help_display('', dict())


class HelpToggler(Image):                                                               # pragma: no cover
    """ widget for to activate and deactivate the help mode.

    For to prevent the dismiss of opened popups and dropdowns at help mode activation, this singleton instance has to:

    * be registered in its __init__ to the :attr:`~ae.gui_help.HelpAppBase.help_activator` attribute and
    * have a :meth:`~HelpToggler.on_touch_down` method that is eating the activation touch event (returning True) and
    * a :meth:`~HelpToggler.on_touch_down` method not passing a activation touch in all DropDown/Popup widgets.

    """
    def __init__(self, **kwargs):
        """ initialize an instance of this class and also :attr:`~ae.gui_help.HelpAppBase.help_activator`. """
        App.get_running_app().main_app.help_activator = self
        super().__init__(**kwargs)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ touch down event handler for to toggle help mode while preventing dismiss of open dropdowns/popups.

        :param touch:           touch event.
        :return:                True if touch happened on this button (and will get no further processed => eaten).
        """
        if self.collide_point(*touch.pos):
            App.get_running_app().main_app.help_activation_toggle()
            return True
        return False
