"""Generate bounded preparation-only planning; never mutate dispatched slots."""
FIELDS = ('active', 'clock', 'hull', 'until', 'enemy-until', 'objective',
          'objective-count', 'seen1', 'seen2', 'seen3', 'candidate', 'valid',
          'failure', 'after-failure', 'write', 'blocked', 'zone', 'live',
          'min-x', 'max-x', 'min-y', 'max-y', 'landing-threats', 'route-threats',
          'screen-validated', 'seed-enemy', 'preferred-enemy', 'chosen-enemy',
          'enemies-tried', 'resume')
STATES = ('BEGIN', 'OBJECTIVE', 'CANDIDATE', 'CACHE', 'SAFETY', 'SAFE-CHECK',
          'FAIL', 'ADVANCE', 'NEXT-OBJECTIVE', 'OBJECTIVE-FAILED',
          'ENEMY-FAILED', 'NEXT-ENEMY', 'ENEMY-SEARCH', 'TERMINAL', 'FINAL-SAFETY')
MEMORY = 16
APPROACHES = (0, 28, -28, 56, -56)


def rule(facts, actions):
    return '(defrule\n\t' + '\n\t'.join(facts) + '\n=>\n\t' + '\n\t'.join(actions) + '\n)'


def definitions():
    out = [';Generated failed-approach memory and singleton preparation planner.']
    out += [f'(defconst gl-ap-{key} {15000+i})' for i, key in enumerate(FIELDS)]
    for p in range(1, 9):
        out += [f'(defconst gl-ap-enemy{p}-{key} {15100+p*4+i})'
                for i, key in enumerate(('failures', 'until', 'visited'))]
    for slot in range(1, MEMORY+1):
        out += [f'(defconst gl-ap-memory{slot}-{key} {15200+slot*8+i})'
                for i, key in enumerate(('enemy', 'objective', 'x', 'y', 'reason', 'until'))]
    out += [f'(defconst AP-{key} {120+i})' for i, key in enumerate(STATES)]
    out += ['(defconst AP-RETRY-SECONDS 300)', '(defconst AP-ENEMY-SECONDS 180)',
            '(defconst AP-MISSION-SECONDS 360)']
    for key in ('hull', 'enemy', 'objective', 'x', 'y', 'reason', 'retry', 'next-enemy'):
        out.append(f'(defconst str-ap-{key} "RAW plan {key}: %d")')
    return '\n'.join(out) + '\n'


def seed_rules():
    """Fresh admission snapshot; never writes the mutable strategic target SN."""
    out = [rule(['(true)'], ['(set-goal gl-ap-seed-enemy -1)',
                            '(up-modify-goal gl-ap-chosen-enemy s:= sn-target-player-number)'])]
    for p in range(1, 9):
        until = f'gl-ap-enemy{p}-until'
        out.append(rule([f'(up-compare-goal {until} c:> 0)',
                         f'(up-compare-goal gl-assault-mission-clock g:>= {until})'],
                        [f'(set-goal {until} 0)', f'(set-goal gl-ap-enemy{p}-failures 0)']))
    for choice in ('gl-ap-preferred-enemy', 'gl-ap-chosen-enemy', None):
        for p in range(1, 9):
            facts = ['(goal gl-ap-seed-enemy -1)', f'(player-in-game {p})',
                     f'(stance-toward {p} enemy)',
                     f'(up-compare-goal gl-assault-mission-clock g:>= gl-ap-enemy{p}-until)']
            if choice: facts += [f'(goal {choice} {p})']
            out.append(rule(facts, [f'(set-goal gl-ap-seed-enemy {p})']))
    return '\n\n'.join(out)


def plans():
    out = [';Generated loaded-assault planner. Only preparation owns this state.',
           ';Reasons: screening2/4/6/7/8/10/11;21 topology;22 total budget;',
           ';23 enemy budget;24 invalid hull/manifest;26 no alternative enemy;',
           ';27 maximum opponents tried;28 enemy unavailable;29 no longer hostile.',
           ';32 fallback danger;33 fallback topology;35 fallback Scout invalid.',
           ';after-failure:0 next approach,2 next enemy,3 terminal recovery.',
           ';A failed beach is excluded. Different beaches require fresh checks.']
    def emit(f, a): out.append(rule(f, a))
    def state(s): return f'(goal gl-transport-route-state {s})'
    def go(s): return f'(set-goal gl-transport-route-state {s})'
    def active(): return ['(goal gl-ap-active YES)']
    def cp(dst, src): return f'(up-modify-goal {dst} g:= {src})'
    def deadline(dst, seconds): return [cp(dst, 'gl-ap-clock'), f'(up-modify-goal {dst} c:+ {seconds})']
    def select_hull():
        return ['(up-full-reset-search)', '(up-add-object-by-id search-local g: gl-transport-route-id)',
                '(up-remove-objects search-local object-data-player != my-player-number)',
                '(up-remove-objects search-local object-data-group-flag != attack-transport-group)']
    def release_screen():
        return ['(up-full-reset-search)', '(up-add-object-by-id search-local g: gl-transport-screen-id)',
                ';OWNERSHIP command: transport-screen-group.',
                '(up-remove-objects search-local object-data-player != my-player-number)',
                '(up-remove-objects search-local object-data-group-flag != transport-screen-group)',
                '(up-target-point gl-transport-route-origin-x action-move -1 stance-no-attack)',
                '(up-create-group 0 0 c: transport-screen-group)',
                '(up-modify-group-flag 0 c: transport-screen-group)',
                '(up-reset-group c: transport-screen-group)', '(set-goal gl-transport-screen-id -1)',
                '(set-goal gl-transport-screen-waits 0)']
    def find_objectives(same_zone):
        a = ['(up-modify-sn sn-focus-player-number g:= gl-assault-manifest-player)',
             '(up-full-reset-search)', '(up-set-target-point gl-transport-route-target-x)']
        a += [f'(up-find-remote c: {kind} c: 20)' for kind in
              ('town-center', 'market', 'barracks', 'archery-range', 'stable', 'siege-workshop', 'castle', 'house')]
        a += ['(up-remove-objects search-remote object-data-player g:!= gl-assault-manifest-player)',
              '(up-remove-objects search-remote object-data-hitpoints <= 0)']
        if same_zone:
            a += ['(up-remove-objects search-remote object-data-map-zone-id g:!= gl-transport-route-target-zone)',
                  '(up-remove-objects search-remote object-data-distance < 24)']
        a += [f'(up-remove-objects search-remote object-data-id g:== gl-ap-seen{i})' for i in (1, 2, 3)]
        return a + ['(up-clean-search search-remote object-data-distance search-order-asc)']
    emit(['(true)'], ['(set-goal gl-ap-active NO)', '(set-goal gl-ap-write 1)',
                     '(set-goal gl-ap-preferred-enemy -1)',
                     *[f'(set-goal gl-ap-memory{i}-until 0)' for i in range(1, MEMORY+1)],
                     '(disable-self)'])
    emit(['(true)'], ['(up-get-fact game-time 0 gl-ap-clock)'])
    for s in ('TRANSPORT-ROUTE-IDLE', 'TRANSPORT-ROUTE-RECOVERY-WAIT', 'TRANSPORT-ROUTE-OWNER-LOST', '101'):
        emit([state(s)], ['(set-goal gl-ap-active NO)'])
    # Existing FIND has already resolved/owned the accepted hull and enemy anchor.
    # Scripted admission selected an overseas objective. Preserve that exact
    # objective across loading instead of replacing it with the closest home-zone
    # TC of the same opponent. If it disappeared, explicitly replan the load.
    emit([state('TRANSPORT-ROUTE-TARGET'), '(goal gl-transport-route-script-load YES)'], [
        '(up-full-reset-search)',
        '(up-add-object-by-id search-remote g: gl-assault-admission-objective)',
        '(up-remove-objects search-remote object-data-player g:!= gl-assault-manifest-player)',
        '(up-remove-objects search-remote object-data-hitpoints <= 0)',
        '(up-remove-objects search-remote object-data-map-zone-id < 0)',
        '(up-remove-objects search-remote object-data-map-zone-id g:== gl-home-zone)'])
    emit([state('TRANSPORT-ROUTE-TARGET')], [
        '(set-goal gl-ap-active YES)', cp('gl-ap-hull', 'gl-transport-route-id'),
        *deadline('gl-ap-until', 'AP-MISSION-SECONDS'), *deadline('gl-ap-enemy-until', 'AP-ENEMY-SECONDS'),
        '(set-goal gl-ap-enemies-tried 1)', '(set-goal gl-ap-objective-count 0)',
        '(set-goal gl-ap-seen1 -1)', '(set-goal gl-ap-seen2 -1)', '(set-goal gl-ap-seen3 -1)',
        '(set-goal gl-ap-objective -1)', '(set-goal gl-ap-valid NO)', '(set-goal gl-ap-after-failure 0)',
        *[f'(set-goal gl-ap-enemy{i}-visited NO)' for i in range(1, 9)], go('AP-BEGIN')])
    emit([state('AP-BEGIN'), '(up-set-target-object search-remote c: 0)'], [
        '(up-get-object-data object-data-id gl-ap-objective)',
        '(up-get-point position-object gl-transport-route-target-x)'])
    emit([state('AP-BEGIN'), '(goal gl-transport-route-script-load YES)',
          '(not (up-set-target-object search-remote c: 0))'],
         ['(set-goal gl-ap-failure 30)',
          '(up-chat-data-to-all str-ap-hull g: gl-transport-route-id)',
          '(up-chat-data-to-all str-ap-reason g: gl-ap-failure)',
          '(up-chat-data-to-all str-ap-objective g: gl-assault-admission-objective)',
          go('AP-ENEMY-SEARCH')])
    emit([state('AP-BEGIN')], [go('AP-OBJECTIVE')])
    # Guard ALL loaded preparation/wait states, not just the initial load.
    emit(active(), ['(set-goal gl-ap-live NO)'])
    for p in range(1, 9):
        emit([*active(), f'(goal gl-assault-manifest-player {p})', f'(player-in-game {p})',
              f'(stance-toward {p} enemy)'], ['(set-goal gl-ap-live YES)'])
    emit([*active(), '(goal gl-ap-live NO)'], ['(set-goal gl-ap-failure 28)'])
    for p in range(1,9):
        emit([*active(), f'(goal gl-assault-manifest-player {p})', f'(player-in-game {p})',
              f'(not (stance-toward {p} enemy))'], ['(set-goal gl-ap-failure 29)'])
    emit([*active(), '(goal gl-ap-live NO)'], [
        '(up-chat-data-to-all str-ap-hull g: gl-transport-route-id)',
        '(up-chat-data-to-all str-ap-enemy g: gl-assault-manifest-player)',
        '(up-chat-data-to-all str-ap-reason g: gl-ap-failure)',go('AP-NEXT-ENEMY')])
    emit(active(), select_hull())
    emit([*active(), '(not (up-set-target-object search-local c: 0))'],
         ['(set-goal gl-ap-active NO)', go('TRANSPORT-ROUTE-OWNER-LOST')])
    hull_bad = ('(or (up-compare-goal gl-ap-hull g:!= gl-transport-route-id)\n'
                '\t(or (up-compare-goal gl-assault-manifest-hull g:!= gl-transport-route-id)\n'
                '\t(or (up-compare-goal gl-assault-manifest-count c:< 5)\n'
                '\t(or (up-object-data object-data-garrison-count g:< gl-assault-manifest-count)\n'
                '\t(or (up-object-data object-data-hitpoints <= 0)\n'
                '\t(up-object-data object-data-under-attack > 0))))))')
    emit([*active(), '(up-set-target-object search-local c: 0)', hull_bad],
         ['(set-goal gl-ap-failure 24)', go('AP-TERMINAL')])
    for timer, reason, after in (('gl-ap-until', 22, 3), ('gl-ap-enemy-until', 23, 2)):
        emit([*active(), '(goal gl-ap-after-failure 0)', f'(up-compare-goal gl-ap-clock g:>= {timer})',
              f'(not {state("AP-TERMINAL")})', f'(not {state("AP-NEXT-ENEMY")})'],
             [f'(set-goal gl-ap-failure {reason})', f'(set-goal gl-ap-after-failure {after})', go('AP-FAIL')])
    emit([state('AP-OBJECTIVE')], [
        '(set-goal gl-transport-route-target-zone -1)',
        '(up-get-point-zone gl-transport-route-target-x gl-transport-route-target-zone)',
        '(up-modify-goal gl-ap-objective-count c:+ 1)', '(set-goal gl-ap-candidate 0)',
        '(set-goal gl-ap-valid NO)', cp('gl-ap-preferred-enemy', 'gl-assault-manifest-player')])
    for i in (1, 2, 3):
        emit([state('AP-OBJECTIVE'), f'(goal gl-ap-objective-count {i})'],
             [cp(f'gl-ap-seen{i}', 'gl-ap-objective')])
    for p in range(1, 9):
        emit([state('AP-OBJECTIVE'), f'(goal gl-assault-manifest-player {p})'],
             [f'(set-goal gl-ap-enemy{p}-visited YES)'])
    emit([state('AP-OBJECTIVE')], [go('AP-CANDIDATE')])
    emit([state('AP-CANDIDATE'), f'(up-compare-goal gl-ap-candidate c:>= {len(APPROACHES)})'],
         [go('AP-OBJECTIVE-FAILED')])
    for i, offset in enumerate(APPROACHES):
        emit([state('AP-CANDIDATE'), f'(goal gl-ap-candidate {i})'], [
            '(up-bound-point gl-transport-route-landing-x gl-transport-route-target-x)',
            *([f'(up-cross-tiles gl-transport-route-landing-x gl-transport-route-origin-x c: {offset})'] if offset else []),
            '(set-goal gl-ap-zone -1)', '(up-get-point-zone gl-transport-route-landing-x gl-ap-zone)',
            '(set-goal gl-ap-valid YES)', '(set-goal gl-ap-blocked NO)',
            cp('gl-ap-min-x', 'gl-transport-route-landing-x'), '(up-modify-goal gl-ap-min-x c:- 12)',
            cp('gl-ap-max-x', 'gl-transport-route-landing-x'), '(up-modify-goal gl-ap-max-x c:+ 12)',
            cp('gl-ap-min-y', 'gl-transport-route-landing-y'), '(up-modify-goal gl-ap-min-y c:- 12)',
            cp('gl-ap-max-y', 'gl-transport-route-landing-y'), '(up-modify-goal gl-ap-max-y c:+ 12)', go('AP-CACHE')])
    # Matching by beach also prevents a different objective evading the exclusion.
    for i in range(1, MEMORY+1):
        v = lambda key: f'gl-ap-memory{i}-{key}'
        emit([state('AP-CACHE'), f'(up-compare-goal {v("enemy")} g:== gl-assault-manifest-player)',
              f'(up-compare-goal gl-ap-clock g:< {v("until")})',
              f'(up-compare-goal {v("x")} g:>= gl-ap-min-x)', f'(up-compare-goal {v("x")} g:<= gl-ap-max-x)',
              f'(up-compare-goal {v("y")} g:>= gl-ap-min-y)', f'(up-compare-goal {v("y")} g:<= gl-ap-max-y)'],
             ['(set-goal gl-ap-blocked YES)'])
    emit([state('AP-CACHE'), '(goal gl-ap-blocked YES)'], [go('AP-ADVANCE')])
    emit([state('AP-CACHE'), '(or (up-compare-goal gl-transport-route-target-zone c:< 0)\n'
          '\t(up-compare-goal gl-ap-zone g:!= gl-transport-route-target-zone))'],
         ['(set-goal gl-ap-failure 21)', go('AP-FAIL')])
    emit([state('AP-CACHE')], ['(set-goal gl-ap-screen-validated NO)',
        '(up-modify-sn sn-focus-player-number g:= gl-assault-manifest-player)',
        go('TRANSPORT-ROUTE-CORRIDOR-PREPARE')])
    # Check all enemies before exposing the Scout AND after its successful screen.
    emit([*active(), state('TRANSPORT-ROUTE-SCREEN-FIND'), '(goal gl-ap-screen-validated NO)'],
         ['(set-goal gl-ap-resume TRANSPORT-ROUTE-SCREEN-FIND)', go('AP-SAFETY')])
    emit([*active(), state('AP-FINAL-SAFETY')],
         ['(set-goal gl-ap-resume TRANSPORT-ROUTE-DEPARTURE-START)', go('AP-SAFETY')])
    emit([state('AP-SAFETY')], ['(set-goal gl-ap-landing-threats 0)', '(set-goal gl-ap-route-threats 0)'])
    for p in range(1, 9):
        a = [f'(set-strategic-number sn-focus-player-number {p})']
        for point, count in (('landing', 'landing'), ('waypoint', 'route')):
            a += ['(up-full-reset-search)', f'(up-set-target-point gl-transport-route-{point}-x)',
                  '(up-filter-distance c: -1 c: 20)']
            a += [f'(up-find-remote c: {kind} c: 40)' for kind in ('tower-class', 'sea-tower', 'castle', 'town-center')]
            a += ['(up-get-search-state local-total)', f'(up-modify-goal gl-ap-{count}-threats g:+ remote-total)']
        emit([state('AP-SAFETY'), f'(player-in-game {p})', f'(stance-toward {p} enemy)'], a)
    emit([state('AP-SAFETY')], ['(up-modify-sn sn-focus-player-number g:= gl-transport-route-focus)', go('AP-SAFE-CHECK')])
    for count, reason in (('landing', 11), ('route', 7)):
        emit([state('AP-SAFE-CHECK'), f'(up-compare-goal gl-ap-{count}-threats c:> 0)'],
             [f'(set-goal gl-ap-failure {reason})', go('AP-FAIL')])
    emit([state('AP-SAFE-CHECK')], ['(set-goal gl-ap-screen-validated YES)',
        '(up-set-timer c: t-transport-route c: 1)', cp('gl-transport-route-state', 'gl-ap-resume')])
    # Exactly one event/record; no hull or passenger order on a replan.
    emit([state('AP-FAIL')], [*release_screen(),
        '(up-modify-sn sn-focus-player-number g:= gl-transport-route-focus)',
        '(set-goal gl-assault-fallback-deadline 0)', '(set-goal gl-assault-fallback-progress-deadline 0)',
        '(set-goal gl-ap-screen-validated NO)',
        '(up-chat-data-to-all str-ap-hull g: gl-transport-route-id)',
        '(up-chat-data-to-all str-ap-enemy g: gl-assault-manifest-player)',
        '(up-chat-data-to-all str-ap-objective g: gl-ap-objective)',
        '(up-chat-data-to-all str-ap-x g: gl-transport-route-landing-x)',
        '(up-chat-data-to-all str-ap-y g: gl-transport-route-landing-y)',
        '(up-chat-data-to-all str-ap-reason g: gl-ap-failure)'])
    emit([state('AP-FAIL'), '(goal gl-ap-valid NO)'], [go('AP-ADVANCE')])
    for i in range(1, MEMORY+1):
        v = lambda key: f'gl-ap-memory{i}-{key}'
        emit([state('AP-FAIL'), f'(goal gl-ap-write {i})'], [
            cp(v('enemy'), 'gl-assault-manifest-player'), cp(v('objective'), 'gl-ap-objective'),
            cp(v('x'), 'gl-transport-route-landing-x'), cp(v('y'), 'gl-transport-route-landing-y'),
            cp(v('reason'), 'gl-ap-failure'), *deadline(v('until'), 'AP-RETRY-SECONDS'),
            f'(up-chat-data-to-all str-ap-retry g: {v("until")})',
            f'(set-goal gl-ap-write {i % MEMORY + 1})', go('AP-ADVANCE')])
    emit([state('AP-ADVANCE'), '(goal gl-ap-after-failure 3)'], [go('AP-TERMINAL')])
    emit([state('AP-ADVANCE'), '(goal gl-ap-after-failure 2)'], [go('AP-ENEMY-FAILED')])
    emit([state('AP-ADVANCE')], ['(up-modify-goal gl-ap-candidate c:+ 1)', go('AP-CANDIDATE')])
    # One exhausted objective is one plan failure, not one rule evaluation.
    for p in range(1, 9):
        emit([state('AP-OBJECTIVE-FAILED'), f'(goal gl-assault-manifest-player {p})'],
             [f'(up-modify-goal gl-ap-enemy{p}-failures c:+ 1)'])
        emit([state('AP-OBJECTIVE-FAILED'), f'(goal gl-assault-manifest-player {p})',
              f'(up-compare-goal gl-ap-enemy{p}-failures c:>= 3)'], [go('AP-ENEMY-FAILED')])
    emit([state('AP-OBJECTIVE-FAILED'), '(up-compare-goal gl-ap-objective-count c:>= 3)'], [go('AP-ENEMY-FAILED')])
    emit([state('AP-OBJECTIVE-FAILED')], [go('AP-NEXT-OBJECTIVE')])
    emit([state('AP-NEXT-OBJECTIVE')], find_objectives(True))
    emit([state('AP-NEXT-OBJECTIVE'), '(up-set-target-object search-remote c: 0)'], [
        '(up-get-object-data object-data-id gl-ap-objective)',
        '(up-get-point position-object gl-transport-route-target-x)', go('AP-OBJECTIVE')])
    emit([state('AP-NEXT-OBJECTIVE')], [go('AP-ENEMY-FAILED')])
    for p in range(1, 9):
        emit([state('AP-ENEMY-FAILED'), f'(goal gl-assault-manifest-player {p})'], [
            *deadline(f'gl-ap-enemy{p}-until', 'AP-RETRY-SECONDS'),
            f'(set-goal gl-ap-enemy{p}-visited YES)', '(set-goal gl-ap-preferred-enemy -1)'])
    emit([state('AP-ENEMY-FAILED')], [go('AP-NEXT-ENEMY')])
    emit([state('AP-NEXT-ENEMY')], [*release_screen(), '(set-goal gl-ap-chosen-enemy -1)'])
    for p in range(1, 9):
        emit([state('AP-NEXT-ENEMY'), '(goal gl-ap-chosen-enemy -1)', f'(player-in-game {p})',
              f'(stance-toward {p} enemy)', f'(goal gl-ap-enemy{p}-visited NO)',
              f'(up-compare-goal gl-ap-clock g:>= gl-ap-enemy{p}-until)'],
             [f'(set-goal gl-ap-chosen-enemy {p})'])
    for condition, reason in (('(up-compare-goal gl-ap-clock g:>= gl-ap-until)',22),
                              ('(up-compare-goal gl-ap-enemies-tried c:>= 3)',27),
                              ('(goal gl-ap-chosen-enemy -1)',26)):
        emit([state('AP-NEXT-ENEMY'),condition],
             [f'(set-goal gl-ap-failure {reason})',go('AP-TERMINAL')])
    emit([state('AP-NEXT-ENEMY')], [
        cp('gl-assault-manifest-player', 'gl-ap-chosen-enemy'), cp('gl-ap-preferred-enemy', 'gl-ap-chosen-enemy'),
        '(up-chat-data-to-all str-ap-hull g: gl-transport-route-id)',
        '(up-chat-data-to-all str-ap-next-enemy g: gl-assault-manifest-player)',
        '(up-modify-goal gl-ap-enemies-tried c:+ 1)', *deadline('gl-ap-enemy-until', 'AP-ENEMY-SECONDS'),
        '(set-goal gl-ap-after-failure 0)', '(set-goal gl-ap-objective-count 0)',
        '(set-goal gl-ap-valid NO)', '(set-goal gl-ap-seen1 -1)', '(set-goal gl-ap-seen2 -1)', '(set-goal gl-ap-seen3 -1)',
        '(up-modify-sn sn-focus-player-number g:= gl-assault-manifest-player)',
        '(up-get-point position-focus gl-transport-route-target-x)', go('AP-ENEMY-SEARCH')])
    emit([state('AP-ENEMY-SEARCH')], find_objectives(False))
    emit([state('AP-ENEMY-SEARCH'), '(goal gl-transport-route-script-load YES)'], [
        '(up-remove-objects search-remote object-data-map-zone-id < 0)',
        '(up-remove-objects search-remote object-data-map-zone-id g:== gl-home-zone)'])
    emit([state('AP-ENEMY-SEARCH'), '(up-set-target-object search-remote c: 0)'], [
        '(up-get-object-data object-data-id gl-ap-objective)',
        '(up-get-point position-object gl-transport-route-target-x)', go('AP-OBJECTIVE')])
    emit([state('AP-ENEMY-SEARCH')], [go('AP-ENEMY-FAILED')])
    emit([state('AP-TERMINAL')], ['(set-goal gl-ap-active NO)',
        '(up-chat-data-to-all str-ap-hull g: gl-transport-route-id)',
        '(up-chat-data-to-all str-ap-reason g: gl-ap-failure)', go('TRANSPORT-ROUTE-SCREEN-RECALL')])
    return '\n\n'.join(out) + '\n'


def outputs():
    return {'rawai-assault-plan-defs.per': definitions(), 'rawai-assault-plans.per': plans()}
