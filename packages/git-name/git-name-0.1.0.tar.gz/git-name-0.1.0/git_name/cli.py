import argparse

from git_name import __version__, NameGenerator


def main(args=None):
    example_text = '''examples:
    git name 90552d1
    git graph -f eighteen inventive hooks
    '''
    name_generator=NameGenerator()

    parser = argparse.ArgumentParser(
        prog='git name',
        description='convert hashes to memorable names',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('word_or_hash')
    parser.add_argument('-f', '--from', help="`from hash` flag used to denote argument is a hash.", action='store_true')
    parser.add_argument('-l', '--length', type=int, default=7, help="`hash length` (default=7) truncate the input output hash to this length")
    args = parser.parse_args(args=args)

    if args.__dict__['from']:
        print(name_generator.generate_hash_from_name(args.word_or_hash, args.length))
    else:
        print(name_generator.generate_name_from_hash(args.word_or_hash, args.length))


if __name__ == '__main__':
    main()