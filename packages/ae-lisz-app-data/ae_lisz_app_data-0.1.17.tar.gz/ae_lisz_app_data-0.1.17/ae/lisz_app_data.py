"""
GUI framework demo implementations
==================================

This module is used as showcase base for the implementation of demo
applications of the GUI framework packages provided
by the ae namespace.

The plan is to integrate the following GUI frameworks on
top of the :class:`abstract base class <~ae.gui_app.MainAppBase>`
(implemented in the :mod:`ae.gui_app` portion of the
ae namespace):

* :mod:`Kivy <ae.kivy_app>` based on the `kivy framework <https://kivy.org>`__:
  `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`__
* :mod:`Enaml <ae.enaml_app>` based on `the enaml framework <https://enaml.readthedocs.io/en/latest/>`__:
  `enaml lisz demo app <https://gitlab.com/ae-group/enaml_lisz>`__
* :mod:`Beeware Toga <ae.toga_app>` based on `the beeware framework <https://beeware.org>`__:
  `beeware toga lisz demo app <https://gitlab.com/ae-group/toga_lisz>`__
* :mod:`Dabo <ae.dabo_app>` based on `the dabo framework <https://dabodev.com/>`__:
  `dabo lisz demo app <https://gitlab.com/ae-group/dabo_lisz>`__
* :mod:`pyglet <ae.pyglet_app>`
* :mod:`pygobject <ae.pygobject_app>`
* :mod:`AppJar <ae.appjar_app>`

The main app base mixin class :class:`LiszDataMixin` provided by this module
is used for to manage the common data structures, functions and methods
for the various demo applications variants based on :mod:`ae.gui_app`
and the related GUI framework implementation portions
(like e.g. :mod:`ae.kivy_app` and :mod:`ae.enaml_app`) of the ae namespace.

Further down in this module you find additional notes on each
of the already implemented GUI frameworks.


Lisz Demo App
=============

The Lisz demo app is managing a recursive item tree that can be used
e.g. as to-do or shopping list.


features of the Lisz demo app
-----------------------------

* recursive item data tree manipulation: add, edit and delete item
* each item can be selected/check marked
* easy filtering of selected/checked and unselected/unchecked items
* each item can be converted to a sub-node (sub-list) and back to a leaf item
* item order changeable via drag & drop
* item movable into parent and sub node
* easy navigation within the item tree (up/down navigation in tree and quick jump)
* simple demo help screen
* colors changeable by user
* font and button sizes are changeable by user
* dark and light theme switchable by user
* sound output support with sound volume configurable by user
* vibration output support with amplitude configurable by user (only for mobile apps)


lisz application data model
---------------------------

To keep it simply, the data managed by the Lisz application is
a minimalistic tree structure that gets stored as
an :ref:`application status`. The root node and with that
the whole recursive data structure
gets stored in the app state variable `root_node`,
without the need of any database.

The root of the tree structure is a list of the type `LiszNode`
containing list items of type `LiszItem`. A `LiszItem` element
represents a dict of the type `Dict[str, Any]`.

Each `LiszItem` element of the tree structure is either a
leaf or a node. And each node is a sub-list with a recursive
structure identical to the root node and of the type `LiszNode`.

The following graph is showing an example data tree:

.. graphviz::

    digraph {
        node [shape=record, width=3]
        rec1 [label="{<rec1>Root Node | { <A>Item A | <C>Item C | <D>... } }"]
        "root_node app state variable" -> rec1 [arrowhead=crow style=tapered penwidth=3]
        rec1:A -> "Leaf Item A" [minlen=3]
        rec2 [label="{<rec2>Node Item C (sub-node) | { <CA>Item CA | <CB>Item CB | <CN>... } }"]
        rec1:C -> rec2
        rec2:CA -> "Leaf Item CA" [minlen=2]
        rec3 [label="{<rec3>Node Item CB (sub-sub-node) | { <CBA>Item CBA | <CDn>... } }"]
        rec2:CB -> rec3
        rec3:CBA -> "Leaf Item CBA"
    }

The above example tree structure is containing
the root node items `A` -which is a leaf - and `C` - which is
a sub-node.

The node `C` consists of the items `CA` and `CB` where `CA` is
a leaf and `CB` is a node.

Finally the first item of the node `CB` is another
sub-node with the leaf item `CBA`.


gui framework implementation variants
=====================================

kivy
----

The `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`__ is based
on the `kivy framework <https://kivy.org>`__,
a `pypi package <https://pypi.org/project/Kivy/>`__
documented `here <https://kivy.org/doc/stable/>`__.


kivy wish list
^^^^^^^^^^^^^^

* kv language looper pseudo widget (like enaml is providing) for to easily generate sets of similar widgets.


enaml
-----

The `enaml lisz demo app <https://gitlab.com/ae-group/enaml_lisz>`__ is
based on the `enaml framework <https://pypi.org/project/enaml/>`__,
a `pypi package <https://pypi.org/project/enaml/>`__
documented `here at ReadTheDocs <https://enaml.readthedocs.io/en/latest/>`__.


automatic update of widget attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies have to be executed/read_from, so e.g. the icon attribute will not be updated if
app.ae_state_light_theme gets changed::

    icon << main_app.cached_icon('font_size') or app.ae_state_light_theme

In contrary the icon will be updated by the following two statements::

    icon << main_app.cached_icon('font_size') if app.ae_state_light_theme else main_app.cached_icon('font_size')
    icon << app.ae_state_light_theme == None or main_app.cached_icon('font_size')

KeyEvent implementation based on this SO answer posted by the enamlx author frmdstryr/Jairus Martin:
https://stackoverflow.com/questions/20380940/how-to-get-key-events-when-using-enaml. Alternative
and more complete implementation can be found in the enamlx package (https://github.com/frmdstryr/enamlx).


enaml wish list
^^^^^^^^^^^^^^^

* type and syntax checking, code highlighting and debugging of enaml files within PyCharm.
* fix freezing of linux/Ubuntu system in debugging of opening/opened PopupViews in PyCharm
  (workaround: killing of java PyCharm process).
"""
from abc import abstractmethod, ABC
import os
import pathlib
from typing import Any, Dict, List, Optional, Sequence

from ae.inspector import try_eval                                               # type: ignore
from ae.core import DEBUG_LEVEL_VERBOSE                                         # type: ignore
from ae.gui_app import id_of_flow, flow_action, flow_key, replace_flow_action   # type: ignore


__version__ = '0.1.17'


NODE_FILE_PREFIX = 'node_'  #: file name prefix for node imports/exports
NODE_FILE_EXT = '.txt'      #: file extension for node imports/exports

FLOW_PATH_ROOT_ID = 'ROOT'  #: needed for flow path jumper and for drop onto leave item button
FLOW_PATH_TEXT_SEP = " / "  #: flow path separator for :meth:`~LiszDataMixin.flow_path_text` and drop enter


LiszItem = Dict[str, Any]           #: node item data (nid) type
LiszNode = List[LiszItem]           #: node/list type


def check_item_id(item_id: str) -> bool:
    """ check if passed item id is valid.

    :param item_id:     item id to check.
    :return:            True if all characters in the pass item id are valid, else False.
    """
    return isinstance(item_id, str) and bool(item_id) \
        and item_id != FLOW_PATH_ROOT_ID and FLOW_PATH_TEXT_SEP not in item_id


class LiszDataMixin(ABC):
    """ lisz data model - independent from used GUI framework. """
    root_node: LiszNode             #: root of lisz data structure
    current_node_items: LiszNode    #: node item data of the current node / sub list (stored as app state via root_node)
    filtered_indexes: List[int]     #: indexes of the filtered/displayed items in the current node
    # additional app-common attributes (never directly referenced/needed, KEEP for completeness/documentation).
    filter_selected: bool           #: True for to hide/filter selected node items
    filter_unselected: bool         #: True for to hide/filter unselected node items

    # mixin shadow attributes - implemented by :class:`~ae.console_app.ConsoleApp` or :class:`~ae.gui_app.MainAppBase`
    debug_level: int                #: :attr:`~AppBase.debug_level`
    flow_id: str                    #: current attr:`flow id <ae.gui_app.MainAppBase.flow_id>`
    flow_path: List[str]            #: :attr:`flow path <ae.gui_app.MainAppBase.flow_path>` ref. current node

    _refreshing_data: bool = False                      #: DEBUG True while running :meth:`~.refresh_all` method

    # abstract methods
    # the gui_app methods are not really abstract (nor callable via super()) but declared here for to hide inspections
    @abstractmethod
    def call_method(self, method: str, *args, **kwargs) -> Any:
        """ call method of this instance (ae.gui_app.MainAppBase method). """

    @abstractmethod
    def change_app_state(self, state_name: str, state_value: Any, send_event: bool = True):
        """ add debug sound on each state change/save (ae.gui_app.MainAppBase method). """

    @abstractmethod
    def change_flow(self, new_flow_id: str, popups_to_close: Sequence = (), **event_kwargs) -> bool:
        """ change/switch flow id. """

    @abstractmethod
    def flow_path_action(self, path_index: int = -1) -> str:
        """ determine the action of the last/newest entry in the flow_path (ae.gui_app.MainAppBase method). """

    @abstractmethod
    def play_sound(self, sound_name: str):
        """ play audio/sound file (ae.gui_app.MainAppBase method). """

    # this a real abstract method (to be implemented by inheriting class)
    @abstractmethod
    def refresh_node_widgets(self):
        """ redraw/refresh the widgets representing the current node items/sub-nodes (GUI framework method). """

    # helper methods

    def change_sub_node_sel(self, node: LiszNode, set_sel_to: bool):
        """ change the selection of all the sub-leaves of the passed node to the specified value.

        :param node:            node of which to change the selection of the sub-item leaves.
        :param set_sel_to:      True will only toggle the unselected sub-item leaves, False only the selected ones.
        """
        for item in node:
            item.pop('sel', None)       # always first remove sel left-overs
            if 'node' in item:
                self.change_sub_node_sel(item['node'], set_sel_to)
            elif set_sel_to:
                item['sel'] = 1.0

    def delete_item(self, item_id: str, node_only: bool):
        """ delete either the complete item or the sub node of the item (identified by the passed item id).

        :param item_id:         item id to identify the item/sub-node to be deleted.
        :param node_only:       True if only delete the sub-node of the identified item, False for to delete the item.
        """
        nid = self.item_by_id(item_id)
        if node_only:
            nid.pop('node')
        else:
            assert nid in self.current_node_items, f"DEL item data: {nid} not in {self.current_node_items}"
            self.current_node_items.remove(nid)
            self.change_flow(id_of_flow('', ''))

        self.play_sound('deleted')

    def edit_validate(self, old_idx: int, new_id: Optional[str] = None, want_node: Optional[bool] = None) -> str:
        """ validate the user changes after adding a new item or editing an existing item.

        :param old_idx:             index in the current node of the edited item or -1 if a new item (to be added).
        :param new_id:              new/edited id string.
        :param want_node:           True if the new/edited item will have a sub-node, False if not.
        :return:                    empty string on successful validation, else error string or
                                    `'request_delete_confirmation_for_item'` if the user has to confirm the deletion
                                    after the user wiped the item id string or
                                    `'request_delete_confirmation_for_node'` if the user has to confirm the
                                    removal of the sub-node.
        """
        add_item = old_idx == -1
        if new_id is not None:
            if not new_id:
                # on empty id cancel edit if add_item, else request confirmation from user for item del
                return "" if add_item else 'request_delete_confirmation_for_item'
            if not check_item_id(new_id):
                return f"invalid item id {new_id} containing '{FLOW_PATH_TEXT_SEP}' or is equal '{FLOW_PATH_ROOT_ID}'"

            new_idx = self.find_item_index(new_id)
            if new_idx != -1 and (add_item or new_idx != old_idx):
                return f"item id '{new_id}' exists already"

        if add_item:                        # add new item
            nid = dict(id=new_id)
            if want_node:
                nid['node'] = list()        # type: ignore   # mypy not supports recursive types see issue #731
            self.current_node_items.insert(0, nid)

        else:                               # edit item
            nid = self.current_node_items[old_idx]
            if new_id:
                nid['id'] = new_id
            if want_node is not None and want_node != ('node' in nid):  # NOTE: != has lower priority than in operator
                if want_node:
                    nid['node'] = list()    # type: ignore   # mypy not supports recursive types see issue #731
                elif nid['node']:           # let user confirm node deletion of non-empty nid['node']
                    return 'request_delete_confirmation_for_node'
                else:
                    nid.pop('node')         # remove empty node

        self.play_sound('added' if add_item else 'edited')

        return ""

    def export_node(self, flow_path: List[str], file_path: str = ".") -> Optional[Exception]:
        """ export node specified by the passed :paramref:`~export_node.flow_path` argument.

        :param flow_path:   flow path of the node to export.
        :param file_path:   folder to store the node data into (def=current working directory).
        :return:            `None` if node got exported without errors, else the raised exception.
        """
        node = self.flow_path_node(flow_path)
        file_name = NODE_FILE_PREFIX + (flow_key(flow_path[-1]) if flow_path else FLOW_PATH_ROOT_ID) + NODE_FILE_EXT

        try:
            # the alternative `os.makedirs(exist_ok=True)` has problems on POSIX with '..'
            pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(file_path, file_name), 'w') as file_handle:
                file_handle.write(str(node))
        except (FileExistsError, FileNotFoundError, OSError, ValueError) as ex:
            return ex
        return None

    def find_item_index(self, item_id: str, searched_node: Optional[LiszNode] = None) -> int:
        """ determine list index of the passed item id in the searched node or in the current node.

        :param item_id:         item id to find.
        :param searched_node:   searched node. if not passed then the current node will be searched instead.
        :return:                item list index in the searched node or -1 if item id was not found.
        """
        if searched_node is None:
            searched_node = self.current_node_items
        for list_idx, nid in enumerate(searched_node):
            if nid['id'] == item_id:
                return list_idx
        return -1

    def flow_key_text(self, flow_id: str, landscape: bool) -> str:
        """ determine shortest possible text fragment of the passed flow key that is unique in the current node.

        Used to display unique part of the key of the focused item/node.

        :param flow_id:         flow id to get key to check from (pass the observed value to update GUI automatically,
                                either self.app_state_flow_id or self.app_states['flow_id']).
        :param landscape:       True if window has landscape shape (resulting in larger abbreviation). Pass the observed
                                attribute, mostly situated in the framework_win (e.g. self.framework_win.landscape).
        :return:                display text containing flow key.
        """
        if flow_action(flow_id) == 'focus':
            key = flow_key(flow_id)
            key_len = len(key)
            id_len = 6 if landscape else 3
            for nid in self.current_node_items:
                item_id = nid['id']
                if item_id != key:
                    while item_id.startswith(key[:id_len]) and id_len < key_len:
                        id_len += 1
            return f" ->{key[:id_len]}"
        return f".{flow_id}" if self.debug_level >= DEBUG_LEVEL_VERBOSE else ""

    def flow_path_from_text(self, text: str) -> List[str]:
        """ restore the full complete flow path from the shortened flow keys generated by :meth:`.flow_path_text`.

        :param text:            flow path text - like returned by :meth:`~LiszDataMixin.flow_path_text`.
        :return:                flow path list.
        """
        flow_path = list()
        if text != FLOW_PATH_ROOT_ID:
            node = self.root_node
            for part in text.split(FLOW_PATH_TEXT_SEP):
                for nid in node:
                    if nid['id'].startswith(part) and 'node' in nid:
                        flo_key = nid['id']
                        path_nid = nid
                        break
                else:
                    break       # actually not needed, will repair data tree errors
                flow_path.append(id_of_flow('enter', 'item', flo_key))
                node = path_nid['node']         # type: ignore   # mypy not supports recursive types see issue #731
        return flow_path

    def flow_path_node(self, flow_path: List[str] = None) -> LiszNode:
        """ determine the current node specified by the passed flow path.

        :param flow_path:       flow path list.
        :return:                current node list.
        """
        if flow_path is None:
            flow_path = self.flow_path
        current_node_items = self.root_node
        for flow_id in flow_path:
            if flow_action(flow_id) != 'enter':
                break
            node_id = flow_key(flow_id)
            item = self.item_by_id(node_id, searched_node=current_node_items)
            if 'node' not in item:
                break                           # actually not needed, will repair broken flow path
            current_node_items = item['node']
        return current_node_items

    def flow_path_quick_jump_nodes(self) -> List[str]:
        """ determine nodes relative to the current flow path to quick-jump to from current node.

        :return:                list of flow path texts.
        """
        def append_nodes(node):
            """ recursively collect all available nodes (possible flow paths) """
            for nid in node:
                if 'node' in nid:
                    deeper_flow_path.append(id_of_flow('enter', 'item', nid['id']))
                    paths.append(self.flow_path_text(deeper_flow_path))
                    append_nodes(nid['node'])
                    deeper_flow_path.pop()

        paths = [FLOW_PATH_ROOT_ID] if self.flow_path_action(0) == 'enter' else list()
        deep = 0
        while deep < len(self.flow_path) - 1 and self.flow_path_action(deep + 1) == 'enter':
            deep += 1
            paths.append(self.flow_path_text(self.flow_path[:deep]))

        deeper_flow_path = self.flow_path[:-1]      # start at current flow path minus the open_flow_path_jumper flow id
        append_nodes(self.current_node_items)

        return paths

    def flow_path_text(self, flow_path: List[str], min_len: int = 3) -> str:
        """ generate shortened display text from the passed flow path.

        :param flow_path:       flow path list.
        :param min_len:         minimum length of node ids (flow id keys).
        :return:                shortened display text from the passed flow path.
        """
        path_nid = None         # suppress Pycharm PyUnboundLocalVariable inspection warning
        shortened_ids = list()
        node = self.root_node
        for flow_id in flow_path:
            if flow_action(flow_id) != 'enter':
                break
            id_len = min_len
            node_id = flow_key(flow_id)
            sub_id_len = len(node_id)
            for nid in node:
                if nid['id'] == node_id:
                    path_nid = nid
                elif 'node' in nid:
                    while nid['id'].startswith(node_id[:id_len]) and id_len < sub_id_len:
                        id_len += 1

            shortened_ids.append(node_id[:id_len])
            if path_nid and 'node' in path_nid:     # prevent error in quick jump to root
                node = path_nid['node']             # type: ignore   # mypy not supports recursive types see issue #731

        return FLOW_PATH_TEXT_SEP.join(shortened_ids)

    def focus_neighbour_item(self, delta: int):
        """ move flow id to previous/next displayed/filtered node item.

        :param delta:           moving step (if greater 0 then forward, else backward).
        """
        filtered_indexes = self.filtered_indexes
        if filtered_indexes:
            flow_id = self.flow_id
            if flow_id:
                item_idx = self.find_item_index(flow_key(flow_id))
                assert item_idx >= 0
                filtered_idx = filtered_indexes.index(item_idx)
                idx = min(max(0, filtered_idx + delta), len(filtered_indexes) - 1)
            else:
                idx = min(max(-1, delta), 0)
            self.change_flow(id_of_flow('focus', 'item', self.current_node_items[filtered_indexes[idx]]['id']))

    def import_nodes(self, file_path: str = ".") -> List[str]:
        """ import all nodes found in the documents app folder of this app into the currently displayed node.

        :param file_path:   path to the folder wherein to store the node data (def=current working directory).
        :return:            empty list if found node(s) got imported without errors,
                            else the list of error strings prefixed with the node file path.
        """
        errors = list()
        try:
            for node_file in os.scandir(file_path):
                file_name = node_file.name
                if file_name.endswith(NODE_FILE_EXT) and node_file.is_file():
                    node_name = "imported node " + file_name[len(NODE_FILE_PREFIX):-len(NODE_FILE_EXT)]
                    err_msg = self.edit_validate(-1, node_name, want_node=True)
                    if err_msg:
                        errors.append(node_file.path + ":" + err_msg)
                        continue
                    with open(node_file.path) as file_handle:
                        file_content = file_handle.read()
                    # update the list instance that got already added by edit_validate() with the loaded node data
                    self.current_node_items[0]['node'][:] = try_eval(file_content)
        except (FileExistsError, FileNotFoundError, OSError, ValueError) as ex:
            errors.append(str(ex))
        return errors

    def item_by_id(self, item_id: str, searched_node: Optional[LiszNode] = None) -> LiszItem:
        """ search item in either the passed or the current node.

        :param item_id:         item id to find.
        :param searched_node:   searched node. if not passed then the current node will be searched instead.
        :return:                found item or empty dict with new/empty id if not found.
        """
        if searched_node is None:
            searched_node = self.current_node_items
        index = self.find_item_index(item_id, searched_node=searched_node)
        if index != -1:
            return searched_node[index]
        return dict(id='')

    def move_item(self, dragged_node: LiszNode, dragged_id: str,
                  dropped_path: Optional[List[str]] = None, dropped_id: str = '') -> bool:
        """ move item id from passed dragged_node to the node and index specified by dropped_path and dropped_id.

        :param dragged_node:    node where the item got dragged/moved from.
        :param dragged_id:      id of the dragged/moved item.
        :param dropped_path:    optional destination/drop node path, if not passed use dragged_node.
        :param dropped_id:      optional destination item where the dragged item will be moved before it.
                                if empty string passed or not passed then the item will be placed at the end of
                                the destination node.
        """
        if dropped_path is None:
            dropped_node = dragged_node
        else:
            dropped_node = self.flow_path_node(dropped_path)

        src_node_idx = self.find_item_index(dragged_id, searched_node=dragged_node)
        dst_node_idx = self.find_item_index(dropped_id, searched_node=dropped_node) if dropped_id else len(dropped_node)
        assert src_node_idx >= 0 and dst_node_idx >= 0

        if dragged_node != dropped_node and self.find_item_index(dragged_id, searched_node=dropped_node) != -1:
            self.play_sound('error')
            return False

        nid = dragged_node.pop(src_node_idx)
        if dragged_node == dropped_node and dst_node_idx > src_node_idx:
            dst_node_idx -= 1
        dropped_node.insert(dst_node_idx, nid)

        return True

    def on_app_init(self):
        """ initialize self.current_node_items from flow_id/flow_path saved on last app stop. """
        self.refresh_current_node_items_from_flow_path()

    def on_app_state_root_node_save(self, root_node: LiszNode) -> LiszNode:
        """ shrink root_node app state variable before it get saved to the config file. """
        self.shrink_node_size(root_node)
        return root_node

    def on_filter_toggle(self, toggle_attr: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ toggle filter on click of either the selected or the unselected filter button.

        Note that the inverted filter may be toggled to prevent both filters active.

        :param toggle_attr:     specifying the filter button to toggle, either 'filter_selected' or 'filter_unselected'.
        :param _event_kwargs:   unused.
        :return:                True to process flow id change.
        """
        # inverted filter will be set to False if was True and toggled filter get changed to True.
        invert_attr = 'filter_unselected' if toggle_attr == 'filter_selected' else 'filter_selected'

        filtering = not getattr(self, toggle_attr)
        self.change_app_state(toggle_attr, filtering)
        if filtering and getattr(self, invert_attr):
            self.change_app_state(invert_attr, False)

        self.play_sound(f'filter_{"on" if filtering else "off"}')
        self.refresh_node_widgets()

        return True

    def on_key_press(self, modifiers: str, key_code: str) -> bool:
        """  check key press event for to be handled and processed as command/action.

        :param modifiers:       modifier keys string.
        :param key_code:        key code string.
        :return:                True if key event got processed/used, else False.
        """
        if key_code == 'r':
            if modifiers == 'Shift':
                self.change_app_state('flow_path', [])  # quick jump to root (also repairing any flow path errors)
                self.change_app_state('flow_id', '')
            self.refresh_all()
            return True

        if modifiers or flow_action(self.flow_id) not in ('', 'focus'):
            return False

        # handle hot key without a modifier key and while in item list, first current item flow changes
        flo_key = flow_key(self.flow_id)
        if key_code == 'up':
            self.focus_neighbour_item(-1)
        elif key_code == 'down':
            self.focus_neighbour_item(1)
        elif key_code == 'pgup':
            self.focus_neighbour_item(-15)
        elif key_code == 'pgdown':
            self.focus_neighbour_item(15)
        elif key_code == 'home':
            self.focus_neighbour_item(-999999)
        elif key_code == 'end':
            self.focus_neighbour_item(999999)

        # toggle selection of current item
        elif key_code == ' ' and flo_key:    # key string 'space' is not in Window.command_keys
            self.change_flow(id_of_flow('toggle', 'item_sel', flo_key))

        # enter/leave flow in current list
        elif key_code in ('enter', 'right') and flo_key and 'node' in self.item_by_id(flo_key):
            self.change_flow(id_of_flow('enter', 'item', flo_key))
        elif key_code in ('escape', 'left') and self.flow_path:
            self.change_flow(id_of_flow('leave', 'item'))

        # item processing: add, edit or request confirmation of deletion of current item
        elif key_code in ('a', '+'):
            self.change_flow(id_of_flow('add', 'item'))

        elif key_code == 'e' and flo_key:
            self.change_flow(replace_flow_action(self.flow_id, 'edit'))  # popup_kwargs=dict(parent=self.framework_win))

        elif key_code in ('-', 'del') and flo_key:
            self.change_flow(id_of_flow('confirm', 'item_deletion', flo_key))

        else:
            return False    # pressed key not processable in the current flow/app-state

        return True         # key press processed

    def on_item_enter(self, _key: str, _event_kwargs: dict) -> bool:
        """ entering sub node from current node.

        :param _key:            flow key (item id).
        :param _event_kwargs:   event kwargs.
        :return:                True for to process/change flow id.
        """
        self.play_sound(id_of_flow('enter', 'item'))
        return True

    def on_item_leave(self, _key: str, _event_kwargs: dict) -> bool:
        """ leaving sub node, setting current node to parent node.

        :param _key:            flow key (item id).
        :param _event_kwargs:   event kwargs.
        :return:                True for to process/change flow id.
        """
        self.play_sound(id_of_flow('leave', 'item'))
        return True

    def on_item_sel_toggle(self, item_id: str, event_kwargs: dict) -> bool:
        """ toggle selection of leaf item.

        :param item_id:         item id of the leaf to toggle selection for.
        :param event_kwargs:    event kwargs.
        :return:                True for to process/change flow id.
        """
        self.toggle_item_sel(self.find_item_index(item_id))
        event_kwargs['flow_id'] = id_of_flow('focus', 'item', item_id)
        return True

    def on_item_sel_change(self, item_id: str, event_kwargs: dict) -> bool:
        """ toggle, set or reset in the current node the selection of a leaf item or of the sub-leaves of a node item.

        :param item_id:         item id of the leaf to toggle selection for.
        :param event_kwargs:    event kwargs, containing a `set_sel_to` key with a boolean value, where
                                True will select and False deselect the item (or the sub-items if the item is a
                                non-empty sub-node).
        :return:                True for to process/change flow id.

        This flow change event can be used alternatively to :meth:`~LiszDataMixin.on_item_sel_toggle`
        for more sophisticated Lisz app implementations, like e.g. the
        `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`__ .
        """
        node_idx = self.find_item_index(item_id)
        set_sel_to = event_kwargs['set_sel_to']
        node = self.current_node_items[node_idx].get('node', list())
        if node:
            self.change_sub_node_sel(node, set_sel_to)
        else:
            # assert not set_sel_to == bool(self.current_node_items[node_idx].get('sel', 0))
            self.toggle_item_sel(node_idx)
        event_kwargs['flow_id'] = id_of_flow('focus', 'item', item_id)
        return True

    def on_node_jump(self, flow_path_text: str, event_kwargs: dict) -> bool:
        """ FlowButton clicked event handler restoring flow path from the flow key.

        Used for to jump to node specified by the flow path text in the passed flow_id key.

        :param flow_path_text:  flow path text (identifying where to jump to).
        :param event_kwargs:    event arguments (used for to reset flow id).
        :return:                True for to process/change flow.
        """
        flow_path = self.flow_path_from_text(flow_path_text)

        # cannot close popup here because the close event will be processed in the next event loop
        # an because flow_path_from_text() is overwriting the open popup action in self.flow_path
        # we have to re-add the latest flow id entry from the current/old flow path that opened the jumper
        # here (for it can be removed by FlowPopup closed event handler when the jumper popup closes).
        # open_jumper_flow_id = id_of_flow('open', 'flow_path_jumper')
        # assert open_jumper_flow_id == self.flow_path[-1]
        flow_path.append(self.flow_path[-1])

        self.change_app_state('flow_path', flow_path, send_event=False)
        event_kwargs['flow_id'] = id_of_flow('', '')
        self.play_sound(id_of_flow('enter', 'item'))

        return True

    def refresh_all(self):
        """ refresh currently displayed items after changing current node. """
        assert not self._refreshing_data
        self._refreshing_data = True
        try:
            if self.debug_level:
                self.play_sound('debug_draw')

            self.refresh_current_node_items_from_flow_path()

            # save last actual flow id (because refreshed/redrawn widget observers could change flow id via focus)
            flow_id = self.flow_id

            self.refresh_node_widgets()

            if flow_action(flow_id) == 'focus':
                item_idx = self.find_item_index(flow_key(flow_id))
                if item_idx not in self.filtered_indexes:
                    flow_id = id_of_flow('', '')  # reset flow id because last focused item got filtered/deleted by user

            self.change_app_state('flow_id', flow_id, send_event=False)     # correct flow or restore silently

            if flow_action(flow_id) == 'focus':
                self.call_method('on_flow_widget_focused')                  # restore focus
        finally:
            assert self._refreshing_data
            self._refreshing_data = False

    def refresh_current_node_items_from_flow_path(self):
        """ refresh current node including the depending display node. """
        self.current_node_items = self.flow_path_node()

    def shrink_node_size(self, node: LiszNode):
        """ shrink size of node and sub-node keys by removing unneeded `sel` keys, for to save space in config file.

        :param node:            start or root node to shrink.
        """
        for item in node:
            if item.get('sel', 1) != 1:
                item.pop('sel')
            elif 'sel' in item:
                item['sel'] = 1  # remove also decimal point and zero (float to int)
            if 'node' in item:
                self.shrink_node_size(item['node'])

    def sub_item_ids(self, item_id: str, leaves_only: bool, hide_sel_val: Optional[bool] = None,
                     node: Optional[LiszNode] = None, sub_ids: Optional[List[str]] = None) -> List[str]:
        """ return item names of all items including their sub-node items (if exists).

        Used for to determine the affected items if user want to delete or de-/select the sub-items of
        the node item specified by the :paramref:`sub_item_ids.item_id` argument.

        :param item_id:         item id of the node item to be investigated (for to be deleted or de-/selected later).
        :param leaves_only:     True if only include the leaf item ids of the sub-nodes of the node item.
        :param hide_sel_val:    pass False/True for to exclude un-/selected items from the returned list of ids.
                                If None or not passed then all found items will be included.
        :param node:            searched node, use current node if not passed (used for recursive calls of this method).
        :param sub_ids:         already found sub item ids (used only for the recursive calls of this method).
        :return:                list of found item ids.
        """
        if node is None:
            node = self.current_node_items
        if sub_ids is None:
            sub_ids = list()

        item = self.item_by_id(item_id, node)

        if not leaves_only and (hide_sel_val is None or bool(item.get('sel')) != hide_sel_val):
            sub_ids.append(item_id)

        node = item.get('node')
        if node is not None:
            for item in node:
                if item.get('node'):
                    self.sub_item_ids(item['id'], leaves_only, hide_sel_val=hide_sel_val, node=node, sub_ids=sub_ids)
                elif hide_sel_val is None or bool(item.get('sel')) != hide_sel_val:
                    sub_ids.append(item['id'])

        return sub_ids

    def toggle_item_sel(self, node_idx: int):
        """ toggle the item selection of the item identified by the list index in the current node.

        :param node_idx:            list index of the item in the current node to change the selection for.
        """
        selected = self.current_node_items[node_idx].get('sel', False)
        if selected:
            self.current_node_items[node_idx].pop('sel')
        else:
            self.current_node_items[node_idx]['sel'] = 1.0
