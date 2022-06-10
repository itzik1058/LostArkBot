import common
import fish
import chaos
import argparse
import time
import pathlib
import json
import cv2
import pyautogui


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(task=None)
    parser.add_argument('--template-path', default='templates', type=str)
    parser.add_argument('--keymap-file', default='keymap.json', type=str)
    parser.add_argument('--timeout', default=None, type=int)
    parser.add_argument('--startup-delay', default=5, type=int)
    subparsers = parser.add_subparsers()
    fish_parser = subparsers.add_parser('fish', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    fish_parser.set_defaults(task='fish')
    chaos_parser = subparsers.add_parser('chaos', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    chaos_parser.set_defaults(task='chaos')
    chaos_parser.add_argument('--skills-file', default='skills.json', type=str)
    chaos_parser.add_argument('--skill-set', default='base', type=str)
    chaos_parser.add_argument('--dungeon-time', default=65, type=int)
    args = parser.parse_args()
    if args.task is None:
        parser.print_help()
        return

    start = time.time() + args.startup_delay
    while time.time() < start:
        print(f'Bot starting in {start - time.time():03.1f}s', end='\r')
    print()

    initial_pos = pyautogui.position()
    templates = {f.stem: cv2.cvtColor(cv2.imread(str(f.absolute())), cv2.COLOR_BGR2RGB) for f in pathlib.Path(args.template_path).glob('*.png')}
    with open(args.keymap_file, 'r') as f:
        keymap = json.load(f)
    common_actions = common.CommonActions(templates, keymap)

    try:
        if args.task == 'fish':
            fish.fish(common_actions, initial_pos, args.timeout)
        elif args.task == 'chaos':
            with open(args.skills_file, 'r') as f:
                skills = json.load(f)
            chaos.chaos(common_actions, skills[args.skill_set], args.dungeon_time, args.timeout)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
