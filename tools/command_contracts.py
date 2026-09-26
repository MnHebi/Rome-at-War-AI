"""Recipient/target contracts for the commands the file trace instruments.

Every rule below is taken from the cached AIRef reference
(`.analysis/airef-reference-20260830.js`, 2026-08-30) and cites the documented
action text. It is deliberately conservative: an unknown command or action is
reported as unclassified, never silently treated as a state write, and no
command claims a packet family the reference does not document.

up-target-point: recipients are the LOCAL search list; the target is the point
  ("Direct local search results to a specific point on the map"). The reference
  states action-default, action-guard, action-follow and action-garrison "will
  perform as action-move"; action-unload unloads transports at the point;
  action-stop stops; action-delete deletes.
up-target-objects: recipients are the LOCAL search list; the target is the
  REMOTE list (Option 0) or the single object set by up-set-target-object
  (Option 1). action-default is "equivalent of a right-click" on the target
  object(s); action-garrison garrisons into the target object; action-guard
  guards it; action-unload is documented as action-none.
up-set-group: "Set the local or remote search results to a search group", so a
  group-based site's recipients are whatever the trace then reads from that
  list; it does not create a hidden selection.
Type-based commands (up-garrison, up-ungarrison, up-reset-unit, delete-unit,
  delete-building) act on every object of a type and are not represented by
  either traced list. Global commands (up-retreat-now, up-send-scout,
  up-reset-scouts, up-delete-idle-units) are likewise not list-anchored.
"""
import re

LOCAL_LIST = 'local-list'
REMOTE_LIST = 'remote-list'
SELECTED_OBJECT = 'selected-object'
TYPE_BASED = 'type-based'
GLOBAL = 'global'
POINT_TARGET = 'point'
NO_TARGET = 'none'

STATE_WRITE = 'state-write'
GROUP_WRITE = 'group-write'
NATIVE_EFFECT = 'native-effect-command'
STATE_READ = 'state-read'
UNCLASSIFIED = 'unclassified'

# command + action -> (recipient source, target source, compatible packet families)
POINT_ACTIONS = {
    'action-default': ({'move', 'order'},),
    'action-move': ({'move', 'order'},),
    'action-guard': ({'move', 'order'},),
    'action-follow': ({'move', 'order'},),
    'action-garrison': ({'move', 'order'},),
    'action-patrol': ({'patrol', 'order'},),
    'action-attack-move': ({'attack-move', 'order'},),
    'action-stop': ({'stop'},),
    'action-unload': ({'unload'},),
    'action-delete': ({'delete'},),
    'action-gather': (set(),),          # sets a building gather point; no direct packet
    'action-none': (set(),),
}
OBJECT_ACTIONS = {
    # "equivalent of a right-click for all objects in the local list on the ...
    # target object(s)": resource -> work, building -> garrison/return,
    # unit -> attack/guard/follow or plain order.
    'action-default': ({'work', 'order', 'garrison', 'guard', 'follow', 'move'},),
    'action-move': ({'move', 'order'},),
    'action-patrol': ({'patrol', 'order'},),
    'action-garrison': ({'garrison'},),
    'action-guard': ({'guard', 'follow'},),
    'action-stop': ({'stop'},),
    'action-unload': (set(),),          # documented as action-none
    'action-delete': ({'delete'},),
    'action-gather': (set(),),          # sets a building gather point
    'action-none': (set(),),
}
TYPE_COMMANDS = {
    'up-garrison': ({'garrison'}, TYPE_BASED, TYPE_BASED),
    'up-ungarrison': ({'unload'}, TYPE_BASED, TYPE_BASED),
    'up-reset-unit': ({'stop'}, TYPE_BASED, TYPE_BASED),
    'delete-unit': ({'delete'}, TYPE_BASED, TYPE_BASED),
    'delete-building': ({'delete'}, TYPE_BASED, TYPE_BASED),
}
GLOBAL_COMMANDS = {
    'up-retreat-now': ({'retreat'},),
    'up-retreat-to': ({'retreat', 'move', 'order'},),
    'up-send-scout': ({'scout'},),
    'up-reset-scouts': ({'scout'},),
    'up-delete-idle-units': ({'delete'},),
}
STATE_COMMANDS = {'set-goal', 'up-modify-goal', 'up-modify-sn', 'set-strategic-number',
                  'up-set-timer', 'up-disable-timer', 'up-enable-timer', 'up-get-rule-id'}
GROUP_COMMANDS = {'up-create-group', 'up-modify-group-flag', 'up-reset-group',
                  'up-disband-group-type', 'up-set-group'}
READ_COMMANDS = {'up-get-object-data', 'up-get-search-state', 'up-get-fact',
                 'up-get-point', 'up-get-precise-time', 'up-get-point-distance',
                 'up-compare-goal'}
NATIVE_EFFECT_COMMANDS = {'up-build', 'up-build-line', 'up-assign-builders', 'build',
                          'build-forward', 'build-wall', 'build-gate', 'attack-now',
                          'up-request-hunters', 'up-find-local', 'up-find-remote',
                          'up-set-target-object', 'up-set-target-point', 'up-filter-distance',
                          'up-target-objects-grouped'}

PACKET_FAMILIES = {
    'garrison': ('SPECIAL', 5),
    'unload': ('UNGARRISON', None),
    'stop': ('STOP', None),
    'delete': ('DELETE', None),
    'work': ('WORK', None),
    'order': ('ORDER', None),
    'move': ('MOVE', None),
    'patrol': ('PATROL', None),
    'guard': ('GUARD', None),
    'follow': ('FOLLOW', None),
    'retreat': ('DE_RETREAT', None),
    'scout': ('DE_AUTOSCOUT', None),
    'attack-move': ('DE_ATTACK_MOVE', None),
}
_BY_SIGNATURE = {(action, order): family for family, (action, order) in PACKET_FAMILIES.items()}


def packet_families(packet):
    """Documented packet families of one replay packet.

    AI_ORDER 706 is the stop/idle order; any other AI_ORDER value is
    undocumented here and therefore matches no command rather than being
    guessed.
    """
    action, order = packet.get('action'), packet.get('order_id')
    if action == 'AI_ORDER':
        return {'stop'} if order == 706 else set()
    family = _BY_SIGNATURE.get((action, order))
    return {family} if family else set()


def _head(command):
    text = command.strip().strip('()').strip()
    return text.split()[0] if text else ''


def describe(command):
    """Recipient/target contract and compatible packet families for a command."""
    text = command.strip().strip('()').strip()
    head = _head(command)
    if head in ('up-target-point', 'up-target-objects'):
        parts = text.split()
        action = parts[2] if len(parts) > 2 else ''
        option = None
        if head == 'up-target-objects' and len(parts) > 1:
            try:
                option = int(parts[1])
            except ValueError:
                option = None
        table = POINT_ACTIONS if head == 'up-target-point' else OBJECT_ACTIONS
        entry = table.get(action)
        if entry is None:
            return dict(kind=UNCLASSIFIED, recipients=LOCAL_LIST, target=POINT_TARGET,
                        packets=set(), action=action,
                        note='action not documented for this command; no candidate families claimed')
        target = POINT_TARGET if head == 'up-target-point' else (
            SELECTED_OBJECT if option == 1 else REMOTE_LIST if option == 0 else UNCLASSIFIED)
        return dict(kind='duc-target', recipients=LOCAL_LIST, target=target,
                    packets=set(entry[0]), action=action, option=option,
                    note='up-target-point actions default/guard/follow/garrison behave as action-move'
                         if head == 'up-target-point' else
                         'up-target-objects action-default is a right-click on the target object(s)')
    if head in TYPE_COMMANDS:
        packets, recipients, target = TYPE_COMMANDS[head]
        return dict(kind='type-based', recipients=recipients, target=target,
                    packets=set(packets), action=None, note='acts on every object of a type')
    if head in GLOBAL_COMMANDS:
        return dict(kind='type-based', recipients=GLOBAL, target=NO_TARGET,
                    packets=set(GLOBAL_COMMANDS[head][0]), action=None,
                    note='global command; recipients are not list-anchored')
    if head in STATE_COMMANDS:
        return dict(kind=STATE_WRITE, recipients=NO_TARGET, target=NO_TARGET, packets=set(),
                    action=None, note='bookkeeping write; later native effects are separate')
    if head in GROUP_COMMANDS:
        return dict(kind=GROUP_WRITE, recipients=NO_TARGET, target=NO_TARGET, packets=set(),
                    action=None, note='search/group bookkeeping, not a recipient order')
    if head in READ_COMMANDS:
        return dict(kind=STATE_READ, recipients=NO_TARGET, target=NO_TARGET, packets=set(),
                    action=None, note='reads state; no packet of its own')
    if head in NATIVE_EFFECT_COMMANDS:
        return dict(kind=NATIVE_EFFECT, recipients=NO_TARGET, target=NO_TARGET, packets=set(),
                    action=None, note='engine-side admission; later native packets are not attributable here')
    return dict(kind=UNCLASSIFIED, recipients=UNCLASSIFIED, target=UNCLASSIFIED, packets=set(),
                action=None, note='command not classified from the reference')


def compatible(packet, command):
    """True when the packet's documented family is one this command can emit."""
    return bool(packet_families(packet) & describe(command)['packets'])


def compatible_any(packet, action_text):
    """True when any command in a rule action text is compatible with the packet."""
    for expression in re.findall(r'\([^()]*\)', action_text):
        if compatible(packet, expression):
            return True
    return False
