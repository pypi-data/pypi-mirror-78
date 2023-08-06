from slacker_game import Slacker


def main() -> None:
    """Run game."""
    with Slacker() as slacker:
        for i in iter(slacker.handle_events, False):
            slacker.update_screen()


if __name__ == '__main__':
    main()
